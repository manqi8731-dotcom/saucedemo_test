# SauceDemo UI 自动化测试项目

本项目是一款基于 **Python + Selenium + Pytest** 构建的 Web UI 自动化测试框架。项目针对典型的电商练习网站 [SauceDemo](https://www.saucedemo.com) 进行了核心业务流的测试覆盖。

## 一、项目亮点

1. **POM (Page Object Model) 设计模式**：高度解耦。将页面元素定位与测试逻辑分离，当 UI 发生变化时，只需修改对应的 Page 类，无需变动测试脚本。
2. **工程化底层封装**：
    * **BasePage**: 对 Selenium 原生方法进行二次封装，集成显示等待（WebDriverWait）、平滑滚动、JS 注入处理等功能。
    * **DriverManager**: 具备自动检测本地 Chrome 版本能力，支持命令行动态切换
    * **Headless（无头模式）** 以及防爬虫规避配置。
3. **数据驱动测试 (DDT)**：利用 `PyYAML` 加载 `test_data/users.yaml` 中的多账号数据，实现一套代码验证标准用户、锁定用户、问题用户等多种场景。
4. **高可用的报告集成**：
    * **Allure Report**: 自动生成结构化的测试报告。
    * **失败自动截图**: 在 `conftest.py` 中利用 Pytest 钩子函数，在用例断言失败时自动捕获屏幕并嵌入 Allure 报告中。
5. **彩色日志系统**: 集成 `colorlog`，支持控制台彩色输出并同步保存至本地 `logs/` 目录，便于快速定位执行过程。

## 二、技术栈

1. **测试框架**: Pytest
2. **浏览器自动化**: Selenium 4.21.0
3. **报告工具**: Allure + allure-pytest
4. **数据管理**: PyYAML
5. **日志系统**: logging + colorlog

## 三、项目结构

```text
saucedemo_test/
├── core/                   # 框架核心底层
│   ├── base_page.py        # 页面操作基类
│   ├── driver_manager.py   # 浏览器驱动生命周期管理
│   └── logger.py           # 彩色日志配置
├── pages/                  # 页面对象模型 (POM)
│   ├── login_page.py       # 登录页
│   ├── inventory_page.py   # 商品列表页
│   ├── cart_page.py        # 购物车页
│   └── checkout_page.py    # 结算信息页
├── test_cases/             # 测试脚本
│   ├── test_login.py       # 登录模块用例
│   ├── test_cart.py        # 购物车模块用例
│   └── test_checkout.py    # 结账流程模块用例
├── test_data/              # 数据中心
│   └── users.yaml          # YAML 数据源
├── utils/                  # 工具类
│   └── data_loader.py      # YAML 数据转换器
├── conftest.py             # Pytest 插件与全局 Fixture (含截图钩子)
├── requirements.txt        # 依赖包列表
└── .gitignore              # Git 忽略配置
```

## 四、快速开始

1. **环境准备**：确保已安装 Python 3.8+ 且本地安装有 Chrome 浏览器。
2. **安装依赖**：
```bash
pip install -r requirements.txt
```
3. **运行测试**：运行所有测试并生成Allure结果：
```bash
pytest --alluredir=./allure-results
```
4. **查看测试报告**：
```bash
allure serve ./allure-results
```

## 五、测试覆盖场景

1. **用户登录功能**：
   * 标准用户登录流程验证。
   * 基于数据驱动的异常登录（锁定用户、错误密码等）验证。
2. **购物车管理共功能**：
   * 商品添加/移除操作及购物车数量同步更新验证。
   * 跨页面（商品页与购物车页）状态保持验证。
3. **结账流程功能**：
   * 配送信息必填项校验。
   * 商品总额、税率及最终金额的计算逻辑验证。
   * 完成下单流程及成功页面状态验证。

## 六、报告展示
