import logging
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infra.config.config import Settings
from app.intrerface.http.url import router as router_task
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
app.include_router(
    router_task,
    prefix=SETTINGS.base.path_service,
)
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
