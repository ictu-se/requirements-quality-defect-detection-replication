let state = {
  items: [],
  filtered: [],
  defectTypes: [],
  severities: [],
  currentIndex: 0,
};

const defectHints = {
  ambiguous_term: "vague wording",
  missing_actor: "actor/system absent",
  missing_trigger: "trigger/condition absent",
  missing_expected_outcome: "observable result absent",
  missing_constraint: "boundary/constraint absent",
  not_testable: "no clear pass/fail test",
  overly_broad_requirement: "scope too broad",
  inconsistent_condition: "contradictory condition/result",
  unsupported_external_assumption: "requires outside assumption",
};

const els = {
  progressText: document.getElementById("progressText"),
  agreementText: document.getElementById("agreementText"),
  itemList: document.getElementById("itemList"),
  searchBox: document.getElementById("searchBox"),
  statusFilter: document.getElementById("statusFilter"),
  rowTitle: document.getElementById("rowTitle"),
  rowMeta: document.getElementById("rowMeta"),
  statement: document.getElementById("statement"),
  defectTypeChecks: document.getElementById("defectTypeChecks"),
  severityRadios: document.getElementById("severityRadios"),
  reviewNotes: document.getElementById("reviewNotes"),
  auditForm: document.getElementById("auditForm"),
  saveBtn: document.getElementById("saveBtn"),
  saveStatus: document.getElementById("saveStatus"),
  prevBtn: document.getElementById("prevBtn"),
  nextBtn: document.getElementById("nextBtn"),
  markNoDefectBtn: document.getElementById("markNoDefectBtn"),
};

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function completed(row) {
  return row.review_has_defect === "TRUE" || row.review_has_defect === "FALSE";
}

function badgeClass(row) {
  if (completed(row)) return "done";
  return "todo";
}

function badgeText(row) {
  return completed(row) ? "done" : "todo";
}

function updateProgress(progress) {
  els.progressText.textContent = `${progress.completed}/${progress.total}`;
  els.agreementText.textContent = `${progress.remaining} rows remaining`;
}

function buildControls() {
  els.defectTypeChecks.innerHTML = state.defectTypes
    .map(
      (type) => `
        <label>
          <input type="checkbox" name="defectType" value="${type}" />
          <span>
            <strong>${type}</strong>
            <small>${defectHints[type] || ""}</small>
          </span>
        </label>
      `,
    )
    .join("");

  els.severityRadios.innerHTML = state.severities
    .map(
      (severity) => `
        <label>
          <input type="radio" name="severity" value="${severity}" />
          ${severity}
        </label>
      `,
    )
    .join("");

}

function applyFilters() {
  const query = els.searchBox.value.trim().toLowerCase();
  const status = els.statusFilter.value;
  state.filtered = state.items.filter((row) => {
    const text = [row.audit_id, row.task_id, row.source_type, row.repo, row.language, row.statement]
      .join(" ")
      .toLowerCase();
    const matchesQuery = !query || text.includes(query);
    let matchesStatus = true;
    if (status === "todo") matchesStatus = !completed(row);
    if (status === "done") matchesStatus = completed(row);
    return matchesQuery && matchesStatus;
  });
  if (state.currentIndex >= state.filtered.length) state.currentIndex = 0;
  renderList();
  renderCurrent();
}

function renderList() {
  els.itemList.innerHTML = state.filtered
    .map((row, index) => {
      const active = index === state.currentIndex ? " active" : "";
      const preview = row.statement.length > 130 ? `${row.statement.slice(0, 130)}...` : row.statement;
      return `
        <button class="item${active}" type="button" data-index="${index}">
          <div class="item-title">
            <span>${escapeHtml(row.audit_id)} · ${escapeHtml(row.task_id)}</span>
            <span class="badge ${badgeClass(row)}">${badgeText(row)}</span>
          </div>
          <div class="item-meta">${escapeHtml(row.source_type)} · ${escapeHtml(row.repo)}</div>
          <div class="item-preview">${escapeHtml(preview)}</div>
        </button>
      `;
    })
    .join("");

  for (const button of els.itemList.querySelectorAll(".item")) {
    button.addEventListener("click", () => {
      state.currentIndex = Number(button.dataset.index);
      renderList();
      renderCurrent();
    });
  }
}

function setRadio(name, value) {
  for (const input of document.querySelectorAll(`input[name="${name}"]`)) {
    input.checked = input.value === value;
  }
}

function getRadio(name) {
  const input = document.querySelector(`input[name="${name}"]:checked`);
  return input ? input.value : "";
}

function setReviewTypes(types) {
  const selected = new Set(types.filter(Boolean));
  for (const input of document.querySelectorAll('input[name="defectType"]')) {
    input.checked = selected.has(input.value);
  }
}

function getReviewTypes() {
  return Array.from(document.querySelectorAll('input[name="defectType"]:checked')).map((input) => input.value);
}

function renderCurrent() {
  const row = state.filtered[state.currentIndex];
  if (!row) {
    els.rowTitle.textContent = "No rows match the current filter";
    els.rowMeta.textContent = "";
    els.statement.textContent = "";
    return;
  }

  els.rowTitle.textContent = `${row.audit_id} · ${row.task_id}`;
  els.rowMeta.textContent = `${row.source_type} · ${row.gold_label_source} · ${row.repo} · ${row.language}`;
  els.statement.textContent = row.statement || "";
  fitStatementText();

  setRadio("hasDefect", row.review_has_defect || "");
  setReviewTypes((row.review_defect_types || "").split("|"));
  setRadio("severity", row.review_severity || "");
  els.reviewNotes.value = row.review_notes || "";
  els.saveStatus.textContent = "";
}

function fitStatementText() {
  const statement = els.statement;
  const card = document.getElementById("auditCard");
  if (!statement || !card || window.innerWidth <= 980) {
    document.documentElement.style.setProperty("--statement-font-size", "14px");
    return;
  }

  const textLength = statement.textContent.length;
  let size = 14;
  if (textLength > 450) size = 12;
  if (textLength > 900) size = 11;
  if (textLength > 1400) size = 10;
  document.documentElement.style.setProperty("--statement-font-size", `${size}px`);

  requestAnimationFrame(() => {
    const bottomLimit = window.innerHeight - 8;
    const cardBottom = card.getBoundingClientRect().bottom;
    if (cardBottom <= bottomLimit) return;
    const nextSize = Math.max(9, size - Math.ceil((cardBottom - bottomLimit) / 180));
    document.documentElement.style.setProperty("--statement-font-size", `${nextSize}px`);
  });
}

function currentOriginalIndex() {
  const row = state.filtered[state.currentIndex];
  return state.items.findIndex((item) => item.audit_id === row.audit_id);
}

async function saveCurrent(options = {}) {
  const row = state.filtered[state.currentIndex];
  if (!row) return;

  const payload = {
    audit_id: row.audit_id,
    review_has_defect: getRadio("hasDefect"),
    review_defect_types: getReviewTypes(),
    review_severity: getRadio("severity"),
    label_agreement: "",
    review_notes: els.reviewNotes.value.trim(),
  };

  if (options.forceNoDefect) {
    payload.review_has_defect = "FALSE";
    payload.review_defect_types = [];
    payload.review_severity = "none";
  }

  if (!payload.review_has_defect) {
    els.saveStatus.textContent = "Choose TRUE or FALSE before saving.";
    return;
  }
  if (payload.review_has_defect === "TRUE" && payload.review_defect_types.length === 0) {
    els.saveStatus.textContent = "TRUE requires at least one defect type.";
    return;
  }
  if (!payload.review_severity) {
    els.saveStatus.textContent = "Choose severity before saving.";
    return;
  }
  els.saveBtn.disabled = true;
  els.saveStatus.textContent = "Saving...";
  const response = await fetch("/api/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  els.saveBtn.disabled = false;

  if (!response.ok) {
    els.saveStatus.textContent = data.error || "Save failed.";
    return;
  }

  const originalIndex = currentOriginalIndex();
  if (originalIndex >= 0) {
    state.items[originalIndex] = {
      ...state.items[originalIndex],
      review_has_defect: payload.review_has_defect,
      review_defect_types: payload.review_defect_types.join("|"),
      review_severity: payload.review_severity,
      label_agreement: payload.label_agreement,
      review_notes: payload.review_notes,
    };
  }
  updateProgress(data.progress);
  applyFilters();
  els.saveStatus.textContent = `Saved ${row.audit_id}`;
}

function markNoDefect() {
  setRadio("hasDefect", "FALSE");
  setReviewTypes([]);
  setRadio("severity", "none");
  if (!els.reviewNotes.value.trim()) els.reviewNotes.value = "Statement is specific enough and testable.";
}

async function load() {
  const response = await fetch("/api/items");
  const data = await response.json();
  state.items = data.items;
  state.defectTypes = data.defect_types;
  state.severities = data.severities;
  updateProgress(data.progress);
  buildControls();
  applyFilters();
}

els.searchBox.addEventListener("input", applyFilters);
els.statusFilter.addEventListener("change", applyFilters);
els.auditForm.addEventListener("submit", (event) => {
  event.preventDefault();
  saveCurrent();
});
els.prevBtn.addEventListener("click", () => {
  if (state.filtered.length === 0) return;
  state.currentIndex = Math.max(0, state.currentIndex - 1);
  renderList();
  renderCurrent();
});
els.nextBtn.addEventListener("click", () => {
  if (state.filtered.length === 0) return;
  state.currentIndex = Math.min(state.filtered.length - 1, state.currentIndex + 1);
  renderList();
  renderCurrent();
});
els.markNoDefectBtn.addEventListener("click", markNoDefect);
window.addEventListener("resize", fitStatementText);

load();
