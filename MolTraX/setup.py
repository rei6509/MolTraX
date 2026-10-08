from setuptools import setup, find_packages

setup(
    name="moltrax",
    version="0.1.0",
    description="MolTraX",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="MolTraX Project Maintainers",
    license="Display-Only",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "moltrax": [],
    },
    data_files=[
        ("data", ["data/sample_rules.db", "data/batch_template.xlsx"]),
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
    ],
    extras_require={
        "chem": ["rdkit>=2023.03.1"],
        "dev": ["pytest", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "moltrax=moltrax.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: Other/Proprietary License",
    ],
)
