import logging
from typing import Any

from fastapi import APIRouter, Depends, Path
from sqlalchemy.exc import DatabaseError, NoResultFound
from starlette import status

from app.domain.schemas.response.error import Http404ErrorSchema, Http500ErrorSchema
from app.usecase.service.task import TaskService
from app.usecase.error.handler import Http500Error, Http404Error
from app.domain.schemas.response.task_get import ResponseTaskSchemaGet

logger = logging.getLogger("console_log")
router = APIRouter()


@router.get(
    "/{id_task}",
    description="Get task by id",
    tags=["Task"],
    summary="Get task by id",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseTaskSchemaGet,
            "description": "task success get",
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
async def get_task_by_id(
    id_task: int = Path(description="ID getting task"),
    task_service: TaskService = Depends(TaskService),
) -> Any:
    try:
        logger.info(f"get task by id = {id_task}")

        task_response = await task_service.get_by_id(id_task)

        return task_response

    except NoResultFound:
        logger.info(f"this task is absent -> id ={id_task}")
        raise Http404Error(detail="task with this id does not exist")

    except DatabaseError as err:
        logger.error(f"database error during create task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
