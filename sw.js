// HM Maps Service Worker - 100% Complete Offline Mode (Zero Wi-Fi Required)
const CACHE_NAME = 'himagiri-maps-offline-v30';
const ASSETS_TO_PRECACHE = [
  './',
  './index.html',
  './style.css',
  './style.css?v=30',
  './app.js',
  './app.js?v=30',
  './layouts_data.js',
  './layouts_data.js?v=30',
  './map_data.js',
  './map_data.js?v=30',
  './analytics.js',
  './analytics.js?v=30',
  './qrcode.min.js',
  './qrcode.min.js?v=30',
  './manifest.json',
  './original_map.png',
  './icon-192.png',
  './icon-512.png'
];

// Install: Pre-cache all essential application files immediately
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching all app assets for offline use...');
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
      return self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({ type: 'OFFLINE_READY', cacheName: CACHE_NAME });
        });
      });
    })
  );
});

// Fetch: Network-First for same-origin application scripts & pages
// 1. If online: fetch fresh code immediately from network & update cache
// 2. If offline / no Wi-Fi: fall back seamlessly to cache
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Ignore non-http schemes
  if (!url.protocol.startsWith('http')) return;

  // External assets (fonts, icons)
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
          return new Response('', { status: 408, headers: { 'Content-Type': 'text/plain' } });
        });
      })
    );
    return;
  }

  // Local assets (HTML, JS, CSS, JSON) - Network-First with offline fallback
  event.respondWith(
    fetch(event.request)
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
        // Offline / No signal: Serve from cache
        return caches.match(event.request).then((cached) => {
          if (cached) return cached;
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
          return caches.match(event.request, { ignoreSearch: true }).then((fuzzyCached) => {
            if (fuzzyCached) return fuzzyCached;
            return new Response('Offline: Resource unavailable', { status: 503 });
          });
        });
      })
  );
});
