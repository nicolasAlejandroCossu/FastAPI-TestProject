from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path

from src.responses.responses import error_response, success_response
from src.models.user_model import User, UserCreate, UserUpdate

users: List[User] = [
    User(
        id=1,
        username='cossu.07',
        country='Argentina'
    ),
    User(
        id=2,
        username='testUser',
        country='Argentina'
    ),
    User(
        id=3,
        username='newUser',
        country='United States'
    )
]

user_router = APIRouter()


@user_router.get('/', tags=['Users'])
def get_users() -> JSONResponse:

    response_content = [obj.model_dump() for obj in users]
    return success_response(status_code=200, data=response_content)


@user_router.get('/by_country', tags=['Users'])
def get_users_by_country(country: str) -> JSONResponse:

    userslist: List[User] = []
    for user in users:
        if user.country == country:
            userslist.append(user)
    if userslist:
        response = [user.model_dump() for user in userslist]
        return success_response(status_code=200, data=response, message="Users list found")

    return success_response(status_code=200, data=[], message="Haven't found users from that country")


@user_router.get('/{id}', tags=['Users'])
def get_user(id: int = Path(gt=0)) -> JSONResponse:

    for user in users:
        if user.id == id:
            response_content = user.model_dump()
            return success_response(status_code=200, data=response_content, message="User found")

    return error_response(status_code=404, message="User not found")


@user_router.post('/', tags=['Users'])
def create_user(obj: UserCreate):

    users.append(obj)
    return success_response(status_code=201, message="User created")


@user_router.put('/{id}', tags=['Users'])
def update_user(id: int, obj: UserUpdate) -> JSONResponse:

    if len(obj.model_dump()) != len(obj.model_dump(exclude_none=True)):
        return error_response(status_code=400, message="Wrong format request, missing data")

    for user in users:
        if user.id == id:
            user.id = obj.id
            user.username = obj.username
            user.country = obj.country
            return success_response(status_code=200, message="User has been edited")

    return error_response(status_code=404, message="User not found")


@user_router.patch('/{id}/username', tags=['Users'])
def update_user_username(id: int, obj: UserUpdate) -> JSONResponse:

    if obj.username == None:
        return error_response(status_code=400, message="Wrong format request, missing data")

    for user in users:
        if user.id == id:
            user.username = obj.username
            return success_response(status_code=200, message="User username patched")

    return error_response(status_code=404, message="User not found")


@user_router.patch('/{id}/country', tags=['Users'])
def update_user_country(id: int, obj: UserUpdate) -> JSONResponse:

    if obj.username == None:
        return error_response(status_code=400, message="Wrong format request, missing data")

    for user in users:
        if user.id == id:
            user.country = obj.country
            return success_response(status_code=200, message="User country patched")

    return error_response(status_code=404, message="User not found")


@user_router.delete('/{id}', tags=['Users'])
def delete_user(id: int) -> JSONResponse:

    for user in users:
        if user.id == id:
            users.remove(user)
            return success_response(status_code=200, message="User deleted")

    return error_response(status_code=404, message="User not found")
