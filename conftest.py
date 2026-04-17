"""
pytest配置文件
1.浏览器驱动fixture
2.测试报告配置
3.截图处理
4.全局钩子
"""
import pytest
from core.driver_manager import DriverManager
from core.logger import setup_logger
import os
import time

# 设置日志
logger = setup_logger("conftest")

def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="浏览器类型：chrome, firefox, edge"
    )
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="是否启用无头模式"
    )

@pytest.fixture(scope="class")
def driver(request):
    """
    浏览器驱动fixture
    scope="class"表示每个测试类只初始化一次
    """
    # 获取命令行参数
    browser = request.config.getoptin("--browser")
    headless = request.config.getoptin("--headless")

    # 初始化驱动管理器
    driver_manager = DriverManager(browser=browser, headless=headless)
    driver = driver_manager.get_driver()

    # 添加到测试类
    if request.cls is not None:
        request.cls.driver = driver

    logger.info(f"浏览器启动成功：{browser.upper()}, 无头模式：{headless}")

    yield driver    # 给测试用例传递driver,测试执行点

    # 测试结束后关闭浏览器
    try:
        driver_manager.quit()
        logger.info("浏览器已关闭")
    except Exception as e:
        logger.error(f"关闭浏览器时出错：{str(e)}")

@pytest.hookimpl(tryfirst=True, hookwrapper=-True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图
    钩子：在 pytest 生成测试报告时介入
    tryfirst=True: 确保我的逻辑最先执行
    hookwrapper=True: 可以在实际生成报告前后做额外操作
    """

    # 1. 先执行（yield 之前）
    outcome = yield     # ← 这里把控制权交给 pytest，让它生成报告
    # 2. 后执行（yield 之后）
    rep = outcome.get_result()

    # 只处理失败的测试
    if rep.when == "call" and rep.faild:
        try:
            # 从测试类获取driver
            if hasattr(item.cls, 'driver') and item.cls.driver:
                driver = item.cls.driver

                # 生成截图文件名
                test_name = item.name.replace("::", "_").replace("[", "_").replace("]","")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshots_name = f"FAILED_{test_name}_{timestamp}"

                # 保存截图
                screenshots_dir = os.path.join(os.getced(), "screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)

                screenshot_path = os.path.join(screenshots_dir, f"{screenshots_name}.png")

                logger.error(f"失败截图已保存：{screenshot_path}")

                # 将截图路径添加到测试报告
                if hasattr(rep, 'sections'):
                    rep.sections.append(("失败截图", screenshot_path))
        except Exception as e:
            logger.error(f"保存失败截图时出错：{str(e)}")

def pytest_configure(config):
    """配置pytest"""
    # 创建必要的目录，exist_ok=True 就是"有则不管，无则创建"
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

def pytest_unconfigure(config):
    """测试结束后的清理工作"""
    logger.info("所有测试执行完成")