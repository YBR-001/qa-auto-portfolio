import allure
from api_project.clients.base_client import BaseClient
from api_project.utils.endpoints import Endpoints

class StoreClient(BaseClient):
    @allure.step("Оформление заказа на питомца")
    def place_order(self, payload):
        return self._request("POST", Endpoints.STORE_ORDER, json=payload)
    @allure.step("Получение заказа по ID: {order_id}")
    def get_order_by_id(self, order_id):
        return self._request("GET", f"{Endpoints.STORE_ORDER.value}/{order_id}")
    @allure.step("Удаление заказа по ID: {order_id}")
    def delete_order_by_id(self, order_id):
        return self._request("DELETE", f"{Endpoints.STORE_ORDER.value}/{order_id}")
    @allure.step("Получение инвентаря питомца")
    def get_inventory(self):
        return self._request("GET", Endpoints.STORE_INVENTORY)