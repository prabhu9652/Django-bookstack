/**
 * TechBookHub PWA Manager
 * Handles service worker registration, install prompts, and offline detection
 */

(function() {
  'use strict';

  const PWA = {
    deferredPrompt: null,
    isInstalled: false,
    isOnline: navigator.onLine,
    swRegistration: null,

    /**
     * Initialize PWA functionality
     */
    init() {
      this.checkInstallState();
      this.registerServiceWorker();
      this.setupInstallPrompt();
      this.setupOnlineOfflineHandlers();
      this.setupUpdateHandler();
    },

    /**
     * Check if app is already installed
     */
    checkInstallState() {
      // Check display-mode
      if (window.matchMedia('(display-mode: standalone)').matches) {
        this.isInstalled = true;
        document.documentElement.classList.add('pwa-installed');
      }

      // iOS Safari check
      if (window.navigator.standalone === true) {
        this.isInstalled = true;
        document.documentElement.classList.add('pwa-installed');
      }

      // Listen for display mode changes
      window.matchMedia('(display-mode: standalone)').addEventListener('change', (e) => {
        this.isInstalled = e.matches;
        document.documentElement.classList.toggle('pwa-installed', e.matches);
      });
    },

    /**
     * Register Service Worker
     */
    async registerServiceWorker() {
      if (!('serviceWorker' in navigator)) {
        console.log('[PWA] Service workers not supported');
        return;
      }

      try {
        this.swRegistration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/'
        });

        console.log('[PWA] Service worker registered:', this.swRegistration.scope);

        // Check for updates periodically
        setInterval(() => {
          this.swRegistration.update();
        }, 60 * 60 * 1000); // Check every hour

      } catch (error) {
        console.error('[PWA] Service worker registration failed:', error);
      }
    },

    /**
     * Setup install prompt handling
     */
    setupInstallPrompt() {
      // Capture the install prompt
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        this.deferredPrompt = e;
        
        // Show install button after user has engaged with the app
        setTimeout(() => {
          this.showInstallButton();
        }, 30000); // Wait 30 seconds before showing

        console.log('[PWA] Install prompt captured');
      });

      // Track successful installation
      window.addEventListener('appinstalled', () => {
        this.isInstalled = true;
        this.deferredPrompt = null;
        this.hideInstallButton();
        document.documentElement.classList.add('pwa-installed');
        console.log('[PWA] App installed successfully');
        
        // Show success message
        this.showNotification('App installed successfully!', 'success');
      });
    },

    /**
     * Show install button in UI
     */
    showInstallButton() {
      if (this.isInstalled || !this.deferredPrompt) return;

      // Check if user has dismissed before
      const dismissed = localStorage.getItem('pwa-install-dismissed');
      if (dismissed) {
        const dismissedTime = parseInt(dismissed, 10);
        const daysSinceDismissed = (Date.now() - dismissedTime) / (1000 * 60 * 60 * 24);
        if (daysSinceDismissed < 7) return; // Don't show for 7 days after dismiss
      }

      // Create install banner
      const banner = document.createElement('div');
      banner.id = 'pwa-install-banner';
      banner.innerHTML = `
        <div class="pwa-install-content">
          <div class="pwa-install-icon">
            <i class="fas fa-mobile-alt"></i>
          </div>
          <div class="pwa-install-text">
            <strong>Install TechBookHub</strong>
            <span>Add to home screen for quick access</span>
          </div>
          <div class="pwa-install-actions">
            <button class="pwa-install-btn" id="pwaInstallBtn">Install</button>
            <button class="pwa-dismiss-btn" id="pwaDismissBtn">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(banner);

      // Animate in
      requestAnimationFrame(() => {
        banner.classList.add('show');
      });

      // Setup button handlers
      document.getElementById('pwaInstallBtn').addEventListener('click', () => {
        this.promptInstall();
      });

      document.getElementById('pwaDismissBtn').addEventListener('click', () => {
        this.dismissInstallBanner();
      });
    },

    /**
     * Hide install button
     */
    hideInstallButton() {
      const banner = document.getElementById('pwa-install-banner');
      if (banner) {
        banner.classList.remove('show');
        setTimeout(() => banner.remove(), 300);
      }
    },

    /**
     * Dismiss install banner
     */
    dismissInstallBanner() {
      localStorage.setItem('pwa-install-dismissed', Date.now().toString());
      this.hideInstallButton();
    },

    /**
     * Trigger install prompt
     */
    async promptInstall() {
      if (!this.deferredPrompt) {
        console.log('[PWA] No install prompt available');
        return;
      }

      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      
      console.log('[PWA] Install prompt outcome:', outcome);
      
      if (outcome === 'accepted') {
        this.hideInstallButton();
      }
      
      this.deferredPrompt = null;
    },

    /**
     * Setup online/offline handlers
     */
    setupOnlineOfflineHandlers() {
      const updateOnlineStatus = () => {
        const wasOnline = this.isOnline;
        this.isOnline = navigator.onLine;
        
        document.documentElement.classList.toggle('offline', !this.isOnline);
        
        if (wasOnline && !this.isOnline) {
          this.showNotification('You are offline. Some features may be limited.', 'warning');
        } else if (!wasOnline && this.isOnline) {
          this.showNotification('Back online!', 'success');
        }
      };

      window.addEventListener('online', updateOnlineStatus);
      window.addEventListener('offline', updateOnlineStatus);
      
      // Initial check
      updateOnlineStatus();
    },

    /**
     * Setup service worker update handler
     */
    setupUpdateHandler() {
      if (!('serviceWorker' in navigator)) return;

      navigator.serviceWorker.addEventListener('controllerchange', () => {
        // New service worker has taken control
        this.showUpdateNotification();
      });
    },

    /**
     * Show update notification
     */
    showUpdateNotification() {
      const notification = document.createElement('div');
      notification.id = 'pwa-update-notification';
      notification.innerHTML = `
        <div class="pwa-update-content">
          <i class="fas fa-sync-alt"></i>
          <span>A new version is available</span>
          <button class="pwa-update-btn" onclick="location.reload()">Refresh</button>
        </div>
      `;
      
      document.body.appendChild(notification);
      
      requestAnimationFrame(() => {
        notification.classList.add('show');
      });
    },

    /**
     * Show notification toast
     */
    showNotification(message, type = 'info') {
      // Remove existing notification
      const existing = document.getElementById('pwa-notification');
      if (existing) existing.remove();

      const notification = document.createElement('div');
      notification.id = 'pwa-notification';
      notification.className = `pwa-notification ${type}`;
      
      const icons = {
        success: 'fa-check-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-times-circle',
        info: 'fa-info-circle'
      };

      notification.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
      `;

      document.body.appendChild(notification);

      requestAnimationFrame(() => {
        notification.classList.add('show');
      });

      // Auto-hide after 4 seconds
      setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
      }, 4000);
    },

    /**
     * Clear all caches (for logout)
     */
    async clearCaches() {
      if (!this.swRegistration) return;

      return new Promise((resolve) => {
        const messageChannel = new MessageChannel();
        messageChannel.port1.onmessage = (event) => {
          resolve(event.data);
        };
        
        navigator.serviceWorker.controller?.postMessage(
          { type: 'CLEAR_CACHE' },
          [messageChannel.port2]
        );
      });
    },

    /**
     * Pre-cache specific URLs
     */
    async cacheUrls(urls) {
      if (!this.swRegistration) return;

      return new Promise((resolve) => {
        const messageChannel = new MessageChannel();
        messageChannel.port1.onmessage = (event) => {
          resolve(event.data);
        };
        
        navigator.serviceWorker.controller?.postMessage(
          { type: 'CACHE_URLS', payload: { urls } },
          [messageChannel.port2]
        );
      });
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => PWA.init());
  } else {
    PWA.init();
  }

  // Expose PWA manager globally
  window.TechBookHubPWA = PWA;

})();
