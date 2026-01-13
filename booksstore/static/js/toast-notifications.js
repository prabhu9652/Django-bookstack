/**
 * Toast Notifications - Standardized UI Component
 * 
 * Displays toast notifications at the TOP of the screen
 * Supports: success, error, warning, info types
 * Auto-dismisses after configurable duration
 * 
 * Usage:
 *   Toast.success('Operation completed successfully');
 *   Toast.error('Something went wrong');
 *   Toast.warning('Please check your input');
 *   Toast.info('New update available');
 *   Toast.show('Custom message', { type: 'success', duration: 5000 });
 */

const Toast = (function() {
  'use strict';
  
  // Configuration
  const config = {
    duration: 4000,        // Default duration in ms
    maxToasts: 5,          // Maximum visible toasts
    position: 'top',       // Always top
    containerClass: 'toast-container',
    toastClass: 'toast'
  };
  
  // Icon mapping
  const icons = {
    success: 'fas fa-check-circle',
    error: 'fas fa-exclamation-circle',
    warning: 'fas fa-exclamation-triangle',
    info: 'fas fa-info-circle'
  };
  
  // Container element
  let container = null;
  
  /**
   * Initialize toast container
   */
  function init() {
    if (container) return;
    
    container = document.createElement('div');
    container.className = config.containerClass;
    container.setAttribute('role', 'alert');
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
  }
  
  /**
   * Create and show a toast
   * @param {string} message - Toast message
   * @param {Object} options - Toast options
   */
  function show(message, options = {}) {
    init();
    
    const type = options.type || 'info';
    const duration = options.duration || config.duration;
    const closable = options.closable !== false;
    
    // Limit number of toasts
    const existingToasts = container.querySelectorAll('.' + config.toastClass);
    if (existingToasts.length >= config.maxToasts) {
      const oldest = existingToasts[0];
      removeToast(oldest);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `${config.toastClass} ${type}`;
    
    // Build toast HTML
    let html = `<i class="${icons[type] || icons.info}"></i>`;
    html += `<span class="toast-message">${escapeHtml(message)}</span>`;
    
    if (closable) {
      html += `<button class="toast-close" aria-label="Close notification">
        <i class="fas fa-times"></i>
      </button>`;
    }
    
    toast.innerHTML = html;
    
    // Add close handler
    if (closable) {
      const closeBtn = toast.querySelector('.toast-close');
      closeBtn.addEventListener('click', () => removeToast(toast));
    }
    
    // Add to container
    container.appendChild(toast);
    
    // Auto-dismiss
    if (duration > 0) {
      setTimeout(() => removeToast(toast), duration);
    }
    
    return toast;
  }
  
  /**
   * Remove a toast with animation
   * @param {HTMLElement} toast - Toast element to remove
   */
  function removeToast(toast) {
    if (!toast || !toast.parentNode) return;
    
    toast.classList.add('hiding');
    
    // Remove after animation
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 200);
  }
  
  /**
   * Clear all toasts
   */
  function clearAll() {
    if (!container) return;
    
    const toasts = container.querySelectorAll('.' + config.toastClass);
    toasts.forEach(toast => removeToast(toast));
  }
  
  /**
   * Escape HTML to prevent XSS
   * @param {string} str - String to escape
   */
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
  
  // Public API
  return {
    show: show,
    success: (msg, opts = {}) => show(msg, { ...opts, type: 'success' }),
    error: (msg, opts = {}) => show(msg, { ...opts, type: 'error' }),
    warning: (msg, opts = {}) => show(msg, { ...opts, type: 'warning' }),
    info: (msg, opts = {}) => show(msg, { ...opts, type: 'info' }),
    clear: clearAll,
    config: (options) => Object.assign(config, options)
  };
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Toast;
}

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  // Check for Django messages and convert to toasts
  const djangoMessages = document.querySelectorAll('.messages .alert, .django-message');
  djangoMessages.forEach(msg => {
    const text = msg.textContent.trim();
    const type = msg.classList.contains('success') ? 'success' :
                 msg.classList.contains('error') ? 'error' :
                 msg.classList.contains('warning') ? 'warning' : 'info';
    
    if (text) {
      Toast.show(text, { type: type });
      msg.remove();
    }
  });
});
