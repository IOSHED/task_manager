from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infra.config.config import Settings
from app.intrerface.http.url import router as router_task

# First init config
settings = Settings()

# Init logger


# Init app
app = FastAPI(
    title=settings.base.name_service,
    openapi_url=f"{settings.base.path_service}/openapi.json",
    docs_url=f"{settings.base.path_service}/docs"
)

# All include routers
app.include_router(
    router_task,
    prefix=settings.base.path_service,
)

# All use middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.base.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
