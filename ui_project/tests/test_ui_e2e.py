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

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Сортировка каталога и покупка из карточки товара")
@pytest.mark.regression
def test_sort_and_buy_from_item_card(go_to_inventory_page, cart_page, checkout_one_page, checkout_two_page, checkout_complete_page):
    go_to_inventory_page.select_sort_option("lohi")
    actual_prices = go_to_inventory_page.get_all_item_prices()
    expected_prices = sorted(actual_prices)
    assert expected_prices == actual_prices, f"Ожидались значения {expected_prices}, а получили {actual_prices}"
    max_item_in_page = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_in_page)
    expected_item_name = go_to_inventory_page.get_item_name_by_number(item_number)
    expected_item_price = go_to_inventory_page.get_item_price_by_name(expected_item_name)
    expected_description = go_to_inventory_page.get_item_description_by_name(expected_item_name)
    go_to_inventory_page.click_item_name(item_number)
    item_name_in_card = go_to_inventory_page.item_card.get_item_name_in_card()
    item_price_in_card = go_to_inventory_page.item_card.get_item_price_in_card()
    item_description_in_card = go_to_inventory_page.item_card.get_item_description_in_card()
    assert expected_item_name == item_name_in_card, f"Ожидалось название товара {expected_item_name}, а получили {item_name_in_card}"
    assert expected_item_price == item_price_in_card, f"Ожидалась цена товара {expected_item_price}, а получили {item_price_in_card}"
    assert expected_description == item_description_in_card, f"Ожидалось описание товара {expected_description}, а получили  {item_description_in_card}"
    go_to_inventory_page.item_card.click_add_to_cart_button()
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.item_card.click_back_to_products_page()
    expect(go_to_inventory_page.title).to_have_text("Products")
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    item_total = checkout_two_page.get_displayed_subtotal()
    assert item_total == item_price_in_card, f"Ожидалась цена {item_price_in_card}, а получили {item_total}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Частичное удаление товара из корзины и возврат к покупкам")
@pytest.mark.regression
def test_edit_cart_and_continue_shopping(go_to_cart_with_items, inventory_page, checkout_one_page, checkout_two_page, checkout_complete_page):
    cart_page, item_number = go_to_cart_with_items
    deleted_item_name = cart_page.get_item_name_by_number(1)
    cart_page.delete_item_by_number(1)
    expect(cart_page.header.cart_badge).to_have_text(str(item_number-1))
    lst_name_in_cart = cart_page.get_all_item_name()
    assert deleted_item_name not in lst_name_in_cart, f"Ожидалось, что названия товара {deleted_item_name} больше не будет в корзине. Актуальный список товаров: {lst_name_in_cart}"
    cart_page.click_continue_shopping_button()
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.header.cart_badge).to_have_text(str(item_number-1))
    inventory_page.add_item_number(1)
    expect(inventory_page.header.cart_badge).to_have_text(str(item_number))
    inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    expected_summ = cart_page.calculate_total_price_in_cart()
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    actual_total_item = checkout_two_page.get_displayed_subtotal()
    assert expected_summ == actual_total_item, f"Ожидалась сумма товаров {expected_summ}, а получили {actual_total_item}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Отмена заказа на финальном шаге и повторное оформление")
@pytest.mark.regression
def test_cancel_overview_and_complete_order_e2e(go_to_overview_page_with_items, inventory_page, cart_page, checkout_one_page, checkout_complete_page):
    checkout_two_page, item_number = go_to_overview_page_with_items
    item_names_in_page = checkout_two_page.get_lst_item_names()
    total_item_value = checkout_two_page.get_displayed_subtotal()
    checkout_two_page.click_cancel_button()
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.header.cart_badge).to_have_text(str(item_number))
    inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    item_name_in_cart = cart_page.get_all_item_name()
    assert len(item_name_in_cart) == item_number, f"Ожидалось значение {item_number}, а получили {len(item_name_in_cart)}"
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    actual_item_names_in_page = checkout_two_page.get_lst_item_names()
    actual_total_item_value = checkout_two_page.get_displayed_subtotal()
    assert actual_item_names_in_page == item_names_in_page, f"Ожидался список {item_names_in_page}, а получили {actual_item_names_in_page}"
    assert actual_total_item_value == total_item_value, f"Ожидалось значение {total_item_value}, а получили {actual_total_item_value}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Восстановление после ошибки валидации на чекауте")
@pytest.mark.regression
def test_checkout_validation_error_recovery_e2e(go_to_checkout_page, checkout_two_page, checkout_complete_page):
    go_to_checkout_page.fill_shipping_info(config.first_name, config.last_name, "")
    go_to_checkout_page.click_continue_button()
    expect(go_to_checkout_page.checkout_error_msg).to_have_text("Error: Postal Code is required")
    go_to_checkout_page.click_error_button()
    expect(go_to_checkout_page.checkout_error_msg).not_to_be_visible()
    go_to_checkout_page.postal_code.fill(config.postal_code)
    go_to_checkout_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Полная очистка корзины и покупка нового товара")
@pytest.mark.regression
def test_empty_cart_and_repopulate_e2e(go_to_cart_page, inventory_page, checkout_one_page, checkout_two_page, checkout_complete_page):
    go_to_cart_page.delete_item_by_number(1)
    cnt_item_in_page = go_to_cart_page.get_items_count()
    assert cnt_item_in_page == 0, f"Ожидалось значение 0, а получили {cnt_item_in_page}"
    expect(go_to_cart_page.header.cart_badge).not_to_be_visible()
    go_to_cart_page.click_continue_shopping_button()
    expect(inventory_page.title).to_have_text("Products")
    max_items_cnt = inventory_page.get_items_count()
    item_number = faker.random_int(2, max_items_cnt)
    item_name = inventory_page.get_item_name_by_number(item_number)
    item_price = inventory_page.get_item_price_by_name(item_name)
    inventory_page.add_item_number(item_number)
    expect(inventory_page.header.cart_badge).to_have_text("1")
    inventory_page.header.click_cart()
    expect(go_to_cart_page.title).to_have_text("Your Cart")
    go_to_cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    item_names_in_order = checkout_two_page.get_lst_item_names()
    item_total_in_order = checkout_two_page.get_displayed_subtotal()
    assert item_name == item_names_in_order[0], f"Ожидался товар {item_name}, а получили {item_names_in_order[0]}"
    assert len(item_names_in_order) == 1, f"Ожидалось значение 1, а получили {len(item_names_in_order)}"
    assert item_price == item_total_in_order, f"Ожидалась сумма {item_price}, а получили {item_total_in_order}"
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сквозные сценарии (E2E)")
@allure.story("Regress")
@allure.title("Сброс состояния приложения через бургер-меню и новый заказ")
@pytest.mark.regression
def test_reset_app_state_from_burger_menu_e2e(go_to_inventory_page, cart_page, checkout_one_page, checkout_two_page, checkout_complete_page):
    max_item_cnt = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(2, max_item_cnt)
    for i in range(1, item_number + 1):
        go_to_inventory_page.add_item_number(i)
    expect(go_to_inventory_page.header.cart_badge).to_have_text(str(item_number))
    go_to_inventory_page.header.click_burger_menu()
    go_to_inventory_page.header.click_reset_app_state()
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    item_cnt_in_cart = cart_page.get_items_count()
    assert item_cnt_in_cart == 0, f"Ожидалось значение 0, а получили {item_cnt_in_cart}"
    cart_page.click_continue_shopping_button()
    expect(go_to_inventory_page.title).to_have_text("Products")
    item_number_single = faker.random_int(1, max_item_cnt)
    go_to_inventory_page.add_item_number(item_number_single)
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    checkout_two_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.header.cart_badge).not_to_be_visible()