
# StockStreamDB

StockStreamDB is a tool for collecting, analyzing, and managing stock data. The project supports fundamental and sentiment analysis, providing insights into stock performance using a command-line interface (CLI).

## Features
- **Stock Data Collection**: Fetch historical stock prices using Yahoo Finance.
- **Fundamental Analysis**: Analyze financial metrics such as P/E ratios, earnings, etc.
- **Sentiment Analysis**: Extract sentiment from financial news articles.
- **Database Integration**: Store and retrieve stock data in a local SQLite database.
- **Command-Line Interface (CLI)**: Interact with the data collection, analysis, and database features through a simple CLI.

## Project Structure

```bash
StockStreamDB/
├── .devcontainer/         # Dev container configuration files
├── src/                   # Source code
│   ├── application/       # Application logic and use cases
│   ├── domain/            # Domain models for stocks, news, etc.
│   ├── infrastructure/    # Infrastructure like databases and API interactions
│   ├── interfaces/        # CLI interfaces and entry points
│   └── utils/             # Utility functions (e.g., logging)
├── tests/                 # Unit and integration tests
├── Dockerfile             # Docker configuration file
├── requirements.txt       # Python dependencies
├── alembic.ini            # Database migration configuration
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.9+
- Docker (for containerized development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dreamjorge/StockStreamDB.git
   cd StockStreamDB
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the CLI to fetch stock data:
```bash
python src/interfaces/cli/cli.py stock AAPL --period 1mo
```

### Testing

To run the tests:
```bash
pytest tests/
```

### Docker Setup

Build and run the Docker container:
```bash
docker build -t stockstreamdb .
docker run -it stockstreamdb
```

### Dev Container

If you're using VS Code, open the project as a Dev Container:
1. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
2. Open the project and select **Reopen in Container**.

## Acknowledgment

This project was developed with assistance from AI tools, including **ChatGPT**, which helped with code generation, problem-solving, and improving the project’s architecture.

## License

This project is licensed under the MIT License.
