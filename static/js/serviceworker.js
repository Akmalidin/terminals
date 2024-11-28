// const CACHE_NAME = "django-pwa-cache-v1";
// const urlsToCache = [
//     "/",
//     "/static/css/main.css", // Замените на ваши стили
//     "/static/css/terminals.css", // Замените на ваши стили
//     "/static/js/main.js",   // Замените на ваши скрипты
//     "/offline.html",
// ];

// // Установка Service Worker и кэширование файлов
// self.addEventListener("install", (event) => {
//     event.waitUntil(
//         caches.open(CACHE_NAME).then((cache) => {
//             return cache.addAll(urlsToCache);
//         })
//     );
// });

// // Обработка запросов: сначала проверяем кэш
// self.addEventListener("fetch", (event) => {
//     event.respondWith(
//         caches.match(event.request).then((response) => {
//             return response || fetch(event.request);
//         }).catch(() => {
//             return caches.match("/offline.html");
//         })
//     );
// });

// // Удаление старого кэша при обновлении
// self.addEventListener("activate", (event) => {
//     const cacheWhitelist = [CACHE_NAME];
//     event.waitUntil(
//         caches.keys().then((cacheNames) => {
//             return Promise.all(
//                 cacheNames.map((cacheName) => {
//                     if (!cacheWhitelist.includes(cacheName)) {
//                         return caches.delete(cacheName);
//                     }
//                 })
//             );
//         })
//     );
// });
