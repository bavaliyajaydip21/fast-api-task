import time
import json
import os
import redis as python_redis

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from dotenv import load_dotenv
load_dotenv()


class RateLimiter:
    def __init__(self, redis_url: str, max_requests: int, period_seconds: int):
        self.max_requests = max_requests
        self.period = period_seconds
        self.redis = python_redis.from_url(redis_url, decode_responses=True)

    async def get_identifier(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        ip = forwarded.split(",")[0] if forwarded else request.client.host
        return f"ratelimit:{ip}:{request.scope['path']}"

    async def _check_rate_limit(self, key: str) -> int:
        now = time.time()
        try:
            raw_history = self.redis.get(key)
            history = json.loads(raw_history) if raw_history else []

            # Clean old timestamps
            history = [ts for ts in history if ts > now - self.period]

            if len(history) >= self.max_requests:
                retry_after = int(self.period - (now - history[0]))
                return retry_after

            history.append(now)
            pipeline = self.redis.pipeline()
            pipeline.setex(key, self.period, json.dumps(history))
            pipeline.execute()
            return 0
        except Exception as e:
            # Fallback: allow request if Redis fails
            print(f"Rate limiter error: {e}")
            return 0

    async def __call__(self, request: Request, response: Response):
        if os.environ.get("ENVIRONMENT") == "pytest":
            return

        key = await self.get_identifier(request)
        retry_after = await self._check_rate_limit(key)

        if retry_after > 0:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too Many Requests. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )
