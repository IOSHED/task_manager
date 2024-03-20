from typing import Dict, Any

import pydantic


class HttpErrorSchema(pydantic.BaseModel):
    detail: Dict[str, Any] | str = NotImplementedError


class Http401ErrorSchema(HttpErrorSchema):
    pass


class Http404ErrorSchema(HttpErrorSchema):
    pass


class Http500ErrorSchema(HttpErrorSchema):
    pass
