from typing import Optional
from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    country: Optional[str] = None

    @field_validator('id')
    def validate_id(cls, value):
        if value < 0:
            raise ValueError('ID should >= 0')
        return value

    @field_validator('country')
    def validate_country(cls, value):
        if len(value) < 3:
            raise ValueError('Country should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Country shouldn\'t be longer than 16 chars')
        return value

    @field_validator('username')
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError('Username should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Username shouldn\'t be longer than 16 chars')
        return value


class UserCreate(User):
    id: int
    username: str
    country: str


class UserUpdate(User):
    pass
