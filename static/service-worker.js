// Listen for the install event
self.addEventListener('install', function(event) {
    console.log('Service worker installed');
  });
  
  // Listen for the activate event
  self.addEventListener('activate', function(event) {
    console.log('Service worker activated');
  });
  
  // Listen for fetch events
  self.addEventListener('fetch', function(event) {
    console.log('Fetch event intercepted:', event.request);
    // You can add caching logic or handle network requests here
  });
  