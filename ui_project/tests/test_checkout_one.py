import allure
import pytest
from playwright.sync_api import expect
from config import config

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Поля ввода данных пользователя")
@allure.title("Проверка доступности и плейсхолдеров полей ввода")
def test_check_shipping_inputs(go_to_checkout_page):
    expect(go_to_checkout_page.first_name).to_be_visible()
    expect(go_to_checkout_page.first_name).to_be_editable()
    expect(go_to_checkout_page.first_name).to_have_attribute("placeholder", "First Name")
    expect(go_to_checkout_page.last_name).to_be_visible()
    expect(go_to_checkout_page.last_name).to_be_editable()
    expect(go_to_checkout_page.last_name).to_have_attribute("placeholder", "Last Name")
    expect(go_to_checkout_page.postal_code).to_be_visible()
    expect(go_to_checkout_page.postal_code).to_be_editable()
    expect(go_to_checkout_page.postal_code).to_have_attribute("placeholder", "Zip/Postal Code")

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Заполнение формы данных пользователя")
@allure.title("Проверка перехода к обзору заказа при заполнении валидными данными")
def test_checkout_success(go_to_checkout_page):
    go_to_checkout_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    go_to_checkout_page.click_continue_button()
    expect(go_to_checkout_page.title).to_have_text("Checkout: Overview")

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Заполнение формы данных пользователя")
@allure.title("Проверка отображения ошибки при отправке формы с пустым обязательным полем")
@pytest.mark.parametrize("first_name, last_name, postal_code, expected_error_msg", [
    ("", config.last_name, config.postal_code, "Error: First Name is required"),
    (config.first_name, "", config.postal_code, "Error: Last Name is required"),
    (config.first_name, config.last_name, "", "Error: Postal Code is required"),
    ("", "", "", "Error: First Name is required")
])
def test_checkout_failure(go_to_checkout_page, first_name: str, last_name: str, postal_code: str, expected_error_msg: str):
    go_to_checkout_page.fill_shipping_info(first_name, last_name, postal_code)
    go_to_checkout_page.click_continue_button()
    expect(go_to_checkout_page.checkout_error_msg).to_have_text(expected_error_msg)
    expect(go_to_checkout_page.checkout_error_msg_container).to_have_css("background-color", "rgb(226, 35, 26)")

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Заполнение формы данных пользователя")
@allure.title("Проверка закрытия сообщения об ошибке по клику на крестик")
def test_check_hidden_error_msg(go_to_checkout_page):
    go_to_checkout_page.fill_shipping_info(config.first_name, config.last_name, "")
    go_to_checkout_page.click_continue_button()
    expect(go_to_checkout_page.checkout_error_msg).to_be_visible()
    expect(go_to_checkout_page.checkout_error_msg_container).to_have_css("background-color", "rgb(226, 35, 26)")
    go_to_checkout_page.click_error_button()
    expect(go_to_checkout_page.checkout_error_msg).not_to_be_visible()

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Управление доступными кнопками на странице")
@allure.title("Проверка видимости и доступности кнопок действий")
def test_check_available_buttons_in_checkout_one(go_to_checkout_page):
    expect(go_to_checkout_page.continue_button).to_be_visible()
    expect(go_to_checkout_page.continue_button).to_be_enabled()
    expect(go_to_checkout_page.cancel_button).to_be_visible()
    expect(go_to_checkout_page.cancel_button).to_be_enabled()
    expect(go_to_checkout_page.header.cart_link).to_be_visible()
    expect(go_to_checkout_page.header.cart_link).to_be_enabled()

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Управление доступными кнопками на странице")
@allure.title("Проверка обратного перехода в корзину")
def test_return_to_cart_from_checkout(go_to_checkout_page, cart_page):
    go_to_checkout_page.click_cancel_button()
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.remove_button).to_be_visible()
    expect(cart_page.continue_shopping_button).to_be_visible()
    expect(cart_page.inventory_item_name).to_be_visible()
    expect(cart_page.inventory_item_description).to_be_visible()
    expect(cart_page.inventory_item_price).to_be_visible()
    expect(cart_page.item_quantity).to_be_visible()
    expect(cart_page.header.cart_badge).to_have_text("1")

@allure.feature("Страница данных пользователя (Checkout One Page)")
@allure.story("Визуальное оформление страницы")
@allure.title("Проверка корректности цвета кнопок действий")
def test_check_color_action_button(go_to_checkout_page):
    expect(go_to_checkout_page.cancel_button).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(go_to_checkout_page.cancel_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")
    expect(go_to_checkout_page.continue_button).to_have_css("background-color", "rgb(61, 220, 145)")
    expect(go_to_checkout_page.continue_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")