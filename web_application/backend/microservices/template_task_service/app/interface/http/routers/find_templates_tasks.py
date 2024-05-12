import logging
from enum import Enum
from typing import List, Any

from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.exc import NoResultFound, DatabaseError
from starlette import status

from app.domain.response.error import Http500ErrorSchema, Http404ErrorSchema
from app.infra.config.config import Settings
from app.usecase.error.handler import Http404Error, Http500Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.template_task_service import TemplateTaskService

logger = logging.getLogger("console_log")
router = APIRouter()
SETTINGS = Settings()


class OrderBy(Enum):
    """Lists all the fields by which task templates can be sorted."""
    created_at: str = "created_at"
    name: str = "name"
    description: str = "description"

    def __str__(self) -> str:
        return f"{self.value}"


@router.get(
    "/list",
    tags=["Template Task"],
    summary="Find templates tasks",
    description="Find templates tasks of the current user using filters and sorting",
    responses={
        status.HTTP_200_OK: {
            "model": List[ResponseTemplateTaskSchemaGet],
            "description": "all template task success got",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http404ErrorSchema,
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
    },
)
@cache(expire=SETTINGS.cache.other_exire.find_templates_task)
async def find_templates_tasks(
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
    desc: bool = Query(
        default=True,
        description="is reverse results by 'order_by'"
    ),
    template_task_service: TemplateTaskService = Depends(TemplateTaskService),
) -> Any:
    try:
        logger.info(f"start find templates tasks:"
                    f"user        -> {user},"
                    f"skip, limit -> {skip}, {limit},"
                    f"order by    -> {order_by},"
                    f"desc        -> {desc},")

        templates_tasks_response = await template_task_service.find_set(
            user_id=user.id,
            skip=skip,
            limit=limit,
            order_by=str(order_by),
            desc=desc,
        )

        logger.info(f"got templates tasks:"
                    f"response -> {templates_tasks_response},")

        return templates_tasks_response

    except NoResultFound:
        logger.info(f"the current user = {user.id} does not have any templates tasks with such request parameters")
        raise Http404Error(detail="the current user does not have any tasks with such request parameters")

    except DatabaseError as err:
        logger.error(f"database error during create task:"
                     f"msg -> {err},")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error:"
                     f"msg -> {err},")
        raise Http500Error(detail="Internal Server Error")
