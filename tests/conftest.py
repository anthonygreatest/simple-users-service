import os

import dotenv
import pytest
import requests

from app.models.user import User
from app.dataclasses.added_user import AddedUserData
from app.helper import generate_random_user_data


#читает файл дотэнв и устаналивает переменные среды
@pytest.fixture(scope='session')
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope='session')
def app_url(envs):
    return os.getenv('APP_URL')

@pytest.fixture
def get_users(app_url):
    response = requests.get(
        f'{app_url}/api/users/'
    )

    users = response.json()

    return users

@pytest.fixture
def added_user(request, app_url):

    user_data = generate_random_user_data()

    response = requests.post(
        url=f"{app_url}/api/users/",
        json=user_data.model_dump(mode='json')
    )

    raw_data = response.json()
    new_user = User(**raw_data)

    yield AddedUserData(
        raw_response=response,
        new_user=new_user,
        user_data=user_data
    )
    if 'delete_user' in request.keywords:
        requests.delete(url=f"{app_url}/api/users/{new_user.id}")


