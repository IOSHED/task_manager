import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.domain.response.error import Http401ErrorSchema, Http500ErrorSchema, Http404ErrorSchema
from app.usecase.error.handler import Http401Error, Http404Error, Http500Error
from app.usecase.requests.user.dependencies import ActiveUser
from app.usecase.service.template_task_service import TemplateTaskService

logger = logging.getLogger("console_log")
router = APIRouter()


@router.delete(
    "/",
    tags=["Template Task"],
    summary="Delete template task",
    description="Delete template task if current user owns this template task",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "template task success delete",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "current user not owns this template task",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Http404ErrorSchema,
            "description": "template task they want to delete is missing",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    },
)
async def delete_template_task(
    user: ActiveUser,
    args_query: RequestTemplateTaskSchemaDelete,
    template_task_service: TemplateTaskService = Depends(TemplateTaskService),
) -> Any:
    try:
        logger.info(f"start delete template task:"
                    f"data         -> {args_query},"
                    f"current user -> {user},")

        result = await template_task_service.delete(args_query, user.id)

        logger.info(f"deleted template task:"
                    f"data deleting -> {args_query},"
                    f"result        -> {result},")

    except Http404Error as err:
        logger.info(f"tasks that were tried to be deleted are missing:"
                    f"data deleting -> {args_query},"
                    f"msg           -> {err.detail},")
        return Http404Error(detail=err.detail)

    except Http401Error as err:
        logger.info(f"current user unauthorized tried deleting new template task:"
                    f"data -> {args_query},")
        raise Http401Error(detail=err.detail)

    except DatabaseError as err:
        logger.error(f"database error during create task:"
                     f"msg -> {err},")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error:"
                     f"msg: -> {err},")
        raise Http500Error(detail="Internal Server Error")
