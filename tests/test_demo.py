import allure
from allure_commons._allure import step
import requests
from selene import browser, have


@allure.feature("Добавление товаров в корзину")
@allure.title("Проверка добавления в корзину - успех")
def test_add_to_cart_laptop():
    with step("add product to cart with API"):
        url = "https://demowebshop.tricentis.com/addproducttocart/details/31/1"
        response = requests.post(url)
    with step("check response API"):
        assert response.status_code == 200
        cookie = response.cookies.get("Nop.customer")

    with step("check from UI added product in cart"):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.element('.product-name').should(have.exact_text('14.1-inch Laptop'))


@allure.title("Проверка добавления в корзину - провал")
def test_add_to_cart_giftcard():
    with step("add product to cart with API"):
        url = "https://demowebshop.tricentis.com/addproducttocart/details/2/1"
        response = requests.post(url)
    with step("check response API"):
        assert response.status_code == 200
        assert response.json() == {"success": False,
                                   "message": [
                                       "Enter valid recipient name",
                                       "Enter valid recipient email",
                                       "Enter valid sender name",
                                       "Enter valid sender email"
                                   ]
                                   }
        cookie = response.cookies.get("Nop.customer")

    with step("check from UI empty cart"):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.element('.order-summary-content').should(have.exact_text('Your Shopping Cart is empty!'))
