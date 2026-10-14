import allure
from ui_project.pages.base_page import BasePage
from ui_project.pages.components.header import HeaderComponent
from playwright.sync_api import Page

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.inventory_item_name = page.locator('[data-test="inventory-item-name"]')
        self.inventory_item_name_in_card = page.locator('[class="inventory_details_name large_size"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.inventory_item_price = page.locator('[data-test="inventory-item-price"]')
        self.inventory_item_description = page.locator('[data-test="inventory-item-desc"]')
        self.remove_button = page.get_by_role("button", name="remove")
        self.item_quantity = page.locator('[data-test="item-quantity"]')

    @allure.step("Получение списка названий товаров в корзине")
    def get_all_item_name(self):
        return self.inventory_item_name.all_inner_texts()
    @allure.step("Нажатие на кнопку Remove")
    def click_remove_button(self):
        self.remove_button.click()
    @allure.step("Нажатие на кнопку Continue-Shopping")
    def click_continue_shopping_button(self):
        self.continue_shopping_button.click()
    @allure.step("Нажатие на кнопку Checkout")
    def click_checkout_button(self):
        self.checkout_button.click()
    @allure.step("Переход в карточку товара путём нажатия на его название")
    def click_item_name(self):
        self.inventory_item_name.click()
    @allure.step("Удаление первого товара по счёту из корзины")
    def click_first_remove_button(self):
        self.remove_button.first.click()
    @allure.step("Получение название товара по номеру: {item_number}")
    def get_item_name_by_number(self, item_number: int):
        return self.inventory_item_name.nth(item_number-1).inner_text()
    @allure.step("Удаление товара из корзины по номеру: {item_number}")
    def delete_item_by_number(self, item_number: int):
        self.remove_button.nth(item_number-1).click()