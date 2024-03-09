from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.usecase.uow.dependencies import UOWDep
from app.domain.shemas.requests.task_create import RequestTaskSchemaCreate
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.task import TaskService
from app.domain.shemas.response.task_create import ResponseTaskSchemaCreate


router = APIRouter()


@router.post(
    "/",
    response_model=ResponseTaskSchemaCreate,
    status_code=status.HTTP_201_CREATED,
    description="Add new task for current user",
    tags=["Task"],
    summary="Add new task for current user",
)
async def add_task(
    new_task: RequestTaskSchemaCreate,
    uow: UOWDep,
    user: ActiveUser,
) -> Any:
    """
    Add a new task for the current user.

    Parameters:
    - new_task (RequestTaskSchemaCreate): The task data to be created.
    - uow (UOWDep): The unit of work dependency for database operations.
    - user (ActiveUser): The current active user.

    Returns:
    - ResponseTaskSchemaCreate: The response containing the created task details.

    Raises:
    - HTTPException 400: If there is a bad request or validation error.
    - HTTPException 401: If current user is not active or not registered.
    - HTTPException 404: If the task could not be created.
    - HTTPException 500: If there is an internal server error.

    Example:
    python
        # Example usage to add a new task
        new_task_data = {
            "name": "Complete project report",
            "description": "Finish the project report by Friday."
        }
        response = client.post("/tasks/", json=new_task_data)
        assert response.status_code == 201
    """
    try:
        task_service = TaskService(uow)
        created_task_response = await task_service.create(new_task, user.id)

        if not created_task_response.task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not created")
        return created_task_response

    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
