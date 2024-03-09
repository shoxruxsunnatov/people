// Listen for the install event
self.addEventListener('install', function(event) {
    console.log('Service worker installed');
  });
  
// Listen for the activate event
self.addEventListener('activate', function(event) {
  console.log('Service worker activated');
});


self.addEventListener('push', function(event) {
  const pushData = event.data.json();
  const title = pushData.title || 'Notification Title';
  const options = {
    body: pushData.body || 'Notification Body',
    icon: pushData.icon || '/path/to/icon.png',
  };
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
