import allure
from faker import Faker
from api_project.models.pet import ApiResponseModel
from api_project.models.user import UserModel

faker = Faker()

@allure.feature("Управление пользователем (USER)")
@allure.story("Позитивные сценарии")
@allure.title("Создание и получение пользователя по username")
def test_create_and_get_user(user_client, new_user):
    username, payload = new_user
    user_info = user_client.get_info_user_by_username(username)
    assert user_info.status_code == 200, f"Ожидался статус 200, а получили {user_info.status_code}"
    fetched_data = UserModel(**user_info.json())
    assert fetched_data.model_dump() == payload, f"Данные пользователя не совпадают! Ожидалось {payload}, а получили {fetched_data.model_dump()}"

@allure.feature("Управление пользователем (USER)")
@allure.story("Позитивные сценарии")
@allure.title("Обновление данных пользователя")
def test_update_user(user_client, new_user):
    username, payload = new_user
    updated_payload = payload.copy()
    updated_payload["firstName"], updated_payload["email"] = "UpdatedFirstName", faker.email()
    update_response = user_client.update_user(username, updated_payload)
    assert update_response.status_code == 200, f"Ожидался статус 200, а получили {update_response.status_code}"
    user_info = user_client.get_info_user_by_username(username)
    assert user_info.status_code == 200, f"Ожидался статус 200, а получили {user_info.status_code}"
    fetched_data = UserModel(**user_info.json())
    assert fetched_data.firstName == "UpdatedFirstName", f"Имя не обновилось: {fetched_data.firstName}"
    assert fetched_data.email == updated_payload["email"], f"Имейл не обновился: {fetched_data.email}"

@allure.feature("Управление пользователем (USER)")
@allure.story("Авторизация")
@allure.title("Авторизация и выход пользователя из системы")
def test_login_and_logout_user(user_client, new_user):
    username, payload = new_user
    login_response = user_client.login_user(username, payload)
    assert login_response.status_code == 200, f"Ожидался статус 200, а получили {login_response.status_code}"
    login_body = ApiResponseModel(**login_response.json())
    assert "logged in user session" in login_body.message
    logout_response = user_client.logout_user()
    assert logout_response.status_code == 200, f"Ожидался статус 200, а получили {logout_response.status_code}"

@allure.feature("Управление пользователем (USER)")
@allure.story("Массовые операции")
@allure.title("Создание списка пользователей")
def test_create_users_with_list(user_client):
    users_payload = [
        {
            "id": faker.random_int(min=1000, max=99999),
            "username": faker.user_name(),
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "email": faker.email(),
            "password": faker.password(),
            "phone": faker.phone_number(),
            "userStatus": 1
        }
        for _ in range(2)
    ]
    create_response = user_client.create_user_with_list(users_payload)
    assert create_response.status_code == 200, f"Ожидался статус 200, а получили {create_response.status_code}"
    for user in users_payload:
        get_response = user_client.get_info_user_by_username(user["username"])
        assert get_response.status_code == 200, f"Ожидался статус 200, а получили {get_response.status_code}"
        user_client.delete_user_by_username(user["username"])

@allure.feature("Управление пользователем (USER)")
@allure.story("Позитивные проверки")
@allure.title("Удаление пользователя и проверка его отсутствия")
def test_delete_user(user_client, new_user):
    username, payload = new_user
    delete_response = user_client.delete_user_by_username(username)
    assert delete_response.status_code == 200, f"Ожидался статус 200, а получили {delete_response.status_code}"
    get_response = user_client.get_info_user_by_username(username)
    assert get_response.status_code == 404, f"Ожидался статус 404, а получили {get_response.status_code}"

@allure.feature("Управление пользователем (USER)")
@allure.story("Негативные проверки")
@allure.title("Поиск несуществующего пользователя по username")
def test_get_non_existing_user(user_client):
    username = f"non_existing_{faker.uuid4()}"
    response = user_client.get_info_user_by_username(username)
    assert response.status_code == 404, f"Ожидался статус 404, а получили {response.status_code}"
    error_body = ApiResponseModel(**response.json())
    assert error_body.type == "error"
    assert error_body.message == "User not found"

@allure.feature("Управление пользователем (USER)")
@allure.story("Негативные проверки")
@allure.title("Удаление несуществующего пользователя по username")
def test_delete_non_existing_user(user_client):
    username = f"non_existing_{faker.uuid4()}"
    response = user_client.delete_user_by_username(username)
    assert response.status_code == 404, f"Ожидался статус 404, а получили {response.status_code}"