
from app.infra.config.enums import Mode
from app.infra.config.config import Settings

SETTINGS = Settings()


def get_log_level() -> str:
    match SETTINGS.mode:
        case Mode.dev:
            return "INFO"
        case Mode.local:
            return "DEBUG"
        case _:
            return "INFO"


LOG_LEVEL = get_log_level()
FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
logging_config = {
    "version": 1,   # mandatory field
    # if you want to overwrite existing loggers' configs
    # "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": FORMAT,
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        }
    },
    "loggers": {
        "console_log": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            # "propagate": False
        }
    },
}
