import pydantic
from pydantic import PositiveInt, EmailStr, constr


class DataUser(pydantic.BaseModel):
    id: PositiveInt
    email: EmailStr
    username: constr(max_length=255, min_length=1)
    is_active: bool
    is_superuser: bool
    is_verified: bool
