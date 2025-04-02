import os
import json
import tempfile
import shutil
import fnmatch
import uuid
from pathlib import Path

class FileProcessor:
    def __init__(self, folder_path=None):
        self.folder_path = folder_path
        self.gitignore_patterns = []
        self.load_gitignore()
        
    def load_gitignore(self):
        """Load patterns from .gitignore if exists"""
        if not self.folder_path:
            return
        
        gitignore_path = os.path.join(self.folder_path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.gitignore_patterns.append(line)
    
    def should_ignore(self, path):
        """Check if path should be ignored based on .gitignore patterns"""
        rel_path = os.path.relpath(path, self.folder_path)
        for pattern in self.gitignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False
    
    def process_folder(self, selected_paths=None):
        """Process the folder into a JSON structure"""
        if not self.folder_path or not os.path.exists(self.folder_path):
            return {"error": "Invalid folder path"}
        
        return self._process_directory(self.folder_path, selected_paths)
    
    # def _process_directory(self, directory, selected_paths=None, base_path=None):
    #     """Recursively process a directory and its contents"""
    #     if base_path is None:
    #         base_path = directory
        
    #     result = {
    #         "name": os.path.basename(directory),
    #         "type": "directory",
    #         "path": os.path.relpath(directory, base_path),
    #         "children": []
    #     }
        
    #     try:
    #         for item in os.listdir(directory):
    #             full_path = os.path.join(directory, item)
                
    #             # Skip if path should be ignored
    #             if self.should_ignore(full_path):
    #                 continue
                
    #             # Skip if not in selected paths (if provided)
    #             rel_path = os.path.relpath(full_path, self.folder_path)
    #             if selected_paths and rel_path not in selected_paths:
    #                 continue
                
    #             if os.path.isdir(full_path):
    #                 child = self._process_directory(full_path, selected_paths, base_path)
    #                 result["children"].append(child)
    #             else:
    #                 # Process file
    #                 file_content = ""
    #                 try:
    #                     with open(full_path, 'r', encoding='utf-8') as f:
    #                         file_content = f.read()
    #                 except Exception as e:
    #                     file_content = f"Error reading file: {str(e)}"
                    
    #                 result["children"].append({
    #                     "name": item,
    #                     "type": "file",
    #                     "path": os.path.relpath(full_path, base_path),
    #                     "content": file_content
    #                 })
    #     except Exception as e:
    #         result["error"] = str(e)
        
    #     return result


    def _process_directory(self, directory, selected_paths=None, base_path=None):
        """Recursively process a directory and its contents"""
        if base_path is None:
            base_path = directory
        
        result = {
            "name": os.path.basename(directory),
            "type": "directory",
            "path": os.path.relpath(directory, base_path),
            "children": []
        }
        
        try:
            items = os.listdir(directory)
            for item in sorted(items):  # Sort items for consistent ordering
                full_path = os.path.join(directory, item)
                
                if self.should_ignore(full_path):
                    continue
                    
                rel_path = os.path.relpath(full_path, self.folder_path)
                if selected_paths and rel_path not in selected_paths:
                    continue
                    
                if os.path.isdir(full_path):
                    child = self._process_directory(full_path, selected_paths, base_path)
                    result["children"].append(child)
                else:
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                    except Exception as e:
                        file_content = f"Error reading file: {str(e)}"
                    
                    result["children"].append({
                        "name": item,
                        "type": "file",
                        "path": rel_path,
                        "content": file_content
                    })
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def save_temp_file(self, uploaded_file):
        """Save uploaded file to temporary directory and extract if needed"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # If it's a zip file, extract it
            if uploaded_file.name.endswith('.zip'):
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    extract_dir = os.path.join(temp_dir, 'extracted')
                    os.makedirs(extract_dir, exist_ok=True)
                    zip_ref.extractall(extract_dir)
                self.folder_path = extract_dir
            else:
                self.folder_path = temp_dir
            
            self.load_gitignore()
            return self.folder_path
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise e
        
        