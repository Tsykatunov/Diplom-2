import pytest
import requests

BASE_URL = 'https://stellarburgers.nomoreparties.site/api'
INGREDIENTS = ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa6f']  # ингредиенты

@pytest.fixture(scope='function')
def create_user():
    def _create_user(email, password, name):
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        return response

    return _create_user


@pytest.fixture(scope='function')
def login_user():
    def _login_user(email, password):
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        return response

    return _login_user


@pytest.fixture(scope='function')
def delete_user():
    def _delete_user(token):
        headers = {'Authorization': token}
        response = requests.delete(f'{BASE_URL}/auth/user', headers=headers)
        return response

    return _delete_user