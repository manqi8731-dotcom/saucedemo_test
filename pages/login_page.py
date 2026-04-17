"""
登录页面对象
1.封装登录页面的所有元素和操作
2.实现登录业务逻辑
3.集成错误处理
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    """SauceDemo登录页面"""

    # 页面元素定位器
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    PRODUCT_CONTAINER = (By.ID, "inventory_container")

    def __init__(self, driver):
        """
        初始化登录页面
        :param driver: WebDriver 实例
        """
        # 调用 BasePage 的 __init__ 方法，完成父类初始化,否则父类的 self.driver 等不会创建
        super().__init__(driver)
        self.url = "http://www.saucedemo.com"

    def open(self):
        """打开登录页面"""
        self.driver.get(self.url)
        # 等待 用户名输入框出现，确认页面加载完成
        self.wait_for_page_load()
        self._get_element(self.USERNAME_FIELD)

    def login(self, username, password):
        """
        执行登录操作
        :param username: 用户名
        :param password: 密码
        :return:
        """
        # 清空并输入用户名
        self.input_text(self.USERNAME_FIELD, username)
        # 输入密码
        self.input_text(self.PASSWORD_FIELD, password)
        # 点击登录按钮
        self.click_element(self.LOGIN_BUTTON)
        # 等待页面加载完成
        self.wait_for_page_load()

    def get_error_message(self):
        """获取错误提示信息"""
        # 用错误定位器进行定位，若出现错误信息(true)，则获取错误文本信息
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_logged_in(self):
        """检查是否登录成功"""
        return self.is_element_visible(self.PRODUCT_CONTAINER)

    def is_login_failed(self):
        """检查是否登录失败"""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def get_current_url(self):
        """获取当前URL"""
        return self.driver.current_url

    def login_with_valid_credentials(self):
        """使用标准用户登录（快捷方法）"""
        self.login("standard_user", "secret_sauce")

    def take_login_screenshot(self, username):
        """保存登录过程截图"""
        return self.take_screenshot(f"login_{username}")    # 该截图的名称是login_{username}

# 使用示例
if __name__ == "__main__":
    from core.driver_manager import DriverManager

    # 初始化驱动
    manager = DriverManager(headless=False)
    driver = manager.get_driver()

    try:
        # 创建登录页面实例
        login_page = LoginPage(driver)
        # 打开登录页面
        login_page.open()
        # 尝试登录
        login_page.login("standard_user", "secret_sauce")
        # 检查是否登录成功
        if login_page.is_logged_in():
            print("登录成功！")
            login_page.take_screenshot("login_success")
        else:
            error_msg = login_page.get_error_message()
            print(f"登录失败：{error_msg}")
            login_page.take_screenshot("login_failed")

    finally:
        manager.quit()









