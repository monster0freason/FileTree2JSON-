// Main JavaScript file

// Function to toggle folder children
function toggleFolder(checkbox) {
    const parentItem = checkbox.closest('.tree-item');
    const folderContent = parentItem.nextElementSibling;
    
    if (folderContent && folderContent.classList.contains('nested')) {
        const childCheckboxes = folderContent.querySelectorAll('input[type="checkbox"]');
        childCheckboxes.forEach(function(cb) {
            cb.checked = checkbox.checked;
        });
    }
}

// Functions for copying and downloading JSON
function copyJsonToClipboard() {
    const jsonContent = document.getElementById('json-content').textContent;
    navigator.clipboard.writeText(jsonContent).then(function() {
        alert('JSON copied to clipboard!');
    }, function(err) {
        console.error('Could not copy JSON: ', err);
    });
}

function downloadJson() {
    const jsonContent = document.getElementById('json-content').textContent;
    const element = document.createElement('a');
    const file = new Blob([jsonContent], {type: 'application/json'});
    element.href = URL.createObjectURL(file);
    element.download = 'file_structure.json';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('structure-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Validate that at least one checkbox is selected
            const checkboxes = form.querySelectorAll('input[name="selected_paths"]:checked');
            if (checkboxes.length === 0) {
                e.preventDefault();
                alert('Please select at least one file or folder.');
            }
        });
    }
});