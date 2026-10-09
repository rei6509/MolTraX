MolTraX is a Python framework for molecular structure difference and transformation analysis, providing a multi-layered workflow from molecular formula comparison and SMILES-based structural alignment to rule-based transformation analysis and batch processing. Built on pandas and integrated with the RDKit cheminformatics ecosystem, MolTraX provides a flexible computational framework for environmental contaminant transformation analysis, metabolite identification, and structure–transformation relationship studies.

Developed by the Song Ninghui Research Group, Nanjing Institute of Environmental Sciences, Ministry of Ecology and Environment, China.

> **Note**: This repository publishes framework code only. Core algorithm modules (structure difference engine, rule matching engine, etc.) are declared as interfaces; their concrete implementations are not included. See [Module Overview](#module-overview).

---

## Table of Contents

- [Background & Motivation](#background--motivation)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command-Line Tool](#command-line-tool)
- [Programming Interface](#programming-interface)
- [Architecture Overview](#architecture-overview)
- [Module Overview](#module-overview)
- [Data Description](#data-description)
- [FAQ](#faq)
- [License](#license)
- [Citation](#citation)

---

## Background & Motivation

Understanding how compounds transform over time is fundamental to research in environmental chemistry, metabolomics, and medicinal chemistry. Accurate prediction of transformation behavior can help elucidate molecular fate, identify previously unknown transformation products, and assess potential environmental or biological risks.
This framework provides an AI-driven solution for predicting and interpreting compound transformation processes. It integrates:
- Structural features of parent compounds
- Potential reactive sites
- Known transformation patterns
- Relationships among structures, reactions, and products
By learning the underlying structure–site–reaction–product relationships, the framework predicts potential transformation reactions and their corresponding products.
It further combines multistep reaction inference with pathway linking to construct candidate transformation networks from parent compounds to downstream products. Key sequential pathways are prioritized by jointly evaluating:
- Structural plausibility
- Site-specific reactivity
- Pathway continuity
The framework provides an intelligent and extensible foundation for unknown transformation-product screening, environmental fate analysis, metabolite identification, and risk-oriented compound assessment.

### Architecture Design

The framework follows two core design principles: layered decoupling and interface openness.

The command-line layer, service layer, and core algorithm layer are independent of each other and connected through clearly defined interface contracts. This modular architecture allows researchers and developers to replace, extend, or customize components at any layer without modifying the overall system.

---

## Key Features

- **Multi-Mode Analysis**
  - Formula & exact mass comparison: supports both formula input and mass input modes, with automatic rule library matching
  - SMILES structural comparison: standardizes and aligns molecular structures based on RDKit, outputting site-level difference information
  - Batch comparison: supports Excel batch input via command-line or programmatic interfaces

- **Extensible Architecture**
  - Configuration and code separation; column name templates, paths, and thresholds are adjustable in `config.py`
  - Inter-module communication via interface contracts; the core algorithm layer can be independently replaced
  - Supports dynamic site column generation with configurable maximum site count

- **Data Management**
  - SQLite-based rule database with dual-path matching by mass difference and formula difference
  - Provides database construction scripts to generate rule libraries from Excel source data
  - Automatic separation of batch processing results and validation backups

- **Dual Command-Line & Programmatic Modes**
  - Provides the `moltrax` command-line tool for common operations
  - Importable as a Python package for integration into your own code

---

## Installation

MolTraX is distributed via GitHub only and is not published on PyPI. Install from source:

```bash
# Clone the repository
git clone https://github.com/REI6509/MolTraX.git
cd MolTraX

# Create a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install
pip install -e .
```

### Optional Dependencies

The core algorithm modules depend on RDKit. Since the core modules are not published with this repository, RDKit is not installed by default. To implement the core modules yourself, install the optional dependency:

```bash
pip install -e .[chem]
```

---

## Quick Start

### 1. Verify Installation

```bash
# Command-line
moltrax info

# Or via Python
python -c "import moltrax; moltrax.hello()"
```

### 2. Generate Sample Data

```bash
moltrax build-sample
moltrax build-template
```

### 3. Run the Examples

```bash
# After cloning the repository, run the example script
python examples/quickstart.py
```

### 4. Programmatic Usage

```python
import moltrax

# Display project info and module availability
moltrax.show_info()

# Read configuration
from moltrax.config import PMD_DB_PATH, MAX_ANCHOR_POINTS
print(f"Sample database: {PMD_DB_PATH}")
print(f"Maximum sites: {MAX_ANCHOR_POINTS}")
```

---

## Command-Line Tool

After installation, the `moltrax` command is available:

```bash
# Display project info and module availability
moltrax info

# Generate the sample database (5 fictional rules)
moltrax build-sample

# Generate the batch upload template
moltrax build-template

# Validate the structural integrity of a result file
moltrax validate <result_file.xlsx>

# Batch analysis (requires core modules; prompts if unavailable)
moltrax analyze <input_file.xlsx>
```

---

## Programming Interface

### Configuration Access

```python
from moltrax.config import (
    PMD_DB_PATH,
    MAX_ANCHOR_POINTS,
    BASE_COLUMNS,
    get_endpoint_columns,
    ELEMENTS_ORDER,
)

# Sample database path
print(PMD_DB_PATH)

# Dynamically generate site column names
columns = get_endpoint_columns(1)
# ['site1_structural_change', 'site1_formula_change', 'site1_strict_formula_diff', ...]
```

### Validation Service

The validation service is an open-source general-purpose module that can be used independently:

```python
from moltrax.services.validator import validate_results

# Validate the column structure of a result file
validate_results("your_result_file.xlsx")

# Validate and generate a backup
validate_results("your_result_file.xlsx", backup_file="backup.xlsx")
```

### Core Module Interfaces (Not Open-Sourced)

Core modules are declared as interfaces; their concrete implementations are not included. The following interface contracts can be used as a reference for self-implementation:

```python
# moltrax.models.pmd_manager
class PMDRuleManager:
    MASS_TOLERANCE = 0.1  # Mass matching tolerance (Da)

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

After implementing the above interfaces, place them in the corresponding module paths and the framework will automatically recognize and invoke them.

---

## Architecture Overview

```
MolTraX/
├── moltrax/                # Main package
│   ├── __init__.py            # Package entry, provides hello() / show_info()
│   ├── cli.py                 # Command-line entry
│   ├── config.py              # Configuration: paths, column names, thresholds
│   ├── core/
│   │   └── __init__.py        # Core engine (interface layer, not open-sourced)
│   ├── services/
│   │   ├── __init__.py
│   │   └── validator.py       # Validation service (open-sourced)
│   ├── utils/
│   │   └── __init__.py        # Utility modules (interface layer, not open-sourced)
│   └── models/
│       └── __init__.py        # Data models (interface layer, not open-sourced)
├── data/
│   ├── sample_rules.db        # Sample rule database (5 fictional rules)
│   └── batch_template.xlsx    # Batch upload template
├── scripts/
│   ├── build_sample_db.py     # Sample database generation script
│   └── build_template.py      # Batch template generation script
├── examples/
│   └── quickstart.py          # Quick start example
├── setup.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

### Layered Design

```
┌─────────────────────────────────────────┐
│   Command-Line / Programmatic Entry     │
│       moltrax info / analyze / ...      │
└──────────────────┬──────────────────────┘
                   │ Interface call
┌──────────────────▼──────────────────────┐
│          Service Layer (services/)       │
│         validator / diff_analyzer       │
└──────────────────┬──────────────────────┘
                   │ Interface call
┌──────────────────▼──────────────────────┐
│    Core Algorithm Layer (core/ + utils/)│
│   analysis_engine / mcs_calculator      │
│   formula_parser                        │
└──────────────────┬──────────────────────┘
                   │ Data access
┌──────────────────▼──────────────────────┐
│        Data Layer (models/ + data/)     │
│      pmd_manager / sample_rules.db      │
└─────────────────────────────────────────┘
```

---

## Module Overview

This repository adopts a **"framework open, core reserved"** publication strategy. The table below marks the open-source status of each module:

| Module | Path | Status | Description |
|--------|------|--------|-------------|
| Package entry | `moltrax/__init__.py` | ✅ Open | Version info, module availability detection |
| Command-line | `moltrax/cli.py` | ✅ Open | CLI entry and subcommands |
| Configuration | `moltrax/config.py` | ✅ Open | Paths, column templates, threshold constants |
| Validation service | `moltrax/services/validator.py` | ✅ Open | Result integrity check (partially degraded) |
| Sample data scripts | `scripts/` | ✅ Open | Sample database and template generation |
| Quick start examples | `examples/` | ✅ Open | Usage examples |
| Core analysis engine | `moltrax/core/analysis_engine.py` | 🔒 Interface | Structure difference analysis engine, implementation not open-sourced |
| MCS calculation | `moltrax/utils/mcs_calculator.py` | 🔒 Interface | Maximum common substructure calculation, implementation not open-sourced |
| Formula parser | `moltrax/utils/formula_parser.py` | 🔒 Interface | Formula parsing and differencing, implementation not open-sourced |
| Diff analyzer | `moltrax/services/diff_analyzer.py` | 🔒 Interface | Site-level difference analysis, implementation not open-sourced |
| Rule matching engine | `moltrax/models/pmd_manager.py` | 🔒 Interface | Rule database matching, implementation not open-sourced |

> Modules marked with 🔒 retain only interface declarations in the repository; their concrete implementation code is not included. At runtime, the framework detects the availability of these modules via `try/except` and, when missing, replaces functional calls with clear prompts.

---

## Data Description

### Sample Database

The repository provides `data/sample_rules.db`, containing 5 **fictional** sample rules:

| pmd_id | formula_change | Description |
|--------|---------------|-------------|
| PMD-DEMO-001 | +C1H2 | Methylation (sample) |
| PMD-DEMO-002 | -C1H2 | Demethylation (sample) |
| PMD-DEMO-003 | +O1 | Hydroxylation (sample) |
| PMD-DEMO-004 | -O1 | Dehydration (sample) |
| PMD-DEMO-005 | +C2H2O1 | Acetylation (sample) |

> This data is for demonstrating the framework's data structure and query workflow only and does not represent the real rule library content.

### Real Rule Library

The complete rule database (containing thousands of rules and their Chinese descriptions) is proprietary project data and **is not published with this repository**. For research or commercial use, please contact the project maintainers for authorization.

### Database Table Structure

```sql
CREATE TABLE pmd_rules (
    pmd_id           TEXT,    -- Rule ID
    pmd_value        TEXT,    -- Mass difference value
    formula_change   TEXT,    -- Formula change
    reaction         TEXT,    -- Reaction type
    description      TEXT,    -- English description
    source           TEXT,    -- Data source
    heavy_atom_count TEXT,    -- Heavy atom count
    bond_tolerance   TEXT,    -- Bond tolerance
    formula_change1  TEXT,    -- Standardized formula change
    中文描述         TEXT     -- Chinese description
);
```

---

## FAQ

**Q: How do I verify a successful installation?**

A: Run `moltrax info` or `python -c "import moltrax; moltrax.hello()"`. Seeing the welcome message indicates a successful installation.

**Q: Why does `moltrax analyze` say "core algorithm modules not open-sourced"?**

A: This is expected behavior. This repository contains only framework code; the core algorithm modules are not published. For full functionality, please contact the maintainers.

**Q: Can I use the sample database for real analysis?**

A: The sample database contains only 5 fictional rules, intended for demonstrating the data structure and query workflow. It is not suitable for real analysis.

**Q: How do I implement the core modules myself?**

A: Refer to the interface contracts in [Programming Interface](#programming-interface), implement the corresponding classes and functions, and place them in the corresponding directories under `moltrax/`. The framework will automatically recognize and invoke them.

**Q: Is Linux / macOS supported?**

A: The framework is built on pure Python and pandas, and is theoretically cross-platform. However, it has currently only been tested on Windows.

**Q: Why is RDKit commented out in requirements.txt?**

A: RDKit is only used in the core algorithm modules. Since the core modules are not open-sourced, installing RDKit is not required for the framework code in this repository. To implement the core modules yourself, install via `pip install -e .[chem]`.

**Q: Why can't I find MolTraX on PyPI?**

A: MolTraX is distributed via GitHub only and is not published on PyPI. Please install from source via `git clone`; see [Installation](#installation) for details.

---

## License

This project uses the **Display-Only License**, see [LICENSE](./LICENSE) for details.

Summary:

- ✅ Viewing and studying the code in this repository is permitted
- ❌ Commercial use is prohibited
- ❌ Creating derivative works is prohibited
- ❌ Redistribution is prohibited
- ❌ Core modules may not be obtained through reverse engineering

For commercial licensing or access to the full version, please contact the project maintainers.

---

## Citation

If you use MolTraX in research or projects, please cite it in the following format:

```bibtex
@misc{moltrax2026,
  title  = {MolTraX},
  author = {MolTraX Project Maintainers},
  year   = {2026},
  url    = {https://github.com/REI6509/MolTraX},
  note   = {Framework code open-sourced; core algorithm modules not open-sourced}
}
```

---

## Acknowledgments

The construction of MolTraX is supported by the following open-source projects:

- [pandas](https://pandas.pydata.org/) — Data processing and analysis
- [RDKit](https://www.rdkit.org/) — Cheminformatics toolkit
- [openpyxl](https://openpyxl.readthedocs.io/) — Excel read/write

Thanks to all developers who have contributed to the open-source community.

---

## Contact

- Project: [GitHub](https://github.com/REI6509/MolTraX)
- Issues: [Issues](https://github.com/REI6509/MolTraX/issues)
- Commercial licensing: please contact the project maintainers

---

*MolTraX © 2026*
