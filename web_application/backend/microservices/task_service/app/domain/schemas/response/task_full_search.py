import pydantic
from pydantic import PositiveInt


class ResponseTaskSchemaFulltextSearch(pydantic.BaseModel):
    task_id: PositiveInt
    name: str
    description: str
