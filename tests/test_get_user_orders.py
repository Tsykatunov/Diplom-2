import requests
import allure
from conftest import BASE_URL
from conftest import INGREDIENTS

@allure.epic('Get User Orders')
class TestGetUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized(self, create_user, login_user, delete_user):
        email = 'SonicTheHedgehog@yandex.ru'
        password = 'GottaGoFast'
        name = 'Sonic'

        # Создаем пользователя и получаем токен
        create_user(email, password, name)
        login_response = login_user(email, password)
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        # Создаем заказ
        payload = {'ingredients': INGREDIENTS}
        requests.post(f'{BASE_URL}/orders', headers=headers, json=payload)

        # Получаем заказы пользователя
        response = requests.get(f'{BASE_URL}/orders', headers=headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True
        assert len(response_data.get('orders')) > 0

        # Удаляем пользователя после теста
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_orders_unauthorized(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'You should be authorised'