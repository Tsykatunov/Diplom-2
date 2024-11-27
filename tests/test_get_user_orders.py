import requests
import allure
from data.urls import ApiEndpoints
from data.user_data import TestUsers, TestIngredients
from data.response_messages import ResponseMessages

@allure.epic('Get User Orders')
class TestGetUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized(self, create_user, login_user, delete_user):
        user = TestUsers.SONIC

        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': TestIngredients.VALID_INGREDIENTS}
        requests.post(ApiEndpoints.ORDERS, headers=headers, json=payload)

        response = requests.get(ApiEndpoints.ORDERS, headers=headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True
        assert len(response_data.get('orders')) > 0

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_orders_unauthorized(self):
        response = requests.get(ApiEndpoints.ORDERS)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.UNAUTHORIZED