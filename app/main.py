import os
import json
from typing import Any
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from app.schema.employee_schema import (
    ListEmployeeQueryParams,
    PageSerializer,
    EmployeeListSerializer,
)
from app.utils.filter_helper import DynamicColumnFilterHelper, EmployeeFilterHelper
from app.rate_limiter.custom_rate_limiter import RateLimiter
from app.utils.dynamic_colums_utils import TransformerDynamicColumn

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = RateLimiter(
    redis_url="redis://{redis_host}:{redis_port}/{redis_db}".format(
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=os.getenv("REDIS_PORT", 6379),
        redis_db=os.getenv("REDIS_DB", 7),
    ),
    max_requests=2,
    period_seconds=10, 
)

transformer_dynamic_column = TransformerDynamicColumn()

# health check endpoint
@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# list employee endpoint
@app.get(
    "/list_employees",
    response_model=PageSerializer,
    status_code=200,
    response_model_exclude_none=True,
)
async def list_employee(
    query_params: ListEmployeeQueryParams = Depends(),
    _: Any = Depends(rate_limiter),
):
    """Get list of employee"""

    employees = EmployeeFilterHelper().filter_employees(query_params)
    paginated_employees = employees.limit(query_params.limit).offset(query_params.offset)
    items = EmployeeListSerializer.model_validate(paginated_employees).model_dump()
    final_items = transformer_dynamic_column(items, query_params.company)

    response = {
        "items": final_items,
        "limit": query_params.limit,
        "offset": query_params.offset,
        "total": employees.count(),
    }

    return Response(content=json.dumps(response), media_type="application/json")