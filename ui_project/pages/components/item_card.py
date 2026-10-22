import allure
from playwright.sync_api import Page

class ItemCard:
    def __init__(self, page: Page):
        self.page = page
        self.inventory_item_name_in_card = page.locator('[class="inventory_details_name large_size"]')
        self.inventory_item_price_in_card = page.locator('[class="inventory_details_price"]')
        self.inventory_item_description_in_card = page.locator('[class="inventory_details_desc large_size"]')
    @allure.step("Получение названия товара в карточке")
    def get_item_name_in_card(self):
        return self.inventory_item_name_in_card.inner_text()
    @allure.step("Получение цены товара в карточке")
    def get_item_price_in_card(self):
        price_text = self.inventory_item_price_in_card.inner_text()
        return float(price_text.replace("$", ""))
    @allure.step("Получение описания товара в карточке")
    def get_item_description_in_card(self):
        return self.inventory_item_description_in_card.inner_text()