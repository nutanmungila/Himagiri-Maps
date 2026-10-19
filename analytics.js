/**
 * Himagiri Meadows Community Map Analytics Tracker
 * Privacy-friendly, zero-cookie, local & cloud ready usage tracking
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'himagiri_analytics_v1';

  // Default initial stats
  function getAnalyticsData() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      if (data) return JSON.parse(data);
    } catch (e) {
      console.warn('Analytics storage error:', e);
    }
    return {
      totalVisits: 0,
      uniqueVisitors: 0,
      visitorId: null,
      deviceStats: { android: 0, ios: 0, desktop: 0 },
      searches: {},
      routes: {},
      shares: 0,
      voiceQueries: 0,
      firstVisit: new Date().toISOString(),
      lastVisit: new Date().toISOString()
    };
  }

  function saveAnalyticsData(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.warn('Could not save analytics:', e);
    }
  }

  // Detect Device OS
  function detectDevice() {
    const ua = navigator.userAgent || navigator.vendor || window.opera;
    if (/android/i.test(ua)) return 'android';
    if (/iPad|iPhone|iPod/.test(ua) && !window.MSStream) return 'ios';
    return 'desktop';
  }

  // Record Session Visit
  function recordVisit() {
    const data = getAnalyticsData();
    const isNewSession = !sessionStorage.getItem('himagiri_session_active');

    if (isNewSession) {
      sessionStorage.setItem('himagiri_session_active', '1');
      data.totalVisits = (data.totalVisits || 0) + 1;

      // Check unique visitor
      if (!data.visitorId) {
        data.visitorId = 'v_' + Math.random().toString(36).substring(2, 10);
        data.uniqueVisitors = (data.uniqueVisitors || 0) + 1;
      }

      // Device stats
      const dev = detectDevice();
      data.deviceStats[dev] = (data.deviceStats[dev] || 0) + 1;
      data.lastVisit = new Date().toISOString();
      saveAnalyticsData(data);
    }

    // Google Analytics 4 event if initialized
    if (window.gtag) {
      window.gtag('event', 'page_view', {
        page_title: document.title,
        page_location: window.location.href,
        device_category: detectDevice()
      });
    }
  }

  // Public Tracker API
  window.HimagiriAnalytics = {
    trackSearch: function (query, isVoice = false) {
      if (!query) return;
      const clean = query.trim().toUpperCase();
      const data = getAnalyticsData();
      data.searches[clean] = (data.searches[clean] || 0) + 1;
      if (isVoice) {
        data.voiceQueries = (data.voiceQueries || 0) + 1;
      }
      saveAnalyticsData(data);

      if (window.gtag) {
        window.gtag('event', 'search', {
          search_term: clean,
          is_voice: isVoice
        });
      }
    },

    trackRoute: function (startLabel, destLabel, distanceMeters) {
      const data = getAnalyticsData();
      const routeKey = `${startLabel} ➔ ${destLabel}`;
      data.routes[routeKey] = (data.routes[routeKey] || 0) + 1;
      saveAnalyticsData(data);

      if (window.gtag) {
        window.gtag('event', 'generate_lead', {
          start_point: startLabel,
          destination: destLabel,
          distance: distanceMeters
        });
      }
    },

    trackShare: function (houseNumber, platform = 'native') {
      const data = getAnalyticsData();
      data.shares = (data.shares || 0) + 1;
      saveAnalyticsData(data);

      if (window.gtag) {
        window.gtag('event', 'share', {
          content_type: 'directions',
          item_id: houseNumber,
          method: platform
        });
      }
    },

    getStats: function () {
      return getAnalyticsData();
    }
  };

  // Run on load
  recordVisit();

})();
