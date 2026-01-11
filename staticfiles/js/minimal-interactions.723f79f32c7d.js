/* ========================================
   LIGHTWEIGHT PRODUCT UI INTERACTIONS
   Enhanced animations and micro-interactions
======================================== */

class ProductUI {
  constructor() {
    this.init();
  }

  init() {
    this.setupNavigation();
    this.setupLibraryFeatures();
    this.setupBookInteractions();
    this.setupAnimations();
    this.setupScrollEffects();
  }

  // Enhanced Navigation
  setupNavigation() {
    // Set active navigation state
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPath || (currentPath !== '/' && href !== '/' && currentPath.startsWith(href))) {
        link.classList.add('active');
      }
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      });
    }

    // Dropdown functionality
    this.setupDropdowns();

    // Mobile menu toggle (if needed)
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.navbar-nav');
    
    if (mobileToggle && navMenu) {
      mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
      });
    }
  }

  // Dropdown navigation setup
  setupDropdowns() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    
    dropdowns.forEach(dropdown => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      const menu = dropdown.querySelector('.dropdown-menu');
      
      if (!toggle || !menu) return;
      
      // Click to toggle dropdown
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        // Close other dropdowns
        dropdowns.forEach(other => {
          if (other !== dropdown) {
            other.classList.remove('active');
          }
        });
        
        // Toggle current dropdown
        dropdown.classList.toggle('active');
      });
      
      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          dropdown.classList.remove('active');
        }
      });
      
      // Close dropdown when pressing Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          dropdown.classList.remove('active');
        }
      });
      
      // Prevent dropdown menu clicks from closing the dropdown
      menu.addEventListener('click', (e) => {
        e.stopPropagation();
      });
    });
  }

  // Enhanced Library Features
  setupLibraryFeatures() {
    // Add to library functionality with animation
    const addToLibraryBtns = document.querySelectorAll('.add-to-library');
    addToLibraryBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.addToLibrary(btn);
      });
    });

    // Library category filtering with smooth transitions
    const categoryBtns = document.querySelectorAll('.library-category');
    categoryBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.filterLibraryByCategory(btn);
      });
    });
  }

  // Enhanced Book Interactions
  setupBookInteractions() {
    // Book card clicks with hover effects
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
      // Add staggered animation delay
      const index = Array.from(bookCards).indexOf(card);
      card.style.animationDelay = `${index * 0.1}s`;
      
      card.addEventListener('click', (e) => {
        // Don't navigate if clicking on buttons
        if (e.target.closest('.btn')) return;
        
        const bookUrl = card.dataset.bookUrl;
        if (bookUrl) {
          // Add loading state
          card.classList.add('loading');
          window.location.href = bookUrl;
        }
      });

      // Enhanced hover effects
      card.addEventListener('mouseenter', () => {
        this.animateBookCard(card, 'enter');
      });

      card.addEventListener('mouseleave', () => {
        this.animateBookCard(card, 'leave');
      });
    });

    // Enhanced image loading
    this.optimizeImageLoading();
  }

  // Animation system
  setupAnimations() {
    // Intersection Observer for scroll animations
    if ('IntersectionObserver' in window) {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      }, observerOptions);

      // Observe elements for animation
      document.querySelectorAll('.feature-card, .stat-card, .book-card').forEach(el => {
        observer.observe(el);
      });
    }

    // Button click animations
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.createRippleEffect(e, btn);
      });
    });
  }

  // Scroll effects
  setupScrollEffects() {
    // Parallax effect for hero section (lightweight)
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        heroSection.style.transform = `translateY(${rate}px)`;
      });
    }

    // Floating books animation
    const floatingBooks = document.querySelectorAll('.book-icon');
    floatingBooks.forEach((book, index) => {
      book.style.animationDelay = `${index * 0.5}s`;
    });
  }

  // Enhanced add to library with visual feedback
  addToLibrary(btn) {
    const bookId = btn.dataset.bookId;
    if (!bookId) return;

    // Show loading state with animation
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    btn.disabled = true;
    btn.classList.add('loading');

    // Make request to add book to library
    fetch('/library/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCSRFToken()
      },
      body: JSON.stringify({ book_id: bookId })
    })
    .then(response => response.json())
    .then(data => {
      btn.classList.remove('loading');
      
      if (data.success) {
        // Success animation
        btn.innerHTML = '<i class="fas fa-check"></i> Added to Library';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
        
        // Animate success
        btn.style.transform = 'scale(1.05)';
        setTimeout(() => {
          btn.style.transform = 'scale(1)';
        }, 200);
        
        this.showNotification(data.message, 'success');
      } else {
        // Reset on error
        btn.innerHTML = originalText;
        btn.disabled = false;
        this.showNotification(data.message || 'Failed to add book', 'error');
      }
    })
    .catch(error => {
      btn.classList.remove('loading');
      btn.innerHTML = originalText;
      btn.disabled = false;
      this.showNotification('Network error. Please try again.', 'error');
    });
  }

  // Enhanced library filtering with smooth transitions
  filterLibraryByCategory(btn) {
    const category = btn.dataset.category;
    
    // Update active state with animation
    document.querySelectorAll('.library-category').forEach(b => {
      b.classList.remove('active');
      b.style.transform = 'scale(1)';
    });
    
    btn.classList.add('active');
    btn.style.transform = 'scale(1.05)';
    setTimeout(() => {
      btn.style.transform = 'scale(1)';
    }, 200);

    // Filter books with staggered animation
    const books = document.querySelectorAll('.library-book');
    books.forEach((book, index) => {
      setTimeout(() => {
        if (category === 'all' || book.dataset.category === category) {
          book.style.display = 'block';
          book.style.animation = `slideUp 0.4s ease-out ${index * 0.05}s both`;
        } else {
          book.style.animation = 'fadeOut 0.3s ease-out both';
          setTimeout(() => {
            book.style.display = 'none';
          }, 300);
        }
      }, index * 20);
    });
  }

  // Book card hover animations
  animateBookCard(card, action) {
    const cover = card.querySelector('.book-cover img');
    const info = card.querySelector('.book-info');
    
    if (action === 'enter') {
      if (cover) {
        cover.style.transform = 'scale(1.05)';
      }
      if (info) {
        info.style.transform = 'translateY(-2px)';
      }
    } else {
      if (cover) {
        cover.style.transform = 'scale(1)';
      }
      if (info) {
        info.style.transform = 'translateY(0)';
      }
    }
  }

  // Enhanced image loading with lazy loading and error handling
  optimizeImageLoading() {
    const images = document.querySelectorAll('.book-cover img, .book-cover-large img');
    
    images.forEach(img => {
      // Add loading class
      img.classList.add('loading');
      
      img.addEventListener('load', function() {
        this.classList.remove('loading');
        this.style.opacity = '1';
        
        // Fade in animation
        this.style.animation = 'fadeIn 0.5s ease-out';
      });
      
      img.addEventListener('error', function() {
        this.classList.remove('loading');
        const placeholder = document.createElement('div');
        placeholder.className = this.closest('.book-cover-large') ? 'book-cover-large-placeholder' : 'book-cover-placeholder';
        placeholder.innerHTML = `
          <i class="fas fa-file-pdf"></i>
          <div class="placeholder-text">PDF Book</div>
        `;
        this.parentNode.replaceChild(placeholder, this);
      });
      
      // Set initial opacity for smooth loading
      if (!img.complete) {
        img.style.opacity = '0';
      }
    });

    // Intersection Observer for lazy loading
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.removeAttribute('data-src');
              observer.unobserve(img);
            }
          }
        });
      });
      
      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  }

  // Ripple effect for buttons
  createRippleEffect(event, button) {
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
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
  }

  // Enhanced notification system
  showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    // Create notification with enhanced styling
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <i class="fas fa-${this.getNotificationIcon(type)}"></i>
        <span>${message}</span>
      </div>
      <button class="notification-close">&times;</button>
    `;

    // Enhanced styles
    notification.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-primary);
      border-radius: var(--radius-lg);
      padding: var(--space-4);
      color: var(--text-primary);
      z-index: 1001;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-3);
      box-shadow: var(--shadow-lg);
      max-width: 350px;
      min-width: 300px;
      animation: slideInRight 0.3s ease-out;
      backdrop-filter: blur(10px);
    `;

    // Type-specific styling
    if (type === 'success') {
      notification.style.borderColor = 'var(--success)';
    } else if (type === 'error') {
      notification.style.borderColor = 'var(--error)';
    }

    document.body.appendChild(notification);

    // Close functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
      notification.style.animation = 'slideOutRight 0.3s ease-out';
      setTimeout(() => notification.remove(), 300);
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
      }
    }, 5000);
  }

  // Helper methods
  getNotificationIcon(type) {
    switch (type) {
      case 'success': return 'check-circle';
      case 'error': return 'exclamation-triangle';
      case 'warning': return 'exclamation-circle';
      default: return 'info-circle';
    }
  }

  getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
  }

  // Utility: Debounce function
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
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
  
  @keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
  
  @keyframes ripple {
    to { transform: scale(2); opacity: 0; }
  }
  
  .animate-in {
    animation: slideUp 0.6s ease-out both;
  }
  
  .notification-content {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }
  
  .notification-close {
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.2em;
    cursor: pointer;
    padding: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all var(--transition-fast);
  }
  
  .notification-close:hover {
    background: var(--bg-elevated);
    color: var(--text-primary);
  }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.productUI = new ProductUI();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProductUI;
}