from typing import Dict, Any

from app.usecase.requests.template_task.getting import get_template_task


class TemplateTaskService:
    def __init__(self, template_id: int) -> None:
        self.id = template_id

    async def fill(self, create_task: Dict[str, Any]) -> Dict[str, Any]:
        template_task = await get_template_task(self.id)
        for key, value in template_task:
            create_task[key] = value
        return create_task
