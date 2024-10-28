import requests
import allure
from conftest import BASE_URL
from conftest import INGREDIENTS

@allure.epic('Order Creation')
class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_authorized(self, create_user, login_user, delete_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': INGREDIENTS}

        response = requests.post(f'{BASE_URL}/orders', headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized(self):
        payload = {'ingredients': INGREDIENTS}
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_no_ingredients(self, create_user, login_user, delete_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': []}

        response = requests.post(f'{BASE_URL}/orders', headers=headers, json=payload)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'Ingredient ids must be provided'

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredient_hash(self, create_user, login_user, delete_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': ['SomeWrongHashStuff']}

        response = requests.post(f'{BASE_URL}/orders', headers=headers, json=payload)
        assert response.status_code == 500

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202