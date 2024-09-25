import os
import yaml
import logging
import traceback
from datetime import datetime
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
        logging.FileHandler("issue_creation.log", mode='w'),  # Save logs to file
        logging.StreamHandler()  # Also output to the console
    ]
)

class GitHubManager:
    def __init__(self, token, repo_owner, repo_name):
        self.github = Github(token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
        self.cached_labels = None
        self.cached_milestones = None
        self.cached_issues = None

    def get_cached_labels(self):
        if self.cached_labels is None:
            self.cached_labels = {label.name: label for label in self.repo.get_labels()}
        return self.cached_labels

    def create_label_if_not_exists(self, label_name, color="ffffff", description=""):
        labels = self.get_cached_labels()
        if label_name in labels:
            logging.info(f"Label '{label_name}' already exists. Skipping creation.")
            return labels[label_name]

        try:
            logging.info(f"Creating new label '{label_name}'.")
            label = self.repo.create_label(name=label_name, color=color, description=description)
            self.cached_labels[label_name] = label  # Cache the newly created label
            logging.info(f"Label '{label_name}' created successfully.")
            return label
        except Exception as e:
            if "already_exists" in str(e):
                logging.info(f"Label '{label_name}' already exists according to the API. Skipping.")
            else:
                logging.error(f"Failed to create label '{label_name}': {traceback.format_exc()}")
            return None

    def get_cached_milestones(self):
        if self.cached_milestones is None:
            self.cached_milestones = {milestone.title: milestone for milestone in self.repo.get_milestones(state='open')}
        return self.cached_milestones

    def create_milestone_if_not_exists(self, milestone_title, description="Milestone created via script", due_on=None):
        milestones = self.get_cached_milestones()
        if milestone_title in milestones:
            logging.info(f"Milestone '{milestone_title}' already exists. Skipping creation.")
            return milestones[milestone_title]

        try:
            logging.info(f"Milestone '{milestone_title}' does not exist. Creating a new milestone.")
            milestone_kwargs = {"title": milestone_title, "state": "open", "description": description}
            if due_on:
                milestone_kwargs["due_on"] = due_on
            milestone = self.repo.create_milestone(**milestone_kwargs)
            self.cached_milestones[milestone_title] = milestone
            logging.info(f"Milestone '{milestone_title}' created successfully.")
            return milestone
        except Exception as e:
            logging.error(f"Failed to create milestone '{milestone_title}': {traceback.format_exc()}")
            return None

    def get_cached_issues(self):
        if self.cached_issues is None:
            self.cached_issues = {issue.title: issue for issue in self.repo.get_issues(state='open')}
        return self.cached_issues

class IssueManager:
    def __init__(self, github_manager):
        self.github_manager = github_manager

    def ensure_labels_exist(self, labels, label_colors):
        for label in labels:
            color = label_colors.get(label, "ffffff")
            self.github_manager.create_label_if_not_exists(label, color)

    def update_issue_if_needed(self, issue, labels, milestone_title, label_colors):
        # Ensure all labels exist
        self.ensure_labels_exist(labels, label_colors)

        # Fetch valid labels from the repository (just the names)
        valid_labels = [label.name for label in self.github_manager.get_cached_labels().values() if label.name in labels]
        
        # Get existing labels from the issue (just the names)
        existing_labels = [label.name for label in issue.labels]
        
        # Check if labels need to be updated
        if set(existing_labels) != set(labels):
            logging.info(f"Updating labels for issue '{issue.title}'.")
            issue.edit(labels=valid_labels)  # Pass the label names as strings

        # Update milestone if needed
        if milestone_title:
            milestone = self.github_manager.create_milestone_if_not_exists(milestone_title)
            if issue.milestone is None or (issue.milestone and issue.milestone.title != milestone_title):
                logging.info(f"Updating milestone for issue '{issue.title}'.")
                issue.edit(milestone=milestone)


    def create_or_update_issue(self, title, body, labels=None, milestone_title=None, label_colors=None, milestone_description=None, milestone_due_on=None):
        if not self.check_rate_limit():
            return "failed"

        issues = self.github_manager.get_cached_issues()
        if title in issues:
            issue = issues[title]
            logging.info(f"Issue with title '{title}' already exists. Checking for updates.")
            self.update_issue_if_needed(issue, labels, milestone_title, label_colors)
            return "updated"


        logging.info(f"Creating new issue: {title}")
        milestone = None
        if milestone_title:
            milestone = self.github_manager.create_milestone_if_not_exists(milestone_title, description=milestone_description, due_on=milestone_due_on)

        if labels:
            # Ensure labels exist, considering case insensitivity
            existing_labels = self.github_manager.get_cached_labels().values()
            normalized_existing_labels = {label.name.lower(): label for label in existing_labels}
            
            for label in labels:
                normalized_label = label.lower()
                if normalized_label in normalized_existing_labels:
                    logging.info(f"Using existing label: {normalized_existing_labels[normalized_label].name}")
                else:
                    logging.info(f"Creating new label: {label}")
                    self.github_manager.create_label(label, label_colors.get(label, "FFFFFF"))

        valid_labels = [label for label in self.github_manager.get_cached_labels().values() if label.name.lower() in [l.lower() for l in labels]]

        issue_kwargs = {"title": title, "body": body, "labels": valid_labels}
        if milestone:
            issue_kwargs["milestone"] = milestone

        try:
            issue = self.github_manager.repo.create_issue(**issue_kwargs)
            logging.info(f'Successfully created issue: {issue.html_url}')
            return "created"
        except Exception as e:
            logging.error(f'Failed to create issue "{title}": {traceback.format_exc()}')
            return "failed"

    def check_rate_limit(self):
        rate_limit = self.github_manager.github.get_rate_limit().core
        if rate_limit.remaining == 0:
            reset_time = datetime.fromtimestamp(rate_limit.reset.timestamp())
            logging.error(f"GitHub API rate limit exceeded. Limit will reset at {reset_time}.")
            return False
        logging.info(f"GitHub API rate limit: {rate_limit.remaining}/{rate_limit.limit}")
        return True

def create_issues_from_yaml(file_path, github_manager):
    issue_manager = IssueManager(github_manager)
    total_issues = created_issues = updated_issues = skipped_issues = failed_issues = 0

    with open(file_path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            issues = data.get('issues', [])
            total_issues = len(issues)
            logging.info(f"Found {total_issues} issues in YAML.")

            for idx, issue in enumerate(issues, start=1):
                prefix = issue.get('prefix', '')  
                title = f"{prefix} {issue.get('title')}".strip()  
                description = issue.get('description')
                labels = issue.get('labels', [])
                label_colors = issue.get('label_colors', {})
                milestone = issue.get('milestone', None)
                milestone_description = issue.get('milestone_description', "Milestone created via script")
                milestone_due_on = issue.get('milestone_due_on', None)
                if milestone_due_on:
                    milestone_due_on = datetime.strptime(milestone_due_on, "%Y-%m-%d").isoformat() + "Z"

                logging.info(f"Processing issue {idx}/{total_issues}: {title}")
                result = issue_manager.create_or_update_issue(title, description, labels, milestone, label_colors, milestone_description, milestone_due_on)

                if result == "created":
                    created_issues += 1
                elif result == "updated":
                    updated_issues += 1
                else:
                    failed_issues += 1

        except yaml.YAMLError as e:
            logging.error(f"Error reading YAML file: {str(e)}")

    logging.info(f"Processing complete. Created: {created_issues}, Updated: {updated_issues}, Skipped: {skipped_issues}, Failed: {failed_issues}")

if __name__ == '__main__':
    try:
        github_manager = GitHubManager(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(script_dir, 'issues.yaml')
        create_issues_from_yaml(yaml_file, github_manager)
    except KeyboardInterrupt:
        logging.error("Script was interrupted by the user. Exiting gracefully.")
        print("\nProcess interrupted. Exiting gracefully.")
