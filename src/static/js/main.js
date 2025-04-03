document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('cv-file');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const uploadButton = document.getElementById('upload-button');
    const uploadForm = document.getElementById('cv-upload-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Only proceed if we're on the upload page
    if (uploadArea && fileInput) {
        // Handle drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadArea.classList.add('dragover');
        }
        
        function unhighlight() {
            uploadArea.classList.remove('dragover');
        }
        
        // Handle file drop
        uploadArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length) {
                fileInput.files = files;
                updateFileInfo();
            }
        }
        
        // Handle file selection via click
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', updateFileInfo);
        
        function updateFileInfo() {
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                
                // Check file extension
                const fileExtension = file.name.split('.').pop().toLowerCase();
                
                if (['pdf', 'docx'].includes(fileExtension)) {
                    fileName.textContent = file.name;
                    uploadArea.classList.add('d-none');
                    fileInfo.classList.remove('d-none');
                    uploadButton.disabled = false;
                    
                    // Show file size
                    const fileSize = formatFileSize(file.size);
                    fileName.textContent = `${file.name} (${fileSize})`;
                    
                    // Check if file is too large (16MB limit)
                    if (file.size > 16 * 1024 * 1024) {
                        showToast('File is too large. Maximum size is 16MB.', 'danger');
                        resetFileUpload();
                    }
                } else {
                    showToast('Invalid file type. Please upload a PDF or DOCX file.', 'danger');
                    resetFileUpload();
                }
            }
        }
        
        // Handle file removal
        removeFileBtn.addEventListener('click', resetFileUpload);
        
        function resetFileUpload() {
            fileInput.value = '';
            uploadArea.classList.remove('d-none');
            fileInfo.classList.add('d-none');
            uploadButton.disabled = true;
        }
        
        // Show loading overlay when form is submitted
        uploadForm.addEventListener('submit', function() {
            if (fileInput.files.length > 0) {
                loadingOverlay.classList.remove('d-none');
            }
        });
    }
    
    // Format file size in KB, MB
    function formatFileSize(bytes) {
        if (bytes < 1024) {
            return bytes + ' bytes';
        } else if (bytes < 1024 * 1024) {
            return (bytes / 1024).toFixed(1) + ' KB';
        } else {
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
    }
    
    // Toast notification function
    function showToast(message, type = 'info') {
        const toastContainer = document.createElement('div');
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1050';
        
        const toastElement = document.createElement('div');
        toastElement.className = `toast show bg-${type === 'danger' ? 'danger' : 'primary'} text-white`;
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');
        
        const toastBody = document.createElement('div');
        toastBody.className = 'toast-body d-flex';
        
        const icon = document.createElement('i');
        icon.className = `fas fa-${type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2`;
        
        const textElement = document.createElement('div');
        textElement.textContent = message;
        
        toastBody.appendChild(icon);
        toastBody.appendChild(textElement);
        toastElement.appendChild(toastBody);
        toastContainer.appendChild(toastElement);
        
        document.body.appendChild(toastContainer);
        
        setTimeout(() => {
            toastContainer.remove();
        }, 5000);
    }
    
    // Initialize any Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
