import allure, pytest
from playwright.sync_api import expect
from config import config


@allure.feature("Оформление заказа")
@allure.title("Успешное оформление заказа")
@pytest.mark.e2e
def test_buy_product_e2e(base_page, cart_page, checkout_one_page, checkout_two_page, checkout_complete_page, login_page, inventory_page):
    login_page.open_url(config.base_url)
    login_page.login(config.standard_user, config.password)
    inventory_page.add_item_name("sauce-labs-backpack")
    expect(inventory_page.header.cart_badge).to_have_text("1")
    inventory_page.header.click_cart()
    item_in_cart = cart_page.get_all_item_name()
    assert "Sauce Labs Backpack" in item_in_cart, "Товара в корзине нет"
    cart_page.checkout_button.click()
    expect(checkout_one_page.page).to_have_url(config.checkout_one_page_url)
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    expect(checkout_two_page.page).to_have_url(config.checkout_two_page_url)
    expect(base_page.title).to_have_text("Checkout: Overview")
    expect(checkout_two_page.finish_button).to_be_visible()
    checkout_two_page.finish_button.click()
    expect(checkout_complete_page.complete_header).to_have_text("Thank you for your order!")
    expect(checkout_complete_page.complete_text).to_have_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!")
    expect(checkout_complete_page.back_home_button).to_be_visible()
    expect(base_page.title).to_have_text("Checkout: Complete!")