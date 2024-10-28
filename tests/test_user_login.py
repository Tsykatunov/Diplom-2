import requests
import allure
from conftest import BASE_URL

@allure.epic('User Login')
class TestUserLogin:

    @allure.title('Логин под существующим пользователем')
    def test_login_existing_user(self, create_user):
        email = 'MilesTailsPrower@yandex.ru'
        password = 'GottaFlyFast'
        name = 'Tails'

        # Создаем пользователя
        create_user(email, password, name)

        payload = {
            'email': email,
            'password': password
        }

        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

        # Удаляем пользователя после теста
        token = response_data.get('accessToken')
        delete_user = requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})
        assert delete_user.status_code == 202

    @allure.title('Логин с неверным логином и паролем')
    def test_login_invalid_credentials(self):
        payload = {
            'email': 'ThereIsNoWayAnyoneWillEverUseThisSuchAFreakingLongNameForTestsHereSoIAmDefinitelyGoingToUseItForSure@goddamn.ru',
            'password': 'IWontBeMakingSuchMessAsCreatingEmailButStillItShouldBeNeverToBeUsedByAnyoneEverLOL'
        }

        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == 'email or password are incorrect'