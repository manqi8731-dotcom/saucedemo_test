"""
日志配置模块
1.统一的日志格式
2.文件和控制台输出
3.按日志级别着色
"""
import logging
import os
from datetime import datetime
import colorlog

def setup_logger(name:str = "selenium_framework") -> logging.Logger:
    """
    配置并返回日志记录器
    :param name: 日志记录器名称
    :return: 配置好的Logger实例
    """
    # 创建logs目录
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重复添加handler
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建文件handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # 创建控制台handler(带颜色)
    console_handler = logging.StreamHandler()
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)

    # 添加 handler
    logger.addHandler(file_handler)         # 文件处理器：日志写入文件
    logger.addHandler(console_handler)      # 控制台处理器：日志打印到屏幕

    return logger

# 使用示例
if __name__ == "__main__":
    logger = setup_logger("test_logger")

    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")

















