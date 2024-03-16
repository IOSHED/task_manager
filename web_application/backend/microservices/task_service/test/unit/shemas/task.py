import pytest
from pydantic import ValidationError

from domain.schemas.models.task import TaskSchema


@pytest.fixture
def valid_task_data():
    return {
        "id": 1,
        "name": "Valid Task",
        "create_by": 123,
    }


def test_valid_task(valid_task_data):
    task = TaskSchema(**valid_task_data)
    assert task.id == 1
    assert task.name == "Valid Task"
    assert task.create_by == 123


def test_invalid_id_type():
    with pytest.raises(ValidationError):
        TaskSchema(id="not_an_int", name="Invalid Task", create_by=123)


def test_name_length_exceeded():
    with pytest.raises(ValidationError):
        TaskSchema(id=1, name="A" * 256, create_by=123)


def test_invalid_create_by_type():
    with pytest.raises(ValidationError):
        TaskSchema(id=1, name="Invalid Task", create_by="not_an_int")


def test_created_at_default_value():
    task = TaskSchema(id=1, name="Task", create_by=123)
    assert task.created_at is not None


def test_optional_fields():
    task = TaskSchema(id=1, name="Task", create_by=123, description="Optional Description", id_template=456)
    assert task.description == "Optional Description"
    assert task.id_template == 456


def test_name_required():
    with pytest.raises(ValidationError):
        TaskSchema(id=1, create_by=123)


def test_create_by_required():
    with pytest.raises(ValidationError):
        TaskSchema(id=1, name="Task")


def test_id_required():
    with pytest.raises(ValidationError):
        TaskSchema(name="Task", create_by=123)


def test_id_positive_integer():
    with pytest.raises(ValidationError):
        TaskSchema(id=-1, name="Task", create_by=123)


def test_create_by_positive_integer():
    with pytest.raises(ValidationError):
        TaskSchema(id=1, name="Task", create_by=-123)
