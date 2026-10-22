import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
    @allure.step("Переход на страницу: {url}")
    def open_url(self, url:str):
        self.page.goto(url)