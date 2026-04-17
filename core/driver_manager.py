"""
智能浏览器驱动管理：
1.自动检测操作系统
2.自动下载对应版本的浏览器驱动
3.支持Chrome/Firefox/Edge
4.驱动缓存机制，避免重复下载
"""

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import platform
import os

class DriverManager:
    """浏览器驱动管理"""

    def __init__(self, browser="chrome", headless=False):
        """
        初始化驱动管理
        :param browser: 浏览器类型（chrome/firefox/edge）
        :param headless: 是否无头模式
        """
        # 将传入的浏览器名转为小写（如 "Chrome" → "chrome"）
        self.browser = browser.lower()
        # 保存是否使用无头模式（True = 后台运行，不显示浏览器窗口）
        self.headless = headless
        # 初始化 driver 为 None，表示此时浏览器驱动尚未创建
        self.driver = None

    def get_driver(self):
        """获取浏览器驱动实例"""
        if self.driver is None:
            if self.browser == "chrome":
                self.driver = self._setup_chrome()
            elif self.browser == "firefox":
                self.driver = self._setup_firefox()
            elif self.browser == "edge":
                self.driver = self._setup_edge()
            else:
                raise ValueError(f"不支持的浏览器类型：{self.browser}")

        # 设置窗口最大化
        self.driver.maximize_window()
        return self.driver

    def _setup_chrome(self):
        """配置Chrome浏览器"""
        options = webdriver.ChromeOptions()

        # 无头模式配置
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            # 关闭沙箱安全机制（Linux/Docker 环境必需，避免权限问题）
            options.add_argument("--no-sandbox")
            # 禁用 /dev/shm 共享内存（解决 Docker/容器环境中内存不足导致的崩溃）
            options.add_argument("--disable-dev-shm-usage")

        # 常用优化参数
        options.add_argument("--start-maximized")
        # 禁用所有扩展插件（避免插件干扰自动化测试）
        options.add_argument("--disable-extensions")
        # 禁用信息提示条（如"Chrome 正受到自动测试软件的控制"提示）
        options.add_argument("--disable-infobars")
        # 禁用信息提示条（如"Chrome 正受到自动测试软件的控制"提示）
        options.add_argument("--disable-notifications")
        # 忽略 SSL 证书错误（测试 HTTPS 自签名证书网站时必需）
        options.add_argument("--ignore-certificate-errors")

        # 设置用户代理
        """
        反反爬
        1.伪装真实浏览器：某些网站会检测Selenium,设置UA降低被识别的概率
        2.模拟特定环境：固定Windows + Chrome 120的标识，避免被识别为自动化工具
        """
        user_agent = ("Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument(f"--user-agent={user_agent}")

        # 自动下载驱动并配置服务
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def _setup_firefox(self):
        """配置Firework浏览器"""
        options = webdriver.FirefoxOptions()

        if self.headless:
            options.add_argument("--headless")

        # 禁用网页通知弹窗（类似 Chrome 的 --disable-notifications）
        options.set_preference("dom.webnotifications.enabled", False)
        # 静音所有媒体（防止网页自动播放声音干扰）
        options.set_preference("media.volume_scale", "0.0")

        # 自动下载并安装 GeckoDriver（Firefox 的 WebDriver）
        service = FirefoxService(GeckoDriverManager().install())
        # 创建 Firefox 浏览器实例，应用所有配置
        driver = webdriver.Firefox(service=service, options=options)
        # 返回配置好的驱动对象
        return driver

    def _setup_edge(self):
        """配置Edge浏览器"""
        options = webdriver.EdgeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def quit(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            self.driver = None

# 使用示例
if __name__ == "__main__":
    # 测试驱动管理器
    # 创建一个DriverManager类的对象，名为manager
    manager = DriverManager(browser="chrome", headless=False)
    driver = manager.get_driver()
    driver.get("https://www.saucedemo.com")
    print(f"成功打开：{driver.title}")
    manager.quit()








