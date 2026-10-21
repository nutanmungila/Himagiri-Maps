/**
 * Himagiri Meadows Layout Navigator & Interactive Vector Map
 * Complete Wayfinding, Turn-by-Turn Directions, Voice & Conversational Assistant
 */

(function () {
  'use strict';

  // Check data availability
  if (!window.HIMAGIRI_DATA) {
    console.error("Himagiri map data not found!");
    return;
  }

  const { plots, nodes, edges, amenities } = window.HIMAGIRI_DATA;

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

  // Pre-build Graph Adjacency List for Dijkstra
  const graph = {};
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

  // --- 1. RENDER SVG MAP ---
  function initMap() {
    renderPerimeterAndLandscaping();
    renderRoads();
    renderPlots();
    renderAmenities();
    populateSelectDropdowns();
    setupPanZoom();
    fitMapToView();
    checkUrlParams();
  }

  // Landscaping & Perimeter
  function renderPerimeterAndLandscaping() {
    const bgGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    bgGroup.setAttribute("id", "landscaping-layer");

    // Outer layout ground polygon
    const ground = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    // Outer perimeter boundary coordinates matching layout board
    ground.setAttribute("points", "40,320 80,180 300,160 850,140 1050,140 1260,170 1250,600 1150,620 950,830 800,900 500,890 280,880 30,830 30,620");
    ground.setAttribute("fill", "#f8fafc");
    ground.setAttribute("stroke", "#94a3b8");
    ground.setAttribute("stroke-width", "2");
    ground.setAttribute("stroke-dasharray", "6,4");
    bgGroup.appendChild(ground);

    // Landscaped perimeter tree border
    const borderTrees = document.createElementNS("http://www.w3.org/2000/svg", "path");
    borderTrees.setAttribute("d", "M 40,320 Q 150,160 300,160 T 850,140 T 1050,140 T 1260,170 L 1250,600 L 1150,620 L 950,830 L 800,900 L 500,890 L 280,880 L 30,830 Z");
    borderTrees.setAttribute("fill", "none");
    borderTrees.setAttribute("stroke", "#86efac");
    borderTrees.setAttribute("stroke-width", "12");
    borderTrees.setAttribute("stroke-linecap", "round");
    borderTrees.setAttribute("stroke-linejoin", "round");
    borderTrees.setAttribute("opacity", "0.6");
    bgGroup.appendChild(borderTrees);

    // Central Garden Park Area polygon
    const gardenPark = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    gardenPark.setAttribute("x", "440");
    gardenPark.setAttribute("y", "625");
    gardenPark.setAttribute("width", "370");
    gardenPark.setAttribute("height", "45");
    gardenPark.setAttribute("rx", "6");
    gardenPark.setAttribute("fill", "#bbf7d0");
    gardenPark.setAttribute("stroke", "#4ade80");
    gardenPark.setAttribute("stroke-width", "1.5");
    bgGroup.appendChild(gardenPark);

    // Children Play Area polygon
    const playArea = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    playArea.setAttribute("x", "250");
    playArea.setAttribute("y", "625");
    playArea.setAttribute("width", "180");
    playArea.setAttribute("height", "45");
    playArea.setAttribute("rx", "6");
    playArea.setAttribute("fill", "#dcfce7");
    playArea.setAttribute("stroke", "#86efac");
    playArea.setAttribute("stroke-width", "1.5");
    bgGroup.appendChild(playArea);

    viewport.insertBefore(bgGroup, viewport.firstChild);
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
      roadPath.setAttribute("stroke", "#27272a");
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

    // Road Labels
    const roadLabels = [
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
    ];

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

      const fillColor = p.color === 'lightgreen' ? '#bbf7d0' : (p.color === 'lightyellow' ? '#fef9c3' : '#fef08a');
      const strokeColor = p.color === 'lightgreen' ? '#16a34a' : '#ca8a04';

      rect.setAttribute("fill", fillColor);
      rect.setAttribute("stroke", strokeColor);

      // Plot number text
      const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
      txt.setAttribute("class", "plot-label");
      txt.setAttribute("x", p.x + p.w / 2);
      txt.setAttribute("y", p.y + p.h / 2);

      // Adjust font size for longer plot numbers like "35/36" or "265/B"
      if (p.number.length >= 5) {
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

  // Render Amenities (Gate 1, Gate 2, Temple, Play Area, etc.)
  function renderAmenities() {
    amenitiesLayer.innerHTML = '';

    for (const am of amenities) {
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "amenity-pin");
      g.setAttribute("id", `amenity-${am.id}`);
      g.setAttribute("cursor", "pointer");

      // Outer circle badge
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", am.x);
      circle.setAttribute("cy", am.y);
      circle.setAttribute("r", am.type === 'gate' ? "15" : "12");

      let bgColor = "#0284c7";
      if (am.type === 'gate') bgColor = "#059669";
      if (am.type === 'worship') bgColor = "#d97706";
      if (am.type === 'recreation') bgColor = "#16a34a";
      if (am.type === 'civic') bgColor = "#7c3aed";
      if (am.type === 'utility') bgColor = "#475569";

      circle.setAttribute("fill", bgColor);
      circle.setAttribute("stroke", "#ffffff");
      circle.setAttribute("stroke-width", "2");
      circle.setAttribute("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.3))");

      // Label text
      const iconTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
      iconTxt.setAttribute("x", am.x);
      iconTxt.setAttribute("y", am.y);
      iconTxt.setAttribute("text-anchor", "middle");
      iconTxt.setAttribute("dominant-baseline", "central");
      iconTxt.setAttribute("fill", "#ffffff");
      iconTxt.setAttribute("font-size", am.type === 'gate' ? "10px" : "8.5px");
      iconTxt.setAttribute("font-weight", "800");

      if (am.id === 'gate_1') iconTxt.textContent = "G1";
      else if (am.id === 'gate_2') iconTxt.textContent = "G2";
      else if (am.type === 'worship') iconTxt.textContent = "🛕";
      else if (am.type === 'recreation') iconTxt.textContent = "🌳";
      else if (am.id === 'school_bus_stop') iconTxt.textContent = "🚌";
      else if (am.id === 'auditorium') iconTxt.textContent = "🏛️";
      else if (am.id === 'atm') iconTxt.textContent = "💳";
      else iconTxt.textContent = "★";

      // Text Title underneath
      const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
      title.setAttribute("x", am.x);
      title.setAttribute("y", am.y + (am.type === 'gate' ? 24 : 20));
      title.setAttribute("text-anchor", "middle");
      title.setAttribute("fill", "#0f172a");
      title.setAttribute("font-size", "10px");
      title.setAttribute("font-weight", "700");
      title.setAttribute("filter", "drop-shadow(0 1px 2px rgba(255,255,255,0.9))");
      title.textContent = am.name.split(' (')[0];

      g.appendChild(circle);
      g.appendChild(iconTxt);
      g.appendChild(title);

      g.addEventListener('click', () => {
        selectAmenity(am.id, true);
      });
      g.addEventListener('mouseenter', (e) => {
        tooltip.innerHTML = `<strong>${am.name}</strong><br><span style="color:#94a3b8;font-size:11px;">${am.description}</span>`;
        tooltip.style.display = 'block';
        movePlotTooltip(e);
      });
      g.addEventListener('mousemove', movePlotTooltip);
      g.addEventListener('mouseleave', hidePlotTooltip);

      amenitiesLayer.appendChild(g);
    }
  }

  // Populate Start & Destination Dropdowns
  function populateSelectDropdowns() {
    startSelect.innerHTML = `
      <optgroup label="📍 Your Position">
        <option value="my_location">📍 My Live Location (GPS)</option>
      </optgroup>
      <optgroup label="Main Gates">
        <option value="gate_1" selected>Gate 1 (Main West Entrance)</option>
        <option value="gate_2">Gate 2 (East Entrance)</option>
      </optgroup>
      <optgroup label="Key Landmarks">
        <option value="ast_main">School Bus Stop</option>
        <option value="blu_s">Children's Play Area</option>
        <option value="dha_garden">Central Garden Area</option>
        <option value="car_garden">Community Auditorium</option>
        <option value="exo_garden">Central Temple</option>
      </optgroup>
    `;

    // Destination selector with all plots & amenities
    destSelect.innerHTML = `<option value="">-- Choose House or Landmark --</option>`;

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
        return na - nb;
      });
      for (const p of roads[roadName]) {
        const opt = document.createElement('option');
        opt.value = `plot:${p.id}`;
        opt.textContent = `House #${p.number} (${p.road})`;
        grp.appendChild(opt);
      }
      destSelect.appendChild(grp);
    }

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
    if (text.includes("gate 2") || text.includes("gate2")) {
      detectedStart = "gate_2";
      startSelect.value = "gate_2";
      state.startNodeId = "gate_2";
    } else if (text.includes("gate 1") || text.includes("gate1")) {
      detectedStart = "gate_1";
      startSelect.value = "gate_1";
      state.startNodeId = "gate_1";
    }

    // Check for Landmarks first
    const landmarkKeywords = [
      { key: "play area", id: "children_play_area" },
      { key: "children", id: "children_play_area" },
      { key: "garden", id: "garden_area" },
      { key: "temple", id: "temple_garden" },
      { key: "auditorium", id: "auditorium" },
      { key: "shopping", id: "shopping_complex" },
      { key: "complex", id: "shopping_complex" },
      { key: "bus stop", id: "school_bus_stop" },
      { key: "bus stand", id: "school_bus_stop" },
      { key: "wtp", id: "wtp_sump" },
      { key: "sump", id: "wtp_sump" },
      { key: "water plant", id: "wtp_sump" },
      { key: "stp", id: "stp_plant" },
      { key: "atm", id: "atm" },
      { key: "waste", id: "dry_waste" },
      { key: "gate 1", id: "gate_1" },
      { key: "gate 2", id: "gate_2" }
    ];

    for (const lmk of landmarkKeywords) {
      if (text.includes(lmk.key) && !text.includes("house") && !text.includes("plot")) {
        selectAmenity(lmk.id, true);
        const am = amenities.find(a => a.id === lmk.id);
        const resp = `${am.name} is located at ${am.description} Click 'Directions' to view the quickest path from ${nodes[detectedStart].label}.`;
        displayAssistantResponse(resp);
        speakText(resp);
        return;
      }
    }

    // Extract plot number
    // Handle formats: "142", "house 142", "plot #85", "no. 265/B", "35/36", "1C"
    let matchedPlot = null;

    // Direct match against known plots
    for (const pid in plots) {
      const pNum = plots[pid].number.toLowerCase();
      // Match whole word or exact pattern
      const regex = new RegExp(`(?:^|[\\s#,#])(${pNum.replace('/', '\\/')})(?:[\\s,\\?!]|$)`, 'i');
      if (regex.test(text)) {
        matchedPlot = plots[pid];
        break;
      }
    }

    // If still not matched, extract any digit sequence
    if (!matchedPlot) {
      const numMatch = text.match(/\b([0-9]{1,3}(?:\/[a-zA-Z0-9]+|[a-zA-Z])?)\b/);
      if (numMatch && plots[numMatch[1]]) {
        matchedPlot = plots[numMatch[1]];
      }
    }

    if (matchedPlot) {
      selectPlot(matchedPlot.id, true);
      const startName = nodes[detectedStart]?.label.split(' (')[0];
      const resp = `House #${matchedPlot.number} is on ${matchedPlot.road} in ${matchedPlot.block}. I have highlighted its exact location on the digital map and plotted your turn-by-turn directions from ${startName}!`;
      displayAssistantResponse(resp);
      speakText(resp);
    } else {
      const notFound = `I couldn't find a house matching "${queryText}". Himagiri Meadows has plots numbered 1 through 360 across Aster, Bluebell, Carnation, Dhalia, Exotica, Florentine, Gardenia, and Hibiscus. Try asking "Where is house 142?" or "Take me to plot 85".`;
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
    document.getElementById('card-house-num').textContent = `#${plot.number}`;
    document.getElementById('card-road').textContent = plot.road;
    document.getElementById('card-block').textContent = plot.block;
    document.getElementById('card-facing').textContent = `${plot.facing} Facing`;

    // Distances from Gate 1 & Gate 2
    const routeG1 = findShortestPath('gate_1', plot.roadNode);
    const distG1 = routeG1 ? Math.round(routeG1.totalDist * 0.95) : '--';
    document.getElementById('card-dist-g1').textContent = `${distG1}m`;

    const routeG2 = findShortestPath('gate_2', plot.roadNode);
    const distG2 = routeG2 ? Math.round(routeG2.totalDist * 0.95) : '--';
    document.getElementById('card-dist-g2').textContent = `${distG2}m`;

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
    const route = findShortestPath(state.startNodeId, am.roadNode);
    if (route) {
      state.activeRoute = route;
      const points = [];
      for (const nid of route.nodes) {
        const n = nodes[nid];
        points.push(`${n.x},${n.y}`);
      }
      points.push(`${am.x},${am.y}`);
      const pathData = "M " + points.join(" L ");

      routeLayer.innerHTML = `
        <path d="${pathData}" class="nav-route-underlay" />
        <path id="active-nav-path" d="${pathData}" class="nav-route-path" />
        <circle cx="${nodes[state.startNodeId].x}" cy="${nodes[state.startNodeId].y}" r="8" fill="#10b981" stroke="#ffffff" stroke-width="2.5" />
        <circle cx="${am.x}" cy="${am.y}" r="12" fill="#ef4444" stroke="#ffffff" stroke-width="2" />
        <circle id="route-traveler" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="2" />
      `;

      startRouteTravelerAnimation();

      const totalDist = Math.round(route.totalDist * 0.95);
      const walkMins = Math.max(1, Math.round(totalDist / 70));
      distanceVal.textContent = `${totalDist} m`;
      walkTimeVal.textContent = `${walkMins} min`;
      driveTimeVal.textContent = `1 min`;

      const steps = generateTurnByTurnDirections(route, null, state.startNodeId);
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
    const routeG1 = findShortestPath('gate_1', p.roadNode);
    const distG1 = routeG1 ? Math.round(routeG1.totalDist * 0.95) : '~180';

    tooltip.innerHTML = `
      <div style="font-weight:800;font-size:13px;color:#38bdf8;margin-bottom:2px;">House #${p.number}</div>
      <div style="font-size:11px;color:#cbd5e1;">Road: <strong>${p.road}</strong></div>
      <div style="font-size:11px;color:#cbd5e1;">Sector: ${p.block} (${p.facing}-facing)</div>
      <div style="font-size:10px;color:#10b981;margin-top:4px;">📍 ${distG1}m from Gate 1</div>
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
      zoomToCoordinates(80, 336, isMobile ? 2.0 : 1.8);
    });

    const focusCenterBtn = document.getElementById('focus-center-btn');
    if (focusCenterBtn) {
      focusCenterBtn.addEventListener('click', () => {
        const isMobile = window.innerWidth <= 900;
        // Center directly on Children's Play Area & Central Garden/Temple precinct
        zoomToCoordinates(320, 650, isMobile ? 1.85 : 1.6);
        showToast("Centered on Children's Play Area & Temple 🛝🛕", 3000);
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
      zoomToCoordinates(940, 336, isMobile ? 2.0 : 1.8);
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

    // Full layout bounds (matching perimeter border, Gate 1, Gate 2, all plots and roads)
    const contentMinX = 20;
    const contentMaxX = 1270;
    const contentWidth = contentMaxX - contentMinX; // 1250
    const centerX = 645; // (20 + 1270) / 2

    const contentMinY = 135;
    const contentMaxY = 935;
    const contentHeight = contentMaxY - contentMinY; // 800
    const centerY = 535; // (135 + 935) / 2

    // Comfortable padding inside the viewport
    const padX = isMobile ? 10 : 28;
    const padY = isMobile ? 10 : 20;

    const availWidth = Math.max(rect.width - padX * 2, 80);
    const availHeight = Math.max(rect.height - padY * 2, 80);

    const fitScale = Math.min(availWidth / contentWidth, availHeight / contentHeight);

    state.transform.scale = fitScale;
    state.transform.x = rect.width / 2 - centerX * fitScale;
    state.transform.y = rect.height / 2 - centerY * fitScale;

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
        navigator.serviceWorker.register('sw.js?v=7').then((reg) => {
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

  // Check URL parameters for direct delivery link sharing
  function checkUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const houseNum = params.get('house') || params.get('plot');
    const gateNum = params.get('gate');

    if (gateNum === '2') {
      state.startNodeId = 'gate_2';
      startSelect.value = 'gate_2';
    }

    if (houseNum) {
      parseAndAnswerQuery(`Where is house ${houseNum}`);
    }
  }

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    initMap();
    setupEventListeners();
  });

})();
