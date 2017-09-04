import os

from github import Github


def get_repository(name, username=None, password=None):
    username = username or os.getenv('GITHUB_USERNAME')
    password = password or os.getenv('GITHUB_PASSWORD')
    return Github(username, password).get_repo(name)
