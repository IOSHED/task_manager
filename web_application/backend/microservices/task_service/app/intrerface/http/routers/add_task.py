import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.domain.schemas.requests.task_create import RequestTaskSchemaCreate
from app.domain.schemas.response.error import Http401ErrorSchema, Http500ErrorSchema, Http404ErrorSchema
from app.usecase.error.handler import Http401Error, Http404Error, Http500Error
from app.domain.schemas.response.task_create import ResponseTaskSchemaCreate
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.task import TaskService


logger = logging.getLogger("console_log")
router = APIRouter()


@router.post(
    "/",
    description="Add new task for current user",
    tags=["Task"],
    summary="Add new task for current user",
    responses={
        status.HTTP_201_CREATED: {
            "model": ResponseTaskSchemaCreate,
            "description": "task success created",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "created task is not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        }
    }
)
async def add_task(
    user: ActiveUser,
    new_task: RequestTaskSchemaCreate,
    task_service: TaskService = Depends(TaskService)
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
    - HTTPException 422: If there is a bad request or validation error.
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
        logger.info(f"creating new task -> {new_task.model_dump()}")

        if isinstance(user, Http401Error):
            logger.info(f"current user is not auth -> {user}")
            raise Http401Error(detail=user.detail)

        created_task_response = await task_service.create(new_task, user.id)
        logger.info(f"created new task -> {created_task_response.model_dump()}")

        if not created_task_response.task:
            logger.error(f"this task not created -> {new_task.model_dump()}")
            raise Http404Error(detail="Task not created")

        return created_task_response

    except DatabaseError as err:
        logger.error(f"database error during create task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
