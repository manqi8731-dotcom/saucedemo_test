"""
test_cart.py - 购物车管理功能测试用例

测试范围：
    1. ✅ 商品添加到购物车
    2. ✅ 商品从购物车移除
    3. ✅ 购物车数量显示
    4. ✅ 跨页面购物车状态保持
    5. ✅ 购物车详情验证
    6. ✅ 继续购物 / 去结算功能

测试数据：
    - 使用标准用户登录
    - 测试多个商品的添加/移除
    - 验证购物车徽章计数
"""

import pytest
import logging

from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("driver")
class TestCartManagement:
    """购物车管理功能测试类"""

    # ==================== 测试前置条件 ====================

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        每个测试方法执行前的自动设置

        流程：
            1. 使用标准用户登录
            2. 初始化商品列表页和购物车页对象
            3. 确保进入商品列表页

        Args:
            driver: WebDriver 实例（通过 fixture 注入）
        """
        logger.info("🔧 ===== 测试前置准备开始 =====")

        # 1. 登录系统（使用标准用户）
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # 2. 验证登录成功 - 使用 URL 检查（最可靠）
        current_url = driver.current_url
        assert "inventory.html" in current_url, \
            f"❌ 登录失败！当前 URL: {current_url}"
        logger.info(f"✅ 登录成功，已进入商品列表页: {current_url}")

        # 3. 初始化页面对象
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)

        # 4. 验证商品列表页已加载
        assert self.inventory_page.is_page_loaded(), "❌ 商品列表页未加载"
        logger.info("✅ 商品列表页加载成功")

        # 5. 确保购物车为空（清理前置状态）
        initial_count = self.inventory_page.get_cart_count()
        if initial_count > 0:
            logger.warning(f"⚠️ 购物车已有 {initial_count} 个商品，将清空购物车")
            self._clear_cart(driver)

        logger.info("🔧 ===== 测试前置准备完成 =====\n")

    def _clear_cart(self, driver):
        """
        辅助方法：清空购物车（用于测试前置清理）

        Args:
            driver: WebDriver 实例
        """
        try:
            # 点击购物车图标
            self.inventory_page.click_shopping_cart()

            # 获取所有商品并逐个移除
            cart_items = self.cart_page.get_all_cart_item_names()
            for item_name in cart_items:
                self.cart_page.remove_item_by_name(item_name)

            # 返回商品列表页
            self.cart_page.click_continue_shopping()

            logger.info(f"🧹 已清空购物车，移除 {len(cart_items)} 个商品")

        except Exception as e:
            logger.error(f"❌ 清空购物车失败: {str(e)}")

    # ==================== 测试用例 1: 添加单个商品 ====================

    def test_add_single_product_to_cart(self):
        """
        测试场景：添加单个商品到购物车

        验证点：
            1. 点击"Add to cart"按钮
            2. 按钮文本变为"Remove"
            3. 购物车徽章显示数量 1
            4. 购物车页面显示该商品

        测试数据：
            - 商品名称: "Sauce Labs Backpack"
        """
        logger.info("🧪 ===== 测试用例 1: 添加单个商品到购物车 =====")

        # 测试数据
        product_name = "Sauce Labs Backpack"

        # 1. 获取添加前的购物车数量
        initial_count = self.inventory_page.get_cart_count()
        logger.info(f"📊 初始购物车数量: {initial_count}")

        # 2. 添加商品到购物车
        assert self.inventory_page.add_to_cart_by_name(product_name), \
            f"❌ 添加商品 '{product_name}' 失败"

        # 3. 验证购物车数量增加
        new_count = self.inventory_page.get_cart_count()
        assert new_count == initial_count + 1, \
            f"❌ 购物车数量未正确更新，期望 {initial_count + 1}，实际 {new_count}"
        logger.info(f"✅ 购物车数量验证通过: {initial_count} -> {new_count}")

        # 4. 验证按钮状态已改变
        assert self.inventory_page.is_product_in_cart(product_name), \
            f"❌ 商品 '{product_name}' 未正确添加到购物车"
        logger.info(f"✅ 按钮状态验证通过，商品已添加")

        # 5. 进入购物车页面验证
        self.inventory_page.click_shopping_cart()

        # 6. 验证购物车页面显示该商品
        assert self.cart_page.is_item_in_cart(product_name), \
            f"❌ 购物车页面未显示商品 '{product_name}'"
        logger.info(f"✅ 购物车页面验证通过，包含商品: {product_name}")

        # 7. 返回商品列表页
        self.cart_page.click_continue_shopping()

        logger.info("✅ ===== 测试用例 1 通过 =====\n")

    # ==================== 测试用例 2: 移除单个商品 ====================

    def test_remove_single_product_from_cart(self):
        """
        测试场景：从购物车中移除单个商品

        验证点：
            1. 先添加商品到购物车
            2. 点击"Remove"按钮
            3. 按钮文本变回"Add to cart"
            4. 购物车徽章数量减少
            5. 购物车页面不再显示该商品

        测试数据：
            - 商品名称: "Sauce Labs Bike Light"
        """
        logger.info("🧪 ===== 测试用例 2: 从购物车移除单个商品 =====")

        # 测试数据
        product_name = "Sauce Labs Bike Light"

        # 1. 先添加商品到购物车
        assert self.inventory_page.add_to_cart_by_name(product_name), \
            f"❌ 预置条件失败：添加商品 '{product_name}' 失败"

        # 2. 记录添加后的购物车数量
        count_before_remove = self.inventory_page.get_cart_count()
        logger.info(f"📊 移除前购物车数量: {count_before_remove}")

        # 3. 从购物车移除商品
        assert self.inventory_page.remove_from_cart_by_name(product_name), \
            f"❌ 移除商品 '{product_name}' 失败"

        # 4. 验证购物车数量减少
        count_after_remove = self.inventory_page.get_cart_count()
        assert count_after_remove == count_before_remove - 1, \
            f"❌ 购物车数量未正确减少，期望 {count_before_remove - 1}，实际 {count_after_remove}"
        logger.info(f"✅ 购物车数量验证通过: {count_before_remove} -> {count_after_remove}")

        # 5. 验证按钮状态已恢复
        assert not self.inventory_page.is_product_in_cart(product_name), \
            f"❌ 商品 '{product_name}' 未正确从购物车移除"
        logger.info(f"✅ 按钮状态验证通过，商品已移除")

        # 6. 进入购物车页面验证
        self.inventory_page.click_shopping_cart()

        # 7. 验证购物车页面不包含该商品
        assert not self.cart_page.is_item_in_cart(product_name), \
            f"❌ 购物车页面仍显示已移除的商品 '{product_name}'"
        logger.info(f"✅ 购物车页面验证通过，不包含商品: {product_name}")

        # 8. 返回商品列表页
        self.cart_page.click_continue_shopping()

        logger.info("✅ ===== 测试用例 2 通过 =====\n")

    # ==================== 测试用例 3: 添加多个商品 ====================

    def test_add_multiple_products_to_cart(self):
        """
        测试场景：添加多个不同商品到购物车

        验证点：
            1. 依次添加多个商品
            2. 购物车徽章显示正确总数
            3. 购物车页面显示所有添加的商品
            4. 每个商品的详细信息正确

        测试数据：
            - 商品列表: ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        """
        logger.info("🧪 ===== 测试用例 3: 添加多个商品到购物车 =====")

        # 测试数据
        products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]

        # 1. 依次添加所有商品
        for product in products:
            assert self.inventory_page.add_to_cart_by_name(product), \
                f"❌ 添加商品 '{product}' 失败"
            logger.info(f"✅ 已添加商品: {product}")

        # 2. 验证购物车徽章显示正确数量
        cart_count = self.inventory_page.get_cart_count()
        assert cart_count == len(products), \
            f"❌ 购物车数量不正确，期望 {len(products)}，实际 {cart_count}"
        logger.info(f"✅ 购物车徽章数量验证通过: {cart_count}")

        # 3. 进入购物车页面
        self.inventory_page.click_shopping_cart()

        # 4. 验证购物车包含所有商品
        cart_items = self.cart_page.get_all_cart_item_names()
        assert len(cart_items) == len(products), \
            f"❌ 购物车商品数量不正确，期望 {len(products)}，实际 {len(cart_items)}"

        for product in products:
            assert product in cart_items, \
                f"❌ 购物车缺少商品: {product}"
            logger.info(f"✅ 购物车包含商品: {product}")

        # 5. 验证每个商品的详细信息
        item_details = self.cart_page.get_cart_item_details()
        logger.info(f"📋 购物车商品详情: {item_details}")

        # 6. 验证商品数量均为 1
        for detail in item_details:
            assert detail["quantity"] == "1", \
                f"❌ 商品 '{detail['name']}' 数量不正确，期望 '1'，实际 '{detail['quantity']}'"

        logger.info("✅ 所有商品数量验证通过")

        # 7. 返回商品列表页
        self.cart_page.click_continue_shopping()

        logger.info("✅ ===== 测试用例 3 通过 =====\n")

    # ==================== 测试用例 4: 跨页面购物车状态保持 ====================

    def test_cart_persistence_across_pages(self):
        """
        测试场景：验证购物车状态在跨页面操作时保持

        验证点：
            1. 添加商品到购物车
            2. 跳转到商品详情页
            3. 返回商品列表页
            4. 购物车数量和内容保持不变
            5. 进入购物车页面验证内容

        测试数据：
            - 商品名称: "Sauce Labs Fleece Jacket"
        """
        logger.info("🧪 ===== 测试用例 4: 跨页面购物车状态保持 =====")

        # 测试数据
        product_name = "Sauce Labs Fleece Jacket"

        # 1. 添加商品到购物车
        assert self.inventory_page.add_to_cart_by_name(product_name), \
            f"❌ 添加商品 '{product_name}' 失败"

        # 2. 记录购物车数量
        count_before_navigation = self.inventory_page.get_cart_count()
        logger.info(f"📊 导航前购物车数量: {count_before_navigation}")

        # 3. 跳转到商品详情页（通过点击商品名称）
        assert self.inventory_page.click_product_name(product_name), \
            f"❌ 跳转到商品详情页失败"
        logger.info(f"🔍 已跳转到商品 '{product_name}' 详情页")

        # 4. 等待页面加载（商品详情页会有"Back to products"按钮）
        self.inventory_page.wait_for_element_visibility(
            (By.ID, "back-to-products")
        )

        # 5. 返回商品列表页
        self.inventory_page.click_element((By.ID, "back-to-products"))
        logger.info("🔙 已返回商品列表页")

        # 6. 验证购物车数量保持不变
        count_after_navigation = self.inventory_page.get_cart_count()
        assert count_after_navigation == count_before_navigation, \
            f"❌ 购物车数量在跨页面后发生变化，之前 {count_before_navigation}，之后 {count_after_navigation}"
        logger.info(f"✅ 购物车数量保持不变: {count_after_navigation}")

        # 7. 验证商品仍在购物车中
        assert self.inventory_page.is_product_in_cart(product_name), \
            f"❌ 跨页面后商品 '{product_name}' 丢失"
        logger.info(f"✅ 商品状态验证通过，仍在购物车中")

        # 8. 进入购物车页面最终验证
        self.inventory_page.click_shopping_cart()

        assert self.cart_page.is_item_in_cart(product_name), \
            f"❌ 购物车页面未显示商品 '{product_name}'"
        logger.info(f"✅ 购物车页面最终验证通过")

        # 9. 返回商品列表页
        self.cart_page.click_continue_shopping()

        logger.info("✅ ===== 测试用例 4 通过 =====\n")

    # ==================== 测试用例 5: 购物车详情验证 ====================

    def test_cart_item_details_verification(self):
        """
        测试场景：验证购物车中商品的详细信息

        验证点：
            1. 添加商品到购物车
            2. 进入购物车页面
            3. 验证商品名称、描述、价格、数量
            4. 验证价格格式正确

        测试数据：
            - 商品名称: "Sauce Labs Onesie"
            - 期望价格: "$7.99"
        """
        logger.info("🧪 ===== 测试用例 5: 购物车商品详情验证 =====")

        # 测试数据
        product_name = "Sauce Labs Onesie"
        expected_price = "$7.99"

        # 1. 添加商品到购物车
        assert self.inventory_page.add_to_cart_by_name(product_name), \
            f"❌ 添加商品 '{product_name}' 失败"

        # 2. 进入购物车页面
        self.inventory_page.click_shopping_cart()

        # 3. 获取商品详细信息
        item_details = self.cart_page.get_cart_item_details()
        assert len(item_details) > 0, "❌ 购物车中无商品详情"

        # 4. 查找目标商品
        target_item = None
        for item in item_details:
            if item["name"] == product_name:
                target_item = item
                break

        assert target_item is not None, f"❌ 未找到商品 '{product_name}' 的详情"
        logger.info(f"📋 找到商品详情: {target_item}")

        # 5. 验证商品名称
        assert target_item["name"] == product_name, \
            f"❌ 商品名称不正确，期望 '{product_name}'，实际 '{target_item['name']}'"
        logger.info(f"✅ 商品名称验证通过: {target_item['name']}")

        # 6. 验证商品价格
        assert target_item["price"] == expected_price, \
            f"❌ 商品价格不正确，期望 '{expected_price}'，实际 '{target_item['price']}'"
        logger.info(f"✅ 商品价格验证通过: {target_item['price']}")

        # 7. 验证商品数量
        assert target_item["quantity"] == "1", \
            f"❌ 商品数量不正确，期望 '1'，实际 '{target_item['quantity']}'"
        logger.info(f"✅ 商品数量验证通过: {target_item['quantity']}")

        # 8. 验证价格格式（应以 $ 开头）
        assert target_item["price"].startswith("$"), \
            f"❌ 价格格式不正确，应以 $ 开头"
        logger.info(f"✅ 价格格式验证通过")

        # 9. 返回商品列表页
        self.cart_page.click_continue_shopping()

        logger.info("✅ ===== 测试用例 5 通过 =====\n")

    # ==================== 测试用例 6: 继续购物和去结算功能 ====================

    def test_continue_shopping_and_checkout_buttons(self):
        """
        测试场景：验证"继续购物"和"去结算"按钮功能

        验证点：
            1. 添加商品到购物车
            2. 进入购物车页面
            3. 点击"继续购物"返回商品列表页
            4. 再次进入购物车页面
            5. 点击"去结算"跳转到结算页面

        测试数据：
            - 商品名称: "Sauce Labs Backpack"
        """
        logger.info("🧪 ===== 测试用例 6: 继续购物和去结算按钮功能 =====")

        # 测试数据
        product_name = "Sauce Labs Backpack"

        # 1. 添加商品到购物车
        assert self.inventory_page.add_to_cart_by_name(product_name), \
            f"❌ 添加商品 '{product_name}' 失败"

        # 2. 进入购物车页面
        self.inventory_page.click_shopping_cart()

        # 3. 验证页面标题
        page_title = self.cart_page.get_page_title()
        assert page_title == "Your Cart", \
            f"❌ 购物车页面标题不正确，期望 'Your Cart'，实际 '{page_title}'"
        logger.info(f"✅ 购物车页面标题验证通过: {page_title}")

        # 4. 点击"继续购物"按钮
        assert self.cart_page.click_continue_shopping(), \
            "❌ 点击'继续购物'按钮失败"

        # 5. 验证已返回商品列表页
        assert self.inventory_page.is_page_loaded(), \
            "❌ 未成功返回商品列表页"
        logger.info("✅ '继续购物'功能验证通过，已返回商品列表页")

        # 6. 再次进入购物车页面
        self.inventory_page.click_shopping_cart()

        # 7. 验证购物车内容保持不变
        assert self.cart_page.is_item_in_cart(product_name), \
            f"❌ 点击'继续购物'后购物车内容丢失"
        logger.info("✅ 购物车内容在'继续购物'后保持不变")

        # 8. 点击"去结算"按钮（注：这里只验证跳转，不进行完整结算流程）
        assert self.cart_page.click_checkout(), \
            "❌ 点击'去结算'按钮失败"
        logger.info("✅ '去结算'按钮功能验证通过")

        # 9. 验证已跳转到结算页面（通过 URL 或页面元素判断）
        # 注意：这里只做简单验证，完整结算流程在其他测试用例中覆盖
        current_url = self.driver.current_url
        assert "checkout" in current_url, \
            f"❌ 未跳转到结算页面，当前 URL: {current_url}"
        logger.info(f"✅ 已成功跳转到结算页面: {current_url}")

        logger.info("✅ ===== 测试用例 6 通过 =====\n")

    # ==================== 测试后置清理 ====================

    def teardown_method(self, method):
        """
        每个测试方法执行后的清理工作

        流程：
            1. 清空购物车（确保不影响后续测试）
            2. 记录测试结束日志

        Args:
            method: 当前执行的测试方法
        """
        logger.info(f"🧹 ===== 测试后置清理: {method.__name__} =====")

        try:
            # 清空购物车
            self._clear_cart(self.driver)
            logger.info("✅ 购物车已清空")
        except Exception as e:
            logger.warning(f"⚠️ 清理购物车时出错: {str(e)}")

        logger.info(f"🧹 ===== 测试后置清理完成 =====\n")