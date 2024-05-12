import logging
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infra.cache.redis import redis
from app.infra.config.config import Settings
from app.infra.logger.log import logging_config
from app.interface.http.routers.create_template_task import router as router_create_template_task
from app.interface.http.routers.delete_template_task import router as router_delete_template_task
from app.interface.http.routers.find_templates_tasks import router as router_find_templates_tasks
from app.interface.http.routers.get_by_id_template_task import router as router_get_by_id_template_task
from app.interface.http.routers.update_template_task import router as router_update_template_task


def main(*_args, **_kwargs) -> None:
    # First init config
    SETTINGS = Settings()

    # Init logger
    dictConfig(logging_config)
    logger = logging.getLogger("console_log")

    # Init redis
    _redis = redis

    # Init app
    app = FastAPI(
        title=SETTINGS.base.name_service,
        openapi_url=f"{SETTINGS.base.path_service}/openapi.json",
        docs_url=f"{SETTINGS.base.path_service}/docs"
    )
    logger.info(f"Complete init FastAPI app")

    # All include routers
    app.include_router(router_create_template_task, prefix=SETTINGS.base.path_service)
    app.include_router(router_delete_template_task, prefix=SETTINGS.base.path_service)
    app.include_router(router_find_templates_tasks, prefix=SETTINGS.base.path_service)
    app.include_router(router_get_by_id_template_task, prefix=SETTINGS.base.path_service)
    app.include_router(router_update_template_task, prefix=SETTINGS.base.path_service)

    logger.info(f"Complete include router")

    # All use middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SETTINGS.base.origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                       "Authorization"],
    )
    logger.info(f"Complete include middleware")


if __name__ == '__main__':
    main()
