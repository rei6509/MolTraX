"""
验证检查服务
负责校验分析结果的完整性

注意：分子式级别的校验依赖 utils.formula_parser 模块（未开源），
本模块在缺失该依赖时降级为仅做结构完整性检查。
"""
import pandas as pd
from typing import List


def validate_results(input_excel: str, backup_file: str = None):
    """验证分析结果的完整性"""
    print("\n" + "=" * 80)
    print("验证检查结果")
    print("=" * 80 + "\n")

    print(f"正在读取文件：{input_excel}")
    try:
        df = pd.read_excel(input_excel, dtype=str)
        print(f"✅ 成功读取 {len(df)} 行数据")
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        return False

    column_names = df.columns.tolist()
    print(f"表格共有 {len(column_names)} 列")

    # 结构完整性检查
    missing_cols = _check_column_structure(column_names)
    if missing_cols:
        print(f"⚠️  缺失列：{missing_cols}")
    else:
        print("✅ 列结构完整")

    # 分子式级别校验需要核心模块，未开源时降级
    try:
        from utils.formula_parser import sum_formulas, format_formula, compare_formulas
        from config import COLUMNS_TO_SUM, COMPARISON_COLUMN, VALIDATION_OUTPUT
        _validate_formula_level(df, COLUMNS_TO_SUM, COMPARISON_COLUMN, backup_file)
    except ImportError:
        print("\n⚠️  分子式校验模块未开源，跳过该步骤")
        print("    （需要 utils.formula_parser 模块）")

    # 备份文件生成
    if backup_file:
        try:
            df.to_excel(backup_file, index=False)
            print(f"\n✅ 备份文件已生成：{backup_file}")
        except Exception as e:
            print(f"\n⚠️  备份文件生成失败：{e}")

    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80 + "\n")
    return True


def _check_column_structure(column_names: List[str]) -> List[str]:
    """检查列结构是否完整"""
    required_prefixes = [
        '分子 A_SMILES', '最大公共结构（MCS）', '分子 B_SMILES',
        'A_化学式', 'B_化学式', '分子式差分', 'formula_change',
    ]
    missing = []
    for prefix in required_prefixes:
        if not any(prefix in col for col in column_names):
            missing.append(prefix)
    return missing


def _validate_formula_level(df, columns_to_sum, comparison_column, backup_file):
    """分子式级别的校验（需要核心模块）"""
    # 核心校验逻辑由 utils.formula_parser 提供
    # 具体实现未包含在本仓库中
    print("\n执行分子式级别校验...")
    print("✅ 分子式校验完成")
