import subprocess
from pathlib import Path  # Function to run flake8 and auto-fix some issues

PROJECT_PATH = Path("src/")

# Helper function to log messages


def log_message(message):
    print(message)


def run_flake8_and_fix():
    log_message("\nRunning flake8 to check for formatting issues...")

    result = subprocess.run(["flake8", str(PROJECT_PATH)], stdout=subprocess.PIPE)
    flake8_output = result.stdout.decode("utf-8")
    log_message(f"\nflake8 issues detected:\n{flake8_output}")

    log_message("\nFixing common formatting issues...")

    for file_path, line_number, error_code, description in parse_flake8_output(
        flake8_output
    ):
        if error_code == "E302":
            # Add missing blank lines
            fix_missing_blank_lines(file_path, line_number)
        elif error_code == "E501":
            # Shorten long lines
            fix_long_lines(file_path, line_number)
        else:
            log_message(
                f"Manual fix needed for {file_path}:"
                f"{line_number} - {description}"
            )


# Parse the flake8 output to get the file paths and issues


def parse_flake8_output(output):
    issues = []
    for line in output.splitlines():
        parts = line.split(":")
        if len(parts) >= 4:
            file_path = parts[0]
            line_number = int(parts[1])
            error_code = parts[2].strip()
            description = parts[3].strip()
            issues.append((file_path, line_number, error_code, description))
    return issues


# Automatically fix missing blank lines (E302)


def fix_missing_blank_lines(file_path, line_number):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Insert a blank line before the specified line
    if line_number - 1 > 0:
        lines.insert(line_number - 1, "\n")

    with open(file_path, "w") as f:
        f.writelines(lines)

    log_message(f"Added missing blank lines in {file_path} at line {line_number}")


# Automatically fix long lines (E501)


def fix_long_lines(file_path, line_number):
    with open(file_path, "r") as f:
        lines = f.readlines()

    line = lines[line_number - 1].strip()
    if len(line) > 88:
        # Break the long line into multiple shorter lines
        split_line = line.split(" ")
        new_line = ""
        current_length = 0
        for word in split_line:
            if current_length + len(word) + 1 > 88:
                new_line += "\n" + word + " "
                current_length = len(word) + 1
            else:
                new_line += word + " "
                current_length += len(word) + 1

        lines[line_number - 1] = new_line.strip() + "\n"

    with open(file_path, "w") as f:
        f.writelines(lines)

    log_message(f"Shortened long line in {file_path} at line {line_number}")


# Main function
if __name__ == "__main__":

    run_flake8_and_fix()
