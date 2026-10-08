# MolTraX

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Display-Only](https://img.shields.io/badge/license-Display--Only-red.svg)](./LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-black.svg)](https://github.com/REI6509/MolTraX)

MolTraX 是一个面向分子结构差异分析的 Python 框架，提供从分子式比较、SMILES 结构比对到批量处理的多层次分析能力。框架以 pandas 为数据处理基础，结合 RDKit 化学信息学生态，为代谢转化研究、结构活性关系分析等场景提供基础设施支持。

> **说明**：本仓库发布的是框架代码。核心算法模块（结构差异计算引擎、规则匹配引擎等）以接口形式声明，具体实现未包含在仓库中。详见 [模块说明](#模块说明)。

---

## 目录

- [背景与动机](#背景与动机)
- [主要特性](#主要特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [命令行工具](#命令行工具)
- [编程接口](#编程接口)
- [架构概览](#架构概览)
- [模块说明](#模块说明)
- [数据说明](#数据说明)
- [常见问题](#常见问题)
- [许可证](#许可证)
- [引用](#引用)

---

## 背景与动机

理解化合物在不同反应条件下的转化行为及其连续演化过程，是环境化学、代谢组学和药物化学等领域的重要研究基础。准确预测化合物的转化行为，有助于揭示分子归趋、识别未知转化产物，并评估其潜在环境或生物风险。
本框架面向化合物转化过程的预测与解析，构建人工智能驱动的分析方法，主要整合：
- 母体化合物的结构特征
- 潜在反应活性位点
- 已知转化模式与反应规律
- 分子结构、反应过程与生成产物之间的关联信息
通过学习“结构—位点—反应—产物”之间的内在关系，框架能够预测潜在转化反应及其对应的转化产物。
在此基础上，框架进一步结合多步反应推演与路径关联，构建母体化合物向下游产物连续演化的候选转化网络，并综合以下信息对关键连续转化路径进行优先排序：
- 结构差异合理性
- 位点反应倾向
- 路径连续性
该框架可为未知转化产物筛查、环境归趋解析、代谢物鉴定及风险导向的化合物评估提供智能化、可扩展的方法基础。
架构设计
本框架遵循两项核心设计原则：分层解耦与接口开放。
命令行层、服务层和核心算法层相互独立，并通过清晰定义的接口契约进行连接。该模块化架构支持研究人员和开发者在不改动整体系统的前提下，对任意层级的组件进行替换、扩展或定制。

---

## 主要特性

- **多模式分析**
  - 分子式与精确质量比较：支持分子式输入与质量输入两种模式，自动识别并匹配规则库
  - SMILES 结构比较：基于 RDKit 进行分子结构标准化与比对，输出位点级别的差异信息
  - 批量比较：支持 Excel 批量输入，命令行或编程方式处理

- **可扩展架构**
  - 配置与代码分离，列名模板、路径、阈值均可在 `config.py` 中调整
  - 模块间通过接口契约通信，核心算法层可独立替换
  - 支持动态位点列生成，最大位点数可配置

- **数据管理**
  - 基于 SQLite 的规则数据库，支持按质量差与分子式差分双路径匹配
  - 提供数据库构建脚本，可从 Excel 源数据生成规则库
  - 批量处理结果与验证备份自动分离

- **命令行与编程双模式**
  - 提供 `moltrax` 命令行工具，支持常用操作
  - 可作为 Python 包导入，在自有代码中集成

---

## 安装

MolTraX 仅通过 GitHub 发布，不发布到 PyPI。请从源码安装：

```bash
# 克隆仓库
git clone https://github.com/REI6509/MolTraX.git
cd MolTraX

# 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装
pip install -e .
```

### 可选依赖

核心算法模块依赖 RDKit，由于核心模块未随本仓库发布，RDKit 默认不安装。如需自行实现核心模块，请安装可选依赖：

```bash
pip install -e .[chem]
```

---

## 快速开始

### 1. 验证安装

```bash
# 命令行方式
moltrax info

# 或 Python 方式
python -c "import moltrax; moltrax.hello()"
```

### 2. 生成示例数据

```bash
moltrax build-sample
moltrax build-template
```

### 3. 运行示例

```bash
# 克隆仓库后，运行示例脚本
python examples/quickstart.py
```

### 4. 编程使用

```python
import moltrax

# 显示项目信息与模块可用性
moltrax.show_info()

# 读取配置
from moltrax.config import PMD_DB_PATH, MAX_ANCHOR_POINTS
print(f"示例数据库: {PMD_DB_PATH}")
print(f"最大位点数: {MAX_ANCHOR_POINTS}")
```

---

## 命令行工具

安装后提供 `moltrax` 命令：

```bash
# 显示项目信息与模块可用性
moltrax info

# 生成示例数据库（5 条虚构规则）
moltrax build-sample

# 生成批量上传模板
moltrax build-template

# 验证结果文件的结构完整性
moltrax validate <结果文件.xlsx>

# 批量分析（需要核心模块，未开源时给出提示）
moltrax analyze <输入文件.xlsx>
```

---

## 编程接口

### 配置访问

```python
from moltrax.config import (
    PMD_DB_PATH,
    MAX_ANCHOR_POINTS,
    BASE_COLUMNS,
    get_endpoint_columns,
    ELEMENTS_ORDER,
)

# 示例数据库路径
print(PMD_DB_PATH)

# 动态生成位点列名
columns = get_endpoint_columns(1)
# ['位点1_结构变化', '位点1_化学式变化', '位点1_严格分子式差分', ...]
```

### 验证服务

验证服务是开源的通用模块，可独立使用：

```python
from moltrax.services.validator import validate_results

# 验证结果文件的列结构完整性
validate_results("你的结果文件.xlsx")

# 验证并生成备份
validate_results("你的结果文件.xlsx", backup_file="backup.xlsx")
```

### 核心模块接口（未开源）

核心模块以接口形式声明，具体实现未包含。以下是接口约定，可参照自行实现：

```python
# moltrax.models.pmd_manager
class PMDRuleManager:
    MASS_TOLERANCE = 0.1  # 质量匹配容差（Da）

    def __init__(self, db_path: str): ...
    def query_by_mass_difference(self, mass_diff: float) -> dict: ...
    def query_by_formula_con(self, formula_con: str) -> dict: ...
    def query_by_formula_change(self, formula_change: str) -> dict: ...

# moltrax.core.analysis_engine
class StructureAnalysisEngine:
    def __init__(self, input_excel: str, output_excel: str, pmd_db_path: str): ...
    def main_structure_analysis(self) -> str: ...

# moltrax.utils.mcs_calculator
def standardize_smiles(smiles: str) -> str: ...
def get_exact_mass(smiles: str) -> float: ...
def get_mcs_with_valence_validation(smiles_a: str, smiles_b: str) -> str: ...

# moltrax.utils.formula_parser
def calculate_formula_change(formula_a: str, formula_b: str) -> str: ...
def calculate_formula_difference(formula_a: str, formula_b: str) -> dict: ...
def format_formula_diff(formula_diff: dict) -> str: ...
def process_formula_change_for_con(formula_change: str) -> str: ...

# moltrax.services.diff_analyzer
def process_diff_analysis(smiles_a: str, smiles_b: str, mcs_smiles: str) -> dict: ...
def analyze_anchor_points(*args, **kwargs) -> dict: ...
```

实现上述接口后，放入对应模块路径即可被框架自动识别并调用。

---

## 架构概览

```
MolTraX/
├── moltrax/                # 主包
│   ├── __init__.py            # 包入口，提供 hello() / show_info()
│   ├── cli.py                 # 命令行入口
│   ├── config.py              # 配置：路径、列名、阈值
│   ├── core/
│   │   └── __init__.py        # 核心引擎（接口层，未开源）
│   ├── services/
│   │   ├── __init__.py
│   │   └── validator.py       # 验证检查服务（开源）
│   ├── utils/
│   │   └── __init__.py        # 工具模块（接口层，未开源）
│   └── models/
│       └── __init__.py        # 数据模型（接口层，未开源）
├── data/
│   ├── sample_rules.db        # 示例规则数据库（5 条虚构规则）
│   └── batch_template.xlsx    # 批量上传模板
├── scripts/
│   ├── build_sample_db.py     # 示例数据库生成脚本
│   └── build_template.py      # 批量模板生成脚本
├── examples/
│   └── quickstart.py          # 快速入门示例
├── setup.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

### 分层设计

```
┌─────────────────────────────────────────┐
│      命令行 / 编程入口 (cli.py)          │
│         moltrax info / analyze / ...     │
└──────────────────┬──────────────────────┘
                   │ 接口调用
┌──────────────────▼──────────────────────┐
│          服务层 (services/)             │
│         validator / diff_analyzer       │
└──────────────────┬──────────────────────┘
                   │ 接口调用
┌──────────────────▼──────────────────────┐
│        核心算法层 (core/ + utils/)      │
│   analysis_engine / mcs_calculator      │
│   formula_parser                        │
└──────────────────┬──────────────────────┘
                   │ 数据访问
┌──────────────────▼──────────────────────┐
│        数据层 (models/ + data/)         │
│      pmd_manager / sample_rules.db      │
└─────────────────────────────────────────┘
```

---

## 模块说明

本仓库采用 **"框架开放、核心保留"** 的发布策略。以下标注各模块的开源状态：

| 模块 | 路径 | 状态 | 说明 |
|------|------|------|------|
| 包入口 | `moltrax/__init__.py` | ✅ 开源 | 版本信息、模块可用性检测 |
| 命令行 | `moltrax/cli.py` | ✅ 开源 | 命令行入口与子命令 |
| 配置 | `moltrax/config.py` | ✅ 开源 | 路径、列名模板、阈值常量 |
| 验证服务 | `moltrax/services/validator.py` | ✅ 开源 | 结果完整性检查（部分功能降级） |
| 示例数据脚本 | `scripts/` | ✅ 开源 | 示例数据库与模板生成 |
| 快速入门示例 | `examples/` | ✅ 开源 | 使用示例 |
| 核心分析引擎 | `moltrax/core/analysis_engine.py` | 🔒 接口层 | 结构差异分析引擎，实现未开源 |
| MCS 计算 | `moltrax/utils/mcs_calculator.py` | 🔒 接口层 | 最大公共子结构计算，实现未开源 |
| 分子式解析 | `moltrax/utils/formula_parser.py` | 🔒 接口层 | 分子式解析与差分，实现未开源 |
| 差分分析 | `moltrax/services/diff_analyzer.py` | 🔒 接口层 | 位点级差异分析，实现未开源 |
| 规则匹配引擎 | `moltrax/models/pmd_manager.py` | 🔒 接口层 | 规则数据库匹配，实现未开源 |

> 🔒 标记的模块在仓库中仅保留接口声明，具体实现代码未包含。框架在运行时会通过 `try/except` 检测这些模块的可用性，缺失时以明确提示替代功能调用。

---

## 数据说明

### 示例数据库

仓库提供 `data/sample_rules.db`，包含 5 条**虚构**的示例规则：

| pmd_id | formula_change | 中文描述 |
|--------|---------------|---------|
| PMD-DEMO-001 | +C1H2 | 甲基化（示例） |
| PMD-DEMO-002 | -C1H2 | 去甲基化（示例） |
| PMD-DEMO-003 | +O1 | 羟基化（示例） |
| PMD-DEMO-004 | -O1 | 脱水（示例） |
| PMD-DEMO-005 | +C2H2O1 | 乙酰化（示例） |

> 此数据仅用于演示框架的数据结构与查询流程，不代表真实规则库内容。

### 真实规则库

完整的规则数据库（包含数千条规则及其中文描述）为项目专有数据，**未随本仓库发布**。如需用于研究或商业用途，请联系项目维护者获取授权。

### 数据库表结构

```sql
CREATE TABLE pmd_rules (
    pmd_id           TEXT,    -- 规则编号
    pmd_value        TEXT,    -- 质量差值
    formula_change   TEXT,    -- 分子式变化
    reaction         TEXT,    -- 反应类型
    description      TEXT,    -- 英文描述
    source           TEXT,    -- 数据来源
    heavy_atom_count TEXT,    -- 重原子数
    bond_tolerance   TEXT,    -- 键容差
    formula_change1  TEXT,    -- 标准化分子式变化
    中文描述         TEXT     -- 中文描述
);
```

---

## 常见问题

**Q: 安装后如何验证安装成功？**

A: 运行 `moltrax info` 或 `python -c "import moltrax; moltrax.hello()"`，看到欢迎信息即表示安装成功。

**Q: 为什么 `moltrax analyze` 提示“核心算法模块未开源”？**

A: 这是预期行为。本仓库仅包含框架代码，核心算法模块未发布。如需完整功能，请联系维护者。

**Q: 可以用示例数据库进行真实分析吗？**

A: 示例数据库仅包含 5 条虚构规则，仅用于演示数据结构与查询流程，不适用于真实分析。

**Q: 如何自行实现核心模块？**

A: 参照 [编程接口](#编程接口) 部分的接口约定，实现对应的类与函数，放入 `moltrax/` 对应目录即可被框架自动识别。

**Q: 支持 Linux / macOS 吗？**

A: 框架基于纯 Python 与 pandas，理论上跨平台。但当前仅在 Windows 上测试通过。

**Q: 为什么 requirements.txt 中 RDKit 被注释掉了？**

A: RDKit 仅在核心算法模块中使用。由于核心模块未开源，安装 RDKit 对本仓库的框架代码并非必需。如需自行实现核心模块，请通过 `pip install -e .[chem]` 安装。

**Q: 为什么 PyPI 上搜不到 MolTraX？**

A: MolTraX 仅通过 GitHub 发布，不上架 PyPI。请通过 `git clone` 从源码安装，详见 [安装](#安装) 部分。

---

## 许可证

本项目采用 **Display-Only License（展示用许可证）**，详见 [LICENSE](./LICENSE)。

简要说明：

- ✅ 允许查看、学习本仓库代码
- ❌ 禁止商业使用
- ❌ 禁止创建衍生作品
- ❌ 禁止再分发
- ❌ 核心模块不可通过逆向工程获取

如需商业授权或获取完整版本，请联系项目维护者。

---

## 引用

如在研究或项目中使用 MolTraX，请按以下格式引用：

```bibtex
@misc{moltrax2026,
  title  = {MolTraX},
  author = {MolTraX Project Maintainers},
  year   = {2026},
  url    = {https://github.com/REI6509/MolTraX},
  note   = {框架代码开源，核心算法模块未开源}
}
```

---

## 致谢

MolTraX 的构建得益于以下开源项目的支持：

- [pandas](https://pandas.pydata.org/) — 数据处理与分析
- [RDKit](https://www.rdkit.org/) — 化学信息学工具包
- [openpyxl](https://openpyxl.readthedocs.io/) — Excel 读写

感谢所有为开源社区做出贡献的开发者。

---

## 联系方式

- 项目地址：[GitHub](https://github.com/REI6509/MolTraX)
- 问题反馈：[Issues](https://github.com/REI6509/MolTraX/issues)
- 商业授权：请联系项目维护者

---

*MolTraX © 2026*
