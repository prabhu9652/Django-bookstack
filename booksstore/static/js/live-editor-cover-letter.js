/**
 * Live Cover Letter Editor
 * Real-time editing with live preview functionality
 */

class CoverLetterEditor {
  constructor(options) {
    this.coverLetterId = options.coverLetterId;
    this.templateId = options.templateId;
    this.autoSave = options.autoSave || true;
    this.autoSaveInterval = options.autoSaveInterval || 2000;
    this.autoSaveTimer = null;
    this.isModified = false;
    this.zoomLevel = 100;
    
    this.init();
  }
  
  init() {
    this.setupEventListeners();
    this.setupSectionToggles();
    this.setupContentStats();
    this.setupAutoSave();
    this.setupPreviewControls();
    this.updatePreview();
    
    console.log('Cover Letter Editor initialized');
  }
  
  setupEventListeners() {
    const form = document.getElementById('coverLetterForm');
    if (!form) return;
    
    // Listen for all form changes
    form.addEventListener('input', (e) => {
      this.handleFormChange(e);
    });
    
    form.addEventListener('change', (e) => {
      this.handleFormChange(e);
    });
    
    // Save button
    const saveBtn = document.getElementById('saveCoverLetter');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        this.saveCoverLetter();
      });
    }
    
    // Auto-save toggle
    const autoSaveToggle = document.getElementById('autoSaveToggle');
    if (autoSaveToggle) {
      autoSaveToggle.addEventListener('click', () => {
        this.toggleAutoSave();
      });
    }
    
    // Collapse all sections
    const collapseBtn = document.getElementById('collapseAllSections');
    if (collapseBtn) {
      collapseBtn.addEventListener('click', () => {
        this.collapseAllSections();
      });
    }
  }
  
  setupSectionToggles() {
    const toggles = document.querySelectorAll('.section-toggle');
    toggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const section = toggle.closest('.form-section');
        section.classList.toggle('collapsed');
      });
    });
    
    // Make section headers clickable
    const headers = document.querySelectorAll('.section-header');
    headers.forEach(header => {
      header.addEventListener('click', (e) => {
        if (e.target.closest('.section-actions')) return;
        const toggle = header.querySelector('.section-toggle');
        if (toggle) toggle.click();
      });
    });
  }
  
  setupContentStats() {
    const contentTextarea = document.getElementById('content');
    const charCount = document.querySelector('.char-count');
    const wordCount = document.querySelector('.word-count');
    
    if (!contentTextarea || !charCount || !wordCount) return;
    
    const updateStats = () => {
      const text = contentTextarea.value;
      const chars = text.length;
      const words = text.trim() ? text.trim().split(/\s+/).length : 0;
      
      charCount.textContent = `${chars} characters`;
      wordCount.textContent = `${words} words`;
      
      // Color coding for length
      if (chars < 200) {
        charCount.style.color = 'var(--error)';
      } else if (chars > 2000) {
        charCount.style.color = 'var(--warning)';
      } else {
        charCount.style.color = 'var(--text-tertiary)';
      }
    };
    
    contentTextarea.addEventListener('input', updateStats);
    updateStats(); // Initial update
  }
  
  setupAutoSave() {
    if (!this.autoSave) return;
    
    // Start auto-save timer
    this.startAutoSaveTimer();
  }
  
  setupPreviewControls() {
    const zoomIn = document.getElementById('zoomIn');
    const zoomOut = document.getElementById('zoomOut');
    const fullscreen = document.getElementById('fullscreenPreview');
    
    if (zoomIn) {
      zoomIn.addEventListener('click', () => {
        this.zoomPreview(10);
      });
    }
    
    if (zoomOut) {
      zoomOut.addEventListener('click', () => {
        this.zoomPreview(-10);
      });
    }
    
    if (fullscreen) {
      fullscreen.addEventListener('click', () => {
        this.toggleFullscreenPreview();
      });
    }
  }
  
  handleFormChange(e) {
    this.isModified = true;
    this.updatePreview();
    
    if (this.autoSave) {
      this.startAutoSaveTimer();
    }
    
    this.updateSaveStatus('modified');
  }
  
  updatePreview() {
    const previewContainer = document.getElementById('coverLetterPreview');
    if (!previewContainer) return;
    
    const formData = this.getFormData();
    const previewHTML = this.generatePreviewHTML(formData);
    
    previewContainer.innerHTML = previewHTML;
  }
  
  getFormData() {
    const form = document.getElementById('coverLetterForm');
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    
    // Basic fields
    for (let [key, value] of formData.entries()) {
      data[key] = value;
    }
    
    return data;
  }
  
  generatePreviewHTML(data) {
    const fullName = data.full_name || 'Your Name';
    const email = data.email || 'your.email@example.com';
    const phone = data.phone || '';
    const location = data.location || '';
    const companyName = data.company_name || 'Company Name';
    const positionTitle = data.position_title || 'Position Title';
    const hiringManager = data.hiring_manager || '';
    const content = data.content || '';
    
    // Format current date
    const currentDate = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    
    let contactInfo = [];
    if (email) contactInfo.push(email);
    if (phone) contactInfo.push(phone);
    if (location) contactInfo.push(location);
    
    // Format content with proper line breaks
    const formattedContent = content.replace(/\n/g, '</p><p>');
    
    let html = `
      <div class="cover-letter-header">
        <h1>${fullName}</h1>
        <div class="contact-info">
          ${contactInfo.map(info => `<p>${info}</p>`).join('')}
        </div>
      </div>
      
      <div class="letter-date">
        <p>${currentDate}</p>
      </div>
      
      <div class="recipient-info">
        ${hiringManager ? `<p>${hiringManager}</p>` : ''}
        <p>${companyName}</p>
      </div>
      
      <div class="letter-content">
        <p>${formattedContent}</p>
      </div>
      
      <div class="letter-closing">
        <p>Sincerely,</p>
        <br>
        <p>${fullName}</p>
      </div>
    `;
    
    return html;
  }
  
  startAutoSaveTimer() {
    if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }
    
    this.autoSaveTimer = setTimeout(() => {
      if (this.isModified) {
        this.saveCoverLetter(true);
      }
    }, this.autoSaveInterval);
  }
  
  async saveCoverLetter(isAutoSave = false) {
    if (!this.isModified && isAutoSave) return;
    
    const formData = this.getFormData();
    
    this.updateSaveStatus('saving');
    
    try {
      const response = await fetch(`/resume-builder/api/save-cover-letter/${this.coverLetterId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        this.isModified = false;
        this.updateSaveStatus('saved');
        if (!isAutoSave) {
          this.showMessage('Cover letter saved successfully!', 'success');
        }
      } else {
        throw new Error('Save failed');
      }
    } catch (error) {
      console.error('Save error:', error);
      this.updateSaveStatus('error');
      this.showMessage('Failed to save cover letter. Please try again.', 'error');
    }
  }
  
  toggleAutoSave() {
    this.autoSave = !this.autoSave;
    const toggle = document.getElementById('autoSaveToggle');
    const status = document.getElementById('autoSaveStatus');
    
    if (toggle && status) {
      status.textContent = `Auto-save: ${this.autoSave ? 'On' : 'Off'}`;
      toggle.classList.toggle('active', this.autoSave);
    }
    
    if (this.autoSave) {
      this.startAutoSaveTimer();
    } else if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }
  }
  
  collapseAllSections() {
    const sections = document.querySelectorAll('.form-section');
    const isAnyExpanded = Array.from(sections).some(section => !section.classList.contains('collapsed'));
    
    sections.forEach(section => {
      if (isAnyExpanded) {
        section.classList.add('collapsed');
      } else {
        section.classList.remove('collapsed');
      }
    });
    
    const btn = document.getElementById('collapseAllSections');
    if (btn) {
      const icon = btn.querySelector('i');
      const text = btn.querySelector('span') || btn;
      if (isAnyExpanded) {
        icon.className = 'fas fa-expand-alt';
        text.textContent = 'Expand All';
      } else {
        icon.className = 'fas fa-compress-alt';
        text.textContent = 'Collapse All';
      }
    }
  }
  
  zoomPreview(delta) {
    this.zoomLevel = Math.max(50, Math.min(150, this.zoomLevel + delta));
    
    const preview = document.getElementById('coverLetterPreview');
    const zoomDisplay = document.querySelector('.zoom-level');
    
    if (preview) {
      preview.className = 'preview-document';
      if (this.zoomLevel !== 100) {
        preview.classList.add(`zoom-${this.zoomLevel}`);
      }
    }
    
    if (zoomDisplay) {
      zoomDisplay.textContent = `${this.zoomLevel}%`;
    }
  }
  
  toggleFullscreenPreview() {
    const previewPanel = document.querySelector('.preview-panel');
    if (previewPanel) {
      previewPanel.classList.toggle('fullscreen');
    }
  }
  
  updateSaveStatus(status) {
    const saveStatus = document.getElementById('saveStatus');
    if (!saveStatus) return;
    
    const icon = saveStatus.querySelector('i');
    const text = saveStatus.querySelector('span');
    
    saveStatus.className = 'save-status';
    
    switch (status) {
      case 'saving':
        saveStatus.classList.add('show', 'saving');
        icon.className = 'fas fa-spinner fa-spin';
        text.textContent = 'Saving...';
        break;
      case 'saved':
        saveStatus.classList.add('show');
        icon.className = 'fas fa-check-circle';
        text.textContent = 'All changes saved';
        setTimeout(() => {
          saveStatus.classList.remove('show');
        }, 2000);
        break;
      case 'error':
        saveStatus.classList.add('show', 'error');
        icon.className = 'fas fa-exclamation-triangle';
        text.textContent = 'Save failed';
        setTimeout(() => {
          saveStatus.classList.remove('show');
        }, 3000);
        break;
      case 'modified':
        // Don't show status for modifications
        break;
    }
  }
  
  showMessage(message, type = 'info') {
    // Create or update a message element
    let messageEl = document.getElementById('editorMessage');
    if (!messageEl) {
      messageEl = document.createElement('div');
      messageEl.id = 'editorMessage';
      messageEl.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 12px 16px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
      `;
      document.body.appendChild(messageEl);
    }
    
    messageEl.textContent = message;
    messageEl.className = `message-${type}`;
    
    // Set background color based on type
    const colors = {
      success: '#22c55e',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    };
    messageEl.style.backgroundColor = colors[type] || colors.info;
    
    // Show message
    setTimeout(() => {
      messageEl.style.transform = 'translateX(0)';
    }, 10);
    
    // Hide message
    setTimeout(() => {
      messageEl.style.transform = 'translateX(100%)';
    }, 3000);
  }
  
  getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                  document.querySelector('meta[name=csrf-token]')?.content;
    return token || '';
  }
}

// Additional CSS for cover letter preview
const coverLetterCSS = `
.cover-letter-header {
  text-align: left;
  margin-bottom: 32px;
}

.cover-letter-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
}

.cover-letter-header .contact-info p {
  margin: 2px 0;
  color: #4a5568;
  font-size: 14px;
}

.letter-date {
  margin-bottom: 24px;
}

.letter-date p {
  color: #4a5568;
  font-size: 14px;
}

.recipient-info {
  margin-bottom: 24px;
}

.recipient-info p {
  margin: 4px 0;
  color: #2d3748;
  font-weight: 500;
}

.letter-content {
  margin-bottom: 32px;
  line-height: 1.7;
}

.letter-content p {
  margin-bottom: 16px;
  color: #4a5568;
  text-align: justify;
}

.letter-closing {
  margin-top: 32px;
}

.letter-closing p {
  color: #2d3748;
  font-weight: 500;
}

.content-stats {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  font-size: 12px;
}

.char-count,
.word-count {
  color: var(--text-tertiary);
}
`;

// Inject cover letter specific CSS
const style = document.createElement('style');
style.textContent = coverLetterCSS;
document.head.appendChild(style);