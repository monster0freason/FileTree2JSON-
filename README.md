# FileTree2JSON

A powerful Django web application that converts file structures into JSON format with an intuitive user interface. Easily process local folders or GitHub repositories and get a structured JSON representation with minimal effort.

## 🌟 Features

- **Multiple Source Options**: Upload local folders, zip files, or provide GitHub repository URLs
- **Smart Filtering**: Automatically respects `.gitignore` rules to exclude unnecessary files
- **Interactive Selection**: Choose exactly which files and folders to include in your JSON output
- **Folder Hierarchy**: Select a folder to automatically include all its contents (with the option to deselect specific items)
- **Complete Content**: Captures both file structure and file contents in a clean JSON format
- **Easy Export**: Copy to clipboard or download the generated JSON with one click
- **Elegant UI**: Clean, responsive design with drag-and-drop support

## 📋 Use Cases

- Extract code for documentation or analysis
- Create code samples from repositories
- Generate structured data for project visualization
- Prepare codebases for processing by other tools
- Archive project structures with content
- Share code snippets with structure intact

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/filetree2json.git
cd filetree2json
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

6. Visit http://127.0.0.1:8000/ in your browser

## 🧰 Usage

### Processing Local Files

1. Click on the upload area or drag & drop a folder/zip file
2. When the file structure loads, select the files you want to include
   - Use the "Select All" button to include everything
   - Use checkboxes to select/deselect specific items
3. Click "Generate JSON"
4. Use the "Copy" or "Download" buttons to save your JSON

### Processing GitHub Repositories

1. Enter a GitHub repository URL (e.g., https://github.com/username/repository)
2. Click "Process Files"
3. Select the files you want to include in the JSON output
4. Click "Generate JSON"
5. Copy or download the generated JSON

## 🔧 Configuration

All configuration is handled through the Django settings. Key settings you might want to modify:

- `MEDIA_ROOT`: Location for temporary file storage
- `MAX_UPLOAD_SIZE`: Maximum file size for uploads (default: 50MB)

## 🔒 Security Notes

- Temporary files are automatically cleaned up after processing
- GitHub API requests are rate-limited, so heavy usage may require authentication
- No file content is stored permanently unless explicitly saved by the user

## 🧪 Development

### Project Structure

```
filestructure_project/
├── filestructure_project/      # Project settings
├── filestructure_app/          # Main application
│   ├── services/              # Core processing logic
│   │   ├── file_processor.py  # File handling
│   │   └── github_service.py  # GitHub integration
│   ├── templates/             # HTML templates
│   ├── static/                # CSS and JavaScript
│   ├── views.py               # View controllers
│   └── models.py              # Data models
└── manage.py                  # Django management script
```

### Running Tests

```bash
python manage.py test filestructure_app
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any problems or have feature requests, please open an issue on GitHub.
