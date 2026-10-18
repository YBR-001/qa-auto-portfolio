import allure
from playwright.sync_api import expect

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Кнопки действия на странице")
@allure.title("Проверка видимости и доступности кнопок действий")
def test_check_available_button_in_checkout_two(go_to_overview_page):
    expect(go_to_overview_page.cancel_button).to_be_visible()
    expect(go_to_overview_page.cancel_button).to_be_enabled()
    expect(go_to_overview_page.finish_button).to_be_visible()
    expect(go_to_overview_page.finish_button).to_be_enabled()
    expect(go_to_overview_page.header.cart_link).to_be_visible()
    expect(go_to_overview_page.header.cart_link).to_be_enabled()

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Визуальное оформление страницы")
@allure.title("Проверка цвета кнопок действия")
def test_check_color_action_button(go_to_overview_page):
    expect(go_to_overview_page.cancel_button).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(go_to_overview_page.cancel_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")
    expect(go_to_overview_page.finish_button).to_have_css("background-color", "rgb(61, 220, 145)")
    expect(go_to_overview_page.finish_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Кнопки действия на странице")
@allure.title("Проверка перехода обратно на страницу с выбором товара")
def test_return_to_inventory_from_overview(go_to_overview_page, inventory_page):
    go_to_overview_page.click_cancel_button()
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.button_action_item.first).to_be_visible()
    expect(inventory_page.sort_dropdown).to_be_visible()
    expect(inventory_page.button_action_item).to_have_count(inventory_page.get_items_count())
    expect(inventory_page.header.cart_badge).to_be_visible()
    expect(inventory_page.header.cart_badge).to_have_text("1")

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Информация о заказе и доставке")
@allure.title("Проверка видимости и валидности информации о товаре и доставке")
def test_check_order_info_visibility(go_to_overview_page):
    expect(go_to_overview_page.item_name).to_be_visible()
    expect(go_to_overview_page.item_price).to_be_visible()
    expect(go_to_overview_page.item_description).to_be_visible()
    expect(go_to_overview_page.item_quantity).to_be_visible()
    expect(go_to_overview_page.payment_info_value).to_be_visible()
    expect(go_to_overview_page.payment_info_value).to_have_text("SauceCard #31337")
    expect(go_to_overview_page.shipping_information).to_be_visible()
    expect(go_to_overview_page.shipping_information).to_have_text("Free Pony Express Delivery!")
    expect(go_to_overview_page.item_total).to_be_visible()

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Информация о товаре в форме доставке")
@allure.title("Проверка расчётов всех значений")
def test_check_order_price_calculation(go_to_overview_page):
    calc_total_price = go_to_overview_page.calculate_items_subtotal()
    total_price_value = go_to_overview_page.get_displayed_subtotal()
    assert calc_total_price == total_price_value, f"Ожидалось значение {total_price_value}, а получили {calc_total_price}"
    expect(go_to_overview_page.tax_value).to_be_visible()
    calc_tax_value = go_to_overview_page.calculate_tax()
    tax_value = go_to_overview_page.get_displayed_tax()
    assert calc_tax_value == tax_value, f"Ожидалось значение {tax_value}, а получили {calc_tax_value}"
    expect(go_to_overview_page.total_amount).to_be_visible()
    calc_total_amount = go_to_overview_page.calculate_total_with_tax()
    convert_item_amount = go_to_overview_page.get_displayed_total_with_tax()
    assert calc_total_amount == convert_item_amount, f"Ожидалось значение {convert_item_amount}, а получили {calc_total_amount}"

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Взаимодействие с товаром на странице")
@allure.title("Проверка корректности информации на данной странице и карточке товара")
def test_check_info_in_item_card(go_to_overview_page, cart_page):
    expect_item_name = go_to_overview_page.get_item_name()
    expect_item_price = go_to_overview_page.get_item_price()
    expect_item_description = go_to_overview_page.get_item_description()
    go_to_overview_page.click_item_name()
    expect(cart_page.inventory_item_name_in_card).to_be_visible()
    expect(cart_page.inventory_item_price_in_card).to_be_visible()
    expect(cart_page.inventory_item_description_in_card).to_be_visible()
    expect(cart_page.remove_button).to_be_visible()
    actual_item_name = cart_page.inventory_item_name_in_card.inner_text() #Позже вынести в отдельный класс
    actual_item_price = cart_page.inventory_item_price_in_card.inner_text()
    actual_item_description = cart_page.inventory_item_description_in_card.inner_text()
    assert expect_item_name == actual_item_name, f"Ожидалось название товара {expect_item_name}, а получили {actual_item_name}"
    assert expect_item_price == actual_item_price, f"Ожидалась цена товара {expect_item_price}, а получили {actual_item_price}"
    assert expect_item_description == actual_item_description, f"Ожидалось описание товара {expect_item_description}, а получили {actual_item_description}"

@allure.feature("Страница просмотра итогового заказа (Checkout Overview)")
@allure.story("Кнопки действия на странице")
@allure.title("Проверка перехода на complete page")
def test_check_go_to_complete_page(go_to_overview_page, checkout_complete_page):
    go_to_overview_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()