import allure
from playwright.sync_api import Page

class HeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.burger_menu = page.locator('[class="bm-burger-button"] button')
        self.all_items_bm = page.locator('[data-test="inventory-sidebar-link"]')
        self.about_bm = page.locator('[data-test="about-sidebar-link"]')
        self.logout_bm = page.locator('[data-test="logout-sidebar-link"]')
        self.reset_app_state_bm = page.locator('[data-test="reset-sidebar-link"]')

    @allure.step("Переход в корзину через Header")
    def click_cart(self):
        self.cart_link.click()
    @allure.step("Нажатие на кнопку бургер меню")
    def click_burger_menu(self):
        self.burger_menu.click()
    @allure.step("Нажатие на кнопку Logout")
    def click_logout(self):
        self.logout_bm.click()
    @allure.step("Нажатие на кнопку All items")
    def click_all_items(self):
        self.all_items_bm.click()
    @allure.step("Нажатие на кнопку About")
    def click_about(self):
        self.about_bm.click()
    @allure.step("Нажатие на кнопку Reset App State")
    def click_reset_app_state(self):
        self.reset_app_state_bm.click()