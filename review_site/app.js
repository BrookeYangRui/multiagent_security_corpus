(() => {
  'use strict';

  const DATA_FILES = [
    ['set1_core', 'data/set1_core.csv'],
    ['set2_emerging', 'data/set2_emerging.csv'],
  ];

  const STORAGE_KEY = 'mas-security-corpus-human-review-v1';
  const INTERFACE_LABELS = {
    I1_boundary_admission: 'I1 Boundary / admission',
    I2_communication_routing: 'I2 Communication / routing',
    I3_state_memory: 'I3 State / memory',
    I4_delegation_action: 'I4 Delegation / action',
    I5_aggregation_outcome: 'I5 Aggregation / outcome',
    I6_observation_defense: 'I6 Observation / defense',
  };

  const state = {
    papers: [],
    filtered: [],
    selectedId: null,
    reviews: loadStoredReviews(),
    dirty: false,
  };

  const el = id => document.getElementById(id);
  const escapeHtml = value => String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let field = '';
    let quoted = false;

    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"') {
          if (text[i + 1] === '"') {
            field += '"';
            i += 1;
          } else {
            quoted = false;
          }
        } else {
          field += ch;
        }
      } else if (ch === '"') {
        quoted = true;
      } else if (ch === ',') {
        row.push(field);
        field = '';
      } else if (ch === '\n') {
        row.push(field.replace(/\r$/, ''));
        rows.push(row);
        row = [];
        field = '';
      } else {
        field += ch;
      }
    }

    if (field.length || row.length) {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
    }
    if (!rows.length) return [];

    const headers = rows[0].map(h => h.trim());
    return rows.slice(1)
      .filter(r => r.some(cell => cell.trim() !== ''))
      .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ''])));
  }

  function toCsv(rows, columns) {
    const quote = value => {
      const str = String(value ?? '');
      return /[",\n\r]/.test(str) ? `"${str.replaceAll('"', '""')}"` : str;
    };
    return [columns.join(','), ...rows.map(row => columns.map(col => quote(row[col])).join(','))].join('\n');
  }

  function splitTags(value) {
    return String(value || '')
      .split(';')
      .map(v => v.trim())
      .filter(Boolean);
  }

  function unique(values) {
    return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
  }

  function paperId(paper) {
    return paper.canonical_paper_id || paper.work_key;
  }

  function loadStoredReviews() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch {
      return {};
    }
  }

  function persistReviews() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.reviews));
    state.dirty = false;
    el('saveState').textContent = 'Saved locally';
    el('saveState').classList.remove('dirty');
    updateSummary();
  }

  function markDirty() {
    if (!state.selectedId) return;
    state.dirty = true;
    el('saveState').textContent = 'Saving...';
    el('saveState').classList.add('dirty');
  }

  function debounce(fn, delay = 180) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  }

  async function loadPapers() {
    const sets = await Promise.all(DATA_FILES.map(async ([setName, path]) => {
      const response = await fetch(path, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Could not load ${path}`);
      return parseCsv(await response.text()).map(row => ({ ...row, evidence_set: row.evidence_set || setName }));
    }));

    state.papers = sets.flat().map(paper => ({ ...paper, _id: paperId(paper) }));
    populateFilterOptions();
    populateInterfaceChoices();
    applyFilters();
    updateSummary();

    if (state.filtered.length) selectPaper(state.filtered[0]._id);
  }

  function populateSelect(id, values) {
    const select = el(id);
    values.forEach(value => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value.replaceAll('_', ' ');
      select.appendChild(option);
    });
  }

  function populateFilterOptions() {
    populateSelect('typeFilter', unique(state.papers.map(p => p.dominant_contribution)));
    populateSelect('interfaceFilter', unique(state.papers.flatMap(p => splitTags(p.interaction_interfaces))));
    populateSelect('riskFilter', unique(state.papers.flatMap(p => splitTags(p.risk_or_property))));

    const datalist = el('riskSuggestions');
    unique(state.papers.flatMap(p => splitTags(p.risk_or_property))).forEach(value => {
      const option = document.createElement('option');
      option.value = value;
      datalist.appendChild(option);
    });
  }

  function populateInterfaceChoices() {
    const observed = unique(state.papers.flatMap(p => splitTags(p.interaction_interfaces)));
    const canonical = Object.keys(INTERFACE_LABELS);
    const all = unique([...canonical, ...observed]);
    el('interfaceChoices').innerHTML = all.map(value => `
      <label class="check-chip">
        <input type="checkbox" value="${escapeHtml(value)}">
        ${escapeHtml(INTERFACE_LABELS[value] || value.replaceAll('_', ' '))}
      </label>
    `).join('');
  }

  function reviewFor(id) {
    return state.reviews[id] || {};
  }

  function effectiveStatus(paper) {
    return reviewFor(paper._id).review_status || 'unreviewed';
  }

  function effectiveType(paper) {
    return reviewFor(paper._id).dominant_contribution || paper.dominant_contribution || '';
  }

  function effectiveInterfaces(paper) {
    const review = reviewFor(paper._id);
    return splitTags(review.interaction_interfaces || paper.interaction_interfaces);
  }

  function effectiveRisks(paper) {
    const review = reviewFor(paper._id);
    return splitTags(review.risk_or_property || paper.risk_or_property);
  }

  function applyFilters() {
    const query = el('searchInput').value.trim().toLowerCase();
    const setValue = el('setFilter').value;
    const status = el('statusFilter').value;
    const type = el('typeFilter').value;
    const iface = el('interfaceFilter').value;
    const risk = el('riskFilter').value;

    state.filtered = state.papers.filter(paper => {
      if (setValue !== 'all' && paper.evidence_set !== setValue) return false;
      if (status !== 'all' && effectiveStatus(paper) !== status) return false;
      if (type !== 'all' && effectiveType(paper) !== type) return false;
      if (iface !== 'all' && !effectiveInterfaces(paper).includes(iface)) return false;
      if (risk !== 'all' && !effectiveRisks(paper).includes(risk)) return false;
      if (query) {
        const haystack = [paper.title, paper.venue, paper.year, paper.doi, paper.arxiv_id, paper.work_key]
          .join(' ').toLowerCase();
        if (!haystack.includes(query)) return false;
      }
      return true;
    });

    sortFiltered();
    renderList();
  }

  function sortFiltered() {
    const sort = el('sortSelect').value;
    state.filtered.sort((a, b) => {
      if (sort === 'review') {
        const rank = { unreviewed: 0, revisit: 1, reviewed: 2 };
        const diff = (rank[effectiveStatus(a)] ?? 0) - (rank[effectiveStatus(b)] ?? 0);
        if (diff) return diff;
        return Number(b.year || 0) - Number(a.year || 0) || a.title.localeCompare(b.title);
      }
      if (sort === 'year_desc') return Number(b.year || 0) - Number(a.year || 0) || a.title.localeCompare(b.title);
      if (sort === 'year_asc') return Number(a.year || 0) - Number(b.year || 0) || a.title.localeCompare(b.title);
      return a.title.localeCompare(b.title);
    });
  }

  function renderList() {
    const list = el('paperList');
    list.innerHTML = state.filtered.map(paper => {
      const status = effectiveStatus(paper);
      const setClass = paper.evidence_set === 'set1_core' ? 'set1' : 'set2';
      const type = effectiveType(paper);
      return `
        <button class="paper-card ${paper._id === state.selectedId ? 'selected' : ''}" data-paper-id="${escapeHtml(paper._id)}">
          <div class="paper-card-title">${escapeHtml(paper.title)}</div>
          <div class="paper-card-meta">
            <span class="status-dot ${escapeHtml(status)}"></span>
            <span>${escapeHtml(paper.year || 'n.d.')}${paper.venue ? ` · ${escapeHtml(paper.venue)}` : ''}</span>
            <span class="mini-badge ${setClass}">${paper.evidence_set === 'set1_core' ? 'Set 1' : 'Set 2'}</span>
            ${type ? `<span class="mini-badge">${escapeHtml(type)}</span>` : ''}
          </div>
        </button>
      `;
    }).join('');

    list.querySelectorAll('[data-paper-id]').forEach(button => {
      button.addEventListener('click', () => selectPaper(button.dataset.paperId));
    });

    el('emptyList').classList.toggle('hidden', state.filtered.length !== 0);
    el('visibleCount').textContent = `${state.filtered.length} paper${state.filtered.length === 1 ? '' : 's'}`;
  }

  function selectedPaper() {
    return state.papers.find(p => p._id === state.selectedId) || null;
  }

  function selectPaper(id) {
    if (state.dirty) saveCurrentReview();
    state.selectedId = id;
    renderList();
    renderReviewPanel();
    const selected = el('paperList').querySelector(`[data-paper-id="${CSS.escape(id)}"]`);
    selected?.scrollIntoView({ block: 'nearest' });
  }

  function sourceLinks(paper) {
    const links = [];
    if (paper.primary_url) links.push(['Primary source', paper.primary_url]);
    if (paper.doi) links.push(['DOI', `https://doi.org/${paper.doi}`]);
    if (paper.arxiv_id) links.push(['arXiv', `https://arxiv.org/abs/${paper.arxiv_id}`]);
    links.push(['GitHub row', paper.evidence_set === 'set1_core'
      ? 'https://github.com/BrookeYangRui/multiagent_security_corpus/blob/main/corpus/set1_core.csv'
      : 'https://github.com/BrookeYangRui/multiagent_security_corpus/blob/main/corpus/set2_emerging.csv']);
    return links;
  }

  function renderReviewPanel() {
    const paper = selectedPaper();
    el('reviewEmpty').classList.toggle('hidden', Boolean(paper));
    el('reviewContent').classList.toggle('hidden', !paper);
    if (!paper) return;

    const status = effectiveStatus(paper);
    el('paperBadges').innerHTML = [
      `<span class="badge ${paper.evidence_set === 'set1_core' ? 'good' : ''}">${paper.evidence_set === 'set1_core' ? 'Set 1 core' : 'Set 2 emerging'}</span>`,
      `<span class="badge ${status === 'reviewed' ? 'good' : status === 'revisit' ? 'warn' : ''}">${status}</span>`,
      paper.peer_reviewed ? `<span class="badge">peer reviewed: ${escapeHtml(paper.peer_reviewed)}</span>` : '',
    ].join('');

    el('paperTitle').textContent = paper.title;
    el('paperMeta').textContent = [paper.year, paper.venue, paper.doi ? `DOI ${paper.doi}` : '', paper.arxiv_id ? `arXiv ${paper.arxiv_id}` : ''].filter(Boolean).join(' · ');
    el('sourceActions').innerHTML = sourceLinks(paper).map(([label, href]) => `<a class="source-link" href="${escapeHtml(href)}" target="_blank" rel="noopener">${escapeHtml(label)} ↗</a>`).join('');

    const current = [
      ['Dominant contribution', paper.dominant_contribution || 'Unclear'],
      ['Interaction dependence', paper.interaction_dependence || 'Unclear'],
      ['Interfaces', paper.interaction_interfaces || 'Uncoded'],
      ['Risk / property', paper.risk_or_property || 'Uncoded'],
      ['Evidence basis', paper.evidence_basis || 'Unclear'],
      ['Citation role', paper.citation_role || 'Uncoded'],
    ];
    el('currentLabels').innerHTML = current.map(([label, value]) => `<div class="current-item"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`).join('');
    el('currentTaxonomyReady').textContent = `taxonomy ready: ${paper.taxonomy_ready || 'unclear'}`;

    const details = [
      ['Scope reason', paper.scope_reason],
      ['Membership', paper.membership_reason],
      ['Decision reason', paper.decision_reason],
      ['Evidence locator', paper.evidence_locator],
      ['Reviewer', paper.reviewer],
      ['Reviewed at', paper.reviewed_at],
    ].filter(([, value]) => value);
    el('decisionDetails').innerHTML = details.map(([label, value]) => `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd>`).join('');

    loadForm(paper);
  }

  function defaultReview(paper) {
    const knownInterfaces = splitTags(paper.interaction_interfaces).filter(v => INTERFACE_LABELS[v]);
    const customInterfaces = splitTags(paper.interaction_interfaces).filter(v => !INTERFACE_LABELS[v]);
    return {
      review_status: 'unreviewed',
      membership_decision: 'retain',
      dominant_contribution: paper.dominant_contribution || '',
      secondary_roles: '',
      interaction_interfaces: knownInterfaces.join(';'),
      custom_interfaces: customInterfaces.join(';'),
      risk_or_property: paper.risk_or_property || '',
      interaction_dependence: paper.interaction_dependence || '',
      evidence_level: '',
      confidence: '',
      human_tags: '',
      review_note: '',
      reviewed_by: '',
      reviewed_at: '',
    };
  }

  function loadForm(paper) {
    const review = { ...defaultReview(paper), ...reviewFor(paper._id) };
    el('reviewStatus').value = review.review_status || 'unreviewed';
    el('membershipDecision').value = review.membership_decision || 'retain';
    el('dominantContribution').value = review.dominant_contribution || '';
    el('interactionDependence').value = review.interaction_dependence || '';
    el('riskProperty').value = review.risk_or_property || '';
    el('evidenceLevel').value = review.evidence_level || '';
    el('confidence').value = review.confidence || '';
    el('humanTags').value = review.human_tags || '';
    el('reviewNote').value = review.review_note || '';
    el('reviewedBy').value = review.reviewed_by || '';
    el('reviewedAt').value = review.reviewed_at || '';
    el('customInterfaces').value = review.custom_interfaces || '';

    const roles = new Set(splitTags(review.secondary_roles));
    el('roleChoices').querySelectorAll('input[type="checkbox"]').forEach(input => { input.checked = roles.has(input.value); });

    const interfaces = new Set(splitTags(review.interaction_interfaces));
    el('interfaceChoices').querySelectorAll('input[type="checkbox"]').forEach(input => { input.checked = interfaces.has(input.value); });

    state.dirty = false;
    el('saveState').textContent = 'Saved locally';
    el('saveState').classList.remove('dirty');
  }

  function collectForm() {
    const roles = [...el('roleChoices').querySelectorAll('input:checked')].map(input => input.value);
    const interfaces = [...el('interfaceChoices').querySelectorAll('input:checked')].map(input => input.value);
    return {
      review_status: el('reviewStatus').value,
      membership_decision: el('membershipDecision').value,
      dominant_contribution: el('dominantContribution').value,
      secondary_roles: roles.join(';'),
      interaction_interfaces: interfaces.join(';'),
      custom_interfaces: el('customInterfaces').value.trim(),
      risk_or_property: normalizeTags(el('riskProperty').value),
      interaction_dependence: el('interactionDependence').value,
      evidence_level: el('evidenceLevel').value,
      confidence: el('confidence').value,
      human_tags: normalizeTags(el('humanTags').value),
      review_note: el('reviewNote').value.trim(),
      reviewed_by: el('reviewedBy').value.trim(),
      reviewed_at: el('reviewedAt').value,
    };
  }

  function normalizeTags(value) {
    return unique(splitTags(value)).join(';');
  }

  function saveCurrentReview() {
    const paper = selectedPaper();
    if (!paper) return;
    const review = collectForm();
    state.reviews[paper._id] = review;
    persistReviews();
    applyFilters();
  }

  function moveSelection(delta) {
    if (!state.filtered.length) return;
    const index = state.filtered.findIndex(p => p._id === state.selectedId);
    const next = index < 0
      ? (delta >= 0 ? 0 : state.filtered.length - 1)
      : Math.min(state.filtered.length - 1, Math.max(0, index + delta));
    selectPaper(state.filtered[next]._id);
  }

  function markReviewedAndNext() {
    if (!selectedPaper()) return;
    el('reviewStatus').value = 'reviewed';
    if (!el('reviewedAt').value) el('reviewedAt').value = new Date().toISOString().slice(0, 10);
    saveCurrentReview();
    moveSelection(1);
  }

  function resetCurrentPaper() {
    const paper = selectedPaper();
    if (!paper) return;
    if (!confirm('Reset your local review for this paper?')) return;
    delete state.reviews[paper._id];
    persistReviews();
    renderReviewPanel();
    applyFilters();
  }

  function updateSummary() {
    const total = state.papers.length;
    const reviewed = state.papers.filter(p => effectiveStatus(p) === 'reviewed').length;
    const set1 = state.papers.filter(p => p.evidence_set === 'set1_core').length;
    const set2 = state.papers.filter(p => p.evidence_set === 'set2_emerging').length;
    const pct = total ? Math.round((reviewed / total) * 100) : 0;
    el('totalCount').textContent = total;
    el('reviewedCount').textContent = reviewed;
    el('set1Count').textContent = set1;
    el('set2Count').textContent = set2;
    el('progressLabel').textContent = `${pct}%`;
    el('progressFill').style.width = `${pct}%`;
  }

  function exportedRows() {
    return state.papers
      .filter(p => state.reviews[p._id])
      .map(p => {
        const r = state.reviews[p._id];
        return {
          paper_id: p._id,
          work_key: p.work_key,
          title: p.title,
          evidence_set: p.evidence_set,
          review_status: r.review_status,
          membership_decision: r.membership_decision,
          dominant_contribution: r.dominant_contribution,
          secondary_roles: r.secondary_roles,
          interaction_interfaces: normalizeTags([r.interaction_interfaces, r.custom_interfaces].filter(Boolean).join(';')),
          risk_or_property: r.risk_or_property,
          interaction_dependence: r.interaction_dependence,
          evidence_level: r.evidence_level,
          confidence: r.confidence,
          human_tags: r.human_tags,
          review_note: r.review_note,
          reviewed_by: r.reviewed_by,
          reviewed_at: r.reviewed_at,
        };
      });
  }

  function downloadBlob(name, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = name;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 500);
  }

  function exportCsv() {
    if (state.dirty) saveCurrentReview();
    const rows = exportedRows();
    const columns = ['paper_id', 'work_key', 'title', 'evidence_set', 'review_status', 'membership_decision', 'dominant_contribution', 'secondary_roles', 'interaction_interfaces', 'risk_or_property', 'interaction_dependence', 'evidence_level', 'confidence', 'human_tags', 'review_note', 'reviewed_by', 'reviewed_at'];
    downloadBlob(`mas_corpus_human_review_${new Date().toISOString().slice(0, 10)}.csv`, toCsv(rows, columns), 'text/csv;charset=utf-8');
  }

  function exportJson() {
    if (state.dirty) saveCurrentReview();
    const payload = {
      schema: 1,
      exported_at: new Date().toISOString(),
      repository: 'BrookeYangRui/multiagent_security_corpus',
      reviews: state.reviews,
    };
    downloadBlob(`mas_corpus_human_review_backup_${new Date().toISOString().slice(0, 10)}.json`, JSON.stringify(payload, null, 2), 'application/json');
  }

  async function importReview(file) {
    const text = await file.text();
    let imported = {};
    if (file.name.toLowerCase().endsWith('.json')) {
      const payload = JSON.parse(text);
      imported = payload.reviews || payload;
    } else {
      const rows = parseCsv(text);
      rows.forEach(row => {
        const id = row.paper_id || row.canonical_paper_id || row.work_key;
        if (!id) return;
        imported[id] = {
          review_status: row.review_status || 'unreviewed',
          membership_decision: row.membership_decision || 'retain',
          dominant_contribution: row.dominant_contribution || '',
          secondary_roles: row.secondary_roles || '',
          interaction_interfaces: splitTags(row.interaction_interfaces).filter(v => INTERFACE_LABELS[v]).join(';'),
          custom_interfaces: splitTags(row.interaction_interfaces).filter(v => !INTERFACE_LABELS[v]).join(';'),
          risk_or_property: row.risk_or_property || '',
          interaction_dependence: row.interaction_dependence || '',
          evidence_level: row.evidence_level || '',
          confidence: row.confidence || '',
          human_tags: row.human_tags || '',
          review_note: row.review_note || '',
          reviewed_by: row.reviewed_by || '',
          reviewed_at: row.reviewed_at || '',
        };
      });
    }
    state.reviews = { ...state.reviews, ...imported };
    persistReviews();
    applyFilters();
    renderReviewPanel();
    alert(`Imported ${Object.keys(imported).length} review records.`);
  }

  function clearFilters() {
    el('searchInput').value = '';
    el('setFilter').value = 'all';
    el('statusFilter').value = 'all';
    el('typeFilter').value = 'all';
    el('interfaceFilter').value = 'all';
    el('riskFilter').value = 'all';
    applyFilters();
  }

  function bindEvents() {
    ['searchInput', 'setFilter', 'statusFilter', 'typeFilter', 'interfaceFilter', 'riskFilter']
      .forEach(id => el(id).addEventListener('input', applyFilters));
    el('sortSelect').addEventListener('change', applyFilters);
    el('clearFiltersButton').addEventListener('click', clearFilters);
    el('prevButton').addEventListener('click', () => moveSelection(-1));
    el('nextButton').addEventListener('click', () => moveSelection(1));
    el('reviewNextButton').addEventListener('click', markReviewedAndNext);
    el('resetPaperButton').addEventListener('click', resetCurrentPaper);
    el('exportCsvButton').addEventListener('click', exportCsv);
    el('exportJsonButton').addEventListener('click', exportJson);
    el('importButton').addEventListener('click', () => el('importFile').click());
    el('importFile').addEventListener('change', event => {
      const file = event.target.files?.[0];
      if (file) importReview(file).catch(err => alert(`Import failed: ${err.message}`));
      event.target.value = '';
    });

    el('reviewForm').addEventListener('input', () => {
      markDirty();
      debouncedSave();
    });

    document.addEventListener('keydown', event => {
      const target = event.target;
      const typing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName);
      if (typing && !event.metaKey && !event.ctrlKey) return;
      if (event.key.toLowerCase() === 'j') { event.preventDefault(); moveSelection(1); }
      if (event.key.toLowerCase() === 'k') { event.preventDefault(); moveSelection(-1); }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') { event.preventDefault(); saveCurrentReview(); }
    });
  }

  const debouncedSave = debounce(() => {
    if (state.dirty) saveCurrentReview();
  }, 350);

  bindEvents();
  loadPapers().catch(error => {
    console.error(error);
    el('reviewEmpty').innerHTML = `<div class="empty-icon">!</div><h2>Could not load corpus data</h2><p>${escapeHtml(error.message)}</p>`;
  });
})();
