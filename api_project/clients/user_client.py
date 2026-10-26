import allure

from api_project.clients.base_client import BaseClient
from api_project.utils.endpoints import Endpoints

class UserClient(BaseClient):
    @allure.step("Создание пользователя")
    def create_user(self, payload):
        return self._request("POST", Endpoints.USER, json=payload)
    @allure.step("Получение информации о пользователе по username: {username}")
    def get_info_user_by_username(self, username):
        return self._request("GET", f"{Endpoints.USER.value}/{username}")
    @allure.step("Обновление пользователя: {username}")
    def update_user(self, username, payload):
        return self._request("PUT", f"{Endpoints.USER.value}/{username}", json=payload)
    @allure.step("Удаление пользователя: {username}")
    def delete_user_by_username(self, username):
        return self._request("DELETE", f"{Endpoints.USER.value}/{username}")
    @allure.step("Пользователь входит в систему: {username}")
    def login_user(self, username, password):
        return self._request("GET", Endpoints.USER_LOGIN, params={"username": username, "password": password})
    @allure.step("Пользователь выходит из системы")
    def logout_user(self):
        return self._request("GET", Endpoints.USER_LOGOUT)
    @allure.step("Создание списка пользователей")
    def create_user_with_list(self, payload):
        return self._request("POST", Endpoints.USER_CREATE_WITH_LIST, json=payload)