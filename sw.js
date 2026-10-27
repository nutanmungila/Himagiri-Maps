// HM Maps Service Worker - 100% Complete Offline Mode (Zero Wi-Fi Required)
const CACHE_NAME = 'himagiri-maps-offline-v28';
const ASSETS_TO_PRECACHE = [
  './',
  './index.html',
  './style.css',
  './style.css?v=25',
  './app.js',
  './app.js?v=25',
  './layouts_data.js',
  './layouts_data.js?v=25',
  './map_data.js',
  './map_data.js?v=25',
  './analytics.js',
  './analytics.js?v=25',
  './qrcode.min.js',
  './qrcode.min.js?v=25',
  './manifest.json',
  './original_map.png',
  './icon-192.png',
  './icon-512.png'
];

// Install: Pre-cache all essential application files immediately
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching all app assets for 100% offline use...');
      // Use individual caching with catch so any missing optional file does not abort installation
      return Promise.all(
        ASSETS_TO_PRECACHE.map((url) => {
          return cache.add(url).catch((err) => {
            console.warn('[SW] Failed to pre-cache item:', url, err);
          });
        })
      );
    }).then(() => {
      return self.skipWaiting();
    })
  );
});

// Activate: Clean up any old caches and claim clients immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[SW] Purging outdated cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    }).then(() => {
      // Notify all connected clients that offline capability is ready
      return self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({ type: 'OFFLINE_READY', cacheName: CACHE_NAME });
        });
      });
    })
  );
});

// Fetch: Stale-While-Revalidate / Cache-First strategy
// 1. If in cache, return immediately (0ms delay, works with ZERO Wi-Fi or cellular signal)
// 2. In background, if online, update the cache with fresh version
// 3. If navigation request (HTML), fallback to cached index.html
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Ignore non-http schemes (extensions, file:, etc.)
  if (!url.protocol.startsWith('http')) return;

  // For Google Fonts or external CDN assets, attempt cache first, fallback to network
  if (url.origin !== self.location.origin) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((res) => {
          if (res && res.status === 200) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return res;
        }).catch(() => {
          // If external font fails offline, fail gracefully without breaking UI
          return new Response('', { status: 408, headers: { 'Content-Type': 'text/plain' } });
        });
      })
    );
    return;
  }

  // Local assets (same origin)
  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then((cachedResponse) => {
      // Background revalidation (if connected to Wi-Fi/network)
      const fetchPromise = fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Offline / no Wi-Fi - If navigation, return index.html
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html', { ignoreSearch: true });
          }
        });

      // Serve from cache immediately if present (instant load, no Wi-Fi needed!)
      if (cachedResponse) {
        return cachedResponse;
      }

      // If not yet in cache, wait for network fetch
      return fetchPromise.then((res) => {
        if (res) return res;
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html', { ignoreSearch: true });
        }
        return new Response('Offline: Resource unavailable', { status: 503 });
      });
    })
  );
});
