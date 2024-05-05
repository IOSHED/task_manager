
from typing import Union

import requests

from app.infra.config.config import Settings
from app.usecase.error.handler import Http500Error

SETTINGS = Settings().request


async def delete_send_notification(notification_task_id: int) -> Union[None, Http500Error]:
    """Send request to `send_notification_service` for further processing"""
    response = requests.delete(SETTINGS.delete_send_notification, data=notification_task_id)
    if response.status_code != 204:
        raise Http500Error(detail=f"part of service not available")
    return None
