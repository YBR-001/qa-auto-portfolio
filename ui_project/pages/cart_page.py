import allure
from ui_project.pages.base_page import BasePage
from ui_project.pages.components.header import HeaderComponent
from ui_project.pages.components.item_card import ItemCard
from playwright.sync_api import Page

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.item_card = ItemCard(page)
        self.inventory_item_name = page.locator('[data-test="inventory-item-name"]')
        self.inventory_item_price = page.locator('[data-test="inventory-item-price"]')
        self.inventory_item_description = page.locator('[data-test="inventory-item-desc"]')
        self.item_quantity = page.locator('[data-test="item-quantity"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.remove_button = page.get_by_role("button", name="remove")

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
    @allure.step("Переход в карточку товара по его названию: {item_name}")
    def click_item_by_name(self, item_name: str):
        self.inventory_item_name.filter(has_text=item_name).click()
    @allure.step("Удаление первого товара по счёту из корзины")
    def click_first_remove_button(self):
        self.remove_button.first.click()
    @allure.step("Получение название товара по номеру: {item_number}")
    def get_item_name_by_number(self, item_number: int):
        return self.inventory_item_name.nth(item_number-1).inner_text()
    @allure.step("Удаление товара из корзины по номеру: {item_number}")
    def delete_item_by_number(self, item_number: int):
        self.remove_button.nth(item_number-1).click()
    @allure.step("Получение названия единственного товара в корзине")
    def get_item_name(self):
        return self.inventory_item_name.inner_text()
    @allure.step("Получение цены единственного товара в корзине")
    def get_item_price(self):
        dirty_price = self.inventory_item_price.inner_text()
        clean_price = dirty_price.replace("$", "")
        return float(clean_price)
    @allure.step("Получение описания единственного товара в корзине")
    def get_item_description(self):
        return self.inventory_item_description.inner_text()
    @allure.step("Получение списка всех цен товаров в корзине")
    def get_all_item_prices(self):
        price_list = self.inventory_item_price.all_inner_texts()
        return [float(price.replace("$", "")) for price in price_list]
    @allure.step("Получение суммы всех товаров в корзине")
    def calculate_total_price_in_cart(self):
        prices = self.get_all_item_prices()
        return round(sum(prices), 2)