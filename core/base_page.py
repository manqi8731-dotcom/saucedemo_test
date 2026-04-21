"""
基础页面类
1.封装常用元素定位方法
2.添加智能等待机制
3.截图功能集成
4.错误处理增强
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
import time
import os
from datetime import datetime

class BasePage:
    """所有页面类的基类"""

    def __init__(self, driver):
        """
        初始化基础页面
        :param driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)   # 默认等待10秒

    def _get_element(self, locator, condition=EC.presence_of_element_located):
        """
        智能获取元素
        :param locator: 元素定位器(By.XPATH, "//input[@id='user']")
        :param condition: 等待条件
        :return: WebElement 对象
        """

        try:
            return self.wait.until(condition(locator))     # 轮询等待，直到满足或超时
        except TimeoutException:
            raise TimeoutException(f"元素定位超时：{locator}")
        except Exception as e:
            raise Exception(f"获取元素失败：{str(e)}")

    def find_element(self, locator):
        """查找单个元素"""
        return self._get_element(locator)

    def find_elements(self, locator):
        """查找多个元素"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []   # 返回空列表，而不是异常

    def click_element(self, locator):
        """安全点击元素"""
        # EC.element_to_be_clickable:等待条件,元素可见且可点击（比默认条件更严格）
        element = self._get_element(locator, EC.element_to_be_clickable)

        # 处理元素被遮挡的情况
        # _ 表示忽略循环变量
        for _ in range(3):  # 最多重试3次
            try:
                element.click()
                return True  # 点击成功，立即返回，结束方法
            except ElementClickInterceptedException:
                time.sleep(0.5)     # 等待0.5秒，让遮挡物可能自动消失
                # execute_script(...)	执行 JavaScript 代码
                # scrollIntoView(true)	滚动页面，让元素居中显示到可视区域
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            except StaleElementReferenceException:  # 元素过时异常（页面刷新或 DOM 重建后，之前找到的元素引用失效）
                time.sleep(0.5)
                element = self._get_element(locator, EC.element_to_be_clickable)

        raise Exception(f"无法点击元素：{locator}")

    def input_text(self, locator, text):
        """输入文本"""
        element = self._get_element(locator, EC.element_to_be_clickable)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """ 获取元素文本"""
        element = self._get_element(locator)
        return element.text.strip()

    def is_element_visible(self, locator):
        """检查元素是否可见"""
        try:
            return self._get_element(locator, EC.visibility_of_element_located) is not None
        except TimeoutException:
            return False

    def is_element_enable(self, locator):
        """检查元素是否可用"""
        element = self._get_element(locator)
        return element.is_enabled()

    def take_screenshot(self, name="screenshot"):
        """
        截图并保存
        :param name: 截图名称
        :return: 截图文件路径
        """
        # 创建screenshots目录
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")    # 年月日_时分秒
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        # 截图
        self.driver.save_screenshot(filepath)
        print(f"截图已保存：{filepath}")
        return filepath

    def wait_for_page_load(self, timeout=10):
        """等待页面完全加载"""
        """
        1.lambda	声明匿名函数的关键字
        2.driver	形参：函数接收的参数（这里是 WebDriver 实例）
        3.driver.execute_script(...)	函数体：执行的具体操作
        4.lambda声明的函数，用完即弃，不需要命名
        """
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element_visibility(self, locator, timeout=10):
        """等待元素可见"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception as e:
            # 现在可以安全使用 self.logger 了
            self.logger.error(f"等待元素可见失败 {locator}: {e}")
            return None
    def wait_for_element_clickable(self, locator, timeout=10):
        """
        等待元素可点击

        Args:
            locator (tuple): 定位器 (By.XXX, "value")
            timeout (int): 超时时间（秒）

        Returns:
            WebElement: 可点击的元素
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except Exception as e:
            self.logger.error(f"等待元素可点击失败: {locator}, 错误: {str(e)}")
            return None

    def scroll_to_element(self, locator):
        """滚动到元素位置"""
        element = self._get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element)
        time.sleep(0.5)     # 等待滚动完成

    def handle_alert(self, accept=True):
        """处理JavaScript弹窗"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            if accept:
                alert.accept()
            else:
                alert.dismiss()
            return True
        except TimeoutException:
            return False

# 使用示例
if __name__ == "__main__":
    from core.driver_manager import DriverManager
    from selenium.webdriver.common.by import By

    # 初始化驱动
    manager = DriverManager(headless=False)
    driver = manager.get_driver()

    try:
        # 打开测试页面
        driver.get("https://www.saucedemo.com")

        # 创建基础页面实例
        base_page = BasePage(driver)

        # 测试元素定位
        username_field = (By.ID, "user-name")
        base_page.input_text(username_field, "standard_user")

        print("基础页面功能测试成功！")

    finally:
        manager.quit()














