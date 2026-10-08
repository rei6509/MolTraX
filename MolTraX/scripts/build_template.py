"""
批量上传模板生成脚本

生成 data/batch_template.xlsx，包含批量比较所需的输入列。

用法：
    python scripts/build_template.py
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(BASE_DIR, "data", "batch_template.xlsx")


def build_template(output_path: str = OUTPUT):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(columns=[
        '分子 A_SMILES',
        '分子 B_SMILES',
    ])

    # 填入两行示例 SMILES（仅用于展示格式，非真实分析对象）
    df.loc[0] = ['CCO', 'CC']
    df.loc[1] = ['c1ccccc1', 'c1ccccc1O']

    df.to_excel(output_path, index=False)
    print(f"✅ 批量上传模板已生成：{output_path}")


if __name__ == "__main__":
    build_template()
