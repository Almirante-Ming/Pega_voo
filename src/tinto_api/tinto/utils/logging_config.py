import logging.config
import os
from datetime import datetime

log_filename = datetime.now().strftime("%Y_%m_%d") + ".log"
log_path = os.path.join('logs', log_filename)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": log_path,
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
}
