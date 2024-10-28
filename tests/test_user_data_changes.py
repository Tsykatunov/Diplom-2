import pytest
import requests
import allure
from conftest import BASE_URL

@allure.epic('User Data Modification')
class TestUserChanges:

    @allure.title('Изменение данных (email или name) пользователя с авторизацией')
    @pytest.mark.parametrize('field, new_value', [
        ('email', 'emerlehegizoidrobot@yandex.ru'),
        ('name', 'Emerl'),
    ])
    def test_change_user_data_email_or_name_authorized(self, field, new_value, create_user, login_user, delete_user):
        email = 'MetalSonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'MetalSonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        # Изменяем данные пользователя
        payload = {field: new_value}
        response = requests.patch(f'{BASE_URL}/auth/user', headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True
        assert response_data['user'][field] == new_value

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Изменение данных (password) пользователя с авторизацией')
    def test_change_user_data_password_authorized(self, create_user, login_user, delete_user):
        email = 'MetalSonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'MetalSonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        # Изменяем данные пользователя
        payload = {'password': 'GottaGoFaster'}
        response = requests.patch(f'{BASE_URL}/auth/user', headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Изменение данных пользователя без авторизации')
    @pytest.mark.parametrize('field, new_value', [
        ('email', 'roguethebat@yandex.ru'),
        ('name', 'Rogue'),
        ('password', 'GottaStealFast')
    ])
    def test_change_user_data_unauthorized(self, field, new_value):
        # Пытаемся изменить данные без токена
        payload = {field: new_value}
        response = requests.patch(f'{BASE_URL}/auth/user', json=payload)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'You should be authorised'


