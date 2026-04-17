"""
数据加载工具
1.从YAML文件加载测试数据
2.支持数据验证
3.路径处理
"""
import yaml
import os
from typing import Dict, List, Any

class DataLoader:
    """测试数据加载器"""

    @staticmethod   # 静态方法，不依赖类
    def get_project_root():
        """获取项目根目录"""
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @classmethod    # 类方法
    def load_yaml(cls, relative_path: str) -> Dict[str, Any]:   # ->表示数据返回值类型
        """
        加载YAML文件
        :param relative_path: 相对于项目根目录的路径
        :return: 解析后的YAML数据
        """
        project_root = cls.get_project_root()
        file_path = os.path.join(project_root, relative_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML文件不存在：{file_path}")

        try:
            # with开启上下文管理，离开with块，文件自动关闭，即使中间报错也会关闭；as file将文件对象赋值给变量file
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)  # 将 YAML 格式的文本 转换为 Python 字典/列表
        except yaml.YAMLError as e:
            raise Exception(f"YAML解析错误：{str(e)}")
        except Exception as e:
            raise Exception(f"文件读取错误：{str(e)}")

    @classmethod
    def get_test_users(cls) -> List[Dict[str, Any]]:
        """获取测试用户数据"""
        data = cls.load_yaml("test_data/users.yaml")
        if "test_users" not in data:
            raise KeyError("YAML文件中缺少'test_users'键")
        return data["test_users"]

    @classmethod
    def get_valid_users(cls) -> List[Dict[str, Any]]:
        """获取有效的测试用户(excepcted: true)"""
        users = cls.get_test_users()
        return [user for user in users if user.get("expected", False)]
    """
              #  ↑        ↑        ↑           ↑
              #  结果   遍历变量    数据源      过滤条件
        1. for user in users	遍历 users 列表中的每个用户字典
        2. if user.get("expected", False)	过滤条件：只保留 expected 为 True 的用户
        3. user	满足条件的元素，加入结果列表
        4. False	默认值，如果键不存在则返回 False
    """

    @classmethod
    def get_invalid_users(cls) -> List[Dict[str, Any]]:
        """获取无效的测试用户(excepcted: false)"""
        users = cls.get_test_users()
        return [user for user in users if user.get("expected", True)]


# 使用示例
if __name__ == "__main__":
    # 加载测试用户数据
    users = DataLoader.get_test_users()

    print("所有测试用户:")
    for user in users:
        print(f"用户名: {user['username']}, 期望结果: {user['expected']}")

    # 获取有效用户
    valid_users = DataLoader.get_valid_users()
    print(f"\n有效用户数量: {len(valid_users)}")

    # 获取无效用户
    invalid_users = DataLoader.get_invalid_users()
    print(f"无效用户数量: {len(invalid_users)}")







