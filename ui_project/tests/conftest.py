import pytest, allure
from playwright.sync_api import expect
from playwright.sync_api import Page
from ui_project.pages.login_page import LoginPage
from ui_project.pages.inventory_page import InventoryPage
from ui_project.pages.base_page import BasePage
from ui_project.pages.cart_page import CartPage
from ui_project.pages.checkout_page import CheckoutOnePage
from ui_project.pages.checkout_page import CheckoutTwoPage
from ui_project.pages.checkout_page import CheckoutCompletePage
from config import config
from faker import Faker

faker = Faker()

@pytest.fixture
def base_page(page: Page):
    return BasePage(page)

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture
def inventory_page(page: Page):
    return InventoryPage(page)

@pytest.fixture
def cart_page(page: Page):
    return CartPage(page)

@pytest.fixture
def checkout_one_page(page: Page):
    return CheckoutOnePage(page)

@pytest.fixture
def checkout_two_page(page: Page):
    return CheckoutTwoPage(page)

@pytest.fixture
def checkout_complete_page(page: Page):
    return CheckoutCompletePage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.screenshot(full_page=True), name="Скриншот ошибки", attachment_type=allure.attachment_type.PNG)

@pytest.fixture
def go_to_inventory_page(login_page, inventory_page):
    login_page.open_url(config.base_url)
    login_page.login(config.standard_user, config.password)
    expect(inventory_page.title).to_have_text("Products")
    yield inventory_page

@pytest.fixture
def go_to_cart_page(cart_page, go_to_inventory_page):
    max_item_cnt = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_cnt)
    go_to_inventory_page.add_item_number(item_number)
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.header.cart_badge).to_have_text("1")
    yield cart_page

@pytest.fixture
def go_to_cart_with_items(cart_page, go_to_inventory_page):
    max_item_cnt = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(2, max_item_cnt)
    for i in range(1, item_number + 1):
        go_to_inventory_page.add_item_number(i)
    expect(go_to_inventory_page.header.cart_badge).to_have_text(str(item_number))
    go_to_inventory_page.header.click_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.header.cart_badge).to_have_text(str(item_number))
    yield cart_page, item_number

@pytest.fixture
def go_to_checkout_page(go_to_cart_page, checkout_one_page):
    go_to_cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    expect(checkout_one_page.header.cart_badge).to_have_text("1")
    yield checkout_one_page

@pytest.fixture
def go_to_overview_page(go_to_checkout_page, checkout_two_page):
    go_to_checkout_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    go_to_checkout_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    expect(checkout_two_page.header.cart_badge).to_have_text("1")
    yield checkout_two_page

@pytest.fixture
def go_to_overview_page_with_items(go_to_cart_with_items, checkout_one_page, checkout_two_page):
    cart_page, item_number = go_to_cart_with_items
    cart_page.click_checkout_button()
    expect(checkout_one_page.title).to_have_text("Checkout: Your Information")
    expect(checkout_one_page.header.cart_badge).to_have_text(str(item_number))
    checkout_one_page.fill_shipping_info(config.first_name, config.last_name, config.postal_code)
    checkout_one_page.click_continue_button()
    expect(checkout_two_page.title).to_have_text("Checkout: Overview")
    expect(checkout_two_page.header.cart_badge).to_have_text(str(item_number))
    yield checkout_two_page, item_number

@pytest.fixture
def go_to_complete_page(go_to_overview_page, checkout_complete_page):
    go_to_overview_page.click_finish_button()
    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    yield checkout_complete_page