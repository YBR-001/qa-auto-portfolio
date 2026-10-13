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