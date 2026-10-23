import allure
from playwright.sync_api import Page

class ItemCard:
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_button = page.locator('[class="btn btn_primary btn_small btn_inventory"]')
        self.back_to_products_button = page.locator('[data-test="back-to-products"]')
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
    @allure.step("Нажатие на кнопку Add to cart")
    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()
    @allure.step("Нажатие на кнопку Back to products")
    def click_back_to_products_page(self):
        self.back_to_products_button.click()