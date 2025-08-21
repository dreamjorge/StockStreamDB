# Refactoring and Simplicity Guidelines for StockStreamDB

This document outlines the best practices for refactoring the StockStreamDB project. The primary goal is to improve code quality, maintainability, and performance while adhering to the principle of simplicity and our established architectural patterns.

## Core Principles

1.  **KISS (Keep It Simple, Stupid):**
    *   Prefer simple, straightforward solutions over complex ones.
    *   Avoid premature optimizations and overly abstract designs.
    *   Each function and class should have a single, clear purpose.

2.  **DRY (Don't Repeat Yourself):**
    *   Reuse code through functions, classes, and modules.
    *   Avoid duplicating logic in multiple places. Centralize common functionalities.

3.  **YAGNI (You Ain't Gonna Need It):**
    *   Do not add functionality unless it is necessary *right now*.
    *   Avoid adding features based on speculation about future needs.

## Architectural Guidelines

This project follows a Clean Architecture pattern. It is crucial to respect the separation of concerns between the different layers.

*   **`src/domain`**: This is the core of the application. It should contain only pure business logic and domain models.
    *   **DO NOT** introduce dependencies on frameworks, databases, or external APIs in this layer.
    *   Entities here should be simple Python objects.

*   **`src/application`**: This layer orchestrates the use cases of the application.
    *   It uses the domain objects and repositories to perform tasks.
    *   It should not contain business logic itself but rather coordinate the domain layer to execute it.

*   **`src/infrastructure`**: This layer contains the implementation details.
    *   Database access (`db/`), external API clients (`api_clients/`), and other concrete implementations of the repository interfaces defined in the domain.
    *   This is the only layer that should be aware of specific technologies (e.g., SQLAlchemy, `yfinance`).

*   **`src/interfaces`**: This layer defines how the outside world interacts with the application.
    *   Includes the Command-Line Interface (`cli/`), REST API, etc.
    *   It should delegate all actions to the application layer.

**Rule of thumb:** Dependencies should always point inwards (e.g., `infrastructure` -> `application` -> `domain`).

## Code-Level Best Practices

1.  **Readability and Naming:**
    *   Use clear, descriptive names for variables, functions, and classes.
    *   Follow PEP 8 style guidelines. Use `flake8` to enforce this (`config/.flake8`).
    *   Keep functions short and focused on a single task.

2.  **Type Hinting:**
    *   Use Python's type hints for all function signatures and variables. This improves clarity and allows for static analysis.

3.  **Testing:**
    *   Every refactoring effort **must** be accompanied by tests. If tests are missing for the code you are refactoring, write them first.
    *   Use `pytest` as the testing framework.
    *   Ensure tests are fast, reliable, and cover both success and failure cases.

4.  **Dependency Injection:**
    *   Use the dependency injection container (`src/containers.py`) to manage dependencies.
    *   Avoid hardcoding dependencies. Instead, inject them where they are needed. This makes the code more modular and easier to test.

5.  **Configuration:**
    *   All configuration should be handled via `config/config.ini`.
    *   Do not hardcode configuration values in the code.

6.  **Database Migrations:**
    *   All changes to the database schema must be done through `alembic` migrations.
    *   This ensures that the schema is version-controlled and can be reproduced reliably.

## Refactoring Workflow

1.  **Identify a Target:** Choose a small, well-defined piece of code to refactor.
2.  **Ensure Test Coverage:** Verify that the existing behavior is covered by tests. If not, write them.
3.  **Refactor:** Make the desired changes, adhering to the principles in this document.
4.  **Run All Tests:** Ensure that your changes have not broken any existing functionality (`pytest`).
5.  **Run Linter:** Check for style issues (`flake8`).
6.  **Commit:** Write a clear and concise commit message explaining the *why* behind the refactoring.
