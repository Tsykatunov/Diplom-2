import requests
import allure
from data.urls import ApiEndpoints
from data.user_data import TestUsers, TestIngredients
from data.response_messages import ResponseMessages

@allure.epic('Order Creation')
class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_authorized(self, create_user, login_user, delete_user):
        user = TestUsers.SONIC
        
        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': TestIngredients.VALID_INGREDIENTS}
        
        response = requests.post(ApiEndpoints.ORDERS, headers=headers, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized(self):
        payload = {'ingredients': TestIngredients.VALID_INGREDIENTS}
        response = requests.post(ApiEndpoints.ORDERS, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_no_ingredients(self, create_user, login_user, delete_user):
        user = TestUsers.SONIC
        
        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': []}

        response = requests.post(ApiEndpoints.ORDERS, headers=headers, json=payload)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.INGREDIENTS_REQUIRED

        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredient_hash(self, create_user, login_user, delete_user):
        user = TestUsers.SONIC
        
        create_user(user['email'], user['password'], user['name'])
        login_response = login_user(user['email'], user['password'])
        token = login_response.json().get('accessToken')
        headers = {'Authorization': token}

        payload = {'ingredients': TestIngredients.INVALID_INGREDIENTS}

        response = requests.post(ApiEndpoints.ORDERS, headers=headers, json=payload)
        assert response.status_code == 500

        delete_response = delete_user(token)
        assert delete_response.status_code == 202