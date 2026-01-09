/* ========================================
   MINIMAL ENTERPRISE INTERACTIONS
   Lightweight JavaScript for Core Functionality
======================================== */

class MinimalUI {
  constructor() {
    this.init();
  }

  init() {
    this.setupNavigation();
    this.setupLibraryFeatures();
    this.setupBookInteractions();
  }

  // Navigation
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

    // Mobile menu toggle (if needed)
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.navbar-nav');
    
    if (mobileToggle && navMenu) {
      mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
      });
    }
  }

  // Library Features
  setupLibraryFeatures() {
    // Add to library functionality
    const addToLibraryBtns = document.querySelectorAll('.add-to-library');
    addToLibraryBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.addToLibrary(btn);
      });
    });

    // Library category filtering
    const categoryBtns = document.querySelectorAll('.library-category');
    categoryBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.filterLibraryByCategory(btn);
      });
    });
  }

  // Book Interactions
  setupBookInteractions() {
    // Book card clicks
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
      card.addEventListener('click', (e) => {
        // Don't navigate if clicking on buttons
        if (e.target.closest('.btn')) return;
        
        const bookUrl = card.dataset.bookUrl;
        if (bookUrl) {
          window.location.href = bookUrl;
        }
      });
    });

    // PDF viewer optimization
    this.optimizePDFViewer();
  }

  // Add book to user library
  addToLibrary(btn) {
    const bookId = btn.dataset.bookId;
    if (!bookId) return;

    // Show loading state
    const originalText = btn.textContent;
    btn.textContent = 'Adding...';
    btn.disabled = true;

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
      if (data.success) {
        btn.textContent = 'Added to Library';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
        this.showNotification('Book added to your library', 'success');
      } else {
        btn.textContent = originalText;
        btn.disabled = false;
        this.showNotification(data.message || 'Failed to add book', 'error');
      }
    })
    .catch(error => {
      btn.textContent = originalText;
      btn.disabled = false;
      this.showNotification('Network error. Please try again.', 'error');
    });
  }

  // Filter library books by category
  filterLibraryByCategory(btn) {
    const category = btn.dataset.category;
    
    // Update active state
    document.querySelectorAll('.library-category').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Filter books
    const books = document.querySelectorAll('.library-book');
    books.forEach(book => {
      if (category === 'all' || book.dataset.category === category) {
        book.style.display = 'block';
      } else {
        book.style.display = 'none';
      }
    });
  }

  // Optimize PDF viewer
  optimizePDFViewer() {
    const pdfViewers = document.querySelectorAll('.pdf-viewer iframe');
    pdfViewers.forEach(iframe => {
      // Add loading indicator
      const loader = document.createElement('div');
      loader.className = 'pdf-loader';
      loader.innerHTML = '<div class="loading-spinner"></div><p>Loading PDF...</p>';
      iframe.parentNode.insertBefore(loader, iframe);

      iframe.addEventListener('load', () => {
        loader.remove();
      });

      // Handle PDF load errors
      iframe.addEventListener('error', () => {
        loader.innerHTML = '<p>Failed to load PDF. Please try again.</p>';
      });
    });
  }

  // Show notification
  showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <span>${message}</span>
      <button class="notification-close">&times;</button>
    `;

    // Add styles
    notification.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-primary);
      border-radius: var(--radius-md);
      padding: var(--space-3) var(--space-4);
      color: var(--text-primary);
      z-index: 1001;
      display: flex;
      align-items: center;
      gap: var(--space-3);
      box-shadow: var(--shadow-md);
      max-width: 300px;
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
    closeBtn.addEventListener('click', () => notification.remove());

    // Auto remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }

  // Get CSRF token
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

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.minimalUI = new MinimalUI();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MinimalUI;
}