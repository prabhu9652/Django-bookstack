/**
 * TechBookHub Service Worker
 * Production-grade PWA implementation with intelligent caching strategies
 * 
 * Caching Strategy:
 * - App Shell (CSS, JS, fonts): Cache-first with network fallback
 * - Static Assets (images): Cache-first with long TTL
 * - API/Dynamic Content: Network-first with cache fallback
 * - Auth Pages: Network-only (never cache)
 * - Forms/POST: Network-only
 */

const CACHE_VERSION = 'v1.2.0';
const CACHE_NAMES = {
  static: `techbookhub-static-${CACHE_VERSION}`,
  pages: `techbookhub-pages-${CACHE_VERSION}`,
  images: `techbookhub-images-${CACHE_VERSION}`,
  fonts: `techbookhub-fonts-${CACHE_VERSION}`,
};

// Maximum cache sizes (prevent unbounded growth)
const CACHE_LIMITS = {
  pages: 50,
  images: 100,
  fonts: 20,
};

// App Shell - Critical resources for offline functionality
const APP_SHELL = [
  '/',
  '/offline/',
  '/static/css/dark-theme-unified.css',
  '/static/css/components-dark.css',
  '/static/css/auth-enterprise.css',
  '/static/css/image-optimization.css',
  '/static/css/responsive-enhancements.css',
  '/static/css/pwa.css',
  '/static/js/library-manager.js',
  '/static/js/image-loader.js',
  '/static/js/auth-enterprise.js',
  '/static/js/minimal-interactions.js',
  '/static/js/page-transitions.js',
  '/static/js/pwa.js',
  '/static/img/pwa/icon-192x192.png',
];

// Routes that should NEVER be cached (auth, forms, admin)
const NEVER_CACHE_PATTERNS = [
  /\/accounts\/login/,
  /\/accounts\/logout/,
  /\/accounts\/signup/,
  /\/accounts\/password/,
  /\/admin\//,
  /\/api\//,
  /\/csrf/,
  /\?.*csrf/,
];

// Routes that should use network-first strategy
const NETWORK_FIRST_PATTERNS = [
  /\/library\//,
  /\/resume-builder\/dashboard/,
  /\/resume-builder\/draft/,
  /\/resume-builder\/edit/,
  /\/careers\/my-applications/,
  /\/careers\/admin/,
  /\/accounts\/access-status/,
];

// Routes that can be cached aggressively (public, read-only)
const CACHE_FIRST_PATTERNS = [
  /\/books\/?$/,
  /\/books\/category/,
  /\/careers\/?$/,
  /\/careers\/job\//,
  /\/roadmap\/?$/,
  /\/roadmap\/path\//,
  /\/about\/?$/,
];

/**
 * Install Event - Cache app shell
 */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAMES.static)
      .then((cache) => {
        console.log('[SW] Caching app shell...');
        // Cache what we can, don't fail on missing resources
        return Promise.allSettled(
          APP_SHELL.map(url => 
            cache.add(url).catch(err => {
              console.warn(`[SW] Failed to cache: ${url}`, err);
            })
          )
        );
      })
      .then(() => {
        console.log('[SW] App shell cached successfully');
        return self.skipWaiting();
      })
  );
});

/**
 * Activate Event - Clean up old caches
 */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => {
              // Delete caches that don't match current version
              return name.startsWith('techbookhub-') && 
                     !Object.values(CACHE_NAMES).includes(name);
            })
            .map((name) => {
              console.log(`[SW] Deleting old cache: ${name}`);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Service worker activated');
        return self.clients.claim();
      })
  );
});

/**
 * Fetch Event - Intelligent request handling
 */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Only handle same-origin requests
  if (url.origin !== location.origin) {
    return;
  }
  
  // Skip non-GET requests (forms, API calls)
  if (request.method !== 'GET') {
    return;
  }
  
  // Never cache auth/admin routes
  if (shouldNeverCache(url.pathname)) {
    event.respondWith(networkOnly(request));
    return;
  }
  
  // Handle static assets (CSS, JS, fonts)
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(request, CACHE_NAMES.static));
    return;
  }
  
  // Handle images
  if (isImage(url.pathname)) {
    event.respondWith(cacheFirst(request, CACHE_NAMES.images));
    return;
  }
  
  // Handle fonts
  if (isFont(url.pathname)) {
    event.respondWith(cacheFirst(request, CACHE_NAMES.fonts));
    return;
  }
  
  // Network-first for user-specific pages
  if (shouldNetworkFirst(url.pathname)) {
    event.respondWith(networkFirst(request, CACHE_NAMES.pages));
    return;
  }
  
  // Cache-first for public pages
  if (shouldCacheFirst(url.pathname)) {
    event.respondWith(staleWhileRevalidate(request, CACHE_NAMES.pages));
    return;
  }
  
  // Default: Network-first with offline fallback
  event.respondWith(networkFirstWithOfflineFallback(request));
});

/**
 * Caching Strategies
 */

// Cache-first: Check cache, fallback to network
async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  
  if (cached) {
    return cached;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.warn('[SW] Cache-first fetch failed:', error);
    return new Response('Resource not available offline', { status: 503 });
  }
}

// Network-first: Try network, fallback to cache
async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) {
      return cached;
    }
    return getOfflinePage();
  }
}

// Network-only: Never cache
async function networkOnly(request) {
  try {
    return await fetch(request);
  } catch (error) {
    // For navigation requests (pages), show offline page
    if (request.mode === 'navigate') {
      return getAuthOfflinePage();
    }
    return new Response('Network connection required', { 
      status: 503,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Stale-while-revalidate: Return cache immediately, update in background
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  
  // Fetch in background to update cache
  const fetchPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        cache.put(request, response.clone());
      }
      return response;
    })
    .catch(() => null);
  
  // Return cached version immediately if available
  if (cached) {
    return cached;
  }
  
  // Otherwise wait for network
  const response = await fetchPromise;
  if (response) {
    return response;
  }
  
  return getOfflinePage();
}

// Network-first with offline fallback page
async function networkFirstWithOfflineFallback(request) {
  try {
    const response = await fetch(request);
    
    // Cache successful HTML responses
    if (response.ok && request.headers.get('Accept')?.includes('text/html')) {
      const cache = await caches.open(CACHE_NAMES.pages);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    // Try cache first
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    
    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      return getOfflinePage();
    }
    
    return new Response('Offline', { status: 503 });
  }
}

/**
 * Helper Functions
 */

function shouldNeverCache(pathname) {
  return NEVER_CACHE_PATTERNS.some(pattern => pattern.test(pathname));
}

function shouldNetworkFirst(pathname) {
  return NETWORK_FIRST_PATTERNS.some(pattern => pattern.test(pathname));
}

function shouldCacheFirst(pathname) {
  return CACHE_FIRST_PATTERNS.some(pattern => pattern.test(pathname));
}

function isStaticAsset(pathname) {
  return /\.(css|js)(\?.*)?$/.test(pathname) || 
         pathname.startsWith('/static/css/') || 
         pathname.startsWith('/static/js/');
}

function isImage(pathname) {
  return /\.(png|jpg|jpeg|gif|webp|svg|ico)(\?.*)?$/.test(pathname) ||
         pathname.startsWith('/static/img/') ||
         pathname.startsWith('/media/');
}

function isFont(pathname) {
  return /\.(woff|woff2|ttf|otf|eot)(\?.*)?$/.test(pathname);
}

async function getOfflinePage() {
  const cached = await caches.match('/offline/');
  if (cached) {
    return cached;
  }
  
  // Fallback HTML if offline page not cached
  return new Response(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Offline - TechBookHub</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: #0f1419;
          color: #e7e9ea;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .offline-container {
          text-align: center;
          max-width: 400px;
        }
        .offline-icon {
          font-size: 64px;
          margin-bottom: 24px;
          opacity: 0.6;
        }
        h1 { font-size: 24px; margin-bottom: 12px; }
        p { color: #71767b; margin-bottom: 24px; line-height: 1.5; }
        .retry-btn {
          background: #4a9eff;
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.2s;
        }
        .retry-btn:hover { background: #3d8be6; }
      </style>
    </head>
    <body>
      <div class="offline-container">
        <div class="offline-icon">📡</div>
        <h1>You're Offline</h1>
        <p>It looks like you've lost your internet connection. Some features may be unavailable until you're back online.</p>
        <button class="retry-btn" onclick="location.reload()">Try Again</button>
      </div>
    </body>
    </html>
  `, {
    status: 200,
    headers: { 'Content-Type': 'text/html' }
  });
}

// Offline page specifically for auth routes
async function getAuthOfflinePage() {
  return new Response(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Connection Required - TechBookHub</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: #0f1419;
          color: #e7e9ea;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .offline-container {
          text-align: center;
          max-width: 420px;
        }
        .offline-icon {
          font-size: 56px;
          margin-bottom: 20px;
        }
        h1 { font-size: 22px; margin-bottom: 12px; font-weight: 600; }
        p { color: #71767b; margin-bottom: 20px; line-height: 1.6; font-size: 15px; }
        .btn-group { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
        .btn {
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 15px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          text-decoration: none;
          border: none;
        }
        .btn-primary {
          background: #4a9eff;
          color: white;
        }
        .btn-primary:hover { background: #3d8be6; }
        .btn-secondary {
          background: transparent;
          color: #4a9eff;
          border: 1px solid #4a9eff;
        }
        .btn-secondary:hover { background: rgba(74, 158, 255, 0.1); }
        .info-box {
          background: rgba(74, 158, 255, 0.08);
          border: 1px solid rgba(74, 158, 255, 0.2);
          border-radius: 10px;
          padding: 14px 18px;
          margin-top: 24px;
          font-size: 13px;
          color: #8b949e;
        }
        .info-box i { color: #4a9eff; margin-right: 8px; }
      </style>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body>
      <div class="offline-container">
        <div class="offline-icon">🔐</div>
        <h1>Internet Connection Required</h1>
        <p>Sign in and sign up require a secure connection to our servers. Please check your internet connection and try again.</p>
        <div class="btn-group">
          <button class="btn btn-primary" onclick="location.reload()">
            <i class="fas fa-rotate-right"></i>&nbsp; Try Again
          </button>
          <a href="/" class="btn btn-secondary">
            <i class="fas fa-home"></i>&nbsp; Go Home
          </a>
        </div>
        <div class="info-box">
          <i class="fas fa-shield-halved"></i>
          For your security, authentication always requires a live connection.
        </div>
      </div>
    </body>
    </html>
  `, {
    status: 200,
    headers: { 'Content-Type': 'text/html' }
  });
}

/**
 * Message Handler - For cache management from main thread
 */
self.addEventListener('message', (event) => {
  const { type, payload } = event.data || {};
  
  switch (type) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;
      
    case 'CLEAR_CACHE':
      clearAllCaches().then(() => {
        event.ports[0]?.postMessage({ success: true });
      });
      break;
      
    case 'CACHE_URLS':
      if (payload?.urls) {
        cacheUrls(payload.urls).then(() => {
          event.ports[0]?.postMessage({ success: true });
        });
      }
      break;
  }
});

async function clearAllCaches() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames
      .filter(name => name.startsWith('techbookhub-'))
      .map(name => caches.delete(name))
  );
  console.log('[SW] All caches cleared');
}

async function cacheUrls(urls) {
  const cache = await caches.open(CACHE_NAMES.pages);
  await Promise.allSettled(
    urls.map(url => cache.add(url).catch(err => console.warn(`[SW] Failed to cache: ${url}`)))
  );
}

/**
 * Trim cache to prevent unbounded growth
 */
async function trimCache(cacheName, maxItems) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  
  if (keys.length > maxItems) {
    // Delete oldest entries (FIFO)
    const deleteCount = keys.length - maxItems;
    for (let i = 0; i < deleteCount; i++) {
      await cache.delete(keys[i]);
    }
    console.log(`[SW] Trimmed ${deleteCount} items from ${cacheName}`);
  }
}

/**
 * Periodic cache maintenance
 */
async function performCacheMaintenance() {
  await trimCache(CACHE_NAMES.pages, CACHE_LIMITS.pages);
  await trimCache(CACHE_NAMES.images, CACHE_LIMITS.images);
  await trimCache(CACHE_NAMES.fonts, CACHE_LIMITS.fonts);
}

console.log('[SW] Service worker loaded');
