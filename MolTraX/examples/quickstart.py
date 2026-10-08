"""
moltrax 快速入门示例

本示例展示如何使用 moltrax 框架。由于核心算法模块未开源，
示例中的核心功能调用会以提示形式说明其行为。

运行方式：
    cd moltrax_release
    python examples/quickstart.py
"""
import sys
import os

# 将上级目录加入路径（仅用于未安装时直接运行示例）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import moltrax


def example_hello():
    """示例 1: 验证包安装"""
    print("\n>>> 示例 1: 验证包安装")
    print("-" * 50)
    moltrax.hello()


def example_show_info():
    """示例 2: 显示模块可用性"""
    print("\n>>> 示例 2: 显示模块可用性")
    print("-" * 50)
    moltrax.show_info()


def example_config():
    """示例 3: 读取配置"""
    print("\n>>> 示例 3: 读取配置")
    print("-" * 50)
    from moltrax.config import PMD_DB_PATH, MAX_ANCHOR_POINTS, BASE_COLUMNS

    print(f"示例数据库路径: {PMD_DB_PATH}")
    print(f"最大位点数: {MAX_ANCHOR_POINTS}")
    print(f"基础列名（前5个）: {BASE_COLUMNS[:5]}")


def example_query_rules():
    """示例 4: 查询示例规则库

    展示如何直接通过 SQLite 访问示例规则库。
    注意：真实的规则匹配引擎（models.pmd_manager）未开源，
    这里仅用原生 sqlite3 演示数据访问方式。
    """
    print("\n>>> 示例 4: 查询示例规则库")
    print("-" * 50)
    import sqlite3
    from moltrax.config import PMD_DB_PATH

    if not os.path.exists(PMD_DB_PATH):
        print(f"⚠️  示例数据库不存在: {PMD_DB_PATH}")
        print("    请先运行: python -m moltrax.cli build-sample")
        return

    conn = sqlite3.connect(PMD_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT pmd_id, formula_change, 中文描述 FROM pmd_rules")
    rows = cur.fetchall()

    print(f"示例规则库共 {len(rows)} 条规则:")
    for row in rows:
        print(f"  {row['pmd_id']}: {row['formula_change']} → {row['中文描述']}")

    conn.close()


def example_core_module_notice():
    """示例 5: 核心模块使用说明

    展示如何尝试导入核心模块，并处理未开源时的提示。
    """
    print("\n>>> 示例 5: 核心模块使用说明")
    print("-" * 50)
    print("尝试导入核心模块...\n")

    try:
        from moltrax.models.pmd_manager import PMDRuleManager
        print("✅ 规则匹配引擎已加载")
        print("   可以使用 PMDRuleManager.query_by_mass_difference() 等方法")
    except ImportError:
        print("🔒 规则匹配引擎未开源")
        print("   接口约定:")
        print("   - PMDRuleManager(db_path)")
        print("   - .query_by_mass_difference(mass_diff) -> dict")
        print("   - .query_by_formula_con(formula_con) -> dict")
        print("   - .query_by_formula_change(formula_change) -> dict")

    print()

    try:
        from moltrax.utils.mcs_calculator import standardize_smiles, get_exact_mass
        print("✅ MCS 计算模块已加载")
    except ImportError:
        print("🔒 MCS 计算模块未开源")
        print("   接口约定:")
        print("   - standardize_smiles(smiles) -> str")
        print("   - get_exact_mass(smiles) -> float")
        print("   - get_mcs_with_valence_validation(smiles_a, smiles_b) -> str")

    print()

    try:
        from moltrax.core.analysis_engine import StructureAnalysisEngine
        print("✅ 核心分析引擎已加载")
    except ImportError:
        print("🔒 核心分析引擎未开源")
        print("   接口约定:")
        print("   - StructureAnalysisEngine(input_excel, output_excel, pmd_db_path)")
        print("   - .main_structure_analysis() -> str  (输出文件路径)")


def example_validate():
    """示例 6: 验证服务

    验证服务（services/validator.py）是开源的通用模块，
    可独立使用做结果文件的结构完整性检查。
    """
    print("\n>>> 示例 6: 验证服务")
    print("-" * 50)
    from moltrax.services.validator import validate_results

    print("验证服务可用于检查结果文件的列结构完整性。")
    print("用法: validate_results(input_excel)")
    print()
    print("如需对示例数据做一次验证演示，可运行:")
    print("  python -m moltrax.cli validate <你的结果文件.xlsx>")


if __name__ == "__main__":
    print("=" * 60)
    print("moltrax 快速入门示例")
    print("=" * 60)

    example_hello()
    example_show_info()
    example_config()
    example_query_rules()
    example_core_module_notice()
    example_validate()

    print("\n" + "=" * 60)
    print("所有示例展示完毕")
    print("=" * 60)
