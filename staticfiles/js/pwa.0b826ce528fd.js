/**
 * TechBookHub PWA Manager
 * Production-grade PWA handling with cross-platform support
 * Handles service worker, install prompts, offline detection, and updates
 */

(function() {
  'use strict';

  const PWA = {
    deferredPrompt: null,
    isInstalled: false,
    isOnline: navigator.onLine,
    swRegistration: null,
    platform: null,

    /**
     * Initialize PWA functionality
     */
    init() {
      this.detectPlatform();
      this.checkInstallState();
      this.registerServiceWorker();
      this.setupInstallPrompt();
      this.setupOnlineOfflineHandlers();
      this.setupUpdateHandler();
      this.setupAppPageHandlers();
      this.applyPlatformOptimizations();
    },

    /**
     * Detect platform for optimizations
     */
    detectPlatform() {
      const ua = navigator.userAgent.toLowerCase();
      const standalone = window.matchMedia('(display-mode: standalone)').matches;
      
      if (/iphone|ipad|ipod/.test(ua)) {
        this.platform = 'ios';
        document.documentElement.classList.add('platform-ios');
      } else if (/android/.test(ua)) {
        this.platform = 'android';
        document.documentElement.classList.add('platform-android');
      } else if (/windows/.test(ua)) {
        this.platform = 'windows';
        document.documentElement.classList.add('platform-windows');
      } else if (/macintosh|mac os x/.test(ua)) {
        this.platform = 'macos';
        document.documentElement.classList.add('platform-macos');
      } else {
        this.platform = 'other';
      }
      
      // Add standalone class if running as PWA
      if (standalone || window.navigator.standalone) {
        document.documentElement.classList.add('pwa-standalone');
      }
    },

    /**
     * Apply platform-specific optimizations
     */
    applyPlatformOptimizations() {
      // iOS-specific: Prevent bounce scroll
      if (this.platform === 'ios') {
        document.body.style.overscrollBehavior = 'none';
      }
      
      // Prevent pull-to-refresh in standalone mode
      if (this.isInstalled) {
        document.body.style.overscrollBehavior = 'none';
      }
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
          scope: '/',
          updateViaCache: 'none'
        });

        console.log('[PWA] Service worker registered:', this.swRegistration.scope);

        // Check for updates on page load
        this.swRegistration.update();

        // Check for updates periodically (every 30 minutes)
        setInterval(() => {
          this.swRegistration.update();
        }, 30 * 60 * 1000);

        // Handle waiting service worker
        if (this.swRegistration.waiting) {
          this.showUpdateNotification();
        }

        // Listen for new service worker
        this.swRegistration.addEventListener('updatefound', () => {
          const newWorker = this.swRegistration.installing;
          
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.showUpdateNotification();
            }
          });
        });

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
        
        // Show install button after user engagement (20 seconds)
        setTimeout(() => {
          this.showInstallButton();
        }, 20000);

        // Also enable any install buttons on the page
        this.enableInstallButtons();

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
        this.showNotification('TechBookHub installed successfully!', 'success');
        
        // Track installation (analytics)
        this.trackEvent('pwa_installed', { platform: this.platform });
      });
    },

    /**
     * Enable install buttons on the page (e.g., on /app/ page)
     */
    enableInstallButtons() {
      const installButtons = document.querySelectorAll('[data-pwa-install], #heroInstallBtn, .btn-app-install');
      
      installButtons.forEach(btn => {
        btn.disabled = false;
        btn.classList.remove('disabled');
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          this.promptInstall();
        });
      });
    },

    /**
     * Setup handlers for the /app/ page
     */
    setupAppPageHandlers() {
      // Hero install button
      const heroInstallBtn = document.getElementById('heroInstallBtn');
      if (heroInstallBtn) {
        heroInstallBtn.addEventListener('click', (e) => {
          e.preventDefault();
          if (this.deferredPrompt) {
            this.promptInstall();
          } else if (this.platform === 'ios') {
            this.showIOSInstallInstructions();
          } else {
            this.showNotification('Install option not available. Try using Chrome or Edge.', 'info');
          }
        });
        
        // Update button state
        this.updateInstallButtonState(heroInstallBtn);
      }
      
      // Update install status text
      const installStatus = document.getElementById('installStatus');
      if (installStatus) {
        if (this.isInstalled) {
          installStatus.textContent = 'App is installed';
          installStatus.style.color = '#22c55e';
        } else if (this.platform === 'ios') {
          installStatus.textContent = 'Use Safari\'s Share menu to install';
        }
      }
    },

    /**
     * Update install button state based on platform
     */
    updateInstallButtonState(btn) {
      if (this.isInstalled) {
        btn.innerHTML = '<i class="fas fa-check"></i> Installed';
        btn.disabled = true;
        btn.classList.add('installed');
      } else if (this.platform === 'ios') {
        btn.innerHTML = '<i class="fas fa-share-square"></i> Add to Home Screen';
      }
    },

    /**
     * Show iOS-specific install instructions
     */
    showIOSInstallInstructions() {
      const modal = document.createElement('div');
      modal.className = 'ios-install-modal';
      modal.innerHTML = `
        <div class="ios-install-content">
          <button class="ios-install-close" aria-label="Close">&times;</button>
          <div class="ios-install-icon">
            <i class="fas fa-share-square"></i>
          </div>
          <h3>Install TechBookHub</h3>
          <p>To install this app on your iPhone or iPad:</p>
          <ol>
            <li>Tap the <strong>Share</strong> button <i class="fas fa-share-square"></i> in Safari</li>
            <li>Scroll down and tap <strong>"Add to Home Screen"</strong></li>
            <li>Tap <strong>"Add"</strong> to confirm</li>
          </ol>
        </div>
      `;
      
      document.body.appendChild(modal);
      
      // Add styles
      const style = document.createElement('style');
      style.textContent = `
        .ios-install-modal {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 10000;
          padding: 20px;
          animation: fadeIn 0.2s ease;
        }
        .ios-install-content {
          background: var(--bg-surface, #1a1f26);
          border-radius: 16px;
          padding: 32px 24px;
          max-width: 340px;
          text-align: center;
          position: relative;
        }
        .ios-install-close {
          position: absolute;
          top: 12px;
          right: 12px;
          background: none;
          border: none;
          font-size: 24px;
          color: var(--text-secondary);
          cursor: pointer;
        }
        .ios-install-icon {
          width: 64px;
          height: 64px;
          background: linear-gradient(135deg, #4a9eff, #6366f1);
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 20px;
        }
        .ios-install-icon i {
          font-size: 28px;
          color: white;
        }
        .ios-install-content h3 {
          font-size: 20px;
          margin-bottom: 12px;
          color: var(--text-primary, #e7e9ea);
        }
        .ios-install-content p {
          color: var(--text-secondary, #71767b);
          margin-bottom: 16px;
        }
        .ios-install-content ol {
          text-align: left;
          padding-left: 20px;
          color: var(--text-primary, #e7e9ea);
        }
        .ios-install-content li {
          margin-bottom: 12px;
          line-height: 1.5;
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `;
      document.head.appendChild(style);
      
      // Close handlers
      modal.querySelector('.ios-install-close').addEventListener('click', () => modal.remove());
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
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
        if (daysSinceDismissed < 7) return;
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
            <button class="pwa-dismiss-btn" id="pwaDismissBtn" aria-label="Dismiss">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(banner);

      // Animate in
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          banner.classList.add('show');
        });
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
        return false;
      }

      try {
        this.deferredPrompt.prompt();
        const { outcome } = await this.deferredPrompt.userChoice;
        
        console.log('[PWA] Install prompt outcome:', outcome);
        
        if (outcome === 'accepted') {
          this.hideInstallButton();
        }
        
        this.deferredPrompt = null;
        return outcome === 'accepted';
      } catch (error) {
        console.error('[PWA] Install prompt error:', error);
        return false;
      }
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
          this.showNotification('You\'re offline. Some features may be limited.', 'warning');
        } else if (!wasOnline && this.isOnline) {
          this.showNotification('Back online!', 'success');
        }
      };

      window.addEventListener('online', updateOnlineStatus);
      window.addEventListener('offline', updateOnlineStatus);
      
      // Initial check
      if (!navigator.onLine) {
        document.documentElement.classList.add('offline');
      }
    },

    /**
     * Setup service worker update handler
     */
    setupUpdateHandler() {
      if (!('serviceWorker' in navigator)) return;

      // Refresh when new service worker takes control
      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (refreshing) return;
        refreshing = true;
        window.location.reload();
      });
    },

    /**
     * Show update notification
     */
    showUpdateNotification() {
      // Remove existing
      const existing = document.getElementById('pwa-update-notification');
      if (existing) existing.remove();
      
      const notification = document.createElement('div');
      notification.id = 'pwa-update-notification';
      notification.innerHTML = `
        <div class="pwa-update-content">
          <i class="fas fa-sync-alt"></i>
          <span>Update available</span>
          <button class="pwa-update-btn" id="pwaUpdateBtn">Refresh</button>
        </div>
      `;
      
      document.body.appendChild(notification);
      
      requestAnimationFrame(() => {
        notification.classList.add('show');
      });
      
      document.getElementById('pwaUpdateBtn').addEventListener('click', () => {
        // Tell waiting service worker to skip waiting
        if (this.swRegistration && this.swRegistration.waiting) {
          this.swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
        }
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
     * Track analytics event (stub - implement with your analytics)
     */
    trackEvent(eventName, params = {}) {
      console.log('[PWA] Event:', eventName, params);
      // Implement with your analytics provider
      // e.g., gtag('event', eventName, params);
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
    },

    /**
     * Check if app can be installed
     */
    canInstall() {
      return !!this.deferredPrompt && !this.isInstalled;
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
