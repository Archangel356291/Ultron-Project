/* Ultron service worker -- the installable-app shell.
 *
 * Rules, in order of importance:
 *  1. /api/* is NEVER touched: live data and anything behind the token go
 *     straight to the network, always. Same for /sw.js itself.
 *  2. The page ("/") is network-first: a redeploy shows up on the next
 *     load while online; offline, the last good copy opens and the page's
 *     own reconnect logic takes over ("reconnecting · showing data from
 *     Ns ago") instead of a browser error screen.
 *  3. Fonts, sprites and icons are stale-while-revalidate: served from
 *     cache instantly, refreshed in the background, so a changed asset is
 *     at most one load behind.
 *  4. The cache name carries a version the backend derives from the
 *     dashboard's own content, so a new deploy drops every old cache on
 *     activate. No update prompt is needed because of rule 2.
 */
const VERSION = '__VERSION__';
const CACHE = 'ultron-shell-' + VERSION;
const SHELL = ['/', '/manifest.webmanifest'];
const ASSET_PREFIXES = ['/fonts/', '/pixel-assets/'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith('/api/') || url.pathname === '/sw.js') return; // network only, never cached

  if (url.pathname === '/' || req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put('/', copy));
          return res;
        })
        .catch(() => caches.match('/'))
    );
    return;
  }

  if (ASSET_PREFIXES.some((p) => url.pathname.startsWith(p)) || url.pathname === '/manifest.webmanifest') {
    event.respondWith(
      caches.open(CACHE).then((cache) =>
        cache.match(req).then((hit) => {
          const refresh = fetch(req).then((res) => {
            if (res.ok) cache.put(req, res.clone());
            return res;
          });
          return hit || refresh;
        })
      )
    );
  }
});
