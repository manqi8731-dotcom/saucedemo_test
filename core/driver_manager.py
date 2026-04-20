"""
Chrome 147+ 专用驱动管理器
使用手动下载的 ChromeDriver
"""
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import subprocess
import re


def get_chrome_version():
    """获取 Chrome 版本号"""
    try:
        # Windows Chrome 版本检测
        result = subprocess.run([
            'reg', 'query',
            'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon',
            '/v', 'version'
        ], capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            version_match = re.search(r'version\s+REG_SZ\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
            if version_match:
                return version_match.group(1)
    except:
        pass
    return "147.0.7727.101"


class DriverManager:
    """Chrome 147+ 专用驱动管理器"""

    def __init__(self, browser="chrome", headless=False):
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None

        # 检查 ChromeDriver 是否存在
        self.chromedriver_path = self._find_chromedriver()
        if not self.chromedriver_path:
            raise FileNotFoundError(
                "❌ 未找到 ChromeDriver！请下载 ChromeDriver 147.0.7727.101 "
                "并放置在 D:\\chromedriver\\ 目录下"
            )

    def _find_chromedriver(self):
        """查找 ChromeDriver 路径"""
        possible_paths = [
            r"D:\chromedriver\chromedriver.exe",
            r"D:\chromedriver\chromedriver-win64\chromedriver.exe",
            r"C:\chromedriver\chromedriver.exe",
            os.path.join(os.path.dirname(__file__), "chromedriver.exe")
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ 找到 ChromeDriver: {path}")
                return path

        print("❌ 未找到 ChromeDriver，请按以下步骤操作：")
        print("1. 访问: https://googlechromelabs.github.io/chrome-for-testing/")
        print("2. 搜索版本: 147.0.7727.101")
        print("3. 下载: ChromeDriver - Win64")
        print("4. 解压到: D:\\chromedriver\\chromedriver.exe")
        return None

    def get_driver(self):
        """获取浏览器驱动实例"""
        if self.driver is None:
            if self.browser == "chrome":
                self.driver = self._setup_chrome()
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser}")

        self.driver.maximize_window()
        return self.driver

    def _setup_chrome(self):
        """配置 Chrome 浏览器 - Chrome 147+ 专用"""
        # 创建服务对象，指定 ChromeDriver 路径
        service = Service(self.chromedriver_path)

        options = Options()

        # 基础配置
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        # Chrome 147+ 专用配置
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")

        # 解决新版本 Chrome 特有问题
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--enable-features=NetworkServiceInProcess")
        options.add_argument("--disable-features=VizDisplayCompositor")

        # 禁用密码管理
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)

        # 彻底禁用密码管理、密码泄露检测、安全浏览密码警告等所有相关功能
        options.add_argument(
            "--disable-features="
            "PasswordLeakDetection,"
            "SafeBrowsingPasswordCheck,"
            "PasswordProtectionWarningTrigger,"
            "PasswordCheck,"
            "ChromePasswordManagerCheckup,"
            "SafetyCheck,"
            "PasswordImport,"
            "PasswordEditing,"
            "PasswordManagerOnboarding"
        )
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-password-manager-reauthentication")

        # 禁用密码泄露检测和安全浏览相关功能
        options.add_argument(
            "--disable-features=PasswordImport,PasswordLeakDetection,ChromePasswordManagerCheckup,SafetyCheck")
        options.add_argument("--disable-save-password-bubble")

        # 用户代理
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{get_chrome_version()} Safari/537.36"
        options.add_argument(f"--user-agent={user_agent}")

        # # 临时目录
        # temp_dir = os.path.join(os.getenv('TEMP'), f'selenium_{os.getpid()}')
        # os.makedirs(temp_dir, exist_ok=True)
        # options.add_argument(f"--user-data-dir={temp_dir}")

        # 使用固定的用户数据目录（项目根目录下的 chrome_profile）
        profile_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chrome_profile")
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={profile_dir}")

        try:
            # 使用手动指定的 ChromeDriver 启动
            driver = webdriver.Chrome(service=service, options=options)

            # 隐藏 webdriver 特征
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                delete navigator.__proto__.webdriver;
            """)

            return driver

        except Exception as e:
            print(f"❌ Chrome 启动失败: {e}")
            print("💡 提示：可能需要以管理员身份运行 PyCharm")
            raise e

    def quit(self):
        """关闭浏览器驱动"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None


def test_driver():
    """测试驱动是否正常工作"""
    print(f"🚀 正在测试 ChromeDriver (Chrome {get_chrome_version()})")

    try:
        manager = DriverManager(browser="chrome", headless=False)
        driver = manager.get_driver()

        print("✅ Chrome 启动成功！")

        # 测试访问
        driver.get("https://www.google.com")
        print(f"✅ Google 访问成功！标题: {driver.title[:50]}...")

        driver.get("https://www.saucedemo.com")
        print(f"✅ SauceDemo 访问成功！标题: {driver.title}")

        print("🎉 驱动测试完全成功！")
        manager.quit()
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n💡 建议解决方案：")
        print("1. 以管理员身份运行 PyCharm")
        print("2. 确保 ChromeDriver 版本与 Chrome 版本完全匹配")
        print("3. 检查防火墙设置")
        return False


if __name__ == "__main__":
    success = test_driver()
    if success:
        print("\n🎉 所有测试通过！可以继续开发。")
    else:
        print("\n❌ 请按照提示解决问题后再试。")


