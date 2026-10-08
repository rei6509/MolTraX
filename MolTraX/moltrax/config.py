"""
配置文件 - 常量与路径定义
"""
import os

# 包目录（moltrax/）
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目根目录（moltrax/ 的上级）
BASE_DIR = os.path.dirname(PACKAGE_DIR)

# 示例数据库路径（仓库仅提供示例数据，完整规则库未发布）
# 查找顺序：项目根 data/ → 包内 data/
_data_candidates = [
    os.path.join(BASE_DIR, "data", "sample_rules.db"),
    os.path.join(PACKAGE_DIR, "data", "sample_rules.db"),
]
PMD_DB_PATH = next((p for p in _data_candidates if os.path.exists(p)), _data_candidates[0])

# 批量处理默认输入输出路径（用户运行时指定）
INPUT_EXCEL = os.path.join(BASE_DIR, "data", "batch_template.xlsx")
OUTPUT_EXCEL = os.path.join(BASE_DIR, "data", "output.xlsx")
VALIDATION_OUTPUT = os.path.join(BASE_DIR, "data", "output_backup.xlsx")

# 列索引配置
COLUMNS_TO_SUM = [23, 28, 33, 38, 43]
COMPARISON_COLUMN = 7
MAX_ANCHOR_POINTS = 5

# 化学元素顺序
ELEMENTS_ORDER = ['C', 'H', 'O', 'N', 'S', 'P', 'F', 'Cl', 'Br', 'I']

# MCS 计算参数
MCS_THRESHOLD = 0.95
MCS_MAX_ITERATIONS = 3

# 输出列名模板
BASE_COLUMNS = [
    '分子 A_SMILES',
    '最大公共结构（MCS）',
    '分子 B_SMILES',
    'A_化学式',
    'B_化学式',
    '分子式差分 (Δ)',
    'formula_change',
    'formula_con',
    '分子量差',
    'reaction_old',
    'reaction_old_中文描述',
    'description_old',
    'reaction_new',
    'reaction_new_中文描述',
    'description_new',
    'A_diff',
    'B_diff',
    '位点个数',
    'A_diff_化学式',
    'B_diff_化学式',
    'A_diff_anchor_pos',
    'B_diff_anchor_pos'
]


def get_endpoint_columns(endpoint_num):
    """获取指定位点的列名"""
    return [
        f'位点{endpoint_num}_结构变化',
        f'位点{endpoint_num}_化学式变化',
        f'位点{endpoint_num}_严格分子式差分',
        f'位点{endpoint_num}_PMD 描述',
        f'位点{endpoint_num}_PMD 描述_中文描述',
        f'位点{endpoint_num}_PMD 反应'
    ]
