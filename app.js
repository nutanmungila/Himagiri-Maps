/**
 * Himagiri Meadows Layout Navigator & Interactive Vector Map
 * Complete Wayfinding, Turn-by-Turn Directions, Voice & Conversational Assistant
 */

(function () {
  'use strict';

  // Check data availability (Support both window.LAYOUTS and legacy window.HIMAGIRI_DATA)
  const layouts = window.LAYOUTS || {};
  let currentLayoutId = 'himagiri';
  let currentLayout = layouts[currentLayoutId] || (window.HIMAGIRI_DATA ? {
    id: 'himagiri',
    name: 'Himagiri Meadows',
    location: 'Bannerghatta Road, Bangalore South',
    type: 'Residential Gated Community',
    unitType: 'Plot',
    bounds: { minX: 20, maxX: 1270, minY: 135, maxY: 935 },
    center: { x: 645, y: 535 },
    groundPolygon: "40,320 80,180 300,160 850,140 1050,140 1260,170 1250,600 1150,620 950,830 800,900 500,890 280,880 30,830 30,620",
    borderTreesPath: "M 40,320 Q 150,160 300,160 T 850,140 T 1050,140 T 1260,170 L 1250,600 L 1150,620 L 950,830 L 800,900 L 500,890 L 280,880 L 30,830 Z",
    gardenPark: { x: 440, y: 625, w: 370, h: 45, rx: 6, label: "Central Community Garden" },
    plots: window.HIMAGIRI_DATA.plots,
    roads: { nodes: window.HIMAGIRI_DATA.nodes, edges: window.HIMAGIRI_DATA.edges },
    amenities: window.HIMAGIRI_DATA.amenities,
    sectors: ['Aster', 'Bluebell', 'Carnation', 'Dhalia', 'Exotica', 'Florentine', 'Gardenia', 'Hibiscus'],
    roadLabels: [
      { name: "ASTER ROAD", x: 188, y: 482, vertical: true },
      { name: "BLUEBELL ROAD", x: 306, y: 482, vertical: true },
      { name: "CARNATION ROAD", x: 424, y: 482, vertical: true },
      { name: "DHALIA ROAD", x: 542, y: 482, vertical: true },
      { name: "EXOTICA ROAD", x: 660, y: 482, vertical: true },
      { name: "FLORENTINE ROAD", x: 778, y: 482, vertical: true },
      { name: "GARDENIA ROAD", x: 896, y: 482, vertical: true },
      { name: "HIBISCUS ROAD", x: 337, y: 810, vertical: true },
      { name: "MAIN AVENUE (GATE 1)", x: 306, y: 336, vertical: false },
      { name: "CENTRAL GARDEN ROAD", x: 600, y: 626, vertical: false },
      { name: "GATE 2 ENTRY ROAD", x: 940, y: 336, vertical: false }
    ]
  } : null);

  if (!currentLayout) {
    console.error("Layout data not found!");
    return;
  }

  let plots = currentLayout.plots;
  let nodes = currentLayout.roads.nodes;
  let edges = currentLayout.roads.edges;
  let amenities = currentLayout.amenities;
  let graph = {};

  // Universal Plot / Unit Lookup Helper
  function findPlotInLayout(layout, query) {
    if (!layout || !layout.plots || !query) return null;
    const qClean = String(query).trim().toUpperCase();
    const qNorm = qClean.replace(/^(PLOT|VILLA|HOUSE|BLOCK|TOWER|ROOM|SITE|H\.?NO)\s*#?\s*/i, '').trim();

    if (layout.plots[qClean]) return layout.plots[qClean];
    if (layout.plots[qNorm]) return layout.plots[qNorm];
    if (layout.plots[`T-${qNorm}`]) return layout.plots[`T-${qNorm}`];
    if (layout.plots[`T-${qClean}`]) return layout.plots[`T-${qClean}`];

    for (const pid in layout.plots) {
      const p = layout.plots[pid];
      const numClean = p.number.toUpperCase();
      if (numClean === qClean || numClean === qNorm) return p;
      if (numClean.replace(/^(PLOT|VILLA|HOUSE|BLOCK|TOWER)\s*/i, '').trim() === qNorm) return p;
      if (p.id.toUpperCase() === qNorm) return p;
    }
    return null;
  }

  // Pre-build Graph Adjacency List for Dijkstra
  function buildGraph() {
    graph = {};
    for (const nid in nodes) {
      graph[nid] = [];
    }
    for (const e of edges) {
      const u = nodes[e.u];
      const v = nodes[e.v];
      if (u && v) {
        const dist = Math.hypot(u.x - v.x, u.y - v.y);
        graph[e.u].push({ node: e.v, dist, road: e.road });
        graph[e.v].push({ node: e.u, dist, road: e.road });
      }
    }
  }

  // State Management
  const state = {
    selectedPlotId: null,
    startNodeId: "gate_1", // Default starting gate
    activeRoute: null,
    transform: { x: 0, y: 0, scale: 0.9 },
    isDragging: false,
    dragStart: { x: 0, y: 0 },
    animationFrameId: null,
    carProgress: 0,
    voiceMuted: false,
    showNumbers: true,
    showAmenities: true,
    showRoadNames: true,
    activeFilter: 'ALL',
    userLocation: null,
    isGeoTracking: false,
    geoWatchId: null
  };

  // DOM Elements
  const svg = document.getElementById('map-svg');
  const viewport = document.getElementById('viewport-group');
  const plotsLayer = document.getElementById('plots-layer');
  const roadsLayer = document.getElementById('roads-layer');
  const amenitiesLayer = document.getElementById('amenities-layer');
  const routeLayer = document.getElementById('route-layer');
  const geoLayer = document.getElementById('geo-layer');
  const labelsLayer = document.getElementById('labels-layer');
  const tooltip = document.getElementById('map-tooltip');

  // UI Controls
  const searchInput = document.getElementById('search-input');
  const voiceBtn = document.getElementById('voice-btn');
  const assistantResponse = document.getElementById('assistant-response');
  const assistantText = document.getElementById('assistant-text');
  const speakBtn = document.getElementById('speak-btn');
  const startSelect = document.getElementById('start-node-select');
  const destSelect = document.getElementById('dest-node-select');
  const routeSummary = document.getElementById('route-summary');
  const distanceVal = document.getElementById('distance-val');
  const walkTimeVal = document.getElementById('walk-time-val');
  const driveTimeVal = document.getElementById('drive-time-val');
  const stepsList = document.getElementById('steps-list');
  const houseCard = document.getElementById('house-card');
  const originalModal = document.getElementById('original-map-modal');

  // Build initial Dijkstra graph
  buildGraph();

  // --- 1. RENDER SVG MAP ---
  function initMap() {
    renderPerimeterAndLandscaping();
    renderRoads();
    renderPlots();
    renderAmenities();
    renderAvenueFilterPills();
    populateSelectDropdowns();
    setupPanZoom();
    checkUrlParams();
  }

  // Landscaping & Perimeter
  function renderPerimeterAndLandscaping() {
    let bgGroup = document.getElementById("landscaping-layer");
    if (!bgGroup) {
      bgGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      bgGroup.setAttribute("id", "landscaping-layer");
      viewport.insertBefore(bgGroup, viewport.firstChild);
    } else {
      bgGroup.innerHTML = '';
    }

    // Outer layout ground polygon
    const ground = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    const groundPoints = currentLayout.groundPolygon || "40,320 80,180 300,160 850,140 1050,140 1260,170 1250,600 1150,620 950,830 800,900 500,890 280,880 30,830 30,620";
    ground.setAttribute("points", groundPoints);
    ground.setAttribute("fill", "#090d16");
    ground.setAttribute("stroke", "#334155");
    ground.setAttribute("stroke-width", "2");
    ground.setAttribute("stroke-dasharray", "6,4");
    bgGroup.appendChild(ground);

    // Landscaped perimeter tree border
    if (currentLayout.borderTreesPath) {
      const borderTrees = document.createElementNS("http://www.w3.org/2000/svg", "path");
      borderTrees.setAttribute("d", currentLayout.borderTreesPath);
      borderTrees.setAttribute("fill", "none");
      borderTrees.setAttribute("stroke", "#059669");
      borderTrees.setAttribute("stroke-width", "12");
      borderTrees.setAttribute("stroke-linecap", "round");
      borderTrees.setAttribute("stroke-linejoin", "round");
      borderTrees.setAttribute("opacity", "0.45");
      bgGroup.appendChild(borderTrees);
    }

    // Central Garden Park Area polygon
    if (currentLayout.gardenPark) {
      const gp = currentLayout.gardenPark;
      const gardenPark = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      gardenPark.setAttribute("x", gp.x);
      gardenPark.setAttribute("y", gp.y);
      gardenPark.setAttribute("width", gp.w);
      gardenPark.setAttribute("height", gp.h);
      gardenPark.setAttribute("rx", gp.rx || "6");
      gardenPark.setAttribute("fill", "#064e3b");
      gardenPark.setAttribute("stroke", "#10b981");
      gardenPark.setAttribute("stroke-width", "1.5");
      bgGroup.appendChild(gardenPark);
    }

    // Children Play Area polygon (Himagiri specific)
    if (currentLayout.id === 'himagiri') {
      const playArea = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      playArea.setAttribute("x", "250");
      playArea.setAttribute("y", "625");
      playArea.setAttribute("width", "180");
      playArea.setAttribute("height", "45");
      playArea.setAttribute("rx", "6");
      playArea.setAttribute("fill", "#065f46");
      playArea.setAttribute("stroke", "#34d399");
      playArea.setAttribute("stroke-width", "1.5");
      bgGroup.appendChild(playArea);
    }
  }

  // Render Asphalt Roads and Centerlines
  function renderRoads() {
    roadsLayer.innerHTML = '';
    const corridorGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const centerlinesGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");

    // Road corridors
    for (const edge of edges) {
      const u = nodes[edge.u];
      const v = nodes[edge.v];
      if (!u || !v) continue;

      const roadPath = document.createElementNS("http://www.w3.org/2000/svg", "line");
      roadPath.setAttribute("x1", u.x);
      roadPath.setAttribute("y1", u.y);
      roadPath.setAttribute("x2", v.x);
      roadPath.setAttribute("y2", v.y);
      roadPath.setAttribute("stroke", "#1e293b");
      roadPath.setAttribute("stroke-width", currentLayout.id === 'tech_horizon' ? "26" : "22");
      roadPath.setAttribute("stroke-linecap", "round");
      roadPath.setAttribute("stroke-linejoin", "round");
      corridorGroup.appendChild(roadPath);

      const cline = document.createElementNS("http://www.w3.org/2000/svg", "line");
      cline.setAttribute("x1", u.x);
      cline.setAttribute("y1", u.y);
      cline.setAttribute("x2", v.x);
      cline.setAttribute("y2", v.y);
      cline.setAttribute("class", "road-centerline");
      cline.setAttribute("stroke-linecap", "round");
      centerlinesGroup.appendChild(cline);
    }

    roadsLayer.appendChild(corridorGroup);
    roadsLayer.appendChild(centerlinesGroup);

    // Dynamic Road Labels from currentLayout
    const roadLabels = currentLayout.roadLabels || [];

    const labelsG = document.createElementNS("http://www.w3.org/2000/svg", "g");
    labelsG.setAttribute("id", "road-name-labels");

    for (const rl of roadLabels) {
      const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
      txt.setAttribute("class", "road-label");
      txt.textContent = rl.name;

      if (rl.vertical) {
        txt.setAttribute("transform", `translate(${rl.x}, ${rl.y}) rotate(-90)`);
        txt.setAttribute("text-anchor", "middle");
      } else {
        txt.setAttribute("x", rl.x);
        txt.setAttribute("y", rl.y - 14);
        txt.setAttribute("text-anchor", "middle");
      }
      labelsG.appendChild(txt);
    }
    roadsLayer.appendChild(labelsG);
  }

  // Render Plots with House Numbers
  function renderPlots() {
    plotsLayer.innerHTML = '';

    for (const pid in plots) {
      const p = plots[pid];
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "svg-plot");
      g.setAttribute("id", `plot-${p.id}`);
      g.setAttribute("data-id", p.id);
      g.setAttribute("data-road", p.road);

      // Plot polygon / rectangle
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", p.x);
      rect.setAttribute("y", p.y);
      rect.setAttribute("width", p.w);
      rect.setAttribute("height", p.h);

      let fillColor = '#1e293b';
      let strokeColor = '#3b82f6';
      if (p.color === 'green' || p.color === 'lightgreen') {
        fillColor = '#064e3b';
        strokeColor = '#10b981';
      } else if (p.color === 'yellow' || p.color === 'lightyellow') {
        fillColor = '#451a03';
        strokeColor = '#f59e0b';
      } else if (p.color === 'blue') {
        fillColor = '#1e3a8a';
        strokeColor = '#38bdf8';
      } else if (p.color === 'purple') {
        fillColor = '#4c1d95';
        strokeColor = '#a855f7';
      }

      rect.setAttribute("fill", fillColor);
      rect.setAttribute("stroke", strokeColor);

      // Plot number text
      const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
      txt.setAttribute("class", "plot-label");
      txt.setAttribute("x", p.x + p.w / 2);
      txt.setAttribute("y", p.y + p.h / 2);

      if (p.number.length >= 8) {
        txt.setAttribute("font-size", "7.5px");
        txt.classList.add("plot-label-long");
      } else if (p.number.length >= 5) {
        txt.setAttribute("font-size", "8.5px");
        txt.classList.add("plot-label-long");
      } else if (p.number.length >= 4) {
        txt.setAttribute("font-size", "10px");
        txt.classList.add("plot-label-mid");
      } else {
        txt.setAttribute("font-size", "11.5px");
      }
      txt.textContent = p.number;

      g.appendChild(rect);
      g.appendChild(txt);

      // Interactions
      g.addEventListener('click', () => selectPlot(p.id, true));
      g.addEventListener('mouseenter', (e) => showPlotTooltip(e, p));
      g.addEventListener('mousemove', (e) => movePlotTooltip(e));
      g.addEventListener('mouseleave', hidePlotTooltip);

      plotsLayer.appendChild(g);
    }
  }

  // Render Amenities (Gates, Parks, Temple, Clubhouse, etc.)
  function renderAmenities() {
    amenitiesLayer.innerHTML = '';

    for (const am of amenities) {
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "amenity-pin");
      g.setAttribute("id", `amenity-${am.id}`);
      g.setAttribute("cursor", "pointer");

      const isGate = am.type === 'gate' || am.id.includes('gate');
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", am.x);
      circle.setAttribute("cy", am.y);
      circle.setAttribute("r", isGate ? "15" : "12");

      let bgColor = "#0284c7";
      if (isGate) bgColor = "#059669";
      else if (am.type === 'worship') bgColor = "#d97706";
      else if (am.type === 'recreation') bgColor = "#16a34a";
      else if (am.type === 'sports' || am.id.includes('clubhouse')) bgColor = "#0891b2";
      else if (am.type === 'civic' || am.id.includes('food')) bgColor = "#ea580c";
      else if (am.type === 'utility') bgColor = "#475569";

      circle.setAttribute("fill", bgColor);
      circle.setAttribute("stroke", "#ffffff");
      circle.setAttribute("stroke-width", "2");
      circle.setAttribute("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.4))");

      const iconTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
      iconTxt.setAttribute("x", am.x);
      iconTxt.setAttribute("y", am.y);
      iconTxt.setAttribute("text-anchor", "middle");
      iconTxt.setAttribute("dominant-baseline", "central");
      iconTxt.setAttribute("fill", "#ffffff");
      iconTxt.setAttribute("font-size", isGate ? "10px" : "8.5px");
      iconTxt.setAttribute("font-weight", "800");

      if (am.id === 'gate_1') iconTxt.textContent = "G1";
      else if (am.id === 'gate_2') iconTxt.textContent = "G2";
      else if (isGate) iconTxt.textContent = "🚪";
      else if (am.type === 'worship') iconTxt.textContent = "🛕";
      else if (am.type === 'recreation') iconTxt.textContent = "🌳";
      else if (am.id.includes('clubhouse') || am.type === 'sports') iconTxt.textContent = "🏊";
      else if (am.id.includes('food') || am.id.includes('cafeteria')) iconTxt.textContent = "🍽️";
      else if (am.id.includes('bus')) iconTxt.textContent = "🚌";
      else if (am.id.includes('parking') || am.id.includes('mlcp')) iconTxt.textContent = "🅿️";
      else if (am.id.includes('auditorium') || am.id.includes('convention')) iconTxt.textContent = "🏛️";
      else if (am.id.includes('atm')) iconTxt.textContent = "💳";
      else if (am.id.includes('ev')) iconTxt.textContent = "⚡";
      else iconTxt.textContent = "★";

      // Text Title underneath
      const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
      title.setAttribute("x", am.x);
      title.setAttribute("y", am.y + (isGate ? 24 : 20));
      title.setAttribute("text-anchor", "middle");
      title.setAttribute("fill", "#f8fafc");
      title.setAttribute("font-size", "10px");
      title.setAttribute("font-weight", "700");
      title.setAttribute("filter", "drop-shadow(0 1px 2px rgba(0,0,0,0.9))");
      title.textContent = am.name.split(' (')[0];

      g.appendChild(circle);
      g.appendChild(iconTxt);
      g.appendChild(title);

      g.addEventListener('click', () => {
        selectAmenity(am.id, true);
      });
      g.addEventListener('mouseenter', (e) => {
        tooltip.innerHTML = `<strong>${am.name}</strong><br><span style="color:#94a3b8;font-size:11px;">${am.description || am.desc || 'Amenity'}</span>`;
        tooltip.style.display = 'block';
        movePlotTooltip(e);
      });
      g.addEventListener('mousemove', movePlotTooltip);
      g.addEventListener('mouseleave', hidePlotTooltip);

      amenitiesLayer.appendChild(g);
    }
  }

  // Dynamic Avenue Filter Pills from currentLayout
  function renderAvenueFilterPills() {
    const container = document.querySelector('.sector-pills');
    if (!container) return;
    const sectors = currentLayout && currentLayout.sectors ? currentLayout.sectors : [];
    const unitLabel = currentLayout.unitType === 'Tower / Block' ? 'Zones' : 'Avenues';
    container.innerHTML = `<button class="sector-pill active" data-sector="ALL">All ${unitLabel}</button>`;

    sectors.forEach(s => {
      const btn = document.createElement('button');
      btn.className = 'sector-pill';
      btn.setAttribute('data-sector', s);
      btn.textContent = s.replace(/ (Road|Avenue|Boulevard|Court|Drive|Way|Link)/i, '');
      btn.addEventListener('click', () => {
        container.querySelectorAll('.sector-pill').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        applySectorFilter(s);
      });
      container.appendChild(btn);
    });

    const allBtn = container.querySelector('[data-sector="ALL"]');
    if (allBtn) {
      allBtn.addEventListener('click', () => {
        container.querySelectorAll('.sector-pill').forEach(p => p.classList.remove('active'));
        allBtn.classList.add('active');
        applySectorFilter('ALL');
      });
    }
  }

  // Populate Start & Destination Dropdowns dynamically
  function populateSelectDropdowns() {
    const gateNodes = Object.entries(nodes).filter(([id, n]) => id.includes('gate') && !id.includes('entry') && !id.includes('_x'));
    const landmarkNodes = amenities.slice(0, 6);

    let startHtml = `
      <optgroup label="📍 Your Position">
        <option value="my_location">📍 My Live Location (GPS)</option>
      </optgroup>
      <optgroup label="Community Gates">`;
    
    if (gateNodes.length > 0) {
      gateNodes.forEach(([id, n], idx) => {
        startHtml += `<option value="${id}" ${idx === 0 ? 'selected' : ''}>${n.label || id}</option>`;
      });
    } else {
      startHtml += `<option value="${Object.keys(nodes)[0]}" selected>Main Entrance</option>`;
    }
    startHtml += `</optgroup><optgroup label="Key Landmarks">`;
    landmarkNodes.forEach(am => {
      startHtml += `<option value="${am.roadNode || am.id}">${am.name}</option>`;
    });
    startHtml += `</optgroup>`;
    startSelect.innerHTML = startHtml;

    // Destination selector with all plots & amenities
    const uType = currentLayout.unitType || 'House';
    destSelect.innerHTML = `<option value="">-- Choose ${uType} or Landmark --</option>`;

    // Amenities group
    const amGroup = document.createElement('optgroup');
    amGroup.label = "Society Amenities & Landmarks";
    for (const am of amenities) {
      const opt = document.createElement('option');
      opt.value = `amenity:${am.id}`;
      opt.textContent = `${am.name}`;
      amGroup.appendChild(opt);
    }
    destSelect.appendChild(amGroup);

    // Plots grouped by road
    const roads = {};
    for (const pid in plots) {
      const road = plots[pid].road;
      if (!roads[road]) roads[road] = [];
      roads[road].push(plots[pid]);
    }

    for (const roadName in roads) {
      const grp = document.createElement('optgroup');
      grp.label = roadName;
      roads[roadName].sort((a, b) => {
        const na = parseInt(a.number) || 0;
        const nb = parseInt(b.number) || 0;
        if (na !== nb) return na - nb;
        return a.number.localeCompare(b.number);
      });
      for (const p of roads[roadName]) {
        const opt = document.createElement('option');
        opt.value = `plot:${p.id}`;
        opt.textContent = `${uType} #${p.number} (${p.road})`;
        grp.appendChild(opt);
      }
      destSelect.appendChild(grp);
    }
  }

  // Layout Switcher: dynamically swaps active dataset, blueprints, roads & units
  function loadLayout(layoutId, targetPlotId = null) {
    if (!layouts[layoutId]) {
      console.warn("Layout not found in window.LAYOUTS:", layoutId);
      return;
    }
    currentLayoutId = layoutId;
    currentLayout = layouts[layoutId];
    plots = currentLayout.plots;
    nodes = currentLayout.roads.nodes;
    edges = currentLayout.roads.edges;
    amenities = currentLayout.amenities;

    // Set default start gate
    const gateNodes = Object.keys(nodes).filter(k => k.includes('gate') && !k.includes('entry') && !k.includes('_x'));
    state.startNodeId = gateNodes.length > 0 ? gateNodes[0] : Object.keys(nodes)[0];
    state.selectedPlotId = null;
    state.activeRoute = null;

    buildGraph();

    renderPerimeterAndLandscaping();
    renderRoads();
    renderPlots();
    renderAmenities();
    renderAvenueFilterPills();
    populateSelectDropdowns();

    updateHeaderForLayout(currentLayout);

    // Switch view
    const portal = document.getElementById('portal-view');
    const mapApp = document.getElementById('app-container');
    const backBtn = document.getElementById('header-back-btn');
    const headerBadges = document.getElementById('header-badges');
    const headerMapControls = document.getElementById('header-map-controls');

    if (portal) portal.style.display = 'none';
    if (mapApp) mapApp.style.display = 'flex';
    if (backBtn) backBtn.style.display = 'flex';
    if (headerBadges) headerBadges.style.display = (window.innerWidth > 900) ? 'flex' : 'none';
    if (headerMapControls) headerMapControls.style.display = 'flex';

    if (routeLayer) routeLayer.innerHTML = '';
    if (houseCard) houseCard.classList.remove('active');
    if (routeSummary) routeSummary.style.display = 'none';

    setTimeout(() => {
      fitMapToView(true);
      if (targetPlotId) {
        selectPlot(targetPlotId, true);
        calculateAndDisplayRoute(state.startNodeId, targetPlotId);
        const p = plots[targetPlotId];
        startLayoutTutorial(currentLayout, p ? p.number : targetPlotId);
      }
    }, 120);
  }

  // Update header titles & badges for current layout
  function updateHeaderForLayout(layout) {
    const brandTitle = document.getElementById('brand-title');
    const brandSub = document.getElementById('brand-subtitle');
    const brandIcon = document.getElementById('brand-icon');
    const headerBadges = document.getElementById('header-badges');

    if (brandTitle) brandTitle.textContent = layout.name;
    if (brandSub) brandSub.textContent = layout.location;
    if (brandIcon) {
      brandIcon.textContent = layout.id === 'tech_horizon' ? '🏢' : (layout.id === 'greenwood' ? '🌳' : '🗺️');
    }

    if (headerBadges) {
      const plotCount = Object.keys(layout.plots).length;
      const secCount = layout.sectors ? layout.sectors.length : 0;
      const amenCount = layout.amenities ? layout.amenities.length : 0;
      const unitLabel = layout.unitType === 'Plot' ? 'Plots' : (layout.unitType === 'Villa' ? 'Villas' : 'Units');

      headerBadges.innerHTML = `
        <span class="badge badge-info">${plotCount} ${unitLabel}</span>
        <span class="badge badge-success">${secCount} ${layout.unitType === 'Tower / Block' ? 'Zones' : 'Avenues'}</span>
        <span class="badge badge-info">${amenCount} Amenities</span>
      `;
    }
  }

  // --- GUIDED LAYOUT TUTORIAL ENGINE ---
  let tutorialCurrentStep = 0;
  let activeTutorialLayout = null;
  let activeTutorialUnit = null;

  function getTutorialSteps(layout, unitNumber) {
    const lay = layout || currentLayout;
    const unitLabel = lay.unitType || 'House';
    const targetUnit = unitNumber ? `${unitLabel} #${unitNumber}` : `your selected ${unitLabel.toLowerCase()}`;
    const sectorsName = lay.unitType === 'Tower / Block' ? 'zones' : 'avenues';
    const sectorsSample = lay.sectors && lay.sectors.length > 0 ? lay.sectors.slice(0, 3).join(', ') : 'main roads';

    return [
      {
        counter: "Feature 1 of 5",
        icon: "🧭",
        title: "Turn-by-Turn Route Navigation",
        desc: `Follow the glowing cyan navigation path from the security gate directly to ${targetUnit}. The route card at the bottom displays real-time pedestrian walking distance and estimated arrival time.`,
        highlightSelector: "#route-summary"
      },
      {
        counter: "Feature 2 of 5",
        icon: "🏠",
        title: `${unitLabel} Information Card`,
        desc: `Tap any ${unitLabel.toLowerCase()} on the map anytime. The property card slides up showing street address, compass facing direction, and exact walking distance from both gates.`,
        highlightSelector: "#house-card"
      },
      {
        counter: "Feature 3 of 5",
        icon: "📡",
        title: "Live GPS Wayfinding Radar",
        desc: `Tap '📍 My Location' to track your exact walking coordinates inside the layout. A pulsating blue radar pin shows your live location and recalculates your route dynamically as you walk.`,
        highlightSelector: "#use-my-loc-btn"
      },
      {
        counter: "Feature 4 of 5",
        icon: "🔍",
        title: "Instant Search & Sector Filters",
        desc: `Use the search box to find any ${unitLabel.toLowerCase()} or amenity, or tap the ${sectorsName} filter pills (${sectorsSample}) to isolate specific areas of the layout.`,
        highlightSelector: ".sector-pills"
      },
      {
        counter: "Feature 5 of 5",
        icon: "🗺️",
        title: "Interactive Canvas & Center Button",
        desc: `Pinch or drag freely across the entire high-definition blueprint. Tap the 'CTR' button anytime to instantly snap your camera back to the central park, temple, and amenities.`,
        highlightSelector: "#focus-center-btn"
      }
    ];
  }

  function startLayoutTutorial(layout, unitNumber = null) {
    activeTutorialLayout = layout || currentLayout;
    activeTutorialUnit = unitNumber;
    tutorialCurrentStep = 0;

    const overlay = document.getElementById('layout-tutorial-overlay');
    if (!overlay) return;

    overlay.style.display = 'flex';
    renderTutorialStep();
  }

  function renderTutorialStep() {
    const steps = getTutorialSteps(activeTutorialLayout, activeTutorialUnit);
    const step = steps[tutorialCurrentStep];
    if (!step) return;

    const counter = document.getElementById('tutorial-step-counter');
    const icon = document.getElementById('tutorial-icon');
    const title = document.getElementById('tutorial-title');
    const desc = document.getElementById('tutorial-desc');
    const prevBtn = document.getElementById('tutorial-prev-btn');
    const nextBtn = document.getElementById('tutorial-next-btn');
    const finishBtn = document.getElementById('tutorial-finish-btn');

    if (counter) counter.textContent = step.counter;
    if (icon) icon.textContent = step.icon;
    if (title) title.textContent = step.title;
    if (desc) desc.textContent = step.desc;

    if (prevBtn) prevBtn.style.display = tutorialCurrentStep > 0 ? 'inline-flex' : 'none';
    if (nextBtn) nextBtn.style.display = tutorialCurrentStep < steps.length - 1 ? 'inline-flex' : 'none';
    if (finishBtn) finishBtn.style.display = tutorialCurrentStep === steps.length - 1 ? 'inline-flex' : 'none';

    document.querySelectorAll('.tutorial-highlight-pulse').forEach(el => el.classList.remove('tutorial-highlight-pulse'));

    if (step.highlightSelector) {
      const el = document.querySelector(step.highlightSelector);
      if (el) {
        el.classList.add('tutorial-highlight-pulse');
        if (el.id === 'house-card' && state.selectedPlotId) {
          el.classList.add('active');
        }
        if (el.id === 'route-summary' && state.activeRoute) {
          el.style.display = 'flex';
        }
      }
    }
  }

  function closeTutorial() {
    const overlay = document.getElementById('layout-tutorial-overlay');
    if (overlay) overlay.style.display = 'none';
    document.querySelectorAll('.tutorial-highlight-pulse').forEach(el => el.classList.remove('tutorial-highlight-pulse'));
  }

  // --- 2. DIJKSTRA SHORTEST PATHFINDING ---
  function findShortestPath(startNid, endNid) {
    if (!nodes[startNid] || !nodes[endNid]) return null;
    if (startNid === endNid) return [startNid];

    const distances = {};
    const previous = {};
    const visited = new Set();
    const unvisited = new Set(Object.keys(nodes));

    for (const nid in nodes) {
      distances[nid] = Infinity;
    }
    distances[startNid] = 0;

    while (unvisited.size > 0) {
      // Find node with min distance
      let current = null;
      let minDist = Infinity;
      for (const nid of unvisited) {
        if (distances[nid] < minDist) {
          minDist = distances[nid];
          current = nid;
        }
      }

      if (current === null || minDist === Infinity) break;
      if (current === endNid) break;

      unvisited.delete(current);
      visited.add(current);

      for (const edge of graph[current]) {
        if (visited.has(edge.node)) continue;
        const alt = distances[current] + edge.dist;
        if (alt < distances[edge.node]) {
          distances[edge.node] = alt;
          previous[edge.node] = { from: current, road: edge.road, dist: edge.dist };
        }
      }
    }

    if (distances[endNid] === Infinity) return null;

    // Reconstruct path
    const pathNodes = [];
    const pathEdges = [];
    let curr = endNid;
    while (curr !== startNid) {
      pathNodes.unshift(curr);
      const prevInfo = previous[curr];
      if (!prevInfo) break;
      pathEdges.unshift({ u: prevInfo.from, v: curr, road: prevInfo.road, dist: prevInfo.dist });
      curr = prevInfo.from;
    }
    pathNodes.unshift(startNid);

    return {
      nodes: pathNodes,
      edges: pathEdges,
      totalDist: distances[endNid]
    };
  }

  // --- 3. TURN-BY-TURN DIRECTIONS BUILDER ---
  function generateTurnByTurnDirections(routeResult, targetPlot, startNodeId) {
    const steps = [];
    const startName = nodes[startNodeId]?.label || "Starting Point";
    const destName = targetPlot ? `House #${targetPlot.number}` : "Destination";

    // Step 1: Start
    steps.push({
      icon: "🚪",
      text: `Start from <strong>${startName}</strong>`,
      dist: 0
    });

    let currentRoad = "";
    let accumulatedDist = 0;

    for (let i = 0; i < routeResult.edges.length; i++) {
      const edge = routeResult.edges[i];
      const roadName = edge.road;
      const legDist = Math.round(edge.dist * 0.9); // scaling to realistic meters

      if (i === 0) {
        currentRoad = roadName;
        accumulatedDist = legDist;
      } else if (roadName === currentRoad) {
        accumulatedDist += legDist;
      } else {
        // Road changed -> Determine Turn direction (Left vs Right)
        const u = nodes[routeResult.edges[i - 1].u];
        const v = nodes[routeResult.edges[i - 1].v];
        const nextV = nodes[edge.v];

        const dx1 = v.x - u.x;
        const dy1 = v.y - u.y;
        const dx2 = nextV.x - v.x;
        const dy2 = nextV.y - v.y;

        // Cross product determines turn direction
        const cross = dx1 * dy2 - dy1 * dx2;
        let turnStr = "Turn onto";
        let turnIcon = "⬆️";

        if (cross > 50) {
          turnStr = "Turn Right onto";
          turnIcon = "↪️";
        } else if (cross < -50) {
          turnStr = "Turn Left onto";
          turnIcon = "↩️";
        } else {
          turnStr = "Continue onto";
          turnIcon = "⬆️";
        }

        steps.push({
          icon: "🚶",
          text: `Follow <strong>${currentRoad}</strong>`,
          dist: accumulatedDist
        });

        steps.push({
          icon: turnIcon,
          text: `<strong>${turnStr} ${roadName}</strong>`,
          dist: 0
        });

        currentRoad = roadName;
        accumulatedDist = legDist;
      }
    }

    if (accumulatedDist > 0) {
      steps.push({
        icon: "🚶",
        text: `Proceed along <strong>${currentRoad}</strong>`,
        dist: accumulatedDist
      });
    }

    // Final arrival step
    if (targetPlot) {
      const facing = targetPlot.facing ? ` (${targetPlot.facing}-facing)` : '';
      steps.push({
        icon: "🏁",
        text: `Arrive at <strong>House #${targetPlot.number}</strong> on ${targetPlot.road}${facing}`,
        dist: 0
      });
    } else {
      steps.push({
        icon: "🏁",
        text: `You have reached your destination!`,
        dist: 0
      });
    }

    return steps;
  }

  // Toast Notification Helper
  function showToast(message, duration = 3500) {
    let toast = document.getElementById('map-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'map-toast';
      toast.style.position = 'fixed';
      toast.style.bottom = window.innerWidth <= 900 ? '49vh' : '24px';
      toast.style.left = '50%';
      toast.style.transform = 'translateX(-50%)';
      toast.style.background = 'rgba(15, 23, 42, 0.94)';
      toast.style.color = '#ffffff';
      toast.style.padding = '10px 18px';
      toast.style.borderRadius = '24px';
      toast.style.fontSize = '12px';
      toast.style.fontWeight = '600';
      toast.style.zIndex = '9999';
      toast.style.boxShadow = '0 6px 20px rgba(0,0,0,0.35)';
      toast.style.backdropFilter = 'blur(6px)';
      toast.style.textAlign = 'center';
      toast.style.maxWidth = '92vw';
      toast.style.pointerEvents = 'none';
      toast.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
      document.body.appendChild(toast);
    }
    toast.innerHTML = message;
    toast.style.opacity = '1';
    toast.style.display = 'block';
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => { toast.style.display = 'none'; }, 250);
    }, duration);
  }

  // --- GEOLOCATION MODULE (GPS to Map Projection & Real-Time Tracking) ---
  const GPS_REF = {
    minLat: 12.8588, // South perimeter (Play Area / Temple)
    maxLat: 12.8622, // North perimeter (Plots 1A/1B/1C)
    minLng: 77.5898, // West perimeter (Gate 1 / Aster Road)
    maxLng: 77.5952, // East perimeter (Gate 2 / Hibiscus Road)
    minX: 140,
    maxX: 1000,
    minY: 200,
    maxY: 640
  };

  function gpsToMap(lat, lng) {
    const normX = (lng - GPS_REF.minLng) / (GPS_REF.maxLng - GPS_REF.minLng);
    const normY = (GPS_REF.maxLat - lat) / (GPS_REF.maxLat - GPS_REF.minLat);
    const mapX = GPS_REF.minX + normX * (GPS_REF.maxX - GPS_REF.minX);
    const mapY = GPS_REF.minY + normY * (GPS_REF.maxY - GPS_REF.minY);
    return { mapX, mapY };
  }

  function getDistanceMeters(lat1, lon1, lat2, lon2) {
    const R = 6371e3;
    const phi1 = lat1 * Math.PI / 180;
    const phi2 = lat2 * Math.PI / 180;
    const deltaPhi = (lat2 - lat1) * Math.PI / 180;
    const deltaLambda = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
              Math.cos(phi1) * Math.cos(phi2) *
              Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function findClosestRoadNode(x, y) {
    let closestId = 'gate_1';
    let minDist = Infinity;
    for (const nid in nodes) {
      const n = nodes[nid];
      const dx = n.x - x;
      const dy = n.y - y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < minDist) {
        minDist = dist;
        closestId = nid;
      }
    }
    return closestId;
  }

  function updateUserLocationMarker(mapX, mapY, accuracyMeters = 15, heading = null) {
    if (!geoLayer) return;
    const clampedX = Math.max(80, Math.min(1250, mapX));
    const clampedY = Math.max(120, Math.min(880, mapY));
    const pxRadius = Math.max(14, Math.min(65, accuracyMeters * 1.1));

    geoLayer.innerHTML = `
      <!-- Accuracy Circle -->
      <circle cx="${clampedX}" cy="${clampedY}" r="${pxRadius}" fill="rgba(37, 99, 235, 0.12)" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,3" />
      <!-- Radar Pulse Ring -->
      <circle id="geo-pulse-ring" cx="${clampedX}" cy="${clampedY}" r="14" fill="rgba(37, 99, 235, 0.28)" />
      <!-- Center User Pin -->
      <circle cx="${clampedX}" cy="${clampedY}" r="8.5" fill="#2563eb" stroke="#ffffff" stroke-width="2.5" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.45))" />
      <circle cx="${clampedX}" cy="${clampedY}" r="3" fill="#ffffff" />
      <!-- Label Pin -->
      <g transform="translate(${clampedX}, ${clampedY - 16})">
        <rect x="-38" y="-18" width="76" height="18" rx="9" fill="#0f172a" />
        <text x="0" y="-5" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="700">YOU ARE HERE</text>
      </g>
    `;
  }

  function startLocationTracking(centerOnUser = true) {
    if (!navigator.geolocation) {
      showToast("Geolocation is not supported by your browser.", 3000);
      return;
    }

    const geoBtn = document.getElementById('geo-btn');
    if (geoBtn) geoBtn.classList.add('active');
    state.isGeoTracking = true;

    showToast("Acquiring GPS location... 🛰️", 2000);

    const geoSuccess = (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const accuracy = position.coords.accuracy || 20;
      const heading = position.coords.heading;

      // Distance from Himagiri Meadows center (12.8605, 77.5925)
      const distToLayout = getDistanceMeters(lat, lng, 12.8605, 77.5925);

      let mapX, mapY;
      if (distToLayout <= 1500) {
        // User is inside or near the layout
        const proj = gpsToMap(lat, lng);
        mapX = proj.mapX;
        mapY = proj.mapY;
        if (!state.userLocation && centerOnUser) {
          showToast("📍 Located inside Himagiri Meadows!", 3000);
          zoomToCoordinates(mapX, mapY, 1.8);
        }
      } else {
        // User is testing outside layout (e.g. at home)
        // Default to Gate 1 Entrance so routing works seamlessly
        mapX = 80;
        mapY = 336;
        if (!state.userLocation) {
          const distKm = (distToLayout / 1000).toFixed(1);
          showToast(`📍 Live GPS active (~${distKm} km away). Placed at Gate 1 for navigation. (Click map to change location)`, 4500);
          if (centerOnUser) {
            zoomToCoordinates(80, 336, 1.8);
          }
        }
      }

      state.userLocation = { lat, lng, mapX, mapY, accuracy, heading };
      updateUserLocationMarker(mapX, mapY, accuracy, heading);

      // If live location route is selected, dynamically re-route
      if (state.startNodeId === 'my_location' && state.selectedPlotId) {
        calculateAndDisplayRoute('my_location', state.selectedPlotId);
      }
    };

    const geoError = (error) => {
      console.warn("Geolocation error:", error);
      showToast("Could not access GPS. Defaulted to Gate 1. Tap anywhere on map to set your location.", 4000);
      state.userLocation = { lat: 12.8605, lng: 77.5898, mapX: 140, mapY: 340, accuracy: 20 };
      updateUserLocationMarker(140, 340, 20);
      if (centerOnUser) {
        zoomToCoordinates(140, 340, 1.8);
      }
    };

    if (state.geoWatchId !== null) {
      navigator.geolocation.clearWatch(state.geoWatchId);
    }
    state.geoWatchId = navigator.geolocation.watchPosition(geoSuccess, geoError, {
      enableHighAccuracy: true,
      maximumAge: 3000,
      timeout: 10000
    });
  }

  function stopLocationTracking() {
    if (state.geoWatchId !== null) {
      navigator.geolocation.clearWatch(state.geoWatchId);
      state.geoWatchId = null;
    }
    state.isGeoTracking = false;
    const geoBtn = document.getElementById('geo-btn');
    if (geoBtn) geoBtn.classList.remove('active');
    if (geoLayer) geoLayer.innerHTML = '';
    state.userLocation = null;
    showToast("Location tracking stopped.", 2000);
  }

  // --- 4. RENDER ROUTE & ANIMATION ON MAP ---
  function calculateAndDisplayRoute(startNid, targetPlotId) {
    const plot = plots[targetPlotId];
    if (!plot) return;

    const targetNodeId = plot.roadNode;
    let effectiveStartNodeId = startNid;
    let isUserLocationStart = false;

    if (startNid === 'my_location') {
      isUserLocationStart = true;
      if (!state.userLocation) {
        state.userLocation = { mapX: 140, mapY: 340, accuracy: 15 };
        updateUserLocationMarker(140, 340, 15);
      }
      effectiveStartNodeId = findClosestRoadNode(state.userLocation.mapX, state.userLocation.mapY);
    }

    const route = findShortestPath(effectiveStartNodeId, targetNodeId);

    if (!route) {
      console.warn("No route found between", effectiveStartNodeId, targetNodeId);
      return;
    }

    state.activeRoute = route;

    // Build SVG Path coordinates
    const points = [];
    if (isUserLocationStart && state.userLocation) {
      points.push(`${state.userLocation.mapX},${state.userLocation.mapY}`);
    }

    for (const nid of route.nodes) {
      const n = nodes[nid];
      points.push(`${n.x},${n.y}`);
    }

    // Connect from road node directly to plot center door
    const plotCenterX = plot.x + plot.w / 2;
    const plotCenterY = plot.y + plot.h / 2;
    points.push(`${plotCenterX},${plotCenterY}`);

    const pathData = "M " + points.join(" L ");

    const startX = isUserLocationStart ? state.userLocation.mapX : nodes[startNid].x;
    const startY = isUserLocationStart ? state.userLocation.mapY : nodes[startNid].y;
    const startColor = isUserLocationStart ? "#2563eb" : "#10b981";

    // Render in SVG
    routeLayer.innerHTML = `
      <!-- Underlay glow -->
      <path d="${pathData}" class="nav-route-underlay" />
      <!-- Animated dashed route -->
      <path id="active-nav-path" d="${pathData}" class="nav-route-path" />
      <!-- Start Pin -->
      <circle cx="${startX}" cy="${startY}" r="8" fill="${startColor}" stroke="#ffffff" stroke-width="2.5" filter="drop-shadow(0 2px 5px rgba(0,0,0,0.4))" />
      <!-- End Pin / House Indicator -->
      <g transform="translate(${plotCenterX}, ${plotCenterY - 14})">
        <path d="M 0,0 C -6,-10 -6,-16 0,-20 C 6,-16 6,-10 0,0 Z" fill="#ef4444" stroke="#ffffff" stroke-width="1.5" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))" />
        <circle cx="0" cy="-14" r="3" fill="#ffffff" />
      </g>
      <!-- Traveling dot / walker -->
      <circle id="route-traveler" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 0 6px #f59e0b)" />
    `;

    // Start traveling animation
    startRouteTravelerAnimation();

    // Generate Steps & Distance
    let totalDistMeters = Math.round((route.totalDist + 15) * 0.95);
    if (isUserLocationStart && state.userLocation) {
      const dx = state.userLocation.mapX - nodes[effectiveStartNodeId].x;
      const dy = state.userLocation.mapY - nodes[effectiveStartNodeId].y;
      totalDistMeters += Math.round(Math.sqrt(dx * dx + dy * dy) * 0.95);
    }

    const walkMins = Math.max(1, Math.round(totalDistMeters / 70)); // ~70m per min
    const driveMins = Math.max(1, Math.round(totalDistMeters / 250)); // ~250m per min

    distanceVal.textContent = `${totalDistMeters} m`;
    walkTimeVal.textContent = `${walkMins} min`;
    driveTimeVal.textContent = `${driveMins} min`;

    const steps = generateTurnByTurnDirections(route, plot, effectiveStartNodeId);
    if (isUserLocationStart) {
      const closestLabel = nodes[effectiveStartNodeId]?.label || 'the road';
      steps.unshift({
        icon: "📍",
        text: `Start from <strong>Your Current Location</strong> and walk to ${closestLabel}`,
        dist: Math.round(Math.sqrt(Math.pow(state.userLocation.mapX - nodes[effectiveStartNodeId].x, 2) + Math.pow(state.userLocation.mapY - nodes[effectiveStartNodeId].y, 2)) * 0.95)
      });
    }
    renderDirectionsList(steps);

    if (window.HimagiriAnalytics) {
      const sName = isUserLocationStart ? 'Live Location' : (nodes[startNid]?.label?.split(' (')[0] || 'Gate 1');
      window.HimagiriAnalytics.trackRoute(sName, `House #${plot.number}`, totalDistMeters);
    }

    // Natural conversational explanation
    const startLabel = isUserLocationStart ? "your current location" : (nodes[startNid]?.label.split(' (')[0] || "your start location");
    const conversationalText = `House #${plot.number} is located on ${plot.road} in ${plot.block} (${plot.facing}-facing). From ${startLabel}, it is approximately ${totalDistMeters} meters away (about a ${walkMins}-minute walk). Follow the glowing cyan navigation route highlighted on the map.`;
    displayAssistantResponse(conversationalText);

    // Highlight active plot
    highlightPlot(plot.id);

    return { totalDistMeters, walkMins, steps, conversationalText };
  }

  // Animated vehicle / traveler along the route path
  function startRouteTravelerAnimation() {
    if (state.animationFrameId) {
      cancelAnimationFrame(state.animationFrameId);
    }

    const pathElem = document.getElementById('active-nav-path');
    const traveler = document.getElementById('route-traveler');
    if (!pathElem || !traveler) return;

    const pathLength = pathElem.getTotalLength();
    let startTime = null;
    const duration = 4000; // 4 seconds loop

    function animate(timestamp) {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = (elapsed % duration) / duration;

      const point = pathElem.getPointAtLength(progress * pathLength);
      traveler.setAttribute('cx', point.x);
      traveler.setAttribute('cy', point.y);

      state.animationFrameId = requestAnimationFrame(animate);
    }

    state.animationFrameId = requestAnimationFrame(animate);
  }

  function renderDirectionsList(steps) {
    stepsList.innerHTML = '';
    steps.forEach((step, idx) => {
      const li = document.createElement('li');
      li.className = 'step-item';
      li.innerHTML = `
        <div class="step-icon">${step.icon}</div>
        <div class="step-content">
          <div class="step-text">${step.text}</div>
          ${step.dist > 0 ? `<div class="step-dist">${step.dist} meters</div>` : ''}
        </div>
      `;
      stepsList.appendChild(li);
    });
  }

  // --- 5. NATURAL LANGUAGE "ASK WHERE A HOUSE IS" PARSER ---
  function parseAndAnswerQuery(queryText, isVoice = false) {
    if (!queryText || !queryText.trim()) return;

    if (window.HimagiriAnalytics) {
      window.HimagiriAnalytics.trackSearch(queryText, isVoice);
    }

    const text = queryText.toLowerCase().trim();

    // Check for origin gate
    let detectedStart = state.startNodeId;
    if (text.includes("gate 2") || text.includes("gate2") || text.includes("east gate")) {
      const g2 = Object.keys(nodes).find(n => (n.includes('east') || n.includes('north') || n === 'gate_2') && n !== 'gate_1');
      if (g2) {
        detectedStart = g2;
        startSelect.value = g2;
        state.startNodeId = g2;
      }
    } else if (text.includes("gate 1") || text.includes("gate1") || text.includes("main gate")) {
      const g1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
      if (g1) {
        detectedStart = g1;
        startSelect.value = g1;
        state.startNodeId = g1;
      }
    }

    // Check for Landmarks / Amenities
    const matchedAmenity = amenities.find(a => {
      const aName = a.name.toLowerCase();
      const aId = a.id.toLowerCase();
      return text.includes(aName) ||
        (text.includes('play') && aId.includes('play')) ||
        (text.includes('garden') && aId.includes('garden')) ||
        (text.includes('temple') && (aName.includes('temple') || aId.includes('temple'))) ||
        (text.includes('clubhouse') && aId.includes('clubhouse')) ||
        (text.includes('pool') && aId.includes('pool')) ||
        (text.includes('lake') && aId.includes('lake')) ||
        (text.includes('food') && (aId.includes('food') || aId.includes('cafeteria'))) ||
        (text.includes('auditorium') && aId.includes('auditorium')) ||
        (text.includes('shopping') && aId.includes('shopping')) ||
        (text.includes('bus') && aId.includes('bus')) ||
        (text.includes('wtp') && aId.includes('wtp')) ||
        (text.includes('parking') && aId.includes('parking')) ||
        (text.includes('atm') && aId.includes('atm'));
    });

    if (matchedAmenity && !text.includes("house") && !text.includes("plot") && !text.includes("villa") && !text.includes("block") && !text.includes("tower")) {
      selectAmenity(matchedAmenity.id, true);
      const gateLabel = nodes[detectedStart]?.label ? nodes[detectedStart].label.split(' (')[0] : 'Entrance Gate';
      const resp = `${matchedAmenity.name} is located at ${matchedAmenity.description || matchedAmenity.desc || 'society grounds'}. Route plotted from ${gateLabel}.`;
      displayAssistantResponse(resp);
      speakText(resp);
      return;
    }

    // Match unit using findPlotInLayout
    const matchedPlot = findPlotInLayout(currentLayout, queryText);

    if (matchedPlot) {
      selectPlot(matchedPlot.id, true);
      const startName = (nodes[detectedStart]?.label || 'the main entrance').split(' (')[0];
      const uType = currentLayout.unitType || 'House';
      const resp = `${uType} #${matchedPlot.number} is on ${matchedPlot.road} in ${matchedPlot.block}. I have highlighted its location and plotted your turn-by-turn directions from ${startName}!`;
      displayAssistantResponse(resp);
      speakText(resp);
    } else {
      const uType = currentLayout.unitType || 'House';
      const notFound = `I couldn't find a ${uType.toLowerCase()} matching "${queryText}" in ${currentLayout.name}. Try asking "Where is ${uType} 12?" or choose from the destination dropdown.`;
      displayAssistantResponse(notFound);
      speakText(notFound);
    }
  }

  function displayAssistantResponse(message) {
    assistantText.innerHTML = message;
    assistantResponse.classList.add('active');
  }

  // Text to Speech
  function speakText(text) {
    if (state.voiceMuted || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    // Clean markdown tags for speech
    const cleanText = text.replace(/<[^>]*>?/gm, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  }

  // Web Speech API Voice Recognition
  function initVoiceRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      voiceBtn.title = "Voice recognition not supported on this browser";
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      voiceBtn.classList.add('listening');
      searchInput.placeholder = "Listening... say 'Where is house 142?'";
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      searchInput.value = transcript;
      parseAndAnswerQuery(transcript, true);
    };

    recognition.onerror = () => {
      voiceBtn.classList.remove('listening');
      searchInput.placeholder = "Ask 'Where is House 142?' or enter plot #";
    };

    recognition.onend = () => {
      voiceBtn.classList.remove('listening');
      searchInput.placeholder = "Ask 'Where is House 142?' or enter plot #";
    };

    voiceBtn.addEventListener('click', () => {
      if (voiceBtn.classList.contains('listening')) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  }

  // --- 6. PLOT SELECTION & DETAILS ---
  function selectPlot(plotId, zoomIn = false) {
    const plot = plots[plotId];
    if (!plot) return;

    state.selectedPlotId = plot.id;
    destSelect.value = `plot:${plot.id}`;

    // Highlight plot in SVG
    highlightPlot(plot.id);

    // Calculate Route
    calculateAndDisplayRoute(state.startNodeId, plot.id);

    // Update House Info Card
    const uLabel = currentLayout.unitType || 'House';
    document.getElementById('card-house-num').textContent = `#${plot.number}`;
    document.getElementById('card-road').textContent = plot.road;
    document.getElementById('card-block').textContent = plot.block;
    document.getElementById('card-facing').textContent = `${plot.facing} Facing`;

    // Distances from primary & secondary gates
    const gate1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
    const gate2 = Object.keys(nodes).find(n => (n.includes('east') || n.includes('north') || n === 'gate_2') && n !== gate1);

    const routeG1 = gate1 ? findShortestPath(gate1, plot.roadNode) : null;
    const distG1 = routeG1 ? Math.round(routeG1.totalDist * 0.95) : '--';
    const cardDistG1 = document.getElementById('card-dist-g1');
    if (cardDistG1) {
      cardDistG1.textContent = `${distG1}m`;
      const prev = cardDistG1.previousElementSibling;
      if (prev && nodes[gate1]) prev.textContent = `From ${nodes[gate1].label.split(' (')[0]}`;
    }

    const routeG2 = gate2 ? findShortestPath(gate2, plot.roadNode) : null;
    const distG2 = routeG2 ? Math.round(routeG2.totalDist * 0.95) : '--';
    const cardDistG2 = document.getElementById('card-dist-g2');
    if (cardDistG2) {
      cardDistG2.textContent = `${distG2}m`;
      const prev = cardDistG2.previousElementSibling;
      if (prev && gate2 && nodes[gate2]) prev.textContent = `From ${nodes[gate2].label.split(' (')[0]}`;
    }

    houseCard.classList.add('active');

    // Pan / Zoom smoothly to the plot
    if (zoomIn) {
      zoomToCoordinates(plot.x + plot.w / 2, plot.y + plot.h / 2, 1.8);
    }
  }

  function selectAmenity(amenityId, zoomIn = false) {
    const am = amenities.find(a => a.id === amenityId);
    if (!am) return;

    destSelect.value = `amenity:${am.id}`;

    // Create route to the amenity's road node
    const startNode = nodes[state.startNodeId] ? state.startNodeId : (Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0]);
    const route = findShortestPath(startNode, am.roadNode);
    if (route) {
      state.activeRoute = route;
      const points = [];
      for (const nid of route.nodes) {
        const n = nodes[nid];
        if (n) points.push(`${n.x},${n.y}`);
      }
      points.push(`${am.x},${am.y}`);
      const pathData = "M " + points.join(" L ");

      const sNode = nodes[startNode] || { x: 80, y: 336 };
      routeLayer.innerHTML = `
        <path d="${pathData}" class="nav-route-underlay" />
        <path id="active-nav-path" d="${pathData}" class="nav-route-path" />
        <circle cx="${sNode.x}" cy="${sNode.y}" r="8" fill="#10b981" stroke="#ffffff" stroke-width="2.5" />
        <circle cx="${am.x}" cy="${am.y}" r="12" fill="#ef4444" stroke="#ffffff" stroke-width="2" />
        <circle id="route-traveler" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="2" />
      `;

      startRouteTravelerAnimation();

      const totalDist = Math.round(route.totalDist * 0.95);
      const walkMins = Math.max(1, Math.round(totalDist / 70));
      distanceVal.textContent = `${totalDist} m`;
      walkTimeVal.textContent = `${walkMins} min`;
      driveTimeVal.textContent = `1 min`;

      const steps = generateTurnByTurnDirections(route, null, startNode);
      renderDirectionsList(steps);
    }

    if (zoomIn) {
      zoomToCoordinates(am.x, am.y, 1.8);
    }
  }

  function highlightPlot(plotId) {
    document.querySelectorAll('.svg-plot').forEach(el => el.classList.remove('active-target'));
    const targetEl = document.getElementById(`plot-${plotId}`);
    if (targetEl) {
      targetEl.classList.add('active-target');
      // Bring to top
      targetEl.parentNode.appendChild(targetEl);
    }
  }

  // --- 7. TOOLTIP SYSTEM ---
  function showPlotTooltip(e, p) {
    const gate1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
    const routeG1 = gate1 ? findShortestPath(gate1, p.roadNode) : null;
    const distG1 = routeG1 ? Math.round(routeG1.totalDist * 0.95) : '~180';
    const gateLabel = nodes[gate1]?.label ? nodes[gate1].label.split(' (')[0] : 'Entrance Gate';
    const uLabel = currentLayout.unitType || 'Unit';

    tooltip.innerHTML = `
      <div style="font-weight:800;font-size:13px;color:#38bdf8;margin-bottom:2px;">${uLabel} #${p.number}</div>
      <div style="font-size:11px;color:#cbd5e1;">Road: <strong>${p.road}</strong></div>
      <div style="font-size:11px;color:#cbd5e1;">Sector: ${p.block} (${p.facing}-facing)</div>
      <div style="font-size:10px;color:#10b981;margin-top:4px;">📍 ${distG1}m from ${gateLabel}</div>
    `;
    tooltip.style.display = 'block';
    movePlotTooltip(e);
  }

  function movePlotTooltip(e) {
    const container = document.querySelector('.map-viewport').getBoundingClientRect();
    tooltip.style.left = `${e.clientX - container.left}px`;
    tooltip.style.top = `${e.clientY - container.top}px`;
  }

  function hidePlotTooltip() {
    tooltip.style.display = 'none';
  }

  // --- 8. PAN & ZOOM CONTROLS ---
  function setupPanZoom() {
    const viewportDiv = document.querySelector('.map-viewport');

    // Apply transform matrix to viewport-group
    function updateTransform() {
      viewport.setAttribute(
        'transform',
        `translate(${state.transform.x}, ${state.transform.y}) scale(${state.transform.scale})`
      );
    }

    // Drag to Pan
    viewportDiv.addEventListener('mousedown', (e) => {
      if (e.target.closest('.map-controls') || e.target.closest('.layer-controls')) return;
      state.isDragging = true;
      state.dragStart = { x: e.clientX - state.transform.x, y: e.clientY - state.transform.y };
    });

    window.addEventListener('mousemove', (e) => {
      if (!state.isDragging) return;
      state.transform.x = e.clientX - state.dragStart.x;
      state.transform.y = e.clientY - state.dragStart.y;
      updateTransform();
    });

    window.addEventListener('mouseup', () => {
      state.isDragging = false;
    });

    // Touch Support
    let lastTouchDist = 0;
    viewportDiv.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        state.isDragging = true;
        state.dragStart = { x: e.touches[0].clientX - state.transform.x, y: e.touches[0].clientY - state.transform.y };
      } else if (e.touches.length === 2) {
        lastTouchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    });

    window.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && state.isDragging) {
        state.transform.x = e.touches[0].clientX - state.dragStart.x;
        state.transform.y = e.touches[0].clientY - state.dragStart.y;
        updateTransform();
      } else if (e.touches.length === 2) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        const factor = dist / lastTouchDist;
        zoomByFactor(factor, (e.touches[0].clientX + e.touches[1].clientX) / 2, (e.touches[0].clientY + e.touches[1].clientY) / 2);
        lastTouchDist = dist;
      }
    });

    let lastTapTime = 0;
    let lastTapX = 0;
    let lastTapY = 0;

    viewportDiv.addEventListener('touchend', (e) => {
      state.isDragging = false;
      const now = Date.now();
      if (e.changedTouches.length === 1) {
        const touch = e.changedTouches[0];
        const dist = Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY);
        if (now - lastTapTime < 320 && dist < 35) {
          // Double-tap zoom on mobile!
          e.preventDefault();
          const rect = viewportDiv.getBoundingClientRect();
          const tapX = touch.clientX - rect.left;
          const tapY = touch.clientY - rect.top;
          zoomByFactor(1.5, tapX, tapY);
          if ('vibrate' in navigator) {
            try { navigator.vibrate(20); } catch (err) {}
          }
          lastTapTime = 0;
          return;
        }
        lastTapTime = now;
        lastTapX = touch.clientX;
        lastTapY = touch.clientY;
      }
    });

    // Mouse Wheel Zoom
    viewportDiv.addEventListener('wheel', (e) => {
      e.preventDefault();
      const rect = viewportDiv.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      zoomByFactor(zoomFactor, mouseX, mouseY);
    }, { passive: false });

    function zoomByFactor(factor, clientX, clientY) {
      const newScale = Math.min(5.0, Math.max(0.25, state.transform.scale * factor));
      state.transform.x = clientX - (clientX - state.transform.x) * (newScale / state.transform.scale);
      state.transform.y = clientY - (clientY - state.transform.y) * (newScale / state.transform.scale);
      state.transform.scale = newScale;
      updateTransform();
    }

    // Zoom Buttons
    document.getElementById('zoom-in-btn').addEventListener('click', () => {
      const rect = viewportDiv.getBoundingClientRect();
      zoomByFactor(1.3, rect.width / 2, rect.height / 2);
    });

    document.getElementById('zoom-out-btn').addEventListener('click', () => {
      const rect = viewportDiv.getBoundingClientRect();
      zoomByFactor(0.75, rect.width / 2, rect.height / 2);
    });

    document.getElementById('zoom-fit-btn').addEventListener('click', () => {
      fitMapToView(true);
      showToast("Reset: Entire Layout Overview 🗺️", 2000);
    });

    document.getElementById('focus-gate1-btn').addEventListener('click', () => {
      const isMobile = window.innerWidth <= 900;
      const g1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
      const gn = nodes[g1] || { x: 80, y: 336 };
      zoomToCoordinates(gn.x, gn.y, isMobile ? 2.0 : 1.8);
      showToast(`Focused on ${nodes[g1]?.label || 'Gate 1'} 🚪`, 2000);
    });

    const focusCenterBtn = document.getElementById('focus-center-btn');
    if (focusCenterBtn) {
      focusCenterBtn.addEventListener('click', () => {
        const isMobile = window.innerWidth <= 900;
        const cx = currentLayout.center ? currentLayout.center.x : 320;
        const cy = currentLayout.center ? currentLayout.center.y : 650;
        // Himagiri specific: center directly on Children's play area & central garden / temple
        const targetX = currentLayout.id === 'himagiri' ? 320 : cx;
        const targetY = currentLayout.id === 'himagiri' ? 650 : cy;
        zoomToCoordinates(targetX, targetY, isMobile ? 1.85 : 1.6);
        showToast(`Centered on ${currentLayout.name} central area 🎯`, 3000);
      });
    }

    const geoBtn = document.getElementById('geo-btn');
    if (geoBtn) {
      geoBtn.addEventListener('click', () => {
        if (state.isGeoTracking) {
          stopLocationTracking();
        } else {
          startLocationTracking(true);
        }
      });
    }

    document.getElementById('focus-gate2-btn').addEventListener('click', () => {
      const isMobile = window.innerWidth <= 900;
      const g1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
      const g2 = Object.keys(nodes).find(n => (n.includes('east') || n.includes('north') || n === 'gate_2') && n !== g1);
      const gn = (g2 && nodes[g2]) ? nodes[g2] : { x: 940, y: 336 };
      zoomToCoordinates(gn.x, gn.y, isMobile ? 2.0 : 1.8);
      showToast(`Focused on ${(g2 && nodes[g2]?.label) || 'Gate 2'} 🚪`, 2000);
    });

    // Map tap to set starting point when in location mode
    svg.addEventListener('click', (e) => {
      if (e.target.id === 'map-svg' || e.target.classList.contains('road-corridor') || e.target.classList.contains('road-centerline')) {
        const pt = svg.createSVGPoint();
        pt.x = e.clientX;
        pt.y = e.clientY;
        const svgP = pt.matrixTransform(viewport.getScreenCTM().inverse());
        if (state.startNodeId === 'my_location' || state.isGeoTracking) {
          state.userLocation = { mapX: svgP.x, mapY: svgP.y, accuracy: 10 };
          updateUserLocationMarker(svgP.x, svgP.y, 10);
          showToast("📍 Location pin set to selected spot!", 2500);
          if (state.selectedPlotId) {
            calculateAndDisplayRoute('my_location', state.selectedPlotId);
          }
        }
      }
    });
  }

  let isOverviewMode = false;

  function zoomToCoordinates(mapX, mapY, targetScale = 1.6) {
    const viewportDiv = document.querySelector('.map-viewport');
    const rect = viewportDiv.getBoundingClientRect();
    const isMobile = window.innerWidth <= 900;

    // On mobile / Android, ensure target plot is large and clearly visible
    const finalScale = isMobile ? Math.max(targetScale, 1.9) : targetScale;

    state.transform.scale = finalScale;
    state.transform.x = rect.width / 2 - mapX * finalScale;
    state.transform.y = rect.height / 2 - mapY * finalScale;

    viewport.setAttribute(
      'transform',
      `translate(${state.transform.x}, ${state.transform.y}) scale(${state.transform.scale})`
    );
  }

  function fitMapToView(forceFullFit = false) {
    const viewportDiv = document.querySelector('.map-viewport');
    if (!viewportDiv) return;
    const rect = viewportDiv.getBoundingClientRect();
    if (!rect.width || !rect.height) return;

    const isMobile = window.innerWidth <= 900;

    // Full layout bounds from currentLayout
    const b = currentLayout && currentLayout.bounds ? currentLayout.bounds : { minX: 20, maxX: 1270, minY: 135, maxY: 935 };
    const contentMinX = b.minX;
    const contentMaxX = b.maxX;
    const contentWidth = contentMaxX - contentMinX;
    const centerX = currentLayout && currentLayout.center ? currentLayout.center.x : (contentMinX + contentMaxX) / 2;

    const contentMinY = b.minY;
    const contentMaxY = b.maxY;
    const contentHeight = contentMaxY - contentMinY;
    const centerY = currentLayout && currentLayout.center ? currentLayout.center.y : (contentMinY + contentMaxY) / 2;

    // Comfortable padding inside the viewport
    const padX = isMobile ? 10 : 28;
    const padY = isMobile ? 10 : 20;

    const availWidth = Math.max(rect.width - padX * 2, 80);
    const availHeight = Math.max(rect.height - padY * 2, 80);

    const fitScale = Math.min(availWidth / contentWidth, availHeight / contentHeight);

    state.transform.scale = isMobile ? fitScale * 0.98 : fitScale;
    state.transform.x = rect.width / 2 - centerX * state.transform.scale;
    state.transform.y = rect.height / 2 - centerY * state.transform.scale;

    viewport.setAttribute(
      'transform',
      `translate(${state.transform.x}, ${state.transform.y}) scale(${state.transform.scale})`
    );
  }

  // --- 9. EVENT LISTENERS & SEARCH ---
  function setupEventListeners() {
    // Search input & button
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        parseAndAnswerQuery(searchInput.value);
        if (window.innerWidth <= 900) {
          searchInput.blur();
        }
      }
    });

    const searchEnterBtn = document.getElementById('search-enter-btn');
    if (searchEnterBtn) {
      searchEnterBtn.addEventListener('click', () => {
        parseAndAnswerQuery(searchInput.value);
        if (window.innerWidth <= 900) {
          searchInput.blur();
        }
      });
    }

    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        parseAndAnswerQuery(searchInput.value);
        if (window.innerWidth <= 900) {
          searchInput.blur();
        }
      });
    }

    const searchClearBtn = document.getElementById('search-clear-btn');
    if (searchClearBtn) {
      searchClearBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchClearBtn.style.display = 'none';
        searchInput.focus();
      });
    }

    searchInput.addEventListener('input', () => {
      if (searchClearBtn) {
        searchClearBtn.style.display = searchInput.value.trim() ? 'flex' : 'none';
      }
    });

    // View Mode Toggle (Full Map vs Split View) - Works on both PC and Mobile!
    const mobileViewToggle = document.getElementById('mobile-view-toggle');
    const headerMapToggleBtn = document.getElementById('header-map-toggle-btn');
    const appContainer = document.querySelector('.app-container');

    function toggleFullMapView() {
      if (!appContainer) return;
      const isFull = appContainer.classList.toggle('full-map');
      const isMobile = window.innerWidth <= 900;

      const toggleText = isFull 
        ? (isMobile ? '<span>↕ Split View</span>' : '<span>⇤ Split View</span>')
        : (isMobile ? '<span>↕ Expand Map</span>' : '<span>⇥ Full Map</span>');

      if (mobileViewToggle) mobileViewToggle.innerHTML = toggleText;
      if (headerMapToggleBtn) headerMapToggleBtn.innerHTML = isFull ? '<span>⇤</span> Split View' : '<span>⇥</span> Full Map';

      showToast(isFull ? "Full Screen Map Active 🗺️" : "Split View Active 🧭", 2000);
      setTimeout(() => {
        fitMapToView(false);
      }, 320);
    }

    if (mobileViewToggle) mobileViewToggle.addEventListener('click', toggleFullMapView);
    if (headerMapToggleBtn) headerMapToggleBtn.addEventListener('click', toggleFullMapView);

    // Prompt chips click
    document.querySelectorAll('.prompt-chips .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const q = chip.getAttribute('data-query');
        searchInput.value = q;
        parseAndAnswerQuery(q);
        if (window.innerWidth <= 900) {
          searchInput.blur();
        }
      });
    });

    // Speak button
    speakBtn.addEventListener('click', () => {
      speakText(assistantText.textContent);
    });

    // Close house card
    document.getElementById('close-house-card').addEventListener('click', () => {
      houseCard.classList.remove('active');
    });

    // Sector Filter Pills
    document.querySelectorAll('.sector-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.sector-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const filter = pill.getAttribute('data-sector');
        applySectorFilter(filter);
      });
    });

    // Layer toggles
    document.getElementById('toggle-numbers').addEventListener('change', (e) => {
      document.querySelectorAll('.plot-label').forEach(el => {
        el.style.display = e.target.checked ? 'block' : 'none';
      });
    });

    const toggleBigText = document.getElementById('toggle-big-text');
    if (toggleBigText) {
      toggleBigText.addEventListener('change', (e) => {
        document.body.classList.toggle('big-labels', e.target.checked);
      });
    }

    document.getElementById('toggle-amenities').addEventListener('change', (e) => {
      amenitiesLayer.style.display = e.target.checked ? 'block' : 'none';
    });

    document.getElementById('toggle-roads').addEventListener('change', (e) => {
      const roadLabels = document.getElementById('road-name-labels');
      if (roadLabels) roadLabels.style.display = e.target.checked ? 'block' : 'none';
    });

    // Share Route / Copy Link
    document.getElementById('share-link-btn').addEventListener('click', () => {
      if (!state.selectedPlotId) {
        alert("Please select a house first to generate a shareable delivery link!");
        return;
      }
      const url = new URL(window.location.href);
      url.searchParams.set('house', plots[state.selectedPlotId].number);
      url.searchParams.set('gate', state.startNodeId === 'gate_2' ? '2' : '1');
      navigator.clipboard.writeText(url.toString()).then(() => {
        const btn = document.getElementById('share-link-btn');
        const origText = btn.innerHTML;
        btn.innerHTML = `✓ Copied!`;
        setTimeout(() => { btn.innerHTML = origText; }, 2500);
      });
      if (window.HimagiriAnalytics) {
        window.HimagiriAnalytics.trackShare(plots[state.selectedPlotId].number, 'link');
      }
    });

    // Native Android Web Share API (WhatsApp / Maps / Messages)
    const nativeShareBtn = document.getElementById('share-native-btn');
    if (nativeShareBtn) {
      nativeShareBtn.addEventListener('click', async () => {
        if (!state.selectedPlotId) {
          alert("Please select a house first to share directions!");
          return;
        }
        const plot = plots[state.selectedPlotId];
        const gateLabel = state.startNodeId === 'gate_2' ? 'Gate 2' : 'Gate 1';
        const url = new URL(window.location.href);
        url.searchParams.set('house', plot.number);
        url.searchParams.set('gate', state.startNodeId === 'gate_2' ? '2' : '1');

        const shareTitle = `Directions to House #${plot.number} - Himagiri Meadows`;
        const shareText = `Here are the directions to House #${plot.number} (${plot.road}) from ${gateLabel} in Himagiri Meadows Layout:\n${url.toString()}`;

        if (window.HimagiriAnalytics) {
          window.HimagiriAnalytics.trackShare(plot.number, 'whatsapp_native');
        }

        if (navigator.share) {
          try {
            await navigator.share({
              title: shareTitle,
              text: shareText,
              url: url.toString()
            });
          } catch (err) {
            // Fallback or user canceled
            if (err.name !== 'AbortError') {
              window.open(`https://wa.me/?text=${encodeURIComponent(shareText)}`, '_blank');
            }
          }
        } else {
          // Fallback to WhatsApp Web/App
          window.open(`https://wa.me/?text=${encodeURIComponent(shareText)}`, '_blank');
        }
      });
    }

    // Analytics Dashboard Modal & Stats Populator
    const analyticsModal = document.getElementById('analytics-modal');
    const analyticsBtn = document.getElementById('analytics-btn');
    const closeAnalyticsModal = document.getElementById('close-analytics-modal');

    function updateAnalyticsUI() {
      if (!window.HimagiriAnalytics) return;
      const stats = window.HimagiriAnalytics.getStats();

      const visitsElem = document.getElementById('stat-total-visits');
      if (visitsElem) visitsElem.textContent = stats.totalVisits || 1;

      const androidCount = stats.deviceStats?.android || 0;
      const iosCount = stats.deviceStats?.ios || 0;
      const desktopCount = stats.deviceStats?.desktop || 0;
      const totalDevices = androidCount + iosCount + desktopCount || 1;
      const mobilePct = Math.round(((androidCount + iosCount) / totalDevices) * 100);

      const mobilePctElem = document.getElementById('stat-mobile-pct');
      if (mobilePctElem) mobilePctElem.textContent = `${mobilePct}%`;

      const totalSearches = Object.values(stats.searches || {}).reduce((a, b) => a + b, 0);
      const searchesElem = document.getElementById('stat-total-searches');
      if (searchesElem) searchesElem.textContent = totalSearches;

      const sharesElem = document.getElementById('stat-total-shares');
      if (sharesElem) sharesElem.textContent = stats.shares || 0;

      const androidElem = document.getElementById('stat-android');
      if (androidElem) androidElem.textContent = `Android: ${androidCount}`;
      const iosElem = document.getElementById('stat-ios');
      if (iosElem) iosElem.textContent = `iOS/iPhone: ${iosCount}`;
      const desktopElem = document.getElementById('stat-desktop');
      if (desktopElem) desktopElem.textContent = `Desktop: ${desktopCount}`;

      // Render Top Searches list
      const topList = document.getElementById('top-searches-list');
      if (topList && stats.searches) {
        const searchEntries = Object.entries(stats.searches).sort((a, b) => b[1] - a[1]).slice(0, 5);
        if (searchEntries.length > 0) {
          topList.innerHTML = '';
          searchEntries.forEach(([query, count], idx) => {
            const item = document.createElement('div');
            item.style.display = 'flex';
            item.style.justifyContent = 'space-between';
            item.style.alignItems = 'center';
            item.style.padding = '4px 0';
            item.style.borderBottom = '1px solid #f1f5f9';
            item.innerHTML = `
              <span><strong>#${idx + 1}</strong> ${query}</span>
              <span style="background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:10px;font-weight:700;font-size:11px;">${count} searches</span>
            `;
            topList.appendChild(item);
          });
        }
      }
    }

    if (analyticsBtn && analyticsModal) {
      analyticsBtn.addEventListener('click', () => {
        updateAnalyticsUI();
        analyticsModal.classList.add('active');
      });
    }

    if (closeAnalyticsModal && analyticsModal) {
      closeAnalyticsModal.addEventListener('click', () => {
        analyticsModal.classList.remove('active');
      });
      analyticsModal.addEventListener('click', (e) => {
        if (e.target === analyticsModal) analyticsModal.classList.remove('active');
      });
    }

    // Android Connect Modal & QR Code Generation
    const androidModal = document.getElementById('android-modal');
    const androidConnectBtn = document.getElementById('android-connect-btn');
    const closeAndroidModal = document.getElementById('close-android-modal');
    const qrcodeBox = document.getElementById('qrcode-box');
    const androidUrlText = document.getElementById('android-url-text');
    const copyAndroidUrlBtn = document.getElementById('copy-android-url-btn');

    // Detect server host IP or production domain
    const currentHost = window.location.hostname;
    const isLocalhost = currentHost === 'localhost' || currentHost === '127.0.0.1' || currentHost.startsWith('192.168.');
    const liveDomain = (!isLocalhost && currentHost) ? window.location.origin : 'https://hmmaps.in';
    const androidIpUrl = isLocalhost ? (window.location.protocol.startsWith('http') ? window.location.origin : 'http://192.168.68.103:8080') : liveDomain;

    if (androidUrlText) {
      androidUrlText.textContent = isLocalhost ? 'https://hmmaps.in (or ' + androidIpUrl + ')' : liveDomain;
    }

    if (androidConnectBtn && androidModal) {
      androidConnectBtn.addEventListener('click', () => {
        androidModal.classList.add('active');
        if (qrcodeBox && window.QRCode) {
          qrcodeBox.innerHTML = '';
          new QRCode(qrcodeBox, {
            text: androidIpUrl,
            width: 200,
            height: 200,
            colorDark: "#0f172a",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.M
          });
        }
      });
    }

    if (closeAndroidModal) {
      closeAndroidModal.addEventListener('click', () => {
        androidModal.classList.remove('active');
      });
    }

    if (copyAndroidUrlBtn) {
      copyAndroidUrlBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(androidIpUrl).then(() => {
          copyAndroidUrlBtn.textContent = '✓ Copied!';
          setTimeout(() => { copyAndroidUrlBtn.textContent = 'Copy'; }, 2000);
        });
      });
    }

    if (androidModal) {
      androidModal.addEventListener('click', (e) => {
        if (e.target === androidModal) androidModal.classList.remove('active');
      });
    }

    // View Original Map Modal
    document.getElementById('view-original-btn').addEventListener('click', () => {
      originalModal.classList.add('active');
    });

    document.getElementById('close-modal-btn').addEventListener('click', () => {
      originalModal.classList.remove('active');
    });

    originalModal.addEventListener('click', (e) => {
      if (e.target === originalModal) originalModal.classList.remove('active');
    });

    // Mobile drawer toggle & backdrop
    const mobileBtn = document.getElementById('mobile-drawer-toggle');
    const sidebar = document.querySelector('.sidebar');
    let backdrop = document.querySelector('.sidebar-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'sidebar-backdrop';
      document.body.appendChild(backdrop);
    }

    if (mobileBtn && sidebar) {
      mobileBtn.addEventListener('click', () => {
        const isOpen = sidebar.classList.toggle('open');
        backdrop.classList.toggle('active', isOpen);
      });
      backdrop.addEventListener('click', () => {
        sidebar.classList.remove('open');
        backdrop.classList.remove('active');
      });
    }

    // Register Service Worker for Android PWA with instant update reload
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js?v=8').then((reg) => {
          reg.update(); // Force immediate update check
        }).catch(err => {
          console.log('SW registration error:', err);
        });
      });
      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (!refreshing) {
          refreshing = true;
          window.location.reload();
        }
      });
    }

    // Auto-fit on screen orientation change or resize
    window.addEventListener('resize', () => {
      if (!state.selectedPlotId && !state.activeRoute) {
        fitMapToView();
      }
    });

    // Voice recognition
    initVoiceRecognition();

    // Portal & Map View Navigation
    const headerBackBtn = document.getElementById('header-back-btn');
    if (headerBackBtn) {
      headerBackBtn.addEventListener('click', showPortalView);
    }

    const headerBrand = document.getElementById('header-brand');
    if (headerBrand) {
      headerBrand.addEventListener('click', () => {
        const portal = document.getElementById('portal-view');
        if (portal && portal.style.display !== 'none') {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          showPortalView();
        }
      });
    }

    // AI Assistant Toggle Buttons
    const headerAiBtn = document.getElementById('header-ai-guide-btn');
    if (headerAiBtn) {
      headerAiBtn.addEventListener('click', () => aiAssistant.open());
    }

    const floatingAiBtn = document.getElementById('floating-ai-btn');
    if (floatingAiBtn) {
      floatingAiBtn.addEventListener('click', () => aiAssistant.open());
    }

    // Portal Directory Live Search & Zone Filter Listeners
    const dirSearchInput = document.getElementById('directory-search-input');
    const dirClearBtn = document.getElementById('directory-clear-search');
    if (dirSearchInput) {
      dirSearchInput.addEventListener('input', (e) => {
        currentDirectorySearch = e.target.value;
        if (dirClearBtn) dirClearBtn.style.display = currentDirectorySearch ? 'flex' : 'none';
        renderPortalDirectory(currentDirectoryZone, currentDirectorySearch);
      });
    }
    if (dirClearBtn) {
      dirClearBtn.addEventListener('click', () => {
        if (dirSearchInput) {
          dirSearchInput.value = '';
          dirSearchInput.focus();
        }
        dirClearBtn.style.display = 'none';
        currentDirectorySearch = '';
        renderPortalDirectory(currentDirectoryZone, '');
      });
    }

    const zoneTabs = document.querySelectorAll('.zone-tab');
    zoneTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        zoneTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentDirectoryZone = tab.getAttribute('data-zone') || 'all';
        renderPortalDirectory(currentDirectoryZone, currentDirectorySearch);
      });
    });

    // Render portal directory with all 50+ layouts
    renderPortalDirectory(currentDirectoryZone, currentDirectorySearch);

    // Dropdown change listeners
    startSelect.addEventListener('change', () => {
      state.startNodeId = startSelect.value;
      if (state.startNodeId === 'my_location') {
        if (!state.userLocation) {
          startLocationTracking(true);
        }
      }
      if (state.selectedPlotId) {
        calculateAndDisplayRoute(state.startNodeId, state.selectedPlotId);
      }
    });

    const useMyLocBtn = document.getElementById('use-my-loc-btn');
    if (useMyLocBtn) {
      useMyLocBtn.addEventListener('click', () => {
        startSelect.value = 'my_location';
        state.startNodeId = 'my_location';
        startLocationTracking(true);
        if (state.selectedPlotId) {
          calculateAndDisplayRoute('my_location', state.selectedPlotId);
        }
      });
    }

    destSelect.addEventListener('change', () => {
      const val = destSelect.value;
      if (!val) return;
      if (val.startsWith('plot:')) {
        const pid = val.replace('plot:', '');
        selectPlot(pid, true);
      } else if (val.startsWith('amenity:')) {
        const aid = val.replace('amenity:', '');
        selectAmenity(aid, true);
      }
    });

    // Guided Tutorial walkthrough buttons
    const tutCloseBtn = document.getElementById('tutorial-close-btn');
    if (tutCloseBtn) tutCloseBtn.addEventListener('click', closeTutorial);

    const tutNextBtn = document.getElementById('tutorial-next-btn');
    if (tutNextBtn) {
      tutNextBtn.addEventListener('click', () => {
        const steps = getTutorialSteps(activeTutorialLayout, activeTutorialUnit);
        if (tutorialCurrentStep < steps.length - 1) {
          tutorialCurrentStep++;
          renderTutorialStep();
        }
      });
    }

    const tutPrevBtn = document.getElementById('tutorial-prev-btn');
    if (tutPrevBtn) {
      tutPrevBtn.addEventListener('click', () => {
        if (tutorialCurrentStep > 0) {
          tutorialCurrentStep--;
          renderTutorialStep();
        }
      });
    }

    const tutFinishBtn = document.getElementById('tutorial-finish-btn');
    if (tutFinishBtn) {
      tutFinishBtn.addEventListener('click', () => {
        closeTutorial();
        showToast(`Ready! Enjoy exploring ${currentLayout.name} 🚀`, 3000);
      });
    }

    // Portal Prompt Chips
    document.querySelectorAll('.portal-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const q = chip.getAttribute('data-query');
        aiAssistant.open(q);
      });
    });

    // Portal AI Search Input
    const portalAiSubmit = document.getElementById('portal-ai-submit-btn');
    const portalAiInput = document.getElementById('portal-ai-input');
    if (portalAiSubmit && portalAiInput) {
      const runPortalAi = () => {
        const q = portalAiInput.value.trim();
        aiAssistant.open(q || "Where do I go?");
      };
      portalAiSubmit.addEventListener('click', runPortalAi);
      portalAiInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') runPortalAi();
      });
    }

    const portalVoice = document.getElementById('portal-ai-voice-btn');
    if (portalVoice) {
      portalVoice.addEventListener('click', () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          const rec = new SpeechRecognition();
          rec.lang = 'en-IN';
          rec.start();
          showToast("Listening to voice... 🎙️", 2500);
          rec.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            if (portalAiInput) portalAiInput.value = transcript;
            aiAssistant.open(transcript);
          };
        } else {
          showToast("Speech recognition not supported in this browser", 2500);
        }
      });
    }

    // AI Drawer close & clear
    document.querySelectorAll('#ai-close-btn, #ai-drawer-backdrop').forEach(el => {
      el.addEventListener('click', () => aiAssistant.close());
    });

    const aiClearBtn = document.getElementById('ai-clear-btn');
    if (aiClearBtn) {
      aiClearBtn.addEventListener('click', () => aiAssistant.reset());
    }

    // AI Drawer input send
    const aiDrawerSend = document.getElementById('ai-drawer-send-btn');
    const aiDrawerInput = document.getElementById('ai-drawer-input');
    if (aiDrawerSend && aiDrawerInput) {
      const sendFromDrawer = () => {
        const val = aiDrawerInput.value.trim();
        if (val) {
          aiDrawerInput.value = '';
          aiAssistant.handleUserQuery(val);
        }
      };
      aiDrawerSend.addEventListener('click', sendFromDrawer);
      aiDrawerInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendFromDrawer();
      });
    }

    // AI Drawer voice recognition
    const aiDrawerVoice = document.getElementById('ai-drawer-voice-btn');
    if (aiDrawerVoice && aiDrawerInput) {
      aiDrawerVoice.addEventListener('click', () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          const rec = new SpeechRecognition();
          rec.lang = 'en-IN';
          rec.start();
          showToast("Listening to voice... 🎙️", 2500);
          rec.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            aiDrawerInput.value = transcript;
            aiAssistant.handleUserQuery(transcript);
          };
        } else {
          showToast("Speech recognition not supported in this browser", 2500);
        }
      });
    }

    // Sample preview buttons
    document.querySelectorAll('.btn-preview-sample, .btn-demo-card').forEach(btn => {
      btn.addEventListener('click', () => {
        const name = btn.getAttribute('data-name') || 'This layout';
        showToast(`${name} is a sample preview. Try Himagiri Meadows for full live navigation! 🗺️`, 3500);
      });
    });

    const onboardBtn = document.getElementById('btn-onboard-society');
    if (onboardBtn) {
      onboardBtn.addEventListener('click', () => {
        showToast("Layout onboarding: Email your layout photo or blueprint to support@hmmaps.in 🚀", 4000);
      });
    }
  }

  function applySectorFilter(sector) {
    state.activeFilter = sector;
    if (sector === 'ALL') {
      document.querySelectorAll('.svg-plot').forEach(p => p.style.opacity = '1');
      fitMapToView();
      return;
    }

    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    let found = false;

    document.querySelectorAll('.svg-plot').forEach(el => {
      const pid = el.getAttribute('data-id');
      const plot = plots[pid];
      if (plot && plot.road.toLowerCase().includes(sector.toLowerCase())) {
        el.style.opacity = '1';
        minX = Math.min(minX, plot.x);
        minY = Math.min(minY, plot.y);
        maxX = Math.max(maxX, plot.x + plot.w);
        maxY = Math.max(maxY, plot.y + plot.h);
        found = true;
      } else {
        el.style.opacity = '0.2';
      }
    });

    if (found) {
      zoomToCoordinates((minX + maxX) / 2, (minY + maxY) / 2, 1.6);
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  let currentDirectoryZone = 'all';
  let currentDirectorySearch = '';

  function renderPortalDirectory(filterZone = 'all', searchQuery = '') {
    currentDirectoryZone = filterZone;
    currentDirectorySearch = searchQuery;
    const grid = document.getElementById('communities-grid');
    if (!grid) return;

    const q = searchQuery.toLowerCase().trim();
    const layoutList = Object.values(layouts);

    // Compute zone counts across all layouts
    const counts = { all: layoutList.length, south: 0, whitefield: 0, ecity: 0, north: 0, west: 0 };
    layoutList.forEach(lay => {
      const z = lay.zone;
      if (z === 'south') counts.south++;
      else if (z === 'whitefield' || z === 'east') counts.whitefield++;
      else if (z === 'ecity' || z === 'southeast') counts.ecity++;
      else if (z === 'north') counts.north++;
      else if (z === 'west' || z === 'central') counts.west++;
    });

    // Update tab count badges if elements exist
    Object.keys(counts).forEach(k => {
      const el = document.getElementById(`count-${k}`);
      if (el) el.textContent = counts[k];
    });

    // Filter layouts according to active zone & search query
    const filtered = layoutList.filter(lay => {
      // Zone filter
      if (filterZone !== 'all') {
        if (filterZone === 'south' && lay.zone !== 'south') return false;
        if (filterZone === 'whitefield' && lay.zone !== 'whitefield' && lay.zone !== 'east') return false;
        if (filterZone === 'ecity' && lay.zone !== 'ecity' && lay.zone !== 'southeast') return false;
        if (filterZone === 'north' && lay.zone !== 'north') return false;
        if (filterZone === 'west' && lay.zone !== 'west' && lay.zone !== 'central') return false;
      }

      // Search query filter
      if (q) {
        const matchesName = lay.name.toLowerCase().includes(q);
        const matchesLoc = lay.location.toLowerCase().includes(q);
        const matchesType = (lay.type || '').toLowerCase().includes(q);
        const matchesZone = (lay.zone || '').toLowerCase().includes(q);
        if (!matchesName && !matchesLoc && !matchesType && !matchesZone) return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div class="directory-no-results" style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; color: #94a3b8;">
          <div style="font-size: 38px; margin-bottom: 12px;">🔍</div>
          <h3 style="color: #f1f5f9; font-size: 18px; margin-bottom: 8px;">No matching layouts found</h3>
          <p style="font-size: 13.5px;">Try searching for another locality like "Whitefield", "Sarjapur", "Hebbal", "HSR", or "South".</p>
          <button id="reset-directory-search-btn" class="btn btn-secondary" style="margin-top: 16px;">View All 50+ Layouts</button>
        </div>
      `;
      const resetBtn = document.getElementById('reset-directory-search-btn');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          const sInput = document.getElementById('directory-search-input');
          if (sInput) sInput.value = '';
          const clearBtn = document.getElementById('directory-clear-search');
          if (clearBtn) clearBtn.style.display = 'none';
          document.querySelectorAll('.zone-tab').forEach(t => t.classList.toggle('active', t.getAttribute('data-zone') === 'all'));
          renderPortalDirectory('all', '');
        });
      }
      return;
    }

    let cardsHtml = '';
    filtered.forEach(lay => {
      const uCount = Object.keys(lay.plots).length;
      const uType = lay.unitType || 'Unit';
      const amenCount = lay.amenities ? lay.amenities.length : 0;
      const roadCount = lay.roads && lay.roads.nodes ? Object.keys(lay.roads.nodes).length : 0;

      // Icon selector
      let icon = '🏡';
      const nameL = lay.name.toLowerCase();
      const typeL = (lay.type || '').toLowerCase();
      if (typeL.includes('villa') || nameL.includes('meadow') || nameL.includes('orchard') || nameL.includes('palm') || nameL.includes('valley')) icon = '🌳';
      if (typeL.includes('tech') || typeL.includes('corporate') || nameL.includes('tech') || nameL.includes('tower') || nameL.includes('gateway')) icon = '🏢';
      if (typeL.includes('golf') || nameL.includes('golf')) icon = '⛳';
      if (nameL.includes('lake') || nameL.includes('habita')) icon = '🌊';
      if (typeL.includes('apartment') || typeL.includes('high-rise')) icon = '🏙️';

      // Badge
      let badge = '🟢 Live Verified Layout';
      if (typeL.includes('township') || nameL.includes('city')) badge = '🟢 Live Verified Township';
      if (typeL.includes('campus') || nameL.includes('park')) badge = '🟢 Live Verified Campus';

      // Description
      let desc = '';
      if (lay.id === 'himagiri') {
        desc = "Premium 344-plot gated community with 8 tree-lined avenues, dual security gates, West & Central temples, children's park, and auditorium.";
      } else if (lay.id === 'greenwood') {
        desc = "Gated luxury villa community with 60 bespoke villas, Orchard Boulevard, Pine Court, Palm Drive, Grand Clubhouse, swimming pool, and lake promenade.";
      } else if (lay.id === 'tech_horizon') {
        desc = "Premier corporate IT campus featuring Towers A to D, 36 tech enterprise blocks, Central Innovation Boulevard, food plaza, and smart MLCP parking.";
      } else {
        desc = `${lay.type || 'Verified residential layout'} featuring ${uCount} ${uType.toLowerCase()}s, ${amenCount} community amenities, and verified turn-by-turn routing.`;
      }

      cardsHtml += `
        <div class="community-card active-card" data-layout-id="${lay.id}">
          <div class="card-badge live-badge">${badge}</div>
          <div class="card-header">
            <div class="community-avatar">${icon}</div>
            <div>
              <h3 class="community-name">${escapeHtml(lay.name)}</h3>
              <p class="community-loc">${escapeHtml(lay.location)}</p>
            </div>
          </div>
          <p class="community-desc">${escapeHtml(desc)}</p>
          <div class="community-tags">
            <span class="tag">📍 ${uCount} ${uType}s</span>
            <span class="tag">🛣️ ${roadCount} Nodes</span>
            <span class="tag">🛕 ${amenCount} Amenities</span>
            <span class="tag">📡 Live GPS</span>
          </div>
          <div class="community-actions">
            <button class="btn btn-primary btn-open-card-map" data-layout-id="${lay.id}" style="flex: 1.3;">
              🗺️ Explore Map
            </button>
            <button class="btn btn-secondary btn-ask-card-ai" data-layout-id="${lay.id}" style="flex: 1;">
              ✨ Ask AI Guide
            </button>
          </div>
        </div>
      `;
    });

    // Append Onboard Society Card at the end
    cardsHtml += `
      <div class="community-card onboard-card" id="card-onboard-society">
        <div class="card-badge free-badge">Free Onboarding</div>
        <div class="card-header">
          <div class="community-avatar">📐</div>
          <div>
            <h3 class="community-name">Onboard Your Community</h3>
            <p class="community-loc">Residential Societies • Campuses</p>
          </div>
        </div>
        <p class="community-desc">
          Have a physical layout board or blueprint photo? Turn it into a smart, GPS-enabled digital map with turn-by-turn AI wayfinding for your residents and delivery visitors.
        </p>
        <div class="community-tags">
          <span class="tag">⚡ 24hr Digitization</span>
          <span class="tag">🧭 AI Navigator</span>
          <span class="tag">📱 Instant PWA</span>
        </div>
        <div class="community-actions">
          <button id="btn-onboard-society" class="btn btn-primary" style="width: 100%;">
            🚀 Submit Layout Blueprint
          </button>
        </div>
      </div>
    `;

    grid.innerHTML = cardsHtml;

    // Attach event listeners to card buttons
    grid.querySelectorAll('.btn-open-card-map').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const lid = btn.getAttribute('data-layout-id');
        loadLayout(lid);
      });
    });

    grid.querySelectorAll('.btn-ask-card-ai').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const lid = btn.getAttribute('data-layout-id');
        aiAssistant.openForLayout(lid);
      });
    });

    // Make whole card clickable (except buttons)
    grid.querySelectorAll('.community-card.active-card').forEach(card => {
      card.addEventListener('click', (e) => {
        if (e.target.closest('button')) return;
        const lid = card.getAttribute('data-layout-id');
        if (lid) loadLayout(lid);
      });
    });

    const onboardBtn = document.getElementById('btn-onboard-society');
    if (onboardBtn) {
      onboardBtn.addEventListener('click', () => {
        const modal = document.getElementById('onboard-modal');
        if (modal) modal.style.display = 'flex';
      });
    }
  }

  function showPortalView() {
    const portal = document.getElementById('portal-view');
    const mapApp = document.getElementById('app-container');
    const backBtn = document.getElementById('header-back-btn');
    const headerBadges = document.getElementById('header-badges');
    const headerMapControls = document.getElementById('header-map-controls');
    const brandTitle = document.getElementById('brand-title');
    const brandSub = document.getElementById('brand-subtitle');
    const brandIcon = document.getElementById('brand-icon');

    if (portal) portal.style.display = 'block';
    if (mapApp) mapApp.style.display = 'none';
    if (backBtn) backBtn.style.display = 'none';
    if (headerBadges) headerBadges.style.display = 'none';
    if (headerMapControls) headerMapControls.style.display = 'none';
    if (brandTitle) brandTitle.textContent = 'HM Maps';
    if (brandSub) brandSub.textContent = 'Smart Layout & Community Wayfinding';
    if (brandIcon) brandIcon.textContent = '🌐';

    renderPortalDirectory(currentDirectoryZone, currentDirectorySearch);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showMapView(communityId = 'himagiri', targetPlot = null) {
    if (communityId && currentLayoutId !== communityId && layouts[communityId]) {
      loadLayout(communityId, targetPlot);
      return;
    }

    const portal = document.getElementById('portal-view');
    const mapApp = document.getElementById('app-container');
    const backBtn = document.getElementById('header-back-btn');
    const headerBadges = document.getElementById('header-badges');
    const headerMapControls = document.getElementById('header-map-controls');

    if (portal) portal.style.display = 'none';
    if (mapApp) mapApp.style.display = 'flex';
    if (backBtn) backBtn.style.display = 'flex';
    if (headerBadges) headerBadges.style.display = (window.innerWidth > 900) ? 'flex' : 'none';
    if (headerMapControls) headerMapControls.style.display = 'flex';

    updateHeaderForLayout(currentLayout);

    setTimeout(() => {
      fitMapToView(true);
      if (targetPlot) {
        selectPlot(targetPlot, true);
        calculateAndDisplayRoute(state.startNodeId || Object.keys(nodes)[0], targetPlot);
      }
    }, 120);
  }

  // --- AI SPATIAL ASSISTANT MODULE ---
  const aiAssistant = {
    state: 'IDLE', // 'IDLE', 'SELECTING_LAYOUT', 'ASKING_SPECIFIC_PLACE', 'ASKING_HOUSE_NUMBER', 'EXPLORING'
    chosenLayoutId: 'himagiri',
    isOpen: false,

    open(initialQuery = null) {
      const drawer = document.getElementById('ai-chat-drawer');
      if (!drawer) return;
      drawer.style.display = 'flex';
      void drawer.offsetWidth;
      drawer.classList.add('open');
      this.isOpen = true;

      const messagesContainer = document.getElementById('ai-chat-messages');
      if (messagesContainer && messagesContainer.children.length === 0) {
        this.addAiMessage({
          text: "Hello! I am your <strong>HM Maps AI Navigator</strong> 🧭.<br>I know 50+ real residential layouts, villas, plots, corporate blocks, and avenues across Bangalore.<br><br>Where would you like to go today?",
          chips: [
            { text: "🧭 Where do I go?", query: "Where do I go?" },
            { text: "🌳 Whitefield & East", query: "Layouts in Whitefield" },
            { text: "🏡 South Bangalore", query: "Layouts in South Bangalore" },
            { text: "🏢 Electronic City & ORR", query: "Layouts in Electronic City" },
            { text: "✈️ North Bangalore", query: "Layouts in North Bangalore" },
            { text: "🏛️ Central & West", query: "Layouts in Central Bangalore" },
            { text: "📡 Live GPS Tracking", query: "Track live location" }
          ]
        });
      }

      if (initialQuery) {
        this.handleUserQuery(initialQuery);
      } else {
        const input = document.getElementById('ai-drawer-input');
        if (input) input.focus();
      }
    },

    openForLayout(layoutId) {
      if (!layouts[layoutId]) layoutId = 'himagiri';
      this.chosenLayoutId = layoutId;
      const targetLayout = layouts[layoutId];
      this.open();

      this.state = 'ASKING_SPECIFIC_PLACE';
      const uLabel = targetLayout.unitType ? targetLayout.unitType.toLowerCase() : 'house';

      const plotKeys = Object.keys(targetLayout.plots);
      const samplePlots = plotKeys.slice(0, 3).map(k => targetLayout.plots[k]);
      const sampleAmenity = targetLayout.amenities && targetLayout.amenities.length > 0 ? targetLayout.amenities[0] : null;

      let chips = [
        { text: `✅ Yes, a specific ${uLabel}`, query: "Yes" },
        { text: `🌿 No, explore full layout`, query: "No" }
      ];

      samplePlots.forEach(p => {
        chips.push({ text: `${targetLayout.unitType || 'Unit'} #${p.number}`, query: `${targetLayout.unitType || 'Unit'} ${p.number}` });
      });

      if (sampleAmenity) {
        chips.push({ text: `📍 ${sampleAmenity.name}`, query: sampleAmenity.name });
      }

      this.addAiMessage({
        text: `Welcome to <strong>${targetLayout.name}</strong> (${targetLayout.location})! 📍<br>${plotKeys.length} ${uLabel}s, ${targetLayout.amenities?.length || 0} community amenities.<br><br><strong>Are you trying to go to a specific ${uLabel} or place?</strong>`,
        chips: chips
      });
    },

    close() {
      const drawer = document.getElementById('ai-chat-drawer');
      if (!drawer) return;
      drawer.classList.remove('open');
      setTimeout(() => {
        if (!this.isOpen) drawer.style.display = 'none';
      }, 300);
      this.isOpen = false;
    },

    reset() {
      const messagesContainer = document.getElementById('ai-chat-messages');
      if (messagesContainer) messagesContainer.innerHTML = '';
      this.state = 'IDLE';
      this.open();
    },

    setTyping(isTyping) {
      const indicator = document.getElementById('ai-typing-indicator');
      if (indicator) {
        indicator.style.display = isTyping ? 'flex' : 'none';
      }
      this.scrollToBottom();
    },

    scrollToBottom() {
      const messagesContainer = document.getElementById('ai-chat-messages');
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }
    },

    addUserMessage(text) {
      const messagesContainer = document.getElementById('ai-chat-messages');
      if (!messagesContainer) return;
      const msgDiv = document.createElement('div');
      msgDiv.className = 'ai-msg user';
      msgDiv.innerHTML = `<div class="ai-bubble user-bubble">${escapeHtml(text)}</div>`;
      messagesContainer.appendChild(msgDiv);
      this.scrollToBottom();
    },

    addAiMessage({ text, chips = [], routeInfo = null }) {
      const messagesContainer = document.getElementById('ai-chat-messages');
      if (!messagesContainer) return;
      const msgDiv = document.createElement('div');
      msgDiv.className = 'ai-msg ai';

      let html = `<div class="ai-bubble">${text}`;
      if (routeInfo) {
        html += `<div class="ai-route-info">${routeInfo}</div>`;
      }
      html += `</div>`;

      if (chips && chips.length > 0) {
        html += `<div class="ai-chips-wrap">`;
        chips.forEach(c => {
          html += `<button class="ai-action-chip" data-query="${escapeHtml(c.query)}">${escapeHtml(c.text)}</button>`;
        });
        html += `</div>`;
      }

      msgDiv.innerHTML = html;
      messagesContainer.appendChild(msgDiv);

      msgDiv.querySelectorAll('.ai-action-chip').forEach(btn => {
        btn.addEventListener('click', () => {
          const q = btn.getAttribute('data-query');
          this.handleUserQuery(q);
        });
      });

      this.scrollToBottom();
    },

    handleUserQuery(rawText) {
      if (!rawText || !rawText.trim()) return;
      const text = rawText.trim();
      this.addUserMessage(text);
      this.setTyping(true);

      setTimeout(() => {
        this.setTyping(false);
        this.processQuery(text);
      }, 350);
    },

    processQuery(query) {
      const lower = query.toLowerCase().trim();

      // Conversational State Machine: ASKING_SPECIFIC_PLACE
      if (this.state === 'ASKING_SPECIFIC_PLACE') {
        const targetLayout = layouts[this.chosenLayoutId] || currentLayout;
        if (/^(yes|yeah|yep|y|sure|true|definitely|specific|correct|of course|i do|i am)/i.test(lower) || lower.includes('yes') || lower.includes('specific')) {
          this.state = 'ASKING_HOUSE_NUMBER';

          const plotKeys = Object.keys(targetLayout.plots);
          const samplePlots = plotKeys.slice(0, 6).map(k => targetLayout.plots[k]);
          const chips = samplePlots.map(p => ({
            text: `${targetLayout.unitType || 'Unit'} #${p.number}`,
            query: `${targetLayout.unitType || 'Unit'} ${p.number}`
          }));

          this.addAiMessage({
            text: `Which <strong>${targetLayout.unitType || 'house'} or room number</strong> are you looking for in <strong>${targetLayout.name}</strong>?`,
            chips: chips
          });
          return;
        } else if (/^(no|nope|nah|not really|just looking|exploring|browse|all)/i.test(lower) || lower.includes('no') || lower.includes('explor')) {
          this.state = 'EXPLORING';
          this.addAiMessage({
            text: `Opening the full <strong>${targetLayout.name}</strong> layout map for you! 🌿<br><br>I'm launching your guided tour so you know where everything is located.`,
            chips: [
              { text: "🚀 Start Tour", query: "Start Tutorial" },
              { text: "📍 My GPS Location", query: "Track live location" },
              { text: "🗺️ All Layouts", query: "Where do I go?" }
            ]
          });
          setTimeout(() => {
            this.close();
            loadLayout(targetLayout.id);
            startLayoutTutorial(targetLayout);
          }, 800);
          return;
        }
      }

      // Conversational State Machine: SELECTING_LAYOUT
      if (this.state === 'SELECTING_LAYOUT') {
        for (const [lid, lay] of Object.entries(layouts)) {
          const lName = lay.name.toLowerCase();
          const cleanName = lName.replace(/layout|phase|stage|block|residency|campus|homes|apartments|villas|city/g, '').trim();
          if (lower.includes(lName) || (cleanName.length >= 3 && lower.includes(cleanName))) {
            this.chosenLayoutId = lid;
            this.state = 'ASKING_SPECIFIC_PLACE';
            const uLabel = lay.unitType ? lay.unitType.toLowerCase() : 'house';
            const plotKeys = Object.keys(lay.plots);
            const samplePlots = plotKeys.slice(0, 3).map(k => lay.plots[k]);
            const chips = [
              { text: `✅ Yes, a specific ${uLabel}`, query: "Yes" },
              { text: `🌿 No, explore full layout`, query: "No" }
            ];
            samplePlots.forEach(p => {
              chips.push({ text: `${lay.unitType || 'Unit'} #${p.number}`, query: `${lay.unitType || 'Unit'} ${p.number}` });
            });
            this.addAiMessage({
              text: `Selected <strong>${lay.name}</strong> in ${lay.location}! 🗺️<br>${plotKeys.length} ${uLabel}s, ${lay.amenities?.length || 0} amenities.<br><br><strong>Are you trying to go to a specific ${uLabel} or house?</strong>`,
              chips: chips
            });
            return;
          }
        }
      }

      // Check if user asked for tutorial directly
      if (lower.includes('tutorial') || lower.includes('tour') || lower.includes('guide me') || lower.includes('walkthrough')) {
        this.close();
        startLayoutTutorial(currentLayout, state.selectedPlotId ? plots[state.selectedPlotId]?.number : null);
        return;
      }

      // Check if user asks about a specific layout name directly
      for (const [lid, lay] of Object.entries(layouts)) {
        const lName = lay.name.toLowerCase();
        const cleanName = lName.replace(/layout|phase|stage|block|residency|campus|homes|apartments|villas|city/g, '').trim();
        if (lower.includes(lName) || (cleanName.length >= 4 && lower.includes(cleanName))) {
          this.chosenLayoutId = lid;
          this.state = 'ASKING_SPECIFIC_PLACE';
          const uLabel = lay.unitType ? lay.unitType.toLowerCase() : 'house';
          const plotKeys = Object.keys(lay.plots);
          const samplePlots = plotKeys.slice(0, 3).map(k => lay.plots[k]);
          const chips = [
            { text: `✅ Yes, a specific ${uLabel}`, query: "Yes" },
            { text: `🌿 No, explore full layout`, query: "No" }
          ];
          samplePlots.forEach(p => {
            chips.push({ text: `${lay.unitType || 'Unit'} #${p.number}`, query: `${lay.unitType || 'Unit'} ${p.number}` });
          });
          this.addAiMessage({
            text: `Welcome to <strong>${lay.name}</strong> (${lay.location})! 📍<br>${plotKeys.length} ${uLabel}s, ${lay.amenities?.length || 0} community amenities.<br><br><strong>Are you trying to go to a specific ${uLabel} or place?</strong>`,
            chips: chips
          });
          return;
        }
      }

      // Area queries: "Where do I go?", "where should i go in whitefield", "layouts in south", etc.
      const isSouth = lower.includes('south') || lower.includes('bannerghatta') || lower.includes('kanakapura') || lower.includes('jp nagar') || lower.includes('jayanagar') || lower.includes('btm') || lower.includes('meenakshi');
      const isEast = lower.includes('whitefield') || lower.includes('sarjapur') || lower.includes('east') || lower.includes('varthur') || lower.includes('marathahalli') || lower.includes('carmelaram');
      const isEcity = lower.includes('electronic city') || lower.includes('ecity') || lower.includes('e-city') || lower.includes('hsr') || lower.includes('bellandur') || lower.includes('orr') || lower.includes('outer ring road') || lower.includes('green glen');
      const isNorth = lower.includes('north') || lower.includes('hebbal') || lower.includes('manyata') || lower.includes('yelahanka') || lower.includes('airport') || lower.includes('jakkur') || lower.includes('sahakara');
      const isWest = lower.includes('central') || lower.includes('west') || lower.includes('koramangala') || lower.includes('indiranagar') || lower.includes('malleswaram') || lower.includes('rajajinagar') || lower.includes('sadashivanagar') || lower.includes('banashankari') || lower.includes('vijayanagar') || lower.includes('peenya');

      const isAreaDiscovery = lower.includes('where do i go') ||
        lower.includes('where to go') ||
        lower.includes('how do i navigate') ||
        lower.includes('where should i go') ||
        lower.includes('help me find where to go') ||
        lower.includes('show layout') ||
        lower.includes('show me layout') ||
        lower.includes('tell me the location') ||
        lower.includes('layouts in') ||
        lower.includes('layout in') ||
        lower === 'navigate' ||
        lower === 'layout' ||
        lower === 'layouts' ||
        isSouth || isEast || isEcity || isNorth || isWest;

      if (isAreaDiscovery) {
        if (isSouth) {
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Here are the top residential layouts in <strong>Bangalore South</strong> (Bannerghatta, Kanakapura, JP Nagar & Jayanagar): 🏡<br><br>
• <strong>Himagiri Meadows</strong> — 344 residential plots, 8 avenues, 2 gates & temples<br>
• <strong>Brigade Meadows</strong> — 48 units, Kanakapura Road township<br>
• <strong>Mantri Tranquil</strong> — 48 units, Gubbalala vicinity<br>
• <strong>Concorde Napa Valley</strong> — 44 luxury villas, Kanakapura corridor<br>
• <strong>JP Nagar 7th Phase & 2nd Phase</strong> — Premier BDA residential layouts<br>
• <strong>Jayanagar 4th & 9th Block</strong> — Historic, prestigious South Bangalore layouts<br><br>
<strong>Which layout would you like to explore, or are you trying to go to a specific house?</strong>`,
            chips: [
              { text: "🏡 Himagiri Meadows", query: "Himagiri Meadows" },
              { text: "🌳 Brigade Meadows", query: "Brigade Meadows" },
              { text: "✨ Mantri Tranquil", query: "Mantri Tranquil" },
              { text: "🍇 Concorde Napa Valley", query: "Concorde Napa Valley" },
              { text: "📍 JP Nagar 7th Phase", query: "JP Nagar 7th Phase" }
            ]
          });
          return;
        } else if (isEast) {
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Here are the top residential layouts in <strong>East Bangalore & Whitefield</strong>: 🌳<br><br>
• <strong>Palm Meadows</strong> — 44 luxury villas, Varthur Main Road<br>
• <strong>Prestige Lakeside Habitat</strong> — 48 units, Varthur Lake township<br>
• <strong>Greenwood Orchards</strong> — 60 bespoke villas, Sarjapur Road<br>
• <strong>Prestige Shantiniketan</strong> — 44 high-rise units, ITPL Main Road<br>
• <strong>Rainbow Drive</strong> — 44 gated villas, Sarjapur Road<br>
• <strong>Divyasree Republic of Whitefield</strong> — 44 units, EPIP Zone<br><br>
<strong>Which layout would you like to explore, or are you looking for a specific villa/apartment?</strong>`,
            chips: [
              { text: "🌳 Palm Meadows", query: "Palm Meadows" },
              { text: "🌊 Prestige Lakeside", query: "Prestige Lakeside Habitat" },
              { text: "🏡 Greenwood Orchards", query: "Greenwood Orchards" },
              { text: "🏢 Prestige Shantiniketan", query: "Prestige Shantiniketan" },
              { text: "🌈 Rainbow Drive", query: "Rainbow Drive" }
            ]
          });
          return;
        } else if (isEcity) {
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Here are the top layouts in <strong>Electronic City, HSR & Outer Ring Road (ORR)</strong>: 🏢<br><br>
• <strong>Tech Horizon Campus</strong> — 36 enterprise blocks & tech towers, Electronic City Phase 1<br>
• <strong>Adarsh Palm Retreat</strong> — 44 luxury villas, Bellandur ORR corridor<br>
• <strong>HSR Layout Sectors 1, 2 & 3</strong> — Premier planned residential sectors<br>
• <strong>Green Glen Layout</strong> — 40 units, Bellandur tech hub<br>
• <strong>Neotown Electronic City</strong> — 44 units, Electronic City Phase 1<br><br>
<strong>Which layout or campus are you trying to visit?</strong>`,
            chips: [
              { text: "🏢 Tech Horizon Campus", query: "Tech Horizon Campus" },
              { text: "🌴 Adarsh Palm Retreat", query: "Adarsh Palm Retreat" },
              { text: "📍 HSR Layout Sector 1", query: "HSR Layout Sector 1" },
              { text: "🌿 Green Glen Layout", query: "Green Glen Layout" },
              { text: "🏙️ Neotown Electronic City", query: "Neotown Electronic City" }
            ]
          });
          return;
        } else if (isNorth) {
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Here are the top residential layouts in <strong>North Bangalore & Airport Corridor</strong>: ✈️<br><br>
• <strong>Sobha City</strong> — 48 units, Thanisandra Main Road luxury township<br>
• <strong>Bhartiya City Nikoo Homes</strong> — 48 units, integrated smart city<br>
• <strong>Manyata Tech Park Residency</strong> — 44 units, Nagavara IT corridor<br>
• <strong>Prestige Golfshire</strong> — 40 signature golf villas, Nandi Hills road<br>
• <strong>Ozone Urbana</strong> — 44 units, Devanahalli airport township<br>
• <strong>RMZ Galleria & Prestige Misty Waters</strong> — Hebbal lake vicinity<br><br>
<strong>Which North Bangalore township would you like to explore?</strong>`,
            chips: [
              { text: "🏙️ Sobha City", query: "Sobha City" },
              { text: "🌆 Bhartiya City", query: "Bhartiya City Nikoo Homes" },
              { text: "🏢 Manyata Residency", query: "Manyata Tech Park Residency" },
              { text: "⛳ Prestige Golfshire", query: "Prestige Golfshire" },
              { text: "✈️ Ozone Urbana", query: "Ozone Urbana" }
            ]
          });
          return;
        } else if (isWest) {
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Here are the top layouts in <strong>Central & West Bangalore</strong>: 🏛️<br><br>
• <strong>Koramangala 4th & 3rd Block</strong> — Bangalore's most prestigious central layouts<br>
• <strong>Indiranagar Defence Colony & HAL 2nd Stage</strong> — Iconic East-Central neighborhoods<br>
• <strong>Brigade Gateway</strong> — 44 units, Rajajinagar landmark township<br>
• <strong>Sadashivanagar Royal Layout</strong> — Premier elite residential enclave<br>
• <strong>Malleswaram 18th Cross</strong> — Historic heritage layout<br>
• <strong>Banashankari 3rd Stage & Vijayanagar BDA</strong> — Major West Bangalore layouts<br><br>
<strong>Which layout would you like to explore?</strong>`,
            chips: [
              { text: "☕ Koramangala 4th Block", query: "Koramangala 4th Block" },
              { text: "🌳 Indiranagar Defence Colony", query: "Indiranagar Defence Colony" },
              { text: "🏢 Brigade Gateway", query: "Brigade Gateway" },
              { text: "👑 Sadashivanagar", query: "Sadashivanagar Royal Layout" },
              { text: "🌺 Malleswaram 18th Cross", query: "Malleswaram 18th Cross" }
            ]
          });
          return;
        } else {
          // General citywide
          this.state = 'SELECTING_LAYOUT';
          this.addAiMessage({
            text: `Welcome to HM Maps! We have <strong>53 verified layouts & townships</strong> across all 5 zones of Bangalore: 🗺️<br><br>
• 🏡 <strong>South</strong>: Himagiri Meadows, Brigade Meadows, Mantri Tranquil, JP Nagar<br>
• 🌳 <strong>Whitefield & East</strong>: Palm Meadows, Prestige Lakeside Habitat, Greenwood Orchards<br>
• 🏢 <strong>Electronic City & ORR</strong>: Tech Horizon Campus, Adarsh Palm Retreat, HSR Layout<br>
• ✈️ <strong>North Bangalore</strong>: Sobha City, Bhartiya City Nikoo Homes, Prestige Golfshire<br>
• 🏛️ <strong>Central & West</strong>: Koramangala 4th Block, Indiranagar Defence Colony, Brigade Gateway<br><br>
<strong>Which area or layout are you trying to visit?</strong>`,
            chips: [
              { text: "🏡 Himagiri Meadows (South)", query: "Himagiri Meadows" },
              { text: "🌳 Palm Meadows (Whitefield)", query: "Palm Meadows" },
              { text: "🏢 Tech Horizon (Electronic City)", query: "Tech Horizon Campus" },
              { text: "✈️ Sobha City (North)", query: "Sobha City" },
              { text: "☕ Koramangala (Central)", query: "Koramangala 4th Block" }
            ]
          });
          return;
        }
      }

      // UNIT LOOKUP: Check in chosen layout first, then active layout, then all layouts
      const searchLayout = layouts[this.chosenLayoutId] || currentLayout;
      let matchedPlot = findPlotInLayout(searchLayout, query);
      let matchedLayout = searchLayout;

      if (!matchedPlot) {
        for (const [lid, lay] of Object.entries(layouts)) {
          const found = findPlotInLayout(lay, query);
          if (found) {
            matchedPlot = found;
            matchedLayout = lay;
            this.chosenLayoutId = lid;
            break;
          }
        }
      }

      if (matchedPlot) {
        const uLabel = matchedLayout.unitType || 'Unit';
        this.state = 'IDLE';
        this.addAiMessage({
          text: `Found it! 🎯<br><strong>${uLabel} #${matchedPlot.number}</strong> is located in <strong>${matchedLayout.name}</strong> on <strong>${matchedPlot.road}</strong> (${matchedPlot.block}, facing ${matchedPlot.facing}).<br><br>🚀 Loading the <strong>${matchedLayout.name}</strong> digital layout now and starting your feature walkthrough tutorial!`,
          chips: [
            { text: "🚀 Start Feature Tutorial", query: "Start Tutorial" },
            { text: "📡 Live GPS Location", query: "Track live location" },
            { text: "🗺️ Full Overview", query: "Where do I go?" }
          ]
        });

        setTimeout(() => {
          this.close();
          loadLayout(matchedLayout.id, matchedPlot.id);
        }, 900);
        return;
      }

      // AMENITY LOOKUP across chosen layout and current layout
      const searchAmenities = searchLayout.amenities || [];
      const matchedAmenity = searchAmenities.find(a => {
        const nameLower = a.name.toLowerCase();
        const idLower = a.id.toLowerCase();
        return lower.includes(nameLower) ||
          (lower.includes('temple') && (nameLower.includes('temple') || idLower.includes('temple'))) ||
          (lower.includes('play') && idLower.includes('play')) ||
          (lower.includes('park') && (idLower.includes('play') || idLower.includes('garden') || idLower.includes('park') || idLower.includes('promenade'))) ||
          (lower.includes('clubhouse') && idLower.includes('clubhouse')) ||
          (lower.includes('pool') && idLower.includes('pool')) ||
          (lower.includes('lake') && idLower.includes('lake')) ||
          (lower.includes('food') && (idLower.includes('food') || idLower.includes('cafeteria'))) ||
          (lower.includes('parking') && idLower.includes('parking')) ||
          (lower.includes('ev') && idLower.includes('ev')) ||
          (lower.includes('auditorium') && idLower.includes('auditorium')) ||
          (lower.includes('gate 1') && idLower.includes('gate_1')) ||
          (lower.includes('gate 2') && idLower.includes('gate_2')) ||
          (lower.includes('wtp') && idLower.includes('wtp')) ||
          (lower.includes('waste') && idLower.includes('waste'));
      });

      if (matchedAmenity) {
        this.state = 'IDLE';
        this.addAiMessage({
          text: `Found <strong>${matchedAmenity.name}</strong> in <strong>${searchLayout.name}</strong>! 📍<br>${matchedAmenity.description || matchedAmenity.desc || 'Society landmark'}.<br><br>Loading layout and plotting route...`,
          chips: [
            { text: "🚀 Start Tutorial", query: "Start Tutorial" },
            { text: "🧭 Where do I go?", query: "Where do I go?" }
          ]
        });

        setTimeout(() => {
          this.close();
          loadLayout(searchLayout.id);
          selectAmenity(matchedAmenity.id, true);
        }, 800);
        return;
      }

      // Live GPS tracking
      if (lower.includes('gps') || lower.includes('live location') || lower.includes('track')) {
        this.close();
        showMapView(currentLayout.id);
        startLocationTracking(true);
        showToast("Started live GPS tracking 📡", 3000);
        return;
      }

      // Fallback
      this.addAiMessage({
        text: `I'm here to guide you across 50+ layouts in Bangalore! 🧭<br><br>You can ask me:<br>• <strong>'Where do I go?'</strong> (to view layouts in Whitefield, South, Electronic City, North, or Central)<br>• A specific layout like <strong>'Palm Meadows'</strong>, <strong>'Sobha City'</strong>, <strong>'HSR Layout'</strong>, or <strong>'Himagiri'</strong><br>• A house/villa number like <strong>'Plot 142'</strong>, <strong>'Villa 24'</strong>, or <strong>'Tower A1'</strong><br>• Society landmarks like <strong>'Grand Clubhouse'</strong>, <strong>'Food Plaza'</strong>, or <strong>'Temple'</strong>`,
        chips: [
          { text: "🧭 Where do I go?", query: "Where do I go?" },
          { text: "🌳 Palm Meadows (Whitefield)", query: "Palm Meadows" },
          { text: "🏡 Himagiri Meadows (South)", query: "Himagiri Meadows" },
          { text: "🏢 Tech Horizon (Electronic City)", query: "Tech Horizon Campus" },
          { text: "✈️ Sobha City (North)", query: "Sobha City" }
        ]
      });
    }
  };

  // Check URL parameters for direct delivery link sharing
  function checkUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const houseNum = params.get('house') || params.get('plot') || params.get('villa') || params.get('unit');
    const gateNum = params.get('gate');
    const mapParam = params.get('map') || params.get('layout');

    if (gateNum === '2') {
      state.startNodeId = 'gate_2';
      startSelect.value = 'gate_2';
    }

    if (mapParam && layouts[mapParam]) {
      loadLayout(mapParam, houseNum);
    } else if (houseNum) {
      loadLayout('himagiri', houseNum);
    } else {
      // By default: Show Portal View! Himagiri is NOT the first map that they see!
      showPortalView();
    }
  }

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    initMap();
    setupEventListeners();
  });

})();
