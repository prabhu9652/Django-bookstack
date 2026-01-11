/**
 * Image Loader - Progressive image loading with performance optimizations
 * Handles lazy loading, loading states, and error fallbacks
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    rootMargin: '50px 0px', // Start loading 50px before entering viewport
    threshold: 0.01,
    retryAttempts: 2,
    retryDelay: 1000
  };

  // Track loaded images to prevent duplicate processing
  const loadedImages = new Set();

  /**
   * Initialize image loading optimizations
   */
  function initImageLoader() {
    // Process all book cover images
    const bookCovers = document.querySelectorAll('.book-cover, .book-cover-large');
    
    bookCovers.forEach(container => {
      const img = container.querySelector('img');
      if (img) {
        setupImageLoading(container, img);
      }
    });

    // Set up Intersection Observer for lazy loading (fallback for browsers without native support)
    if ('IntersectionObserver' in window) {
      setupIntersectionObserver();
    }

    // Listen for dynamically added content
    observeDOMChanges();
  }

  /**
   * Set up loading behavior for a single image
   */
  function setupImageLoading(container, img) {
    // Skip if already processed
    if (loadedImages.has(img)) return;
    loadedImages.add(img);

    // Check if image is already loaded (cached)
    if (img.complete && img.naturalHeight !== 0) {
      handleImageLoaded(container, img);
      return;
    }

    // Set up load handler
    img.addEventListener('load', function onLoad() {
      handleImageLoaded(container, img);
      img.removeEventListener('load', onLoad);
    });

    // Set up error handler with retry logic
    let retryCount = 0;
    img.addEventListener('error', function onError() {
      if (retryCount < CONFIG.retryAttempts) {
        retryCount++;
        setTimeout(() => {
          // Try reloading with cache-busting parameter
          const originalSrc = img.dataset.originalSrc || img.src;
          img.dataset.originalSrc = originalSrc;
          img.src = originalSrc + (originalSrc.includes('?') ? '&' : '?') + 'retry=' + retryCount;
        }, CONFIG.retryDelay);
      } else {
        handleImageError(container, img);
        img.removeEventListener('error', onError);
      }
    });
  }

  /**
   * Handle successful image load
   */
  function handleImageLoaded(container, img) {
    // Add loaded class to image
    img.classList.add('loaded');
    
    // Add loaded class to container (hides skeleton)
    container.classList.add('loaded');
    container.classList.remove('error');

    // Trigger custom event for analytics or other handlers
    container.dispatchEvent(new CustomEvent('imageLoaded', {
      bubbles: true,
      detail: { src: img.src }
    }));
  }

  /**
   * Handle image load error
   */
  function handleImageError(container, img) {
    container.classList.add('error');
    container.classList.remove('loaded');
    
    // Hide the broken image
    img.style.display = 'none';
    
    // Show placeholder if it exists
    const placeholder = container.querySelector('.book-cover-placeholder, .book-cover-large-placeholder');
    if (placeholder) {
      placeholder.style.display = 'flex';
    } else {
      // Create a placeholder if none exists
      createPlaceholder(container);
    }

    // Log error for debugging (only in development)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.warn('Image failed to load:', img.dataset.originalSrc || img.src);
    }
  }

  /**
   * Create a placeholder element for failed images
   */
  function createPlaceholder(container) {
    const isLarge = container.classList.contains('book-cover-large');
    const placeholderClass = isLarge ? 'book-cover-large-placeholder' : 'book-cover-placeholder';
    
    const placeholder = document.createElement('div');
    placeholder.className = placeholderClass;
    placeholder.innerHTML = `
      <i class="fas fa-file-code"></i>
      <span${isLarge ? ' class="placeholder-text"' : ''}>Technical Book</span>
    `;
    
    container.appendChild(placeholder);
  }

  /**
   * Set up Intersection Observer for enhanced lazy loading
   */
  function setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const container = entry.target;
          const img = container.querySelector('img[data-src]');
          
          if (img && img.dataset.src) {
            // Load the actual image
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          
          // Stop observing this element
          observer.unobserve(container);
        }
      });
    }, {
      rootMargin: CONFIG.rootMargin,
      threshold: CONFIG.threshold
    });

    // Observe all book covers with data-src images
    document.querySelectorAll('.book-cover, .book-cover-large').forEach(container => {
      const img = container.querySelector('img[data-src]');
      if (img) {
        observer.observe(container);
      }
    });
  }

  /**
   * Observe DOM changes for dynamically added images
   */
  function observeDOMChanges() {
    if (!('MutationObserver' in window)) return;

    const observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Check if the added node is a book cover
            if (node.matches && (node.matches('.book-cover') || node.matches('.book-cover-large'))) {
              const img = node.querySelector('img');
              if (img) {
                setupImageLoading(node, img);
              }
            }
            
            // Check for book covers within the added node
            const covers = node.querySelectorAll ? node.querySelectorAll('.book-cover, .book-cover-large') : [];
            covers.forEach(container => {
              const img = container.querySelector('img');
              if (img) {
                setupImageLoading(container, img);
              }
            });
          }
        });
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  /**
   * Preload critical images (above the fold)
   */
  function preloadCriticalImages() {
    // Get first 4 book covers (typically visible on initial load)
    const criticalCovers = document.querySelectorAll('.book-cover img, .book-cover-large img');
    const toPreload = Array.from(criticalCovers).slice(0, 4);

    toPreload.forEach(img => {
      if (img.src && !img.complete) {
        // Create a preload link
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = img.src;
        document.head.appendChild(link);
      }
    });
  }

  /**
   * Get image loading performance metrics
   */
  function getPerformanceMetrics() {
    if (!('performance' in window)) return null;

    const entries = performance.getEntriesByType('resource')
      .filter(entry => entry.initiatorType === 'img')
      .filter(entry => entry.name.includes('/media/'));

    return {
      totalImages: entries.length,
      averageLoadTime: entries.length > 0 
        ? entries.reduce((sum, e) => sum + e.duration, 0) / entries.length 
        : 0,
      slowestImage: entries.length > 0 
        ? entries.reduce((max, e) => e.duration > max.duration ? e : max, entries[0])
        : null
    };
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initImageLoader();
      preloadCriticalImages();
    });
  } else {
    initImageLoader();
    preloadCriticalImages();
  }

  // Expose API for debugging and external use
  window.ImageLoader = {
    init: initImageLoader,
    preloadCritical: preloadCriticalImages,
    getMetrics: getPerformanceMetrics
  };

})();
