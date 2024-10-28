import pytest
import requests
import allure
from conftest import BASE_URL

@allure.epic('User Creation')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, create_user, delete_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        with allure.step('Создаем уникального пользователя'):
            response = create_user(email, password, name)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data.get('success') is True

        with allure.step('Удаляем пользователя после теста'):
            token = response_data.get('accessToken')
            delete_response = delete_user(token)
            assert delete_response.status_code == 202

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, create_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        # Создаем пользователя первый раз
        response_first = create_user(email, password, name)
        assert response_first.status_code == 200
        token = response_first.json().get('accessToken')

        # Пытаемся создать того же пользователя еще раз
        response_second = create_user(email, password, name)
        assert response_second.status_code == 403
        response_data = response_second.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'User already exists'

        # Удаляем пользователя после теста
        delete_user = requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})
        assert delete_user.status_code == 202

    @allure.title('Создание пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, field, create_user):
        user_data = {
            'email': 'ShadowTheHedgehog@yandex.ru',
            'password': 'GottaGoFast',
            'name': 'Shadow'
        }
        user_data.pop(field)

        response = requests.post(f'{BASE_URL}/auth/register', json=user_data)
        assert response.status_code == 403
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'Email, password and name are required fields'