import requests
import allure
from data.urls import ApiEndpoints
from data.user_data import TestUsers
from data.response_messages import ResponseMessages

@allure.epic('User Login')
class TestUserLogin:

    @allure.title('Логин под существующим пользователем')
    def test_login_existing_user(self, create_user, delete_user):
        user = TestUsers.TAILS

        create_user(user['email'], user['password'], user['name'])

        payload = {
            'email': user['email'],
            'password': user['password']
        }

        response = requests.post(ApiEndpoints.LOGIN, json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        token = response_data.get('accessToken')
        delete_response = delete_user(token)
        assert delete_response.status_code == 202

    @allure.title('Логин с неверным логином и паролем')
    def test_login_invalid_credentials(self):
        payload = {
            'email': 'ThereIsNoWayAnyoneWillEverUseThisSuchAFreakingLongNameForTestsHereSoIAmDefinitelyGoingToUseItForSure@goddamn.ru',
            'password': 'IWontBeMakingSuchMessAsCreatingEmailButStillItShouldBeNeverToBeUsedByAnyoneEverLOL'
        }

        response = requests.post(ApiEndpoints.LOGIN, json=payload)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == ResponseMessages.INVALID_CREDENTIALS