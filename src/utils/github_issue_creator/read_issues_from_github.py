import os
import yaml
import logging
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

# GitHub repository details
REPO_OWNER = os.getenv('REPO_OWNER', 'your_repo_owner')  # Set a default owner if not in .env
REPO_NAME = os.getenv('REPO_NAME', 'your_repo_name')     # Set a default repo if not in .env

# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("issue_export.log", mode='w'),  # Save logs to file
        logging.StreamHandler()  # Also output to the console
    ]
)

# Authenticate with GitHub using the token
g = Github(GITHUB_TOKEN)

# Initialize the repo object globally
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

# Function to fetch all issues and write them to a YAML file
def export_issues_to_yaml(output_file):
    logging.info("Fetching all issues from the repository.")
    
    # Fetch all open issues from the repo
    issues = repo.get_issues(state='all')
    
    issues_list = []

    # Loop through each issue and structure it for YAML
    for issue in issues:
        issue_data = {
            'prefix': '[%s]' % issue.labels[0].name if issue.labels else '',  # Assuming first label as prefix
            'title': issue.title,
            'description': issue.body or '',
            'labels': [label.name for label in issue.labels],
            'milestone': issue.milestone.title if issue.milestone else None,
            'milestone_description': issue.milestone.description if issue.milestone else '',
            'milestone_due_on': issue.milestone.due_on.strftime('%Y-%m-%d') if issue.milestone and issue.milestone.due_on else None,
        }
        issues_list.append(issue_data)
    
    # Structure the issues in a dictionary for YAML
    issues_dict = {'issues': issues_list}

    # Write the issues to the YAML file
    with open(output_file, 'w') as yaml_file:
        yaml.dump(issues_dict, yaml_file, default_flow_style=False)

    logging.info(f"Issues exported successfully to {output_file}")

# Example usage
if __name__ == '__main__':
    output_yaml = os.path.join(os.getcwd(), 'exported_issues.yaml')
    export_issues_to_yaml(output_yaml)
    print(f"Issues exported to {output_yaml}")
