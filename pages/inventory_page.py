"""
inventory_page.py - Sauce Demo 商品列表页对象封装

功能说明：
    1. 商品展示与操作（添加/移除购物车）
    2. 排序功能
    3. 购物车数量显示
    4. 商品详情页跳转

页面元素定位策略：
    - 使用相对 XPath，避免硬编码索引
    - 优先使用语义化定位（如商品名称、按钮文本）
    - 兼容多种浏览器（Chrome/Firefox/Edge）
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import logging

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """商品列表页 - Page Object 模式封装"""

    # ==================== 页面元素定位器 ====================
    # 顶部导航栏
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")  # 购物车图标链接
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")  # 购物车数量徽章

    # 排序下拉框
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    # 商品列表容器
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")  # 单个商品卡片
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")  # 所有商品列表

    # 商品名称（用于定位特定商品）
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    # 商品价格
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")

    # 添加/移除按钮（动态变化）
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(),'Add to cart')]")
    REMOVE_BUTTON = (By.XPATH, "//button[contains(text(),'Remove')]")

    # 商品图片和描述
    ITEM_IMAGE = (By.CLASS_NAME, "inventory_item_img")
    ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")

    # ==================== 排序选项文本 ====================
    SORT_OPTIONS = {
        "name_asc": "Name (A to Z)",
        "name_desc": "Name (Z to A)",
        "price_asc": "Price (low to high)",
        "price_desc": "Price (high to low)"
    }

    def __init__(self, driver):
        """
        初始化商品列表页

        Args:
            driver: WebDriver 实例
        """
        super().__init__(driver)
        logger.info("✅ 初始化 InventoryPage - 商品列表页对象")

    # ==================== 购物车相关操作 ====================

    def get_cart_count(self):
        """
        获取购物车徽章显示的数量

        Returns:
            int: 购物车商品数量（0 表示空）
        """
        try:
            cart_badge_locator = (By.CLASS_NAME, "shopping_cart_badge")

            # 检查徽章是否存在
            if self.is_element_visible(cart_badge_locator):
                count_text = self.driver.find_element(*cart_badge_locator).text.strip()
                count = int(count_text) if count_text.isdigit() else 0
                logger.info(f"🛒 购物车数量: {count}")
                return count
            else:
                logger.info("🛒 购物车为空（徽章不存在）")
                return 0

        except Exception as e:
            logger.error(f"❌ 获取购物车数量失败: {str(e)}")
            return 0



    # ==================== 商品操作 ====================
    def add_to_cart_by_name(self, product_name):
        """
        根据商品名称添加到购物车（使用 data-test 属性，最可靠）

        Args:
            product_name (str): 商品名称，如 "Sauce Labs Backpack"

        Returns:
            bool: 操作是否成功
        """
        try:
            # 将商品名称转换为 data-test 格式：小写 + 去空格 + 连字符
            # 示例: "Sauce Labs Backpack" -> "sauce-labs-backpack"
            data_test_value = product_name.lower().replace(" ", "-")
            button_locator = (
                By.CSS_SELECTOR,
                f"button[data-test='add-to-cart-{data_test_value}']"
            )

            # 使用显式等待确保按钮可点击
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            wait = WebDriverWait(self.driver, 10)
            add_button = wait.until(EC.element_to_be_clickable(button_locator))
            add_button.click()

            # 验证按钮已变为 Remove
            remove_locator = (
                By.CSS_SELECTOR,
                f"button[data-test='remove-{data_test_value}']"
            )

            # 等待 Remove 按钮出现
            wait.until(EC.presence_of_element_located(remove_locator))
            logger.info(f"✅ 商品 '{product_name}' 已成功添加到购物车")
            return True

        except Exception as e:
            logger.error(f"❌ 添加商品 '{product_name}' 到购物车失败: {str(e)}")
            return False

    def remove_from_cart_by_name(self, product_name):
        try:
            data_test_value = product_name.lower().replace(" ", "-")
            remove_locator = (
                By.CSS_SELECTOR,
                f"button[data-test='remove-{data_test_value}']"
            )

            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            wait = WebDriverWait(self.driver, 10)
            remove_button = wait.until(EC.element_to_be_clickable(remove_locator))
            remove_button.click()

            # 验证变回 Add 按钮
            add_locator = (
                By.CSS_SELECTOR,
                f"button[data-test='add-to-cart-{data_test_value}']"
            )
            wait.until(EC.presence_of_element_located(add_locator))
            logger.info(f"✅ 商品 '{product_name}' 已成功从购物车移除")
            return True

        except Exception as e:
            logger.error(f"❌ 移除商品 '{product_name}' 失败: {e}")
            return False

    def click_shopping_cart(self):
        """
        点击购物车图标进入购物车页面

        Returns:
            bool: 操作是否成功
        """
        try:
            cart_locator = (By.CLASS_NAME, "shopping_cart_link")
            self.click_element(cart_locator)
            logger.info("✅ 已点击购物车图标，进入购物车页面")
            return True
        except Exception as e:
            logger.error(f"❌ 点击购物车图标失败: {str(e)}")
            return False

    def is_product_in_cart(self, product_name):
        """
        检查商品是否已在购物车中（通过检查按钮是否变为 Remove）

        Args:
            product_name (str): 商品名称

        Returns:
            bool: True 表示商品已在购物车中
        """
        try:
            # 将商品名称转换为 data-test 格式
            data_test_value = product_name.lower().replace(" ", "-")

            # 检查 Remove 按钮是否存在（表示商品已在购物车）
            remove_locator = (
                By.CSS_SELECTOR,
                f"button[data-test='remove-{data_test_value}']"
            )

            # 使用显式等待检查元素是否存在
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(remove_locator)
                )
                logger.info(f"✅ 检测到商品 '{product_name}' 的 Remove 按钮，商品已在购物车中")
                return True
            except:
                logger.warning(f"⚠️ 商品 '{product_name}' 的 Remove 按钮不存在，商品可能未在购物车中")
                return False

        except Exception as e:
            logger.error(f"❌ 检查商品 '{product_name}' 是否在购物车中失败: {str(e)}")
            return False

    # ==================== 排序功能 ====================

    def sort_products(self, sort_option):
        """
        对商品进行排序

        Args:
            sort_option (str): 排序选项
                - "name_asc": 名称 A-Z
                - "name_desc": 名称 Z-A
                - "price_asc": 价格低到高
                - "price_desc": 价格高到低

        Returns:
            bool: 操作是否成功
        """
        try:
            # 获取排序下拉框
            sort_element = self.find_element(self.SORT_DROPDOWN)
            select = Select(sort_element)

            # 选择排序选项
            if sort_option in self.SORT_OPTIONS:
                select.select_by_visible_text(self.SORT_OPTIONS[sort_option])
                logger.info(f"✅ 已按 '{self.SORT_OPTIONS[sort_option]}' 排序商品")
                # 等待排序完成（页面会重新渲染）
                self.wait_for_page_load()
                return True
            else:
                logger.error(f"❌ 无效的排序选项: {sort_option}")
                return False

        except Exception as e:
            logger.error(f"❌ 排序商品失败: {str(e)}")
            return False

    def get_all_product_names(self):
        """
        获取当前页面所有商品的名称列表

        Returns:
            list: 商品名称列表

        Example:
            names = page.get_all_product_names()
            # ['Sauce Labs Backpack', 'Sauce Labs Bike Light', ...]
        """
        try:
            elements = self.find_elements(self.ITEM_NAME)
            product_names = [el.text for el in elements]
            logger.info(f"📦 当前页面共有 {len(product_names)} 个商品")
            return product_names
        except Exception as e:
            logger.error(f"❌ 获取商品名称列表失败: {str(e)}")
            return []

    def get_product_price(self, product_name):
        """
        获取指定商品的价格

        Args:
            product_name (str): 商品名称

        Returns:
            str: 价格文本（如 "$29.99"），失败返回 None
        """
        try:
            # 定位商品价格元素
            price_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item_description']"
                "//div[@class='pricebar']/div[@class='inventory_item_price']"
            )
            price_text = self.get_text(price_locator)
            logger.info(f"💰 商品 '{product_name}' 价格: {price_text}")
            return price_text
        except Exception as e:
            logger.error(f"❌ 获取商品 '{product_name}' 价格失败: {str(e)}")
            return None

    # ==================== 商品详情页跳转 ====================

    def click_product_name(self, product_name):
        try:
            locator = (
                By.XPATH,
                f"//a[.//div[contains(text(), '{product_name}')]]"
            )
            self.click_element(locator)
            return True
        except Exception as e:
            self.logger.error(f"❌ 点击商品名称失败 {product_name}: {e}")
            return False
    def click_product_image(self, product_name):
        """
        点击商品图片，跳转到商品详情页

        Args:
            product_name (str): 商品名称

        Returns:
            bool: 操作是否成功
        """
        try:
            # 定位商品图片
            image_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//img[@class='inventory_item_img']"
            )
            self.click_element(image_locator)
            logger.info(f"🖼️ 点击商品 '{product_name}' 图片，跳转到详情页")
            return True
        except Exception as e:
            logger.error(f"❌ 点击商品 '{product_name}' 图片失败: {str(e)}")
            return False

    # ==================== 页面验证 ====================

    def is_page_loaded(self):
        """
        验证商品列表页是否已加载完成

        Returns:
            bool: True 表示页面已加载
        """
        try:
            # 检查至少存在一个商品卡片
            return self.is_element_visible(self.INVENTORY_ITEM)
        except Exception as e:
            logger.error(f"❌ 页面加载验证失败: {str(e)}")
            return False

    def get_total_products_count(self):
        """
        获取当前页面显示的商品总数

        Returns:
            int: 商品数量
        """
        try:
            elements = self.find_elements(self.INVENTORY_ITEMS)
            count = len(elements)
            logger.info(f"📊 当前页面商品总数: {count}")
            return count
        except Exception as e:
            logger.error(f"❌ 获取商品总数失败: {str(e)}")
            return 0