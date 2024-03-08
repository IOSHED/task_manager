
import pytest
from datetime import datetime

from app.infra.postgres.models.task import Task


@pytest.fixture
def task_data():
    return {
        "id": 1,
        "id_template": None,
        "name": "Test Task",
        "description": None,
        "create_by": 1,
        "created_at": datetime.utcnow()
    }


def test_task_repr(task_data):
    task = Task(**task_data)
    assert repr(task) == f"Task(id={task_data['id']!r}, name={task_data['name']!r})"


def test_task_to_read_model(task_data):
    task = Task(**task_data)
    task_schema = task.to_read_model()
    assert task_schema.id == task_data["id"]
    assert task_schema.id_template == task_data["id_template"]
    assert task_schema.name == task_data["name"]
    assert task_schema.description == task_data["description"]
    assert task_schema.create_by == task_data["create_by"]
    assert task_schema.created_at == task_data["created_at"]


def test_task_init(task_data):
    task = Task(**task_data)
    assert task.id == task_data["id"]
    assert task.id_template == task_data["id_template"]
    assert task.name == task_data["name"]
    assert task.description == task_data["description"]
    assert task.create_by == task_data["create_by"]
    assert task.created_at == task_data["created_at"]
