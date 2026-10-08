"""
MolTraX

一个面向分子结构差异分析的 Python 框架，提供从分子式比较、SMILES 结构比对
到批量处理的多层次分析能力。

注意：
    本仓库发布的是框架代码。核心算法模块以接口形式声明，具体实现未包含。
    详见 README.md 的"模块说明"部分。

快速使用：
    >>> import moltrax
    >>> moltrax.hello()
"""
from moltrax.config import PMD_DB_PATH, MAX_ANCHOR_POINTS

__version__ = "0.1.0"
__author__ = "MolTraX Project Maintainers"
__all__ = ["PMD_DB_PATH", "MAX_ANCHOR_POINTS", "hello", "show_info"]


def hello():
    """打印欢迎信息，用于验证包是否安装成功"""
    print("MolTraX")
    print(f"版本: {__version__}")
    print(f"示例数据库路径: {PMD_DB_PATH}")
    print()
    print("注意：本仓库为框架代码，核心算法模块未开源。")
    print("详见 README.md 的'模块说明'部分。")


def show_info():
    """显示项目信息与模块可用性"""
    print("=" * 60)
    print("MolTraX")
    print("=" * 60)
    print(f"版本: {__version__}")
    print(f"作者: {__author__}")
    print()

    print("模块可用性检查:")
    _check_module("moltrax.core.analysis_engine", "核心分析引擎")
    _check_module("moltrax.utils.mcs_calculator", "MCS 计算")
    _check_module("moltrax.utils.formula_parser", "分子式解析")
    _check_module("moltrax.services.diff_analyzer", "差分分析")
    _check_module("moltrax.models.pmd_manager", "规则匹配引擎")
    print()

    try:
        from moltrax.services.validator import validate_results
        print("✅ 验证服务: 可用")
    except ImportError:
        print("⚠️ 验证服务: 部分功能降级")

    print()
    print("示例数据库:", PMD_DB_PATH)
    print("=" * 60)


def _check_module(module_path: str, display_name: str):
    """检查模块是否可用"""
    try:
        __import__(module_path)
        print(f"✅ {display_name}: 可用")
    except ImportError:
        print(f"🔒 {display_name}: 未开源（接口层）")
