import allure
from faker import Faker
from api_project.models.store import OrderModel

faker = Faker()

@allure.feature("Управление магазином (Store)")
@allure.story("Позитивные сценарии")
@allure.title("Создание и получение заказа на существующего питомца")
def test_create_order(store_client, new_order):
    order_id, payload = new_order
    get_response = store_client.get_order_by_id(order_id)
    assert get_response.status_code == 200, f"Ожидался статус 200, а получили: {get_response.status_code}"
    body = OrderModel(**get_response.json())
    assert body.id == order_id, f"Ожидался ID заказа {order_id}, а получили: {body.id}"
    assert body.petId == payload["petId"], f"Ожидался petId {payload["petId"]}, а получили: {body.petId}"
    assert body.quantity == payload["quantity"], f"Ожидался quantity {payload["quantity"]}, а получили: {body.quantity}"
    assert body.status == payload["status"], f"Ожидался status {payload["status"]}, а получили: {body.status}"

@allure.feature("Управление магазином (Store)")
@allure.story("Инвентарь магазина")
@allure.title("Получение инвентаря магазина")
def test_get_store_inventory(store_client):
    response = store_client.get_inventory()
    assert response.status_code == 200, f"Ожидался статус 200, а получили: {response.status_code}"
    inventory_body = response.json()
    assert isinstance(inventory_body, dict), f"Ожидался словарь, а получили {type(inventory_body)}"
    assert "available" in inventory_body, "В инвентаре отсутствует ключ available"
    assert isinstance(inventory_body["available"], int), f"Количество доступных животных должно быть int, а имеем: {type(inventory_body['available'])}"

@allure.feature("Управление магазином (Store)")
@allure.story("Позитивные сценарии")
@allure.title("Удаление заказа и проверка его отсутствия")
def test_delete_order(store_client, new_order):
    order_id, payload = new_order
    delete_response = store_client.delete_order_by_id(order_id)
    assert delete_response.status_code == 200, f"Ожидался статус 200, а получили: {delete_response.status_code}"
    get_response = store_client.get_order_by_id(order_id)
    assert get_response.status_code == 404, f"Ожидался статус 404, а получили: {get_response.status_code}"

@allure.feature("Управление магазином (Store)")
@allure.story("Негативные сценарии")
@allure.title("Поиск несуществующего заказа по ID (404)")
def test_get_non_existing_order(store_client):
    non_existing_order_id = 9999999999999999999
    response = store_client.get_order_by_id(non_existing_order_id)
    assert response.status_code == 404, f"Ожидался статус 404, а получили: {response.status_code}"

@allure.feature("Управление магазином (Store)")
@allure.story("Негативные сценарии")
@allure.title("Поиск несуществующего заказа по ID (404)")
def test_delete_non_existing_order(store_client):
    non_existing_order_id = 9999999999999999999
    response = store_client.delete_order_by_id(non_existing_order_id)
    assert response.status_code == 404, f"Ожидался статус 404, а получили: {response.status_code}"