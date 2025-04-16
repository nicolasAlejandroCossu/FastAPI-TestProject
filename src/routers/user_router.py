from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.models.user_model import User
from src.database import get_db
from src.responses.responses import error_response, success_response
from src.schemas.user_schema import BaseUser, UserCreate, UserResponse, UserUpdate

user_router = APIRouter()


"""
---- GET USERS LIST ---- 
"""

@user_router.get('/', tags=['Users'])
def get_users(db: Session = Depends(get_db)) -> JSONResponse:

    users = db.query(User).all()
    response = [UserResponse.model_validate(user).model_dump() for user in users]
    return success_response(status_code=200, data=response)


"""
---- GET USERS LIST BY COUNTRY ---- 
"""

@user_router.get('/by_country', tags=['Users'])
def get_users_by_country(country: str, db: Session = Depends(get_db)) -> JSONResponse:

    users = db.query(User).filter(User.country == country)

    response = [UserResponse.model_validate(user).model_dump() for user in users]

    if not response:
        return success_response(status_code=200, data=[], message="Haven't found users from that country")

    return success_response(status_code=200, data=response, message="Users list found")


"""
---- GET USERS BY USERNAME LIKE ----
"""

@user_router.get('/by_user', tags=['Users'])
def get_users_by_username(username: str, db: Session = Depends(get_db)) -> JSONResponse:

    users = db.query(User).filter(User.username.like(f'%{username}%'))

    response = [UserResponse.model_validate(user).model_dump() for user in users]

    if not response:
        return success_response(status_code=200, data=[], message="Haven't found username matches")

    return success_response(status_code=200, data=response, message="Users list found")


"""
---- GET USER BY ID ---- 
"""

@user_router.get('/{id}', tags=['Users'])
def get_user(id: int = Path(ge=0), db: Session = Depends(get_db)) -> JSONResponse:

    user = db.query(User).filter(User.id == id).first()

    if not user:
        return success_response(status_code=200, data={}, message="Haven't found a user with that id")

    response = UserResponse.model_validate(user).model_dump()

    return success_response(status_code=200, data=response, message="User found")


"""
---- CREATE USER ---- 
"""

@user_router.post('/', tags=['Users'])
def create_user(obj: UserCreate, db: Session = Depends(get_db)):

    user = User(
        id=obj.id,
        username=obj.username,
        firstname=obj.firstname,
        lastname=obj.lastname,
        age=obj.age,
        gender=obj.gender,
        country=obj.country
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response(status_code=201, message="User created")


"""
---- EDIT USER ---- 
"""

@user_router.put('/{id}', tags=['Users'])
def update_user(id: int, obj: UserUpdate, db: Session = Depends(get_db)) -> JSONResponse:

    if obj.model_dump(exclude_none=True).keys() != BaseUser.__annotations__.keys():
        return error_response(status_code=400, message="Request must include all fields")

    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return error_response(status_code=404, message="User not found")

    for key, value in obj.model_dump().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return success_response(status_code=200, message="User has been edited")


"""
---- PATCH USER ---- 
"""

@user_router.patch("/{id}", tags=["Users"])
def patch_user(id: int, obj: UserUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return error_response(status_code=404, message="User not found")

    updated_data = obj.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return success_response(status_code=200, message="User patched")


"""
---- DELETE USER ---- 
"""

@user_router.delete('/{id}', tags=['Users'])
def delete_user(id: int, db: Session = Depends(get_db)) -> JSONResponse:

    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return error_response(status_code=404, message="User not found")

    db.delete(user)
    db.commit()

    return success_response(status_code=200, message="User deleted")
