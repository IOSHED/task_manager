import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import DatabaseError, NoResultFound
from starlette import status

from app.domain.response.error import Http401ErrorSchema, Http500ErrorSchema, Http404ErrorSchema
from app.usecase.error.handler import Http404Error, Http500Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.template_task_service import TemplateTaskService

logger = logging.getLogger("console_log")
router = APIRouter()


@router.put(
    "",
    tags=["Template Task"],
    summary="Changes the template task data",
    description="Changes the template task data recreating her",
    responses={
        status.HTTP_201_CREATED: {
            "model": ReposnseTemplateTaskSchemaCreate,
            "description": "template task success changed",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "template task with this id does not exist",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    },
)
async def update_template_task(
    user: ActiveUser,
    template_task_id: int,
    updating_data_template_task: RequestTemplateTaskSchemaCreate,
    template_task_service: TemplateTaskService = Depends(TemplateTaskService),
) -> Any:
    try:
        logger.info(f"start update template task:"
                    f"template_task_id            -> {template_task_id},"
                    f"updating_data_template_task -> {updating_data_template_task},"
                    f"user_id                     -> {user.id},")

        updated_template_task = await template_task_service.update(
            updating_data_template_task=updating_data_template_task,
            template_task_id=template_task_id,
            user_id=user.id,
        )

        logger.info(f"updated template task:"
                    f"updating_data_template_task -> {updating_data_template_task},"
                    f"response                    -> {updated_template_task}")

        return updated_template_task

    except NoResultFound:
        logger.info(f"this template task is absent:"
                    f"template_task_id -> {template_task_id},")
        raise Http404Error(detail="template task with this id does not exist")

    except DatabaseError as err:
        logger.error(f"database error during create task:"
                     f"msg -> {err},")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error:"
                     f"msg -> {err},")
        raise Http500Error(detail="Internal Server Error")
