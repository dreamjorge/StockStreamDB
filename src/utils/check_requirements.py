import os
import ast
import pkg_resources
import subprocess
import sys

# Define paths to the requirements files
ROOT_REQUIREMENTS_FILE = "requirements.txt"
DEVCONTAINER_REQUIREMENTS_FILE = ".devcontainer/requirements.txt"


def get_installed_packages():
    """Get a list of all installed packages and their versions."""
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    return installed_packages


def get_imported_modules(directory):
    """Recursively find all Python files and extract imported modules."""
    imported_modules = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                    except SyntaxError:
                        continue  # Skip files with syntax errors

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imported_modules.add(alias.name.split(".")[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imported_modules.add(node.module.split(".")[0])

    return imported_modules


def get_requirements_from_file(file_path):
    """Read a requirements file and return a set of requirements."""
    if not os.path.exists(file_path):
        return set()

    with open(file_path, "r") as f:
        return set(
            line.split("==")[0].strip()
            for line in f
            if line.strip() and not line.startswith("#")
        )


def update_requirements_file(missing_packages, requirements_file):
    """Add missing packages to a requirements.txt and sort it alphabetically."""
    if missing_packages:
        print(
            f"Adding missing packages to {requirements_file}: "
            f"{', '.join(missing_packages)}"
        )
        # Install the missing packages and add them to the requirements.txt file
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + list(missing_packages)
        )

        installed_packages = get_installed_packages()

        with open(requirements_file, "a") as f:
            for package in missing_packages:
                version = installed_packages.get(package, "")
                if version:
                    f.write(f"{package}=={version}\n")

    # Read the updated file and sort it alphabetically
    with open(requirements_file, "r") as f:
        lines = sorted(f.readlines())

    with open(requirements_file, "w") as f:
        f.writelines(lines)

    print(f"{requirements_file} has been updated and sorted alphabetically.")


def check_and_sync_requirements():
    """Check if both requirements.txt files are consistent and sync them."""
    # Get the requirements from both files
    root_requirements = get_requirements_from_file(ROOT_REQUIREMENTS_FILE)
    devcontainer_requirements = get_requirements_from_file(
        DEVCONTAINER_REQUIREMENTS_FILE
    )

    # Find any missing packages in either file
    missing_in_root = devcontainer_requirements - root_requirements
    missing_in_devcontainer = root_requirements - devcontainer_requirements

    if missing_in_root:
        print(f"Missing in {ROOT_REQUIREMENTS_FILE}: {missing_in_root}")
        update_requirements_file(missing_in_root, ROOT_REQUIREMENTS_FILE)

    if missing_in_devcontainer:
        print(f"Missing in {DEVCONTAINER_REQUIREMENTS_FILE}: {missing_in_devcontainer}")
        update_requirements_file(
            missing_in_devcontainer, DEVCONTAINER_REQUIREMENTS_FILE
        )

    if not missing_in_root and not missing_in_devcontainer:
        print("Both requirements.txt files are already consistent and up to date.")


if __name__ == "__main__":
    project_dir = "src"  # Replace with your project's source directory

    print("Checking requirements...")

    # Get the set of installed packages and their versions
    installed_packages = get_installed_packages()

    # Get the set of imported modules in the project
    imported_modules = get_imported_modules(project_dir)

    # Check and synchronize the requirements files
    check_and_sync_requirements()

    # Ensure that all imported modules are listed in both requirements files
    root_requirements = get_requirements_from_file(ROOT_REQUIREMENTS_FILE)
    devcontainer_requirements = get_requirements_from_file(
        DEVCONTAINER_REQUIREMENTS_FILE
    )

    # Find missing packages across the two requirements files and installed packages
    missing_packages = imported_modules - (
        root_requirements | devcontainer_requirements
    )

    missing_packages_to_add = {
        pkg for pkg in missing_packages if pkg in installed_packages
    }

    if missing_packages_to_add:
        update_requirements_file(missing_packages_to_add, ROOT_REQUIREMENTS_FILE)
        update_requirements_file(
            missing_packages_to_add, DEVCONTAINER_REQUIREMENTS_FILE
        )
    else:
        print("No missing packages found. All requirements are up to date.")
