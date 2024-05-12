import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound, DatabaseError
from starlette import status

from app.domain.response.error import Http401ErrorSchema, Http500ErrorSchema, Http404ErrorSchema
from app.usecase.error.handler import Http401Error, Http404Error, Http500Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.template_task_service import TemplateTaskService

logger = logging.getLogger("console_log")
router = APIRouter()


@router.post(
    "/",
    tags=["Template Task"],
    summary="Add new template task for current user",
    description="Create template task using JSON record for current user",
    responses={
        status.HTTP_201_CREATED: {
            "model": ResponseTaskSchemaCreate,
            "description": "template task success created",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "created template task is lost",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    },
)
async def created_template_task(
    user: ActiveUser,
    new_template_task: RequestTemplateTaskSchemaCreate,
    template_task_service: TemplateTaskService = Depends(TemplateTaskService)
) -> Any:
    try:
        logger.info(f"start creating new template task: "
                    f"data -> {new_template_task.model_dump()},"
                    f"current_user -> {user},")

        created_template_task = await template_task_service.create(new_template_task)

        logger.info(f"created new template task:"
                    f"data creating -> {new_template_task},"
                    f"new task -> {created_template_task,}")

        return created_template_task

    except NoResultFound:
        logger.info(f"created new template task is lost:"
                    f"data creating -> {new_template_task},")
        return Http404Error(detail="created template task is lost")

    except Http401Error as err:
        logger.info(f"current user unauthorized tried creating new template task:"
                    f"data -> {new_template_task.model_dump()},")
        raise Http401Error(detail=err.detail)

    except DatabaseError as err:
        logger.error(f"database error during create template task:"
                     f"msg -> {err},")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error:"
                     f"msg -> {err}",)
        raise Http500Error(detail="Internal Server Error")
