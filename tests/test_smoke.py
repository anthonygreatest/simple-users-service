from http import HTTPStatus

import requests


def test_app_running(app_url):

    response = requests.get(
        url=f'{app_url}/status'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['database'] == True