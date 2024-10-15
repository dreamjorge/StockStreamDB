import pkg_resources

REQUIREMENTS_FILE = "requirements.txt"


def check_missing_dependencies():
    # Read the requirements.txt file
    with open(REQUIREMENTS_FILE, "r") as f:
        required_packages = [line.strip().split("==")[0] for line in f if line.strip()]

    # Get the installed packages
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    # Find missing dependencies
    missing_packages = [
        pkg for pkg in required_packages if pkg.lower() not in installed_packages
    ]

    if missing_packages:
        print("Missing dependencies detected:")
        for pkg in missing_packages:
            print(f"- {pkg}")
        print(
            "\nPlease run `pip install -r requirements.txt` \
            to install the missing dependencies."
        )
        return False  # Return failure status for GitHub Action
    else:
        print("All dependencies are installed.")
        return True  # Return success status


if __name__ == "__main__":
    success = check_missing_dependencies()
    if not success:
        exit(1)  # Exit with a non-zero status to fail the GitHub Action
