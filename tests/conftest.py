import pytest
import requests
from data.urls import ApiEndpoints

@pytest.fixture(scope='function')
def create_user():
    def _create_user(email, password, name):
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.post(ApiEndpoints.REGISTER, json=payload)
        return response
    return _create_user


@pytest.fixture(scope='function')
def login_user():
    def _login_user(email, password):
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(ApiEndpoints.LOGIN, json=payload)
        return response

    return _login_user


@pytest.fixture(scope='function')
def delete_user():
    def _delete_user(token):
        headers = {'Authorization': token}
        response = requests.delete(ApiEndpoints.USER, headers=headers)
        return response

    return _delete_user