"""统一的 YAML 测试数据加载器，供各测试文件 parametrize 使用。"""

from pathlib import Path
import yaml

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_cases(filename: str, key: str) -> list[dict]:
    """
    读取 data/{filename} 中 key 对应的用例列表。
    用法：load_cases("product_cases.yaml", "get_by_id")
    """
    path = _DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data[key]
