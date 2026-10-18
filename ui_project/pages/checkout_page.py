import allure
from playwright.sync_api import Page
from ui_project.pages.base_page import BasePage
from ui_project.pages.components.header import HeaderComponent

class CheckoutOnePage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
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
        self.payment_info_value = page.locator('[data-test="payment-info-value"]')
        self.shipping_information = page.locator('[data-test="shipping-info-value"]')
        self.item_total = page.locator('[data-test="subtotal-label"]')
        self.tax_value = page.locator('[data-test="tax-label"]')
        self.total_amount = page.locator('[data-test="total-label"]')
        self.overview_cancel_button = page.locator('[data-test="cancel"]')
        self.finish_button = page.locator('[data-test="finish"]')
    @allure.step("Переход на последнюю страницу магазина")
    def click_finish_button(self):
        self.finish_button.click()

class CheckoutCompletePage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')
    @allure.step("Переход обратно на главную страницу магазина")
    def back_home(self):
        self.back_home_button.click()