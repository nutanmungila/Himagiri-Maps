/**
 * Himagiri Meadows Layout Navigator & Interactive Vector Map
 * Complete Wayfinding, Turn-by-Turn Directions, Voice & Conversational Assistant
 */

(function () {
  'use strict';

  // Check data availability (Support both window.LAYOUTS and legacy window.HIMAGIRI_DATA)
  const layouts = window.LAYOUTS || {};
  let currentLayoutId = ('prestige_falcon_city' in layouts) ? 'prestige_falcon_city' : (Object.keys(layouts)[0] || 'himagiri');
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

  // Universal Plot / Apartment / Unit Lookup Helper
  function findPlotInLayout(layout, query) {
    if (!layout || !layout.plots || !query) return null;
    const qClean = String(query).trim().toUpperCase();
    const isTowerOrBlock = /^(TOWER|BLOCK|WING)\s+/i.test(qClean);
    const qNorm = qClean.replace(/^(FLAT|APT|APARTMENT|PLOT|VILLA|HOUSE|BLOCK|TOWER|ROOM|SITE|H\.?NO|WING)\s*#?\s*/i, '').trim();

    // If user searched for a specific Tower or Block (e.g. 'Tower 5', 'Block A')
    if (isTowerOrBlock) {
      for (const pid in layout.plots) {
        const p = layout.plots[pid];
        if (p.number.toUpperCase().startsWith(qClean) || (p.block && p.block.toUpperCase().startsWith(qClean))) {
          return p;
        }
      }
    }

    // Exact ID / Number matches
    if (layout.plots[qClean]) return layout.plots[qClean];
    if (layout.plots[qNorm]) return layout.plots[qNorm];

    for (const pid in layout.plots) {
      const p = layout.plots[pid];
      const numClean = p.number.toUpperCase();
      const numNorm = numClean.replace(/^(FLAT|APT|APARTMENT|PLOT|VILLA|HOUSE|BLOCK|TOWER|ROOM|SITE|WING)\s*#?\s*/i, '').trim();

      if (numClean === qClean || numClean === qNorm) return p;
      if (numNorm === qClean || numNorm === qNorm) return p;

      if (numClean.replace(/\s*-\s*/g, ' ').includes(qClean.replace(/\s*-\s*/g, ' '))) return p;
      if (numClean.replace(/[\s-]/g, '').includes(qClean.replace(/[\s-]/g, ''))) return p;

      if (/^\d+$/.test(qNorm)) {
        if (numClean.endsWith(' ' + qNorm) || numClean.endsWith('-' + qNorm) || numClean.endsWith('- ' + qNorm)) return p;
      }
    }

    if (!isTowerOrBlock) {
      for (const pid in layout.plots) {
        const p = layout.plots[pid];
        if (p.id.toUpperCase() === qNorm) return p;
        if (p.block && p.block.toUpperCase().includes(qClean)) return p;
      }
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

  // Simplified click helper (interior feature removed)
  function enableHoldTrigger(el, onTrigger) {
    if (!el) return;
    el._justFiredHold = () => false;
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

    // Water Body (Lakes, Lagoon, Reflection Pools, Olympic Swimming Facilities)
    if (currentLayout.waterBody) {
      const wb = currentLayout.waterBody;
      const waterG = document.createElementNS("http://www.w3.org/2000/svg", "g");
      waterG.setAttribute("class", "water-body-element");

      if (wb.points) {
        const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        poly.setAttribute("points", wb.points);
        poly.setAttribute("fill", "#075985");
        poly.setAttribute("stroke", "#38bdf8");
        poly.setAttribute("stroke-width", "2");
        waterG.appendChild(poly);
      } else {
        const water = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        water.setAttribute("x", wb.x);
        water.setAttribute("y", wb.y);
        water.setAttribute("width", wb.w);
        water.setAttribute("height", wb.h);
        water.setAttribute("rx", wb.rx || "12");
        water.setAttribute("fill", "#0c4a6e");
        water.setAttribute("stroke", "#0284c7");
        water.setAttribute("stroke-width", "2");
        waterG.appendChild(water);
      }

      if (wb.label) {
        const wtxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        const cx = wb.points ? (wb.cx || 620) : (wb.x + wb.w / 2);
        const cy = wb.points ? (wb.cy || 480) : (wb.y + wb.h / 2 + 4);
        wtxt.setAttribute("x", cx);
        wtxt.setAttribute("y", cy);
        wtxt.setAttribute("text-anchor", "middle");
        wtxt.setAttribute("fill", "#7dd3fc");
        wtxt.setAttribute("font-size", "11px");
        wtxt.setAttribute("font-weight", "700");
        wtxt.setAttribute("letter-spacing", "0.8px");
        wtxt.textContent = `💧 ${wb.label.toUpperCase()}`;
        waterG.appendChild(wtxt);
      }
      bgGroup.appendChild(waterG);
    }

    // Central Garden Park Area polygon
    if (currentLayout.gardenPark) {
      const gp = currentLayout.gardenPark;
      const parkG = document.createElementNS("http://www.w3.org/2000/svg", "g");
      parkG.setAttribute("class", "garden-park-element");

      if (gp.points) {
        const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        poly.setAttribute("points", gp.points);
        poly.setAttribute("fill", "#064e3b");
        poly.setAttribute("stroke", "#10b981");
        poly.setAttribute("stroke-width", "1.5");
        parkG.appendChild(poly);
      } else {
        const gardenPark = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        gardenPark.setAttribute("x", gp.x);
        gardenPark.setAttribute("y", gp.y);
        gardenPark.setAttribute("width", gp.w);
        gardenPark.setAttribute("height", gp.h);
        gardenPark.setAttribute("rx", gp.rx || "6");
        gardenPark.setAttribute("fill", "#064e3b");
        gardenPark.setAttribute("stroke", "#10b981");
        gardenPark.setAttribute("stroke-width", "1.5");
        parkG.appendChild(gardenPark);
      }

      if (gp.label) {
        const gtxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        const cx = gp.points ? (gp.cx || 620) : (gp.x + gp.w / 2);
        const cy = gp.points ? (gp.cy || 480) : (gp.y + gp.h / 2 + 4);
        gtxt.setAttribute("x", cx);
        gtxt.setAttribute("y", cy);
        gtxt.setAttribute("text-anchor", "middle");
        gtxt.setAttribute("fill", "#a7f3d0");
        gtxt.setAttribute("font-size", "11px");
        gtxt.setAttribute("font-weight", "700");
        gtxt.setAttribute("letter-spacing", "0.5px");
        gtxt.textContent = `🌳 ${gp.label.toUpperCase()}`;
        parkG.appendChild(gtxt);
      }
      bgGroup.appendChild(parkG);
    }

    // Landmark Architectural Complexes (Malls, Tech Parks, World Trade Centers, Convention Halls)
    if (currentLayout.landmarks && Array.isArray(currentLayout.landmarks)) {
      for (const lm of currentLayout.landmarks) {
        const lmG = document.createElementNS("http://www.w3.org/2000/svg", "g");
        lmG.setAttribute("class", "landmark-element");

        const lmRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        lmRect.setAttribute("x", lm.x);
        lmRect.setAttribute("y", lm.y);
        lmRect.setAttribute("width", lm.w);
        lmRect.setAttribute("height", lm.h);
        lmRect.setAttribute("rx", lm.rx || "8");
        lmRect.setAttribute("fill", lm.fill || "#1e1b4b");
        lmRect.setAttribute("stroke", lm.stroke || "#818cf8");
        lmRect.setAttribute("stroke-width", "2");
        lmG.appendChild(lmRect);

        if (lm.label) {
          const lmtxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
          lmtxt.setAttribute("x", lm.x + lm.w / 2);
          lmtxt.setAttribute("y", lm.y + lm.h / 2 + 4);
          lmtxt.setAttribute("text-anchor", "middle");
          lmtxt.setAttribute("fill", lm.textColor || "#c7d2fe");
          lmtxt.setAttribute("font-size", lm.fontSize || "11px");
          lmtxt.setAttribute("font-weight", "700");
          lmtxt.textContent = lm.label;
          lmG.appendChild(lmtxt);
        }

        lmG.addEventListener('click', (e) => {
          e.stopPropagation();
          const lbl = lm.label || 'Commercial Complex';
          showToast(`🏢 ${lbl}`, 2000);
        });

        bgGroup.appendChild(lmG);
      }
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
      roadPath.setAttribute("stroke-width", "22");
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

  // Helper: check if layout is an apartment/tower/block community
  function isApartmentOrBlockLayout(layout) {
    if (!layout) return false;
    if (layout.id === 'himagiri') return false; // Himagiri Meadows is a landed plot community with 344 individual surveyed plots
    const uType = (layout.unitType || '').toLowerCase();
    const lType = (layout.type || '').toLowerCase();
    if (lType.includes('gated plotted') || lType.includes('plotted layout') || lType.includes('villa estate') || uType.includes('plot') || uType.includes('site')) {
      return false; // Landed plotted communities have individual surveyed sites!
    }
    if (uType.includes('apartment') || uType.includes('tower') || uType.includes('block') || uType.includes('wing') || uType.includes('flat')) return true;
    if (lType.includes('apartment') || lType.includes('township') || lType.includes('high-rise') || lType.includes('flat') || lType.includes('condominium')) return true;
    return false;
  }

  // Clean block/apartment names to guarantee ZERO numbers or digits inside apartment shapes & UI
  function cleanBlockTitle(bName) {
    if (!bName) return 'Residential Block';
    let str = String(bName).trim();

    // Extract inside parentheses if present, e.g. "Tower 1 (Block A)" -> "Block A", "Tower 1 (Aurum)" -> "Aurum Tower"
    const paren = str.match(/\(([^)]+)\)/);
    if (paren) {
      let inside = paren[1].trim();
      if (/block\s+[A-Za-z]/i.test(inside)) {
        return inside;
      }
      if (!/tower|block|wing/i.test(inside)) {
        inside += ' Tower';
      }
      return inside;
    }

    // Common named tower range / number conversions
    str = str.replace(/Tower\s+1[-–—]\d+/gi, 'Tower A');
    str = str.replace(/Tower\s+2[-–—]\d+/gi, 'Tower B');
    str = str.replace(/Tower\s+[3-5][-–—]\d+/gi, 'Tower B');
    str = str.replace(/Tower\s+[6-9][-–—]\d+/gi, 'Tower B');
    str = str.replace(/Tower\s+1[0-9][-–—]\d+/gi, 'Tower C');
    str = str.replace(/Tower\s+1\b/gi, 'Tower A');
    str = str.replace(/Tower\s+2\b/gi, 'Tower B');
    str = str.replace(/Tower\s+3\b/gi, 'Tower C');
    str = str.replace(/Tower\s+4\b/gi, 'Tower D');
    str = str.replace(/Tower\s+5\b/gi, 'Tower E');
    str = str.replace(/Tower\s+6\b/gi, 'Tower F');
    str = str.replace(/Tower\s+7\b/gi, 'Tower G');
    str = str.replace(/Nikoo\s+Homes\s+1/gi, 'Nikoo Homes A');
    str = str.replace(/Nikoo\s+Homes\s+2/gi, 'Nikoo Homes B');
    str = str.replace(/West\s+End\s+Tower\s+1/gi, 'West End Tower A');
    str = str.replace(/West\s+End\s+Tower\s+2/gi, 'West End Tower B');
    str = str.replace(/1st\s+Stage/gi, 'Stage A');
    str = str.replace(/4th\s+Cross/gi, 'Cross B');

    // Remove any remaining numbers or digits from apartment/block titles
    str = str.replace(/\b[0-9]+(?:st|nd|rd|th)?\b/gi, '').replace(/\d+/g, '').replace(/\s+/g, ' ').trim();
    if (!str || str.toLowerCase() === 'tower' || str.toLowerCase() === 'block') {
      return (bName.replace(/\d+/g, '').trim() || 'Block');
    }
    return str;
  }

  // Short clean unit number helper (e.g. "Tower 1 - 101" -> "101", "Block A - 202" -> "202")
  function getShortUnitNumber(p) {
    if (!p) return '';
    const numStr = String(p.number || p.id || '').trim();
    const dashMatch = numStr.match(/[-–—:]\s*([A-Za-z0-9]+)$/);
    if (dashMatch) return dashMatch[1];
    const flatMatch = numStr.match(/(?:flat|unit|plot|house|no\.?)\s*([A-Za-z0-9]+)/i);
    if (flatMatch) return flatMatch[1];
    const blockUnitMatch = numStr.match(/(?:tower|block|wing)\s+([A-Za-z0-9]+)/i);
    if (blockUnitMatch && numStr.length <= 10) return blockUnitMatch[1];
    return numStr;
  }

  // Render Plots / Apartment Blocks (No numbers inside blocks/apartments)
  function renderPlots() {
    plotsLayer.innerHTML = '';

    const isApt = isApartmentOrBlockLayout(currentLayout);

    if (isApt) {
      // Group plots by block/tower
      const blockGroups = {};
      for (const pid in plots) {
        const p = plots[pid];
        const bName = p.block || 'Main Tower';
        if (!blockGroups[bName]) blockGroups[bName] = [];
        blockGroups[bName].push(p);
      }

      for (const bName in blockGroups) {
        const uList = blockGroups[bName];
        const isBlockActive = uList.some(p => p.id === state.selectedPlotId);

        // Calculate bounding box and center of the block
        const xs = uList.map(u => u.x);
        const ys = uList.map(u => u.y);
        const minX = Math.min(...xs);
        const minY = Math.min(...ys);
        const maxX = Math.max(...uList.map(u => u.x + u.w));
        const maxY = Math.max(...uList.map(u => u.y + u.h));
        const cx = (minX + maxX) / 2;
        const cy = (minY + maxY) / 2;

        // Clean architectural building footprint
        const blockW = Math.max(124, maxX - minX + 16);
        const blockH = Math.max(72, maxY - minY + 16);
        const bx = cx - blockW / 2;
        const by = cy - blockH / 2;

        const cleanName = cleanBlockTitle(bName);
        const safeBlockId = cleanName.replace(/[^a-zA-Z0-9]/g, '_');
        const blockG = document.createElementNS("http://www.w3.org/2000/svg", "g");
        blockG.setAttribute("class", `svg-building-block svg-plot ${isBlockActive ? 'block-has-active active-target' : ''}`);
        blockG.setAttribute("id", `building-block-${safeBlockId}`);
        blockG.setAttribute("data-id", uList[0].id);
        blockG.setAttribute("data-block", cleanName);
        blockG.setAttribute("data-road", uList[0].road);
        blockG.style.cursor = "pointer";

        // Building base footprint shell
        const shell = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        shell.setAttribute("class", "building-shell");
        shell.setAttribute("x", bx);
        shell.setAttribute("y", by);
        shell.setAttribute("width", blockW);
        shell.setAttribute("height", blockH);
        shell.setAttribute("rx", "8");
        shell.setAttribute("fill", isBlockActive ? "#1e293b" : "#0f172a");

        if (isBlockActive) {
          shell.setAttribute("stroke", "#f59e0b");
          shell.setAttribute("stroke-width", "2.5");
        } else {
          shell.setAttribute("stroke", "#3b82f6");
          shell.setAttribute("stroke-width", "1.5");
        }

        blockG.appendChild(shell);

        // Top architectural accent line
        const accent = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        accent.setAttribute("x", bx);
        accent.setAttribute("y", by);
        accent.setAttribute("width", blockW);
        accent.setAttribute("height", "4");
        accent.setAttribute("rx", "2");
        accent.setAttribute("fill", isBlockActive ? "#f59e0b" : "#38bdf8");
        blockG.appendChild(accent);

        // Block Title text (e.g. 🏢 Block A, 🏢 Aurum Tower) - Absolutely NO numbers or digits inside
        const titleTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        titleTxt.setAttribute("class", "building-title");
        titleTxt.setAttribute("x", cx);
        titleTxt.setAttribute("y", cy - 2);
        titleTxt.setAttribute("text-anchor", "middle");
        titleTxt.setAttribute("font-size", "12px");
        titleTxt.setAttribute("font-weight", "700");
        titleTxt.setAttribute("fill", isBlockActive ? "#fbbf24" : "#f1f5f9");
        titleTxt.textContent = `🏢 ${cleanName}`;
        blockG.appendChild(titleTxt);

        // Subtitle text (e.g. Apartment Tower / Block)
        const subTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        subTxt.setAttribute("class", "building-subtitle");
        subTxt.setAttribute("x", cx);
        subTxt.setAttribute("y", cy + 15);
        subTxt.setAttribute("text-anchor", "middle");
        subTxt.setAttribute("font-size", "9.5px");
        subTxt.setAttribute("font-weight", "500");
        subTxt.setAttribute("fill", isBlockActive ? "#fde68a" : "#94a3b8");
        subTxt.textContent = (currentLayout.unitType === 'Flat' ? 'Residential Flat' : (currentLayout.unitType ? currentLayout.unitType.replace(/ \/ .*/, '') : 'Apartment Tower')).replace(/\d+/g, '').trim();
        blockG.appendChild(subTxt);

        // Click to select block & track to its flats/doorstep
        blockG.addEventListener('click', (e) => {
          e.stopPropagation();
          selectPlot(uList[0].id, false);
        });

        // Hover Tooltip (clean name with NO digits)
        blockG.addEventListener('mouseenter', (e) => {
          showPlotTooltip(e, {
            number: cleanName,
            block: cleanName,
            road: uList[0].road,
            facing: uList[0].facing
          });
        });
        blockG.addEventListener('mousemove', (e) => movePlotTooltip(e));
        blockG.addEventListener('mouseleave', hidePlotTooltip);

        plotsLayer.appendChild(blockG);
      }
      return;
    }

    // Standard Landed Plot Layout (Himagiri Meadows 1-344, Plotted layouts)
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

      // Only append number label for standard plotted layouts (never inside apartments/blocks)
      if (!isApartmentOrBlockLayout(currentLayout)) {
        g.appendChild(txt);
      }

      // Click to select plot & track to house doorstep
      g.addEventListener('click', (e) => {
        e.stopPropagation();
        selectPlot(p.id, false);
      });

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
        if (g._justFiredHold && g._justFiredHold()) return;
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

    // Plots or Blocks in Destination dropdown
    if (isApartmentOrBlockLayout(currentLayout)) {
      const blockGroups = {};
      for (const pid in plots) {
        const p = plots[pid];
        const b = cleanBlockTitle(p.block || 'Main Block');
        if (!blockGroups[b]) blockGroups[b] = [];
        blockGroups[b].push(p);
      }
      for (const bName in blockGroups) {
        const groupOpt = document.createElement('optgroup');
        groupOpt.label = `🏢 ${bName}`;
        for (const p of blockGroups[bName]) {
          const opt = document.createElement('option');
          opt.value = `plot:${p.id}`;
          opt.textContent = `${p.number} (${p.road})`;
          groupOpt.appendChild(opt);
        }
        destSelect.appendChild(groupOpt);
      }
    } else {
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
  }

  // Layout Switcher: dynamically swaps active dataset, blueprints, roads & units
  function loadLayout(layoutId, targetPlotId = null) {
    if (!layouts[layoutId]) {
      // Try dynamic fetch from MongoDB REST API if running on a server
      if (window.location.protocol.startsWith('http')) {
        fetch(`/api/layouts/${layoutId}`)
          .then(res => res.ok ? res.json() : null)
          .then(doc => {
            if (doc && doc.plots) {
              layouts[layoutId] = doc;
              loadLayout(layoutId, targetPlotId);
            } else {
              console.warn("Layout not found in window.LAYOUTS or MongoDB:", layoutId);
            }
          })
          .catch(() => console.warn("Layout not found:", layoutId));
        return;
      }
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

    // Update document title and URL parameters for this layout
    document.title = `${currentLayout.name} — HM Maps Layout Navigator`;
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('map', layoutId);
      if (!targetPlotId) {
        url.searchParams.delete('house');
        url.searchParams.delete('plot');
      }
      window.history.replaceState({}, '', url.toString());
    } catch (_) {}

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
        let resolvedPlotId = targetPlotId;
        if (!plots[targetPlotId]) {
          const cleanTarget = String(targetPlotId).toLowerCase().replace(/^(house|plot|villa|flat|unit)\s*#?/i, '').trim();
          for (const [pid, p] of Object.entries(plots)) {
            const pNum = String(p.number || '').toLowerCase();
            if (pNum === cleanTarget || pid.toLowerCase() === cleanTarget || pNum.endsWith(cleanTarget) || pid.endsWith(`_${cleanTarget}`)) {
              resolvedPlotId = pid;
              break;
            }
          }
        }
        if (plots[resolvedPlotId]) {
          selectPlot(resolvedPlotId, true);
          calculateAndDisplayRoute(state.startNodeId, resolvedPlotId);
          const p = plots[resolvedPlotId];
          startLayoutTutorial(currentLayout, p ? p.number : resolvedPlotId);
          try {
            const url = new URL(window.location.href);
            url.searchParams.set('map', layoutId);
            url.searchParams.set('plot', (p && p.number) ? p.number : resolvedPlotId);
            window.history.replaceState({}, '', url.toString());
          } catch (_) {}
        }
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
      if (layout.id === 'prestige_falcon_city') brandIcon.textContent = '🏢';
      else if (layout.id === 'prestige_elysian') brandIcon.textContent = '✨';
      else if (layout.id === 'kristal_beryl') brandIcon.textContent = '💎';
      else if (layout.id === 'sattva_greenage') brandIcon.textContent = '🌳';
      else if (layout.id === 'sobha_dream_acres') brandIcon.textContent = '🌊';
      else if (layout.id === 'himagiri') brandIcon.textContent = '🏡';
      else brandIcon.textContent = (layout.unitType && layout.unitType.includes('Tower')) ? '🏢' : '🗺️';
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
    if (startNid === endNid) return { nodes: [startNid], edges: [], totalDist: 0 };

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

  // Project a point onto a line segment
  function projectPointOnSegment(px, py, x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const lenSq = dx * dx + dy * dy;
    if (lenSq === 0) return { x: x1, y: y1, t: 0, dist: Math.hypot(px - x1, py - y1) };
    let t = ((px - x1) * dx + (py - y1) * dy) / lenSq;
    t = Math.max(0, Math.min(1, t));
    const projX = x1 + t * dx;
    const projY = y1 + t * dy;
    const dist = Math.hypot(px - projX, py - projY);
    return { x: projX, y: projY, t, dist };
  }

  // Find exact curb point on the road right next to the location (prevents routing to the centre of the road)
  function findBestCurbPoint(plot, edgeList, nodeDict) {
    if (!plot) return null;
    const pcx = plot.x + plot.w / 2;
    const pcy = plot.y + plot.h / 2;
    let best = null;
    let minScore = Infinity;
    const targetRoad = (plot.road || '').toLowerCase().trim();

    for (const e of edgeList) {
      const u = nodeDict[e.u];
      const v = nodeDict[e.v];
      if (!u || !v) continue;
      const proj = projectPointOnSegment(pcx, pcy, u.x, u.y, v.x, v.y);
      const edgeRoad = (e.road || '').toLowerCase().trim();

      let roadMatch = false;
      if (targetRoad && edgeRoad) {
        if (targetRoad === edgeRoad || targetRoad.includes(edgeRoad) || edgeRoad.includes(targetRoad)) {
          roadMatch = true;
        }
      }

      let score = proj.dist;
      if (!roadMatch) {
        score += 70; // Prioritize edges on the same road as the plot
      }

      if (score < minScore) {
        minScore = score;
        best = {
          edge: e,
          u: e.u,
          v: e.v,
          x: Math.round(proj.x),
          y: Math.round(proj.y),
          t: proj.t,
          dist: Math.round(proj.dist),
          road: e.road || plot.road || 'Road'
        };
      }
    }

    if (!best && plot.roadNode && nodeDict[plot.roadNode]) {
      const n = nodeDict[plot.roadNode];
      return {
        edge: null,
        u: plot.roadNode,
        v: plot.roadNode,
        x: n.x,
        y: n.y,
        t: 0,
        dist: Math.hypot(pcx - n.x, pcy - n.y),
        road: plot.road || 'Road'
      };
    }

    return best;
  }

  // Find shortest path to the curb point right next to the location
  function findShortestPathToCurb(startNid, curb) {
    if (!curb || !curb.u || !curb.v) return null;
    if (!nodes[startNid] || !nodes[curb.u] || !nodes[curb.v]) return null;

    const uNode = nodes[curb.u];
    const vNode = nodes[curb.v];
    const distU = Math.hypot(uNode.x - curb.x, uNode.y - curb.y);
    const distV = Math.hypot(vNode.x - curb.x, vNode.y - curb.y);

    let routeU = null;
    let routeV = null;

    if (startNid === curb.u) {
      routeU = { nodes: [curb.u], edges: [], totalDist: 0 };
    } else {
      routeU = findShortestPath(startNid, curb.u);
    }

    if (startNid === curb.v) {
      routeV = { nodes: [curb.v], edges: [], totalDist: 0 };
    } else {
      routeV = findShortestPath(startNid, curb.v);
    }

    const costU = (routeU ? routeU.totalDist : Infinity) + distU;
    const costV = (routeV ? routeV.totalDist : Infinity) + distV;

    if (costU === Infinity && costV === Infinity) return null;

    const viaU = costU <= costV;
    const bestRoute = viaU ? routeU : routeV;
    const entryNode = viaU ? curb.u : curb.v;
    const distToCurb = viaU ? distU : distV;

    const routeEdges = [...bestRoute.edges];
    if (distToCurb > 2) {
      routeEdges.push({ u: entryNode, v: 'curb', road: curb.road, dist: distToCurb });
    }

    return {
      nodes: bestRoute.nodes,
      edges: routeEdges,
      totalDist: bestRoute.totalDist + distToCurb,
      curbPoint: { x: curb.x, y: curb.y },
      entryNode: entryNode,
      distToCurb: distToCurb
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
        const u = nodes[routeResult.edges[i - 1].u] || routeResult.curbPoint;
        const v = nodes[routeResult.edges[i - 1].v] || routeResult.curbPoint;
        const nextV = nodes[edge.v] || routeResult.curbPoint;

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
      const isApt = isApartmentOrBlockLayout(currentLayout);
      const bTitle = cleanBlockTitle(targetPlot.block);
      const targetLabel = isApt ? `<strong>${bTitle}</strong>` : `<strong>House #${targetPlot.number}</strong>`;
      const facing = targetPlot.facing ? ` (${targetPlot.facing}-facing)` : '';
      steps.push({
        icon: "🏁",
        text: `Arrive at ${targetLabel} on ${targetPlot.road}${facing}`,
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

  
  function getLayoutDefaultGate() {
    if (!nodes) return { id: 'gate_1', node: { x: 500, y: 500, label: 'Main Entrance Gate' } };
    const gateNodes = Object.keys(nodes).filter(k => k.includes('gate') && !k.includes('entry') && !k.includes('_x'));
    const gateId = gateNodes.length > 0 ? gateNodes[0] : (Object.keys(nodes)[0] || 'gate_1');
    const gateNode = nodes[gateId] || { x: 500, y: 500, label: 'Main Entrance Gate' };
    return { id: gateId, node: gateNode };
  }

  function findClosestRoadNode(x, y) {
    let closestId = Object.keys(nodes)[0] || 'gate_1';
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
    const geoBtn = document.getElementById('geo-btn');
    if (geoBtn) geoBtn.classList.add('active');
    state.isGeoTracking = true;

    const gate = getLayoutDefaultGate();
    const defaultX = gate.node.x;
    const defaultY = gate.node.y;
    const gateLabel = (gate.node.label || 'Entrance Gate').split(' (')[0];

    // Always guarantee an active user location pin immediately at the layout's real gate
    if (!state.userLocation) {
      state.userLocation = { mapX: defaultX, mapY: defaultY, accuracy: 15 };
      updateUserLocationMarker(defaultX, defaultY, 15);
      if (centerOnUser) {
        zoomToCoordinates(defaultX, defaultY, 1.35);
      }
    }

    if (!navigator.geolocation) {
      showToast(`📍 Live location active at ${gateLabel}. Tap anywhere on the map to set your spot!`, 4000);
      return;
    }

    showToast("Acquiring GPS location... 🛰️", 2000);

    const geoSuccess = (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const accuracy = Math.min(position.coords.accuracy || 20, 45);
      const heading = position.coords.heading;

      let mapX = defaultX;
      let mapY = defaultY;

      if (currentLayout.id === 'himagiri') {
        const distToHim = getDistanceMeters(lat, lng, 12.8605, 77.5925);
        if (distToHim <= 1500) {
          const proj = gpsToMap(lat, lng);
          mapX = proj.mapX;
          mapY = proj.mapY;
          showToast("📍 Located inside Himagiri Meadows!", 2500);
        } else {
          showToast(`📍 Live GPS active. Positioned at ${gateLabel}. Tap map to move pin!`, 3500);
        }
      } else {
        showToast(`📍 Live GPS active! Positioned at ${gateLabel}. Tap anywhere on map to move pin!`, 3500);
      }

      state.userLocation = { lat, lng, mapX, mapY, accuracy, heading };
      updateUserLocationMarker(mapX, mapY, accuracy, heading);

      if (centerOnUser) {
        zoomToCoordinates(mapX, mapY, 1.35);
      }

      if (state.startNodeId === 'my_location' && state.selectedPlotId) {
        calculateAndDisplayRoute('my_location', state.selectedPlotId);
      }
    };

    const geoError = (err) => {
      console.warn("Geolocation warning/timeout:", err);
      showToast(`📍 Placed at ${gateLabel}. Tap anywhere on map to move your location!`, 4000);
      state.userLocation = { mapX: defaultX, mapY: defaultY, accuracy: 20 };
      updateUserLocationMarker(defaultX, defaultY, 20);
      if (centerOnUser) {
        zoomToCoordinates(defaultX, defaultY, 1.35);
      }
      if (state.startNodeId === 'my_location' && state.selectedPlotId) {
        calculateAndDisplayRoute('my_location', state.selectedPlotId);
      }
    };

    if (state.geoWatchId !== null) {
      navigator.geolocation.clearWatch(state.geoWatchId);
    }
    state.geoWatchId = navigator.geolocation.watchPosition(geoSuccess, geoError, {
      enableHighAccuracy: true,
      maximumAge: 5000,
      timeout: 8000
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

    let effectiveStartNodeId = startNid;
    let isUserLocationStart = false;

    if (startNid === 'my_location') {
      isUserLocationStart = true;
      if (!state.userLocation) {
        const g = getLayoutDefaultGate();
        state.userLocation = { mapX: g.node.x, mapY: g.node.y, accuracy: 15 };
        updateUserLocationMarker(g.node.x, g.node.y, 15);
      }
      effectiveStartNodeId = findClosestRoadNode(state.userLocation.mapX, state.userLocation.mapY);
    }

    // Find curb point directly adjacent to the location on the road network
    const curb = findBestCurbPoint(plot, edges, nodes);
    let route = curb ? findShortestPathToCurb(effectiveStartNodeId, curb) : null;

    if (!route) {
      const fallbackNodeId = plot.roadNode || Object.keys(nodes)[0];
      route = findShortestPath(effectiveStartNodeId, fallbackNodeId);
      if (!route) {
        console.warn("No route found between", effectiveStartNodeId, fallbackNodeId);
        return;
      }
    }

    state.activeRoute = route;

    // Build SVG Path coordinates
    const points = [];
    if (isUserLocationStart && state.userLocation) {
      points.push(`${state.userLocation.mapX},${state.userLocation.mapY}`);
    }

    for (const nid of route.nodes) {
      const n = nodes[nid];
      if (n) points.push(`${n.x},${n.y}`);
    }

    // Add curb point right next to location so route stops beside the plot, not in the centre of the road
    if (route.curbPoint) {
      const lastPoint = points[points.length - 1];
      const curbStr = `${route.curbPoint.x},${route.curbPoint.y}`;
      if (lastPoint !== curbStr) {
        points.push(curbStr);
      }
    }

    // Connect from road curb directly to plot center door
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
      <!-- End Pin / House Doorstep Indicator -->
      <g transform="translate(${plotCenterX}, ${plotCenterY - 14})">
        <path d="M 0,0 C -6,-10 -6,-16 0,-20 C 6,-16 6,-10 0,0 Z" fill="#ef4444" stroke="#ffffff" stroke-width="1.5" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))" />
        <circle cx="0" cy="-14" r="3" fill="#ffffff" />
      </g>
      <!-- House / Flat Doorstep Badge -->
      <g transform="translate(${plotCenterX}, ${plotCenterY - 36})">
        <rect x="-42" y="-11" width="84" height="20" rx="10" fill="#ef4444" stroke="#ffffff" stroke-width="1.2" filter="drop-shadow(0 2px 5px rgba(0,0,0,0.4))" />
        <text x="0" y="3" text-anchor="middle" font-size="9" font-weight="700" fill="#ffffff">${escapeHtml(plot.number)}</text>
      </g>
      <!-- Traveling dot / walker -->
      <circle id="route-traveler" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 0 6px #f59e0b)" />
    `;

    // Start traveling animation
    startRouteTravelerAnimation();

    // Generate Steps & Distance
    let totalDistMeters = Math.round((route.totalDist + (curb ? curb.dist : 15)) * 0.95);
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
    const isApt = isApartmentOrBlockLayout(currentLayout);
    const bTitle = cleanBlockTitle(plot.block);
    const targetLabel = isApt ? bTitle : `House #${plot.number}`;
    const conversationalText = `${targetLabel} is located on ${plot.road}${plot.block && !isApt ? ' in ' + plot.block : ''} (${plot.facing}-facing). From ${startLabel}, it is approximately ${totalDistMeters} meters away (about a ${walkMins}-minute walk). Follow the glowing cyan navigation route highlighted on the map.`;
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
      const isApt = isApartmentOrBlockLayout(currentLayout);
      const bTitle = cleanBlockTitle(matchedPlot.block);
      const resp = isApt
        ? `${matchedPlot.number} in ${bTitle} is on ${matchedPlot.road}. Directions and tracking plotted right to the doorstep!`
        : `${uType} #${matchedPlot.number} is on ${matchedPlot.road} in ${matchedPlot.block}. Directions plotted right to the doorstep!`;
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

    const isApt = isApartmentOrBlockLayout(currentLayout);

    // Populate unit chips in house card for apartment/flat layouts
    const blockUnitsEl = document.getElementById('card-block-units');
    if (blockUnitsEl) {
      if (isApt && plot.block) {
        const siblingPlots = Object.values(plots).filter(p => p.block === plot.block);
        if (siblingPlots.length > 0) {
          blockUnitsEl.innerHTML = `
            <div class="card-block-units-title">🏠 Select House / Flat in ${escapeHtml(cleanBlockTitle(plot.block))}:</div>
            <div class="card-unit-chips">
              ${siblingPlots.map(sp => `
                <button class="unit-chip-btn ${sp.id === plot.id ? 'active' : ''}" data-plot-id="${sp.id}" title="Track to ${escapeHtml(sp.number)}">
                  ${escapeHtml(sp.number)}
                </button>
              `).join('')}
            </div>
          `;
          blockUnitsEl.style.display = 'flex';
          blockUnitsEl.querySelectorAll('.unit-chip-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
              e.stopPropagation();
              const spId = btn.getAttribute('data-plot-id');
              if (spId && plots[spId]) {
                selectPlot(spId, true);
                showToast(`📍 Tracking to ${plots[spId].number} doorstep!`, 2000);
              }
            });
          });
        } else {
          blockUnitsEl.style.display = 'none';
        }
      } else {
        blockUnitsEl.style.display = 'none';
      }
    }

    // Highlight plot in SVG
    highlightPlot(plot.id);

    // Calculate Route directly to house doorstep
    calculateAndDisplayRoute(state.startNodeId, plot.id);

    // Update House Info Card with exact flat/house number
    let displayNum = `#${plot.number}`;
    if (isApt) {
      if (plot.number) {
        displayNum = (plot.number.toLowerCase().includes('flat') || plot.number.toLowerCase().includes('villa') || plot.number.toLowerCase().includes('unit') || plot.number.startsWith('#'))
          ? plot.number
          : `Flat #${plot.number}`;
      } else {
        displayNum = cleanBlockTitle(plot.block);
      }
    }
    document.getElementById('card-house-num').textContent = displayNum;
    document.getElementById('card-road').textContent = plot.road;
    document.getElementById('card-block').textContent = cleanBlockTitle(plot.block || currentLayout.name);
    document.getElementById('card-facing').textContent = `${plot.facing} Facing`;

    // Distances from primary & secondary gates
    const gate1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
    const gate2 = Object.keys(nodes).find(n => (n.includes('east') || n.includes('north') || n === 'gate_2') && n !== gate1);

    const curb = findBestCurbPoint(plot, edges, nodes);
    const routeG1 = gate1 ? (curb ? findShortestPathToCurb(gate1, curb) : findShortestPath(gate1, plot.roadNode)) : null;
    const distG1 = routeG1 ? Math.round((routeG1.totalDist + (curb ? curb.dist : 15)) * 0.95) : '--';
    const cardDistG1 = document.getElementById('card-dist-g1');
    if (cardDistG1) {
      cardDistG1.textContent = `${distG1}m`;
      const prev = cardDistG1.previousElementSibling;
      if (prev && nodes[gate1]) prev.textContent = `From ${nodes[gate1].label.split(' (')[0]}`;
    }

    const routeG2 = gate2 ? (curb ? findShortestPathToCurb(gate2, curb) : findShortestPath(gate2, plot.roadNode)) : null;
    const distG2 = routeG2 ? Math.round((routeG2.totalDist + (curb ? curb.dist : 15)) * 0.95) : '--';
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
    document.querySelectorAll('.svg-plot').forEach(el => el.classList.remove('active-target', 'active-unit-tile'));
    const targetEl = document.getElementById(`plot-${plotId}`);
    if (targetEl) {
      targetEl.classList.add('active-target', 'active-unit-tile');
      // Bring to top
      targetEl.parentNode.appendChild(targetEl);
    }

    // Update active building block shell if in apartment layout
    const targetPlot = plots[plotId];
    if (targetPlot && targetPlot.block) {
      document.querySelectorAll('.svg-building-block').forEach(b => {
        b.classList.remove('block-has-active');
        const s = b.querySelector('.building-shell');
        if (s) {
          s.setAttribute('stroke', '#3b82f6');
          s.setAttribute('stroke-width', '1.5');
        }
      });
      const cleanName = cleanBlockTitle(targetPlot.block);
      const safeBlockId = cleanName.replace(/[^a-zA-Z0-9]/g, '_');
      const blk = document.getElementById(`building-block-${safeBlockId}`);
      if (blk) {
        blk.classList.add('block-has-active');
        const s = blk.querySelector('.building-shell');
        if (s) {
          s.setAttribute('stroke', '#f59e0b');
          s.setAttribute('stroke-width', '2.5');
        }
      }
    }
  }

  // --- 7. TOOLTIP SYSTEM ---
  function showPlotTooltip(e, p) {
    const gate1 = Object.keys(nodes).find(n => n.includes('main') || n === 'gate_1') || Object.keys(nodes)[0];
    const curb = findBestCurbPoint(p, edges, nodes);
    const routeG1 = gate1 ? (curb ? findShortestPathToCurb(gate1, curb) : findShortestPath(gate1, p.roadNode)) : null;
    const distG1 = routeG1 ? Math.round((routeG1.totalDist + (curb ? curb.dist : 15)) * 0.95) : '~180';
    const gateLabel = nodes[gate1]?.label ? nodes[gate1].label.split(' (')[0] : 'Entrance Gate';
    const uLabel = currentLayout.unitType || 'Unit';
    const isApt = isApartmentOrBlockLayout(currentLayout);
    const titleText = isApt ? `🏢 ${cleanBlockTitle(p.block || p.number)}` : `${uLabel} #${p.number}`;
    const blockLabel = isApt ? cleanBlockTitle(p.block) : p.block;

    tooltip.innerHTML = `
      <div style="font-weight:800;font-size:13px;color:#38bdf8;margin-bottom:2px;">${titleText}</div>
      <div style="font-size:11px;color:#cbd5e1;">Road: <strong>${p.road}</strong></div>
      <div style="font-size:11px;color:#cbd5e1;">Sector: ${blockLabel} (${p.facing}-facing)</div>
      <div style="font-size:10px;color:#10b981;margin-top:4px;">📍 ${distG1}m from ${gateLabel}</div>
      <div style="font-size:10px;color:#f59e0b;margin-top:4px;font-weight:700;">👉 Hold button or plot to explore inside</div>
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
          const ptX = Math.round(svgP.x);
          const ptY = Math.round(svgP.y);
          state.userLocation = { mapX: ptX, mapY: ptY, accuracy: 10 };
          updateUserLocationMarker(ptX, ptY, 10);
          showToast("📍 Live location moved to selected point!", 2000);
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

    // On mobile, keep comfortable overview scale so user can see route & surroundings
    const finalScale = isMobile ? Math.min(Math.max(targetScale, 1.2), 1.55) : targetScale;

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
        alert("Please select a house/plot first to generate a shareable delivery link!");
        return;
      }
      const plot = plots[state.selectedPlotId];
      const plotNum = plot ? (plot.number || state.selectedPlotId) : state.selectedPlotId;
      const shareUrl = new URL(window.location.origin + window.location.pathname);
      shareUrl.searchParams.set('map', currentLayoutId);
      shareUrl.searchParams.set('plot', plotNum);
      if (state.startNodeId) {
        const gateVal = state.startNodeId === 'gate_2' ? '2' : (state.startNodeId === 'gate_1' ? '1' : state.startNodeId);
        shareUrl.searchParams.set('gate', gateVal);
      }
      navigator.clipboard.writeText(shareUrl.toString()).then(() => {
        const btn = document.getElementById('share-link-btn');
        const origText = btn.innerHTML;
        btn.innerHTML = `✓ Copied Link!`;
        setTimeout(() => { btn.innerHTML = origText; }, 2500);
      });
      if (window.HimagiriAnalytics) {
        window.HimagiriAnalytics.trackShare(plotNum, 'link');
      }
    });

    // Native Android Web Share API (WhatsApp / Maps / Messages)
    const nativeShareBtn = document.getElementById('share-native-btn');
    if (nativeShareBtn) {
      nativeShareBtn.addEventListener('click', async () => {
        if (!state.selectedPlotId) {
          alert("Please select a house/plot first to share directions!");
          return;
        }
        const plot = plots[state.selectedPlotId];
        const plotNum = plot ? (plot.number || state.selectedPlotId) : state.selectedPlotId;
        const layoutName = (currentLayout && currentLayout.name) ? currentLayout.name : 'Community Map';
        const unitLabel = (currentLayout && currentLayout.unitType) ? currentLayout.unitType : 'House / Plot';
        const gateLabel = (nodes && nodes[state.startNodeId]) ? nodes[state.startNodeId].label.split(' (')[0] : (state.startNodeId === 'gate_2' ? 'Gate 2' : 'Gate 1');
        
        const shareUrl = new URL(window.location.origin + window.location.pathname);
        shareUrl.searchParams.set('map', currentLayoutId);
        shareUrl.searchParams.set('plot', plotNum);
        if (state.startNodeId) {
          const gateVal = state.startNodeId === 'gate_2' ? '2' : (state.startNodeId === 'gate_1' ? '1' : state.startNodeId);
          shareUrl.searchParams.set('gate', gateVal);
        }

        const roadInfo = plot.road ? ` (${plot.road})` : '';
        const shareTitle = `Directions to ${unitLabel} #${plotNum} — ${layoutName}`;
        const shareText = `Here are the directions to ${unitLabel} #${plotNum}${roadInfo} from ${gateLabel} in ${layoutName}:\n${shareUrl.toString()}`;

        if (window.HimagiriAnalytics) {
          window.HimagiriAnalytics.trackShare(plotNum, 'whatsapp_native');
        }

        if (navigator.share) {
          try {
            await navigator.share({
              title: shareTitle,
              text: shareText,
              url: shareUrl.toString()
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
    const viewOrigBtn = document.getElementById('view-original-btn');
    if (viewOrigBtn) viewOrigBtn.addEventListener('click', () => {
      originalModal.classList.add('active');
    });

    document.getElementById('close-modal-btn').addEventListener('click', () => {
      originalModal.classList.remove('active');
    });

    originalModal.addEventListener('click', (e) => {
      if (e.target === originalModal) originalModal.classList.remove('active');
    });

    // Direct Track to House Doorstep Button
    const trackHouseBtn = document.getElementById('card-track-house-btn');
    if (trackHouseBtn) {
      trackHouseBtn.addEventListener('click', () => {
        if (!state.selectedPlotId || !plots[state.selectedPlotId]) {
          showToast("Please choose a house, flat, or building on the map first.", 2500);
          return;
        }
        const p = plots[state.selectedPlotId];
        const isApt = isApartmentOrBlockLayout(currentLayout);
        const name = (isApt && p.number) ? p.number : `Plot #${p.number}`;
        startLocationTracking(true);
        calculateAndDisplayRoute('my_location', state.selectedPlotId);
        showToast(`📍 Live tracking to ${name} doorstep active!`, 3000);
      });
    }

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

    // Register Service Worker for Complete Offline PWA (Zero Wi-Fi Required)
    if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js?v=25').then((reg) => {
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
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'OFFLINE_READY') {
          showToast('⚡ HM Maps is offline-ready! No Wi-Fi required.', 3500);
        }
      });
    }

    // Dynamic Online / Offline status badge tracking
    function updateOnlineStatus() {
      const badge = document.getElementById('offline-badge');
      const badgeText = document.getElementById('offline-badge-text');
      if (!badge || !badgeText) return;
      if (navigator.onLine) {
        badge.classList.remove('offline-active');
        badgeText.textContent = '⚡ Offline Ready';
        badge.title = 'All 59+ layouts cached. Works without Wi-Fi!';
      } else {
        badge.classList.add('offline-active');
        badgeText.textContent = '⚡ Offline (No Wi-Fi)';
        badge.title = 'Running in offline mode without Wi-Fi';
        showToast('⚡ Running in Offline Mode. All 59+ maps available without Wi-Fi!', 3000);
      }
    }
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus();

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

    // Portal Hero Layout Search & Quick Jump Suggestions
    const heroLayoutSearch = document.getElementById('portal-layout-search-input');
    const heroSearchClear = document.getElementById('portal-search-clear-btn');
    const searchDropdown = document.getElementById('portal-search-results');

    function renderHeroSearchResults(query) {
      if (!searchDropdown) return;
      const q = (query || '').toLowerCase().trim();
      if (!q) {
        searchDropdown.style.display = 'none';
        searchDropdown.innerHTML = '';
        return;
      }

      const matches = Object.values(layouts).filter(lay => {
        return (lay.name && lay.name.toLowerCase().includes(q)) ||
               (lay.location && lay.location.toLowerCase().includes(q)) ||
               (lay.zone && lay.zone.toLowerCase().includes(q)) ||
               (lay.type && lay.type.toLowerCase().includes(q));
      }).slice(0, 8);

      if (matches.length === 0) {
        searchDropdown.style.display = 'block';
        searchDropdown.innerHTML = `
          <div style="padding: 16px; text-align: center; color: #94a3b8; font-size: 13px;">
            No blueprints matching "<strong>${escapeHtml(query)}</strong>" found.
          </div>
        `;
        return;
      }

      let html = '';
      matches.forEach(m => {
        let icon = '🏢';
        const lowerType = (m.type || '').toLowerCase();
        const lowerUnit = (m.unitType || '').toLowerCase();

        if (lowerType.includes('gated plotted') || m.id === 'himagiri' || m.id === 'classic_orchards' || m.id === 'rainbow_drive') {
          icon = '🏡';
        } else if (lowerUnit.includes('villa') || lowerType.includes('villa')) {
          icon = '🌴';
        } else if (lowerUnit.includes('flat') || lowerType.includes('flat')) {
          icon = '🏢';
        } else {
          icon = '🏙️';
        }

        const unitCount = m.unitCount || (m.plots ? Object.keys(m.plots).length : 0);
        const unitLabel = `${unitCount} ${m.unitType || 'Units'}`;
        html += `
          <div class="portal-search-item" data-layout-id="${m.id}">
            <div class="portal-search-item-info">
              <span class="portal-search-item-title">${icon} ${escapeHtml(m.name)}</span>
              <span class="portal-search-item-sub">📍 ${escapeHtml(m.location || '')} &bull; <strong style="color: #38bdf8;">${escapeHtml(m.type || '')}</strong> &bull; ${unitLabel}</span>
            </div>
            <span class="portal-search-item-action">Open Map ➔</span>
          </div>
        `;
      });
      searchDropdown.innerHTML = html;
      searchDropdown.style.display = 'flex';

      searchDropdown.querySelectorAll('.portal-search-item').forEach(item => {
        item.addEventListener('click', () => {
          const lid = item.getAttribute('data-layout-id');
          if (lid) {
            searchDropdown.style.display = 'none';
            if (heroLayoutSearch) heroLayoutSearch.value = '';
            if (heroSearchClear) heroSearchClear.style.display = 'none';
            loadLayout(lid);
          }
        });
      });
    }

    if (heroLayoutSearch) {
      heroLayoutSearch.addEventListener('input', (e) => {
        const val = e.target.value;
        if (heroSearchClear) heroSearchClear.style.display = val ? 'block' : 'none';
        renderHeroSearchResults(val);
      });
      heroLayoutSearch.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const val = heroLayoutSearch.value.trim().toLowerCase();
          const match = Object.values(layouts).find(l => l.name.toLowerCase().includes(val) || l.id.toLowerCase().includes(val));
          if (match) {
            if (searchDropdown) searchDropdown.style.display = 'none';
            heroLayoutSearch.value = '';
            if (heroSearchClear) heroSearchClear.style.display = 'none';
            loadLayout(match.id);
          }
        } else if (e.key === 'Escape') {
          if (searchDropdown) searchDropdown.style.display = 'none';
        }
      });
    }

    if (heroSearchClear) {
      heroSearchClear.addEventListener('click', () => {
        if (heroLayoutSearch) {
          heroLayoutSearch.value = '';
          heroLayoutSearch.focus();
        }
        heroSearchClear.style.display = 'none';
        renderHeroSearchResults('');
      });
    }

    document.addEventListener('click', (e) => {
      if (searchDropdown && !e.target.closest('.portal-ai-card')) {
        searchDropdown.style.display = 'none';
      }
    });

    // Portal Quick Jump Chips
    document.querySelectorAll('.portal-chip[data-layout]').forEach(chip => {
      chip.addEventListener('click', () => {
        const lid = chip.getAttribute('data-layout');
        if (lid) loadLayout(lid);
      });
    });

    // Sample preview buttons
    document.querySelectorAll('.btn-preview-sample, .btn-demo-card').forEach(btn => {
      btn.addEventListener('click', () => {
        const name = btn.getAttribute('data-name') || 'This layout';
        showToast(`${name} is a sample preview. Explore any verified layout for full live navigation! 🗺️`, 3500);
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
      document.querySelectorAll('.svg-plot, .svg-building-block').forEach(p => p.style.opacity = '1');
      fitMapToView();
      return;
    }

    if (isApartmentOrBlockLayout(currentLayout)) {
      const allPlots = Object.values(plots);
      const matchPlot = allPlots.find(p => p.block && (p.block.toLowerCase().includes(sector.toLowerCase()) || sector.toLowerCase().includes(p.block.toLowerCase())));
      if (matchPlot) {
        selectPlot(matchPlot.id, true);
        return;
      }
    }

    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    let found = false;

    document.querySelectorAll('.svg-plot').forEach(el => {
      const pid = el.getAttribute('data-id');
      const plot = plots[pid];
      if (plot && (plot.road.toLowerCase().includes(sector.toLowerCase()) || (plot.block && plot.block.toLowerCase().includes(sector.toLowerCase())))) {
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

    document.querySelectorAll('.svg-building-block').forEach(el => {
      const b = el.getAttribute('data-block') || '';
      if (b.toLowerCase().includes(sector.toLowerCase()) || sector.toLowerCase().includes(b.toLowerCase())) {
        el.style.opacity = '1';
      } else {
        el.style.opacity = '0.3';
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
          <button id="reset-directory-search-btn" class="btn btn-secondary" style="margin-top: 16px;">View All 32 Verified Blueprints</button>
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
      if (lay.id === 'prestige_falcon_city') {
        desc = "Iconic 7-tower residential township on Kanakapura Road, connected to Forum Falcon City Mall & Konanakunte Cross Metro, with Olympic pool, tennis arena, and central amphitheatre.";
      } else if (lay.id === 'prestige_elysian') {
        desc = "Luxury high-rise residential community on Bannerghatta Main Road (opposite Meenakshi Mall), featuring Aurum, Argent, Cuprum & Platin towers, infinity pool, and Zen gardens.";
      } else if (lay.id === 'kristal_beryl') {
        desc = "Gated residential apartment enclave in Kasavanahalli (Sarjapur Road vicinity) with 5 residential blocks (A to E), central swimming pool, gymnasium, and play areas.";
      } else if (lay.id === 'sattva_greenage') {
        desc = "50-acre integrated gated community on Hosur Main Road with 10 residential towers (Alpine to Jasmine), 60,000 sq ft Clayey Park clubhouse, 4 pools, and sports arena.";
      } else if (lay.id === 'sobha_dream_acres') {
        desc = "Massive precast residential township in Panathur/Balagere with Rainforest, Coral, Palm & Spring wings, 5 clubhouses, lap pools, and sports courts.";
      } else if (lay.id === 'prestige_song_south') {
        desc = "Premier 17-tower high-rise township off Bannerghatta Road / Begur with Symphony clubhouse, natural lake promenade, and sports arenas.";
      } else if (lay.id === 'brigade_millennium') {
        desc = "Landmark integrated residential campus in JP Nagar 7th Phase with Cassia, Jacaranda, Laburnum, Magnolia & Mayflower towers, The Woodrose Club, and MLR Convention Centre.";
      } else if (lay.id === 'purva_westend') {
        desc = "Cinema-themed luxury high-rise community at Kudlu Gate (Hosur Main Road) featuring Broadway and Opera towers, open-air cinema amphitheatre, and resort wave pool.";
      } else if (lay.id === 'himagiri') {
        desc = "Premium 344-plot gated community with 8 tree-lined avenues, dual security gates, West & Central temples, children's park, and auditorium.";
      } else {
        desc = `${lay.type || 'Verified residential layout'} featuring ${uCount} ${uType.toLowerCase()}s, ${amenCount} community amenities, and verified turn-by-turn routing.`;
      }

      cardsHtml += `
        <div class="community-card active-card" data-layout-id="${lay.id}">
          <div class="card-badge live-badge">✓ Verified Blueprint</div>
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
            <button class="btn btn-primary btn-open-card-map" data-layout-id="${lay.id}" style="width: 100%;">
              🗺️ Explore Layout & Navigator
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
          Have a physical layout board or blueprint photo? Turn it into a smart, GPS-enabled digital map with turn-by-turn wayfinding for your residents and delivery visitors.
        </p>
        <div class="community-tags">
          <span class="tag">⚡ 24hr Digitization</span>
          <span class="tag">🧭 Live Wayfinding</span>
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
    if (brandSub) brandSub.textContent = 'Bangalore Layout Navigator & Directory';
    if (brandIcon) brandIcon.textContent = '🌐';

    document.title = 'HM Maps — Bangalore Layouts, Townships & Plot Navigator';
    try {
      const url = new URL(window.location.href);
      url.searchParams.delete('map');
      url.searchParams.delete('layout');
      url.searchParams.delete('house');
      url.searchParams.delete('plot');
      url.searchParams.delete('gate');
      window.history.replaceState({}, '', url.pathname + (url.search ? url.search : ''));
    } catch (_) {}

    renderPortalDirectory(currentDirectoryZone, currentDirectorySearch);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showMapView(communityId = null, targetPlot = null) {
    const targetId = communityId || currentLayoutId || (('prestige_falcon_city' in layouts) ? 'prestige_falcon_city' : Object.keys(layouts)[0]);
    if (targetId && (currentLayoutId !== targetId || !currentLayout) && layouts[targetId]) {
      loadLayout(targetId, targetPlot);
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

  // Safe helper stub for legacy or external callers
  const aiAssistant = {
    state: 'IDLE',
    chosenLayoutId: null,
    pendingUnitNumber: null,
    isOpen: false,
    open(q) {
      if (q && layouts[q]) loadLayout(q);
    },
    openForLayout(lid) {
      if (lid && layouts[lid]) loadLayout(lid);
    },
    close() {},
    reset() {},
    setTyping() {},
    scrollToBottom() {},
    addAiMessage() {},
    addUserMessage() {},
    handleUserQuery(query) {
      if (!query) return;
      const q = query.toLowerCase().trim();
      const match = Object.values(layouts).find(l => l.name.toLowerCase().includes(q) || l.id.toLowerCase().includes(q));
      if (match) loadLayout(match.id);
    },
    processQuery() {}
  };

  // Check URL parameters for direct delivery link sharing
  function checkUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const houseNum = params.get('plot') || params.get('house') || params.get('villa') || params.get('unit');
    const gateNum = params.get('gate');
    const mapParam = params.get('map') || params.get('layout');

    if (gateNum) {
      const gateKey = gateNum === '2' ? 'gate_2' : (gateNum === '1' ? 'gate_1' : gateNum);
      state.startNodeId = gateKey;
      if (startSelect) startSelect.value = gateKey;
    }

    if (mapParam) {
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
