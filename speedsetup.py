"""
speedsetup.py: A CLI tool for rapid project initialization.

speedsetup.py simplifies the process of starting new development projects by automating the setup of various types of project environments.
It can initialize projects like React applications, Chrome extensions, and more, with just a single command. 
The tool also handles the creation of corresponding GitHub repositories, allowing developers to focus on the creative aspect of their work from the get-go.

Developed by: MD Arifuzzaman
Date: February 22, 2023
License: MIT

Usage:
    python speedsetup.py <project_type> <project_name> [--open]
    - project_type: The type of project to initialize (e.g., 'react', 'chrome-extension').
    - project_name: The name of the new project.
    - --open: (Optional) Open the project in the default code editor after creation.

Example:
    python speedsetup.py react my-new-react-app --open

Please report any issues or contribute to the project at:
https://github.com/mdarifuzzaman11/speedsetup
"""


import argparse
import os
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the setup functions from the other modules
from chrome_extension import setup as setup_chrome_extension
from react_project import setup as setup_react_project

def initialize_git_repo(project_path):
    os.chdir(project_path)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", "Initial commit"])

def create_github_repo(repo_name):
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise Exception("GitHub token not found. Set your GITHUB_TOKEN environment variable.")
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False  # Set to True for a private repository
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["clone_url"]
    else:
        raise Exception(f"Failed to create repository on GitHub: {response.content}")

def push_to_github(project_path, repo_url):
    os.chdir(project_path)
    subprocess.run(["git", "remote", "add", "origin", repo_url])
    subprocess.run(["git", "push", "-u", "origin", "main"])

def main():
    parser = argparse.ArgumentParser(description="Project Creation Tool")
    subparsers = parser.add_subparsers(dest="project_type")

    chrome_parser = subparsers.add_parser('chrome-extension', help='Create a Chrome Extension project')
    chrome_parser.add_argument('name', type=str, help='Project name')
    chrome_parser.add_argument('--open', action='store_true', help='Open in VS Code after creation')

    react_parser = subparsers.add_parser('react', help='Create a React.js project')
    react_parser.add_argument('name', type=str, help='Project name')
    react_parser.add_argument('--open', action='store_true', help='Open in VS Code and run the project')

    args = parser.parse_args()

    project_path = os.path.join(os.path.expanduser('~'), 'Desktop', args.name)

    if args.project_type == 'chrome-extension':
        setup_chrome_extension(args.name, args.open)
        project_path = os.path.join(os.path.expanduser('~'), 'Desktop', args.name)
    elif args.project_type == 'react':
        setup_react_project(args.name, args.open)
        project_path = os.path.join(os.path.expanduser('~'), 'Desktop', args.name)
    else:
        parser.print_help()
        return

    initialize_git_repo(project_path)
    repo_url = create_github_repo(args.name)
    push_to_github(project_path, repo_url)

if __name__ == "__main__":
    main()
