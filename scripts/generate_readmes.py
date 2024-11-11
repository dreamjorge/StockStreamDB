import os


def generate_readme(directory):
    """Generate README.md for the given directory."""
    readme_path = os.path.join(directory, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(f"# {os.path.basename(directory)}\n\n")
        readme_file.write("## Scripts\n\n")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    readme_file.write(f"### {file}\n\n")
                    readme_file.write(f"Path: `{file_path}`\n\n")
                    readme_file.write("#### Functions:\n\n")
                    with open(file_path, "r") as script_file:
                        for line in script_file:
                            if line.strip().startswith("def "):
                                function_name = line.split("(")[0].replace("def ", "")
                                readme_file.write(f"- `{function_name}`\n")
                    readme_file.write("\n")


def generate_readmes_for_all_subfolders(base_directory):
    """Generate README.md for all subfolders in the base directory."""
    for root, dirs, _ in os.walk(base_directory):
        for dir in dirs:
            generate_readme(os.path.join(root, dir))


if __name__ == "__main__":
    # Change base_directory to point to the src directory relative to the
    # script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.join(script_dir, "..", "src")
    generate_readmes_for_all_subfolders(base_directory)
