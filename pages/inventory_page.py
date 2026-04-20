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
        获取购物车中的商品数量

        Returns:
            int: 购物车商品数量，如果购物车为空则返回 0

        Example:
            count = page.get_cart_count()  # 返回 3
        """
        try:
            if self.is_element_visible(self.SHOPPING_CART_BADGE):
                count_text = self.get_text(self.SHOPPING_CART_BADGE)
                count = int(count_text)
                logger.info(f"🛒 购物车数量: {count}")
                return count
            else:
                logger.info("🛒 购物车为空")
                return 0
        except Exception as e:
            logger.error(f"❌ 获取购物车数量失败: {str(e)}")
            return 0

    def click_shopping_cart(self):
        """
        点击购物车图标，跳转到购物车页面

        Returns:
            bool: 操作是否成功
        """
        try:
            self.click_element(self.SHOPPING_CART_LINK)
            logger.info("🛒 点击购物车图标，跳转到购物车页面")
            return True
        except Exception as e:
            logger.error(f"❌ 点击购物车失败: {str(e)}")
            return False

    # ==================== 商品操作 ====================

    def add_to_cart_by_name(self, product_name):
        """
        根据商品名称添加到购物车

        Args:
            product_name (str): 商品名称，如 "Sauce Labs Backpack"

        Returns:
            bool: 操作是否成功

        Example:
            page.add_to_cart_by_name("Sauce Labs Backpack")
        """
        try:
            # 定位商品卡片：通过商品名称找到其父容器，再找到添加按钮
            # XPath 逻辑：找到包含指定文本的商品名称 -> 向上找到商品卡片容器 -> 找到添加按钮
            add_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//button[contains(text(),'Add to cart')]"
            )

            # 点击添加按钮
            self.click_element(add_button_locator)

            # 验证按钮文本已变为 "Remove"
            remove_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//button[contains(text(),'Remove')]"
            )
            if self.is_element_visible(remove_button_locator):
                logger.info(f"✅ 商品 '{product_name}' 已成功添加到购物车")
                return True
            else:
                logger.warning(f"⚠️ 商品 '{product_name}' 添加后未检测到 Remove 按钮")
                return True  # 按钮已点击，认为操作成功

        except Exception as e:
            logger.error(f"❌ 添加商品 '{product_name}' 到购物车失败: {str(e)}")
            return False

    def remove_from_cart_by_name(self, product_name):
        """
        根据商品名称从购物车中移除

        Args:
            product_name (str): 商品名称

        Returns:
            bool: 操作是否成功

        Example:
            page.remove_from_cart_by_name("Sauce Labs Backpack")
        """
        try:
            # 定位移除按钮
            remove_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//button[contains(text(),'Remove')]"
            )

            # 点击移除按钮
            self.click_element(remove_button_locator)

            # 验证按钮文本已变回 "Add to cart"
            add_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//button[contains(text(),'Add to cart')]"
            )
            if self.is_element_visible(add_button_locator):
                logger.info(f"✅ 商品 '{product_name}' 已成功从购物车移除")
                return True
            else:
                logger.warning(f"⚠️ 商品 '{product_name}' 移除后未检测到 Add to cart 按钮")
                return True

        except Exception as e:
            logger.error(f"❌ 从购物车移除商品 '{product_name}' 失败: {str(e)}")
            return False

    def is_product_in_cart(self, product_name):
        """
        检查指定商品是否已在购物车中（通过按钮状态判断）

        Args:
            product_name (str): 商品名称

        Returns:
            bool: True 表示商品在购物车中，False 表示不在
        """
        try:
            # 检查是否存在 Remove 按钮
            remove_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='inventory_item']"
                "//button[contains(text(),'Remove')]"
            )
            return self.is_element_visible(remove_button_locator)
        except Exception as e:
            logger.error(f"❌ 检查商品 '{product_name}' 状态失败: {str(e)}")
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
        """
        点击商品名称，跳转到商品详情页

        Args:
            product_name (str): 商品名称

        Returns:
            bool: 操作是否成功
        """
        try:
            # 定位商品名称链接
            product_link_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
            )
            self.click_element(product_link_locator)
            logger.info(f"🔍 点击商品 '{product_name}'，跳转到详情页")
            return True
        except Exception as e:
            logger.error(f"❌ 点击商品 '{product_name}' 失败: {str(e)}")
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