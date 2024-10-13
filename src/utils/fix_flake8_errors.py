import os
import re
import autopep8

# Path to your project files
PROJECT_PATH = 'src/'  # Change this to your project's root directory

# Flake8 Error Codes
LONG_LINE_ERROR = "E501"
UNUSED_VAR_ERROR = "F841"
UNDEFINED_NAME_ERROR = "F821"
UNUSED_IMPORT_ERROR = "F401"
REDEFINED_VAR_ERROR = "F811"


def fix_long_lines(file_path):
    """Fix long lines using autopep8."""
    autopep8.fix_file(
        file_path,
        options={
            'max_line_length': 88,
            'aggressive': 2
        }
    )
    print(f"Fixed long lines in {file_path}")


def fix_unused_vars(file_path, line_number):
    """Remove unused variables from the specified file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    line = lines[line_number - 1]
    # Detect assignment in the form of `variable = ...`
    variable_match = re.search(r"(\w+)\s*=", line)
    if variable_match:
        variable = variable_match.group(1)
        # Remove the line
        lines.pop(line_number - 1)
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(
            f"Removed unused variable '{variable}' "
            f"from {file_path}:{line_number}"
        )


def remove_unused_imports(file_path, line_number):
    """Remove unused import lines."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove the import line
    lines.pop(line_number - 1)
    with open(file_path, 'w') as f:
        f.writelines(lines)
    print(f"Removed unused import from {file_path}:{line_number}")


def resolve_redefined_vars(file_path, line_number):
    """Fix redefined variable errors by keeping the correct definition."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove the line with the redefinition
    lines.pop(line_number - 1)
    with open(file_path, 'w') as f:
        f.writelines(lines)
    print(f"Resolved redefined variable in {file_path}:{line_number}")


def process_flake8_errors():
    """Process the flake8 errors and fix them."""
    result = os.popen('flake8').read()

    for line in result.splitlines():
        parts = line.split(":")
        if len(parts) >= 4:
            file_path = parts[0]
            line_number = int(parts[1])
            error_code = parts[2].strip()

            if error_code == LONG_LINE_ERROR:
                fix_long_lines(file_path)
            elif error_code == UNUSED_VAR_ERROR:
                fix_unused_vars(file_path, line_number)
            elif error_code == UNUSED_IMPORT_ERROR:
                remove_unused_imports(file_path, line_number)
            elif error_code == REDEFINED_VAR_ERROR:
                resolve_redefined_vars(file_path, line_number)
            elif error_code == UNDEFINED_NAME_ERROR:
                print(
                    f"Undefined name found in {file_path}:{line_number}. "
                    "Manual fix required."
                )


if __name__ == "__main__":
    process_flake8_errors()
