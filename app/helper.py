import json
import random

import requests

from .models.user import UserCreate
from .paths import USER_DATA


def get_users_ids(app_url, page, size):

    response = requests.get(
        f'{app_url}/api/users?page={page}&size={size}'
    )

    users = response.json()['items']

    users_ids = sorted(user['id'] for user in users)

    return users_ids

def generate_random_user_data():

    users = []

    with open(USER_DATA) as f:
        test_data_users = json.load(f)

    for user in test_data_users:
        users.append(user)

    return UserCreate(**random.choice(users))

