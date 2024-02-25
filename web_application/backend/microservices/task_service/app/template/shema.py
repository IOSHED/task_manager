from typing import List

from pydantic import BaseModel

from app.task.schema import TaskSchema


class TemplateBase(BaseModel):
    pass


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int
    tasks: List[TaskSchema] = []

    class Config:
        orm_mode = True
