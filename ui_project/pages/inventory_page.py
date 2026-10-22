import allure
from playwright.sync_api import Page
from ui_project.pages.base_page import BasePage
from ui_project.pages.components.header import HeaderComponent
from ui_project.pages.components.item_card import ItemCard

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.item_card = ItemCard(page)
        self.button_action_item = page.locator("[data-test='inventory-item-description'] button")
        self.button_action_item_in_card = page.locator(".inventory_details_desc_container button")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.item_desc = page.locator('[data-test="inventory-item-desc"]')
        self.inventory_items = page.locator("[data-test='inventory-item']")

    @allure.step("Добавление товара '{item_name}' в корзину")
    def add_item_name(self, item_name: str):
        button = self.page.locator(f'[data-test="add-to-cart-{item_name}"]')
        button.click()
    @allure.step("Добавление товара в корзину по номеру (от 1 до 6): {item_number}")
    def add_item_number(self, item_number: int):
        button = self.page.locator(f":nth-match([data-test='inventory-item-description'] button, {item_number})")
        button.click()
    @allure.step("Удаление товара {item_number} из корзины")
    def delete_item_number(self, item_number: int):
        button = self.page.locator(f":nth-match([data-test='inventory-item-description'] button, {item_number})")
        button.click()
    @allure.step("Удаление товара '{item_name}' из корзины")
    def delete_item_name(self, item_name: str):
        button = self.page.locator(f'[data-test="remove-{item_name}"]')
        button.click()
    @allure.step("Получение общего количества товаров на странице")
    def get_items_count(self):
        self.button_action_item.first.wait_for()
        return self.button_action_item.count()
    @allure.step("Нажатие по названию товара по номеру товара на странице: {item_number}")
    def click_item_name(self, item_number: int):
        inventory_item_name = self.page.locator(f":nth-match([data-test='inventory-item-name'], {item_number})")
        inventory_item_name.click()
    @allure.step("Выбор сортировки: {sort_value}")
    def select_sort_option(self, sort_value: str):
        self.sort_dropdown.select_option(value=sort_value)
    @allure.step("Получение списка названий всех товаров")
    def get_all_item_names(self):
        return self.item_names.all_inner_texts()
    @allure.step("Получение списка цен всех товаров")
    def get_all_item_prices(self):
        price_text = self.item_prices.all_inner_texts()
        return [float(price.replace("$", "")) for price in price_text]
    @allure.step("Расчёт суммы всех товаров")
    def calculate_item_prices(self):
        prices = self.get_all_item_prices()
        return round(sum(prices), 2)
    @allure.step("Получение названия товара по номеру: {item_number}")
    def get_item_name_by_number(self, item_number: int):
        return self.item_names.nth(item_number - 1).inner_text()
    @allure.step("Получение цены товара по его названию: {item_name}")
    def get_item_price_by_name(self, item_name: str):
        dirty_price = self.inventory_items.filter(has_text=item_name).locator(self.item_prices).inner_text()
        clean_price = dirty_price.replace("$", "")
        return float(clean_price)
    @allure.step("Получение описания товара по его названию: {item_name}")
    def get_item_description_by_name(self, item_name: str):
        return self.inventory_items.filter(has_text=item_name).locator(self.item_desc).inner_text()