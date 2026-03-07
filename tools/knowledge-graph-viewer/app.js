const MANIFEST_URL = '../../data/knowledge-graph/manifest.json';
const DATASET_BASE = '../../data/knowledge-graph/';
const REPO_BASE = '../../';
const STORAGE_KEY = 'studio-system-knowledge-graph';

const state = {
  manifest: null,
  datasets: new Map(),
  currentView: null,
  dataset: null,
  index: null,
  snapshot: null,
  search: '',
  selectedNodeTypes: new Set(),
  selectedRelations: new Set(),
  focusedNodeId: null,
  hoveredNodeId: null,
  focusDepth: 0,
  positions: new Map(),
  simulation: null,
  focusHistory: [],
  pinnedNodes: new Set(loadPreference('pinnedNodes', [])),
  layoutMode: loadPreference('layoutMode', 'force'),
  sizeMode: loadPreference('sizeMode', 'degree'),
  showLabels: loadPreference('showLabels', true),
  glowEnabled: loadPreference('glowEnabled', true),
};

const els = {
  status: document.getElementById('status'),
  tabs: document.getElementById('view-tabs'),
  stats: document.getElementById('graph-stats'),
  description: document.getElementById('view-description'),
  relationBreakdown: document.getElementById('relation-breakdown'),
  selectionSummary: document.getElementById('selection-summary'),
  nodeFilters: document.getElementById('node-type-filters'),
  relationFilters: document.getElementById('relation-filters'),
  hotspotList: document.getElementById('hotspot-list'),
  searchResults: document.getElementById('search-results'),
  historyList: document.getElementById('history-list'),
  inspector: document.getElementById('inspector'),
  canvas: document.getElementById('graph-canvas'),
  title: document.getElementById('view-title'),
  subtitle: document.getElementById('view-subtitle'),
  searchInput: document.getElementById('search-input'),
  clearFocus: document.getElementById('clear-focus'),
  focusNeighbors: document.getElementById('focus-neighbors'),
  focusTwoHops: document.getElementById('focus-two-hops'),
  focusAll: document.getElementById('focus-all'),
  layoutMode: document.getElementById('layout-mode'),
  sizeMode: document.getElementById('size-mode'),
  toggleLabels: document.getElementById('toggle-labels'),
  toggleHalo: document.getElementById('toggle-halo'),
  pinFocused: document.getElementById('pin-focused'),
  exportSvg: document.getElementById('export-svg'),
};

const nodeColor = d3.scaleOrdinal()
  .domain([
    'file',
    'python_function',
    'python_class',
    'python_variable',
    'ts_symbol',
    'ts_variable',
    'node_dependency',
    'python_dependency',
    'environment_variable',
    'collection',
    'unknown',
  ])
  .range([
    '#8dd7ff',
    '#4fd1c5',
    '#74e0ff',
    '#80f5d6',
    '#f6c177',
    '#f5a6e6',
    '#ffb449',
    '#ff7f9d',
    '#c084fc',
    '#9fb8ca',
    '#6d8192',
  ]);

const relationColor = d3.scaleOrdinal()
  .domain([
    'defines',
    'imports',
    'calls',
    'calls_into',
    'uses_component',
    'references',
    'writes',
    'dispatches_to',
    'depends_on',
    'loads',
    'drives',
    'validates_with',
    'uses_env',
    'delegates_to',
    'iterates_over',
    'uses_runtime',
  ])
  .range([
    '#4fd1c5',
    '#8dd7ff',
    '#f6c177',
    '#ff7f9d',
    '#c084fc',
    '#6ee7b7',
    '#f97316',
    '#38bdf8',
    '#f59e0b',
    '#94a3b8',
    '#2dd4bf',
    '#60a5fa',
    '#a78bfa',
    '#34d399',
    '#fb7185',
    '#22c55e',
  ]);

function loadPreference(key, fallback) {
  try {
    const raw = window.localStorage.getItem(`${STORAGE_KEY}:${key}`);
    if (raw === null) return fallback;
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

function savePreference(key, value) {
  try {
    window.localStorage.setItem(`${STORAGE_KEY}:${key}`, JSON.stringify(value));
  } catch {
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function formatNumber(value) {
  return new Intl.NumberFormat().format(value);
}

function setStatus(message, isError = false) {
  els.status.textContent = message;
  els.status.style.color = isError ? 'var(--danger)' : 'var(--muted)';
}

async function fetchJson(url) {
  const response = await fetch(url, {cache: 'no-store'});
  if (!response.ok) {
    throw new Error(`Failed to load ${url}: ${response.status}`);
  }
  return response.json();
}

function labelForNode(node) {
  return node.label || node.path || node.name || node.package || node.env || node.id;
}

function searchableText(node) {
  return [
    node.id,
    node.label,
    node.name,
    node.path,
    node.hint,
    node.package,
    node.env,
    node.module,
    node.value,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();
}

function relationLabel(relation) {
  return state.manifest?.relationTypeLabels?.[relation] || relation;
}

function nodeTypeLabel(type) {
  return state.manifest?.nodeTypeLabels?.[type] || type;
}

function relationSwatch(relation) {
  return relationColor(relation) || '#94a3b8';
}

function edgeNodeId(endpoint) {
  return typeof endpoint === 'string' ? endpoint : endpoint.id;
}

function repoHref(path) {
  return `${REPO_BASE}${path}`;
}

function deriveSourcePath(node) {
  if (node.path) return node.path;
  const incoming = state.index?.incoming.get(node.id) || [];
  for (const edge of incoming) {
    if (edge.relation !== 'defines') continue;
    const sourceNode = state.index.nodesById.get(edge.source);
    if (sourceNode?.path) return sourceNode.path;
  }
  return null;
}

function readHashState() {
  const raw = window.location.hash.replace(/^#/, '');
  const params = new URLSearchParams(raw);
  return {
    view: params.get('view'),
    focus: params.get('focus'),
    depth: params.get('depth') ? Number(params.get('depth')) : 0,
  };
}

function updateHash() {
  const params = new URLSearchParams();
  if (state.currentView?.id) params.set('view', state.currentView.id);
  if (state.focusedNodeId) params.set('focus', state.focusedNodeId);
  if (state.focusDepth) params.set('depth', String(state.focusDepth));
  const next = params.toString();
  const hash = next ? `#${next}` : '';
  if (window.location.hash !== hash) {
    history.replaceState(null, '', hash || window.location.pathname);
  }
}

function buildIndex(dataset) {
  const nodesById = new Map(dataset.nodes.map((node) => [node.id, node]));
  const incoming = new Map();
  const outgoing = new Map();
  const neighbors = new Map();
  const degree = new Map();

  for (const node of dataset.nodes) {
    incoming.set(node.id, []);
    outgoing.set(node.id, []);
    neighbors.set(node.id, new Set());
    degree.set(node.id, 0);
  }

  for (const edge of dataset.edges) {
    if (!incoming.has(edge.target)) incoming.set(edge.target, []);
    if (!outgoing.has(edge.source)) outgoing.set(edge.source, []);
    if (!neighbors.has(edge.source)) neighbors.set(edge.source, new Set());
    if (!neighbors.has(edge.target)) neighbors.set(edge.target, new Set());
    incoming.get(edge.target).push(edge);
    outgoing.get(edge.source).push(edge);
    neighbors.get(edge.source).add(edge.target);
    neighbors.get(edge.target).add(edge.source);
    degree.set(edge.source, (degree.get(edge.source) || 0) + 1);
    degree.set(edge.target, (degree.get(edge.target) || 0) + 1);
  }

  return {nodesById, incoming, outgoing, neighbors, degree};
}

function listAvailableNodeTypes(dataset) {
  const counts = new Map();
  for (const node of dataset.nodes) {
    counts.set(node.type, (counts.get(node.type) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

function listAvailableRelations(dataset) {
  const counts = new Map();
  for (const edge of dataset.edges) {
    counts.set(edge.relation, (counts.get(edge.relation) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

function renderTabs() {
  els.tabs.innerHTML = '';
  for (const view of state.manifest.views) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = view.title;
    button.className = view.id === state.currentView?.id ? 'active' : '';
    button.addEventListener('click', () => loadView(view.id));
    els.tabs.appendChild(button);
  }
}

function renderCheckboxList(container, values, selectedSet, onToggle, labelFn) {
  container.innerHTML = '';
  for (const [value, count] of values) {
    const wrapper = document.createElement('div');
    wrapper.className = 'filter-item';

    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.checked = selectedSet.has(value);
    input.addEventListener('change', () => onToggle(value, input.checked));

    const text = document.createElement('span');
    text.textContent = labelFn(value);

    const countEl = document.createElement('span');
    countEl.className = 'filter-count';
    countEl.textContent = formatNumber(count);

    label.append(input, text);
    wrapper.append(label, countEl);
    container.appendChild(wrapper);
  }
}

function renderFilters() {
  const nodeTypes = listAvailableNodeTypes(state.dataset);
  const relations = listAvailableRelations(state.dataset);

  renderCheckboxList(
    els.nodeFilters,
    nodeTypes,
    state.selectedNodeTypes,
    (value, checked) => {
      checked ? state.selectedNodeTypes.add(value) : state.selectedNodeTypes.delete(value);
      renderDashboard();
    },
    nodeTypeLabel,
  );

  renderCheckboxList(
    els.relationFilters,
    relations,
    state.selectedRelations,
    (value, checked) => {
      checked ? state.selectedRelations.add(value) : state.selectedRelations.delete(value);
      renderDashboard();
    },
    relationLabel,
  );
}

function getSearchMatches(limit = 18) {
  const query = state.search.trim().toLowerCase();
  if (!query) return [];
  return state.dataset.nodes
    .filter((node) => state.selectedNodeTypes.has(node.type))
    .filter((node) => searchableText(node).includes(query))
    .sort((a, b) => labelForNode(a).localeCompare(labelForNode(b)))
    .slice(0, limit);
}

function collectWithinDepth(startId, depth, allowedIds) {
  const seen = new Set([startId]);
  const queue = [{id: startId, depth: 0}];

  while (queue.length) {
    const current = queue.shift();
    if (current.depth >= depth) continue;
    for (const neighbor of state.index.neighbors.get(current.id) || []) {
      if (allowedIds && !allowedIds.has(neighbor)) continue;
      if (seen.has(neighbor)) continue;
      seen.add(neighbor);
      queue.push({id: neighbor, depth: current.depth + 1});
    }
  }

  return seen;
}

function computeVisibleGraph() {
  const nodeTypeIds = new Set(
    state.dataset.nodes
      .filter((node) => state.selectedNodeTypes.has(node.type))
      .map((node) => node.id),
  );

  const searchMatches = getSearchMatches(24);
  let visibleIds = new Set(nodeTypeIds);

  if (searchMatches.length) {
    const expanded = new Set(searchMatches.map((node) => node.id));
    for (const node of searchMatches) {
      for (const neighbor of state.index.neighbors.get(node.id) || []) {
        if (nodeTypeIds.has(neighbor)) {
          expanded.add(neighbor);
        }
      }
    }
    visibleIds = expanded;
  }

  if (state.focusedNodeId && visibleIds.has(state.focusedNodeId) && state.focusDepth > 0) {
    visibleIds = collectWithinDepth(state.focusedNodeId, state.focusDepth, visibleIds);
  }

  const edges = state.dataset.edges.filter(
    (edge) => state.selectedRelations.has(edge.relation)
      && visibleIds.has(edge.source)
      && visibleIds.has(edge.target),
  );

  const nodes = [...visibleIds]
    .map((id) => ({...state.index.nodesById.get(id)}))
    .sort((a, b) => labelForNode(a).localeCompare(labelForNode(b)));

  const visibleDegree = new Map(nodes.map((node) => [node.id, 0]));
  for (const edge of edges) {
    visibleDegree.set(edge.source, (visibleDegree.get(edge.source) || 0) + 1);
    visibleDegree.set(edge.target, (visibleDegree.get(edge.target) || 0) + 1);
  }

  const nodeTypeCounts = new Map();
  for (const node of nodes) {
    nodeTypeCounts.set(node.type, (nodeTypeCounts.get(node.type) || 0) + 1);
  }

  const relationCounts = new Map();
  for (const edge of edges) {
    relationCounts.set(edge.relation, (relationCounts.get(edge.relation) || 0) + 1);
  }

  const averageDegree = nodes.length
    ? [...visibleDegree.values()].reduce((sum, value) => sum + value, 0) / nodes.length
    : 0;

  const density = nodes.length > 1
    ? edges.length / (nodes.length * (nodes.length - 1))
    : 0;

  return {
    nodes,
    edges,
    visibleIds,
    searchMatches,
    visibleDegree,
    nodeTypeCounts,
    relationCounts,
    averageDegree,
    density,
  };
}

function syncPositions(nodes) {
  for (const node of nodes) {
    const stored = state.positions.get(node.id);
    if (stored) {
      node.x = stored.x;
      node.y = stored.y;
      node.vx = 0;
      node.vy = 0;
    }
    if (state.pinnedNodes.has(node.id) && Number.isFinite(node.x) && Number.isFinite(node.y)) {
      node.fx = node.x;
      node.fy = node.y;
    } else {
      node.fx = null;
      node.fy = null;
    }
  }
}

function persistPositions(nodes) {
  for (const node of nodes) {
    if (Number.isFinite(node.x) && Number.isFinite(node.y)) {
      state.positions.set(node.id, {x: node.x, y: node.y});
    }
  }
}

function isPinned(nodeId) {
  return state.pinnedNodes.has(nodeId);
}

function togglePinnedNode(nodeId, explicitState) {
  const shouldPin = explicitState ?? !state.pinnedNodes.has(nodeId);
  if (shouldPin) {
    state.pinnedNodes.add(nodeId);
  } else {
    state.pinnedNodes.delete(nodeId);
  }
  savePreference('pinnedNodes', [...state.pinnedNodes]);
  renderDashboard();
}

function addToHistory(nodeId) {
  if (!nodeId || !state.index?.nodesById.has(nodeId)) return;
  state.focusHistory = [nodeId, ...state.focusHistory.filter((id) => id !== nodeId)].slice(0, 10);
}

function focusNode(nodeId, depth = 1, options = {}) {
  if (!state.index?.nodesById.has(nodeId)) return;
  state.focusedNodeId = nodeId;
  state.hoveredNodeId = null;
  state.focusDepth = depth;
  if (options.pushHistory !== false) {
    addToHistory(nodeId);
  }
  renderDashboard();
}

function resetFocus() {
  state.focusedNodeId = null;
  state.hoveredNodeId = null;
  state.focusDepth = 0;
  renderDashboard();
}

function updateControlState() {
  els.layoutMode.value = state.layoutMode;
  els.sizeMode.value = state.sizeMode;
  els.toggleLabels.textContent = `Labels: ${state.showLabels ? 'On' : 'Off'}`;
  els.toggleHalo.textContent = `Glow: ${state.glowEnabled ? 'On' : 'Off'}`;
  els.toggleLabels.classList.toggle('active-flag', state.showLabels);
  els.toggleHalo.classList.toggle('active-flag', state.glowEnabled);

  const pinActive = state.focusedNodeId && isPinned(state.focusedNodeId);
  els.pinFocused.textContent = state.focusedNodeId ? (pinActive ? 'Unpin Focus' : 'Pin Focus') : 'Pin Focus';
  els.pinFocused.disabled = !state.focusedNodeId;
  els.pinFocused.classList.toggle('active-flag', Boolean(pinActive));
}

function renderStats(snapshot) {
  const visibleNodes = snapshot.nodes.length;
  const visibleEdges = snapshot.edges.length;
  const matchCount = snapshot.searchMatches.length;
  const densityPct = `${(snapshot.density * 100).toFixed(2)}%`;

  els.stats.innerHTML = `
    <h3>View Metrics</h3>
    <div class="metric-grid">
      <div class="metric-tile">
        <div class="metric-label">Visible Nodes</div>
        <div class="metric-value">${formatNumber(visibleNodes)}</div>
        <div class="metric-subvalue">of ${formatNumber(state.dataset.summary.nodeCount)} nodes in this view</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Visible Edges</div>
        <div class="metric-value">${formatNumber(visibleEdges)}</div>
        <div class="metric-subvalue">of ${formatNumber(state.dataset.summary.edgeCount)} edges in this view</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Average Degree</div>
        <div class="metric-value">${snapshot.averageDegree.toFixed(1)}</div>
        <div class="metric-subvalue">local connectivity under current filters</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Search Hits</div>
        <div class="metric-value">${formatNumber(matchCount)}</div>
        <div class="metric-subvalue">density ${densityPct}</div>
      </div>
    </div>
  `;
}

function renderLegend(types) {
  return `
    <div class="legend">
      ${types.map((type) => `
        <div class="legend-item">
          <span class="legend-swatch" style="background:${nodeColor(type)}"></span>
          <span>${escapeHtml(nodeTypeLabel(type))}</span>
        </div>
      `).join('')}
    </div>
  `;
}

function renderViewDescription(snapshot) {
  const types = [...snapshot.nodeTypeCounts.keys()].sort();
  const chips = [
    `Layout: ${state.layoutMode}`,
    `Node Size: ${state.sizeMode}`,
    `Labels ${state.showLabels ? 'enabled' : 'hidden'}`,
    `Glow ${state.glowEnabled ? 'enabled' : 'disabled'}`,
  ];

  els.description.innerHTML = `
    <h3>View Profile</h3>
    <p>${escapeHtml(state.currentView.description)}</p>
    <div class="chip-row">
      ${chips.map((chip) => `<span class="chip">${escapeHtml(chip)}</span>`).join('')}
    </div>
    ${renderLegend(types)}
  `;
}
function renderRelationBreakdown(snapshot) {
  const entries = [...snapshot.relationCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  const max = entries[0]?.[1] || 1;

  els.relationBreakdown.innerHTML = `
    <h3>Relation Heat</h3>
    ${entries.length ? `
      <div class="bar-list">
        ${entries.map(([relation, count]) => `
          <div class="bar-row">
            <div class="bar-row-header">
              <span>${escapeHtml(relationLabel(relation))}</span>
              <span>${formatNumber(count)}</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width:${(count / max) * 100}%; background:linear-gradient(90deg, ${relationSwatch(relation)}, var(--accent-3));"></div>
            </div>
          </div>
        `).join('')}
      </div>
    ` : '<p class="empty">No visible relations under the current filters.</p>'}
  `;
}

function renderSelectionSummary(snapshot) {
  const focusedNode = state.focusedNodeId ? state.index.nodesById.get(state.focusedNodeId) : null;
  const hoveredNode = state.hoveredNodeId ? state.index.nodesById.get(state.hoveredNodeId) : null;

  els.selectionSummary.innerHTML = `
    <h3>Selection State</h3>
    <div class="summary-row">
      <span class="chip">Focus depth ${state.focusDepth || 'all'}</span>
      <span class="chip">Pinned ${formatNumber(state.pinnedNodes.size)}</span>
      <span class="chip">Node filters ${formatNumber(state.selectedNodeTypes.size)}</span>
      <span class="chip">Relation filters ${formatNumber(state.selectedRelations.size)}</span>
    </div>
    <div class="bar-list" style="margin-top:12px;">
      <div class="bar-row">
        <div class="bar-row-header"><span>Focused Node</span><span>${focusedNode ? nodeTypeLabel(focusedNode.type) : 'none'}</span></div>
        <div class="metric-subvalue">${focusedNode ? escapeHtml(labelForNode(focusedNode)) : 'Nothing is currently focused.'}</div>
      </div>
      <div class="bar-row">
        <div class="bar-row-header"><span>Hovered Node</span><span>${hoveredNode ? nodeTypeLabel(hoveredNode.type) : 'none'}</span></div>
        <div class="metric-subvalue">${hoveredNode ? escapeHtml(labelForNode(hoveredNode)) : 'Hover a node to highlight its local structure.'}</div>
      </div>
    </div>
  `;
}

function bindFocusButtons(root) {
  root.querySelectorAll('[data-focus]').forEach((button) => {
    button.addEventListener('click', () => focusNode(button.dataset.focus, 1));
  });
  root.querySelectorAll('[data-depth]').forEach((button) => {
    button.addEventListener('click', () => {
      state.focusDepth = Number(button.dataset.depth);
      renderDashboard();
    });
  });
  root.querySelectorAll('[data-pin-target]').forEach((button) => {
    button.addEventListener('click', () => togglePinnedNode(button.dataset.pinTarget));
  });
}

function renderHotspots(snapshot) {
  const ranked = [...snapshot.nodes]
    .map((node) => ({node, degree: snapshot.visibleDegree.get(node.id) || 0}))
    .sort((a, b) => b.degree - a.degree || labelForNode(a.node).localeCompare(labelForNode(b.node)))
    .slice(0, 10);

  if (!ranked.length) {
    els.hotspotList.innerHTML = '<p class="empty">No visible nodes under the current filters.</p>';
    return;
  }

  els.hotspotList.innerHTML = ranked.map(({node, degree}) => `
    <div class="hotspot-item">
      <div class="hotspot-row">
        <span>${escapeHtml(labelForNode(node))}</span>
        <button type="button" data-focus="${escapeHtml(node.id)}">Focus</button>
      </div>
      <div class="hotspot-meta">${escapeHtml(nodeTypeLabel(node.type))} · degree ${formatNumber(degree)}</div>
    </div>
  `).join('');
  bindFocusButtons(els.hotspotList);
}

function renderSearchResults(snapshot) {
  const matches = snapshot.searchMatches;
  if (!state.search.trim()) {
    els.searchResults.innerHTML = '<p class="empty">No active search.</p>';
    return;
  }
  if (!matches.length) {
    els.searchResults.innerHTML = `<p class="empty">No matches for “${escapeHtml(state.search.trim())}”.</p>`;
    return;
  }

  els.searchResults.innerHTML = matches.map((node) => {
    const sourcePath = deriveSourcePath(node);
    return `
      <div class="result-item">
        <div class="result-head">
          <span>${escapeHtml(labelForNode(node))}</span>
          <button type="button" data-focus="${escapeHtml(node.id)}">Focus</button>
        </div>
        <div class="result-meta">${escapeHtml(nodeTypeLabel(node.type))}</div>
        ${sourcePath ? `<a class="repo-link" href="${repoHref(sourcePath)}" target="_blank" rel="noreferrer">${escapeHtml(sourcePath)}</a>` : ''}
      </div>
    `;
  }).join('');

  bindFocusButtons(els.searchResults);
}

function renderHistory() {
  if (!state.focusHistory.length) {
    els.historyList.innerHTML = '<p class="empty">No focus history yet.</p>';
    return;
  }

  els.historyList.innerHTML = state.focusHistory.map((nodeId, index) => {
    const node = state.index.nodesById.get(nodeId);
    if (!node) return '';
    return `
      <div class="history-item">
        <div class="result-head">
          <span>${escapeHtml(labelForNode(node))}</span>
          <button type="button" data-focus="${escapeHtml(node.id)}">Focus</button>
        </div>
        <div class="result-meta">Trail ${index + 1} · ${escapeHtml(nodeTypeLabel(node.type))}</div>
      </div>
    `;
  }).join('');

  bindFocusButtons(els.historyList);
}

function renderNodeMetrics(node, outgoing, incoming, snapshot) {
  const degree = snapshot.visibleDegree.get(node.id) || 0;
  const sourcePath = deriveSourcePath(node);
  return `
    <div class="metric-grid">
      <div class="metric-tile">
        <div class="metric-label">Visible Degree</div>
        <div class="metric-value">${formatNumber(degree)}</div>
        <div class="metric-subvalue">under current filters</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Pinned</div>
        <div class="metric-value">${isPinned(node.id) ? 'Yes' : 'No'}</div>
        <div class="metric-subvalue">shift-click or button toggle</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Outgoing</div>
        <div class="metric-value">${formatNumber(outgoing.length)}</div>
        <div class="metric-subvalue">selected relation set</div>
      </div>
      <div class="metric-tile">
        <div class="metric-label">Incoming</div>
        <div class="metric-value">${formatNumber(incoming.length)}</div>
        <div class="metric-subvalue">selected relation set</div>
      </div>
    </div>
    ${sourcePath ? `<a class="repo-link" href="${repoHref(sourcePath)}" target="_blank" rel="noreferrer">Open ${escapeHtml(sourcePath)}</a>` : ''}
  `;
}

function makeEdgeRows(edges, direction) {
  if (!edges.length) {
    return '<p class="empty">No relationships in this direction for the current filters.</p>';
  }

  return `
    <ul class="edge-list">
      ${edges.slice(0, 80).map((edge) => {
        const peerId = direction === 'out' ? edge.target : edge.source;
        const peer = state.index.nodesById.get(peerId) || {id: peerId, type: 'unknown'};
        const peerPath = deriveSourcePath(peer);
        return `
          <li class="edge-item">
            <div class="edge-meta">${escapeHtml(relationLabel(edge.relation))}${edge.note ? ` · ${escapeHtml(edge.note)}` : ''}</div>
            <div class="edge-target">
              <span>${escapeHtml(labelForNode(peer))}</span>
              <button type="button" data-focus="${escapeHtml(peer.id)}">Focus</button>
            </div>
            ${peerPath ? `<a class="repo-link" href="${repoHref(peerPath)}" target="_blank" rel="noreferrer">${escapeHtml(peerPath)}</a>` : ''}
          </li>
        `;
      }).join('')}
    </ul>
  `;
}

function renderInspector() {
  if (!state.focusedNodeId || !state.index.nodesById.has(state.focusedNodeId)) {
    const hoveredNode = state.hoveredNodeId ? state.index.nodesById.get(state.hoveredNodeId) : null;
    els.inspector.innerHTML = `
      <div class="inspector-body">
        <p>Select a node to inspect metadata, inbound and outbound relationships, and source links.</p>
        ${hoveredNode ? `<div class="chip-row"><span class="chip">Hovering ${escapeHtml(labelForNode(hoveredNode))}</span></div>` : ''}
        <div>
          <h3>Search Context</h3>
          ${state.search.trim() ? `<p class="small-note">${formatNumber(state.snapshot.searchMatches.length)} matches for “${escapeHtml(state.search.trim())}”.</p>` : '<p class="empty">Run a search or click any node in the graph.</p>'}
        </div>
      </div>
    `;
    return;
  }

  const node = state.index.nodesById.get(state.focusedNodeId);
  const metadataEntries = Object.entries(node)
    .filter(([key, value]) => !['id', 'label'].includes(key) && value !== null && value !== undefined && value !== '')
    .sort(([a], [b]) => a.localeCompare(b));
  const outgoing = (state.index.outgoing.get(node.id) || []).filter((edge) => state.selectedRelations.has(edge.relation));
  const incoming = (state.index.incoming.get(node.id) || []).filter((edge) => state.selectedRelations.has(edge.relation));

  els.inspector.innerHTML = `
    <div class="inspector-body">
      <div>
        <h3>${escapeHtml(labelForNode(node))}</h3>
        <p class="empty">${escapeHtml(nodeTypeLabel(node.type))} · ${escapeHtml(node.id)}</p>
      </div>

      <div class="inspect-actions">
        <button type="button" data-depth="1">Show 1 Hop</button>
        <button type="button" data-depth="2">Show 2 Hops</button>
        <button type="button" data-depth="0">Show All</button>
        <button type="button" data-pin-target="${escapeHtml(node.id)}">${isPinned(node.id) ? 'Unpin Node' : 'Pin Node'}</button>
      </div>

      ${renderNodeMetrics(node, outgoing, incoming, state.snapshot)}

      <dl class="kv">
        ${metadataEntries.map(([key, value]) => `<dt>${escapeHtml(key)}</dt><dd>${escapeHtml(String(value))}</dd>`).join('')}
      </dl>

      <div>
        <h3>Outgoing</h3>
        ${makeEdgeRows(outgoing, 'out')}
      </div>

      <div>
        <h3>Incoming</h3>
        ${makeEdgeRows(incoming, 'in')}
      </div>
    </div>
  `;

  bindFocusButtons(els.inspector);
}

function buildEmphasisSet(snapshot) {
  const emphasized = new Set();
  const anchors = [state.focusedNodeId, state.hoveredNodeId].filter(Boolean);

  for (const id of anchors) {
    emphasized.add(id);
    for (const neighbor of state.index.neighbors.get(id) || []) {
      if (snapshot.visibleIds.has(neighbor)) emphasized.add(neighbor);
    }
  }

  if (!anchors.length && state.search.trim()) {
    for (const node of snapshot.searchMatches.slice(0, 12)) {
      emphasized.add(node.id);
    }
  }

  return emphasized;
}

function computeNodeRadius(node, snapshot) {
  if (state.sizeMode === 'flat') return 6;
  if (state.sizeMode === 'type') {
    const typeSizes = {
      collection: 8,
      file: 7,
      python_function: 6,
      python_class: 7,
      python_variable: 5,
      ts_symbol: 6,
      ts_variable: 5,
      node_dependency: 7,
      python_dependency: 7,
      environment_variable: 8,
      unknown: 5,
    };
    return typeSizes[node.type] || 6;
  }
  const degree = snapshot.visibleDegree.get(node.id) || 0;
  return 4.5 + Math.min(10, Math.sqrt(degree + 1) * 1.6);
}

function buildTypeAnchors(nodes, width, height) {
  const types = [...new Set(nodes.map((node) => node.type))].sort();
  const radiusX = Math.max(180, width * 0.28);
  const radiusY = Math.max(150, height * 0.24);
  const anchors = new Map();

  types.forEach((type, index) => {
    const angle = (index / Math.max(types.length, 1)) * Math.PI * 2 - Math.PI / 2;
    anchors.set(type, {
      x: width / 2 + Math.cos(angle) * radiusX,
      y: height / 2 + Math.sin(angle) * radiusY,
    });
  });

  return anchors;
}

function radialDistance(node) {
  const distances = {
    collection: 90,
    environment_variable: 130,
    python_function: 190,
    python_class: 180,
    python_variable: 240,
    ts_symbol: 190,
    ts_variable: 230,
    file: 300,
    node_dependency: 360,
    python_dependency: 360,
    unknown: 270,
  };
  return distances[node.type] || 260;
}

function buildRadialAnchors(nodes, width, height) {
  const sorted = [...nodes].sort((a, b) => `${a.type}:${labelForNode(a)}`.localeCompare(`${b.type}:${labelForNode(b)}`));
  const anchors = new Map();

  sorted.forEach((node, index) => {
    const angle = (index / Math.max(sorted.length, 1)) * Math.PI * 2 - Math.PI / 2;
    const distance = radialDistance(node);
    anchors.set(node.id, {
      x: width / 2 + Math.cos(angle) * distance,
      y: height / 2 + Math.sin(angle) * distance,
    });
  });

  return anchors;
}
function edgeStrokeDash(edge) {
  const dashed = {
    writes: '8 6',
    dispatches_to: '4 4',
    validates_with: '2 6',
    loads: '5 5',
    depends_on: '10 6',
    uses_env: '2 5',
  };
  return dashed[edge.relation] || null;
}

function edgeStrokeWidth(edge) {
  const widths = {
    defines: 1.6,
    imports: 1.4,
    calls: 1.8,
    calls_into: 1.6,
    uses_component: 1.6,
    writes: 2.2,
    dispatches_to: 2.2,
    depends_on: 1.6,
    drives: 2.4,
    loads: 2.0,
  };
  return widths[edge.relation] || 1.3;
}

function linkPath(edge) {
  const sourceX = edge.source.x;
  const sourceY = edge.source.y;
  const targetX = edge.target.x;
  const targetY = edge.target.y;
  const dx = targetX - sourceX;
  const dy = targetY - sourceY;
  const distance = Math.sqrt(dx * dx + dy * dy) || 1;
  const curve = Math.min(42, distance * 0.12);
  const mx = (sourceX + targetX) / 2;
  const my = (sourceY + targetY) / 2;
  const nx = -dy / distance;
  const ny = dx / distance;
  const cx = mx + nx * curve;
  const cy = my + ny * curve;
  return `M${sourceX},${sourceY} Q${cx},${cy} ${targetX},${targetY}`;
}

function createSvgScene(svg, width, height) {
  svg.selectAll('*').remove();
  svg.attr('viewBox', [0, 0, width, height]);

  const defs = svg.append('defs');

  const grid = defs.append('pattern')
    .attr('id', 'grid-pattern')
    .attr('width', 32)
    .attr('height', 32)
    .attr('patternUnits', 'userSpaceOnUse');

  grid.append('path')
    .attr('d', 'M 32 0 L 0 0 0 32')
    .attr('fill', 'none')
    .attr('stroke', 'rgba(141, 215, 255, 0.06)')
    .attr('stroke-width', 1);

  const glow = defs.append('filter')
    .attr('id', 'node-glow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%');

  glow.append('feGaussianBlur').attr('stdDeviation', 5).attr('result', 'blur');
  glow.append('feMerge').selectAll('feMergeNode')
    .data(['blur', 'SourceGraphic'])
    .join('feMergeNode')
    .attr('in', (d) => d);

  svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'url(#grid-pattern)')
    .attr('opacity', 0.85);

  svg.append('circle')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', Math.min(width, height) * 0.24)
    .attr('fill', 'rgba(79, 209, 197, 0.08)');

  svg.append('circle')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', Math.min(width, height) * 0.38)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(141, 215, 255, 0.08)')
    .attr('stroke-width', 1);

  const root = svg.append('g').attr('class', 'graph-root');
  svg.call(
    d3.zoom()
      .scaleExtent([0.12, 6])
      .on('zoom', (event) => root.attr('transform', event.transform)),
  );

  return {root};
}

function renderGraph(snapshot) {
  if (state.simulation) {
    state.simulation.stop();
  }

  const width = els.canvas.clientWidth || 1400;
  const height = els.canvas.clientHeight || 820;
  const svg = d3.select(els.canvas);
  const scene = createSvgScene(svg, width, height);

  if (!snapshot.nodes.length) {
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height / 2)
      .attr('text-anchor', 'middle')
      .attr('fill', 'var(--muted)')
      .style('font-size', '18px')
      .text('No nodes match the current filters.');
    return;
  }

  const nodes = snapshot.nodes.map((node) => ({...node}));
  const edges = snapshot.edges.map((edge) => ({...edge}));
  syncPositions(nodes);

  const root = scene.root;
  const edgeLayer = root.append('g').attr('class', 'edge-layer');
  const auraLayer = root.append('g').attr('class', 'aura-layer');
  const ringLayer = root.append('g').attr('class', 'ring-layer');
  const nodeLayer = root.append('g').attr('class', 'node-layer');
  const labelLayer = root.append('g').attr('class', 'label-layer');

  const link = edgeLayer.selectAll('path')
    .data(edges)
    .join('path')
    .attr('fill', 'none')
    .attr('stroke-linecap', 'round');

  const aura = auraLayer.selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('fill', (d) => nodeColor(d.type))
    .attr('opacity', 0);

  const ring = ringLayer.selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('fill', 'none')
    .attr('stroke-width', 1.6)
    .attr('opacity', 0);

  const node = nodeLayer.selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('cursor', 'pointer')
    .call(
      d3.drag()
        .on('start', (event, d) => {
          if (!event.active) state.simulation.alphaTarget(0.2).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          persistPositions([d]);
          if (!event.active) state.simulation.alphaTarget(0);
          if (isPinned(d.id)) {
            d.fx = d.x;
            d.fy = d.y;
          } else {
            d.fx = null;
            d.fy = null;
          }
        }),
    )
    .on('mouseenter', (_event, d) => {
      state.hoveredNodeId = d.id;
      setStatus(`Hovering ${labelForNode(d)} · ${nodeTypeLabel(d.type)}`);
      applyAppearance();
      renderSelectionSummary(snapshot);
    })
    .on('mouseleave', () => {
      state.hoveredNodeId = null;
      setStatus(`Loaded ${state.currentView.title}. ${state.dataset.summary.nodeCount} nodes and ${state.dataset.summary.edgeCount} edges are available in this view.`);
      applyAppearance();
      renderSelectionSummary(snapshot);
    })
    .on('click', (event, d) => {
      if (event.shiftKey) {
        togglePinnedNode(d.id);
        return;
      }
      focusNode(d.id, 1);
    })
    .on('dblclick', (_event, d) => {
      const sourcePath = deriveSourcePath(d);
      if (sourcePath) {
        window.open(repoHref(sourcePath), '_blank', 'noreferrer');
      }
    });

  node.append('title').text((d) => `${labelForNode(d)}\n${nodeTypeLabel(d.type)}`);

  const label = labelLayer.selectAll('text')
    .data(nodes)
    .join('text')
    .attr('class', 'graph-label')
    .attr('fill', '#eef6ff')
    .style('font-size', '11px')
    .style('pointer-events', 'none')
    .text((d) => labelForNode(d));

  function applyAppearance() {
    const emphasized = buildEmphasisSet(snapshot);
    const hasActiveEmphasis = emphasized.size > 0;
    const matchedIds = new Set(snapshot.searchMatches.map((entry) => entry.id));

    link
      .attr('stroke', (d) => relationSwatch(d.relation))
      .attr('stroke-width', (d) => edgeStrokeWidth(d))
      .attr('stroke-dasharray', (d) => edgeStrokeDash(d))
      .attr('opacity', (d) => {
        const sourceId = edgeNodeId(d.source);
        const targetId = edgeNodeId(d.target);
        const connected = emphasized.has(sourceId) || emphasized.has(targetId);
        if (!hasActiveEmphasis) return 0.42;
        return connected ? 0.92 : 0.08;
      })
      .attr('filter', state.glowEnabled ? 'url(#node-glow)' : null);

    aura
      .attr('r', (d) => computeNodeRadius(d, snapshot) + (emphasized.has(d.id) ? 14 : 8))
      .attr('opacity', (d) => {
        if (!state.glowEnabled) return 0;
        if (state.focusedNodeId === d.id) return 0.32;
        if (state.hoveredNodeId === d.id) return 0.24;
        if (matchedIds.has(d.id)) return 0.18;
        if (isPinned(d.id)) return 0.18;
        return hasActiveEmphasis && emphasized.has(d.id) ? 0.12 : 0.05;
      })
      .attr('filter', state.glowEnabled ? 'url(#node-glow)' : null);

    ring
      .attr('r', (d) => computeNodeRadius(d, snapshot) + 4)
      .attr('stroke', (d) => {
        if (state.focusedNodeId === d.id) return '#ffffff';
        if (isPinned(d.id)) return '#f6c177';
        if (matchedIds.has(d.id)) return '#4fd1c5';
        return relationSwatch('references');
      })
      .attr('opacity', (d) => (state.focusedNodeId === d.id || isPinned(d.id) || matchedIds.has(d.id)) ? 0.9 : 0);

    node
      .attr('r', (d) => computeNodeRadius(d, snapshot))
      .attr('fill', (d) => nodeColor(d.type))
      .attr('stroke', (d) => {
        if (state.focusedNodeId === d.id) return '#ffffff';
        if (state.hoveredNodeId === d.id) return '#d9f7ff';
        if (isPinned(d.id)) return '#f6c177';
        return '#0a131f';
      })
      .attr('stroke-width', (d) => {
        if (state.focusedNodeId === d.id) return 2.4;
        if (state.hoveredNodeId === d.id || isPinned(d.id)) return 1.8;
        return 1.1;
      })
      .attr('opacity', (d) => {
        if (!hasActiveEmphasis) return 0.95;
        return emphasized.has(d.id) || matchedIds.has(d.id) ? 1 : 0.18;
      })
      .attr('filter', (d) => state.glowEnabled && (state.focusedNodeId === d.id || state.hoveredNodeId === d.id || matchedIds.has(d.id)) ? 'url(#node-glow)' : null);

    label
      .style('display', (d) => {
        const highlighted = emphasized.has(d.id) || matchedIds.has(d.id) || state.focusedNodeId === d.id || state.hoveredNodeId === d.id;
        return state.showLabels || highlighted || snapshot.nodes.length <= 140 ? 'block' : 'none';
      })
      .attr('opacity', (d) => {
        if (!hasActiveEmphasis) return 0.82;
        return emphasized.has(d.id) || matchedIds.has(d.id) ? 0.96 : 0.18;
      });
  }

  function linkDistance(edge) {
    const distances = {
      defines: 34,
      imports: 74,
      calls: 88,
      calls_into: 84,
      writes: 112,
      dispatches_to: 130,
      drives: 140,
      depends_on: 94,
      uses_component: 78,
      references: 64,
      loads: 80,
    };
    return distances[edge.relation] || 68;
  }

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(edges).id((d) => d.id).distance((edge) => linkDistance(edge)).strength(0.3))
    .force('charge', d3.forceManyBody().strength((d) => {
      const base = state.layoutMode === 'force' ? -170 : -115;
      return state.focusedNodeId === d.id ? base * 1.5 : base;
    }))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collide', d3.forceCollide().radius((d) => computeNodeRadius(d, snapshot) + 8));

  if (state.layoutMode === 'clusters') {
    const anchors = buildTypeAnchors(nodes, width, height);
    simulation
      .force('x', d3.forceX((d) => anchors.get(d.type)?.x ?? width / 2).strength(0.14))
      .force('y', d3.forceY((d) => anchors.get(d.type)?.y ?? height / 2).strength(0.14));
  } else if (state.layoutMode === 'radial') {
    const radialAnchors = buildRadialAnchors(nodes, width, height);
    simulation
      .force('x', d3.forceX((d) => radialAnchors.get(d.id)?.x ?? width / 2).strength(0.12))
      .force('y', d3.forceY((d) => radialAnchors.get(d.id)?.y ?? height / 2).strength(0.12));
  } else {
    simulation
      .force('x', d3.forceX(width / 2).strength(0.05))
      .force('y', d3.forceY(height / 2).strength(0.05));
  }

  simulation.on('tick', () => {
    link.attr('d', (d) => linkPath(d));

    aura
      .attr('cx', (d) => d.x)
      .attr('cy', (d) => d.y);

    ring
      .attr('cx', (d) => d.x)
      .attr('cy', (d) => d.y);

    node
      .attr('cx', (d) => d.x)
      .attr('cy', (d) => d.y);

    label
      .attr('x', (d) => d.x + computeNodeRadius(d, snapshot) + 6)
      .attr('y', (d) => d.y + 4);

    persistPositions(nodes);
  });

  state.simulation = simulation;
  applyAppearance();
}

function renderDashboard() {
  if (!state.dataset || !state.index) return;
  state.snapshot = computeVisibleGraph();
  updateControlState();
  renderStats(state.snapshot);
  renderViewDescription(state.snapshot);
  renderRelationBreakdown(state.snapshot);
  renderSelectionSummary(state.snapshot);
  renderHotspots(state.snapshot);
  renderSearchResults(state.snapshot);
  renderHistory();
  renderInspector();
  renderGraph(state.snapshot);
  updateHash();

  els.title.textContent = state.currentView.title;
  els.subtitle.textContent = `${state.currentView.description} Visible: ${formatNumber(state.snapshot.nodes.length)} nodes, ${formatNumber(state.snapshot.edges.length)} edges.`;
  savePreference('lastViewId', state.currentView.id);
}

async function loadView(viewId) {
  const view = state.manifest.views.find((item) => item.id === viewId);
  if (!view) return;

  setStatus(`Loading ${view.title}...`);
  state.currentView = view;
  state.dataset = state.datasets.get(view.id);

  if (!state.dataset) {
    state.dataset = await fetchJson(`${DATASET_BASE}${view.file}`);
    state.datasets.set(view.id, state.dataset);
  }

  state.index = buildIndex(state.dataset);
  state.selectedNodeTypes = new Set(listAvailableNodeTypes(state.dataset).map(([type]) => type));
  state.selectedRelations = new Set(listAvailableRelations(state.dataset).map(([relation]) => relation));
  state.focusedNodeId = null;
  state.hoveredNodeId = null;
  state.focusDepth = 0;

  renderTabs();
  renderFilters();
  renderDashboard();
  setStatus(`Loaded ${view.title}. ${view.summary.nodeCount} nodes and ${view.summary.edgeCount} edges are available in this view.`);
}

function exportSvg() {
  const clone = els.canvas.cloneNode(true);
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
  const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  style.textContent = '.graph-label{font:11px "Segoe UI",sans-serif;fill:#eef6ff;text-shadow:0 1px 8px rgba(0,0,0,.62);}';
  clone.prepend(style);

  const blob = new Blob([clone.outerHTML], {type: 'image/svg+xml;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${state.currentView?.id || 'knowledge-graph'}-${new Date().toISOString().replaceAll(':', '-')}.svg`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function bindKeyboardShortcuts() {
  window.addEventListener('keydown', (event) => {
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement || event.target instanceof HTMLSelectElement) {
      if (event.key === 'Escape') {
        event.target.blur();
      }
      return;
    }

    if (event.key === '/') {
      event.preventDefault();
      els.searchInput.focus();
      els.searchInput.select();
      return;
    }

    if (event.key === 'Escape') {
      event.preventDefault();
      resetFocus();
      return;
    }

    if (event.key === '1' && state.focusedNodeId) {
      event.preventDefault();
      state.focusDepth = 1;
      renderDashboard();
      return;
    }

    if (event.key === '2' && state.focusedNodeId) {
      event.preventDefault();
      state.focusDepth = 2;
      renderDashboard();
      return;
    }

    if (event.key === '0') {
      event.preventDefault();
      state.focusDepth = 0;
      renderDashboard();
      return;
    }

    if (event.key.toLowerCase() === 'l') {
      event.preventDefault();
      state.showLabels = !state.showLabels;
      savePreference('showLabels', state.showLabels);
      renderDashboard();
      return;
    }

    if (event.key.toLowerCase() === 'g') {
      event.preventDefault();
      state.glowEnabled = !state.glowEnabled;
      savePreference('glowEnabled', state.glowEnabled);
      renderDashboard();
      return;
    }

    if (event.key.toLowerCase() === 'p' && state.focusedNodeId) {
      event.preventDefault();
      togglePinnedNode(state.focusedNodeId);
    }
  });
}

function bindGlobalControls() {
  els.searchInput.addEventListener('input', (event) => {
    state.search = event.target.value;
    renderDashboard();
  });

  els.layoutMode.addEventListener('change', (event) => {
    state.layoutMode = event.target.value;
    savePreference('layoutMode', state.layoutMode);
    renderDashboard();
  });

  els.sizeMode.addEventListener('change', (event) => {
    state.sizeMode = event.target.value;
    savePreference('sizeMode', state.sizeMode);
    renderDashboard();
  });

  els.clearFocus.addEventListener('click', resetFocus);

  els.focusNeighbors.addEventListener('click', () => {
    if (!state.focusedNodeId) return;
    state.focusDepth = 1;
    renderDashboard();
  });

  els.focusTwoHops.addEventListener('click', () => {
    if (!state.focusedNodeId) return;
    state.focusDepth = 2;
    renderDashboard();
  });

  els.focusAll.addEventListener('click', () => {
    state.focusDepth = 0;
    renderDashboard();
  });

  els.toggleLabels.addEventListener('click', () => {
    state.showLabels = !state.showLabels;
    savePreference('showLabels', state.showLabels);
    renderDashboard();
  });

  els.toggleHalo.addEventListener('click', () => {
    state.glowEnabled = !state.glowEnabled;
    savePreference('glowEnabled', state.glowEnabled);
    renderDashboard();
  });

  els.pinFocused.addEventListener('click', () => {
    if (!state.focusedNodeId) return;
    togglePinnedNode(state.focusedNodeId);
  });

  els.exportSvg.addEventListener('click', exportSvg);

  window.addEventListener('resize', () => renderDashboard());
  bindKeyboardShortcuts();
}

async function init() {
  if (!window.d3) {
    setStatus('D3 failed to load from engine/node_modules.', true);
    return;
  }

  try {
    bindGlobalControls();
    state.manifest = await fetchJson(MANIFEST_URL);
    renderTabs();

    const hashState = readHashState();
    const preferredView = hashState.view || loadPreference('lastViewId', state.manifest.views[0].id) || state.manifest.views[0].id;
    await loadView(preferredView);

    if (hashState.focus && state.index?.nodesById.has(hashState.focus)) {
      state.focusedNodeId = hashState.focus;
      state.focusDepth = hashState.depth || 1;
      addToHistory(hashState.focus);
      renderDashboard();
    }
  } catch (error) {
    console.error(error);
    setStatus(error.message, true);
    els.inspector.innerHTML = `<p class="empty">${escapeHtml(error.message)}</p>`;
  }
}

init();
