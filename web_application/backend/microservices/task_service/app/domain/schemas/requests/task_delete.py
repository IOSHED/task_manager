from typing import List

import pydantic
from pydantic import PositiveInt


class RequestTaskSchemaDelete(pydantic.BaseModel):
    id_for_deleting_tasks: List[PositiveInt]
