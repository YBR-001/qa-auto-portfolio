import allure, pytest
from playwright.sync_api import expect
from config import config

@allure.feature("Авторизация")
@allure.title("Успешный вход с стандартным пользователем")
@pytest.mark.smoke
def test_login_successful(login_page, inventory_page, base_page):
    login_page.open_url(config.base_url)
    expect(login_page.login_button).to_have_css("background-color", "rgb(61, 220, 145)")
    login_page.login(config.standard_user, config.password)
    expect(base_page.title).to_have_text("Products")

@allure.feature("Авторизация")
@allure.title("Негативные проверки при авторизации")
@pytest.mark.parametrize("username, password, expected_error_msg", [("locked_out_user", config.password, "Epic sadface: Sorry, this user has been locked out."),
                                                                    (config.standard_user, "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
                                                                    ("", "", "Epic sadface: Username is required"),
                                                                    (config.standard_user, "", "Epic sadface: Password is required"),
                                                                    ("", config.password, "Epic sadface: Username is required")])
def test_login_failure(login_page, username: str, password: str, expected_error_msg):
    login_page.open_url(config.base_url)
    login_page.login(username, password)
    expect(login_page.login_error_msg).to_have_text(expected_error_msg)
    expect(login_page.login_container_error_msg).to_have_css("background-color", "rgb(226, 35, 26)")

@pytest.mark.skip(reason= f"Баг Jira-1234: {config.problem_user} вызывает зависания страницы")
def test_problem_user_login(login_page, inventory_page):
    login_page.open_url(config.base_url)
    login_page.login(config.problem_user, config.password)