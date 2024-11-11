import requests
import os

def get_github_directory_files(owner, repo, directory_path):
    """
    Fetch the download URLs for all files in a specific directory of a GitHub repository.

    Parameters:
    owner (str): GitHub username or organization name
    repo (str): Repository name
    directory_path (str): Path to the directory within the repository
    token (str): GitHub Personal Access Token

    Returns:
    dict: Dictionary of filenames and their download URLs
    """
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{directory_path}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        file_urls = {}
        for file in files:
            if file['type'] == 'file':
                file_urls[file['name']] = file['download_url']
        return file_urls
    else:
        raise Exception(f"Failed to retrieve directory contents: {response.json().get('message')}")

# Example usage:
owner = 'TeoEchavarria'  # Replace with GitHub username or organization name
repo = 'knowledge'  # Replace with the repository name
directory_path = '_notes/Public'  # Replace with the path to the directory

try:
    files = get_github_directory_files(owner, repo, directory_path)
    for filename, url in files.items():
        print(f"{filename}: {url}")
except Exception as e:
    print(e)
