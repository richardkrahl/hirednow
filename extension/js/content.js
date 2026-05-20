// JARVIS Job Hunter - Content Script
// Runs on job application pages and auto-fills forms

(function() {
  'use strict';
  
  // Detect which site we're on
  const hostname = window.location.hostname;
  const pathname = window.location.pathname;
  
  // Job data extractor for different sites
  const extractors = {
    linkedin: () => {
      const title = document.querySelector('h1')?.textContent?.trim();
      const company = document.querySelector('[data-testid="job-details-company"]')?.textContent?.trim() ||
                     document.querySelector('.job-details-jobs-unified-top-card__company-name')?.textContent?.trim();
      const location = document.querySelector('.job-details-jobs-unified-top-card__bullet')?.textContent?.trim();
      
      return { title, company, location, source: 'LinkedIn' };
    },
    
    indeed: () => {
      const title = document.querySelector('h1')?.textContent?.trim() ||
                   document.querySelector('.jobsearch-JobInfoHeader-title')?.textContent?.trim();
      const company = document.querySelector('[data-testid="company-name"]')?.textContent?.trim() ||
                     document.querySelector('.jobsearch-InlineCompanyRating')?.textContent?.trim();
      const location = document.querySelector('[data-testid="job-location"]')?.textContent?.trim();
      
      return { title, company, location, source: 'Indeed' };
    },
    
    greenhouse: () => {
      const title = document.querySelector('.app-title')?.textContent?.trim() ||
                   document.querySelector('h1')?.textContent?.trim();
      const company = document.querySelector('.company-name')?.textContent?.trim() ||
                     document.title?.split('-')[1]?.trim();
      
      return { title, company, location: '', source: 'Greenhouse' };
    },
    
    lever: () => {
      const title = document.querySelector('.posting-headline h2')?.textContent?.trim();
      const company = document.querySelector('.main-header-text')?.textContent?.trim();
      
      return { title, company, location: '', source: 'Lever' };
    },
    
    generic: () => {
      // Try to extract from common selectors
      const title = document.querySelector('h1')?.textContent?.trim() ||
                   document.querySelector('[class*="title"]')?.textContent?.trim();
      const company = document.querySelector('[class*="company"]')?.textContent?.trim() ||
                       document.querySelector('[class*="employer"]')?.textContent?.trim();
      
      return { title, company, location: '', source: 'Unknown' };
    }
  };
  
  // Detect site and extract job data
  function detectSite() {
    if (hostname.includes('linkedin.com')) return 'linkedin';
    if (hostname.includes('indeed.com')) return 'indeed';
    if (hostname.includes('greenhouse.io') || hostname.includes('boards.greenhouse.io')) return 'greenhouse';
    if (hostname.includes('lever.co') || hostname.includes('jobs.lever.co')) return 'lever';
    return 'generic';
  }
  
  function extractJobData() {
    const site = detectSite();
    const extractor = extractors[site] || extractors.generic;
    return extractor();
  }
  
  // Form field fillers for different sites
  const fieldFillers = {
    linkedin: (profile) => {
      // LinkedIn Easy Apply fields
      const fields = [
        { selector: 'input[name="firstName"]', value: profile.firstName },
        { selector: 'input[name="lastName"]', value: profile.lastName },
        { selector: 'input[name="email"]', value: profile.email },
        { selector: 'input[name="phoneNumber"]', value: profile.phone },
        { selector: 'input[name="city"]', value: profile.city },
      ];
      
      return fillFields(fields);
    },
    
    greenhouse: (profile) => {
      // Greenhouse fields
      const fields = [
        { selector: 'input[name="first_name"]', value: profile.firstName },
        { selector: 'input[name="last_name"]', value: profile.lastName },
        { selector: 'input[name="email"]', value: profile.email },
        { selector: 'input[name="phone"]', value: profile.phone },
        { selector: 'input[name="linkedin"]', value: profile.linkedin },
        { selector: 'input[name="website"]', value: profile.website },
        { selector: 'input[name="location"]', value: `${profile.city}, ${profile.state}` },
      ];
      
      return fillFields(fields);
    },
    
    lever: (profile) => {
      // Lever fields
      const fields = [
        { selector: 'input[name="name"]', value: `${profile.firstName} ${profile.lastName}` },
        { selector: 'input[name="email"]', value: profile.email },
        { selector: 'input[name="phone"]', value: profile.phone },
        { selector: 'input[name="org"]', value: profile.currentCompany || '' },
        { selector: 'input[name="linkedin"]', value: profile.linkedin },
        { selector: 'input[name="urls[Portfolio]"]', value: profile.website },
      ];
      
      return fillFields(fields);
    },
    
    generic: (profile) => {
      // Try common field names
      const fields = [
        { selector: 'input[name*="first"], input[name*="fname"], input[id*="first"]', value: profile.firstName },
        { selector: 'input[name*="last"], input[name*="lname"], input[id*="last"]', value: profile.lastName },
        { selector: 'input[name*="email"], input[type="email"]', value: profile.email },
        { selector: 'input[name*="phone"], input[type="tel"]', value: profile.phone },
        { selector: 'input[name*="linkedin"], input[name*="linked"]', value: profile.linkedin },
        { selector: 'input[name*="website"], input[name*="url"], input[name*="portfolio"]', value: profile.website },
      ];
      
      return fillFields(fields);
    }
  };
  
  function fillFields(fields) {
    let filled = 0;
    fields.forEach(field => {
      const elements = document.querySelectorAll(field.selector);
      elements.forEach(el => {
        if (el && field.value && !el.value) {
          el.value = field.value;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          filled++;
        }
      });
    });
    return filled;
  }
  
  // Create JARVIS floating button
  function createJarvisButton() {
    // Don't create if already exists
    if (document.getElementById('jarvis-job-hunter-btn')) return;
    
    const button = document.createElement('div');
    button.id = 'jarvis-job-hunter-btn';
    button.innerHTML = `
      <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 50px;
        cursor: pointer;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: transform 0.2s, box-shadow 0.2s;
      " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.5)';" 
         onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.4)';">
        🤖 JARVIS
      </div>
    `;
    
    button.addEventListener('click', showJarvisMenu);
    document.body.appendChild(button);
  }
  
  // Show JARVIS action menu
  function showJarvisMenu() {
    // Remove existing menu
    const existing = document.getElementById('jarvis-menu');
    if (existing) {
      existing.remove();
      return;
    }
    
    const jobData = extractJobData();
    
    const menu = document.createElement('div');
    menu.id = 'jarvis-menu';
    menu.innerHTML = `
      <div style="
        position: fixed;
        bottom: 80px;
        right: 20px;
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        z-index: 999999;
        min-width: 280px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      ">
        <div style="font-weight: 600; margin-bottom: 12px; color: #333;">
          🤖 JARVIS Job Hunter
        </div>
        
        ${jobData.title ? `
          <div style="font-size: 13px; color: #666; margin-bottom: 12px; padding: 8px; background: #f5f5f5; border-radius: 6px;">
            <strong>${jobData.title}</strong><br/>
            ${jobData.company || 'Unknown Company'}
          </div>
        ` : ''}
        
        <button id="jarvis-fill-btn" style="
          width: 100%;
          padding: 10px;
          background: #667eea;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          margin-bottom: 8px;
        ">📝 Auto-Fill Application</button>
        
        <button id="jarvis-save-btn" style="
          width: 100%;
          padding: 10px;
          background: #10b981;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          margin-bottom: 8px;
        ">💾 Save Job to Tracker</button>
        
        <button id="jarvis-track-btn" style="
          width: 100%;
          padding: 10px;
          background: #6b7280;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
        ">📊 View My Stats</button>
        
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; font-size: 11px; color: #999; text-align: center;">
          JARVIS v1.0 • Local • Private
        </div>
      </div>
    `;
    
    document.body.appendChild(menu);
    
    // Add button handlers
    document.getElementById('jarvis-fill-btn')?.addEventListener('click', () => autoFillForm(jobData));
    document.getElementById('jarvis-save-btn')?.addEventListener('click', () => saveJob(jobData));
    document.getElementById('jarvis-track-btn')?.addEventListener('click', showStats);
    
    // Close menu when clicking outside
    document.addEventListener('click', function closeMenu(e) {
      if (!menu.contains(e.target) && e.target.id !== 'jarvis-job-hunter-btn') {
        menu.remove();
        document.removeEventListener('click', closeMenu);
      }
    });
  }
  
  // Auto-fill form
  function autoFillForm(jobData) {
    chrome.storage.local.get('profile', (result) => {
      if (!result.profile) {
        alert('🤖 Please set up your profile first!\n\nClick the JARVIS extension icon and create your profile.');
        return;
      }
      
      const site = detectSite();
      const filler = fieldFillers[site] || fieldFillers.generic;
      const filled = filler(result.profile);
      
      // Show success notification
      const notification = document.createElement('div');
      notification.innerHTML = `
        <div style="
          position: fixed;
          top: 20px;
          right: 20px;
          background: #10b981;
          color: white;
          padding: 12px 20px;
          border-radius: 8px;
          z-index: 999999;
          font-family: sans-serif;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
          ✅ Auto-filled ${filled} fields!
        </div>
      `;
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 3000);
      
      // Close menu
      document.getElementById('jarvis-menu')?.remove();
    });
  }
  
  // Save job to tracker
  function saveJob(jobData) {
    const fullData = {
      ...jobData,
      url: window.location.href,
      dateSaved: new Date().toISOString()
    };
    
    chrome.runtime.sendMessage({
      action: 'logApplication',
      data: fullData
    }, (response) => {
      const notification = document.createElement('div');
      notification.innerHTML = `
        <div style="
          position: fixed;
          top: 20px;
          right: 20px;
          background: ${response?.success ? '#10b981' : '#f59e0b'};
          color: white;
          padding: 12px 20px;
          border-radius: 8px;
          z-index: 999999;
          font-family: sans-serif;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
          ${response?.success ? '💾 Job saved to tracker!' : '⚠️ ' + (response?.message || 'Already saved')}
        </div>
      `;
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 3000);
      
      document.getElementById('jarvis-menu')?.remove();
    });
  }
  
  // Show stats
  function showStats() {
    chrome.runtime.sendMessage({ action: 'getStats' }, (stats) => {
      const notification = document.createElement('div');
      notification.innerHTML = `
        <div style="
          position: fixed;
          top: 20px;
          right: 20px;
          background: white;
          color: #333;
          padding: 16px 20px;
          border-radius: 8px;
          z-index: 999999;
          font-family: sans-serif;
          box-shadow: 0 4px 20px rgba(0,0,0,0.15);
          min-width: 200px;
        ">
          <div style="font-weight: 600; margin-bottom: 8px;">📊 Your Job Hunt</div>
          <div style="font-size: 13px; color: #666;">
            Total: ${stats?.total || 0}<br/>
            Applied: ${stats?.applied || 0}<br/>
            Interviews: ${stats?.interview || 0}<br/>
            Offers: ${stats?.offer || 0}
          </div>
        </div>
      `;
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 5000);
      
      document.getElementById('jarvis-menu')?.remove();
    });
  }
  
  // Initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createJarvisButton);
  } else {
    createJarvisButton();
  }
  
  // Re-create button if page dynamically updates
  setInterval(() => {
    if (!document.getElementById('jarvis-job-hunter-btn')) {
      createJarvisButton();
    }
  }, 2000);
  
})();
