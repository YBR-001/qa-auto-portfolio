import allure
from playwright.sync_api import Page
from ui_project.pages.base_page import BasePage
from ui_project.pages.components.header import HeaderComponent
from ui_project.pages.components.item_card import ItemCard

class CheckoutOnePage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.item_card = ItemCard(page)
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.checkout_error_msg = page.locator('[data-test="error"]')
        self.checkout_error_msg_container = page.locator('[class="error-message-container error"]')
        self.error_button = page.locator('[data-test="error-button"]')
    @allure.step("Заполнение данных доставки: имя {first_name}, фамилия {last_name} и почтовый индекс {postal_code}")
    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
    @allure.step("Частичное заполнение данных доставки: почтовый индекс {postal_code}")
    def fill_postal_code(self, postal_code):
        self.postal_code.fill(postal_code)
    @allure.step("Нажатие на кнопку Cancel")
    def click_cancel_button(self):
        self.cancel_button.click()
    @allure.step("Нажатие на кнопку Continue")
    def click_continue_button(self):
        self.continue_button.click()
    @allure.step("Нажатие на кнопку крестик у сообщения об ошибке")
    def click_error_button(self):
        self.error_button.click()

class CheckoutTwoPage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.item_card = ItemCard(page)
        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.item_price = page.locator('[data-test="inventory-item-price"]')
        self.item_description = page.locator('[data-test="inventory-item-desc"]')
        self.item_quantity = page.locator('[data-test="item-quantity"]')
        self.payment_info_value = page.locator('[data-test="payment-info-value"]')
        self.shipping_information = page.locator('[data-test="shipping-info-value"]')
        self.item_total = page.locator('[data-test="subtotal-label"]')
        self.tax_value = page.locator('[data-test="tax-label"]')
        self.total_amount = page.locator('[data-test="total-label"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.finish_button = page.locator('[data-test="finish"]')
    @allure.step("Нажатие на кнопку Finish (завершение заказа)")
    def click_finish_button(self):
        self.finish_button.click()
    @allure.step("Нажатие на кнопку Cancel")
    def click_cancel_button(self):
        self.cancel_button.click()
    @allure.step("Подсчёт конечной суммы товаров в корзине")
    def calculate_items_subtotal(self):
        price_text = self.item_price.all_inner_texts()
        total_price = 0
        for item in price_text:
            clean_price = item.replace("$", "")
            total_price += float(clean_price)
        return round(total_price, 2)
    @allure.step("Преобразование item total в число")
    def get_displayed_subtotal(self):
        item_total = self.item_total.inner_text()
        item_total = item_total.replace("Item total: $", "")
        return round(float(item_total), 2)
    @allure.step("Расчёт налогов от суммы товаров в корзине")
    def calculate_tax(self):
        tax_value = self.calculate_items_subtotal()*0.08
        return round(tax_value, 2)
    @allure.step("Преобразование Tax в число")
    def get_displayed_tax(self):
        tax_value = self.tax_value.inner_text()
        tax_value = tax_value.replace("Tax: $", "")
        return float(tax_value)
    @allure.step("Расчёт итоговой суммы товаров с налогами")
    def calculate_total_with_tax(self):
        total_value = self.calculate_items_subtotal() + self.calculate_tax()
        return round(total_value, 2)
    @allure.step("Преобразование итоговой суммы с налогами")
    def get_displayed_total_with_tax(self):
        total_value = self.total_amount.inner_text()
        total_value = total_value.replace("Total: $", "")
        return float(total_value)
    @allure.step("Переход в карточку товара из overview")
    def click_item_name(self):
        self.item_name.click()
    @allure.step("Получение названия единственного товара")
    def get_item_name(self):
        return self.item_name.inner_text()
    @allure.step("Получение цены единственного товара")
    def get_item_price(self):
        dirty_price = self.item_price.inner_text()
        clean_price = dirty_price.replace("$", "")
        return float(clean_price)
    @allure.step("Получение описания единственного товара")
    def get_item_description(self):
        return self.item_description.inner_text()
    @allure.step("Получение количества всех добавленных товаров в заказе")
    def get_item_count_in_order(self):
        return len(self.item_name.all_inner_texts())
    @allure.step("Получение списка названий товаров в заказе")
    def get_lst_item_names(self):
        return self.item_name.all_inner_texts()

class CheckoutCompletePage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')
        self.image_success = page.locator('[data-test="pony-express"]')
    @allure.step("Переход обратно на главную страницу магазина")
    def click_back_home_button(self):
        self.back_home_button.click()