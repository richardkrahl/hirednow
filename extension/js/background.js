// JARVIS Job Hunter - Background Script
// Handles data storage and cross-tab communication

chrome.runtime.onInstalled.addListener(() => {
  console.log('🤖 JARVIS Job Hunter installed');
  
  // Initialize storage
  chrome.storage.local.get(['profile', 'applications'], (result) => {
    if (!result.profile) {
      chrome.storage.local.set({ profile: null });
    }
    if (!result.applications) {
      chrome.storage.local.set({ applications: [] });
    }
  });
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getProfile') {
    chrome.storage.local.get('profile', (result) => {
      sendResponse(result.profile);
    });
    return true; // Keep channel open for async
  }
  
  if (request.action === 'saveProfile') {
    chrome.storage.local.set({ profile: request.data }, () => {
      sendResponse({ success: true });
    });
    return true;
  }
  
  if (request.action === 'logApplication') {
    chrome.storage.local.get('applications', (result) => {
      const apps = result.applications || [];
      
      // Check for duplicates
      const exists = apps.some(app => app.url === request.data.url);
      if (!exists) {
        apps.push({
          ...request.data,
          dateApplied: new Date().toISOString(),
          status: 'applied'
        });
        chrome.storage.local.set({ applications: apps });
        sendResponse({ success: true, message: 'Application logged' });
      } else {
        sendResponse({ success: false, message: 'Already applied' });
      }
    });
    return true;
  }
  
  if (request.action === 'getApplications') {
    chrome.storage.local.get('applications', (result) => {
      sendResponse(result.applications || []);
    });
    return true;
  }
  
  if (request.action === 'getStats') {
    chrome.storage.local.get('applications', (result) => {
      const apps = result.applications || [];
      const stats = {
        total: apps.length,
        applied: apps.filter(a => a.status === 'applied').length,
        interview: apps.filter(a => a.status === 'interview').length,
        offer: apps.filter(a => a.status === 'offer').length,
        rejected: apps.filter(a => a.status === 'rejected').length
      };
      sendResponse(stats);
    });
    return true;
  }
});

// Open popup on icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      alert('🤖 JARVIS Job Hunter\n\nPress the JARVIS button on job pages to auto-fill!');
    }
  });
});
