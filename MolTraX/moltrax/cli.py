"""
moltrax 命令行入口

用法:
    python -m moltrax.cli info          # 显示项目信息与模块可用性
    python -m moltrax.cli build-sample  # 生成示例数据库
    python -m moltrax.cli build-template  # 生成批量上传模板
    python -m moltrax.cli validate <file>  # 验证结果文件
    python -m moltrax.cli analyze <file>  # 批量分析（需要核心模块）
"""
import sys
import os
from datetime import datetime


def cmd_info():
    """显示项目信息与模块可用性"""
    from moltrax import show_info
    show_info()


def cmd_build_sample():
    """生成示例数据库"""
    from moltrax.config import BASE_DIR
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.build_sample_db import build_sample_db
    build_sample_db()


def cmd_build_template():
    """生成批量上传模板"""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.build_template import build_template
    build_template()


def cmd_validate(input_file: str):
    """验证结果文件"""
    try:
        from moltrax.services.validator import validate_results
    except ImportError as e:
        print(f"❌ 验证服务不可用: {e}")
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)

    validate_results(input_file)


def cmd_analyze(input_file: str):
    """批量分析（需要核心模块）"""
    try:
        from moltrax.core.analysis_engine import StructureAnalysisEngine
        from moltrax.config import PMD_DB_PATH
    except ImportError as e:
        print("\n" + "=" * 60)
        print("⚠️  核心算法模块未开源")
        print("=" * 60)
        print(f"缺失模块: {e.name if hasattr(e, 'name') else str(e)}")
        print()
        print("本仓库仅发布框架代码，核心分析引擎未包含。")
        print("如需完整版本，请联系项目维护者。")
        print("=" * 60)
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)

    input_dir = os.path.dirname(os.path.abspath(input_file))
    input_filename = os.path.basename(input_file)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_path = os.path.join(input_dir, f"{name_without_ext}计算结果.xlsx")

    print(f"\n{'=' * 60}")
    print("moltrax - 批量分析")
    print(f"{'=' * 60}")
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_path}")

    engine = StructureAnalysisEngine(input_file, output_path, PMD_DB_PATH)
    result_excel = engine.main_structure_analysis()

    if result_excel:
        print(f"\n✅ 分析完成！输出文件：{result_excel}")
    else:
        print("\n❌ 分析失败，请检查日志")

    print(f"\n{'=' * 60}")
    print("完成")
    print(f"{'=' * 60}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "info":
        cmd_info()
    elif cmd == "build-sample":
        cmd_build_sample()
    elif cmd == "build-template":
        cmd_build_template()
    elif cmd == "validate":
        if len(sys.argv) < 3:
            print("用法: python -m moltrax.cli validate <file>")
            sys.exit(1)
        cmd_validate(sys.argv[2])
    elif cmd == "analyze":
        if len(sys.argv) < 3:
            print("用法: python -m moltrax.cli analyze <file>")
            sys.exit(1)
        cmd_analyze(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
