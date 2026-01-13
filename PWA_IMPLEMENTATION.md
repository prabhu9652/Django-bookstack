# TechBookHub PWA Implementation

## Overview

This document describes the Progressive Web App (PWA) implementation for TechBookHub, a Django-based SaaS platform for technical books, resume building, career tools, and learning roadmaps.

## Architecture

### Files Created

```
booksstore/
├── static/
│   ├── manifest.json          # Web App Manifest
│   ├── sw.js                  # Service Worker
│   ├── css/
│   │   └── pwa.css           # PWA-specific styles
│   ├── js/
│   │   └── pwa.js            # PWA registration & install handling
│   └── img/pwa/
│       ├── icon-*.png        # App icons (72-512px)
│       ├── icon-maskable-*.png # Maskable icons for Android
│       ├── shortcut-*.png    # App shortcut icons
│       └── screenshot-*.png  # Store screenshots
├── templates/
│   └── offline.html          # Offline fallback page
└── urls.py                   # Added /sw.js and /manifest.json routes
```

### URL Routes Added

| Route | Purpose |
|-------|---------|
| `/sw.js` | Service worker (served from root for proper scope) |
| `/manifest.json` | Web App Manifest |
| `/offline/` | Offline fallback page |

## Caching Strategy

### Cache Names
- `techbookhub-static-v1.0.0` - CSS, JS, fonts
- `techbookhub-pages-v1.0.0` - HTML pages
- `techbookhub-images-v1.0.0` - Images
- `techbookhub-fonts-v1.0.0` - Web fonts

### Strategy by Route Type

| Route Pattern | Strategy | Rationale |
|--------------|----------|-----------|
| `/accounts/login`, `/accounts/logout`, `/admin/` | Network-only | Security - never cache auth |
| `/library/`, `/resume-builder/dashboard/`, `/careers/my-applications/` | Network-first | User-specific data |
| `/books/`, `/careers/`, `/roadmap/`, `/about/` | Stale-while-revalidate | Public, cacheable content |
| Static assets (CSS, JS) | Cache-first | Versioned, immutable |
| Images | Cache-first | Long TTL appropriate |

### Never Cached Routes
- Authentication pages (`/accounts/login`, `/logout`, `/signup`)
- Password reset flows
- Admin panel (`/admin/`)
- API endpoints (`/api/`)
- CSRF-related requests

## Features

### 1. Installability
- Full Web App Manifest with all required fields
- Icons for all platforms (72px to 512px)
- Maskable icons for Android adaptive icons
- App shortcuts for quick access to key features
- Screenshots for app stores

### 2. Offline Support
- Graceful offline fallback page
- Cached pages remain accessible offline
- Visual offline indicator (yellow bar at top)
- Auto-reload when connection restored

### 3. Install Prompt
- Non-intrusive install banner (appears after 30s)
- Respects user dismissal (7-day cooldown)
- Works on Chrome, Edge, and supported browsers
- iOS Safari "Add to Home Screen" compatible

### 4. Update Handling
- Automatic update checks (hourly)
- User notification when update available
- One-click refresh to apply updates

### 5. Performance
- App shell caching for instant loads
- Stale-while-revalidate for dynamic content
- Background cache updates

## Platform Support

| Platform | Browser | Install | Offline |
|----------|---------|---------|---------|
| Android | Chrome | ✅ | ✅ |
| Android | Edge | ✅ | ✅ |
| Windows | Chrome | ✅ | ✅ |
| Windows | Edge | ✅ | ✅ |
| macOS | Chrome | ✅ | ✅ |
| macOS | Safari | ⚠️ Limited | ✅ |
| iOS | Safari | ⚠️ Add to Home | ✅ |

## Security Considerations

1. **Auth pages never cached** - Login, logout, signup, password reset
2. **CSRF tokens excluded** - All CSRF-related requests bypass cache
3. **Admin panel excluded** - `/admin/` routes always network-only
4. **User data network-first** - Library, applications, dashboard
5. **HTTPS required** - Service workers only work over HTTPS

## Testing

### Lighthouse PWA Audit
Run Chrome DevTools → Lighthouse → PWA audit to verify:
- ✅ Installable
- ✅ PWA Optimized
- ✅ Offline capable

### Manual Testing
1. Install the app from browser
2. Disconnect network
3. Navigate to cached pages
4. Verify offline page for uncached routes
5. Reconnect and verify auto-refresh

### Service Worker DevTools
Chrome DevTools → Application → Service Workers:
- Check registration status
- View cached resources
- Test offline mode
- Clear caches for testing

## Updating the PWA

### Version Bump
1. Update `CACHE_VERSION` in `sw.js`
2. Run `collectstatic`
3. Deploy

### Adding New Cached Routes
1. Add pattern to appropriate array in `sw.js`:
   - `CACHE_FIRST_PATTERNS` for public pages
   - `NETWORK_FIRST_PATTERNS` for user-specific pages
   - `NEVER_CACHE_PATTERNS` for sensitive routes

### Updating Icons
1. Replace SVG source: `booksstore/static/img/pwa/icon-512x512.svg`
2. Regenerate PNGs using cairosvg/pillow
3. Run `collectstatic`

## Troubleshooting

### Service Worker Not Registering
- Ensure HTTPS (or localhost)
- Check browser console for errors
- Verify `/sw.js` returns 200

### Install Prompt Not Showing
- Must be served over HTTPS
- Manifest must be valid (check DevTools)
- User must have engaged with site
- May have been dismissed (check localStorage)

### Offline Page Not Working
- Verify `/offline/` route exists
- Check service worker is active
- Ensure offline.html is cached

### Cache Not Updating
- Increment `CACHE_VERSION` in sw.js
- Hard refresh (Ctrl+Shift+R)
- Clear site data in DevTools

## API Reference

### JavaScript API (window.TechBookHubPWA)

```javascript
// Check if installed
TechBookHubPWA.isInstalled

// Check online status
TechBookHubPWA.isOnline

// Trigger install prompt
TechBookHubPWA.promptInstall()

// Clear all caches (for logout)
await TechBookHubPWA.clearCaches()

// Pre-cache specific URLs
await TechBookHubPWA.cacheUrls(['/books/', '/careers/'])
```

### Service Worker Messages

```javascript
// Skip waiting (apply update immediately)
navigator.serviceWorker.controller.postMessage({ type: 'SKIP_WAITING' })

// Clear all caches
navigator.serviceWorker.controller.postMessage({ type: 'CLEAR_CACHE' })

// Cache specific URLs
navigator.serviceWorker.controller.postMessage({ 
  type: 'CACHE_URLS', 
  payload: { urls: ['/books/', '/careers/'] }
})
```
