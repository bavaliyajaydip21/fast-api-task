from fastapi.testclient import TestClient
import sys
from pathlib import Path

current_dir = Path(__file__).resolve(strict=True).parent
sys.path.append(str(current_dir.parent))

from app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_filter_employee_by_status():
    response = client.get("/list_employees", params={"status": "active"})
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list) or isinstance(data, dict), "Response should be a list or dict"
    
    employees = data if isinstance(data, list) else data.get("items", [])

    for emp in employees:
        assert emp["status"] == "active"


def test_filter_employee_by_company():

    response = client.get("/list_employees", params={"company": "Test Company"})
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list) or isinstance(data, dict), "Response should be a list or dict"
    
    employees = data if isinstance(data, list) else data.get("items", [])

    assert len(employees) == 0


def test_filter_employee_by_status_not_started():

    response = client.get("/list_employees", params={"status": "not_started"})
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list) or isinstance(data, dict), "Response should be a list or dict"

    employees = data if isinstance(data, list) else data.get("items", [])

    assert len(employees) == 0

