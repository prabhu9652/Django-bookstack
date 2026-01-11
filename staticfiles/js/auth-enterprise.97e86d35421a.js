/**
 * Enterprise-Grade Authentication JavaScript
 * Handles form interactions, validation, and UX enhancements
 */

class AuthenticationManager {
  constructor() {
    this.init();
  }

  init() {
    this.setupPasswordToggles();
    this.setupFormValidation();
    this.setupPasswordStrength();
    this.setupFormSubmission();
    this.setupAnimations();
  }

  /**
   * Setup password visibility toggles
   */
  setupPasswordToggles() {
    const toggles = document.querySelectorAll('.password-toggle');
    
    toggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const input = toggle.parentElement.querySelector('input');
        const icon = toggle.querySelector('i');
        
        if (input.type === 'password') {
          input.type = 'text';
          icon.className = 'fas fa-eye-slash';
          toggle.setAttribute('aria-label', 'Hide password');
        } else {
          input.type = 'password';
          icon.className = 'fas fa-eye';
          toggle.setAttribute('aria-label', 'Show password');
        }
        
        // Add subtle animation
        toggle.style.transform = 'scale(0.9)';
        setTimeout(() => {
          toggle.style.transform = 'scale(1)';
        }, 150);
      });
    });
  }

  /**
   * Setup real-time form validation
   */
  setupFormValidation() {
    const inputs = document.querySelectorAll('.auth-form input');
    
    inputs.forEach(input => {
      // Real-time validation on input
      input.addEventListener('input', () => {
        this.validateField(input);
      });
      
      // Validation on blur
      input.addEventListener('blur', () => {
        this.validateField(input);
      });
      
      // Enhanced focus effects
      input.addEventListener('focus', () => {
        this.addFocusEffect(input);
      });
      
      input.addEventListener('blur', () => {
        this.removeFocusEffect(input);
      });
    });

    // Password confirmation validation
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    
    if (password1 && password2) {
      password2.addEventListener('input', () => {
        this.validatePasswordMatch(password1, password2);
      });
    }
  }

  /**
   * Validate individual form field
   */
  validateField(input) {
    const wrapper = input.closest('.input-wrapper');
    const validationIcon = wrapper.querySelector('.input-validation-icon');
    
    if (!validationIcon) return;

    const isValid = this.isFieldValid(input);
    
    if (input.value.trim() === '') {
      validationIcon.className = 'input-validation-icon';
      return;
    }
    
    if (isValid) {
      validationIcon.className = 'input-validation-icon valid';
      this.addSuccessEffect(input);
    } else {
      validationIcon.className = 'input-validation-icon invalid';
      this.addErrorEffect(input);
    }
  }

  /**
   * Check if field is valid
   */
  isFieldValid(input) {
    if (input.type === 'text' || input.name === 'username') {
      return input.value.trim().length >= 3;
    }
    
    if (input.type === 'password') {
      return input.value.length >= 8;
    }
    
    return input.value.trim() !== '';
  }

  /**
   * Validate password match
   */
  validatePasswordMatch(password1, password2) {
    const wrapper = password2.closest('.input-wrapper');
    const validationIcon = wrapper.querySelector('.input-validation-icon');
    
    if (!validationIcon || password2.value === '') {
      validationIcon.className = 'input-validation-icon';
      return;
    }
    
    if (password1.value === password2.value) {
      validationIcon.className = 'input-validation-icon valid';
      this.addSuccessEffect(password2);
    } else {
      validationIcon.className = 'input-validation-icon invalid';
      this.addErrorEffect(password2);
    }
  }

  /**
   * Setup password strength indicator
   */
  setupPasswordStrength() {
    const passwordInput = document.getElementById('id_password1');
    const strengthIndicator = document.getElementById('passwordStrength');
    
    if (!passwordInput || !strengthIndicator) return;
    
    passwordInput.addEventListener('input', () => {
      const strength = this.calculatePasswordStrength(passwordInput.value);
      this.updatePasswordStrength(strengthIndicator, strength);
    });
    
    passwordInput.addEventListener('focus', () => {
      strengthIndicator.classList.add('visible');
    });
  }

  /**
   * Calculate password strength
   */
  calculatePasswordStrength(password) {
    let score = 0;
    
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    if (score <= 2) return 'weak';
    if (score <= 3) return 'fair';
    if (score <= 4) return 'good';
    return 'strong';
  }

  /**
   * Update password strength indicator
   */
  updatePasswordStrength(indicator, strength) {
    const fill = indicator.querySelector('.strength-fill');
    const text = indicator.querySelector('.strength-text');
    
    fill.className = `strength-fill ${strength}`;
    
    const strengthTexts = {
      weak: 'Weak password',
      fair: 'Fair password',
      good: 'Good password',
      strong: 'Strong password'
    };
    
    text.textContent = strengthTexts[strength] || 'Password strength';
  }

  /**
   * Setup form submission with loading states
   */
  setupFormSubmission() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        const submitBtn = form.querySelector('.btn-auth-primary');
        
        if (submitBtn && !submitBtn.disabled) {
          this.showLoadingState(submitBtn);
          
          // Prevent double submission
          submitBtn.disabled = true;
          
          // Re-enable after 3 seconds as fallback
          setTimeout(() => {
            if (submitBtn.disabled) {
              this.hideLoadingState(submitBtn);
              submitBtn.disabled = false;
            }
          }, 3000);
        }
      });
    });
  }

  /**
   * Show loading state on button
   */
  showLoadingState(button) {
    button.classList.add('loading');
    button.style.pointerEvents = 'none';
  }

  /**
   * Hide loading state on button
   */
  hideLoadingState(button) {
    button.classList.remove('loading');
    button.style.pointerEvents = 'auto';
  }

  /**
   * Setup entrance animations
   */
  setupAnimations() {
    // Trigger animations on page load
    setTimeout(() => {
      const animatedElements = document.querySelectorAll('[class*="animate-"]');
      animatedElements.forEach(el => {
        el.style.animationPlayState = 'running';
      });
    }, 100);
    
    // Setup intersection observer for scroll animations
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.animationPlayState = 'running';
          }
        });
      });
      
      document.querySelectorAll('[class*="animate-"]').forEach(el => {
        observer.observe(el);
      });
    }
  }

  /**
   * Add focus effect to input
   */
  addFocusEffect(input) {
    const wrapper = input.closest('.input-wrapper');
    wrapper.style.transform = 'scale(1.02)';
    wrapper.style.transition = 'transform 0.2s ease';
  }

  /**
   * Remove focus effect from input
   */
  removeFocusEffect(input) {
    const wrapper = input.closest('.input-wrapper');
    wrapper.style.transform = 'scale(1)';
  }

  /**
   * Add success effect to input
   */
  addSuccessEffect(input) {
    input.style.borderColor = '#22c55e';
    setTimeout(() => {
      if (input !== document.activeElement) {
        input.style.borderColor = '';
      }
    }, 2000);
  }

  /**
   * Add error effect to input
   */
  addErrorEffect(input) {
    input.style.borderColor = '#ef4444';
    setTimeout(() => {
      if (input !== document.activeElement) {
        input.style.borderColor = '';
      }
    }, 2000);
  }
}

/**
 * Access Request Success Handler
 * Handles the success flow after account creation
 */
class AccessRequestHandler {
  constructor() {
    this.init();
  }

  init() {
    // Check if we're on the access status page after signup
    if (this.isAfterSignup()) {
      this.showWelcomeMessage();
    }
    
    this.setupAccessRequestFlow();
  }

  /**
   * Check if user just signed up
   */
  isAfterSignup() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('signup') === 'success' || 
           document.referrer.includes('/accounts/signup/');
  }

  /**
   * Show welcome message for new users
   */
  showWelcomeMessage() {
    const welcomeMessage = this.createWelcomeMessage();
    const container = document.querySelector('.access-status-section');
    
    if (container) {
      container.insertBefore(welcomeMessage, container.firstChild);
      
      // Animate in
      setTimeout(() => {
        welcomeMessage.style.opacity = '1';
        welcomeMessage.style.transform = 'translateY(0)';
      }, 100);
    }
  }

  /**
   * Create welcome message element
   */
  createWelcomeMessage() {
    const message = document.createElement('div');
    message.className = 'welcome-message';
    message.style.cssText = `
      background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
      border: 2px solid rgba(34, 197, 94, 0.3);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
      text-align: center;
      opacity: 0;
      transform: translateY(-20px);
      transition: all 0.6s ease;
    `;
    
    message.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <i class="fas fa-check" style="color: white; font-size: 1.5rem;"></i>
        </div>
        <div>
          <h3 style="color: #22c55e; margin: 0; font-size: 1.5rem; font-weight: 600;">Welcome to TechBookHub!</h3>
          <p style="color: var(--text-secondary); margin: 0; font-size: 1rem;">Your account has been created successfully.</p>
        </div>
      </div>
      <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 1.5rem; margin-top: 1rem;">
        <h4 style="color: var(--text-primary); margin-bottom: 0.75rem; font-size: 1.125rem;">Next Steps:</h4>
        <ol style="text-align: left; color: var(--text-secondary); line-height: 1.6; margin: 0; padding-left: 1.5rem;">
          <li>Click "Request Access" below to submit your access request</li>
          <li>An administrator will review your request within 24 hours</li>
          <li>You'll receive an email notification when approved</li>
          <li>Once approved, you'll have full access to our technical library</li>
        </ol>
      </div>
    `;
    
    return message;
  }

  /**
   * Setup access request flow with enhanced UX
   */
  setupAccessRequestFlow() {
    const requestButtons = document.querySelectorAll('[id*="requestAccess"], .btn-request-access');
    
    requestButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        this.handleAccessRequest(e, button);
      });
    });
  }

  /**
   * Handle access request with enhanced feedback
   */
  handleAccessRequest(e, button) {
    e.preventDefault();
    
    // Show loading state
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting Request...';
    button.disabled = true;
    
    // Simulate request (replace with actual AJAX call)
    setTimeout(() => {
      this.showAccessRequestSuccess();
      button.innerHTML = originalText;
      button.disabled = false;
    }, 1500);
  }

  /**
   * Show access request success message
   */
  showAccessRequestSuccess() {
    const successMessage = this.createSuccessMessage();
    document.body.appendChild(successMessage);
    
    // Animate in
    setTimeout(() => {
      successMessage.style.opacity = '1';
      successMessage.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 100);
    
    // Auto-hide after 4 seconds
    setTimeout(() => {
      this.hideSuccessMessage(successMessage);
    }, 4000);
  }

  /**
   * Create success message modal
   */
  createSuccessMessage() {
    const modal = document.createElement('div');
    modal.className = 'access-request-success-modal';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(4px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s ease;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
      background: var(--bg-surface);
      border-radius: 16px;
      padding: 3rem 2rem;
      max-width: 480px;
      width: 90%;
      text-align: center;
      transform: translate(-50%, -50%) scale(0.9);
      transition: transform 0.3s ease;
      position: relative;
      top: 50%;
      left: 50%;
    `;
    
    content.innerHTML = `
      <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
        <i class="fas fa-paper-plane" style="color: white; font-size: 2rem;"></i>
      </div>
      <h3 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 1.5rem; font-weight: 600;">Request Submitted Successfully!</h3>
      <p style="color: var(--text-secondary); margin-bottom: 2rem; line-height: 1.6;">Your access request has been submitted to our administrators. You'll receive an email notification once your request is reviewed and approved.</p>
      <div style="background: rgba(74, 158, 255, 0.1); border: 1px solid rgba(74, 158, 255, 0.3); border-radius: 8px; padding: 1rem; margin-bottom: 2rem;">
        <p style="color: #4a9eff; margin: 0; font-size: 0.875rem; font-weight: 500;">
          <i class="fas fa-clock" style="margin-right: 0.5rem;"></i>
          Typical approval time: 24 hours or less
        </p>
      </div>
      <button onclick="this.closest('.access-request-success-modal').remove()" style="background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%); color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease;">
        Got it, thanks!
      </button>
    `;
    
    modal.appendChild(content);
    
    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.hideSuccessMessage(modal);
      }
    });
    
    return modal;
  }

  /**
   * Hide success message
   */
  hideSuccessMessage(modal) {
    modal.style.opacity = '0';
    setTimeout(() => {
      if (modal.parentNode) {
        modal.parentNode.removeChild(modal);
      }
    }, 300);
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new AuthenticationManager();
  new AccessRequestHandler();
});

// Export for potential external use
window.AuthenticationManager = AuthenticationManager;
window.AccessRequestHandler = AccessRequestHandler;