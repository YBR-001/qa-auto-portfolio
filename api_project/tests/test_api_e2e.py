import pytest, allure
from api_project.models.pet import PetModel
from api_project.models.user import UserModel
from api_project.models.store import OrderModel
from faker import Faker

faker = Faker()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Smoke - основные бизнес-процессы")
@allure.title("Полный цикл покупки питомца авторизованным пользователям")
@pytest.mark.smoke
def test_full_purchase_lifecycle(user_client, pet_client, store_client, new_user, new_pet, new_order):
    username, user_payload = new_user
    pet_id, pet_payload = new_pet
    order_id, order_payload = new_order
    login_response = user_client.login_user(username, user_payload)
    assert login_response.status_code == 200, f"Ожидался статус 200, а получили: {login_response.status_code}"
    pet_info = pet_client.get_pet_by_id(pet_id)
    assert pet_info.status_code == 200, f"Ожидался статус 200, а получили: {pet_info.status_code}"
    pet_body = PetModel(**pet_info.json())
    assert pet_body.status == "available", f"Питомец не доступен для заказа"
    order_info = store_client.get_order_by_id(order_id)
    assert order_info.status_code == 200, f"Ожидался статус 200, а получили {order_info.status_code}"
    order_body = OrderModel(**order_info.json())
    assert order_body.petId == pet_id, f"Название питомца не совпало. Ожидали {pet_id}, а получили: {order_body.petId}"
    updated_pet_payload = pet_payload.copy()
    updated_pet_payload["status"] = "sold"
    updated_response = pet_client.update_pet(updated_pet_payload)
    assert updated_response.status_code == 200, f"Ожидался статус 200, а получили: {updated_response.status_code}"
    sold_pet_response = pet_client.get_pet_by_id(pet_id)
    assert sold_pet_response.status_code == 200, f"Ожидался статус 200, а получили: {sold_pet_response.status_code}"
    sold_pet_body = PetModel(**sold_pet_response.json())
    assert sold_pet_body.status == "sold", f"Ожидался статус sold, а получили {sold_pet_body.status}"
    logout_response = user_client.logout_user()
    assert logout_response.status_code == 200, f"Ожидался статус 200, а получили {logout_response.status_code}"

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regression — расширенные сценарии")
@allure.title("Отмена заказа и возврат зарезервированного питомца в продажу")
@pytest.mark.regression
def test_order_cancel_and_return_pet(pet_client, store_client, new_pet, new_order):
    pet_id, pet_payload = new_pet
    order_id, order_payload = new_order
    order_info = store_client.get_order_by_id(order_id)
    assert order_info.status_code == 200, f"Ожидался статус 200, а получили: {order_info.status_code}"
    pending_pet_payload = pet_payload.copy()
    pending_pet_payload["status"] = "pending"
    pending_response = pet_client.update_pet(pending_pet_payload)
    assert pending_response.status_code == 200, f"Ожидался статус 200, а получили: {pending_response.status_code}"
    pending_pet_body = PetModel(**pending_response.json())
    assert pending_pet_body.status == "pending", f"Статус не изменился. Ожидался статус pending, а получили: {pending_pet_body.status}"
    cancel_order = store_client.delete_order_by_id(order_id)
    assert cancel_order.status_code == 200, f"Ожидался статус 200, а получили {cancel_order.status_code}"
    get_resp_order = store_client.get_order_by_id(order_id)
    assert get_resp_order.status_code == 404, f"Ожидался статус 404, а получили {get_resp_order.status_code}"
    available_payload = pet_payload.copy()
    available_payload["status"] = "available"
    available_response = pet_client.update_pet(available_payload)
    assert available_response.status_code == 200, f"Ожидался статус 200, а получили: {available_response.status_code}"
    get_resp_pet = pet_client.get_pet_by_id(pet_id)
    assert get_resp_pet.status_code == 200, f"Ожидался статус 200, а получили {get_resp_pet.status_code}"
    get_pet_body = PetModel(**get_resp_pet.json())
    assert get_pet_body.status == "available", f"Статус не обновился! Ожидался статус available, а получили {get_pet_body.status}"

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regression — расширенные сценарии")
@allure.title("Полный жизненный цикл аккаунта пользователя от регистрации до удаления")
@pytest.mark.regression
def test_user_account_full_lifecycle(user_client, new_user):
    username, user_payload = new_user
    user_info = user_client.get_info_user_by_username(username)
    assert user_info.status_code == 200, f"Ожидался статус 200, а получили: {user_info.status_code}"
    login_response = user_client.login_user(username, user_payload["password"])
    assert login_response.status_code == 200, f"Ожидался статус 200, а получили {login_response.status_code}"
    new_password = faker.password()
    new_first_name = "ChangeFirstName"
    change_payload = user_payload.copy()
    change_payload["firstName"], change_payload["password"] = new_first_name, new_password
    change_response = user_client.update_user(username, change_payload)
    assert change_response.status_code == 200, f"Ожидался статус 200, а получили: {change_response.status_code}"
    get_resp_user = user_client.get_info_user_by_username(username)
    assert get_resp_user.status_code == 200, f"Ожидался статус 200, а получили: {get_resp_user.status_code}"
    fetched_user = UserModel(**get_resp_user.json())
    assert fetched_user.firstName == new_first_name, f"Имя не обновилось! Ожидалось {new_first_name}, а получили {fetched_user.firstName}"
    assert fetched_user.password == new_password, f"Пароль не обновился! Ожидался {new_password}, а получили {fetched_user.password}"
    logout_response = user_client.logout_user()
    assert logout_response.status_code == 200, f"Ожидался статус 200, а получили {logout_response.status_code}"