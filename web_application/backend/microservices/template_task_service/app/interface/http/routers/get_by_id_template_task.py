import logging
from typing import Any

from fastapi import APIRouter, Path, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.exc import DatabaseError, NoResultFound
from starlette import status

from app.domain.response.error import Http500ErrorSchema, Http404ErrorSchema
from app.infra.config.config import Settings
from app.usecase.error.handler import Http404Error, Http500Error
from app.usecase.service.template_task_service import TemplateTaskService

logger = logging.getLogger("console_log")
router = APIRouter()
SETTINGS = Settings()


@router.get(
    "/{id_template_task}",
    tags=["Template Task"],
    summary="Get template task by id",
    description="GEt template task by id",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseTemplateTaskSchemaGet,
            "description": "template task success got",
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
@cache(expire=SETTINGS.cache.other_expire.get_template_task_by_id)
async def get_template_task_by_id(
    id_template_task: int = Path(description="ID getting template task"),
    template_task_service: TemplateTaskService = Depends(TemplateTaskService),
) -> Any:
    try:
        logger.info(f"start get template task:"
                    f"id_template_task -> {id_template_task},")

        template_task_response = await template_task_service.find_one(id_template_task)

        logger.info(f"got template task:"
                    f"id       -> {id_template_task},"
                    f"response -> {template_task_response},")

        return template_task_response

    except NoResultFound:
        logger.info(f"this template task is absent:"
                    f"id -> {id_template_task}")
        raise Http404Error(detail="task with this id does not exist")

    except DatabaseError as err:
        logger.error(f"database error during create task:"
                     f"msg -> {err},")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error:"
                     f"msg -> {err},")
        raise Http500Error(detail="Internal Server Error")
