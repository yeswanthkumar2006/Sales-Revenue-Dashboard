"""Setup configuration for Sales Analytics Dashboard."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sales-analytics-dashboard",
    version="2.0.0",
    author="Analytics Team",
    author_email="team@example.com",
    description="A comprehensive sales analytics and reporting dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sales-analytics-dashboard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Enterprise",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "plotly>=5.18.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sales-dashboard=main:main",
        ],
    },
)
