import logging

from app.usecase.uow.dependencies import UOWDep

logger = logging.getLogger("console_log")


class TemplateTaskService:
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def create(self, new_template_task):
        pass

    async def delete(self, args_query, id):
        pass

    async def find_set(self, user_id, skip, limit, order_by, desc):
        pass

    async def find_one(self, id_template_task):
        pass

    async def update(self, updating_data_template_task, template_task_id, user_id):
        pass
