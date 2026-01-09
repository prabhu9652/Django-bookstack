/* ========================================
   UNIFIED DARK THEME INTERACTIONS
   Premium animations and micro-interactions
======================================== */

class DarkThemeInteractions {
  constructor() {
    this.init();
  }

  init() {
    this.setupScrollEffects();
    this.setupIntersectionObserver();
    this.setupMagneticButtons();
    this.setupRippleEffects();
    this.setupParallaxEffects();
    this.setupSmoothScrolling();
    this.setupFormEnhancements();
    this.setupCardAnimations();
    this.setupNavbarEffects();
    this.setupLoadingStates();
  }

  // Navbar scroll effects
  setupNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    const updateNavbar = () => {
      const scrollY = window.scrollY;
      
      if (scrollY > 100) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }

      // Hide/show navbar on scroll
      if (scrollY > lastScrollY && scrollY > 200) {
        navbar.style.transform = 'translateY(-100%)';
      } else {
        navbar.style.transform = 'translateY(0)';
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
  }

  // Intersection Observer for animations
  setupIntersectionObserver() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          
          // Add animation classes based on data attributes
          if (element.dataset.animate) {
            element.classList.add(element.dataset.animate);
          } else {
            element.classList.add('animate-fade-in-up');
          }
          
          // Stagger animations for multiple elements
          if (element.dataset.delay) {
            element.style.animationDelay = element.dataset.delay;
          }
          
          observer.unobserve(element);
        }
      });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('[data-animate], .card-dark, .feature-item, .book-card').forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }

  // Magnetic button effects
  setupMagneticButtons() {
    const magneticElements = document.querySelectorAll('.btn-primary, .btn-accent, .card-dark');
    
    magneticElements.forEach(element => {
      element.addEventListener('mousemove', (e) => {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const moveX = x * 0.1;
        const moveY = y * 0.1;
        
        element.style.transform = `translate(${moveX}px, ${moveY}px)`;
      });
      
      element.addEventListener('mouseleave', () => {
        element.style.transform = 'translate(0, 0)';
      });
    });
  }

  // Ripple effects for buttons
  setupRippleEffects() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-accent');
    
    buttons.forEach(button => {
      button.addEventListener('click', (e) => {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          left: ${x}px;
          top: ${y}px;
          background: rgba(255, 255, 255, 0.3);
          border-radius: 50%;
          transform: scale(0);
          animation: ripple 0.6s ease-out;
          pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });

    // Add ripple animation CSS
    if (!document.querySelector('#ripple-styles')) {
      const style = document.createElement('style');
      style.id = 'ripple-styles';
      style.textContent = `
        @keyframes ripple {
          to {
            transform: scale(2);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  // Parallax effects
  setupParallaxEffects() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElements.length === 0) return;
    
    let ticking = false;
    
    const updateParallax = () => {
      const scrollY = window.scrollY;
      
      parallaxElements.forEach(element => {
        const speed = parseFloat(element.dataset.parallax) || 0.5;
        const yPos = -(scrollY * speed);
        element.style.transform = `translateY(${yPos}px)`;
      });
      
      ticking = false;
    };
    
    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    };
    
    window.addEventListener('scroll', requestTick, { passive: true });
  }

  // Smooth scrolling for anchor links
  setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  // Enhanced form interactions
  setupFormEnhancements() {
    const formControls = document.querySelectorAll('.form-control-dark');
    
    formControls.forEach(input => {
      // Floating label effect
      const label = input.previousElementSibling;
      
      const checkInput = () => {
        if (input.value || input === document.activeElement) {
          label?.classList.add('floating');
        } else {
          label?.classList.remove('floating');
        }
      };
      
      input.addEventListener('focus', checkInput);
      input.addEventListener('blur', checkInput);
      input.addEventListener('input', checkInput);
      
      // Initial check
      checkInput();
      
      // Add focus glow effect
      input.addEventListener('focus', () => {
        input.parentElement?.classList.add('focused');
      });
      
      input.addEventListener('blur', () => {
        input.parentElement?.classList.remove('focused');
      });
    });

    // Add floating label styles
    if (!document.querySelector('#form-styles')) {
      const style = document.createElement('style');
      style.id = 'form-styles';
      style.textContent = `
        .form-group {
          position: relative;
          margin-bottom: 1.5rem;
        }
        
        .form-label-dark {
          position: absolute;
          left: 1rem;
          top: 0.75rem;
          transition: all 0.3s ease;
          pointer-events: none;
          z-index: 1;
        }
        
        .form-label-dark.floating {
          top: -0.5rem;
          left: 0.75rem;
          font-size: 0.8rem;
          background: var(--bg-secondary);
          padding: 0 0.5rem;
          color: var(--text-accent);
        }
        
        .form-group.focused .form-control-dark {
          box-shadow: 0 0 0 0.2rem var(--shadow-light);
        }
      `;
      document.head.appendChild(style);
    }
  }

  // Card hover animations
  setupCardAnimations() {
    const cards = document.querySelectorAll('.card-dark, .book-card');
    
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        // Add subtle rotation and scale
        card.style.transform = 'translateY(-10px) rotateX(5deg) rotateY(5deg) scale(1.02)';
        card.style.transition = 'transform 0.3s ease';
        
        // Add glow effect
        card.style.boxShadow = '0 20px 40px rgba(102, 126, 234, 0.2)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) rotateX(0) rotateY(0) scale(1)';
        card.style.boxShadow = '';
      });
      
      // Add tilt effect based on mouse position
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `translateY(-10px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
      });
    });
  }

  // Scroll effects for elements
  setupScrollEffects() {
    let ticking = false;
    
    const updateScrollEffects = () => {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      
      // Update elements with scroll effects
      document.querySelectorAll('[data-scroll-speed]').forEach(element => {
        const speed = parseFloat(element.dataset.scrollSpeed);
        const yPos = scrollY * speed;
        element.style.transform = `translateY(${yPos}px)`;
      });
      
      // Fade elements based on scroll position
      document.querySelectorAll('[data-fade-scroll]').forEach(element => {
        const rect = element.getBoundingClientRect();
        const elementTop = rect.top;
        const elementHeight = rect.height;
        
        let opacity = 1;
        if (elementTop < 0) {
          opacity = Math.max(0, 1 + elementTop / elementHeight);
        } else if (elementTop > windowHeight) {
          opacity = Math.max(0, 1 - (elementTop - windowHeight) / elementHeight);
        }
        
        element.style.opacity = opacity;
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

  // Loading states and skeleton screens
  setupLoadingStates() {
    // Add loading skeletons for images
    document.querySelectorAll('img[data-src]').forEach(img => {
      const skeleton = document.createElement('div');
      skeleton.className = 'loading-skeleton';
      skeleton.style.cssText = `
        width: 100%;
        height: 200px;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
      `;
      
      img.parentNode.insertBefore(skeleton, img);
      img.style.display = 'none';
      
      // Lazy load image
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const image = entry.target;
            image.src = image.dataset.src;
            image.onload = () => {
              skeleton.remove();
              image.style.display = 'block';
              image.classList.add('animate-fade-in-up');
            };
            observer.unobserve(image);
          }
        });
      });
      
      observer.observe(img);
    });
  }

  // Utility methods
  static debounce(func, wait) {
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

  static throttle(func, limit) {
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
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new DarkThemeInteractions();
});

// Add performance monitoring
if ('performance' in window) {
  window.addEventListener('load', () => {
    const perfData = performance.getEntriesByType('navigation')[0];
    console.log(`Page loaded in ${perfData.loadEventEnd - perfData.loadEventStart}ms`);
  });
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DarkThemeInteractions;
}