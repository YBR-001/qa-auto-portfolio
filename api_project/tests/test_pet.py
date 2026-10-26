import allure, pytest
from faker import Faker
from api_project.models.pet import PetModel, ApiResponseModel

fake = Faker()

@allure.feature("Управление питомцами (PET)")
@allure.story("Позитивные сценарии")
@allure.title("Создание и получение питомца по ID")
def test_create_and_get_pet(pet_client, new_pet):
    pet_id, payload = new_pet
    get_response = pet_client.get_pet_by_id(pet_id)
    assert get_response.status_code == 200, f"Ожидался статус 200, а получили: {get_response.status_code}"
    fetched_pet = PetModel(**get_response.json())
    assert fetched_pet.model_dump() == payload, f"Данные питомца не совпадают! Ожидалось {payload}, а получили {fetched_pet.model_dump()}"

@allure.feature("Управление питомцами (PET)")
@allure.story("Позитивные сценарии")
@allure.title("Обновление данных существующего питомца")
def test_update_pet(pet_client, new_pet):
    pet_id, pet_payload = new_pet
    update_payload = pet_payload.copy()
    update_payload["name"], update_payload["status"] = "UpdatedName", "sold"
    update_response = pet_client.update_pet(update_payload)
    assert update_response.status_code == 200, f"Ожидался 200, но получили: {update_response.status_code}"
    get_response = pet_client.get_pet_by_id(pet_id)
    assert get_response.status_code == 200, f"Ожидался статус 200, а получили: {get_response.status_code}"
    fetched_body = PetModel(**get_response.json())
    assert fetched_body.name == "UpdatedName", f"Имя не обновилось! Ожидалось 'UpdatedName', а получили {fetched_body.name}"
    assert fetched_body.status == "sold", f"Обновление питомца не произошло: {fetched_body.status}"

@allure.feature("Управление питомцами (PET)")
@allure.story("Поиск и фильтрация")
@allure.title("Поиск и фильтрация по статусу: {status}")
@pytest.mark.parametrize('status', ["sold", "available", "pending"])
def test_find_pet_by_status(pet_client, status):
    response = pet_client.find_pet_by_status(status)
    assert response.status_code == 200, f"Ожидался статус 200, а получили: {response.status_code}"
    pets_lst = response.json()
    assert isinstance(pets_lst, list), f"Ожидался список, а получили {type(pets_lst)}"
    assert len(pets_lst) > 0, f"Список со статусом {status} пуст"
    for pet_data in pets_lst[:5]:
        pet = PetModel(**pet_data)
        assert pet.status == status, f"Ожидался статус {status}, а получили {pet.status}"

@allure.feature("Управление питомцами (PET)")
@allure.story("Позитивные сценарии")
@allure.title("Удаление питомца и проверка его отсутствия")
def test_delete_pet(pet_client, new_pet):
    pet_id, _ = new_pet
    delete_response = pet_client.delete_pet_by_id(pet_id)
    assert delete_response.status_code == 200, f"Ожидался статус 200, а получили: {delete_response.status_code}"
    delete_info = ApiResponseModel(**delete_response.json())
    assert delete_info.message == str(pet_id)
    get_response = pet_client.get_pet_by_id(pet_id)
    assert get_response.status_code == 404, f"Ожидался статус 404, а получили: {get_response.status_code}"

@allure.feature("Управление питомцами (PET)")
@allure.story("Негативные сценарии")
@allure.story("Получение несуществующего питомца  по ID (404)")
def test_get_non_existing_pet(pet_client):
    non_existing_pet_id = 999999999999999
    response = pet_client.get_pet_by_id(non_existing_pet_id)
    assert response.status_code == 404, f"Ожидался статус 404, а получили: {response.status_code}"
    error_body = ApiResponseModel(**response.json())
    assert error_body.type == "error"
    assert error_body.message == "Pet not found"

@allure.feature("Управление питомцами (PET)")
@allure.story("Негативные сценарии")
@allure.title("Удаление несуществующего питомца (404)")
def test_delete_non_existing_pet(pet_client):
    non_existing_pet_id = 999999999999999
    response = pet_client.delete_pet_by_id(non_existing_pet_id)
    assert response.status_code == 404, f"Ожидался статус 404, а получили: {response.status_code}"