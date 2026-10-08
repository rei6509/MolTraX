"""
示例数据库构建脚本

生成 data/sample_rules.db，包含 5 条虚构的示例规则。
真实规则库未随本仓库发布。

用法：
    python scripts/build_sample_db.py
"""
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DB = os.path.join(BASE_DIR, "data", "sample_rules.db")


def build_sample_db(output_path: str = OUTPUT_DB):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        os.remove(output_path)

    conn = sqlite3.connect(output_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE pmd_rules (
            pmd_id          TEXT,
            pmd_value       TEXT,
            formula_change  TEXT,
            reaction        TEXT,
            description     TEXT,
            source          TEXT,
            heavy_atom_count TEXT,
            bond_tolerance  TEXT,
            formula_change1 TEXT,
            中文描述        TEXT
        )
    """)

    # 5 条虚构示例规则（非真实数据，仅用于演示框架流程）
    sample_rules = [
        ('PMD-DEMO-001', '14.0156',  '+C1H2',   '', 'methylation',          'sample', None, None, "'+C1H2",   '甲基化（示例）'),
        ('PMD-DEMO-002', '-14.0156', '-C1H2',   '', 'demethylation',        'sample', None, None, "'-C1H2",   '去甲基化（示例）'),
        ('PMD-DEMO-003', '15.9949',  '+O1',     '', 'hydroxylation',        'sample', None, None, "'+O1",     '羟基化（示例）'),
        ('PMD-DEMO-004', '-15.9949', '-O1',     '', 'dehydration',          'sample', None, None, "'-O1",     '脱水（示例）'),
        ('PMD-DEMO-005', '42.0105',  '+C2H2O1', '', 'acetylation',          'sample', None, None, "'+C2H2O1", '乙酰化（示例）'),
    ]

    cur.executemany("""
        INSERT INTO pmd_rules
        (pmd_id, pmd_value, formula_change, reaction, description,
         source, heavy_atom_count, bond_tolerance, formula_change1, 中文描述)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_rules)

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM pmd_rules")
    count = cur.fetchone()[0]
    conn.close()

    print(f"✅ 示例数据库已生成：{output_path}")
    print(f"   包含 {count} 条示例规则")
    print(f"   注意：此为虚构示例数据，非真实规则库。")


if __name__ == "__main__":
    build_sample_db()
