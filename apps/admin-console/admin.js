const state = {
  apiBase: "",
  lastDraft: null,
  lastUpload: null,
};

const $ = (selector) => document.querySelector(selector);

function localDefaultApiBase() {
  if (["localhost", "127.0.0.1", ""].includes(window.location.hostname)) {
    return "http://127.0.0.1:8000";
  }
  return "";
}

function initApiBase() {
  const configured = window.CAVRA_ADMIN_API_BASE || localStorage.getItem("cavraAdminApiBase") || localDefaultApiBase();
  state.apiBase = configured.replace(/\/$/, "");
  $("#api-base").value = state.apiBase;
}

function writeOutput(value) {
  $("#output").textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

function showDisabled(show) {
  $("#disabled-panel").classList.toggle("hidden", !show);
}

async function api(path, options = {}) {
  if (!state.apiBase) {
    throw new Error("API base URL is required.");
  }
  const response = await fetch(`${state.apiBase}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    const message = data.detail || `${response.status} ${response.statusText}`;
    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }
  return data;
}

function post(path, payload) {
  return api(path, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

function summarizeStatus(status) {
  const deployment = status.deployment || {};
  $("#deployment-title").textContent = `${deployment.platform || "unknown"} / ${deployment.runtime || "unknown"}`;
  $("#deployment-detail").textContent = [
    deployment.environment,
    deployment.orchestrator,
    deployment.install_target,
    deployment.hostname,
  ]
    .filter(Boolean)
    .join(" | ");
  const stores = status.stores || {};
  $("#stores-title").textContent = String(stores.total || 0);
  $("#stores-detail").textContent = `${(stores.items || []).filter((item) => item.exists).length} stores currently exist`;
}

function summarizeReadiness(readiness) {
  const blockers = readiness.blockers || readiness.required_actions || [];
  const ready =
    readiness.ready_for_production === true ||
    readiness.ready_for_aispm_production === true ||
    readiness.status === "ready";
  $("#readiness-title").textContent = ready ? "Ready" : "Needs review";
  $("#readiness-detail").textContent = blockers.length
    ? `${blockers.length} blocker/action item(s) returned by the gate`
    : "No blocker/action items returned by the gate";
}

async function refreshAdminState() {
  try {
    showDisabled(false);
    const status = await api("/admin/status");
    summarizeStatus(status);
    writeOutput(status);
  } catch (error) {
    if (error.status === 404) showDisabled(true);
    writeOutput({ error: error.message, detail: error.data || null });
  }
}

async function runReadiness() {
  const readiness = await api("/admin/readiness");
  summarizeReadiness(readiness);
  writeOutput(readiness);
}

async function loadStores() {
  const stores = await api("/admin/stores");
  $("#stores-title").textContent = String(stores.total || 0);
  $("#stores-detail").textContent = `${(stores.items || []).filter((item) => item.exists).length} stores currently exist`;
  writeOutput(stores);
}

async function readPolicyFile() {
  const file = $("#policy-file").files[0];
  if (!file) throw new Error("Choose a policy pack YAML or JSON file first.");
  return {
    filename: file.name,
    content: await file.text(),
    actor: $("#requested-by").value || "admin-console",
  };
}

async function validatePolicyUpload() {
  const payload = await readPolicyFile();
  const result = await post("/admin/policy-packs/upload", payload);
  state.lastUpload = result;
  state.lastDraft = result.draft?.policy_pack || result.draft;
  writeOutput(result);
}

async function buildPolicyPlan() {
  if (!state.lastDraft) await validatePolicyUpload();
  const result = await post("/admin/policy-packs/publish-plan", { draft: state.lastDraft });
  writeOutput(result);
}

async function requestPolicyApproval() {
  if (!state.lastDraft) await validatePolicyUpload();
  const result = await post("/admin/policy-packs/publish-request", {
    draft: state.lastDraft,
    approver_group: $("#approver-group").value || "Platform Security",
    requested_by: $("#requested-by").value || "admin-console",
  });
  writeOutput(result);
}

async function backupPlan() {
  const result = await post("/admin/backups/plan", {
    output_dir: $("#backup-output").value,
    include_missing: true,
    actor: "admin-console",
  });
  writeOutput(result);
}

async function backupRun() {
  const result = await post("/admin/backups/run", {
    output_dir: $("#backup-output").value,
    include_missing: true,
    confirm: $("#backup-confirm").value,
    actor: "admin-console",
  });
  writeOutput(result);
}

async function retentionPlan() {
  const result = await post("/admin/retention-plan", {
    retention_days: Number($("#retention-days").value || 2555),
    classification: $("#classification").value || "regulated-sdlc",
    legal_hold: $("#legal-hold").checked,
    actor: "admin-console",
  });
  writeOutput(result);
}

function bind(id, handler) {
  $(`#${id}`).addEventListener("click", async () => {
    try {
      await handler();
    } catch (error) {
      if (error.status === 404) showDisabled(true);
      writeOutput({ error: error.message, detail: error.data || null });
    }
  });
}

initApiBase();
bind("save-api", async () => {
  state.apiBase = $("#api-base").value.replace(/\/$/, "");
  localStorage.setItem("cavraAdminApiBase", state.apiBase);
  await refreshAdminState();
});
bind("refresh", refreshAdminState);
bind("readiness", runReadiness);
bind("stores", loadStores);
bind("policy-upload", validatePolicyUpload);
bind("policy-plan", buildPolicyPlan);
bind("policy-request", requestPolicyApproval);
bind("backup-plan", backupPlan);
bind("backup-run", backupRun);
bind("retention-plan", retentionPlan);
refreshAdminState();
