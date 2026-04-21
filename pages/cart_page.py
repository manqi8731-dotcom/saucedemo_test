"""
cart_page.py - Sauce Demo 购物车页面对象封装

功能说明：
    1. 查看购物车中的商品
    2. 继续购物 / 去结算
    3. 移除购物车中的商品
    4. 验证购物车状态

页面元素定位策略：
    - 使用语义化定位器
    - 支持动态商品列表
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """购物车页面 - Page Object 模式封装"""

    # ==================== 页面元素定位器 ====================
    # 页面标题
    PAGE_TITLE = (By.CLASS_NAME, "title")  # "Your Cart"

    # 购物车商品列表容器
    CART_ITEMS = (By.CLASS_NAME, "cart_item")  # 所有购物车商品项

    # 单个商品相关元素
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")  # 商品名称
    ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")  # 商品描述
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")  # 商品价格
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")  # 商品数量

    # 移除按钮
    REMOVE_BUTTON = (By.XPATH, "//button[contains(text(),'Remove')]")

    # 操作按钮
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")  # 继续购物
    CHECKOUT_BUTTON = (By.ID, "checkout")  # 去结算

    # 空购物车提示（如果存在）
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(),'Your cart is empty')]")

    def __init__(self, driver):
        """
        初始化购物车页面

        Args:
            driver: WebDriver 实例
        """
        super().__init__(driver)
        logger.info("初始化 CartPage - 购物车页面对象")

    # ==================== 页面基本信息 ====================

    def get_page_title(self):
        """
        获取购物车页面标题

        Returns:
            str: 页面标题文本

        Example:
            title = page.get_page_title()  # "Your Cart"
        """
        try:
            title = self.get_text(self.PAGE_TITLE)
            logger.info(f"购物车页面标题: {title}")
            return title
        except Exception as e:
            logger.error(f"获取页面标题失败: {str(e)}")
            return ""

    def is_empty(self):
        """
        检查购物车是否为空

        Returns:
            bool: True 表示购物车为空，False 表示有商品
        """
        try:
            # 检查是否存在购物车商品项
            return not self.is_element_visible(self.CART_ITEMS)
        except Exception as e:
            logger.error(f"检查购物车是否为空失败: {str(e)}")
            return True

    # ==================== 购物车商品操作 ====================

    def get_cart_items_count(self):
        """
        获取购物车中的商品数量（按商品种类计数）

        Returns:
            int: 购物车中商品种类数量

        Example:
            count = page.get_cart_items_count()  # 3
        """
        try:
            if self.is_empty():
                logger.info("购物车为空，商品数量: 0")
                return 0

            elements = self.find_elements(self.CART_ITEMS)
            count = len(elements)
            logger.info(f"购物车中商品种类数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取购物车商品数量失败: {str(e)}")
            return 0

    def get_all_cart_item_names(self):
        """
        获取购物车中所有商品的名称列表

        Returns:
            list: 商品名称列表

        Example:
            names = page.get_all_cart_item_names()
            # ['Sauce Labs Backpack', 'Sauce Labs Bike Light']
        """
        try:
            if self.is_empty():
                logger.info("购物车为空，无商品名称")
                return []

            elements = self.find_elements(self.ITEM_NAME)
            item_names = [el.text for el in elements]
            logger.info(f"购物车商品列表: {item_names}")
            return item_names
        except Exception as e:
            logger.error(f"获取购物车商品名称列表失败: {str(e)}")
            return []

    def get_cart_item_details(self):
        """
        获取购物车中所有商品的详细信息

        Returns:
            list: 每个商品的字典信息列表
                [
                    {
                        "name": "Sauce Labs Backpack",
                        "description": "carry.allTheThings()...",
                        "price": "$29.99",
                        "quantity": "1"
                    },
                    ...
                ]
        """
        try:
            if self.is_empty():
                logger.info("购物车为空，无商品详情")
                return []

            cart_items = self.find_elements(self.CART_ITEMS)
            details = []

            for item in cart_items:
                try:
                    # 获取商品名称
                    name_elem = item.find_element(*self.ITEM_NAME)
                    name = name_elem.text

                    # 获取商品描述
                    desc_elem = item.find_element(*self.ITEM_DESC)
                    description = desc_elem.text

                    # 获取商品价格
                    price_elem = item.find_element(*self.ITEM_PRICE)
                    price = price_elem.text

                    # 获取商品数量
                    qty_elem = item.find_element(*self.ITEM_QUANTITY)
                    quantity = qty_elem.text

                    details.append({
                        "name": name,
                        "description": description,
                        "price": price,
                        "quantity": quantity
                    })

                except Exception as e:
                    logger.warning(f"获取单个商品详情失败: {str(e)}")
                    continue

            logger.info(f"购物车商品详情: {details}")
            return details

        except Exception as e:
            logger.error(f"获取购物车商品详情失败: {str(e)}")
            return []

    def remove_item_by_name(self, product_name):
        """
        从购物车中移除指定商品

        Args:
            product_name (str): 要移除的商品名称

        Returns:
            bool: 操作是否成功

        Example:
            page.remove_item_by_name("Sauce Labs Backpack")
        """
        try:
            # 定位指定商品的移除按钮
            # XPath 逻辑：找到包含指定商品名称的购物车项 -> 找到移除按钮
            remove_button_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
                "/ancestor::div[@class='cart_item']"
                "//button[contains(text(),'Remove')]"
            )

            # 点击移除按钮
            self.click_element(remove_button_locator)

            # 验证商品已被移除（检查商品名称是否还存在）
            product_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
            )

            # 等待元素消失
            self.wait_for_element_invisibility(product_locator)

            logger.info(f"已从购物车移除商品: {product_name}")
            return True

        except Exception as e:
            logger.error(f"从购物车移除商品 '{product_name}' 失败: {str(e)}")
            return False

    def is_item_in_cart(self, product_name):
        """
        检查指定商品是否在购物车中

        Args:
            product_name (str): 商品名称

        Returns:
            bool: True 表示商品在购物车中
        """
        try:
            product_locator = (
                By.XPATH,
                f"//div[@class='inventory_item_name' and text()='{product_name}']"
            )
            return self.is_element_visible(product_locator)
        except Exception as e:
            logger.error(f"检查商品 '{product_name}' 是否在购物车中失败: {str(e)}")
            return False

    # ==================== 按钮操作 ====================

    def click_continue_shopping(self):
        """
        点击"继续购物"按钮，返回商品列表页

        Returns:
            bool: 操作是否成功
        """
        try:
            self.click_element(self.CONTINUE_SHOPPING_BUTTON)
            logger.info("点击'继续购物'，返回商品列表页")
            return True
        except Exception as e:
            logger.error(f"点击'继续购物'按钮失败: {str(e)}")
            return False

    def click_checkout(self):
        """
        点击"去结算"按钮，跳转到结算页面

        Returns:
            bool: 操作是否成功
        """
        try:
            self.click_element(self.CHECKOUT_BUTTON)
            logger.info("点击'去结算'，跳转到结算页面")
            return True
        except Exception as e:
            logger.error(f"点击'去结算'按钮失败: {str(e)}")
            return False

    # ==================== 购物车验证 ====================

    def verify_cart_contains(self, expected_items):
        """
        验证购物车中包含指定的商品列表

        Args:
            expected_items (list): 期望的商品名称列表

        Returns:
            bool: True 表示购物车包含所有期望商品

        Example:
            page.verify_cart_contains(["Sauce Labs Backpack", "Sauce Labs Bike Light"])
        """
        try:
            actual_items = self.get_all_cart_item_names()

            # 检查是否包含所有期望商品
            for item in expected_items:
                if item not in actual_items:
                    logger.error(f"购物车缺少商品: {item}")
                    return False

            logger.info(f"购物车验证通过，包含所有期望商品: {expected_items}")
            return True

        except Exception as e:
            logger.error(f"验证购物车内容失败: {str(e)}")
            return False

    def verify_cart_empty(self):
        """
        验证购物车是否为空

        Returns:
            bool: True 表示购物车为空
        """
        try:
            is_empty = self.is_empty()
            if is_empty:
                logger.info("购物车为空，验证通过")
            else:
                logger.error("购物车不为空，验证失败")
            return is_empty
        except Exception as e:
            logger.error(f"验证购物车为空失败: {str(e)}")
            return False