import pytest
from faker import Faker
from api_project.clients.pet_client import PetClient
from api_project.clients.store_client import StoreClient
from api_project.clients.user_client import UserClient
from config import config

faker = Faker()

@pytest.fixture
def pet_client():
    return PetClient(base_url=config.api_base_url)

@pytest.fixture
def store_client():
    return StoreClient(base_url=config.api_base_url)

@pytest.fixture
def user_client():
    return UserClient(base_url=config.api_base_url)

@pytest.fixture
def new_pet(pet_client):
    pet_id = faker.random_int(min=1000, max=999999)
    payload = {
        "id": pet_id,
        "name": faker.first_name(),
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": [faker.image_url()],
        "tags": [{"id": 1, "name": "good_boy"}],
        "status": "available"
    }
    pet_client.create_pet(payload)
    yield pet_id, payload
    pet_client.delete_pet_by_id(pet_id)

@pytest.fixture
def new_order(store_client, new_pet):
    pet_id, _ = new_pet
    order_id = faker.random_int(min=1, max=9999)
    payload = {
        "id": order_id,
        "petId": pet_id,
        "quantity": 0,
        "shipDate": "2026-10-08T08:16:09.217Z",
        "status": "placed",
        "complete": True
    }
    store_client.place_order(payload)
    yield order_id, payload
    store_client.delete_order_by_id(order_id)

@pytest.fixture
def new_user(user_client):
    username = faker.user_name()
    payload = {
        "id": faker.random_int(min=1, max=100000),
        "username": username,
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
        "phone": faker.phone_number(),
        "userStatus": 1
    }
    user_client.create_user(payload)
    yield username, payload
    user_client.delete_user_by_username(username)