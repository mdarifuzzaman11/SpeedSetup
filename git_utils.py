import os
import subprocess
import requests

def initialize_git_repo(project_path):
    # Change to project directory
    os.chdir(project_path)

    # Initialize the Git repository
    subprocess.run(["git", "init"])

    # Add all files to the staging area
    subprocess.run(["git", "add", "-A"])

    # Commit the changes
    subprocess.run(["git", "commit", "-m", "Initial commit"])

def create_github_repo(token, repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False  # Set to True if you want private repository
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["clone_url"]
    else:
        raise Exception(f"Failed to create repository on GitHub: {response.content}")

def push_to_github(project_path, repo_url):
    # Set the remote origin and push the code
    try:
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=project_path, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_path, check=True)
        print("Code pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pushing code to GitHub: {e}")
