import logging
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infra.config.config import Settings
from app.intrerface.http.routers.add_task import router as router_add_task
from app.intrerface.http.routers.delete_task import router as router_delete_task
from app.intrerface.http.routers.get_user_task import router as router_get_user_task
from app.intrerface.http.routers.get_task_by_id import router as router_get_task_by_id
from app.intrerface.http.routers.update_task import router as router_update_task
from app.intrerface.http.routers.text_search_by_task import router as router_text_search_by_task
from app.infra.logger.log import logging_config

# First init config
SETTINGS = Settings()

# Init logger
dictConfig(logging_config)
logger = logging.getLogger("console_log")

# Init app
app = FastAPI(
    title=SETTINGS.base.name_service,
    openapi_url=f"{SETTINGS.base.path_service}/openapi.json",
    docs_url=f"{SETTINGS.base.path_service}/docs"
)
logger.info(f"Complete init FastAPI app")

# All include routers
app.include_router(router_add_task, prefix=SETTINGS.base.path_service)
app.include_router(router_delete_task, prefix=SETTINGS.base.path_service)
app.include_router(router_get_user_task, prefix=SETTINGS.base.path_service)
app.include_router(router_get_task_by_id, prefix=SETTINGS.base.path_service)
app.include_router(router_update_task, prefix=SETTINGS.base.path_service)
app.include_router(router_text_search_by_task, prefix=SETTINGS.base.path_service)

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
