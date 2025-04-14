from typing import Optional
from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None

    @field_validator('id')
    def validate_id(cls, value):
        if value < 0:
            raise ValueError('ID should >= 0')
        return value

    @field_validator('username')
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError('Username should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Username shouldn\'t be longer than 16 chars')
        return value
    
    @field_validator('firstname')
    def validate_firstname(cls, value):
        if len(value) < 3:
            raise ValueError('Firstname should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Firstname shouldn\'t be longer than 16 chars')
        return value
    
    @field_validator('lastname')
    def validate_lastname(cls, value):
        if len(value) < 3:
            raise ValueError('Lastname should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Lastname shouldn\'t be longer than 16 chars')
        return value
    
    @field_validator('age')
    def validate_age(cls, value):
        if value < 18:
            raise ValueError('Age should >= 18')
        return value
    
    @field_validator('gender')
    def validate_gender(cls, value):
        if value != 'M' and value != 'F':
            raise ValueError('Wrong gender value')
        return value

    @field_validator('country')
    def validate_country(cls, value):
        if len(value) < 3:
            raise ValueError('Country should be at least 3 chars')
        if len(value) > 16:
            raise ValueError('Country shouldn\'t be longer than 16 chars')
        return value


class UserCreate(User):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    gender: str
    country: str


class UserUpdate(User):
    pass
