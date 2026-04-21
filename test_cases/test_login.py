"""
登录测试用例
1.数据驱动测试
2.验证成功登录
3.验证失败登录
4.参数化测试
"""
import pytest
from pages.login_page import LoginPage
from utils.data_loader import DataLoader
import time

@pytest.mark.usefixtures("driver")
class TestLogin:
    """登录功能测试类"""

    @pytest.mark.parametrize("user_data", DataLoader.get_test_users())
    def test_user_login(self, user_data):
        """
        测试用户登录
        :param user_data: 从YAML加载的用户数据
        """
        login_page = LoginPage(self.driver)

        try:
            # 打开登录页面
            login_page.open()

            # 执行登录
            login_page.login(user_data["username"], user_data["password"])

            # 根据expected参数验证结果
            if user_data["expected"]:
                # 预期：登录成功
                assert login_page.is_logged_in(), f"用户{user_data['username']}应该登录成功"
                print(f"用户{user_data['username']}登录成功")

                # 保存成功截图
                screenshots_path = login_page.take_login_screenshot(user_data["username"])
                print(f"成功截图：{screenshots_path}")
            else:
                # 预期：登录失败
                assert login_page.is_login_failed(), f"用户{user_data['username']}应该登录失败"

                # 验证错误提示
                error_msg = login_page.get_error_message()
                assert user_data["error_msg"] in error_msg, (
                    f"错误提示不匹配\n"
                    f"预期包含：'{user_data['error_msg']}'\n"
                    f"实际得到：'{error_msg}'"
                )
                print(f"用户{user_data['username']}登录失败，错误提示正确")

                # 保存失败截图
                screenshots_path = login_page.take_login_screenshot(user_data["username"])
                print(f"失败截图：{screenshots_path}")

            # 等待一会儿，让截图更清晰
            time.sleep(1)

        except Exception as e:
            # 发生异常时截图
            screenshots_path = login_page.take_screenshot(f"ERROR_{user_data['username']}")
            print(f"测试异常，截图已保存：{screenshots_path}")
            raise e

    def test_page_title(self):
        """测试页面标题"""
        login_page = LoginPage(self.driver)
        login_page.open()

        expected_title = "Swag Labs"
        actual_title = self.driver.title

        assert expected_title in actual_title, (
            f"标题不匹配\n"
            f"预期: '{expected_title}'\n"
            f"实际: '{actual_title}'"
        )
        print(f"页面标题正确: {actual_title}")

    def test_standard_user_flow(self):
        """标准用户完整流程测试"""
        login_page = LoginPage(self.driver)

        # 1. 打开登录页面
        login_page.open()
        assert "saucedemo.com" in login_page.get_current_url()
        print("登录页面打开成功")

        # 2. 使用标准用户登录
        login_page.login_with_valid_credentials()

        # 3. 验证登录成功
        assert login_page.is_logged_in(), "标准用户登录失败"
        print("标准用户登录成功")

        # 3. 验证登录成功
        assert login_page.is_logged_in(), "标准用户登录失败"
        print("标准用户登录成功")

# 测试运行配置
if __name__ == "__main__":
    # 直接运行测试（不通过pytest）
    pytest.main([
        "-v",  # 详细输出
        "-s",  # 显示print输出
        "--browser=chrome",  # 指定浏览器
        # "--headless",  # 无头模式
        __file__  # 当前文件
    ])









