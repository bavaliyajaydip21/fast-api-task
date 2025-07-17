# fast-api-task

## Prerequisites
> Python 3.10+ (for development)

> Docker & Docker Compose

> make installed (default on Unix systems)


## Setup Instructions

copy .env.example to .env file 
> cp .env.example .env

Update the .env with following 

```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_DB=hr_management

REDIS_HOST=redis
REDIS_PORT=6379
```

Note: Make sure no other service is running on port 5432, 6379, or 8000 to avoid port binding conflicts.


## Running Tests
Run all the test cases, including database migrations and data setup:

```
make test
```
This will:
- Start Docker containers in detached mode
- Run alembic upgrade head to migrate schema
- Execute all Pytest test cases


## Run the Application
Start the FastAPI app along with PostgreSQL and Redis:

```
make runserver
```

This will:
- Build and start all containers
- Run migrations via Alembic
- Launch the FastAPI server at http://localhost:8000


Note : i have added one dummy data in DB throgh migration file please hit the `/list_employees` api to see what data it contains. 
