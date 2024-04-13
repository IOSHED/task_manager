import pytest
from pydantic import ValidationError
from datetime import datetime, time, timedelta

from domain.schemas.models.notification_task import NotificationTaskSchema


@pytest.fixture
def valid_notification_task_data():
    return {
        "id": 1,
        "task_id": 123,
        "send_notification_at": datetime.utcnow(),
        "duration_send_notification_at": time(hour=1)
    }


def test_create_notification_task_schema(valid_notification_task_data):
    notification_task = NotificationTaskSchema(**valid_notification_task_data)
    assert notification_task.id == valid_notification_task_data["id"]
    assert notification_task.task_id == valid_notification_task_data["task_id"]
    assert notification_task.send_notification_at == valid_notification_task_data["send_notification_at"]
    assert notification_task.duration_send_notification_at == valid_notification_task_data["duration_send_notification_at"]


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        NotificationTaskSchema()


def test_optional_field_default_value():
    notification_task = NotificationTaskSchema(id=1, task_id=123, send_notification_at=datetime.utcnow())
    assert notification_task.duration_send_notification_at is None


def test_valid_send_notification_at_future_date():
    future_date = datetime.utcnow() + timedelta(days=1)
    notification_task = NotificationTaskSchema(id=1, task_id=123, send_notification_at=future_date)
    assert notification_task.send_notification_at == future_date


def test_valid_duration_send_notification_at():
    valid_time = time(hour=10, minute=30)
    notification_task = NotificationTaskSchema(id=1, task_id=123, send_notification_at=datetime.utcnow(), duration_send_notification_at=valid_time)
    assert notification_task.duration_send_notification_at == valid_time


def test_valid_duration_send_notification_at_valid_time():
    valid_time = time(hour=23, minute=30)
    notification_task = NotificationTaskSchema(
        id=1, task_id=123, send_notification_at=datetime.utcnow(), duration_send_notification_at=valid_time
    )
    assert notification_task.duration_send_notification_at is not None


def test_update_notification_task_schema(valid_notification_task_data):
    notification_task = NotificationTaskSchema(**valid_notification_task_data)
    updated_data = {"task_id": 456}
    updated_notification_task = notification_task.copy(update=updated_data)
    assert updated_notification_task.task_id == updated_data["task_id"]
    assert updated_notification_task.send_notification_at == valid_notification_task_data["send_notification_at"]
