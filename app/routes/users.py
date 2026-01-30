from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException
from ..database import users
from ..models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix='/api/users')


#когда прилетит запрос на этот путь, вызови функцию
@router.get(path='/{user_id}', status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid user')

    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return user

@router.get(path='/', status_code=HTTPStatus.OK)
def get_users() -> Iterable[User]:
    return users.get_users()

@router.post(path='/', status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate) -> User:
    user = User.model_validate(user.model_dump())
    return users.create_user(user)

@router.patch(path='/{user_id}', status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user_endpoint(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    user = users.get_user(user_id)
    users.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return {'detail': 'User deleted'}

