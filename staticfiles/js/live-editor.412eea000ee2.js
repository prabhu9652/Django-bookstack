/**
 * Live Resume Editor
 * Real-time editing with live preview functionality
 */

class ResumeEditor {
  constructor(options) {
    this.resumeId = options.resumeId;
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
    this.setupSkillsManager();
    this.setupExperienceManager();
    this.setupEducationManager();
    this.setupAutoSave();
    this.setupPreviewControls();
    this.updatePreview();
    
    console.log('Resume Editor initialized');
  }
  
  setupEventListeners() {
    const form = document.getElementById('resumeForm');
    if (!form) return;
    
    // Listen for all form changes
    form.addEventListener('input', (e) => {
      this.handleFormChange(e);
    });
    
    form.addEventListener('change', (e) => {
      this.handleFormChange(e);
    });
    
    // Save button
    const saveBtn = document.getElementById('saveResume');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        this.saveResume();
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
  
  setupSkillsManager() {
    const skillInput = document.getElementById('skillInput');
    const addSkillBtn = document.getElementById('addSkill');
    const skillsList = document.getElementById('skillsList');
    
    if (!skillInput || !addSkillBtn || !skillsList) return;
    
    // Add skill on button click
    addSkillBtn.addEventListener('click', () => {
      this.addSkill();
    });
    
    // Add skill on Enter key
    skillInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        this.addSkill();
      }
    });
    
    // Remove skill handlers
    skillsList.addEventListener('click', (e) => {
      if (e.target.closest('.remove-skill')) {
        const skillTag = e.target.closest('.skill-tag');
        this.removeSkill(skillTag);
      }
    });
  }
  
  setupExperienceManager() {
    const addBtn = document.getElementById('addExperience');
    const container = document.getElementById('experienceContainer');
    
    if (!addBtn || !container) return;
    
    addBtn.addEventListener('click', () => {
      this.addExperience();
    });
    
    container.addEventListener('click', (e) => {
      if (e.target.closest('.remove-item')) {
        const item = e.target.closest('.experience-item');
        this.removeExperience(item);
      }
    });
  }
  
  setupEducationManager() {
    const addBtn = document.getElementById('addEducation');
    const container = document.getElementById('educationContainer');
    
    if (!addBtn || !container) return;
    
    addBtn.addEventListener('click', () => {
      this.addEducation();
    });
    
    container.addEventListener('click', (e) => {
      if (e.target.closest('.remove-item')) {
        const item = e.target.closest('.education-item');
        this.removeEducation(item);
      }
    });
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
  
  addSkill() {
    const skillInput = document.getElementById('skillInput');
    const skillsList = document.getElementById('skillsList');
    
    if (!skillInput || !skillsList) return;
    
    const skillText = skillInput.value.trim();
    if (!skillText) return;
    
    // Check if skill already exists
    const existingSkills = Array.from(skillsList.querySelectorAll('.skill-tag span'))
      .map(span => span.textContent.toLowerCase());
    
    if (existingSkills.includes(skillText.toLowerCase())) {
      this.showMessage('Skill already added', 'warning');
      return;
    }
    
    // Create skill tag
    const skillTag = document.createElement('div');
    skillTag.className = 'skill-tag';
    skillTag.innerHTML = `
      <span>${skillText}</span>
      <button type="button" class="remove-skill">
        <i class="fas fa-times"></i>
      </button>
    `;
    
    skillsList.appendChild(skillTag);
    skillInput.value = '';
    
    this.handleFormChange();
  }
  
  removeSkill(skillTag) {
    skillTag.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => {
      skillTag.remove();
      this.handleFormChange();
    }, 300);
  }
  
  addExperience() {
    const container = document.getElementById('experienceContainer');
    if (!container) return;
    
    const index = container.children.length;
    const experienceItem = document.createElement('div');
    experienceItem.className = 'experience-item';
    experienceItem.dataset.index = index;
    
    experienceItem.innerHTML = `
      <div class="item-header">
        <h4>Experience ${index + 1}</h4>
        <button type="button" class="remove-item">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label>Job Title *</label>
          <input type="text" name="exp_title" required>
        </div>
        <div class="form-group">
          <label>Company *</label>
          <input type="text" name="exp_company" required>
        </div>
        <div class="form-group">
          <label>Location</label>
          <input type="text" name="exp_location">
        </div>
        <div class="form-group">
          <label>Start Date</label>
          <input type="text" name="exp_start_date" placeholder="e.g., Jan 2023">
        </div>
        <div class="form-group">
          <label>End Date</label>
          <input type="text" name="exp_end_date" placeholder="e.g., Present">
        </div>
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea name="exp_description" rows="3" placeholder="Describe your key responsibilities and achievements..."></textarea>
      </div>
    `;
    
    container.appendChild(experienceItem);
    
    // Focus on the first input
    const firstInput = experienceItem.querySelector('input');
    if (firstInput) firstInput.focus();
    
    this.handleFormChange();
  }
  
  removeExperience(item) {
    item.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => {
      item.remove();
      this.updateExperienceNumbers();
      this.handleFormChange();
    }, 300);
  }
  
  addEducation() {
    const container = document.getElementById('educationContainer');
    if (!container) return;
    
    const index = container.children.length;
    const educationItem = document.createElement('div');
    educationItem.className = 'education-item';
    educationItem.dataset.index = index;
    
    educationItem.innerHTML = `
      <div class="item-header">
        <h4>Education ${index + 1}</h4>
        <button type="button" class="remove-item">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label>Degree *</label>
          <input type="text" name="edu_degree" required>
        </div>
        <div class="form-group">
          <label>School *</label>
          <input type="text" name="edu_school" required>
        </div>
        <div class="form-group">
          <label>Location</label>
          <input type="text" name="edu_location">
        </div>
        <div class="form-group">
          <label>Graduation Date</label>
          <input type="text" name="edu_graduation_date" placeholder="e.g., May 2023">
        </div>
      </div>
    `;
    
    container.appendChild(educationItem);
    
    // Focus on the first input
    const firstInput = educationItem.querySelector('input');
    if (firstInput) firstInput.focus();
    
    this.handleFormChange();
  }
  
  removeEducation(item) {
    item.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => {
      item.remove();
      this.updateEducationNumbers();
      this.handleFormChange();
    }, 300);
  }
  
  updateExperienceNumbers() {
    const items = document.querySelectorAll('.experience-item');
    items.forEach((item, index) => {
      const header = item.querySelector('.item-header h4');
      if (header) {
        header.textContent = `Experience ${index + 1}`;
      }
      item.dataset.index = index;
    });
  }
  
  updateEducationNumbers() {
    const items = document.querySelectorAll('.education-item');
    items.forEach((item, index) => {
      const header = item.querySelector('.item-header h4');
      if (header) {
        header.textContent = `Education ${index + 1}`;
      }
      item.dataset.index = index;
    });
  }
  
  updatePreview() {
    const previewContainer = document.getElementById('resumePreview');
    if (!previewContainer) return;
    
    const formData = this.getFormData();
    const previewHTML = this.generatePreviewHTML(formData);
    
    previewContainer.innerHTML = previewHTML;
  }
  
  getFormData() {
    const form = document.getElementById('resumeForm');
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    
    // Basic fields
    for (let [key, value] of formData.entries()) {
      data[key] = value;
    }
    
    // Skills
    const skillTags = document.querySelectorAll('.skill-tag span');
    data.skills = Array.from(skillTags).map(tag => tag.textContent);
    
    // Experience
    const experienceItems = document.querySelectorAll('.experience-item');
    data.experience = Array.from(experienceItems).map(item => {
      return {
        title: item.querySelector('[name="exp_title"]')?.value || '',
        company: item.querySelector('[name="exp_company"]')?.value || '',
        location: item.querySelector('[name="exp_location"]')?.value || '',
        start_date: item.querySelector('[name="exp_start_date"]')?.value || '',
        end_date: item.querySelector('[name="exp_end_date"]')?.value || '',
        description: item.querySelector('[name="exp_description"]')?.value || ''
      };
    });
    
    // Education
    const educationItems = document.querySelectorAll('.education-item');
    data.education = Array.from(educationItems).map(item => {
      return {
        degree: item.querySelector('[name="edu_degree"]')?.value || '',
        school: item.querySelector('[name="edu_school"]')?.value || '',
        location: item.querySelector('[name="edu_location"]')?.value || '',
        graduation_date: item.querySelector('[name="edu_graduation_date"]')?.value || ''
      };
    });
    
    return data;
  }
  
  generatePreviewHTML(data) {
    const fullName = data.full_name || 'Your Name';
    const email = data.email || 'your.email@example.com';
    const phone = data.phone || '';
    const location = data.location || '';
    const website = data.website || '';
    const linkedin = data.linkedin || '';
    const summary = data.summary || '';
    
    let contactInfo = [];
    if (email) contactInfo.push(email);
    if (phone) contactInfo.push(phone);
    if (location) contactInfo.push(location);
    if (website) contactInfo.push(`<a href="${website}" target="_blank">${website}</a>`);
    if (linkedin) contactInfo.push(`<a href="${linkedin}" target="_blank">LinkedIn</a>`);
    
    let html = `
      <h1>${fullName}</h1>
      <div class="contact-info">
        ${contactInfo.map(info => `<p>${info}</p>`).join('')}
      </div>
    `;
    
    // Professional Summary
    if (summary) {
      html += `
        <div class="section">
          <h2>Professional Summary</h2>
          <p>${summary}</p>
        </div>
      `;
    }
    
    // Skills
    if (data.skills && data.skills.length > 0) {
      html += `
        <div class="section">
          <h2>Skills</h2>
          <div class="skills-grid">
            ${data.skills.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
          </div>
        </div>
      `;
    }
    
    // Experience
    if (data.experience && data.experience.length > 0) {
      const validExperience = data.experience.filter(exp => exp.title || exp.company);
      if (validExperience.length > 0) {
        html += `
          <div class="section">
            <h2>Work Experience</h2>
            ${validExperience.map(exp => `
              <div class="experience-item">
                <div class="item-header">
                  <div>
                    <div class="item-title">${exp.title || 'Job Title'}</div>
                    <div class="item-company">${exp.company || 'Company Name'}</div>
                    ${exp.location ? `<div class="item-location">${exp.location}</div>` : ''}
                  </div>
                  <div class="item-date">
                    ${exp.start_date || 'Start'} - ${exp.end_date || 'End'}
                  </div>
                </div>
                ${exp.description ? `<div class="item-description">${exp.description}</div>` : ''}
              </div>
            `).join('')}
          </div>
        `;
      }
    }
    
    // Education
    if (data.education && data.education.length > 0) {
      const validEducation = data.education.filter(edu => edu.degree || edu.school);
      if (validEducation.length > 0) {
        html += `
          <div class="section">
            <h2>Education</h2>
            ${validEducation.map(edu => `
              <div class="education-item">
                <div class="item-header">
                  <div>
                    <div class="item-title">${edu.degree || 'Degree'}</div>
                    <div class="item-company">${edu.school || 'School Name'}</div>
                    ${edu.location ? `<div class="item-location">${edu.location}</div>` : ''}
                  </div>
                  ${edu.graduation_date ? `<div class="item-date">${edu.graduation_date}</div>` : ''}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      }
    }
    
    return html;
  }
  
  startAutoSaveTimer() {
    if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }
    
    this.autoSaveTimer = setTimeout(() => {
      if (this.isModified) {
        this.saveResume(true);
      }
    }, this.autoSaveInterval);
  }
  
  async saveResume(isAutoSave = false) {
    if (!this.isModified && isAutoSave) return;
    
    const formData = this.getFormData();
    
    this.updateSaveStatus('saving');
    
    try {
      const response = await fetch(`/resume-builder/api/save-resume/${this.resumeId}/`, {
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
          this.showMessage('Resume saved successfully!', 'success');
        }
      } else {
        throw new Error('Save failed');
      }
    } catch (error) {
      console.error('Save error:', error);
      this.updateSaveStatus('error');
      this.showMessage('Failed to save resume. Please try again.', 'error');
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
    
    const preview = document.getElementById('resumePreview');
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

// Additional CSS for animations
const additionalCSS = `
@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-20px);
  }
}

.preview-panel.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background: var(--bg-secondary);
}

.preview-panel.fullscreen .panel-header {
  background: var(--bg-primary);
}
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);