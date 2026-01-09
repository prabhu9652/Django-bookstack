/* ========================================
   ENTERPRISE INTERACTION SYSTEM
   Production-Ready JavaScript
======================================== */

class EnterpriseUI {
  constructor() {
    this.init();
  }

  init() {
    this.setupNavigation();
    this.setupScrollEffects();
    this.setupIntersectionObserver();
    this.setupFormEnhancements();
    this.setupAccessibility();
    this.setupPerformanceOptimizations();
  }

  // Navigation System
  setupNavigation() {
    const navbar = document.querySelector('.navbar-enterprise');
    if (!navbar) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    const updateNavbar = () => {
      const scrollY = window.scrollY;
      
      if (scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }

      lastScrollY = scrollY;
      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateNavbar);
        ticking = true;
      }
    };

    window.addEventListener('scroll', requestTick, { passive: true });

    // Active navigation state
    this.setActiveNavigation();
  }

  setActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link-enterprise');
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPath || (currentPath !== '/' && href !== '/' && currentPath.startsWith(href))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  // Scroll Effects
  setupScrollEffects() {
    const elements = document.querySelectorAll('[data-scroll]');
    if (elements.length === 0) return;

    let ticking = false;

    const updateScrollEffects = () => {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;

      elements.forEach(element => {
        const speed = parseFloat(element.dataset.scroll) || 0.5;
        const rect = element.getBoundingClientRect();
        
        if (rect.top < windowHeight && rect.bottom > 0) {
          const yPos = scrollY * speed;
          element.style.transform = `translateY(${yPos}px)`;
        }
      });

      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateScrollEffects);
        ticking = true;
      }
    };

    window.addEventListener('scroll', requestTick, { passive: true });
  }

  // Intersection Observer for Animations
  setupIntersectionObserver() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          
          // Add animation classes
          if (element.dataset.animate) {
            element.classList.add(element.dataset.animate);
          } else {
            element.classList.add('animate-fade-in-up');
          }
          
          // Handle stagger animations
          if (element.classList.contains('animate-stagger')) {
            const children = element.children;
            Array.from(children).forEach((child, index) => {
              child.style.animationDelay = `${(index + 1) * 0.1}s`;
            });
          }
          
          observer.unobserve(element);
        }
      });
    }, observerOptions);

    // Observe elements
    document.querySelectorAll('[data-animate], .animate-stagger, .card-enterprise, .feature-item').forEach(el => {
      observer.observe(el);
    });
  }

  // Form Enhancements
  setupFormEnhancements() {
    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      this.enhanceForm(form);
    });

    // Input focus effects
    const inputs = document.querySelectorAll('.form-control-enterprise');
    inputs.forEach(input => {
      this.enhanceInput(input);
    });

    // Password visibility toggle
    this.setupPasswordToggles();
  }

  enhanceForm(form) {
    const inputs = form.querySelectorAll('.form-control-enterprise');
    
    form.addEventListener('submit', (e) => {
      let isValid = true;
      
      inputs.forEach(input => {
        if (!this.validateInput(input)) {
          isValid = false;
        }
      });
      
      if (!isValid) {
        e.preventDefault();
        this.showFormErrors(form);
      } else {
        this.showFormLoading(form);
      }
    });

    // Real-time validation
    inputs.forEach(input => {
      input.addEventListener('blur', () => {
        this.validateInput(input);
      });
      
      input.addEventListener('input', () => {
        this.clearInputError(input);
      });
    });
  }

  enhanceInput(input) {
    const group = input.closest('.form-group-enterprise');
    if (!group) return;

    // Focus effects
    input.addEventListener('focus', () => {
      group.classList.add('focused');
    });

    input.addEventListener('blur', () => {
      group.classList.remove('focused');
    });

    // Floating label effect
    const label = group.querySelector('.form-label-enterprise');
    if (label) {
      const checkValue = () => {
        if (input.value || input === document.activeElement) {
          label.classList.add('floating');
        } else {
          label.classList.remove('floating');
        }
      };

      input.addEventListener('focus', checkValue);
      input.addEventListener('blur', checkValue);
      input.addEventListener('input', checkValue);
      checkValue(); // Initial check
    }
  }

  validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    const required = input.hasAttribute('required');
    
    this.clearInputError(input);
    
    if (required && !value) {
      this.showInputError(input, 'This field is required');
      return false;
    }
    
    if (value && type === 'email' && !this.isValidEmail(value)) {
      this.showInputError(input, 'Please enter a valid email address');
      return false;
    }
    
    if (value && input.name === 'password' && value.length < 8) {
      this.showInputError(input, 'Password must be at least 8 characters');
      return false;
    }
    
    this.showInputSuccess(input);
    return true;
  }

  showInputError(input, message) {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    let errorElement = input.parentNode.querySelector('.form-error-enterprise');
    if (!errorElement) {
      errorElement = document.createElement('div');
      errorElement.className = 'form-error-enterprise';
      input.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = message;
  }

  showInputSuccess(input) {
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
    this.clearInputError(input);
  }

  clearInputError(input) {
    input.classList.remove('is-invalid', 'is-valid');
    const errorElement = input.parentNode.querySelector('.form-error-enterprise');
    if (errorElement) {
      errorElement.remove();
    }
  }

  showFormErrors(form) {
    const firstError = form.querySelector('.is-invalid');
    if (firstError) {
      firstError.focus();
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  showFormLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }
  }

  setupPasswordToggles() {
    const toggles = document.querySelectorAll('[data-password-toggle]');
    toggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        const targetId = toggle.dataset.passwordToggle;
        const input = document.getElementById(targetId);
        const icon = toggle.querySelector('i');
        
        if (input.type === 'password') {
          input.type = 'text';
          icon.classList.remove('fa-eye');
          icon.classList.add('fa-eye-slash');
        } else {
          input.type = 'password';
          icon.classList.remove('fa-eye-slash');
          icon.classList.add('fa-eye');
        }
      });
    });
  }

  // Accessibility Enhancements
  setupAccessibility() {
    // Keyboard navigation for dropdowns
    this.setupDropdownKeyboard();
    
    // Focus management
    this.setupFocusManagement();
    
    // ARIA live regions
    this.setupLiveRegions();
  }

  setupDropdownKeyboard() {
    const dropdowns = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    dropdowns.forEach(dropdown => {
      dropdown.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          dropdown.click();
        }
      });
    });
  }

  setupFocusManagement() {
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'sr-only sr-only-focusable';
    skipLink.style.cssText = `
      position: absolute;
      top: -40px;
      left: 6px;
      z-index: 1000;
      padding: 8px 16px;
      background: var(--primary-600);
      color: white;
      text-decoration: none;
      border-radius: 4px;
    `;
    
    skipLink.addEventListener('focus', () => {
      skipLink.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', () => {
      skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
  }

  setupLiveRegions() {
    // Create live region for announcements
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);
  }

  // Performance Optimizations
  setupPerformanceOptimizations() {
    // Lazy load images
    this.setupLazyLoading();
    
    // Debounced resize handler
    this.setupResizeHandler();
    
    // Preload critical resources
    this.preloadCriticalResources();
  }

  setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    if (images.length === 0) return;

    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.add('loaded');
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  }

  setupResizeHandler() {
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        this.handleResize();
      }, 250);
    });
  }

  handleResize() {
    // Update any size-dependent calculations
    this.setActiveNavigation();
  }

  preloadCriticalResources() {
    // Preload critical fonts
    const fontLinks = [
      'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    ];

    fontLinks.forEach(href => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'style';
      link.href = href;
      document.head.appendChild(link);
    });
  }

  // Utility Methods
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  debounce(func, wait) {
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

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  // Public API for announcements
  announce(message, priority = 'polite') {
    const liveRegion = document.getElementById('live-region');
    if (liveRegion) {
      liveRegion.setAttribute('aria-live', priority);
      liveRegion.textContent = message;
      
      // Clear after announcement
      setTimeout(() => {
        liveRegion.textContent = '';
      }, 1000);
    }
  }
}

// Initialize Enterprise UI
document.addEventListener('DOMContentLoaded', () => {
  window.enterpriseUI = new EnterpriseUI();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EnterpriseUI;
}

// Performance monitoring
if ('performance' in window) {
  window.addEventListener('load', () => {
    const perfData = performance.getEntriesByType('navigation')[0];
    if (perfData) {
      console.log(`Page loaded in ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
    }
  });
}