from uuid import UUID

from pydantic import BaseModel, EmailStr, field_serializer


class CreateCustomerDto(BaseModel):
    email: EmailStr
    password: str


class CustomerDetailDto(BaseModel):
    uuid: UUID

    username: str | None
    email: EmailStr

    is_admin: bool
    is_active: bool
    is_enabled: bool

    @field_serializer("uuid")
    def serialize_uuid(self, value, _info):
        return str(value)