from setuptools import setup, find_packages

setup(
    name="stock_stream_db",
    version="1.0.0",
    description="Recolección de datos de acciones, criptomonedas y noticias",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "yfinance",
        "ccxt",
        "newsapi-python",
        "vaderSentiment",
        "SQLAlchemy",
        "Flask"
    ],
    entry_points={
        "console_scripts": [
            "financial-cli = interfaces.cli.cli:main",  # Ruta correcta al script de la CLI
        ],
    },
)
