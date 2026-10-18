import allure
from playwright.sync_api import expect

@allure.feature("Страница завершения покупки (Checkout Complete)")
@allure.story("Информация на странице")
@allure.title("Проверка корректности информации на странице")
def test_check_info_in_page(go_to_complete_page):
    expect(go_to_complete_page.complete_header).to_be_visible()
    expect(go_to_complete_page.complete_header).to_have_text("Thank you for your order!")
    expect(go_to_complete_page.complete_text).to_be_visible()
    expect(go_to_complete_page.complete_text).to_have_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!")
    expect(go_to_complete_page.back_home_button).to_be_visible()
    expect(go_to_complete_page.back_home_button).to_be_enabled()
    expect(go_to_complete_page.back_home_button).to_have_css("background-color", "rgb(61, 220, 145)")
    expect(go_to_complete_page.back_home_button).to_have_css("border-bottom-color", "rgb(19, 35, 34)")
    expect(go_to_complete_page.image_success).to_be_visible()
    expect(go_to_complete_page.header.cart_badge).not_to_be_visible()

@allure.feature("Страница завершения покупки (Checkout Complete)")
@allure.story("Кнопки действия")
@allure.title("Проверка перехода обратно на главную страницу магазина")
def test_return_to_inventory_page(go_to_complete_page, inventory_page):
    go_to_complete_page.click_back_home_button()
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.button_action_item.first).to_be_visible()
    expect(inventory_page.sort_dropdown).to_be_visible()
    expect(inventory_page.button_action_item).to_have_count(inventory_page.get_items_count())
    expect(inventory_page.header.cart_badge).not_to_be_visible()