/**
 * TechBookHub Library Manager
 * Shared library management functionality across all pages
 * Ensures consistent state and behavior
 */

class LibraryManager {
  constructor() {
    this.processingRequests = new Set();
    this.init();
  }

  init() {
    console.log('LibraryManager initialized');
    this.attachEventListeners();
  }

  attachEventListeners() {
    // Use event delegation for dynamic content
    document.addEventListener('click', (e) => {
      const addButton = e.target.closest('.add-to-library');
      const removeButton = e.target.closest('.remove-from-library') || e.target.closest('.library-remove-btn');

      if (addButton) {
        e.preventDefault();
        e.stopImmediatePropagation();
        this.handleAddToLibrary(addButton);
        return false;
      }

      if (removeButton) {
        e.preventDefault();
        e.stopImmediatePropagation();
        this.handleRemoveFromLibrary(removeButton);
        return false;
      }
    }, true);
  }

  async handleAddToLibrary(button) {
    const bookId = button.dataset.bookId;
    
    if (this.processingRequests.has(`add-${bookId}`)) {
      console.log('Add request already in progress for book:', bookId);
      return;
    }

    console.log('Adding book to library:', bookId);

    const csrfToken = this.getCsrfToken();
    if (!csrfToken) {
      this.showNotification('Security token missing. Please refresh the page.', 'error');
      return;
    }

    this.processingRequests.add(`add-${bookId}`);
    this.setButtonLoading(button, true, 'Adding...');

    try {
      const response = await fetch('/library/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ book_id: parseInt(bookId) })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
      }

      const data = await response.json();
      console.log('Add response:', data);

      if (data.success) {
        this.updateButtonToRemoveState(button);
        this.showNotification(data.message, 'success');
      } else {
        this.setButtonLoading(button, false);
        this.showNotification(data.message, 'error');
      }
    } catch (error) {
      console.error('Add to library error:', error);
      this.setButtonLoading(button, false);
      this.showNotification(`Error: ${error.message}`, 'error');
    } finally {
      this.processingRequests.delete(`add-${bookId}`);
    }
  }

  async handleRemoveFromLibrary(button) {
    const bookId = button.dataset.bookId;
    
    if (this.processingRequests.has(`remove-${bookId}`)) {
      console.log('Remove request already in progress for book:', bookId);
      return;
    }

    console.log('Removing book from library:', bookId);

    // Check if we're on the library page (different behavior)
    const isLibraryPage = window.location.pathname.includes('/library/');
    
    if (isLibraryPage && !confirm('Remove this technical book from your library?')) {
      return;
    }

    const csrfToken = this.getCsrfToken();
    if (!csrfToken) {
      this.showNotification('Security token missing. Please refresh the page.', 'error');
      return;
    }

    this.processingRequests.add(`remove-${bookId}`);
    this.setButtonLoading(button, true, 'Removing...');

    try {
      const response = await fetch('/library/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ book_id: parseInt(bookId) })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
      }

      const data = await response.json();
      console.log('Remove response:', data);

      if (data.success) {
        if (isLibraryPage) {
          this.removeBookCardFromLibrary(button);
        } else {
          this.updateButtonToAddState(button);
        }
        this.showNotification(data.message, 'success');
      } else {
        this.setButtonLoading(button, false);
        this.showNotification(data.message, 'error');
      }
    } catch (error) {
      console.error('Remove from library error:', error);
      this.setButtonLoading(button, false);
      this.showNotification(`Error: ${error.message}`, 'error');
    } finally {
      this.processingRequests.delete(`remove-${bookId}`);
    }
  }

  updateButtonToRemoveState(button) {
    button.className = 'btn btn-danger btn-sm remove-from-library';
    button.innerHTML = '<i class="fas fa-bookmark-slash"></i> Remove';
    button.disabled = false;
  }

  updateButtonToAddState(button) {
    button.className = 'btn btn-primary btn-sm add-to-library';
    button.innerHTML = '<i class="fas fa-bookmark"></i> Add to Library';
    button.disabled = false;
  }

  setButtonLoading(button, isLoading, text = '') {
    if (isLoading) {
      button.disabled = true;
      button.dataset.originalContent = button.innerHTML;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i>${text ? ' ' + text : ''}`;
    } else {
      button.disabled = false;
      if (button.dataset.originalContent) {
        button.innerHTML = button.dataset.originalContent;
        delete button.dataset.originalContent;
      }
    }
  }

  removeBookCardFromLibrary(button) {
    const bookCard = button.closest('.tech-book-card');
    if (!bookCard) {
      console.error('Could not find book card to remove');
      return;
    }

    console.log('Removing book card from library page');

    // Animate removal
    bookCard.style.transition = 'all 0.3s ease-out';
    bookCard.style.opacity = '0';
    bookCard.style.transform = 'scale(0.95) translateY(-10px)';

    setTimeout(() => {
      bookCard.remove();

      // Check if library is now empty
      const remainingBooks = document.querySelectorAll('.tech-book-card');
      console.log('Remaining books after removal:', remainingBooks.length);
      
      if (remainingBooks.length === 0) {
        console.log('Library is empty, reloading to show empty state');
        window.location.reload();
      }
    }, 300);
  }

  getCsrfToken() {
    // Try multiple sources for CSRF token
    const sources = [
      () => document.querySelector('[name=csrfmiddlewaretoken]')?.value,
      () => document.querySelector('meta[name="csrf-token"]')?.getAttribute('content'),
      () => {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
          const [name, value] = cookie.trim().split('=');
          if (name === 'csrftoken') return value;
        }
        return null;
      }
    ];

    for (const getToken of sources) {
      const token = getToken();
      if (token) {
        console.log('CSRF token found');
        return token;
      }
    }

    console.error('CSRF token not found');
    return null;
  }

  showNotification(message, type) {
    // Remove existing notifications
    document.querySelectorAll('.notification-toast').forEach(n => n.remove());

    const notification = document.createElement('div');
    notification.className = 'notification-toast';
    notification.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      background: ${type === 'success' ? 'var(--success)' : 'var(--error)'};
      color: white;
      padding: 12px 16px;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      z-index: 1001;
      font-size: var(--font-size-sm);
      font-weight: 500;
      max-width: 300px;
      opacity: 0;
      transform: translateX(100%);
      transition: all var(--transition-smooth);
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Animate in
    requestAnimationFrame(() => {
      notification.style.opacity = '1';
      notification.style.transform = 'translateX(0)';
    });

    // Auto remove
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 250);
      }
    }, 3000);
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new LibraryManager());
} else {
  new LibraryManager();
}

// Export for potential use in other scripts
window.LibraryManager = LibraryManager;