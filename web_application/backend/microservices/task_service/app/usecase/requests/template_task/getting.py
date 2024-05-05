from typing import Any, Dict, Union

import requests


from app.infra.config.config import Settings
from app.usecase.error.handler import Http404Error

SETTINGS = Settings().request


async def get_template_task(template_id: int) -> Union[Dict[str, Any], Http404Error]:
    """Send request to `template_task_service` and git data about template by id"""
    response = requests.get(SETTINGS.get_template, params={"id_template": template_id})
    template_task_info = response.json()
    if response.status_code == 404:
        raise Http404Error(detail=f"template with this id={template_id} does not exist")
    return template_task_info
