import allure
from playwright.sync_api import expect
from faker import Faker

faker = Faker()

@allure.feature("Управление товарами на странице")
@allure.title("Добавление товара в корзину по имени")
def test_add_item_name(go_to_inventory_page):
    go_to_inventory_page.add_item_name("sauce-labs-backpack")
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")

@allure.feature("Управление товарами на странице")
@allure.title("Удаление товара из корзины по имени")
def test_delete_item_name(go_to_inventory_page):
    go_to_inventory_page.add_item_name("sauce-labs-backpack")
    go_to_inventory_page.delete_item_name("sauce-labs-backpack")
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()

@allure.feature("Управление товарами на странице")
@allure.title("Добавление товара в корзину по номеру")
def test_add_item_number(go_to_inventory_page):
    max_item_count = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_count)
    go_to_inventory_page.add_item_number(item_number)
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")

@allure.feature("Управление товарами на странице")
@allure.title("Удаление товара из корзины по имени")
def test_delete_item_number(go_to_inventory_page):
    max_item_count = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_count)
    go_to_inventory_page.add_item_number(item_number)
    go_to_inventory_page.delete_item_number(item_number)
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()

@allure.feature("Управление товарами на странице")
@allure.title("Добавление всех товаров на странице")
def test_add_all_items(go_to_inventory_page):
    items_count = go_to_inventory_page.get_items_count()
    for i in range(1, items_count + 1):
        go_to_inventory_page.add_item_number(i)
    expect(go_to_inventory_page.header.cart_badge).to_have_text("6")
    expect(go_to_inventory_page.header.cart_badge).to_have_css("background-color", "rgb(226, 35, 26)")

@allure.feature("Управление товарами на странице")
@allure.title("Удаление всех товаров на странице")
def test_delete_all_items(go_to_inventory_page):
    items_count = go_to_inventory_page.get_items_count()
    for i in range(1, items_count + 1):
        go_to_inventory_page.add_item_number(i)
    for j in range(1, items_count + 1):
        go_to_inventory_page.delete_item_number(j)
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()

@allure.feature("Визуальное оформление страницы")
@allure.title("Проверка корректности цветов интерфейса")
def test_check_color(go_to_inventory_page):
    max_item_count = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_count)
    go_to_inventory_page.add_item_number(item_number)
    expect(go_to_inventory_page.button_action_item.nth(item_number-1)).to_have_css("border-bottom-color", "rgb(226, 35, 26)")
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    expect(go_to_inventory_page.header.cart_badge).to_have_css("background-color", "rgb(226, 35, 26)")

@allure.feature("Управление товарами на странице")
@allure.title("ДОбавление товара в корзину через карточку товара")
def test_add_item_through_product_card(go_to_inventory_page):
    max_item_count = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_count)
    go_to_inventory_page.click_item_name(item_number)
    go_to_inventory_page.button_action_item_in_card.click()
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")

@allure.feature("Управление товарами на странице")
@allure.title("Удаление товара из корзины через карточку товара")
def test_delete_item_through_product_card(go_to_inventory_page):
    max_item_count = go_to_inventory_page.get_items_count()
    item_number = faker.random_int(1, max_item_count)
    go_to_inventory_page.click_item_name(item_number)
    go_to_inventory_page.button_action_item_in_card.click()
    expect(go_to_inventory_page.header.cart_badge).to_have_text("1")
    go_to_inventory_page.button_action_item_in_card.click()
    expect(go_to_inventory_page.header.cart_badge).not_to_be_visible()

@allure.feature("Сортировка товаров на странице")
@allure.title("Проверки сортировки товаров по алфавиту (Z to A)")
def test_sort_items_z_to_a(go_to_inventory_page):
    go_to_inventory_page.select_sort_option("za")
    actual_names = go_to_inventory_page.get_all_item_names()
    expected_names = sorted(actual_names, reverse=True)
    assert actual_names == expected_names, f"Ожидался порядок {expected_names}, а получили {actual_names}"

@allure.feature("Сортировка товаров на странице")
@allure.title("Проверка сортировки товаров по алфавиту (A to Z)")
def test_sort_items_a_to_z(go_to_inventory_page):
    go_to_inventory_page.select_sort_option("az")
    actual_names = go_to_inventory_page.get_all_item_names()
    expected_names = sorted(actual_names)
    assert actual_names == expected_names, f"Ожидался порядок {expected_names}, а получили {actual_names}"

@allure.feature("Сортировка товаров на странице")
@allure.title("Проверка сортировки товаров по цене (Low to High)")
def test_sort_items_price_low_to_high(go_to_inventory_page):
    go_to_inventory_page.select_sort_option("lohi")
    actual_prices = go_to_inventory_page.get_all_item_prices()
    expected_prices = sorted(actual_prices)
    assert actual_prices == expected_prices, f"Цены не отсортировались по возврастанию. Ожидалось {expected_prices}, а получили {actual_prices}"

@allure.feature("Сортировка товаров на странице")
@allure.title("Проверка сортировки товаров по цене (High to Low)")
def test_sort_items_price_high_to_low(go_to_inventory_page):
    go_to_inventory_page.select_sort_option("hilo")
    actual_prices = go_to_inventory_page.get_all_item_prices()
    expected_prices = sorted(actual_prices, reverse=True)
    assert actual_prices == expected_prices, f"Цены не отсортировались по убыванию. Ожидалось {expected_prices}, а получили {actual_prices}"