import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound, DatabaseError
from starlette import status

from app.domain.schemas.requests.task_update import RequestUpdatingDataTaskSchema
from app.domain.schemas.response.error import Http404ErrorSchema, Http500ErrorSchema, Http401ErrorSchema
from app.usecase.error.handler import Http500Error, Http404Error, Http401Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.task import TaskService

logger = logging.getLogger("console_log")
router = APIRouter()


@router.patch(
    "",
    description="Changes the task data",
    tags=["Task"],
    summary="Changes the task data",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "task success changed",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "task with this id does not exist",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    }
)
async def update_task(
    user: ActiveUser,
    updating_data_task: RequestUpdatingDataTaskSchema,
    task_service: TaskService = Depends(TaskService),
) -> Any:
    try:
        logger.info(f"update task with data -> {updating_data_task}")

        if isinstance(user, Http401Error):
            logger.info(f"current user is not auth -> {user}")
            raise Http401Error(detail=user.detail)

        await task_service.update_task(updating_data_task)

    except NoResultFound:
        logger.info(f"this task is absent -> id ={updating_data_task.task_id}")
        raise Http404Error(detail="task with this id does not exist")

    except DatabaseError as err:
        logger.error(f"database error during create task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
