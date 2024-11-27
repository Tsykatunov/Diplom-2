import pytest
import requests
import allure
from data.urls import ApiEndpoints
from data.user_data import TestUsers
from data.response_messages import ResponseMessages

@allure.epic('User Data Modification')
class TestUserChanges:

    @allure.title('Изменение данных (email или name) пользователя с авторизацией')
    @pytest.mark.parametrize('field, new_value', [
        ('email', 'emerlehegizoidrobot@yandex.ru'),
        ('name', 'Emerl'),
    ])
    def test_change_user_data_email_or_name_authorized(self, field, new_value, create_user, login_user, delete_user):
        user = TestUsers.METAL_SONIC

        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {field: new_value}
        response = requests.patch(ApiEndpoints.USER, headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True
        assert response_data['user'][field] == new_value

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Изменение данных (password) пользователя с авторизацией')
    def test_change_user_data_password_authorized(self, create_user, login_user, delete_user):
        user = TestUsers.METAL_SONIC

        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'password': 'GottaGoFaster'}
        response = requests.patch(ApiEndpoints.USER, headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Изменение данных пользователя без авторизации')
    @pytest.mark.parametrize('field, new_value', [
        ('email', 'roguethebat@yandex.ru'),
        ('name', 'Rogue'),
        ('password', 'GottaStealFast')
    ])
    def test_change_user_data_unauthorized(self, field, new_value):
        payload = {field: new_value}
        response = requests.patch(ApiEndpoints.USER, json=payload)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.UNAUTHORIZED


