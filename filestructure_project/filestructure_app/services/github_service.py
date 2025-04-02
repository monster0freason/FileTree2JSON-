# filestructure_app/services/github_service.py
import os
import tempfile
import requests
import zipfile
import io
import shutil

class GitHubService:
    def __init__(self):
        self.temp_dir = None
    
    def download_repository(self, repo_url):
        """Download a GitHub repository and return its local path"""
        try:
            # Convert GitHub URL to download URL
            # Example: https://github.com/username/repo -> https://github.com/username/repo/archive/main.zip
            if repo_url.endswith('/'):
                repo_url = repo_url[:-1]
            
            # Parse repository owner and name
            parts = repo_url.split('/')
            if len(parts) < 5 or parts[2] != 'github.com':
                return None, "Invalid GitHub URL"
            
            owner = parts[3]
            repo = parts[4]
            branch = 'main'  # Default branch
            
            # Try to get the default branch
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url)
            if response.status_code == 200:
                branch = response.json().get('default_branch', 'main')
            
            # Download the repository as a zip file
            download_url = f"https://github.com/{owner}/{repo}/archive/{branch}.zip"
            response = requests.get(download_url)
            if response.status_code != 200:
                return None, f"Failed to download repository: {response.status_code}"
            
            # Create a temporary directory
            self.temp_dir = tempfile.mkdtemp()
            
            # Extract the zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            # The zip file extracts to a directory with the format {repo}-{branch}
            extracted_dir = os.path.join(self.temp_dir, f"{repo}-{branch}")
            if not os.path.exists(extracted_dir):
                # Try to find the extracted directory
                dirs = os.listdir(self.temp_dir)
                if len(dirs) > 0:
                    extracted_dir = os.path.join(self.temp_dir, dirs[0])
            
            return extracted_dir, None
        except Exception as e:
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            return None, str(e)
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)