/* ===== PREMIUM INTERACTIONS & ANIMATIONS FRAMEWORK ===== */

class PremiumInteractions {
  constructor() {
    this.init();
    this.setupAdvancedObservers();
    this.setupMagneticElements();
    this.setupParallaxEffects();
    this.setupAdvancedAnimations();
    this.setupPageTransitions();
  }

  init() {
    this.setupIntersectionObserver();
    this.setupSmoothScrolling();
    this.setupMicroInteractions();
    this.setupLoadingStates();
    this.setupSearchEnhancements();
    this.setupCardHoverEffects();
    this.setupNavbarEffects();
    this.setupRippleEffects();
    this.setupFloatingParticles();
  }

  // Advanced Intersection Observer with multiple thresholds
  setupAdvancedObservers() {
    const observerOptions = {
      threshold: [0, 0.1, 0.25, 0.5, 0.75, 1],
      rootMargin: '0px 0px -10% 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const element = entry.target;
        const ratio = entry.intersectionRatio;
        
        if (entry.isIntersecting) {
          // Progressive animation based on visibility
          if (ratio > 0.1) {
            element.classList.add('in-view');
            element.style.setProperty('--visibility-ratio', ratio);
          }
          
          // Trigger stagger animations
          if (element.classList.contains('stagger-container')) {
            setTimeout(() => {
              element.classList.add('animate');
            }, 100);
          }
          
          // Parallax calculations
          if (element.classList.contains('parallax-element')) {
            this.updateParallax(element, ratio);
          }
        } else {
          element.classList.remove('in-view');
        }
      });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.scroll-animate, .scroll-animate-left, .scroll-animate-right, .scroll-animate-scale, .stagger-container, .parallax-element').forEach(el => {
      observer.observe(el);
    });
  }

  // Magnetic hover effects for interactive elements
  setupMagneticElements() {
    document.querySelectorAll('.magnetic').forEach(element => {
      element.addEventListener('mousemove', (e) => {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const moveX = x * 0.15;
        const moveY = y * 0.15;
        
        element.style.setProperty('--mouse-x', `${moveX}px`);
        element.style.setProperty('--mouse-y', `${moveY}px`);
        
        element.style.transform = `translate(${moveX}px, ${moveY}px)`;
      });
      
      element.addEventListener('mouseleave', () => {
        element.style.transform = 'translate(0, 0)';
      });
    });
  }

  // Advanced parallax with multiple layers
  setupParallaxEffects() {
    let ticking = false;
    
    const updateParallax = () => {
      const scrolled = window.pageYOffset;
      
      document.querySelectorAll('.parallax-element').forEach(element => {
        const speed = element.dataset.speed || 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
      });
      
      // Update floating elements
      document.querySelectorAll('.animate-floating').forEach((element, index) => {
        const offset = Math.sin(Date.now() * 0.001 + index) * 15;
        element.style.transform = `translateY(${offset}px)`;
      });
      
      ticking = false;
    };
    
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    });
  }

  // Advanced ripple effects with color variations
  setupRippleEffects() {
    document.querySelectorAll('.btn-premium, .card-premium, .interactive-element').forEach(element => {
      element.addEventListener('click', (e) => {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        // Determine ripple color based on element type
        let rippleColor = 'rgba(255, 255, 255, 0.4)';
        if (element.classList.contains('btn-primary-premium')) {
          rippleColor = 'rgba(255, 255, 255, 0.5)';
        } else if (element.classList.contains('btn-secondary-premium')) {
          rippleColor = 'rgba(79, 70, 229, 0.4)';
        }
        
        ripple.style.cssText = `
          position: absolute;
          border-radius: 50%;
          background: ${rippleColor};
          width: ${size}px;
          height: ${size}px;
          left: ${x}px;
          top: ${y}px;
          transform: scale(0);
          animation: ripple-animation 0.6s linear;
          pointer-events: none;
          z-index: 1000;
        `;
        
        element.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });

    // Add ripple animation styles
    if (!document.querySelector('#ripple-styles')) {
      const style = document.createElement('style');
      style.id = 'ripple-styles';
      style.textContent = `
        @keyframes ripple-animation {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
        .btn-premium, .card-premium, .interactive-element {
          position: relative;
          overflow: hidden;
        }
      `;
      document.head.appendChild(style);
    }
  }

  // Enhanced card hover effects with 3D transforms
  setupCardHoverEffects() {
    document.querySelectorAll('.card-premium').forEach(card => {
      card.addEventListener('mouseenter', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        
        // Add enhanced glow effect
        card.style.boxShadow = `
          0 25px 50px rgba(0, 0, 0, 0.4),
          0 0 40px rgba(79, 70, 229, 0.3)
        `;
      });
      
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 8;
        const rotateY = (centerX - x) / 8;
        
        card.style.transform = `
          perspective(1000px) 
          rotateX(${rotateX}deg) 
          rotateY(${rotateY}deg) 
          translateZ(20px)
          scale(1.02)
        `;
        
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0) scale(1)';
        card.style.boxShadow = '';
      });
    });
  }

  // Advanced navbar with scroll direction detection
  setupNavbarEffects() {
    const navbar = document.querySelector('.nav-premium');
    if (!navbar) return;
    
    let lastScrollY = window.scrollY;
    let scrollDirection = 'up';
    
    window.addEventListener('scroll', () => {
      const currentScrollY = window.scrollY;
      scrollDirection = currentScrollY > lastScrollY ? 'down' : 'up';
      
      // Add scrolled class
      if (currentScrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      
      // Hide/show navbar based on scroll direction (mobile only)
      if (window.innerWidth <= 768) {
        if (scrollDirection === 'down' && currentScrollY > 200) {
          navbar.style.transform = 'translateY(-100%)';
        } else {
          navbar.style.transform = 'translateY(0)';
        }
      }
      
      lastScrollY = currentScrollY;
    });
  }

  // Advanced search with debouncing and suggestions
  setupSearchEnhancements() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    let searchTimeout;
    
    // Enhanced search functionality
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      
      // Add loading state
      searchInput.classList.add('searching');
      
      searchTimeout = setTimeout(() => {
        this.performAdvancedSearch(e.target.value);
        searchInput.classList.remove('searching');
      }, 300);
    });
    
    // Focus and blur events
    searchInput.addEventListener('focus', () => {
      searchInput.parentElement.classList.add('focused');
    });
    
    searchInput.addEventListener('blur', () => {
      searchInput.parentElement.classList.remove('focused');
    });
  }

  performAdvancedSearch(query) {
    // Add search analytics
    if (query.length > 2) {
      this.trackSearchAnalytics(query);
    }
  }

  trackSearchAnalytics(query) {
    // Track search patterns for UX improvements
    const searchData = {
      query: query,
      timestamp: Date.now(),
      userAgent: navigator.userAgent
    };
    
    // Store in localStorage for analytics
    const searches = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    searches.push(searchData);
    
    // Keep only last 50 searches
    if (searches.length > 50) {
      searches.shift();
    }
    
    localStorage.setItem('searchHistory', JSON.stringify(searches));
  }

  // Page transition effects
  setupPageTransitions() {
    // Add page transition on navigation
    document.addEventListener('DOMContentLoaded', () => {
      document.body.classList.add('page-transition-enter');
      
      setTimeout(() => {
        document.body.classList.add('page-transition-enter-active');
      }, 50);
    });
    
    // Handle link clicks for smooth transitions
    document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"]').forEach(link => {
      link.addEventListener('click', (e) => {
        if (e.ctrlKey || e.metaKey) return; // Allow opening in new tab
        
        // Skip if it's a same-page anchor link
        if (link.getAttribute('href').startsWith('#')) return;
        
        e.preventDefault();
        
        document.body.classList.add('page-transition-exit-active');
        
        setTimeout(() => {
          window.location.href = link.href;
        }, 300);
      });
    });
  }

  // Advanced loading states with skeleton screens
  setupLoadingStates() {
    // Create skeleton loaders for images
    document.querySelectorAll('img[data-src]').forEach(img => {
      const skeleton = this.createSkeleton(img);
      img.parentNode.insertBefore(skeleton, img);
      img.style.display = 'none';
      
      // Intersection observer for lazy loading
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            
            img.onload = () => {
              skeleton.remove();
              img.style.display = 'block';
              img.classList.add('animate-fade-in-scale');
            };
            
            imageObserver.unobserve(img);
          }
        });
      });
      
      imageObserver.observe(img);
    });
  }

  createSkeleton(element) {
    const skeleton = document.createElement('div');
    skeleton.className = 'shimmer';
    skeleton.style.width = element.getAttribute('width') || '100%';
    skeleton.style.height = element.getAttribute('height') || '200px';
    return skeleton;
  }

  // Micro-interactions for enhanced UX
  setupMicroInteractions() {
    // Button press feedback
    document.querySelectorAll('.btn-premium').forEach(button => {
      button.addEventListener('mousedown', () => {
        button.style.transform = 'scale(0.95)';
      });
      
      button.addEventListener('mouseup', () => {
        button.style.transform = '';
      });
      
      button.addEventListener('mouseleave', () => {
        button.style.transform = '';
      });
    });
    
    // Form input focus effects
    document.querySelectorAll('.form-premium').forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });
      
      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
      });
    });
  }

  // Smooth scrolling with easing
  setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        
        if (target) {
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
          const startPosition = window.pageYOffset;
          const distance = targetPosition - startPosition;
          const duration = 800;
          let start = null;
          
          const easeInOutCubic = (t) => {
            return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
          };
          
          const animation = (currentTime) => {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const progress = Math.min(timeElapsed / duration, 1);
            const ease = easeInOutCubic(progress);
            
            window.scrollTo(0, startPosition + distance * ease);
            
            if (timeElapsed < duration) {
              requestAnimationFrame(animation);
            }
          };
          
          requestAnimationFrame(animation);
        }
      });
    });
  }

  // Setup floating particles
  setupFloatingParticles() {
    // Add floating particles to hero sections
    document.querySelectorAll('.hero-section, .books-hero, .auth-hero').forEach(section => {
      this.createFloatingParticles(section, 12);
    });
  }

  // Utility method to create floating particles
  createFloatingParticles(container, count = 15) {
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.className = 'floating-particle';
      
      const size = Math.random() * 4 + 2;
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const duration = Math.random() * 4 + 3;
      const delay = Math.random() * 3;
      
      particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: rgba(79, 70, 229, 0.4);
        border-radius: 50%;
        left: ${x}%;
        top: ${y}%;
        animation: float ${duration}s ease-in-out infinite;
        animation-delay: ${delay}s;
        pointer-events: none;
        z-index: 1;
      `;
      
      container.appendChild(particle);
    }
  }

  // Performance monitoring
  static monitorPerformance() {
    if ('performance' in window) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          const perfData = performance.getEntriesByType('navigation')[0];
          console.log('Page Load Performance:', {
            domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
            loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
            totalTime: perfData.loadEventEnd - perfData.fetchStart
          });
        }, 0);
      });
    }
  }
}

// Enhanced page transition effects
class PageTransitions {
  static fadeIn() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    
    window.addEventListener('load', () => {
      document.body.style.opacity = '1';
    });
  }

  static slideIn() {
    const main = document.querySelector('main') || document.body;
    main.style.transform = 'translateY(40px)';
    main.style.opacity = '0';
    main.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    
    window.addEventListener('load', () => {
      main.style.transform = 'translateY(0)';
      main.style.opacity = '1';
    });
  }

  static morphIn() {
    const elements = document.querySelectorAll('.card-premium, .btn-premium');
    elements.forEach((element, index) => {
      element.style.opacity = '0';
      element.style.transform = 'scale(0.8) rotate(5deg)';
      element.style.transition = 'all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
      element.style.transitionDelay = `${index * 0.1}s`;
      
      setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'scale(1) rotate(0deg)';
      }, 100);
    });
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PremiumInteractions();
  PageTransitions.fadeIn();
  PremiumInteractions.monitorPerformance();
  
  // Add initial animation classes to elements
  document.querySelectorAll('.card-premium').forEach((card, index) => {
    card.classList.add('scroll-animate');
    card.style.animationDelay = `${index * 100}ms`;
  });
  
  // Initialize stagger containers
  document.querySelectorAll('.books-grid, .features-grid').forEach(container => {
    container.classList.add('stagger-container');
    container.querySelectorAll('.card-premium, .feature-card').forEach(item => {
      item.classList.add('stagger-item');
    });
  });
});

// Export for use in other scripts
window.PremiumInteractions = PremiumInteractions;
window.PageTransitions = PageTransitions;