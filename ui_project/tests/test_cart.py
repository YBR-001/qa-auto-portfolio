import allure
from playwright.sync_api import expect
from faker import Faker

faker = Faker()

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление доступными кнопками в корзине")
@allure.title("Проверка видимости доступности кнопок действий в корзине")
def test_check_available_buttons(go_to_cart_page):
    expect(go_to_cart_page.checkout_button).to_be_visible()
    expect(go_to_cart_page.checkout_button).to_be_enabled()
    expect(go_to_cart_page.continue_shopping_button).to_be_visible()
    expect(go_to_cart_page.continue_shopping_button).to_be_enabled()
    expect(go_to_cart_page.remove_button).to_be_visible()
    expect(go_to_cart_page.remove_button).to_be_enabled()
    expect(go_to_cart_page.header.cart_link).to_be_visible()
    expect(go_to_cart_page.header.cart_link).to_be_enabled()

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление товарами в корзине")
@allure.title("Проверка удаления товара из корзины")
def test_delete_item_in_cart(go_to_cart_page):
    expect(go_to_cart_page.remove_button).to_be_enabled()
    go_to_cart_page.click_remove_button()
    expect(go_to_cart_page.header.cart_badge).not_to_be_visible()
    expect(go_to_cart_page.remove_button).not_to_be_visible()
    expect(go_to_cart_page.continue_shopping_button).to_be_visible()
    expect(go_to_cart_page.checkout_button).to_be_visible()

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление доступными кнопками в корзине")
@allure.title("Проверка перехода обратно к выбору товаров")
def test_return_to_inventory_page(go_to_cart_page, inventory_page):
    go_to_cart_page.click_continue_shopping_button()
    expect(go_to_cart_page.title).to_have_text("Products")
    expect(inventory_page.button_action_item.first).to_be_visible()
    expect(inventory_page.sort_dropdown).to_be_visible()
    expect(inventory_page.button_action_item).to_have_count(inventory_page.get_items_count())
    expect(inventory_page.header.cart_badge).to_be_visible()
    expect(inventory_page.header.cart_badge).to_have_text("1")

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление доступными кнопками в корзине")
@allure.title("Проверка перехода к оформлению заказа (Checkout Page) из корзины")
def test_go_to_checkout_page_through_button(go_to_cart_page):
    go_to_cart_page.click_checkout_button()
    expect(go_to_cart_page.title).to_have_text("Checkout: Your Information")

@allure.feature("Корзина (Cart Page)")
@allure.story("Информация о товаре в корзине")
@allure.title("Проверка видимости информации о товаре")
def test_check_info_about_item(go_to_cart_page):
    expect(go_to_cart_page.inventory_item_name).to_be_visible()
    expect(go_to_cart_page.item_quantity).to_be_visible()
    expect(go_to_cart_page.inventory_item_description).to_be_visible()
    expect(go_to_cart_page.inventory_item_price).to_be_visible()

@allure.feature("Корзина (Cart Page)")
@allure.story("Визуальное оформление страницы")
@allure.title("Проверка корректности цвета кнопок действий")
def test_check_color_button_action(go_to_cart_page):
    expect(go_to_cart_page.checkout_button).to_have_css("background-color", "rgb(61, 220, 145)")
    expect(go_to_cart_page.checkout_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")
    expect(go_to_cart_page.continue_shopping_button).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(go_to_cart_page.continue_shopping_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")
    expect(go_to_cart_page.remove_button).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(go_to_cart_page.remove_button).to_have_css("border-bottom-color", "rgb(226, 35, 26)")

@allure.feature("Корзина (Cart Page)")
@allure.story("Информация карточки товара в корзине")
@allure.title("Проверка корректности информации в карточке товара")
def test_check_info_in_item_card(go_to_cart_page):
    name_item_cart = go_to_cart_page.get_item_name_by_number(1)
    go_to_cart_page.click_item_name()
    name_item_in_card = go_to_cart_page.inventory_item_name_in_card.inner_text()
    assert name_item_in_card == name_item_cart, f"Названия товаров должны быть равными. Ожидалось {name_item_cart}, а получили {name_item_in_card}"

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление товарами в корзине")
@allure.title("Проверка отображения информации и кнопок действий у товаров")
def test_check_info_about_items(go_to_cart_with_items):
    cart_page, item_number = go_to_cart_with_items
    expect(cart_page.inventory_item_name).to_have_count(item_number)
    expect(cart_page.item_quantity).to_have_count(item_number)
    expect(cart_page.inventory_item_description).to_have_count(item_number)
    expect(cart_page.inventory_item_price).to_have_count(item_number)
    expect(cart_page.remove_button).to_have_count(item_number)

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление товарами в корзине")
@allure.title("Проверка удаления всех товаров из корзины")
def test_check_remove_all_items(go_to_cart_with_items):
    cart_page, item_number = go_to_cart_with_items
    for _ in range(item_number):
        cart_page.click_first_remove_button()
    expect(cart_page.remove_button).not_to_be_visible()
    expect(cart_page.inventory_item_name).not_to_be_visible()
    expect(cart_page.item_quantity).not_to_be_visible()
    expect(cart_page.inventory_item_description).not_to_be_visible()
    expect(cart_page.inventory_item_price).not_to_be_visible()
    expect(cart_page.header.cart_badge).not_to_be_visible()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.continue_shopping_button).to_be_visible()

@allure.feature("Корзина (Cart Page)")
@allure.story("Управление товарами в корзине")
@allure.title("Проверка частичного удаления товаров из корзины")
def test_delete_partial_item_in_cart(go_to_cart_with_items):
    cart_page, item_number = go_to_cart_with_items
    delete_item_number = faker.random_int(1, item_number)
    delete_item_name = cart_page.get_item_name_by_number(delete_item_number)
    cart_page.delete_item_by_number(delete_item_number)
    expect(cart_page.header.cart_badge).to_have_text(str(item_number-1))
    expect(cart_page.inventory_item_name).to_have_count(item_number-1)
    expect(cart_page.remove_button).to_have_count(item_number-1)
    remaining_items = cart_page.get_all_item_name()
    assert delete_item_name not in remaining_items, f"Названия товара {delete_item_number} не должно было быть в списке {remaining_items}"