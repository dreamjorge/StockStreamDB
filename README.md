# StockStreamDB

StockStreamDB is a tool for collecting, analyzing, and managing stock data. The project supports fundamental and sentiment analysis, providing insights into stock performance using a command-line interface (CLI).

## Features
- **Stock Data Collection**: Fetch historical stock prices using Yahoo Finance.
- **Fundamental Analysis**: Analyze financial metrics such as P/E ratios, earnings, etc.
- **Sentiment Analysis**: Extract sentiment from financial news articles.
- **Database Integration**: Store and retrieve stock data in a local SQLite database.
- **Command-Line Interface (CLI)**: Interact with the data collection, analysis, and database features through a simple CLI.

## Clean Architecture

This project follows a Clean Architecture pattern, emphasizing separation of concerns and maintainability. The core principle is that dependencies should always point inwards, meaning inner layers should not depend on outer layers.

- **`src/domain`**: This is the innermost layer, containing the core business logic and enterprise-wide business rules. It defines the fundamental entities and use cases of the application. This layer should be independent of any frameworks, databases, or external services.

- **`src/application`**: This layer orchestrates the use cases defined in the domain layer. It contains application-specific business rules and coordinates the flow of data to and from the domain entities. It depends on the domain layer but is independent of the infrastructure and interfaces.

- **`src/infrastructure`**: This layer consists of concrete implementations of interfaces defined in the outer layers. It handles external concerns such as database interactions, external API calls, and other technical details. It depends on the application and domain layers.

- **`src/interfaces`**: This is the outermost layer, responsible for handling user interactions and external communication. It includes the Command-Line Interface (CLI), REST APIs, or GUI components. It depends on the application layer to execute use cases.

## Project Structure

```bash
StockStreamDB/
├── .devcontainer/         # Dev container configuration files
├── src/                   # Source code organized by Clean Architecture layers
│   ├── application/       # Application-specific business rules and use case orchestration
│   ├── domain/            # Core business logic, entities, and abstract interfaces
│   ├── infrastructure/    # Concrete implementations for databases, external APIs, etc.
│   ├── interfaces/        # User-facing interfaces (e.g., CLI, REST API)
│   └── utils/             # Utility functions (e.g., logging)
├── tests/                 # Unit and integration tests
├── Dockerfile             # Docker configuration file
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