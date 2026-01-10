/**
 * Resume Builder JavaScript
 * Handles interactive functionality for the Resume & Cover Letter Builder
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Resume Builder functionality
    initializeResumeBuilder();
    
    function initializeResumeBuilder() {
        // Template selection functionality
        initializeTemplateSelection();
        
        // Form handling
        initializeFormHandling();
        
        // Live preview functionality
        initializeLivePreview();
        
        // Section management
        initializeSectionManagement();
        
        // Auto-save functionality
        initializeAutoSave();
        
        // Print functionality
        initializePrintHandling();
    }
    
    /**
     * Template Selection
     */
    function initializeTemplateSelection() {
        const templateCards = document.querySelectorAll('.template-card');
        
        templateCards.forEach(card => {
            card.addEventListener('click', function() {
                // Remove active class from all cards
                templateCards.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked card
                this.classList.add('active');
                
                // Update preview if available
                const templateId = this.dataset.templateId;
                if (templateId) {
                    updateTemplatePreview(templateId);
                }
            });
            
            // Hover effects
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
    
    /**
     * Form Handling
     */
    function initializeFormHandling() {
        const forms = document.querySelectorAll('.resume-form, .cover-letter-form');
        
        forms.forEach(form => {
            // Add loading states
            form.addEventListener('submit', function() {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
                }
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', validateField);
                input.addEventListener('input', clearFieldError);
            });
        });
    }
    
    /**
     * Live Preview
     */
    function initializeLivePreview() {
        const previewContainer = document.getElementById('live-preview');
        if (!previewContainer) return;
        
        const formInputs = document.querySelectorAll('.resume-form input, .resume-form textarea');
        
        formInputs.forEach(input => {
            input.addEventListener('input', debounce(updateLivePreview, 500));
        });
    }
    
    function updateLivePreview() {
        const previewContainer = document.getElementById('live-preview');
        if (!previewContainer) return;
        
        // Collect form data
        const formData = collectFormData();
        
        // Update preview content
        updatePreviewContent(formData);
    }
    
    /**
     * Section Management
     */
    function initializeSectionManagement() {
        // Add section buttons
        const addSectionBtns = document.querySelectorAll('.add-section-btn');
        addSectionBtns.forEach(btn => {
            btn.addEventListener('click', addSection);
        });
        
        // Remove section buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-section-btn')) {
                removeSection(e.target);
            }
        });
        
        // Drag and drop for section reordering
        initializeSectionReordering();
    }
    
    function addSection(e) {
        const sectionType = e.target.dataset.sectionType;
        const container = document.getElementById(`${sectionType}-container`);
        
        if (!container) return;
        
        const template = document.getElementById(`${sectionType}-template`);
        if (!template) return;
        
        const newSection = template.content.cloneNode(true);
        
        // Update field names with unique indices
        const index = container.children.length;
        updateFieldNames(newSection, sectionType, index);
        
        container.appendChild(newSection);
        
        // Add animation
        const addedSection = container.lastElementChild;
        addedSection.style.opacity = '0';
        addedSection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            addedSection.style.transition = 'all 0.3s ease';
            addedSection.style.opacity = '1';
            addedSection.style.transform = 'translateY(0)';
        }, 10);
    }
    
    function removeSection(btn) {
        const section = btn.closest('.section-item');
        if (!section) return;
        
        // Add animation
        section.style.transition = 'all 0.3s ease';
        section.style.opacity = '0';
        section.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            section.remove();
        }, 300);
    }
    
    /**
     * Auto-save functionality
     */
    function initializeAutoSave() {
        const form = document.querySelector('.resume-form, .cover-letter-form');
        if (!form) return;
        
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', debounce(autoSave, 2000));
        });
    }
    
    function autoSave() {
        const form = document.querySelector('.resume-form, .cover-letter-form');
        if (!form) return;
        
        const formData = new FormData(form);
        const url = form.dataset.autoSaveUrl;
        
        if (!url) return;
        
        // Show saving indicator
        showSavingIndicator();
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSavedIndicator();
            } else {
                showSaveError();
            }
        })
        .catch(error => {
            console.error('Auto-save error:', error);
            showSaveError();
        });
    }
    
    /**
     * Print Handling
     */
    function initializePrintHandling() {
        const printBtns = document.querySelectorAll('.print-btn');
        
        printBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                window.print();
            });
        });
        
        // Download buttons
        const downloadBtns = document.querySelectorAll('.download-btn');
        
        downloadBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const format = this.dataset.format || 'pdf';
                const documentId = this.dataset.documentId;
                const documentType = this.dataset.documentType;
                
                if (documentId && documentType) {
                    downloadDocument(documentId, documentType, format);
                }
            });
        });
    }
    
    /**
     * Utility Functions
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        // Clear previous errors
        clearFieldError(e);
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            showFieldError(field, 'This field is required');
            return false;
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                showFieldError(field, 'Please enter a valid email address');
                return false;
            }
        }
        
        // Phone validation
        if (field.name === 'phone' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                showFieldError(field, 'Please enter a valid phone number');
                return false;
            }
        }
        
        return true;
    }
    
    function showFieldError(field, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        
        field.classList.add('error');
        field.parentNode.appendChild(errorDiv);
    }
    
    function clearFieldError(e) {
        const field = e.target;
        field.classList.remove('error');
        
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    function collectFormData() {
        const form = document.querySelector('.resume-form, .cover-letter-form');
        if (!form) return {};
        
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    function updatePreviewContent(data) {
        // Update preview elements based on form data
        const previewElements = {
            'full_name': '.preview-name',
            'email': '.preview-email',
            'phone': '.preview-phone',
            'location': '.preview-location',
            'summary': '.preview-summary'
        };
        
        Object.entries(previewElements).forEach(([field, selector]) => {
            const element = document.querySelector(selector);
            if (element && data[field]) {
                element.textContent = data[field];
            }
        });
    }
    
    function updateFieldNames(element, sectionType, index) {
        const inputs = element.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            const name = input.name;
            if (name) {
                input.name = `${sectionType}_${index}_${name}`;
                input.id = `${sectionType}_${index}_${name}`;
            }
        });
        
        const labels = element.querySelectorAll('label');
        labels.forEach(label => {
            const forAttr = label.getAttribute('for');
            if (forAttr) {
                label.setAttribute('for', `${sectionType}_${index}_${forAttr}`);
            }
        });
    }
    
    function initializeSectionReordering() {
        const containers = document.querySelectorAll('.sortable-container');
        
        containers.forEach(container => {
            // Simple drag and drop implementation
            let draggedElement = null;
            
            container.addEventListener('dragstart', function(e) {
                draggedElement = e.target.closest('.section-item');
                e.target.style.opacity = '0.5';
            });
            
            container.addEventListener('dragend', function(e) {
                e.target.style.opacity = '';
                draggedElement = null;
            });
            
            container.addEventListener('dragover', function(e) {
                e.preventDefault();
            });
            
            container.addEventListener('drop', function(e) {
                e.preventDefault();
                
                if (draggedElement) {
                    const afterElement = getDragAfterElement(container, e.clientY);
                    
                    if (afterElement == null) {
                        container.appendChild(draggedElement);
                    } else {
                        container.insertBefore(draggedElement, afterElement);
                    }
                }
            });
        });
    }
    
    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.section-item:not(.dragging)')];
        
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
    
    function showSavingIndicator() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.textContent = 'Saving...';
            indicator.className = 'save-indicator saving';
        }
    }
    
    function showSavedIndicator() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.textContent = 'Saved';
            indicator.className = 'save-indicator saved';
            
            setTimeout(() => {
                indicator.className = 'save-indicator';
            }, 2000);
        }
    }
    
    function showSaveError() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.textContent = 'Save failed';
            indicator.className = 'save-indicator error';
            
            setTimeout(() => {
                indicator.className = 'save-indicator';
            }, 3000);
        }
    }
    
    function updateTemplatePreview(templateId) {
        const previewContainer = document.getElementById('template-preview');
        if (!previewContainer) return;
        
        // Show loading state
        previewContainer.innerHTML = '<div class="loading">Loading preview...</div>';
        
        // Fetch template preview
        fetch(`/resume-builder/api/template-preview/${templateId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    previewContainer.innerHTML = data.html;
                } else {
                    previewContainer.innerHTML = '<div class="error">Preview not available</div>';
                }
            })
            .catch(error => {
                console.error('Template preview error:', error);
                previewContainer.innerHTML = '<div class="error">Preview not available</div>';
            });
    }
    
    function downloadDocument(documentId, documentType, format) {
        const url = `/resume-builder/api/download/${documentType}/${documentId}/${format}/`;
        
        // Create temporary link and trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = '';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    function getCsrfToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
    
    // Export functions for external use
    window.ResumeBuilder = {
        updatePreview: updateLivePreview,
        validateForm: function() {
            const form = document.querySelector('.resume-form, .cover-letter-form');
            if (!form) return true;
            
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField({ target: input })) {
                    isValid = false;
                }
            });
            
            return isValid;
        },
        autoSave: autoSave
    };
});