import pytest

from app.infra.postgres.models.complete_task import CompleteTask


@pytest.fixture
def complete_task_data():
    return {
        "id": 1,
        "task_id": 1,
        "complete_at": None,
        "planned_complete_at": None,
    }


def test_complete_task_repr(complete_task_data):
    complete_task = CompleteTask(**complete_task_data)
    assert repr(complete_task) == \
           f"CompleteTask(id={complete_task_data['id']!r}, " \
           f"planned_complete_at={complete_task_data['planned_complete_at']!r})"


def test_task_to_read_model(complete_task_data):
    complete_task = CompleteTask(**complete_task_data)
    complete_task_schema = complete_task.to_read_model()
    assert complete_task_schema.id == complete_task_data["id"]
    assert complete_task_schema.task_id == complete_task_data["task_id"]
    assert complete_task_schema.complete_at == complete_task_data["complete_at"]
    assert complete_task_schema.planned_complete_at == complete_task_data["planned_complete_at"]


def test_task_init(complete_task_data):
    complete_task = CompleteTask(**complete_task_data)
    assert complete_task.id == complete_task_data["id"]
    assert complete_task.task_id == complete_task_data["task_id"]
    assert complete_task.complete_at == complete_task_data["complete_at"]
    assert complete_task.planned_complete_at == complete_task_data["planned_complete_at"]
