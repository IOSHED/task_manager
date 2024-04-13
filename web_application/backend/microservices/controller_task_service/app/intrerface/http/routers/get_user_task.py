import logging
from enum import Enum
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import NoResultFound, DatabaseError
from starlette import status

from app.domain.schemas.response.error import Http404ErrorSchema, Http500ErrorSchema, Http401ErrorSchema
from app.domain.schemas.response.task_get import ResponseTaskSchemaGet
from app.usecase.error.handler import Http401Error, Http404Error, Http500Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.task import TaskService

logger = logging.getLogger("console_log")
router = APIRouter()


class OrderBy(Enum):
    created_at: str = "task.created_at"
    planned_complete_at: str = "complete_task.planned_complete_at"
    complete_at: str = "complete_task.complete_at"
    send_notification_at: str = "notification_task.send_notification_at"
    duration_send_notification_at: str = "notification_task.duration_send_notification_at"

    def __str__(self) -> str:
        return f"{self.value}"


@router.get(
    "/list",
    description="""
        Getting user tasks with a max limit is 25 and grouping by field priority:
        created_at, planned_complete_at, complete_at
    """,
    tags=["Task"],
    summary="Getting user tasks with a max limit",
    responses={
        status.HTTP_200_OK: {
            "model": List[ResponseTaskSchemaGet],
            "descriptions": "all task success get",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "no task was found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    }
)
async def get_user_task(
    user: ActiveUser,
    order_by: OrderBy,
    skip: int = Query(
        default=0,
        ge=0,
        description="the number of records to skip before receiving a limited number of records",
    ),
    limit: int = Query(
        gt=0,
        le=25,
        description="the number of records to be output",
    ),
    id_template: Optional[int] = Query(
        gt=0,
        default=None,
        description="if is not None then select all task having template by this id"
    ),
    desc: bool = Query(
        default=True,
        description="is reverse results by 'order_by'"
    ),
    is_show_notification: Optional[bool] = Query(
        default=None,
        description="show only task having send notification or, on the contrary, task not having send notification",
    ),
    is_show_complete: Optional[bool] = Query(
        default=None,
        description="""
            show only task having possibility of completion or, on the contrary, task not having possibility of completion
        """,
    ),
    task_service: TaskService = Depends(TaskService),
) -> Any:
    try:
        logger.info(f"get task user = {user.id} with limit = {limit}, skip = {skip}, group_by = {str(order_by)}")

        if isinstance(user, Http401Error):
            logger.info(f"current user is not auth -> {user}")
            raise Http401Error(detail=user.detail)

        tasks_response = await task_service.get_user_task(
            user.id,
            skip,
            limit,
            str(order_by),
            desc,
            id_template=id_template,
            is_show_notification=is_show_notification,
            is_show_complete=is_show_complete,
        )
        logger.info(f"got task -> {tasks_response}")

        return tasks_response

    except NoResultFound:
        logger.info(f"the current user = {user.id} does not have any tasks with such request parameters")
        raise Http404Error(detail="the current user does not have any tasks with such request parameters")

    except DatabaseError as err:
        logger.error(f"database error during create task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
