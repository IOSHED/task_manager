import pytest
from datetime import datetime

from app.infra.postgres.models.notification_task import NotificationTask


@pytest.fixture
def task_data():
    return {
        "id": 1,
        "task_id": 1,
        "send_notification_at": datetime.utcnow(),
        "duration_send_notification_at": None,
    }


def test_task_repr(task_data):
    notification_task = NotificationTask(**task_data)
    assert repr(notification_task) == \
           f"NotificationTask(id={task_data['id']!r}, send_notification_at={task_data['send_notification_at']!r})"


def test_task_to_read_model(task_data):
    notification_task = NotificationTask(**task_data)
    task_schema = notification_task.to_read_model()
    assert task_schema.id == task_data["id"]
    assert task_schema.task_id == task_data["task_id"]
    assert task_schema.send_notification_at == task_data["send_notification_at"]
    assert task_schema.duration_send_notification_at == task_data["duration_send_notification_at"]


def test_task_init(task_data):
    notification_task = NotificationTask(**task_data)
    assert notification_task.id == task_data["id"]
    assert notification_task.task_id == task_data["task_id"]
    assert notification_task.send_notification_at == task_data["send_notification_at"]
    assert notification_task.duration_send_notification_at == task_data["duration_send_notification_at"]
