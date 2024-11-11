import pytest
import requests
import allure
from data.urls import ApiEndpoints
from data.user_data import TestUsers
from data.response_messages import ResponseMessages

@allure.epic('User Creation')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, create_user, delete_user):
        user = TestUsers.SONIC

        with allure.step('Создаем уникального пользователя'):
            response = create_user(user['email'], user['password'], user['name'])
            assert response.status_code == 200
            response_data = response.json()
            assert response_data.get('success') is True

        with allure.step('Удаляем пользователя после теста'):
            token = response_data.get('accessToken')
            delete_response = delete_user(token)
            assert delete_response.status_code == 202

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, create_user, delete_user):
        user = TestUsers.SONIC

        response_first = create_user(user['email'], user['password'], user['name'])
        assert response_first.status_code == 200
        token = response_first.json().get('accessToken')

        response_second = create_user(user['email'], user['password'], user['name'])
        assert response_second.status_code == 403
        response_data = response_second.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.USER_EXISTS

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Создание пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, field):
        user_data = TestUsers.SONIC.copy()
        user_data.pop(field)

        response = requests.post(ApiEndpoints.REGISTER, json=user_data)
        assert response.status_code == 403
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.MISSING_FIELDS