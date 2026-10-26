import allure
from api_project.clients.base_client import BaseClient
from api_project.utils.endpoints import Endpoints

class PetClient(BaseClient):
    @allure.step("Создание питомца")
    def create_pet(self, payload):
        return self._request("POST", Endpoints.PET, json=payload)
    @allure.step("Получение питомца по ID: {pet_id}")
    def get_pet_by_id(self, pet_id):
        return self._request("GET", f"{Endpoints.PET.value}/{pet_id}")
    @allure.step("Удаление питомца по ID: {pet_id}")
    def delete_pet_by_id(self, pet_id):
        return self._request("DELETE", f"{Endpoints.PET.value}/{pet_id}")
    @allure.step("Обновление питомца")
    def update_pet(self, payload):
        return self._request("PUT", Endpoints.PET, json=payload)
    @allure.step("Поиск питомца по статусу: {status}")
    def find_pet_by_status(self, status: str):
        return self._request("GET", Endpoints.PET_FIND_BY_STATUS, params={"status": status})