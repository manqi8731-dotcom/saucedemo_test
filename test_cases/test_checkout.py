import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout:

    def test_checkout_success(self, driver):
        # 1️⃣ 打开登录页面并登录
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # 2️⃣ 加商品（使用正确的现有方法）
        inventory = InventoryPage(driver)
        inventory.add_to_cart_by_name("Sauce Labs Backpack")
        inventory.add_to_cart_by_name("Sauce Labs Bike Light")
        inventory.click_shopping_cart()  # 进入购物车页面

        # 3️⃣ 购物车 → checkout
        cart = CartPage(driver)
        cart.click_checkout()

        # 4️⃣ 填写信息
        checkout = CheckoutPage(driver)
        checkout.fill_info("test", "user", "123456")
        checkout.click_continue()

        # 5️⃣ 校验金额（PO重点）
        item_total = checkout.get_item_total()
        tax = checkout.get_tax()
        total = checkout.get_total()

        assert "Item total" in item_total
        assert "Tax" in tax
        assert "Total" in total

        # 6️⃣ 提交订单
        checkout.click_finish()

        # 7️⃣ 校验成功
        success = checkout.get_success_text()
        assert "Thank you for your order" in success

    def test_checkout_info_required(self, driver):
        # 1️⃣ 打开登录页面并登录
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        inventory.add_to_cart_by_name("Sauce Labs Backpack")
        inventory.click_shopping_cart()  # 进入购物车页面

        cart = CartPage(driver)
        cart.click_checkout()

        checkout = CheckoutPage(driver)
        checkout.click_continue()  # 不填信息

        error = checkout.get_error_msg()
        assert "Error" in error

    # 金额计算
    def test_checkout_price_calculation(self, driver):
        # 1️⃣ 打开登录页面并登录
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        inventory.add_to_cart_by_name("Sauce Labs Backpack")
        inventory.click_shopping_cart()  # 进入购物车页面

        cart = CartPage(driver)
        cart.click_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_info("test", "user", "123456")
        checkout.click_continue()

        item_total = float(checkout.get_item_total().split("$")[1])
        tax = float(checkout.get_tax().split("$")[1])
        total = float(checkout.get_total().split("$")[1])

        assert round(item_total + tax, 2) == round(total, 2)