/**
 * Resume AI Content Generator
 * Enterprise-grade AI-powered content generation for resumes and cover letters
 * 
 * Features:
 * - Role-specific summary generation
 * - Achievement bullet point generation
 * - Skills list generation
 * - ATS optimization analysis
 * - Cover letter content generation
 */

class ResumeAIGenerator {
    constructor(options = {}) {
        this.csrfToken = options.csrfToken || document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        this.role = options.role || 'software_engineer';
        this.baseUrl = '/resume-builder/api/ai';
        this.onSuccess = options.onSuccess || this.showToast.bind(this);
        this.onError = options.onError || this.showError.bind(this);
    }

    /**
     * Generate a professional summary based on role
     */
    async generateSummary(years = 5) {
        try {
            const response = await this.makeRequest('/generate-summary/', {
                role: this.role,
                years: years
            });
            
            if (response.success) {
                return response.summary;
            }
            throw new Error(response.error || 'Failed to generate summary');
        } catch (error) {
            this.onError('Failed to generate summary: ' + error.message);
            throw error;
        }
    }

    /**
     * Generate achievement bullet points
     */
    async generateBullets(count = 5) {
        try {
            const response = await this.makeRequest('/generate-bullets/', {
                role: this.role,
                count: count
            });
            
            if (response.success) {
                return response.bullets;
            }
            throw new Error(response.error || 'Failed to generate bullets');
        } catch (error) {
            this.onError('Failed to generate bullet points: ' + error.message);
            throw error;
        }
    }

    /**
     * Generate skills list for the role
     */
    async generateSkills(count = 12) {
        try {
            const response = await this.makeRequest('/generate-skills/', {
                role: this.role,
                count: count
            });
            
            if (response.success) {
                return {
                    skills: response.skills,
                    categorized: response.categorized_skills
                };
            }
            throw new Error(response.error || 'Failed to generate skills');
        } catch (error) {
            this.onError('Failed to generate skills: ' + error.message);
            throw error;
        }
    }

    /**
     * Generate cover letter content
     */
    async generateCoverLetter(company, position, years = 5) {
        try {
            const response = await this.makeRequest('/generate-cover-letter/', {
                role: this.role,
                company: company,
                position: position,
                years: years
            });
            
            if (response.success) {
                return response.content;
            }
            throw new Error(response.error || 'Failed to generate cover letter');
        } catch (error) {
            this.onError('Failed to generate cover letter: ' + error.message);
            throw error;
        }
    }

    /**
     * Analyze text for ATS optimization
     */
    async analyzeATS(text) {
        try {
            const response = await this.makeRequest('/optimize-ats/', {
                role: this.role,
                text: text
            });
            
            if (response.success) {
                return response.analysis;
            }
            throw new Error(response.error || 'Failed to analyze ATS');
        } catch (error) {
            this.onError('Failed to analyze ATS: ' + error.message);
            throw error;
        }
    }

    /**
     * Make API request
     */
    async makeRequest(endpoint, data) {
        const response = await fetch(this.baseUrl + endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }

    /**
     * Show success toast notification
     */
    showToast(message) {
        const toast = document.getElementById('successToast');
        if (toast) {
            const messageEl = document.getElementById('toastMessage');
            if (messageEl) messageEl.textContent = message;
            toast.style.display = 'flex';
            setTimeout(() => { toast.style.display = 'none'; }, 3000);
        }
    }

    /**
     * Show error notification
     */
    showError(message) {
        console.error(message);
        alert(message);
    }

    /**
     * Set the current role
     */
    setRole(role) {
        this.role = role;
    }
}

/**
 * AI Button Component - Adds AI generation buttons to form fields
 */
class AIButtonManager {
    constructor(aiGenerator) {
        this.ai = aiGenerator;
        this.buttons = [];
    }

    /**
     * Add AI generate button to a field
     */
    addButton(targetSelector, type, options = {}) {
        const target = document.querySelector(targetSelector);
        if (!target) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'ai-button-wrapper';
        wrapper.style.cssText = 'display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;';

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-generate-btn';
        btn.innerHTML = `<i class="fas fa-magic"></i> AI Generate`;
        btn.onclick = () => this.handleGenerate(target, type, options, btn);

        wrapper.appendChild(btn);
        target.parentNode.appendChild(wrapper);
        this.buttons.push({ target, btn, type });
    }

    /**
     * Handle AI generation
     */
    async handleGenerate(target, type, options, btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        btn.disabled = true;
        btn.classList.add('loading');

        try {
            let result;
            switch (type) {
                case 'summary':
                    result = await this.ai.generateSummary(options.years || 5);
                    target.value = result;
                    break;
                case 'bullets':
                    result = await this.ai.generateBullets(options.count || 5);
                    target.value = result.join('\n');
                    break;
                case 'skills':
                    const skillsData = await this.ai.generateSkills(options.count || 12);
                    target.value = skillsData.skills.join('\n');
                    break;
            }
            this.ai.showToast('Content generated successfully!');
        } catch (error) {
            console.error('Generation failed:', error);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
            btn.classList.remove('loading');
        }
    }
}

/**
 * ATS Score Component - Shows ATS optimization score
 */
class ATSScoreComponent {
    constructor(aiGenerator, containerSelector) {
        this.ai = aiGenerator;
        this.container = document.querySelector(containerSelector);
        this.score = 0;
    }

    /**
     * Render the ATS score component
     */
    render() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="ats-score-indicator">
                <div class="ats-score-circle">
                    <svg viewBox="0 0 36 36">
                        <path class="score-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                        <path class="score-fill" stroke-dasharray="${this.score}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                    </svg>
                    <span class="ats-score-value">${this.score}%</span>
                </div>
                <div class="ats-score-info">
                    <span class="ats-score-label">${this.getScoreLabel()}</span>
                    <p>${this.getScoreDescription()}</p>
                </div>
                <button type="button" class="btn btn-ghost btn-sm" onclick="window.atsComponent?.analyze()">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
        `;
    }

    /**
     * Analyze current resume content
     */
    async analyze() {
        const summaryEl = document.querySelector('[name="summary"]');
        const skillsEl = document.getElementById('skillsInput');
        const experienceEls = document.querySelectorAll('[data-field="bullets"]');

        let text = '';
        if (summaryEl) text += summaryEl.value + ' ';
        if (skillsEl) text += skillsEl.value + ' ';
        experienceEls.forEach(el => { text += el.value + ' '; });

        if (!text.trim()) {
            this.score = 0;
            this.render();
            return;
        }

        try {
            const analysis = await this.ai.analyzeATS(text);
            this.score = Math.round(analysis.score);
            this.foundKeywords = analysis.found_keywords;
            this.missingKeywords = analysis.missing_keywords;
            this.render();
        } catch (error) {
            console.error('ATS analysis failed:', error);
        }
    }

    getScoreLabel() {
        if (this.score >= 80) return 'Excellent';
        if (this.score >= 60) return 'Good';
        if (this.score >= 40) return 'Fair';
        return 'Needs Improvement';
    }

    getScoreDescription() {
        if (this.score >= 80) return 'Your resume is well-optimized for ATS systems';
        if (this.score >= 60) return 'Good keyword coverage, consider adding more';
        if (this.score >= 40) return 'Add more role-specific keywords';
        return 'Include more industry keywords for better ATS matching';
    }
}

// Export for use in templates
window.ResumeAIGenerator = ResumeAIGenerator;
window.AIButtonManager = AIButtonManager;
window.ATSScoreComponent = ATSScoreComponent;
