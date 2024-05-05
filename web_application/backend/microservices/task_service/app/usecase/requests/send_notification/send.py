
from typing import Any, Dict, Union

import requests

from app.infra.config.config import Settings
from app.usecase.error.handler import Http500Error

SETTINGS = Settings().request


async def send_notification(notification_task: Dict[str, Any], massage: Dict[str, Any]) -> Union[None, Http500Error]:
    """Send request to `send_notification_service` for further processing"""
    notification_task["massage"] = massage
    response = requests.post(SETTINGS.send_notification, json=notification_task)
    if response.status_code != 201:
        raise Http500Error(detail=f"part of service not available")
    return None
