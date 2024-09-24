# Contributing to StockStreamDB

Thank you for considering contributing to StockStreamDB! We appreciate your time and effort in making the project better.

## Branch Naming Conventions

We follow a strict branch naming convention to maintain a clean and understandable Git history. Please ensure you name your branches using the following patterns:

- **feature/short-description**: Use this for new features. Example: `feature/add-login-functionality`
- **bugfix/short-description**: Use this for bug fixes. Example: `bugfix/fix-login-error`
- **improvement/short-description**: Use this for minor improvements or refactors. Example: `improvement/clean-up-logging`

Ensure the short description is concise and related to the changes you are making.

## Commit Message Guidelines

Commit messages should follow this format:

   [type] Short summary of the changes
   Optional detailed description of what was changed, why, and how.

Where `type` is one of the following:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **test**: Adding missing or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries

Example commit message:

   [feat] Implement user authentication
   Added a new feature for user authentication using JWT tokens.

## Code Review Process

1. **Open a Pull Request (PR)**:
   - Ensure your branch is up-to-date with the latest `main`.
   - Open a PR and provide a clear description of the changes.
   - Ensure that your PR title follows the branch naming conventions.
   
2. **Await Review**:
   - Wait for one or more team members to review your PR.
   - Be open to feedback and be ready to make changes.

## Testing Guidelines

We require that all contributions include adequate testing. Ensure that your changes do not break any existing tests and that new tests are included for new features or bug fixes.

1. Run the test suite using `pytest` before submitting your PR.
2. Include both unit and integration tests for your code when applicable.

## Code Formatting and Linting

We use `black` for code formatting and `flake8` for linting. Please make sure your code adheres to the following before submitting:

1. Run `black` to format your code:
   ```
   black .
   ```

2. Run `flake8` to check for linting errors:
   ```
   flake8 .
   ```

## Issues and Feature Requests

If you encounter any issues or have ideas for new features, please feel free to open an issue in the GitHub repository. Make sure to provide enough information for others to understand and replicate the issue.

## License

By contributing to StockStreamDB, you agree that your contributions will be licensed under the MIT License.
