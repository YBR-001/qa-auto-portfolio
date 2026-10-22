import allure, pytest
from playwright.sync_api import expect
from config import config
from faker import Faker

faker = Faker()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Smoke — основные пользовательские пути")
@allure.title("Покупка одного товара с полной сверкой данных и выходом из системы")
@pytest.mark.smoke
def test_buy_single_item_e2e(login_page, go_to_inventory_page, cart_page, checkout_one_page, checkout_two_page, checkout_complete_page):
    cnt_item_in_page = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, cnt_item_in_page)
    item_name = go_to_inventory_page.get_item_name_by_number(item_number)
    item_price = go_to_inventory_page.get_item_price_by_name(item_name)
    item_description = go_to_inventory_page.get_item_description_by_name(item_name)
    go_to_inventory_page.add_item_number(item_number)
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    item_name_in_cart = cart_page.get_item_name()
    item_price_in_cart = cart_page.get_item_price()
    item_description_in_cart = cart_page.get_item_description()
    assert item_name == item_name_in_cart, f"Ожидалось название {item_name}, а получили {item_name_in_cart}"
    assert item_price == item_price_in_cart, f"Ожидалась цена {item_price}, а получили {item_price_in_cart}"
    assert item_description == item_description_in_cart, f"Ожидалось описание {item_description}, а получили {item_description_in_cart}"
    expect(cart_page.inventory_item_name).to_have_count(1)
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    item_name_in_order = checkout_two_page.get_item_name()
    item_price_in_order = checkout_two_page.get_item_price()
    item_description_in_order = checkout_two_page.get_item_description()
    assert item_name_in_cart == item_name_in_order, f"Ожидалось название {item_name_in_cart}, а получили {item_name_in_order}"
    assert item_price_in_cart == item_price_in_order, f"Ожидалась цена {item_price_in_cart}, а получили {item_price_in_order}"
    assert item_description_in_cart == item_description_in_order, f"Ожидалось описание {item_description_in_cart}, а получили {item_description_in_order}"
    item_total = checkout_two_page.get_displayed_subtotal()
    assert item_price_in_order == item_total, f"Ожидалось значение {item_price_in_order}, а получили {item_total}"
    calc_item_tax = checkout_two_page.calculate_tax()
    item_tax_value = checkout_two_page.get_displayed_tax()
    assert calc_item_tax == item_tax_value, f"Ожидалось значение {item_tax_value}, а получили {calc_item_tax}"
    calc_total_with_tax = checkout_two_page.calculate_total_with_tax()
    total_with_tax = checkout_two_page.get_displayed_total_with_tax()
    assert calc_total_with_tax == total_with_tax, f"Ожидалось значение {calc_total_with_tax}, а получили {total_with_tax}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.complete_header).to_be_visible()
    expect(checkout_complete_page.complete_header).to_have_text("Thank you for your order!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()
    checkout_complete_page.click_back_home_button()
    expect(go_to_inventory_page.title).to_have_text("Products")
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()
    go_to_inventory_page.header.click_burger_menu()
    go_to_inventory_page.header.click_logout()
    go_to_inventory_page.page.wait_for_url(config.base_url)
    expect(login_page.login_button).to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Smoke — основные пользовательские пути")
@allure.title("Покупка нескольких товаров с проверкой расчета итоговой стоимости и налога")
@pytest.mark.smoke
def test_buy_multiple_items_e2e(go_to_cart_with_items, checkout_one_page, checkout_two_page, checkout_complete_page):
    cart_page, item_number = go_to_cart_with_items
    lst_item_name_in_cart = cart_page.get_all_item_name()
    summ_item_prices = cart_page.calculate_total_price_in_cart()
    assert len(lst_item_name_in_cart) == item_number, f"Ожидалось количество значений {item_number}, а получили {len(lst_item_name_in_cart)}"
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    item_count_in_order = checkout_two_page.get_item_count_in_order()
    assert item_count_in_order == item_number, f"Ожидалось значение {item_number}, а получили {item_count_in_order}"
    convert_item_total = checkout_two_page.get_displayed_subtotal()
    assert summ_item_prices == convert_item_total, f"Ожидалась сумма {convert_item_total}, а получили {summ_item_prices}"
    calc_item_tax = checkout_two_page.calculate_tax()
    convert_item_tax = checkout_two_page.get_displayed_tax()
    assert calc_item_tax == convert_item_tax, f"Ожидалось значение {convert_item_tax}, а получили {calc_item_tax}"
    calc_item_total_with_tax = checkout_two_page.calculate_total_with_tax()
    convert_item_total_with_tax = checkout_two_page.get_displayed_total_with_tax()
    assert calc_item_total_with_tax == convert_item_total_with_tax, f"Ожидалась сумма {convert_item_total_with_tax}, а получили {calc_item_total_with_tax}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()