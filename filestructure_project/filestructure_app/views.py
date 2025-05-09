# filestructure_app/views.py
import os
import json
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .services.file_processor import FileProcessor
from .services.github_service import GitHubService
from .models import ProcessedFile

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def process_files(request):
    if request.method == 'POST':
        session_id = str(uuid.uuid4())
        
        try:
            folder_path = None
            processor = FileProcessor()
            
            # Check if a file was uploaded
            if 'folder' in request.FILES:
                uploaded_file = request.FILES['folder']
                
                # Only accept zip files
                if not uploaded_file.name.endswith('.zip'):
                    messages.error(request, "Only .zip files are supported. Please upload a zip archive.")
                    return redirect('home')
                
                folder_path = processor.save_temp_file(uploaded_file)

            
            # Check if a GitHub URL was provided
            elif 'github_url' in request.POST and request.POST['github_url']:
                github_service = GitHubService()
                folder_path, error = github_service.download_repository(request.POST['github_url'])
                if error:
                    messages.error(request, f"GitHub Error: {error}")
                    return redirect('home')
                
                processor.folder_path = folder_path
                processor.load_gitignore()
            
            if not folder_path:
                messages.error(request, "Please upload a file or provide a GitHub URL.")
                return redirect('home')
            
            # First pass: get the directory structure (without file contents)
            structure = processor.process_folder()
            
            # Store the session ID and file path
            request.session['folder_path'] = folder_path
            request.session['session_id'] = session_id
            
            # Redirect to result page
            return redirect('result', session_id=session_id)
        
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('home')
    
    return redirect('home')

# filestructure_app/views.py - updated result function

# def result(request, session_id):
#     try:
#         folder_path = request.session.get('folder_path')
        
#         if not folder_path or not os.path.exists(folder_path):
#             messages.error(request, "Session expired or folder not found.")
#             return redirect('home')
        
#         # Process the folder structure (without file contents initially)
#         processor = FileProcessor(folder_path)
#         structure = processor.process_folder()
        
#         # If form was submitted with selected paths
#         if request.method == 'POST':
#             selected_paths = request.POST.getlist('selected_paths')
            
#             # Process only selected paths with content
#             full_structure = processor.process_folder(selected_paths)
            
#             # Save to database
#             processed_file = ProcessedFile.objects.create(
#                 session_id=session_id,
#                 json_data=full_structure
#             )
            
#             # Return JSON response
#             return render(request, 'result.html', {
#                 'session_id': session_id,
#                 'structure': json.dumps(structure),  # Serialized structure
#                 'json_data': json.dumps(full_structure, indent=2),
#                 'selected_paths': selected_paths
#             })
        
#         return render(request, 'result.html', {
#             'session_id': session_id,
#             'structure': json.dumps(structure),  # Serialized structure
#             'json_data': None,
#             'selected_paths': []
#         })
    
#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")


def result(request, session_id):
    try:
        folder_path = request.session.get('folder_path')
        
        if not folder_path or not os.path.exists(folder_path):
            messages.error(request, "Session expired or folder not found.")
            return redirect('home')
        
        # Process the folder structure (without file contents initially)
        processor = FileProcessor(folder_path)
        structure = processor.process_folder()
        
        # If form was submitted with selected paths
        if request.method == 'POST':
            selected_paths = request.POST.getlist('selected_paths')
            
            # Process only selected paths with content
            full_structure = processor.process_folder(selected_paths)
            
            # Save to database
            processed_file = ProcessedFile.objects.create(
                session_id=session_id,
                json_data=full_structure
            )
            
            # Return JSON response
            return render(request, 'result.html', {
                'session_id': session_id,
                'structure': json.dumps(structure),  # Serialized structure
                'json_data': json.dumps(full_structure, indent=2),
                'selected_paths': selected_paths
            })
        
        return render(request, 'result.html', {
            'session_id': session_id,
            'structure': json.dumps(structure),  # Serialized structure
            'json_data': None,
            'selected_paths': []
        })
    
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('home')