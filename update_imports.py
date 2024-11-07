import os
import re


def update_imports_in_file(file_path):
    """Update 'from src.' imports to remove the 'src.' prefix."""
    with open(file_path, "r") as file:
        content = file.read()

    # Replace 'from src.' with 'from ' (remove the 'src.' prefix)
    updated_content = re.sub(r"from src\.", "from ", content)

    # Replace 'import src.' with 'import ' (if applicable)
    updated_content = re.sub(r"import src\.", "import ", updated_content)

    # If changes were made, overwrite the file
    if updated_content != content:
        with open(file_path, "w") as file:
            file.write(updated_content)
        print(f"Updated imports in {file_path}")


def update_imports_in_directory(directory):
    """Recursively update 'from src.' imports in all Python files in the directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                update_imports_in_file(file_path)


if __name__ == "__main__":
    src_directory = "src"  # Path to your src directory
    print(f"Starting import update in directory: {src_directory}")
    update_imports_in_directory(src_directory)
    print("Finished updating imports.")
