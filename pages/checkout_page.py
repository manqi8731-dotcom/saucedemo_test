from selenium.webdriver.common.by import By
from core.base_page import BasePage


class CheckoutPage(BasePage):

    # Step1 页面元素
    first_name_input = (By.ID, "first-name")
    last_name_input = (By.ID, "last-name")
    postal_code_input = (By.ID, "postal-code")
    continue_btn = (By.ID, "continue")

    # Step2 页面元素
    item_total = (By.CLASS_NAME, "summary_subtotal_label")
    tax = (By.CLASS_NAME, "summary_tax_label")
    total = (By.CLASS_NAME, "summary_total_label")
    finish_btn = (By.ID, "finish")

    # 成功页
    success_text = (By.CLASS_NAME, "complete-header")

    # 错误提示
    error_msg = (By.CLASS_NAME, "error-message-container")

    # ====== 操作方法 ======

    def __init__(self, driver):
        """初始化 CheckoutPage"""
        super().__init__(driver)

    def fill_info(self, first, last, zip_code):
        """填写配送信息"""
        self.input_text(self.first_name_input, first)
        self.input_text(self.last_name_input, last)
        self.input_text(self.postal_code_input, zip_code)

    def click_continue(self):
        """点击继续按钮"""
        self.click_element(self.continue_btn)

    def get_item_total(self):
        """获取商品总额"""
        return self.get_text(self.item_total)

    def get_tax(self):
        """获取税额"""
        return self.get_text(self.tax)

    def get_total(self):
        """获取总金额"""
        return self.get_text(self.total)

    def click_finish(self):
        """点击完成按钮"""
        self.click_element(self.finish_btn)

    def get_success_text(self):
        """获取成功页面文本"""
        return self.get_text(self.success_text)

    def get_error_msg(self):
        """获取错误提示信息"""
        return self.get_text(self.error_msg)