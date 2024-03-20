import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.usecase.error.handler import Http401Error, Http500Error
from app.domain.schemas.requests.task_delete import RequestTaskSchemaDelete
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.task import TaskService
from app.domain.schemas.response.error import Http500ErrorSchema, Http401ErrorSchema, Http404ErrorSchema

logger = logging.getLogger("console_log")
router = APIRouter()


@router.delete(
    "/",
    description="Delete task if user is admin or owner",
    tags=["Task"],
    summary="Delete task if user is admin or owner",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "task success deleted",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "the task they want to delete is missing",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        }
    }
)
async def delete_task(
    user: ActiveUser,
    args_query: RequestTaskSchemaDelete,
    task_service: TaskService = Depends(TaskService),
) -> Any:
    try:
        logger.info(f"delete task -> {args_query}")

        if isinstance(user, Http401Error):
            logger.info(f"current user is not auth -> {user}")
            raise Http401Error(detail=user.detail)

        await task_service.delete(args_query, user)

        logger.info(f"deleted task -> {args_query}")

    # except Http404Error as err:
    #     logger.info(f"the tasks that were tried to be deleted are missing -> {args_query}")
    #     raise err
    #
    # except Http401Error as err:
    #     logger.info(f"current user does not own task -> {user}")
    #     raise err

    except DatabaseError as err:
        logger.error(f"database error during create task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
