import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from domain.shemas.models.complete_task import CompleteTaskSchema


@pytest.fixture
def valid_complete_task_data():
    return {
        "id": 1,
        "task_id": 123,
        "complete_at": datetime.utcnow(),
        "planned_complete_at": datetime.utcnow()
    }


def test_valid_complete_task_schema(valid_complete_task_data):
    complete_task = CompleteTaskSchema(**valid_complete_task_data)
    assert complete_task.id == valid_complete_task_data["id"]
    assert complete_task.task_id == valid_complete_task_data["task_id"]
    assert complete_task.complete_at == valid_complete_task_data["complete_at"]
    assert complete_task.planned_complete_at == valid_complete_task_data["planned_complete_at"]


def test_valid_complete_at_future_date():
    future_date = datetime.utcnow() + timedelta(days=1)
    complete_task = CompleteTaskSchema(id=1, task_id=123, complete_at=future_date)
    assert complete_task.complete_at is not None


def test_valid_planned_complete_at_past_date():
    past_date = datetime.utcnow() - timedelta(days=1)
    complete_task = CompleteTaskSchema(id=1, task_id=123, planned_complete_at=past_date)
    assert complete_task.planned_complete_at is not None


def test_update_complete_task_schema(valid_complete_task_data):
    complete_task = CompleteTaskSchema(**valid_complete_task_data)
    updated_data = {"task_id": 456}
    updated_complete_task = complete_task.copy(update=updated_data)
    assert updated_complete_task.task_id == updated_data["task_id"]
    assert updated_complete_task.complete_at == valid_complete_task_data["complete_at"]


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        CompleteTaskSchema()


def test_invalid_id_type():
    with pytest.raises(ValidationError):
        CompleteTaskSchema(
            id="invalid", task_id=123, complete_at=datetime.utcnow(), planned_complete_at=datetime.utcnow()
        )


def test_invalid_task_id_negative():
    with pytest.raises(ValidationError):
        CompleteTaskSchema(id=1, task_id=-1, complete_at=datetime.utcnow(), planned_complete_at=datetime.utcnow())


def test_invalid_task_id_zero():
    with pytest.raises(ValidationError):
        CompleteTaskSchema(
            id=1, task_id=0, complete_at=datetime.utcnow(), planned_complete_at=datetime.utcnow()
        )


def test_valid_task_id_positive():
    complete_task = CompleteTaskSchema(
        id=1, task_id=123, complete_at=datetime.utcnow(), planned_complete_at=datetime.utcnow()
    )
    assert complete_task.task_id == 123


def test_valid_planned_complete_at_past_date():
    past_date = datetime.utcnow() - timedelta(days=1)
    complete_task = CompleteTaskSchema(id=1, task_id=123, complete_at=datetime.utcnow(), planned_complete_at=past_date)
    assert complete_task.planned_complete_at == past_date
