# Dockerfile

FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Set PYTHONPATH so 'from app.main import app' works
ENV PYTHONPATH=/code

# Default command (can override via docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
