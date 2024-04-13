import logging
from typing import List, Any

from fastapi import APIRouter, Path, Depends, Query
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.domain.schemas.response.error import Http500ErrorSchema, Http401ErrorSchema
from app.usecase.error.handler import Http500Error, Http401Error
from app.usecase.service.task import TaskService
from app.domain.schemas.response.task_full_search import ResponseTaskSchemaFulltextSearch
from app.usecase.requests.user.dependencies import ActiveUser

logger = logging.getLogger("console_log")
router = APIRouter()


@router.get(
    "/fulltext_search/{string_search}",
    description="""
        Takes a string as input and returns the id and text fields of the required tasks using a full-text search
    """,
    tags=["Task"],
    summary="Full-text search",
    responses={
        status.HTTP_200_OK: {
            "model": List[ResponseTaskSchemaFulltextSearch],
            "description": "tasks success get",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Http401ErrorSchema,
            "description": "user unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Http500ErrorSchema,
            "description": "unexpected error",
        },
    }
)
async def text_search_by_task(
    user: ActiveUser,
    string_search: str = Path(description="the line where the task will be searched"),
    limit: int = Query(
        gt=0,
        le=25,
        description="the number of records to be output",
    ),
    task_service: TaskService = Depends(TaskService),
) -> Any:
    try:
        logger.info(f"search string = {string_search}")

        if isinstance(user, Http401Error):
            logger.info(f"current user is not auth -> {user}")
            raise Http401Error(detail=user.detail)

        tasks_response = await task_service.fulltext_search(string_search, user.id, limit)
        logger.info(f"got result full-text search -> {tasks_response}")

        return tasks_response

    except DatabaseError as err:
        logger.error(f"database error in full-text search task -> {err}")
        raise Http500Error(detail="Database Error")

    except Exception as err:
        logger.error(f"not expected error -> {err}")
        raise Http500Error(detail="Internal Server Error")
