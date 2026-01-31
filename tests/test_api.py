from http import HTTPStatus

import pytest
import requests

from app.helper import get_users_ids, generate_random_user_data
from app.models.user import User

@pytest.mark.delete_user
def test_users(app_url):
    response = requests.get(
        f'{app_url}/api/users/'
    )
    users = response.json()
    for user in users:
        User.model_validate(user)

    assert response.status_code == HTTPStatus.OK

@pytest.mark.delete_user
def test_user_can_be_found(app_url, added_user):

    user_id = added_user.new_user.id

    response = requests.get(
        f'{app_url}/api/users/{user_id}'
    )

    user = response.json()

    User.model_validate(user)

    assert response.status_code == HTTPStatus.OK

@pytest.mark.delete_user
def test_user_can_be_created(app_url, added_user):

    data_to_send = added_user.user_data
    response = added_user.raw_response
    user_in_response = added_user.new_user

    User.model_validate(user_in_response)

    assert response.status_code == HTTPStatus.CREATED

    assert data_to_send.email == user_in_response.email
    assert data_to_send.avatar == user_in_response.avatar
    assert data_to_send.last_name == user_in_response.last_name
    assert data_to_send.first_name == user_in_response.first_name

@pytest.mark.delete_user
def test_user_data_can_be_updated(app_url, added_user):

    user_id = added_user.new_user.id

    new_data = generate_random_user_data()

    response = requests.patch(
        url=f'{app_url}/api/users/{user_id}',
        json=new_data.model_dump(mode='json')
    )

    validated_response = User.model_validate(response.json())

    assert response.status_code == HTTPStatus.OK

    assert new_data.email == validated_response.email
    assert new_data.avatar == validated_response.avatar
    assert new_data.first_name == validated_response.first_name
    assert new_data.last_name == validated_response.last_name
    assert user_id == validated_response.id

def test_user_can_be_deleted(app_url, added_user):

    user_id = added_user.new_user.id

    response = requests.delete(
        url=f"{app_url}/api/users/{user_id}",
    )

    double_check_response = requests.get(
        url=f"{app_url}/api/users/{user_id}",
    )

    assert response.json()['detail'] == 'User deleted'
    assert response.status_code == HTTPStatus.OK
    assert double_check_response.json()['detail'] == 'User not found'


@pytest.mark.parametrize('user_id, expected_status', [
    [0, HTTPStatus.UNPROCESSABLE_ENTITY],
    [13, HTTPStatus.NOT_FOUND],
    ['abc', HTTPStatus.UNPROCESSABLE_ENTITY]
])
def test_invalid_user(app_url, user_id, expected_status):
    response = requests.get(
        f'{app_url}/api/users/{user_id}'
    )

    assert response.status_code == expected_status

def test_returns_unique_users(get_users):

    users_ids = [user['id'] for user in get_users]

    assert len(users_ids) == len(set(users_ids))
#
# @pytest.mark.parametrize('size, page, expected_pages', [
#     (5, 2, 3),
#     (1, 5, 12)
# ])
# def test_pagination(app_url, size, page, expected_pages):
#
#     response = requests.get(
#         f'{app_url}/api/users?page={page}&size={size}'
#     )
#
#     users = response.json()['items']
#     for user in users:
#         User.model_validate(user)
#
#     assert response.json()['page'] == page
#     assert response.json()['size'] == size
#     assert response.json()['pages'] == expected_pages
#     assert len(users) == size
#
#
# def test_pagination_returns_unique_data_on_each_page(app_url):
#
#     first_page_users = get_users_ids(
#         app_url=app_url,
#         size=4,
#         page=1
#     )
#     second_page_users = get_users_ids(
#         app_url=app_url,
#         size=4,
#         page=2
#     )
#     third_page_users = get_users_ids(
#         app_url=app_url,
#         size=4,
#         page=3
#     )
#
#     assert first_page_users != second_page_users
#     assert second_page_users != third_page_users
#     assert first_page_users != third_page_users
#
# @pytest.mark.parametrize('size, page, expected_pages, expected_response', [
#     (0, 0, 0, HTTPStatus.UNPROCESSABLE_ENTITY),
#     (13, 1, 12, HTTPStatus.BAD_REQUEST),
#     (3, 5, 12, HTTPStatus.BAD_REQUEST),
#     ('abc', 5, 12, HTTPStatus.UNPROCESSABLE_ENTITY),
#     (3, 'abc', 12, HTTPStatus.UNPROCESSABLE_ENTITY),
#     # (3, 4, 5) #wrong count
# ])
# def test_invalid_pagination(app_url, size, page, expected_pages, expected_response):
#
#     response = requests.get(
#         f'{app_url}/api/users?page={page}&size={size}'
#     )
#     print(response.json())
#
#     assert response.status_code == expected_response