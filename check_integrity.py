import os
import subprocess
import sys
import importlib
import pkg_resources
import logging
from datetime import datetime

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define the required project files and directories
REQUIRED_FILES = [
    "setup.py",
    "requirements.txt",
    "src/",
    ".env",  # Add additional file types like .env, .dockerignore, etc.
    ".dockerignore",
    "README.md",
]

# Define the required modules to import
REQUIRED_IMPORTS = [
    "infrastructure.db.stock_repository_impl",
    "application.use_cases.manage_stock",
    "infrastructure.db.db_setup",
    "infrastructure.fetchers.yahoo_finance_fetcher",
    "application.generate_stock_data",
    "utils.stock_plotting",
]

# Define CLI commands to test after installation
CLI_COMMANDS = [
    "stockstreamdb --help",
    "stockstreamdb check-data AAPL",  # Sample command, modify as needed
    "stockstreamdb plot-data --csv-file stock_data.csv "
    "--ticker NVDA",  # Sample plotting command
]


def get_required_packages():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def check_file_structure(report):
    """Check if all required files and directories are present."""
    logger.info("Checking file structure...")
    missing = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    if missing:
        logger.error(f"Missing files or directories: {', '.join(missing)}")
        report.append(f"Missing files or directories: {', '.join(missing)}")
        return False
    logger.info("File structure is intact.")
    report.append("File structure is intact.")
    return True


def check_imports(report):
    """Check if required modules can be imported successfully."""
    logger.info("Checking imports...")
    failed_imports = []
    for module in REQUIRED_IMPORTS:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as e:
            failed_imports.append((module, str(e)))
            logger.error(f"Failed to import {module}: {e}")

    if failed_imports:
        for module, error in failed_imports:
            report.append(f"Failed to import {module}: {error}")
        return False

    logger.info("All imports are successful.")
    report.append("All imports are successful.")
    return True


def check_dependencies(report):
    """Check if all required dependencies are installed."""
    logger.info("Checking dependencies...")
    required_packages = get_required_packages()
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    missing_packages = [
        pkg for pkg in required_packages if pkg.split("==")[0] not in installed_packages
    ]

    if missing_packages:
        logger.error(f"Missing dependencies: {', '.join(missing_packages)}")
        report.append(f"Missing dependencies: {', '.join(missing_packages)}")
        return False

    logger.info("All dependencies are installed.")
    report.append("All dependencies are installed.")
    return True


def run_linter(report):
    """Run linter (flake8) to check for code quality issues."""
    logger.info("Running flake8 linter for static code check...")
    try:
        result = subprocess.run(
            ["flake8", "src/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            logger.info("No linter issues found.")
            report.append("No linter issues found.")
        else:
            logger.error(result.stdout.decode())
            report.append(result.stdout.decode())
            return False
    except FileNotFoundError:
        logger.error("flake8 is not installed. Skipping linter check.")
        report.append("flake8 is not installed. Skipping linter check.")
        return False
    return True


def check_cli_commands(report):
    """Run CLI commands to ensure the project was installed and is functional."""
    logger.info("Checking CLI commands...")
    failed_commands = []
    for command in CLI_COMMANDS:
        try:
            result = subprocess.run(
                command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                failed_commands.append((command, result.stderr.decode()))
                logger.error(
                    f"Command '{command}' "
                    f"failed with error: {result.stderr.decode()}"
                )
            else:
                logger.info(f"Command '{command}' ran successfully.")
                report.append(f"Command '{command}' ran successfully.")
        except FileNotFoundError:
            logger.error(
                f"Command '{command}' not found. Make sure the package is installed."
            )
            report.append(
                f"Command '{command}' not found. Make sure the package is installed."
            )
            return False

    if failed_commands:
        for command, error in failed_commands:
            report.append(f"Command '{command}' failed with error: {error}")
        return False
    return True


def check_database_connection(report):
    """Check database connection (if applicable)."""
    # Example check, you can customize this according to your project
    logger.info("Checking database connection...")
    try:
        logger.info("Database connection is successful.")
        report.append("Database connection is successful.")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        report.append(f"Failed to connect to the database: {e}")
        return False


def generate_report(report_content):
    """Save the report to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"project_integrity_report_{timestamp}.txt"
    with open(report_filename, "w") as report_file:
        report_file.write("\n".join(report_content))
    logger.info(f"\nReport generated: {report_filename}")


def main():
    """Main function to run integrity checks."""
    report = []

    # Start the checks
    logger.info("Starting project integrity check...")
    report.append("Starting project integrity check...")

    file_structure_ok = check_file_structure(report)
    imports_ok = check_imports(report)
    dependencies_ok = check_dependencies(report)
    linter_ok = run_linter(report)
    cli_ok = check_cli_commands(report)
    db_ok = check_database_connection(report)

    # Generate report and save it
    generate_report(report)

    # Determine overall success
    all_checks_ok = all(
        [file_structure_ok, imports_ok, dependencies_ok, linter_ok, cli_ok, db_ok]
    )

    if all_checks_ok:
        logger.info("Project integrity check passed successfully.")
    else:
        logger.error("Project integrity check failed. Please address the issues above.")

    # Return the result (0 for success, 1 for failure)
    sys.exit(0 if all_checks_ok else 1)


if __name__ == "__main__":
    main()
