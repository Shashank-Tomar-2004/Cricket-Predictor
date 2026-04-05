const state = {
  format: "odi",
  mode: "manual",
  meta: null,
  selectedTeams: [],
  squads: { team1: null, team2: null },
  selectedXI: { team1: new Set(), team2: new Set() },
  charts: {
    winDonut: null,
    rrLine: null,
    radar: null,
    bar: null,
    formWin: null,
    explainBar: null,
    backtestScatter: null,
    backtestPhase: null,
    liveWorm: null,
    liveRR: null,
    liveManhattan: null,
    liveWinProb: null,
    liveWicketFall: null,
    liveMomentum: null,
    liveConfidence: null,
    scoreConfidence: null,
    dlsResource: null,
    dlsTarget: null,
    tossSim: null,
    winTimeline: null,
    formHeatmap: null,
    formPartnership: null,
  },
  lastScorePayload: null,
  lastLive: null,
  livePack: null,
  lastOutputs: { score: null, explain: null, backtest: null, win: null, form: null, dls: null, uncertainty: null },
  presentation: { active: false, step: 0 },
  beginnerMode: true,
  hero3d: null,
  winTimelineSeries: null,
};

const el = {
  toast: document.getElementById("toast"),
  presentationBtn: document.getElementById("presentation-btn"),
  presentationOverlay: document.getElementById("presentation-overlay"),
  presentationTitle: document.getElementById("presentation-title"),
  presentationText: document.getElementById("presentation-text"),
  presentationNext: document.getElementById("presentation-next"),
  presentationExit: document.getElementById("presentation-exit"),
  backendStatus: document.getElementById("backend-status"),
  modeManualBtn: document.getElementById("mode-manual-btn"),
  modeAutoBtn: document.getElementById("mode-auto-btn"),
  beginnerToggle: document.getElementById("beginner-toggle"),
  heroCanvas: document.getElementById("hero-3d-canvas"),
  fmtButtons: document.querySelectorAll(".fmt-btn"),
  teamGrid: document.getElementById("team-grid"),
  setupError: document.getElementById("setup-error"),
  xiSection: document.getElementById("xi-section"),
  dashboard: document.getElementById("dashboard"),
  xiTeam1Title: document.getElementById("xi-team1-title"),
  xiTeam2Title: document.getElementById("xi-team2-title"),
  xiTeam1Count: document.getElementById("xi-team1-count"),
  xiTeam2Count: document.getElementById("xi-team2-count"),
  xiTeam1List: document.getElementById("xi-team1-list"),
  xiTeam2List: document.getElementById("xi-team2-list"),
  xiTeam1Suggestions: document.getElementById("xi-team1-suggestions"),
  xiTeam2Suggestions: document.getElementById("xi-team2-suggestions"),
  tabButtons: document.querySelectorAll(".tab-btn"),
  tabPanels: document.querySelectorAll(".tab-panel"),
  liveSource: document.getElementById("live-source"),
  liveDemoMatch: document.getElementById("live-demo-match"),
  liveProvider: document.getElementById("live-provider"),
  liveUrl: document.getElementById("live-url"),
  liveApiKey: document.getElementById("live-api-key"),
  liveRootPath: document.getElementById("live-root-path"),
  liveFieldMap: document.getElementById("live-field-map"),
  liveHelp: document.getElementById("live-help"),
  liveIngestBtn: document.getElementById("live-ingest-btn"),
  liveStatus: document.getElementById("live-status"),
  liveError: document.getElementById("live-error"),
  liveFixtures: document.getElementById("live-fixtures"),
  liveXiTeam1: document.getElementById("live-xi-team1"),
  liveXiTeam2: document.getElementById("live-xi-team2"),
  liveRawTeam1: document.getElementById("live-raw-team1"),
  liveRawTeam2: document.getElementById("live-raw-team2"),
  liveFetchedSquad: document.getElementById("live-fetched-squad"),
  liveFormat: document.getElementById("live-format"),
  liveCurrentInnings: document.getElementById("live-current-innings"),
  liveInningsView: document.getElementById("live-innings-view"),
  liveManhattanMode: document.getElementById("live-manhattan-mode"),
  liveToss: document.getElementById("live-toss"),
  liveVenue: document.getElementById("live-venue"),
  liveDataQuality: document.getElementById("live-data-quality"),
  liveConfidence: document.getElementById("live-confidence"),
  livePressure: document.getElementById("live-pressure"),
  liveMiniCommentary: document.getElementById("live-mini-commentary"),
  liveSimilarity: document.getElementById("live-similarity"),
  liveCoachNotes: document.getElementById("live-coach-notes"),
  livePartnershipImpact: document.getElementById("live-partnership-impact"),
  liveBowlerMatchups: document.getElementById("live-bowler-matchups"),
  liveMomentumChart: document.getElementById("live-momentum-chart"),
  liveConfidenceChart: document.getElementById("live-confidence-chart"),
  liveWormChart: document.getElementById("live-worm-chart"),
  liveRRChart: document.getElementById("live-rr-chart"),
  liveWicketChart: document.getElementById("live-wicket-chart"),
  liveManhattanChart: document.getElementById("live-manhattan-chart"),
  liveBreakdown: document.getElementById("live-breakdown"),
  liveWinProbChart: document.getElementById("live-winprob-chart"),
  liveWinProbNote: document.getElementById("live-winprob-note"),
  aiModelType: document.getElementById("ai-model-type"),
  aiVersion: document.getElementById("ai-version"),
  aiUses: document.getElementById("ai-uses"),
  aiNotUses: document.getElementById("ai-not-uses"),
  aiLimitations: document.getElementById("ai-limitations"),
  aiEthics: document.getElementById("ai-ethics"),
  scoreBattingTeam: document.getElementById("score-batting-team"),
  scoreTossWinner: document.getElementById("score-toss-winner"),
  scoreTossDecision: document.getElementById("score-toss-decision"),
  scoreVenueRegion: document.getElementById("score-venue-region"),
  scoreVenueCountry: document.getElementById("score-venue-country"),
  scoreVenue: document.getElementById("score-venue"),
  scorePitch: document.getElementById("score-pitch"),
  scoreWeather: document.getElementById("score-weather"),
  scoreRuns: document.getElementById("score-runs"),
  scoreWickets: document.getElementById("score-wickets"),
  scoreOvers: document.getElementById("score-overs"),
  presetButtons: document.querySelectorAll(".preset-btn"),
  scoreBtn: document.getElementById("score-btn"),
  scoreLow: document.getElementById("score-low"),
  scoreAvg: document.getElementById("score-avg"),
  scoreHigh: document.getElementById("score-high"),
  scorePar: document.getElementById("score-par"),
  scorePhaseBreakdown: document.getElementById("score-phase-breakdown"),
  scoreAdvancedInsights: document.getElementById("score-advanced-insights"),
  scoreNote: document.getElementById("score-note"),
  scoreError: document.getElementById("score-error"),
  scoreWarning: document.getElementById("score-warning"),
  explainBtn: document.getElementById("explain-btn"),
  explainError: document.getElementById("explain-error"),
  explainStoryline: document.getElementById("explain-storyline"),
  explainLow: document.getElementById("explain-low"),
  explainAvg: document.getElementById("explain-avg"),
  explainHigh: document.getElementById("explain-high"),
  explainConfidence: document.getElementById("explain-confidence"),
  explainChart: document.getElementById("explain-chart"),
  explainTopDrivers: document.getElementById("explain-top-drivers"),
  backtestBtn: document.getElementById("backtest-btn"),
  backtestError: document.getElementById("backtest-error"),
  backtestSamples: document.getElementById("backtest-samples"),
  backtestMae: document.getElementById("backtest-mae"),
  backtestRmse: document.getElementById("backtest-rmse"),
  backtestCalib: document.getElementById("backtest-calib"),
  backtestNotes: document.getElementById("backtest-notes"),
  backtestScatter: document.getElementById("backtest-scatter"),
  backtestPhase: document.getElementById("backtest-phase"),
  winChasingTeam: document.getElementById("win-chasing-team"),
  winTossWinner: document.getElementById("win-toss-winner"),
  winTossDecision: document.getElementById("win-toss-decision"),
  winTarget: document.getElementById("win-target"),
  winRuns: document.getElementById("win-runs"),
  winWickets: document.getElementById("win-wickets"),
  winOvers: document.getElementById("win-overs"),
  winTargetSlider: document.getElementById("win-target-slider"),
  winScoreSlider: document.getElementById("win-score-slider"),
  winWicketsSlider: document.getElementById("win-wickets-slider"),
  winBtn: document.getElementById("win-btn"),
  winPercent: document.getElementById("win-percent"),
  winRunsNeeded: document.getElementById("win-runs-needed"),
  winBallsLeft: document.getElementById("win-balls-left"),
  winCrr: document.getElementById("win-crr"),
  winRrr: document.getElementById("win-rrr"),
  winXi: document.getElementById("win-xi"),
  winOverSlider: document.getElementById("win-over-slider"),
  winTimelineChart: document.getElementById("win-timeline-chart"),
  winTimelineNote: document.getElementById("win-timeline-note"),
  winError: document.getElementById("win-error"),
  winWarning: document.getElementById("win-warning"),
  winDonut: document.getElementById("win-donut"),
  rrScore: document.getElementById("rr-score"),
  rrWickets: document.getElementById("rr-wickets"),
  rrOvers: document.getElementById("rr-overs"),
  rrTarget: document.getElementById("rr-target"),
  rrBtn: document.getElementById("rr-btn"),
  rrChart: document.getElementById("rr-chart"),
  uncertaintyChart: document.getElementById("uncertainty-chart"),
  reproPdfBtn: document.getElementById("repro-pdf-btn"),
  scoreConfidenceBtn: document.getElementById("score-confidence-btn"),
  scoreConfidenceChart: document.getElementById("score-confidence-chart"),
  tossSimNote: document.getElementById("toss-sim-note"),
  tossSimChart: document.getElementById("toss-sim-chart"),
  inningsPlan: document.getElementById("innings-plan"),
  rrError: document.getElementById("rr-error"),
  formTeam1: document.getElementById("form-team1"),
  formTeam2: document.getElementById("form-team2"),
  formRadar: document.getElementById("form-radar"),
  formBar: document.getElementById("form-bar"),
  formWin: document.getElementById("form-win"),
  formHeatmap: document.getElementById("form-heatmap"),
  formPartnership: document.getElementById("form-partnership"),
  formInsight: document.getElementById("form-insight"),
  formRefresh: document.getElementById("form-refresh"),
  formError: document.getElementById("form-error"),
  dlsScore: document.getElementById("dls-score"),
  dlsO1: document.getElementById("dls-o1"),
  dlsO2: document.getElementById("dls-o2"),
  dlsW: document.getElementById("dls-w"),
  dlsStopOver: document.getElementById("dls-stop-over"),
  dlsStopW: document.getElementById("dls-stop-w"),
  dlsRevOver: document.getElementById("dls-rev-over"),
  dlsBtn: document.getElementById("dls-btn"),
  dlsTarget: document.getElementById("dls-target"),
  dlsPar: document.getElementById("dls-par"),
  dlsR1: document.getElementById("dls-r1"),
  dlsR2: document.getElementById("dls-r2"),
  dlsExplain: document.getElementById("dls-explain"),
  dlsResourceChart: document.getElementById("dls-resource-chart"),
  dlsTargetChart: document.getElementById("dls-target-chart"),
  dlsError: document.getElementById("dls-error"),
  dlsWarning: document.getElementById("dls-warning"),
};

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

function toast(message) {
  el.toast.textContent = message;
  el.toast.classList.remove("hidden");
  setTimeout(() => el.toast.classList.add("hidden"), 1700);
}

function setOptions(select, items, labelFn, valueFn) {
  select.innerHTML = "";
  items.forEach((item) => {
    const opt = document.createElement("option");
    opt.textContent = labelFn(item);
    opt.value = valueFn(item);
    select.appendChild(opt);
  });
}

function teamName(obj) {
  return obj.team || obj.name || "";
}

function teamShortCode(name) {
  const map = {
    England: "ENG",
    "West Indies": "WI",
    India: "IND",
    Australia: "AUS",
    Pakistan: "PAK",
    "South Africa": "SA",
    "New Zealand": "NZ",
    "Sri Lanka": "SL",
    Bangladesh: "BAN",
    Afghanistan: "AFG",
  };
  return map[name] || name.slice(0, 3).toUpperCase();
}

function renderFlag(obj, cls = "team-flag") {
  if (obj.flag_img) {
    return `<img class="${cls}-img" src="${obj.flag_img}" alt="${teamName(obj)} flag" />`;
  }
  return `<span class="${cls}">${obj.flag || "🏏"}</span>`;
}

function teamLabel(obj) {
  const name = teamName(obj);
  if (obj.flag_img) return `[${teamShortCode(name)}] ${name}`;
  return `${obj.flag || "🏏"} ${name}`;
}

function clearMessages() {
  [el.setupError, el.liveError, el.scoreError, el.scoreWarning, el.explainError, el.backtestError, el.winError, el.winWarning, el.rrError, el.formError, el.dlsError, el.dlsWarning].forEach((n) => {
    n.textContent = "";
  });
  if (el.scorePhaseBreakdown) el.scorePhaseBreakdown.innerHTML = "";
  if (el.scoreAdvancedInsights) el.scoreAdvancedInsights.innerHTML = "";
}

function renderPhaseBreakdown(phaseProjection) {
  const phases = phaseProjection?.phases || [];
  if (!el.scorePhaseBreakdown) return;
  if (!phases.length) {
    el.scorePhaseBreakdown.innerHTML = "";
    return;
  }
  const cards = phases.map((p) => {
    const statusLabel = p.status === "completed" ? "Completed" : p.status === "live" ? "Live" : "Upcoming";
    const cum = p.cumulative == null ? "-" : p.cumulative;
    return `
      <article class="phase-card">
        <div class="phase-head">
          <h4>${p.phase}</h4>
          <span class="phase-status ${p.status}">${statusLabel}</span>
        </div>
        <p class="phase-overs">Overs ${p.start_over}-${p.end_over}</p>
        <p class="phase-metric">Projected add: <strong>+${p.runs}</strong></p>
        <p class="phase-metric">Projected total by phase end: <strong>${cum}</strong></p>
      </article>
    `;
  });
  el.scorePhaseBreakdown.innerHTML = cards.join("");
}

function renderAdvancedInsights(result) {
  if (!el.scoreAdvancedInsights) return;
  const inningsClosed = Boolean(result.innings_closed);
  const confidence = result.confidence || {};
  const death = result.death_context || {};
  const bowl = result.opponent_death_bowling || {};
  const shock = result.wicket_shock || {};
  const batter = result.batter_projection || {};
  const contributors = batter.contributors || [];
  const batterRows = inningsClosed
    ? `<tr><td colspan="3">Innings complete. Remaining batter projection is not applicable.</td></tr>`
    : (contributors.length
      ? contributors.map((b) => `<tr><td>${b.name}</td><td>${b.balls}</td><td>${b.runs}</td></tr>`).join("")
      : `<tr><td colspan="3">No batter simulation available.</td></tr>`);
  el.scoreAdvancedInsights.innerHTML = `
    <article class="insight-card">
      <h4>Confidence Meter</h4>
      <p class="insight-big">${confidence.score ?? "-"} <span>${confidence.band || "-"}</span></p>
      <p class="muted">Higher in late innings with tighter range.</p>
    </article>
    <article class="insight-card">
      <h4>Death Overs Venue Factor</h4>
      <p class="insight-big">${death.multiplier ?? "-"}x</p>
      <p class="muted">Est. final 5 overs RR: ${death.historical_final5_rr ?? "-"} (${death.boundary_context || "N/A"} boundaries)</p>
    </article>
    <article class="insight-card">
      <h4>Opponent Death Bowling</h4>
      <p class="insight-big">${bowl.attack_score ?? "-"} <span>${bowl.label || ""}</span></p>
      <p class="muted">Batting multiplier vs this attack: ${bowl.multiplier ?? "-"}x</p>
    </article>
    <article class="insight-card">
      <h4>Wicket Shock Model</h4>
      <p class="insight-big">${shock.next_over_wicket_prob ?? "-"}%</p>
      <p class="muted">If wicket in next over, projected total: ${shock.if_wicket_next_over_total ?? "-"}</p>
    </article>
    <article class="insight-card insight-wide">
      <h4>Remaining Batter Projection</h4>
      <p class="muted">Projected additional runs: <strong>${inningsClosed ? 0 : (batter.projected_additional_runs ?? "-")}</strong> | Projected total: <strong>${batter.projected_total ?? "-"}</strong></p>
      <table class="mini-table">
        <thead><tr><th>Batter</th><th>Balls</th><th>Runs</th></tr></thead>
        <tbody>${batterRows}</tbody>
      </table>
    </article>
  `;
}

function toNum(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function sanitizeOvers(v, maxOvers) {
  let val = Math.max(0, toNum(v, 0));
  let whole = Math.floor(val);
  let balls = Math.round((val - whole) * 10);
  if (balls > 5) balls = 5;
  if (whole > maxOvers) {
    whole = maxOvers;
    balls = 0;
  }
  return Number(`${whole}.${balls}`);
}

function debounce(fn, delay = 220) {
  let timer = null;
  return (...args) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

function pulseValue(node) {
  if (!node) return;
  node.classList.remove("updated");
  // Force reflow so repeated updates animate.
  void node.offsetWidth;
  node.classList.add("updated");
}

function animateNumber(node, target, decimals = 0, suffix = "", duration = 380) {
  if (!node) return;
  const parsed = Number(String(node.textContent || "").replace(/[^\d.-]/g, ""));
  const start = Number.isFinite(parsed) ? parsed : 0;
  const end = Number(target);
  if (!Number.isFinite(end)) {
    node.textContent = String(target);
    return;
  }
  const t0 = performance.now();
  const tick = (ts) => {
    const p = Math.min(1, (ts - t0) / duration);
    const eased = 1 - ((1 - p) ** 3);
    const value = start + ((end - start) * eased);
    node.textContent = `${value.toFixed(decimals)}${suffix}`;
    if (p < 1) {
      requestAnimationFrame(tick);
    } else {
      pulseValue(node);
    }
  };
  requestAnimationFrame(tick);
}

function setBeginnerMode(enabled) {
  state.beginnerMode = Boolean(enabled);
  document.body.classList.toggle("beginner-off", !state.beginnerMode);
}

function selectOptionByHint(selectNode, hints) {
  if (!selectNode?.options?.length) return;
  const arr = Array.isArray(hints) ? hints : [hints];
  const lowerHints = arr.map((x) => String(x || "").toLowerCase()).filter(Boolean);
  const match = Array.from(selectNode.options).find((o) => {
    const txt = `${o.value} ${o.textContent}`.toLowerCase();
    return lowerHints.some((h) => txt.includes(h));
  });
  if (match) selectNode.value = match.value;
}

function applyScorePreset(kind) {
  if (!kind) return;
  const presets = {
    flat: { pitch: ["flat", "batting paradise"], weather: ["clear", "sunny"], toss: "bat" },
    seam: { pitch: ["green", "pacer"], weather: ["cloud", "overcast"], toss: "bowl" },
    spin: { pitch: ["dry", "spinner"], weather: ["dry", "hot"], toss: "bat" },
    dew: { pitch: ["flat", "balanced"], weather: ["dew", "humid"], toss: "bowl" },
  };
  const p = presets[kind];
  if (!p) return;
  selectOptionByHint(el.scorePitch, p.pitch);
  selectOptionByHint(el.scoreWeather, p.weather);
  if (el.scoreTossDecision?.querySelector(`option[value="${p.toss}"]`)) el.scoreTossDecision.value = p.toss;
  el.presetButtons?.forEach((b) => b.classList.toggle("active", b.dataset.preset === kind));
  if (bothXIReady()) runScorePrediction();
}

function initHero3D() {
  if (!el.heroCanvas) return;
  const ensureFallback = () => {
    const parent = el.heroCanvas.parentElement;
    if (!parent) return;
    if (!parent.querySelector(".hero-fallback-ball")) {
      const ball = document.createElement("div");
      ball.className = "hero-fallback-ball";
      ball.setAttribute("aria-hidden", "true");
      parent.appendChild(ball);
    }
    parent.classList.add("hero-fallback-active");
  };
  if (!window.THREE) {
    ensureFallback();
    return;
  }
  const reduceMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
  const canvas = el.heroCanvas;
  try {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 100);
    camera.position.set(0, 0, 6.8);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    const group = new THREE.Group();
    scene.add(group);
    const ball = new THREE.Mesh(
      new THREE.IcosahedronGeometry(1.32, 5),
      new THREE.MeshStandardMaterial({ color: 0x72b7ff, metalness: 0.08, roughness: 0.32, emissive: 0x133c63, emissiveIntensity: 0.72 })
    );
    const seamA = new THREE.Mesh(
      new THREE.TorusGeometry(1.02, 0.07, 16, 72),
      new THREE.MeshStandardMaterial({ color: 0x9cf0c9, metalness: 0.22, roughness: 0.38, emissive: 0x245b4f, emissiveIntensity: 0.5 })
    );
    seamA.rotation.x = Math.PI / 2;
    const seamB = seamA.clone();
    seamB.rotation.y = Math.PI / 2;
    group.add(ball, seamA, seamB);
    const key = new THREE.PointLight(0x9bc7ff, 1.45, 38);
    key.position.set(3.4, 2.8, 5.1);
    const fill = new THREE.PointLight(0x6be7ad, 0.7, 38);
    fill.position.set(-3, -1.2, 4.2);
    scene.add(key, fill, new THREE.AmbientLight(0x6f88b7, 0.48));

    const resize = () => {
      const w = canvas.clientWidth || 600;
      const h = canvas.clientHeight || 220;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    resize();
    let raf = null;
    const animate = () => {
      ball.rotation.y += 0.0085;
      seamA.rotation.y += 0.012;
      seamB.rotation.x += 0.009;
      group.rotation.x = Math.sin(performance.now() * 0.00045) * 0.11;
      group.rotation.y += 0.0022;
      renderer.render(scene, camera);
      if (!reduceMotion) raf = requestAnimationFrame(animate);
    };
    animate();
    window.addEventListener("resize", resize);
    state.hero3d = { renderer, scene, camera, group, raf };
  } catch {
    ensureFallback();
  }
}

function renderInningsPlan(result) {
  if (!el.inningsPlan) return;
  const phases = result?.phase_projection?.phases || [];
  if (!phases.length) {
    el.inningsPlan.innerHTML = `<article class="phase-card"><p class="muted">Run score prediction to see suggested phase checkpoints.</p></article>`;
    return;
  }
  el.inningsPlan.innerHTML = phases.map((p) => {
    const target = p.cumulative == null ? "-" : p.cumulative;
    const guide = state.beginnerMode
      ? `Aim to be around ${target} by over ${p.end_over}.`
      : `Checkpoint at ${p.end_over} overs.`;
    return `<article class="phase-card"><div class="phase-head"><h4>${p.phase}</h4></div><p class="phase-metric">${guide}</p><p class="phase-overs">Projected phase add: +${p.runs}</p></article>`;
  }).join("");
}

function drawTossSimulation(scoreResult) {
  if (!el.tossSimChart) return;
  if (state.charts.tossSim) state.charts.tossSim.destroy();
  const base = toNum(scoreResult?.avg, 0);
  const weatherText = String(el.scoreWeather?.value || "").toLowerCase();
  const pitchText = String(el.scorePitch?.value || "").toLowerCase();
  const dewBoost = weatherText.includes("dew") || weatherText.includes("humid") ? 0.028 : 0;
  const spinDrag = pitchText.includes("dry") || pitchText.includes("spinner") ? 0.012 : 0;
  const batFirst = Math.round(base * (1 + spinDrag));
  const chaseFirst = Math.round(base * (1 + dewBoost - (spinDrag * 0.4)));

  state.charts.tossSim = new Chart(el.tossSimChart.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Toss: Bat First", "Toss: Bowl First"],
      datasets: [{ data: [batFirst, chaseFirst], backgroundColor: ["rgba(105,178,255,0.78)", "rgba(107,231,173,0.78)"] }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.1)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
      },
    },
  });
  if (el.tossSimNote) {
    const pref = chaseFirst > batFirst ? "Bowl first looks slightly better." : "Bat first looks slightly better.";
    el.tossSimNote.textContent = state.beginnerMode
      ? `Quick read: compare the two bars and pick the higher expected total. ${pref}`
      : `Toss simulation by current venue, pitch and weather. ${pref}`;
  }
}

function buildWinTimelineSeries(winProb, overs, maxOvers, wickets) {
  const currOver = Math.max(1, Math.min(maxOvers, Math.ceil(overs)));
  const safeProb = Math.max(1, Math.min(99, toNum(winProb, 50)));
  const wobble = Math.max(1.2, 4.2 - (Math.min(9, wickets) * 0.28));
  const finalProb = Math.max(1, Math.min(99, safeProb + ((50 - safeProb) * 0.18)));
  const labels = Array.from({ length: maxOvers }, (_, i) => i + 1);
  const values = labels.map((ov) => {
    if (ov <= currOver) {
      const t = ov / currOver;
      return Math.max(1, Math.min(99, 50 + ((safeProb - 50) * t)));
    }
    const t = (ov - currOver) / Math.max(1, (maxOvers - currOver));
    const trend = safeProb + ((finalProb - safeProb) * t);
    const wave = Math.sin((ov - currOver) * 0.65) * wobble * (1 - t);
    return Math.max(1, Math.min(99, trend + wave));
  }).map((x) => Number(x.toFixed(1)));
  return { labels, values, currOver };
}

function updateWinTimelineNote() {
  if (!el.winTimelineNote || !state.winTimelineSeries) return;
  const over = Math.max(1, Math.min(state.winTimelineSeries.labels.length, toNum(el.winOverSlider?.value, state.winTimelineSeries.currOver)));
  const idx = over - 1;
  const pct = state.winTimelineSeries.values[idx];
  el.winTimelineNote.textContent = state.beginnerMode
    ? `At over ${over}, projected win chance is about ${pct}%. Move slider to explore scenarios.`
    : `Timeline estimate at over ${over}: ${pct}%.`;
}

function drawWinTimelineChart(series) {
  if (!el.winTimelineChart) return;
  if (state.charts.winTimeline) state.charts.winTimeline.destroy();
  state.winTimelineSeries = series;
  state.charts.winTimeline = new Chart(el.winTimelineChart.getContext("2d"), {
    type: "line",
    data: {
      labels: series.labels,
      datasets: [{
        label: "Win %",
        data: series.values,
        borderColor: "#6ab4ff",
        backgroundColor: "rgba(106,180,255,0.2)",
        fill: true,
        tension: 0.22,
        pointRadius: 0,
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9", autoSkip: true, maxTicksLimit: 12 }, grid: { color: "rgba(180,200,240,0.1)" } },
        y: { min: 0, max: 100, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
      },
    },
  });
  if (el.winOverSlider) {
    el.winOverSlider.max = String(series.labels.length);
    el.winOverSlider.value = String(series.currOver);
  }
  updateWinTimelineNote();
}

function drawFormExtras(cmp) {
  if (el.formHeatmap) {
    if (state.charts.formHeatmap) state.charts.formHeatmap.destroy();
    const metrics = ["Batting", "Bowling", "Role", "Overall"];
    const t1 = [cmp.team1.batting, cmp.team1.bowling, cmp.team1.role_balance, cmp.team1.overall];
    const t2 = [cmp.team2.batting, cmp.team2.bowling, cmp.team2.role_balance, cmp.team2.overall];
    const points = [];
    for (let m = 0; m < metrics.length; m += 1) {
      points.push({ x: m + 1, y: 2, r: Math.max(5, (toNum(t1[m], 0) / 7)), label: `${cmp.team1.name} ${metrics[m]}` });
      points.push({ x: m + 1, y: 1, r: Math.max(5, (toNum(t2[m], 0) / 7)), label: `${cmp.team2.name} ${metrics[m]}` });
    }
    state.charts.formHeatmap = new Chart(el.formHeatmap.getContext("2d"), {
      type: "bubble",
      data: {
        datasets: [{
          label: "Strength Heat Bubbles",
          data: points,
          backgroundColor: points.map((p) => (p.y === 2 ? "rgba(106,180,255,0.58)" : "rgba(107,231,173,0.58)")),
          borderColor: points.map((p) => (p.y === 2 ? "rgba(106,180,255,0.92)" : "rgba(107,231,173,0.92)")),
        }],
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#e4ebfb" } },
          tooltip: { callbacks: { label: (ctx) => `${ctx.raw.label}: ${ctx.raw.r.toFixed(1)} impact` } },
        },
        scales: {
          x: {
            min: 0.5,
            max: metrics.length + 0.5,
            ticks: { color: "#a4b3d9", callback: (v) => metrics[Number(v) - 1] || "" },
            grid: { color: "rgba(180,200,240,0.12)" },
          },
          y: {
            min: 0.5,
            max: 2.5,
            ticks: { color: "#a4b3d9", callback: (v) => (Number(v) === 2 ? cmp.team1.name : Number(v) === 1 ? cmp.team2.name : "") },
            grid: { color: "rgba(180,200,240,0.12)" },
          },
        },
      },
    });
  }

  if (el.formPartnership) {
    if (state.charts.formPartnership) state.charts.formPartnership.destroy();
    const s1 = cmp.team1;
    const s2 = cmp.team2;
    const split = (team) => {
      const top = Math.max(0, (team.batting * 0.44) + (team.role_balance * 0.16));
      const mid = Math.max(0, (team.batting * 0.33) + (team.overall * 0.08));
      const fin = Math.max(0, (team.batting * 0.23) + (team.overall * 0.1));
      return [Math.round(top), Math.round(mid), Math.round(fin)];
    };
    const [aTop, aMid, aFin] = split(s1);
    const [bTop, bMid, bFin] = split(s2);
    state.charts.formPartnership = new Chart(el.formPartnership.getContext("2d"), {
      type: "bar",
      data: {
        labels: [s1.name, s2.name],
        datasets: [
          { label: "Top Order", data: [aTop, bTop], backgroundColor: "rgba(106,180,255,0.82)" },
          { label: "Middle Overs", data: [aMid, bMid], backgroundColor: "rgba(255,219,141,0.82)" },
          { label: "Finishing", data: [aFin, bFin], backgroundColor: "rgba(107,231,173,0.82)" },
        ],
      },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#e4ebfb" } } },
        scales: {
          x: { stacked: true, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
          y: { stacked: true, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        },
      },
    });
  }
}

function getSideByTeam(teamName) {
  if (state.squads.team1?.team === teamName) return "team1";
  return "team2";
}

function getXI(teamName) {
  const side = getSideByTeam(teamName);
  return Array.from(state.selectedXI[side]);
}

function bothXIReady() {
  return state.selectedXI.team1.size === 11 && state.selectedXI.team2.size === 11;
}

function updateDashboardVisibility() {
  if (state.mode === "auto") {
    el.dashboard.classList.remove("hidden");
    return;
  }
  el.dashboard.classList.toggle("hidden", !bothXIReady());
}

function autoPickXI(players, format = "odi") {
  const sorted = [...players].sort((a, b) => (b.rating || 0) - (a.rating || 0));
  const xi = [];
  const add = (list) => {
    list.forEach((p) => {
      if (!xi.some((x) => x.name === p.name) && xi.length < 11) xi.push(p);
    });
  };

  add(sorted.filter((p) => p.role === "WK-Batter").slice(0, 1));
  add(sorted.filter((p) => p.role === "Bowler").slice(0, 3));
  add(sorted.filter((p) => p.role === "All-Rounder").slice(0, 2));

  const srCut = format === "t20" ? 128 : 88;
  add(sorted.filter((p) => (p.role === "Batter" || p.role === "WK-Batter") && (p.strike_rate || 0) >= srCut).slice(0, 3));
  add(sorted);
  return xi.slice(0, 11).map((p) => p.name);
}

function updateTeamCounts() {
  el.xiTeam1Count.textContent = `${state.selectedXI.team1.size}/11 selected`;
  el.xiTeam2Count.textContent = `${state.selectedXI.team2.size}/11 selected`;
  updateXISuggestions();
  updateDashboardVisibility();
}

function xiSuggestionForSide(side) {
  const squad = state.squads[side];
  if (!squad) return null;
  const selected = squad.players.filter((p) => state.selectedXI[side].has(p.name));
  const wk = selected.filter((p) => p.role === "WK-Batter").length;
  const bowlOptions = selected.filter((p) => p.role === "Bowler" || p.role === "All-Rounder").length;
  const openerCutSr = state.format === "t20" ? 130 : 88;
  const openerCutAvg = state.format === "t20" ? 28 : 35;
  const finisherCutSr = state.format === "t20" ? 145 : 98;
  const openers = selected.filter((p) => (p.strike_rate || 0) >= openerCutSr && (p.bat_avg || 0) >= openerCutAvg).length;
  const finishers = selected.filter((p) => (p.strike_rate || 0) >= finisherCutSr).length;
  const rules = [
    { ok: wk >= 1, text: `WK: ${wk}/1 minimum` },
    { ok: bowlOptions >= 5, text: `Bowling options: ${bowlOptions}/5 minimum` },
    { ok: openers >= 2, text: `Openers: ${openers}/2 suggested` },
    { ok: finishers >= 2, text: `Finishers: ${finishers}/2 suggested` },
    { ok: state.selectedXI[side].size === 11, text: `Playing XI count: ${state.selectedXI[side].size}/11` },
  ];
  return {
    allOk: rules.every((r) => r.ok),
    rules,
  };
}

function updateXISuggestions() {
  const t1 = xiSuggestionForSide("team1");
  const t2 = xiSuggestionForSide("team2");

  const render = (node, payload) => {
    if (!payload) {
      node.textContent = "";
      return;
    }
    const lines = payload.rules
      .map((r) => `<span class="${r.ok ? "ok" : "warn"}">${r.ok ? "✓" : "⚠"} ${r.text}</span>`)
      .join("<br/>");
    node.innerHTML = lines;
    node.classList.toggle("ok", payload.allOk);
  };

  render(el.xiTeam1Suggestions, t1);
  render(el.xiTeam2Suggestions, t2);
}

function renderTeamCards() {
  el.teamGrid.innerHTML = "";
  state.meta.teams.forEach((team) => {
    const selected = state.selectedTeams.includes(team.name);
    const card = document.createElement("div");
    card.className = `team-card ${selected ? "selected" : ""}`;
    card.innerHTML = `${renderFlag(team)}<div class="team-name">${team.name}</div>`;
    card.addEventListener("click", () => {
      const idx = state.selectedTeams.indexOf(team.name);
      if (idx >= 0) {
        state.selectedTeams.splice(idx, 1);
      } else {
        if (state.selectedTeams.length >= 2) {
          toast("Select only 2 teams");
          return;
        }
        state.selectedTeams.push(team.name);
      }
      renderTeamCards();
      handleTeamSelection();
    });
    el.teamGrid.appendChild(card);
  });
}

async function handleTeamSelection() {
  clearMessages();
  if (state.selectedTeams.length !== 2) {
    el.xiSection.classList.add("hidden");
    updateDashboardVisibility();
    return;
  }

  const [t1, t2] = state.selectedTeams;
  const [s1, s2] = await Promise.all([
    api(`/api/squad?team=${encodeURIComponent(t1)}&format=${state.format}`),
    api(`/api/squad?team=${encodeURIComponent(t2)}&format=${state.format}`),
  ]);
  state.squads.team1 = s1;
  state.squads.team2 = s2;
  state.selectedXI.team1 = new Set(autoPickXI(s1.players, state.format));
  state.selectedXI.team2 = new Set(autoPickXI(s2.players, state.format));

  renderXIPanels();
  populateContextSelectors();
  if (state.mode === "manual") {
    el.xiSection.classList.remove("hidden");
  } else {
    el.xiSection.classList.add("hidden");
  }
  updateTeamCounts();
  await refreshFormComparison();
}

function renderPlayerList(container, side, players) {
  container.innerHTML = "";
  players.forEach((p) => {
    const checked = state.selectedXI[side].has(p.name) ? "checked" : "";
    const row = document.createElement("label");
    row.className = "player-row";
    row.innerHTML = `
      <input type="checkbox" data-side="${side}" data-player="${p.name}" ${checked} />
      <div>
        <strong>${p.name}</strong>
        <div class="player-meta">${p.role} | Avg ${p.bat_avg || "-"} | SR ${p.strike_rate || "-"}</div>
      </div>
      <span class="player-meta">${p.rating}</span>
    `;
    container.appendChild(row);
  });

  container.querySelectorAll("input[type='checkbox']").forEach((cb) => {
    cb.addEventListener("change", (e) => {
      const sideName = e.target.dataset.side;
      const player = e.target.dataset.player;
      if (e.target.checked) {
        if (state.selectedXI[sideName].size >= 11) {
          e.target.checked = false;
          el.setupError.textContent = "Only 11 players allowed in XI.";
          return;
        }
        state.selectedXI[sideName].add(player);
      } else {
        state.selectedXI[sideName].delete(player);
      }
      el.setupError.textContent = "";
      updateTeamCounts();
    });
  });
}

function renderXIPanels() {
  const s1 = state.squads.team1;
  const s2 = state.squads.team2;
  el.xiTeam1Title.innerHTML = `${renderFlag(s1, "title-flag")} ${s1.team}`;
  el.xiTeam2Title.innerHTML = `${renderFlag(s2, "title-flag")} ${s2.team}`;
  renderPlayerList(el.xiTeam1List, "team1", s1.players);
  renderPlayerList(el.xiTeam2List, "team2", s2.players);
  updateTeamCounts();
}

function populateContextSelectors() {
  const teams = [state.squads.team1, state.squads.team2];
  setOptions(el.scoreBattingTeam, teams, (t) => teamLabel(t), (t) => t.team);
  setOptions(el.scoreTossWinner, [{ team: "Auto", flag: "🎲" }, ...teams], (t) => teamLabel(t), (t) => t.team);
  setOptions(el.winChasingTeam, teams, (t) => teamLabel(t), (t) => t.team);
  setOptions(el.winTossWinner, [{ team: "Auto", flag: "🎲" }, ...teams], (t) => teamLabel(t), (t) => t.team);
  const regions = [{ name: "All" }, ...state.meta.regions.map((r) => ({ name: r }))];
  setOptions(el.scoreVenueRegion, regions, (r) => r.name, (r) => r.name);
  updateCountryOptions("All");
  updateVenueOptions("All", "All");
  setOptions(el.scorePitch, state.meta.pitch_types, (p) => `${p.emoji || ""} ${p.type} (${p.moisture || "-"})`, (p) => p.type);
  setOptions(el.scoreWeather, state.meta.weather_types, (w) => `${w.emoji || ""} ${w.label}`, (w) => w.label);
  el.dlsO1.value = state.meta.rules.max_overs;
  el.dlsO2.value = state.meta.rules.max_overs;
  el.winTargetSlider.max = state.format === "t20" ? 280 : 390;
  el.winScoreSlider.max = state.format === "t20" ? 280 : 390;
  if (el.winOverSlider) {
    el.winOverSlider.max = String(state.format === "t20" ? 20 : 50);
    el.winOverSlider.value = String(state.format === "t20" ? 6 : 15);
  }
  el.winTargetSlider.value = state.format === "t20" ? 180 : 285;
  el.winScoreSlider.value = state.format === "t20" ? 120 : 180;
  el.winWicketsSlider.value = 4;
  el.winTarget.value = el.winTargetSlider.value;
  el.winRuns.value = el.winScoreSlider.value;
  el.winWickets.value = el.winWicketsSlider.value;
  const defaults = state.format === "t20"
    ? { score: 72, wickets: 2, overs: 8.4, target: 178, winOvers: 10.2, dlsScore: 168, dlsW: 2 }
    : { score: 128, wickets: 3, overs: 24.2, target: 286, winOvers: 30.0, dlsScore: 286, dlsW: 3 };
  el.scoreRuns.value = defaults.score;
  el.scoreWickets.value = defaults.wickets;
  el.scoreOvers.value = defaults.overs;
  el.rrScore.value = defaults.score;
  el.rrWickets.value = defaults.wickets;
  el.rrOvers.value = defaults.overs;
  el.rrTarget.value = defaults.target;
  el.winTarget.value = defaults.target;
  el.winRuns.value = Math.max(0, defaults.score - 8);
  el.winWickets.value = defaults.wickets + 1;
  el.winOvers.value = defaults.winOvers;
  el.winTargetSlider.value = defaults.target;
  el.winScoreSlider.value = Math.max(0, defaults.score - 8);
  el.winWicketsSlider.value = defaults.wickets + 1;
  el.presetButtons?.forEach((b) => b.classList.remove("active"));
  el.dlsScore.value = defaults.dlsScore;
  el.dlsW.value = defaults.dlsW;
  el.dlsStopOver.value = "";
  el.dlsStopW.value = "";
  el.dlsRevOver.value = "";
}

function updateCountryOptions(region) {
  const filtered = region === "All" ? state.meta.venues : state.meta.venues.filter((v) => v.region === region);
  const countries = [{ name: "All" }, ...Array.from(new Set(filtered.map((v) => v.country))).sort().map((c) => ({ name: c }))];
  setOptions(el.scoreVenueCountry, countries, (c) => c.name, (c) => c.name);
}

function updateVenueOptions(region, country) {
  let venues = state.meta.venues;
  if (region !== "All") venues = venues.filter((v) => v.region === region);
  if (country !== "All") venues = venues.filter((v) => v.country === country);
  setOptions(
    el.scoreVenue,
    venues,
    (v) => `${v.name} • ${v.city}, ${v.country} (${v.region}) • Avg ${v.avg_score}`,
    (v) => v.name
  );
}

function applyBestVenueMatch(venueName) {
  if (!venueName || !el.scoreVenue?.options?.length) return;
  const incoming = String(venueName).toLowerCase();
  const exact = Array.from(el.scoreVenue.options).find((o) => String(o.value).toLowerCase() === incoming);
  if (exact) {
    el.scoreVenue.value = exact.value;
    return;
  }
  const fuzzy = Array.from(el.scoreVenue.options).find((o) => {
    const v = String(o.value).toLowerCase();
    return v.includes(incoming) || incoming.includes(v);
  });
  if (fuzzy) el.scoreVenue.value = fuzzy.value;
}

function drawWinDonut(prob) {
  if (state.charts.winDonut) state.charts.winDonut.destroy();
  state.charts.winDonut = new Chart(el.winDonut.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: ["Win", "Lose"],
      datasets: [{ data: [prob, 100 - prob], backgroundColor: ["#69b2ff", "rgba(255, 126, 126, 0.55)"], borderWidth: 1 }],
    },
    options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, cutout: "72%" },
  });
}

function drawRunRateChart(payload) {
  if (state.charts.rrLine) state.charts.rrLine.destroy();
  const labels = payload.full_labels || payload.labels;
  const datasets = [];
  const wicketOvers = Array.isArray(payload.wicket_overs) ? payload.wicket_overs : (state.lastLive?.innings_timeline?.wicket_overs || []);
  const wicketIdx = new Set(
    wicketOvers
      .map((ov) => {
        const n = Number(ov);
        if (!Number.isFinite(n) || n <= 0) return null;
        return Math.max(0, Math.min(labels.length - 1, Math.ceil(n) - 1));
      })
      .filter((v) => v != null)
  );
  if (payload.current_line) {
    datasets.push({
      label: "Actual Innings",
      data: payload.current_line,
      borderColor: "#ffd56f",
      backgroundColor: "rgba(255,213,111,0.14)",
      fill: false,
      tension: 0.34,
      cubicInterpolationMode: "monotone",
      pointRadius: (ctx) => (wicketIdx.has(ctx.dataIndex) ? 5 : 2),
      pointBackgroundColor: (ctx) => (wicketIdx.has(ctx.dataIndex) ? "#ff7f7f" : "#ffd56f"),
      pointBorderColor: (ctx) => (wicketIdx.has(ctx.dataIndex) ? "#ffb3b3" : "#ffd56f"),
    });
  }

  const fan = state.lastOutputs.uncertainty;
  // Keep trajectory chart clean in manual mode; uncertainty is shown in the dedicated chart below.
  const showBands = false;
  if (showBands && fan?.labels?.length && fan?.low?.length && fan?.avg?.length && fan?.high?.length) {
    const toFull = (arr) => {
      const out = Array(labels.length).fill(null);
      // fan starts with current over label; skip that point and map by over index.
      for (let i = 1; i < fan.labels.length; i += 1) {
        const ov = Number(fan.labels[i]);
        if (Number.isFinite(ov)) {
          const idx = Math.max(0, Math.min(labels.length - 1, Math.round(ov) - 1));
          out[idx] = arr[i];
        }
      }
      return out;
    };
    const low = toFull(fan.low);
    const avg = toFull(fan.avg);
    const high = toFull(fan.high);
    const present = (arr) => arr.filter((v) => v != null).length;
    if (present(low) <= 1 || present(avg) <= 1 || present(high) <= 1) {
      const fin = state.lastOutputs.score || {};
      const lowFinal = toNum(fin.low, toNum(fin.avg, 0));
      const avgFinal = toNum(fin.avg, lowFinal);
      const highFinal = toNum(fin.high, avgFinal);
      for (let i = 0; i < labels.length; i += 1) {
        const frac = (i + 1) / labels.length;
        low[i] = Math.round(lowFinal * frac);
        avg[i] = Math.round(avgFinal * frac);
        high[i] = Math.round(highFinal * frac);
      }
    }
    datasets.push({ label: "Low", data: low, borderColor: "rgba(255,141,141,.8)", backgroundColor: "rgba(255,141,141,.08)", fill: false, tension: 0.32, cubicInterpolationMode: "monotone", pointRadius: 0 });
    datasets.push({ label: "High", data: high, borderColor: "rgba(107,178,255,.85)", backgroundColor: "rgba(107,178,255,.18)", fill: "-1", tension: 0.32, cubicInterpolationMode: "monotone", pointRadius: 0 });
    datasets.push({ label: "Average", data: avg, borderColor: "#6be7ad", backgroundColor: "rgba(107,231,173,.1)", fill: false, tension: 0.32, cubicInterpolationMode: "monotone", pointRadius: 0 });
  } else {
    const isComplete = Boolean(state.lastLive?.innings_complete);
    if (!isComplete) {
      datasets.push({
        label: "Projected Score",
        data: payload.projected_line || payload.projected,
        borderColor: "#64b0ff",
        backgroundColor: "rgba(100,176,255,0.2)",
        fill: true,
        tension: 0.34,
        cubicInterpolationMode: "monotone",
      });
    }
  }
  if (payload.target_line) {
    const targetFull = Array(labels.length).fill(null);
    for (let i = 0; i < payload.target_line.length; i += 1) {
      const idx = (labels.length - payload.target_line.length) + i;
      if (idx >= 0 && idx < labels.length) targetFull[idx] = payload.target_line[i];
    }
    datasets.push({ label: "Target Pace", data: targetFull, borderColor: "#ff92c7", borderDash: [6, 4], fill: false, pointRadius: 0 });
  }
  state.charts.rrLine = new Chart(el.rrChart.getContext("2d"), {
    type: "line",
    data: { labels, datasets },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.15)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.15)" } },
      },
    },
  });
}

function renderLiveXIBox(node, teamName, xi, squad) {
  if (!node) return;
  if (!teamName || !Array.isArray(xi) || !xi.length) {
    node.textContent = "Playing XI not available.";
    return;
  }
  const byName = squad?.players ? new Map(squad.players.map((p) => [p.name, p])) : new Map();
  const rows = xi
    .map((name) => {
      const p = byName.get(name);
      if (!p) return `<div class="live-xi-row"><strong>${name}</strong><span>Live fetched player</span></div>`;
      return `<div class="live-xi-row"><strong>${p.name}</strong><span>${p.role} | Avg ${p.bat_avg || "-"} | SR ${p.strike_rate || "-"} | Rt ${p.rating || "-"}</span></div>`;
    })
    .join("");
  node.innerHTML = `<h4>${teamName}</h4>${rows}`;
}

function renderLiveRawXIBox(node, teamName, xi) {
  if (!node) return;
  if (!teamName || !Array.isArray(xi) || !xi.length) {
    node.textContent = "Live page squad not available.";
    return;
  }
  const rows = xi.map((name) => `<div class="live-xi-row"><strong>${name}</strong></div>`).join("");
  node.innerHTML = `<h4>${teamName}</h4>${rows}`;
}

function getLiveTeamPoints(live, teamName) {
  const raw = live?.team_progress_points?.[teamName];
  if (Array.isArray(raw) && raw.length) {
    return raw
      .map((p) => ({ x: toNum(p.over, 0), y: toNum(p.score, 0) }))
      .filter((p) => Number.isFinite(p.x) && Number.isFinite(p.y))
      .sort((a, b) => a.x - b.x);
  }
  const tl = live?.team_timelines?.[teamName];
  if (tl?.overs?.length && tl?.runs?.length) {
    return tl.overs
      .map((ov, i) => ({ x: toNum(ov, 0), y: toNum(tl.runs[i], 0) }))
      .filter((p) => Number.isFinite(p.x) && Number.isFinite(p.y))
      .sort((a, b) => a.x - b.x);
  }
  return [];
}

function phaseOrder(format) {
  return format === "t20"
    ? [{ key: "powerplay", label: "Powerplay" }, { key: "middle", label: "Middle Overs" }, { key: "death", label: "Death Overs" }]
    : [{ key: "powerplay", label: "Powerplay" }, { key: "middle", label: "Middle Overs" }, { key: "death", label: "Final Overs" }];
}

function formatOversDisplay(value) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) return "-";
  const whole = Math.floor(n);
  const balls = Math.round((n - whole) * 10);
  if (balls >= 6) return String(whole + 1);
  return balls === 0 ? String(whole) : `${whole}.${balls}`;
}

function getSelectedLiveTeams(live) {
  const mode = el.liveInningsView?.value || "both";
  if (mode === "team1") return [live.team1];
  if (mode === "team2") return [live.team2];
  return [live.team1, live.team2];
}

function wicketCountsByOver(live, teamName, maxOvers) {
  const out = Array(maxOvers).fill(0);
  const wk = live?.team_timelines?.[teamName]?.wicket_overs || [];
  wk.forEach((ov) => {
    const n = Number(ov);
    if (!Number.isFinite(n) || n <= 0) return;
    const idx = Math.max(0, Math.min(maxOvers - 1, Math.ceil(n) - 1));
    out[idx] += 1;
  });
  return out;
}

function aggregateBlocks(arr, blockSize = 5) {
  const out = [];
  for (let i = 0; i < arr.length; i += blockSize) {
    let s = 0;
    for (let j = i; j < Math.min(arr.length, i + blockSize); j += 1) s += Number(arr[j] || 0);
    out.push(s);
  }
  return out;
}

function getManhattanMode(maxOvers) {
  const mode = el.liveManhattanMode?.value || "auto";
  if (mode === "over" || mode === "block5") return mode;
  return maxOvers > 30 ? "block5" : "over";
}

function renderLiveFetchedSquad(live) {
  if (!el.liveFetchedSquad) return;
  const names = Array.isArray(live?.raw_player_names) ? live.raw_player_names : [];
  if (!names.length) {
    el.liveFetchedSquad.textContent = "No player names were parsed from this URL.";
    return;
  }
  const rows = names.slice(0, 30).map((n) => `<div class="live-xi-row"><strong>${n}</strong></div>`).join("");
  el.liveFetchedSquad.innerHTML = `<h4>Parsed Names</h4>${rows}`;
}

function renderLiveBreakdown(live) {
  if (!el.liveBreakdown) return;
  const t1 = live?.team1;
  const t2 = live?.team2;
  const bd = live?.scoring_breakdown || {};
  const phases = phaseOrder(state.format);
  if (!t1 || !t2 || !bd[t1] || !bd[t2]) {
    el.liveBreakdown.innerHTML = `<article class="phase-card"><p class="muted">Scoring breakdown unavailable.</p></article>`;
    return;
  }
  const renderTeamCol = (team) => {
    const rows = phases.map((ph) => {
      const v = bd[team]?.[ph.key] || { runs: 0, wickets: 0 };
      return `
        <article class="phase-card breakdown-row">
          <div class="phase-head"><h4>${ph.label}</h4></div>
          <p class="phase-metric"><strong>${v.runs}/${v.wickets}</strong></p>
        </article>
      `;
    }).join("");
    return `
      <section class="breakdown-team-col">
        <h4 class="breakdown-team-title">${team}</h4>
        ${rows}
      </section>
    `;
  };
  el.liveBreakdown.innerHTML = `
    <div class="breakdown-two-col">
      ${renderTeamCol(t1)}
      ${renderTeamCol(t2)}
    </div>
  `;
}

function drawLiveWormChart(live) {
  if (!el.liveWormChart) return;
  if (state.charts.liveWorm) state.charts.liveWorm.destroy();
  const t1 = live.team1;
  const t2 = live.team2;
  const d1 = getLiveTeamPoints(live, t1);
  const d2 = getLiveTeamPoints(live, t2);
  const selected = new Set(getSelectedLiveTeams(live));
  const ds = [];
  if (selected.has(t1)) ds.push({ label: t1, data: d1, parsing: false, borderColor: "#4ea8ff", backgroundColor: "rgba(78,168,255,0.15)", pointRadius: 2, tension: 0.2 });
  if (selected.has(t1)) {
    ds[ds.length - 1].pointRadius = 4;
    ds[ds.length - 1].pointHoverRadius = 5;
    ds[ds.length - 1].pointBackgroundColor = "#4ea8ff";
    ds[ds.length - 1].borderWidth = 2.4;
  }
  if (selected.has(t2)) ds.push({ label: t2, data: d2, parsing: false, borderColor: "#ff9b3f", backgroundColor: "rgba(255,155,63,0.12)", pointRadius: 4, pointHoverRadius: 5, pointBackgroundColor: "#ff9b3f", borderWidth: 2.4, tension: 0.2 });
  const maxOvers = state.meta?.rules?.max_overs || (state.format === "t20" ? 20 : 50);
  state.charts.liveWorm = new Chart(el.liveWormChart.getContext("2d"), {
    type: "line",
    data: { datasets: ds },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { type: "linear", min: 0, max: maxOvers, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Overs", color: "#a4b3d9" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Runs", color: "#a4b3d9" } },
      },
    },
  });
}

function drawLiveRunRateChart(live) {
  if (!el.liveRRChart) return;
  if (state.charts.liveRR) state.charts.liveRR.destroy();
  const interpolateScoreAt = (pts, over) => {
    if (!Array.isArray(pts) || !pts.length) return 0;
    const sorted = [...pts].sort((a, b) => a.x - b.x);
    if (over <= sorted[0].x) return Number(sorted[0].y || 0);
    for (let i = 0; i < sorted.length - 1; i += 1) {
      const a = sorted[i];
      const b = sorted[i + 1];
      if (a.x <= over && over <= b.x) {
        if (b.x === a.x) return Number(b.y || a.y || 0);
        const frac = (over - a.x) / (b.x - a.x);
        return Number(a.y || 0) + ((Number(b.y || 0) - Number(a.y || 0)) * frac);
      }
    }
    return Number(sorted[sorted.length - 1].y || 0);
  };
  const toRRSeries = (pts, maxOvers) => {
    if (!Array.isArray(pts) || !pts.length) return [];
    const maxSeen = Math.max(0, ...pts.map((p) => Number(p.x || 0)));
    const limit = Math.max(0, Math.min(maxOvers, maxSeen));
    const out = [];
    const full = Math.floor(limit);
    for (let ov = 1; ov <= full; ov += 1) {
      const scoreAt = interpolateScoreAt(pts, ov);
      out.push({ x: ov, y: Number((scoreAt / ov).toFixed(2)) });
    }
    if (limit > full) {
      const scoreAt = interpolateScoreAt(pts, limit);
      out.push({ x: Number(limit.toFixed(1)), y: Number((scoreAt / limit).toFixed(2)) });
    }
    return out;
  };
  const t1 = live.team1;
  const t2 = live.team2;
  const maxOvers = state.meta?.rules?.max_overs || (state.format === "t20" ? 20 : 50);
  const d1 = toRRSeries(getLiveTeamPoints(live, t1), maxOvers);
  const d2 = toRRSeries(getLiveTeamPoints(live, t2), maxOvers);
  const selected = new Set(getSelectedLiveTeams(live));
  const ds = [];
  if (selected.has(t1)) ds.push({ label: t1, data: d1, parsing: false, borderColor: "#4ea8ff", pointRadius: 3.5, pointHoverRadius: 5, borderWidth: 2.2, tension: 0.18 });
  if (selected.has(t2)) ds.push({ label: t2, data: d2, parsing: false, borderColor: "#ff9b3f", pointRadius: 3.5, pointHoverRadius: 5, borderWidth: 2.2, tension: 0.18 });
  state.charts.liveRR = new Chart(el.liveRRChart.getContext("2d"), {
    type: "line",
    data: { datasets: ds },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { type: "linear", min: 0, max: maxOvers, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Overs", color: "#a4b3d9" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Run Rate", color: "#a4b3d9" } },
      },
    },
  });
}

function drawLiveWicketFallChart(live) {
  if (!el.liveWicketChart) return;
  if (state.charts.liveWicketFall) state.charts.liveWicketFall.destroy();
  const maxOvers = state.meta?.rules?.max_overs || (state.format === "t20" ? 20 : 50);
  const t1 = live.team1;
  const t2 = live.team2;
  const selected = new Set(getSelectedLiveTeams(live));
  const wk1 = (live?.team_timelines?.[t1]?.wicket_overs || []).map((ov) => ({ x: Number(ov), y: 1 }));
  const wk2 = (live?.team_timelines?.[t2]?.wicket_overs || []).map((ov) => ({ x: Number(ov), y: 2 }));
  const datasets = [];
  if (selected.has(t1)) datasets.push({ label: t1, data: wk1, borderColor: "#4ea8ff", backgroundColor: "#4ea8ff", pointRadius: 6, pointHoverRadius: 7, showLine: false });
  if (selected.has(t2)) datasets.push({ label: t2, data: wk2, borderColor: "#ff9b3f", backgroundColor: "#ff9b3f", pointRadius: 6, pointHoverRadius: 7, showLine: false });
  state.charts.liveWicketFall = new Chart(el.liveWicketChart.getContext("2d"), {
    type: "scatter",
    data: { datasets },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { type: "linear", min: 0, max: maxOvers, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Over", color: "#a4b3d9" } },
        y: {
          min: 0.5,
          max: 2.5,
          ticks: {
            color: "#a4b3d9",
            stepSize: 1,
            callback: (v) => (Number(v) === 1 ? t1 : Number(v) === 2 ? t2 : ""),
          },
          grid: { color: "rgba(180,200,240,0.14)" },
          title: { display: true, text: "Team", color: "#a4b3d9" },
        },
      },
    },
  });
}

function drawConfidenceGauge(node, chartKey, score, label, color = "#6be7ad") {
  if (!node) return;
  if (state.charts[chartKey]) state.charts[chartKey].destroy();
  const val = Math.max(0, Math.min(100, Number(score || 0)));
  state.charts[chartKey] = new Chart(node.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: ["Value", "Remaining"],
      datasets: [{ data: [val, 100 - val], backgroundColor: [color, "rgba(180,200,240,0.18)"], borderWidth: 0 }],
    },
    options: {
      maintainAspectRatio: false,
      cutout: "72%",
      plugins: {
        legend: { display: false },
        title: { display: true, text: `${label}: ${val}`, color: "#d8e7ff", font: { size: 13, weight: "700" } },
      },
    },
  });
}

function renderLivePack(pack) {
  state.livePack = pack;
  if (el.liveDataQuality) el.liveDataQuality.textContent = `${pack?.data_quality?.score ?? "-"}${pack?.data_quality?.label ? ` (${pack.data_quality.label})` : ""}`;
  if (el.liveConfidence) el.liveConfidence.textContent = `${pack?.confidence?.score ?? "-"}${pack?.confidence?.label ? ` (${pack.confidence.label})` : ""}`;
  if (el.livePressure) el.livePressure.textContent = `${pack?.pressure_meter?.score ?? "-"} / 100`;

  if (el.liveMiniCommentary) {
    const lines = pack?.mini_commentary || [];
    el.liveMiniCommentary.innerHTML = lines.length ? lines.map((x) => `<li>${x}</li>`).join("") : "<li>No commentary available.</li>";
  }
  if (el.liveCoachNotes) {
    const notes = pack?.coach_notes || [];
    el.liveCoachNotes.innerHTML = notes.length ? notes.map((x) => `<li>${x}</li>`).join("") : "<li>No coach notes available.</li>";
  }
  if (el.liveSimilarity) {
    const rows = pack?.similar_matches || [];
    const note = pack?.similarity_metric_note || "Higher similarity means match flow looked more alike at the same stage.";
    el.liveSimilarity.innerHTML = rows.length
      ? `<article class="phase-card"><p class="phase-overs">${note}</p></article>` + rows.map((r) => `<article class="phase-card"><div class="phase-head"><h4>${r.match}</h4></div><p class="phase-metric">Similarity: <strong>${r.similarity ?? "-" }%</strong></p><p class="phase-overs">Compared at: ${r.at_compare_point || "-"}</p><p class="phase-overs">Final score: ${r.final_score || "-"}</p><p class="phase-overs">Result: ${r.result}</p></article>`).join("")
      : `<article class="phase-card"><p class="muted">No similar states found.</p></article>`;
  }
  if (el.livePartnershipImpact) {
    const rows = pack?.partnership_impact || [];
    el.livePartnershipImpact.innerHTML = rows.length
      ? rows.map((r) => `<article class="phase-card"><div class="phase-head"><h4>${r.label}</h4></div><p class="phase-metric">${r.runs} runs in ${r.balls} balls</p></article>`).join("")
      : `<article class="phase-card"><p class="muted">Partnership data unavailable.</p></article>`;
  }
  if (el.liveBowlerMatchups) {
    const rows = pack?.bowler_matchups || [];
    el.liveBowlerMatchups.innerHTML = rows.length
      ? rows.map((r) => `<article class="phase-card"><div class="phase-head"><h4>${r.bowler}</h4></div><p class="phase-metric">${r.phase}</p><p class="phase-overs">${r.note}</p></article>`).join("")
      : `<article class="phase-card"><p class="muted">Bowler matchups unavailable.</p></article>`;
  }

  drawConfidenceGauge(el.liveConfidenceChart, "liveConfidence", pack?.confidence?.score || 0, "Confidence", "#6be7ad");

  if (el.liveMomentumChart) {
    if (state.charts.liveMomentum) state.charts.liveMomentum.destroy();
    const strip = pack?.momentum_strip || [];
    const labels = strip.map((x) => String(x.over));
    const runs = strip.map((x) => Number(x.runs || 0));
    const wickets = strip.map((x) => (x.event === "W" ? 1 : 0));
    state.charts.liveMomentum = new Chart(el.liveMomentumChart.getContext("2d"), {
      type: "bar",
      data: {
        labels,
        datasets: [
          { label: "Runs in Over", data: runs, backgroundColor: "rgba(99,176,255,0.78)" },
          { label: "Wicket", data: wickets.map((w) => (w ? Math.max(...runs, 1) * 0.9 : 0)), backgroundColor: "rgba(255,120,120,0.75)" },
        ],
      },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#e4ebfb" } } },
        scales: {
          x: { ticks: { color: "#a4b3d9", autoSkip: true, maxTicksLimit: 18 }, grid: { color: "rgba(180,200,240,0.1)" } },
          y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
        },
      },
    });
  }
}

async function fetchLivePack() {
  if (!state.lastLive) return;
  const pack = await api("/api/live_pack", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ live: state.lastLive }),
  });
  renderLivePack(pack);
}

function pointsToManhattan(pts, maxOvers) {
  const out = Array(maxOvers).fill(0);
  if (!pts?.length) return out;
  const sorted = [...pts].sort((a, b) => a.x - b.x);
  let prevScore = 0;
  sorted.forEach((p) => {
    const overEnd = Math.max(1, Math.min(maxOvers, Math.ceil(p.x)));
    const delta = Math.max(0, p.y - prevScore);
    out[overEnd - 1] = Math.max(out[overEnd - 1], delta);
    prevScore = p.y;
  });
  return out;
}

function timelineToManhattan(live, teamName, maxOvers) {
  const tl = live?.team_timelines?.[teamName];
  if (!tl?.overs?.length || !tl?.runs?.length) return null;
  const overMap = new Map();
  tl.overs.forEach((ov, i) => {
    const oi = Math.max(1, Math.min(maxOvers, Math.round(Number(ov))));
    overMap.set(oi, Number(tl.runs[i] || 0));
  });
  const out = Array(maxOvers).fill(0);
  let prev = 0;
  for (let ov = 1; ov <= maxOvers; ov += 1) {
    const cur = overMap.has(ov) ? overMap.get(ov) : prev;
    out[ov - 1] = Math.max(0, cur - prev);
    prev = cur;
  }
  return out;
}

function drawLiveManhattanChart(live) {
  if (!el.liveManhattanChart) return;
  if (state.charts.liveManhattan) state.charts.liveManhattan.destroy();
  const t1 = live.team1;
  const t2 = live.team2;
  const maxOvers = state.meta?.rules?.max_overs || (state.format === "t20" ? 20 : 50);
  const p1 = getLiveTeamPoints(live, t1);
  const p2 = getLiveTeamPoints(live, t2);
  let d1 = timelineToManhattan(live, t1, maxOvers) || pointsToManhattan(p1, maxOvers);
  let d2 = timelineToManhattan(live, t2, maxOvers) || pointsToManhattan(p2, maxOvers);
  let w1 = wicketCountsByOver(live, t1, maxOvers);
  let w2 = wicketCountsByOver(live, t2, maxOvers);
  const mode = getManhattanMode(maxOvers);
  let labels = Array.from({ length: maxOvers }, (_, i) => String(i + 1));
  if (mode === "block5") {
    d1 = aggregateBlocks(d1, 5);
    d2 = aggregateBlocks(d2, 5);
    w1 = aggregateBlocks(w1, 5);
    w2 = aggregateBlocks(w2, 5);
    labels = Array.from({ length: d1.length }, (_, i) => `${(i * 5) + 1}-${Math.min((i + 1) * 5, maxOvers)}`);
  }
  const pxPerLabel = mode === "block5" ? 64 : 18;
  const targetWidth = Math.max(760, labels.length * pxPerLabel);
  if (mode === "over") {
    el.liveManhattanChart.style.minWidth = `${targetWidth}px`;
    el.liveManhattanChart.style.width = `${targetWidth}px`;
  } else {
    el.liveManhattanChart.style.minWidth = "100%";
    el.liveManhattanChart.style.width = "100%";
  }
  const parent = el.liveManhattanChart.parentElement;
  if (parent) parent.classList.add("chart-scroll-x");
  const selected = new Set(getSelectedLiveTeams(live));
  const datasets = [];
  if (selected.has(t1)) datasets.push({ label: t1, data: d1, wickets: w1, backgroundColor: "rgba(78,168,255,0.8)" });
  if (selected.has(t2)) datasets.push({ label: t2, data: d2, wickets: w2, backgroundColor: "rgba(255,155,63,0.8)" });
  state.charts.liveManhattan = new Chart(el.liveManhattanChart.getContext("2d"), {
    type: "bar",
    data: { labels, datasets },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#e4ebfb" } },
        wicketsOverlay: { enabled: true },
      },
      scales: {
        x: {
          ticks: { color: "#a4b3d9", maxRotation: 0, minRotation: 0, autoSkip: true, maxTicksLimit: mode === "block5" ? 12 : 25 },
          grid: { color: "rgba(180,200,240,0.1)" },
        },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Runs Per Over", color: "#a4b3d9" } },
      },
    },
    plugins: [
      {
        id: "wicketsOverlay",
        afterDatasetsDraw(chart, args, pluginOptions) {
          if (!pluginOptions?.enabled) return;
          const { ctx } = chart;
          ctx.save();
          ctx.font = "600 10px system-ui";
          ctx.textAlign = "center";
          ctx.fillStyle = "#ffd56f";
          chart.data.datasets.forEach((ds, dsIdx) => {
            const meta = chart.getDatasetMeta(dsIdx);
            const wk = Array.isArray(ds.wickets) ? ds.wickets : [];
            meta.data.forEach((bar, i) => {
              const c = wk[i] || 0;
              if (!c) return;
              const text = c > 1 ? `${c}W` : "W";
              ctx.fillText(text, bar.x, bar.y - 6);
            });
          });
          ctx.restore();
        },
      },
    ],
  });
}

function drawLiveWinProbChart(live) {
  if (!el.liveWinProbChart) return;
  if (state.charts.liveWinProb) state.charts.liveWinProb.destroy();
  const target = toNum(live.target, 0);
  const maxOvers = state.meta?.rules?.max_overs || (state.format === "t20" ? 20 : 50);
  const team1 = String(live.team1 || "Team 1");
  const team2 = String(live.team2 || "Team 2");
  const batting = String(live.batting_team || team1);
  const bowling = batting === team1 ? team2 : team1;
  const battingPts = getLiveTeamPoints(live, batting);
  const wicketOvers = live?.team_timelines?.[batting]?.wicket_overs || [];
  const parScore = Number(state.lastOutputs?.score?.par || (state.format === "t20" ? 165 : 285));

  const wicketsTill = (over) => wicketOvers.filter((w) => Number(w) <= over).length;
  const clampPct = (n) => Math.max(1, Math.min(99, Math.round(n)));
  const isFirstInningsComplete = Boolean(live?.innings_complete)
    && Math.abs(target - (toNum(live.score, 0) + 1)) <= 1;

  let battingProb = [];
  let note = "Higher % means stronger winning position at that point.";

  if (!battingPts.length) {
    battingProb = [{ x: 0, y: 50 }];
    note = "Not enough over-by-over points yet, so this starts from a neutral 50-50.";
  } else if (target > 0 && !isFirstInningsComplete) {
    battingProb = battingPts.map((p) => {
      const ballsLeft = Math.max(0, Math.round((maxOvers - p.x) * 6));
      const runsNeeded = Math.max(0, target - p.y);
      const wkLost = wicketsTill(p.x);
      if (runsNeeded <= 0) return { x: p.x, y: 99 };
      if (ballsLeft <= 0) return { x: p.x, y: 1 };
      const reqRR = runsNeeded / (ballsLeft / 6);
      const curRR = p.y / Math.max(0.2, p.x);
      const pressure = reqRR - curRR;
      const wicketsInHand = Math.max(0, 10 - wkLost);
      const prob = 55 - (pressure * 14) + ((wicketsInHand - 5) * 2.2);
      return { x: p.x, y: clampPct(prob) };
    });
    if (Boolean(live?.innings_complete)) {
      const finalWon = toNum(live.score, 0) >= target;
      battingProb[battingProb.length - 1] = { ...battingProb[battingProb.length - 1], y: finalWon ? 99 : 1 };
    }
    note = `Live chase view for ${batting}. Higher line means ${batting} is more likely to win.`;
  } else {
    battingProb = battingPts.map((p) => {
      const expected = (parScore * (p.x / maxOvers));
      const overRate = p.y / Math.max(0.2, p.x);
      const parRate = parScore / maxOvers;
      const wkPenalty = wicketsTill(p.x) * 1.3;
      const defendProb = 50 + ((p.y - expected) / 6.5) + ((overRate - parRate) * 8) - wkPenalty;
      return { x: p.x, y: clampPct(defendProb) };
    });
    note = `${batting} was batting first here. This line shows defend chance if innings ended at each stage.`;
  }

  const bowlingProb = battingProb.map((p) => ({ x: p.x, y: Math.max(1, 100 - p.y) }));
  if (el.liveWinProbNote) el.liveWinProbNote.textContent = note;

  state.charts.liveWinProb = new Chart(el.liveWinProbChart.getContext("2d"), {
    type: "line",
    data: {
      datasets: [
        {
          label: `${batting} Win %`,
          data: battingProb,
          parsing: false,
          borderColor: "#ff6b6b",
          backgroundColor: "rgba(255,107,107,0.15)",
          pointRadius: 2.8,
          pointHoverRadius: 4.2,
          borderWidth: 2.5,
          tension: 0.24,
        },
        {
          label: `${bowling} Win %`,
          data: bowlingProb,
          parsing: false,
          borderColor: "#69b2ff",
          backgroundColor: "rgba(105,178,255,0.12)",
          pointRadius: 2.2,
          pointHoverRadius: 4,
          borderDash: [5, 4],
          borderWidth: 2,
          tension: 0.24,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { type: "linear", min: 0, max: maxOvers, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.1)" }, title: { display: true, text: "Overs", color: "#a4b3d9" } },
        y: { min: 0, max: 100, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" }, title: { display: true, text: "Win Probability %", color: "#a4b3d9" } },
      },
    },
  });
}

function renderLiveDashboard(live) {
  if (!live) return;
  if (el.liveInningsView) {
    const curr = el.liveInningsView.value || "both";
    const opts = [
      { value: "both", label: "Both Teams" },
      { value: "team1", label: live.team1 || "Team 1" },
      { value: "team2", label: live.team2 || "Team 2" },
    ];
    el.liveInningsView.innerHTML = opts.map((o) => `<option value="${o.value}">${o.label}</option>`).join("");
    el.liveInningsView.value = ["both", "team1", "team2"].includes(curr) ? curr : "both";
  }
  if (el.liveFormat) el.liveFormat.textContent = String(live.format || "-").toUpperCase();
  if (el.liveCurrentInnings) el.liveCurrentInnings.textContent = `${live.batting_team || "-"} ${live.score ?? "-"} / ${live.wickets ?? "-"} (${formatOversDisplay(live.overs)})`;
  if (el.liveToss) el.liveToss.textContent = `${live.toss_winner || "Auto"} / ${live.toss_decision || "auto"}`;
  if (el.liveVenue) el.liveVenue.textContent = live.venue || "Unknown";
  renderLiveFetchedSquad(live);
  renderLiveBreakdown(live);
  drawLiveWormChart(live);
  drawLiveRunRateChart(live);
  drawLiveWicketFallChart(live);
  drawLiveWinProbChart(live);
  drawLiveManhattanChart(live);
}

function refreshScoreConfidenceGauge() {
  const conf = state.lastOutputs.score?.confidence?.score ?? 0;
  drawConfidenceGauge(el.scoreConfidenceChart, "scoreConfidence", conf, "Score Confidence", "#69b2ff");
}

function drawUncertaintyChart(fan) {
  if (!el.uncertaintyChart) return;
  if (state.charts.uncertaintyFan) state.charts.uncertaintyFan.destroy();
  state.charts.uncertaintyFan = new Chart(el.uncertaintyChart.getContext("2d"), {
    type: "line",
    data: {
      labels: fan.labels,
      datasets: [
        { label: "Low", data: fan.low, borderColor: "rgba(255, 147, 147, 0.9)", backgroundColor: "rgba(255, 147, 147, 0.06)", fill: false, tension: 0.25, pointRadius: 0 },
        { label: "High", data: fan.high, borderColor: "rgba(120, 190, 255, 0.9)", backgroundColor: "rgba(120, 190, 255, 0.20)", fill: "-1", tension: 0.25, pointRadius: 0 },
        { label: "Average", data: fan.avg, borderColor: "#6be7ad", backgroundColor: "rgba(107, 231, 173, 0.12)", fill: false, tension: 0.25, borderWidth: 2, pointRadius: 0 },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
      },
    },
  });
}

function buildFallbackUncertaintyFromTrajectory(traj, score) {
  const labels = [];
  const low = [score];
  const avg = [score];
  const high = [score];
  const projected = Array.isArray(traj?.projected_line) ? traj.projected_line : [];
  for (let i = 0; i < projected.length; i += 1) {
    const v = projected[i];
    if (v == null) continue;
    const over = i + 1;
    const p = over / Math.max(1, projected.length);
    const spread = state.format === "t20" ? (0.17 - (0.07 * p)) : (0.14 - (0.055 * p));
    labels.push(String(over));
    avg.push(v);
    low.push(Math.max(score, Math.round(v * (1 - spread))));
    high.push(Math.max(v, Math.round(v * (1 + spread))));
  }
  return { labels: [String(toNum(el.rrOvers.value, 0)), ...labels], low, avg, high };
}

async function ensureUncertaintyFromTrajectory(traj, score, wickets, overs) {
  try {
    if (bothXIReady() && state.selectedTeams.length === 2) {
      const battingTeam = el.scoreBattingTeam.value || state.selectedTeams[0];
      const bowlingTeam = state.selectedTeams.find((t) => t !== battingTeam) || state.selectedTeams[1];
      const payload = {
        format: state.format,
        batting_team: battingTeam,
        selected_xi: getXI(battingTeam),
        bowling_team: bowlingTeam,
        bowling_xi: getXI(bowlingTeam),
        toss_winner: el.scoreTossWinner.value,
        toss_decision: el.scoreTossDecision.value,
        venue: el.scoreVenue.value,
        pitch: el.scorePitch.value,
        weather: el.scoreWeather.value,
        score,
        wickets,
        overs,
      };
      const fan = await api("/api/uncertainty", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      state.lastOutputs.uncertainty = fan;
      drawUncertaintyChart(fan);
      return;
    }
  } catch {
    // Fall through to deterministic local fallback.
  }
  const fallback = buildFallbackUncertaintyFromTrajectory(traj, score);
  state.lastOutputs.uncertainty = fallback;
  drawUncertaintyChart(fallback);
}

async function runUncertaintyFan(silent = false) {
  if (!silent) clearMessages();
  try {
    if (!state.lastScorePayload) throw new Error("Run score prediction first.");
    const fan = await api("/api/uncertainty", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state.lastScorePayload),
    });
    state.lastOutputs.uncertainty = fan;
    drawUncertaintyChart(fan);
  } catch (err) {
    el.scoreError.textContent = err.message;
  }
}

async function loadLiveDemoOptions() {
  try {
    const data = await api("/api/live_demo_matches");
    const matches = data.matches || [];
    setOptions(el.liveDemoMatch, matches, (m) => `${m.title} (${m.format.toUpperCase()})`, (m) => m.id);
  } catch {
    el.liveStatus.textContent = "Unable to load demo live feeds.";
  }
}

async function loadLiveProviders() {
  try {
    const data = await api("/api/live_providers");
    const providers = (data.providers || []).filter((p) => {
      const id = String(p.id || "").toLowerCase();
      const label = String(p.label || "").toLowerCase();
      return !id.includes("espn") && !label.includes("espn");
    });
    setOptions(el.liveProvider, providers, (p) => p.label, (p) => p.id);
  } catch {
    if (el.liveProvider) {
      el.liveProvider.innerHTML = `<option value="generic">Generic JSON</option>`;
    }
  }
}

async function loadFixtures() {
  if (!el.liveFixtures) return;
  try {
    const data = await api(`/api/fixtures?format=${state.format}`);
    const fixtures = data.fixtures || [];
    el.liveFixtures.innerHTML = fixtures
      .map(
        (f, idx) => `
          <div class="fixture-item">
            <div class="fixture-row">
              <div><strong>${f.date}</strong> • ${f.title}</div>
              <button class="fixture-use" data-idx="${idx}">Use Fixture</button>
            </div>
            <div class="fixture-meta">${f.home} (Home) vs ${f.away} (Away) • ${f.status}</div>
          </div>
        `
      )
      .join("");
    const buttons = el.liveFixtures.querySelectorAll(".fixture-use");
    buttons.forEach((btn) => {
      btn.addEventListener("click", async () => {
        const idx = Number(btn.dataset.idx);
        const f = fixtures[idx];
        if (!f) return;
        await ensureTeams(f.team1, f.team2, f.format);
        renderLiveXIBox(el.liveXiTeam1, f.team1, Array.from(state.selectedXI.team1), state.squads.team1);
        renderLiveXIBox(el.liveXiTeam2, f.team2, Array.from(state.selectedXI.team2), state.squads.team2);
        el.scoreBattingTeam.value = f.team1;
        el.scoreTossWinner.value = "Auto";
        el.scoreTossDecision.value = "auto";
        el.scoreRuns.value = 0;
        el.scoreWickets.value = 0;
        el.scoreOvers.value = 0.1;
        el.liveStatus.textContent = `Fixture loaded: ${f.title} (${f.date})`;
        switchTab("score-tab");
      });
    });
  } catch {
    el.liveFixtures.textContent = "Unable to load fixtures right now.";
  }
}


function setMode(mode) {
  state.mode = mode;
  el.modeManualBtn.classList.toggle("active", mode === "manual");
  el.modeAutoBtn.classList.toggle("active", mode === "auto");
  const showManual = mode === "manual";
  el.teamGrid.closest(".shell-card").classList.toggle("hidden", !showManual);
  el.xiSection.classList.toggle("hidden", !showManual);
  el.dashboard.classList.remove("hidden");
  if (mode === "auto") {
    switchTab("live-tab");
  }
  updateDashboardVisibility();
}

function renderList(node, items = []) {
  if (!node) return;
  node.innerHTML = (items || []).map((x) => `<li>${x}</li>`).join("");
}

async function loadModelCard() {
  try {
    const card = await api("/api/model_card");
    el.aiModelType.textContent = card.model_type || "-";
    el.aiVersion.textContent = `Version: ${card.version || "-"}`;
    renderList(el.aiUses, card.what_it_uses || []);
    renderList(el.aiNotUses, card.what_it_does_not_use || []);
    renderList(el.aiLimitations, card.limitations || []);
    renderList(el.aiEthics, card.ethics_and_usage || []);
  } catch {
    el.aiModelType.textContent = "Unable to load model card.";
  }
}

async function ensureTeams(team1, team2, format = null) {
  if (format && format !== state.format) {
    state.format = format;
    el.fmtButtons.forEach((b) => b.classList.toggle("active", b.dataset.format === state.format));
    await loadMeta();
  }
  state.selectedTeams = [team1, team2];
  renderTeamCards();
  await handleTeamSelection();
}

async function runLiveIngest() {
  clearMessages();
  try {
    let fieldMap = undefined;
    const rawMap = (el.liveFieldMap.value || "").trim();
    if (rawMap) {
      try {
        fieldMap = JSON.parse(rawMap);
      } catch {
        throw new Error("Field Map JSON is invalid. Please fix JSON syntax.");
      }
    }
    const payload = {
      source: "url",
      url: el.liveUrl.value.trim(),
      provider: el.liveProvider.value || "generic",
      api_key: (el.liveApiKey?.value || "").trim() || undefined,
      root_path: (el.liveRootPath.value || "").trim() || undefined,
      field_map: fieldMap,
    };
    const urlLc = String(payload.url || "").toLowerCase();
    if (payload.provider === "generic" && urlLc.includes("cricbuzz.com")) payload.provider = "cricbuzz_html";
    const live = await api("/api/live_ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    await ensureTeams(live.team1, live.team2, live.format);
    state.lastLive = live;
    setMode("auto");

    if (Array.isArray(live.team1_xi) && live.team1_xi.length === 11 && Array.isArray(live.team1_xi_raw) && live.team1_xi_raw.length === 11) {
      state.selectedXI.team1 = new Set(live.team1_xi);
    }
    if (Array.isArray(live.team2_xi) && live.team2_xi.length === 11 && Array.isArray(live.team2_xi_raw) && live.team2_xi_raw.length === 11) {
      state.selectedXI.team2 = new Set(live.team2_xi);
    }
    renderXIPanels();
    const liveNames1 = live.team1_xi_raw || live.team1_xi || [];
    const liveNames2 = live.team2_xi_raw || live.team2_xi || [];
    renderLiveXIBox(el.liveXiTeam1, live.team1, liveNames1, null);
    renderLiveXIBox(el.liveXiTeam2, live.team2, liveNames2, null);
    renderLiveRawXIBox(el.liveRawTeam1, live.team1, live.team1_squad_raw || live.team1_xi_raw || live.team1_xi || []);
    renderLiveRawXIBox(el.liveRawTeam2, live.team2, live.team2_squad_raw || live.team2_xi_raw || live.team2_xi || []);

    el.scoreBattingTeam.value = live.batting_team;
    el.scoreTossWinner.value = live.toss_winner || "Auto";
    el.scoreTossDecision.value = live.toss_decision || "auto";
    if (live.venue) applyBestVenueMatch(live.venue);
    if (live.pitch) el.scorePitch.value = live.pitch;
    if (live.weather) el.scoreWeather.value = live.weather;
    el.scoreRuns.value = live.score;
    el.scoreWickets.value = live.wickets;
    el.scoreOvers.value = live.overs;

    el.winChasingTeam.value = state.selectedTeams.find((t) => t !== live.batting_team) || live.team2;
    if (live.target != null) el.winTarget.value = live.target;
    el.winRuns.value = live.score;
    el.winWickets.value = live.wickets;
    el.winOvers.value = live.overs;

    el.rrScore.value = live.score;
    el.rrWickets.value = live.wickets;
    el.rrOvers.value = live.overs;
    if (live.target != null) el.rrTarget.value = live.target;

    try {
      await runScorePrediction(true);
    } catch {
      // Live view should still render even if model XI is incomplete.
    }
    renderLiveDashboard(live);
    await fetchLivePack();
    const tossText = `${live.toss_winner || "Auto"} / ${live.toss_decision || "auto"}`;
    const venueText = live.venue || "Unknown";
    el.liveStatus.textContent = `Live match loaded: ${live.title} • ${live.score}/${live.wickets} (${formatOversDisplay(live.overs)}) • toss ${tossText} • venue ${venueText} • updated ${live.last_updated}`;
    switchTab("live-tab");
  } catch (err) {
    const base = err?.message || "Live fetch failed.";
    el.liveError.textContent = `${base} Please paste a valid Cricbuzz match link. If it still fails, open Advanced options and select the provider manually.`;
  }
}


async function downloadReproPdf() {
  clearMessages();
  try {
    if (!state.lastOutputs.score) throw new Error("Run score prediction first.");
    const [team1, team2] = state.selectedTeams;
    const payload = {
      format: state.format,
      team1,
      team2,
      venue: el.scoreVenue.value,
      pitch: el.scorePitch.value,
      weather: el.scoreWeather.value,
      score: toNum(el.scoreRuns.value, 0),
      wickets: toNum(el.scoreWickets.value, 0),
      overs: toNum(el.scoreOvers.value, 0),
      target: toNum(el.winTarget.value, 0),
      score_low: state.lastOutputs.score.low,
      score_avg: state.lastOutputs.score.avg,
      score_high: state.lastOutputs.score.high,
      win_prob: state.lastOutputs.win?.win_prob ?? "N/A",
      backtest_mae: state.lastOutputs.backtest?.summary?.mae ?? "N/A",
      backtest_rmse: state.lastOutputs.backtest?.summary?.rmse ?? "N/A",
      confidence: state.lastOutputs.score.confidence?.score ?? "N/A",
    };
    const res = await fetch("/api/repro_pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Unable to download reproducibility PDF");
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cricket_repro_report.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast("Reproducibility PDF downloaded");
  } catch (err) {
    el.scoreError.textContent = err.message;
  }
}

function drawFormCharts(cmp) {
  if (state.charts.radar) state.charts.radar.destroy();
  if (state.charts.bar) state.charts.bar.destroy();
  if (state.charts.formWin) state.charts.formWin.destroy();

  state.charts.radar = new Chart(el.formRadar.getContext("2d"), {
    type: "radar",
    data: {
      labels: cmp.radar_labels,
      datasets: [
        { label: cmp.team1.name, data: cmp.radar_team1, borderColor: "#63b0ff", backgroundColor: "rgba(99,176,255,.26)" },
        { label: cmp.team2.name, data: cmp.radar_team2, borderColor: "#6be7ad", backgroundColor: "rgba(107,231,173,.20)" },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        r: {
          grid: { color: "rgba(190,206,242,.18)" },
          angleLines: { color: "rgba(190,206,242,.16)" },
          pointLabels: { color: "#dce6ff" },
          ticks: { display: false },
        },
      },
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
    },
  });

  state.charts.bar = new Chart(el.formBar.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Batting", "Bowling", "Role Balance", "Overall"],
      datasets: [
        { label: cmp.team1.name, data: [cmp.team1.batting, cmp.team1.bowling, cmp.team1.role_balance, cmp.team1.overall], backgroundColor: "rgba(99,176,255,.75)" },
        { label: cmp.team2.name, data: [cmp.team2.batting, cmp.team2.bowling, cmp.team2.role_balance, cmp.team2.overall], backgroundColor: "rgba(107,231,173,.65)" },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.14)" } },
      },
    },
  });

  state.charts.formWin = new Chart(el.formWin.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: [cmp.team1.name, cmp.team2.name],
      datasets: [{ data: [cmp.team1_win_chance, cmp.team2_win_chance], backgroundColor: ["#6ab4ff", "#6be7ad"] }],
    },
    options: { maintainAspectRatio: false, plugins: { legend: { labels: { color: "#e4ebfb" } } }, cutout: "66%" },
  });
  drawFormExtras(cmp);
}

function drawExplainChart(factors) {
  if (!el.explainChart) return;
  if (state.charts.explainBar) state.charts.explainBar.destroy();
  const sorted = [...factors].sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact)).slice(0, 8);
  state.charts.explainBar = new Chart(el.explainChart.getContext("2d"), {
    type: "bar",
    data: {
      labels: sorted.map((f) => f.factor),
      datasets: [{
        label: "Impact on Final Score",
        data: sorted.map((f) => f.impact),
        backgroundColor: sorted.map((f) => (f.impact >= 0 ? "rgba(107,231,173,0.7)" : "rgba(255,140,140,0.75)")),
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
      },
    },
  });
}

function drawBacktestCharts(backtest) {
  if (state.charts.backtestScatter) state.charts.backtestScatter.destroy();
  if (state.charts.backtestPhase) state.charts.backtestPhase.destroy();
  const rows = backtest.rows || [];
  state.charts.backtestScatter = new Chart(el.backtestScatter.getContext("2d"), {
    type: "line",
    data: {
      labels: rows.map((r, i) => `S${i + 1}`),
      datasets: [
        { label: "Predicted Avg", data: rows.map((r) => r.predicted), borderColor: "#63b0ff", backgroundColor: "rgba(99,176,255,.2)", tension: 0.25 },
        { label: "Actual", data: rows.map((r) => r.actual), borderColor: "#ff8eb5", backgroundColor: "rgba(255,142,181,.15)", tension: 0.25 },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
      },
    },
  });

  const phaseMae = backtest.phase_mae || {};
  state.charts.backtestPhase = new Chart(el.backtestPhase.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Powerplay", "Middle", "Death"],
      datasets: [{
        label: "Phase MAE",
        data: [phaseMae.Powerplay, phaseMae.Middle, phaseMae.Death],
        backgroundColor: ["rgba(116,170,255,.75)", "rgba(255,219,141,.75)", "rgba(255,140,140,.75)"],
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e4ebfb" } } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        y: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
      },
    },
  });
}

function drawDLSCharts(result, firstScore) {
  if (!el.dlsResourceChart || !el.dlsTargetChart) return;
  if (state.charts.dlsResource) state.charts.dlsResource.destroy();
  if (state.charts.dlsTarget) state.charts.dlsTarget.destroy();

  state.charts.dlsResource = new Chart(el.dlsResourceChart.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Team 1 Resource", "Team 2 Resource"],
      datasets: [{ data: [result.resource_team1, result.resource_team2], backgroundColor: ["rgba(106,180,255,0.75)", "rgba(107,231,173,0.75)"] }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        y: { min: 0, max: 100, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
      },
    },
  });

  state.charts.dlsTarget = new Chart(el.dlsTargetChart.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Team 1 Score", "Par Score", "DLS Target"],
      datasets: [{ data: [firstScore, result.par_score, result.target], backgroundColor: ["rgba(140,168,217,0.75)", "rgba(255,219,141,0.75)", "rgba(122,212,255,0.78)"] }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
        y: { beginAtZero: true, ticks: { color: "#a4b3d9" }, grid: { color: "rgba(180,200,240,0.12)" } },
      },
    },
  });
}
function renderTopDrivers(drivers = []) {
  if (!el.explainTopDrivers) return;
  if (!drivers.length) {
    el.explainTopDrivers.innerHTML = "";
    return;
  }
  el.explainTopDrivers.innerHTML = drivers.map((d, idx) => `
    <article class="phase-card">
      <div class="phase-head"><h4>#${idx + 1} ${d.factor}</h4></div>
      <p class="phase-metric">Impact: <strong>${d.impact > 0 ? "+" : ""}${d.impact}</strong></p>
      <p class="phase-overs">${d.detail || ""}</p>
    </article>
  `).join("");
}

async function runExplainability(silent = false) {
  if (!silent) clearMessages();
  try {
    if (!bothXIReady()) throw new Error("Select complete XI for both teams first.");
    const battingTeam = el.scoreBattingTeam.value;
    const bowlingTeam = state.selectedTeams.find((t) => t !== battingTeam) || "";
    const maxOvers = state.meta.rules.max_overs;
    const score = Math.max(0, Math.floor(toNum(el.scoreRuns.value, 0)));
    const wickets = Math.min(10, Math.max(0, Math.floor(toNum(el.scoreWickets.value, 0))));
    const overs = sanitizeOvers(el.scoreOvers.value, maxOvers);
    const payload = {
      format: state.format,
      batting_team: battingTeam,
      selected_xi: getXI(battingTeam),
      bowling_team: bowlingTeam,
      bowling_xi: bowlingTeam ? getXI(bowlingTeam) : [],
      toss_winner: el.scoreTossWinner.value,
      toss_decision: el.scoreTossDecision.value,
      venue: el.scoreVenue.value,
      pitch: el.scorePitch.value,
      weather: el.scoreWeather.value,
      score,
      wickets,
      overs,
    };
    state.lastScorePayload = payload;
    const result = await api("/api/explain_score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    el.explainLow.textContent = result.predicted?.low ?? "-";
    el.explainAvg.textContent = result.predicted?.avg ?? "-";
    el.explainHigh.textContent = result.predicted?.high ?? "-";
    el.explainConfidence.textContent = `${result.confidence?.score ?? "-"} (${result.confidence?.band ?? "-"})`;
    const baseStory = result.storyline || "No storyline available.";
    el.explainStoryline.textContent = state.beginnerMode
      ? `Beginner view: Green bars increase predicted score, red bars decrease it. ${baseStory}`
      : baseStory;
    state.lastOutputs.explain = result;
    drawExplainChart(result.factors || []);
    renderTopDrivers(result.top_drivers || []);
  } catch (err) {
    el.explainError.textContent = err.message;
  }
}

async function runBacktest() {
  clearMessages();
  try {
    if (!bothXIReady()) throw new Error("Complete both XIs before backtesting.");
    const [team1, team2] = state.selectedTeams;
    const result = await api("/api/backtest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: state.format,
        team1,
        team2,
        xi1: getXI(team1),
        xi2: getXI(team2),
        venue: el.scoreVenue.value,
        pitch: el.scorePitch.value,
        weather: el.scoreWeather.value,
        samples: state.format === "t20" ? 42 : 49,
      }),
    });
    const s = result.summary || {};
    el.backtestSamples.textContent = s.samples ?? "-";
    el.backtestMae.textContent = s.mae ?? "-";
    el.backtestRmse.textContent = s.rmse ?? "-";
    el.backtestCalib.textContent = s.calibration_in_range_pct != null ? `${s.calibration_in_range_pct}%` : "-";
    const notes = (result.notes || []).join(" ");
    el.backtestNotes.textContent = state.beginnerMode
      ? `Beginner view: lower MAE/RMSE is better, and higher In Range % is better. ${notes}`
      : notes;
    state.lastOutputs.backtest = result;
    drawBacktestCharts(result);
  } catch (err) {
    el.backtestError.textContent = err.message;
  }
}

const presentationSteps = [
  { tab: "score-tab", title: "Step 1: Score Prediction", text: "Show live score projection with phase-wise and death-overs analytics." },
  { tab: "explain-tab", title: "Step 2: Explainable AI", text: "Explain contribution of each factor to the final prediction." },
  { tab: "backtest-tab", title: "Step 3: Backtesting", text: "Demonstrate MAE, RMSE, calibration, and phase-wise error profile." },
  { tab: "win-tab", title: "Step 4: Win Probability", text: "Move to chase forecasting and win chance insights." },
  { tab: "form-tab", title: "Step 5: Team Analytics", text: "Compare team strengths with radar, bar, and expected win split." },
  { tab: "dls-tab", title: "Step 6: DLS Engine", text: "Close with rain-interruption handling and revised target capability." },
];

async function startPresentationMode() {
  if (!bothXIReady()) {
    toast("Pick both XIs first to start presentation mode.");
    return;
  }
  state.presentation.active = true;
  state.presentation.step = 0;
  el.presentationOverlay.classList.remove("hidden");
  await runScorePrediction();
  await runExplainability(true);
  await refreshFormComparison();
  await runBacktest();
  updatePresentationStep();
}

function updatePresentationStep() {
  const step = presentationSteps[state.presentation.step];
  if (!step) return;
  switchTab(step.tab);
  el.presentationTitle.textContent = step.title;
  el.presentationText.textContent = step.text;
}

function nextPresentationStep() {
  if (!state.presentation.active) return;
  state.presentation.step += 1;
  if (state.presentation.step >= presentationSteps.length) {
    stopPresentationMode();
    return;
  }
  updatePresentationStep();
}

function stopPresentationMode() {
  state.presentation.active = false;
  state.presentation.step = 0;
  el.presentationOverlay.classList.add("hidden");
}

async function runScorePrediction(lightweight = false) {
  clearMessages();
  try {
    if (!bothXIReady()) throw new Error("Select complete XI for both teams first.");
    const battingTeam = el.scoreBattingTeam.value;
    const bowlingTeam = state.selectedTeams.find((t) => t !== battingTeam) || "";
    const maxOvers = state.meta.rules.max_overs;
    const score = Math.max(0, Math.floor(toNum(el.scoreRuns.value, 0)));
    const wickets = Math.min(10, Math.max(0, Math.floor(toNum(el.scoreWickets.value, 0))));
    const overs = sanitizeOvers(el.scoreOvers.value, maxOvers);
    el.scoreRuns.value = score;
    el.scoreWickets.value = wickets;
    el.scoreOvers.value = overs;
    if (!el.scoreVenue.value) updateVenueOptions(el.scoreVenueRegion.value || "All", el.scoreVenueCountry.value || "All");
    const payload = {
      format: state.format,
      batting_team: battingTeam,
      selected_xi: getXI(battingTeam),
      bowling_team: bowlingTeam,
      bowling_xi: bowlingTeam ? getXI(bowlingTeam) : [],
      toss_winner: el.scoreTossWinner.value,
      toss_decision: el.scoreTossDecision.value,
      venue: el.scoreVenue.value,
      pitch: el.scorePitch.value,
      weather: el.scoreWeather.value,
      score,
      wickets,
      overs,
    };
    state.lastScorePayload = payload;
    const result = await api("/api/predict_score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const lowRaw = Math.max(score, Math.floor(toNum(result.low, score)));
    const highRaw = Math.max(lowRaw + 1, Math.floor(toNum(result.high, lowRaw + 1)));
    const low = lowRaw;
    const high = highRaw;
    const avg = Math.round((low + high) / 2);
    result.low = low;
    result.avg = avg;
    result.high = high;
    animateNumber(el.scoreLow, low, 0);
    animateNumber(el.scoreAvg, avg, 0);
    animateNumber(el.scoreHigh, high, 0);
    animateNumber(el.scorePar, result.par, 0);
    const xiStrength = Number.isFinite(Number(result.team_overall)) && Number(result.team_overall) > 0 ? result.team_overall : "-";
    el.scoreNote.textContent = state.beginnerMode
      ? `${battingTeam} projected range ${low}-${high}. Higher confidence means narrower uncertainty. XI strength ${xiStrength}.`
      : `${battingTeam} projected range ${low}-${high}. XI strength ${xiStrength}.`;
    state.lastOutputs.score = result;
    refreshScoreConfidenceGauge();
    renderPhaseBreakdown(result.phase_projection);
    renderAdvancedInsights(result);
    drawTossSimulation(result);
    renderInningsPlan(result);
    if (result.warnings?.length) el.scoreWarning.textContent = result.warnings.join(" ");
    el.rrScore.value = score;
    el.rrWickets.value = wickets;
    el.rrOvers.value = overs;
    if (!el.rrTarget.value && result.avg) el.rrTarget.value = result.avg;
    if (!lightweight) {
      await runRunRatePlot(true);
      await runUncertaintyFan(true);
    }
  } catch (err) {
    el.scoreError.textContent = err.message;
  }
}

async function runWinPrediction() {
  clearMessages();
  try {
    if (!bothXIReady()) throw new Error("Select complete XI for both teams first.");
    const chasingTeam = el.winChasingTeam.value;
    const bowlingTeam = state.selectedTeams.find((t) => t !== chasingTeam);
    const maxOvers = state.meta.rules.max_overs;
    const target = Math.max(1, Math.floor(toNum(el.winTarget.value, 1)));
    const score = Math.max(0, Math.floor(toNum(el.winRuns.value, 0)));
    const wickets = Math.min(10, Math.max(0, Math.floor(toNum(el.winWickets.value, 0))));
    const overs = sanitizeOvers(el.winOvers.value, maxOvers);
    el.winTarget.value = target;
    el.winRuns.value = score;
    el.winWickets.value = wickets;
    el.winOvers.value = overs;
    if (score === 0 && wickets === 0 && overs === 0) {
      el.winPercent.textContent = "-";
      el.winRunsNeeded.textContent = "-";
      el.winBallsLeft.textContent = "-";
      el.winCrr.textContent = "-";
      el.winRrr.textContent = "-";
      el.winXi.textContent = "-";
      if (state.charts.winDonut) {
        state.charts.winDonut.destroy();
        state.charts.winDonut = null;
      }
      if (state.charts.winTimeline) {
        state.charts.winTimeline.destroy();
        state.charts.winTimeline = null;
      }
      return;
    }
    el.winTargetSlider.value = target;
    el.winScoreSlider.max = Math.max(target + 25, 60);
    el.winScoreSlider.value = Math.min(score, Number(el.winScoreSlider.max));
    el.winWicketsSlider.value = wickets;
    if (score > target + (state.format === "t20" ? 12 : 25)) {
      throw new Error("Current score is unrealistically higher than target. Please correct score/target.");
    }
    const result = await api("/api/win_probability", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: state.format,
        target,
        score,
        wickets,
        overs,
        venue: el.scoreVenue.value,
        weather: el.scoreWeather.value,
        toss_winner: el.winTossWinner.value,
        toss_decision: el.winTossDecision.value,
        chasing_team: chasingTeam,
        bowling_team: bowlingTeam,
        chasing_xi: getXI(chasingTeam),
        bowling_xi: getXI(bowlingTeam),
      }),
    });
    animateNumber(el.winPercent, result.win_prob, 0, "%");
    animateNumber(el.winRunsNeeded, result.runs_needed, 0);
    animateNumber(el.winBallsLeft, result.balls_left, 0);
    animateNumber(el.winCrr, result.crr, 2);
    if (result.rrr == null) {
      el.winRrr.textContent = "N/A";
      pulseValue(el.winRrr);
    } else {
      animateNumber(el.winRrr, result.rrr, 2);
    }
    const xiText = result.xi_validation ? `${result.xi_validation.openers}/${result.xi_validation.finishers}/${result.xi_validation.bowling_options}` : "-";
    el.winXi.textContent = xiText;
    pulseValue(el.winXi);
    state.lastOutputs.win = result;
    drawWinDonut(result.win_prob);
    drawWinTimelineChart(buildWinTimelineSeries(result.win_prob, overs, maxOvers, wickets));
    if (result.warnings?.length) el.winWarning.textContent = result.warnings.join(" ");
  } catch (err) {
    el.winError.textContent = err.message;
  }
}

async function runRunRatePlot(silent = false) {
  if (!silent) clearMessages();
  try {
    const maxOvers = state.meta.rules.max_overs;
    const score = Math.max(0, toNum(el.rrScore.value, 0));
    const wickets = Math.min(10, Math.max(0, Math.floor(toNum(el.rrWickets.value, 0))));
    const overs = sanitizeOvers(el.rrOvers.value, maxOvers);
    const target = el.rrTarget.value ? Math.max(1, toNum(el.rrTarget.value, 1)) : null;
    el.rrScore.value = score;
    el.rrWickets.value = wickets;
    el.rrOvers.value = overs;
    const result = await api("/api/trajectory", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: state.format,
        score,
        wickets,
        overs,
        target,
        current_timeline: state.lastLive?.innings_timeline || null,
        innings_complete: Boolean(state.lastLive?.innings_complete),
      }),
    });
    drawRunRateChart(result);
    await ensureUncertaintyFromTrajectory(result, score, wickets, overs);
  } catch (err) {
    el.rrError.textContent = err.message;
  }
}

async function refreshFormComparison() {
  clearMessages();
  try {
    if (!bothXIReady()) throw new Error("Complete both XIs before comparison.");
    const [team1, team2] = state.selectedTeams;
    const result = await api("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: state.format,
        team1,
        team2,
        xi1: getXI(team1),
        xi2: getXI(team2),
        venue: el.scoreVenue.value,
        weather: el.scoreWeather.value,
      }),
    });

    el.formTeam1.innerHTML = `<h3>${renderFlag(state.squads.team1, "title-flag")} ${result.team1.name}</h3><p>Batting: <strong>${result.team1.batting}</strong></p><p>Bowling: <strong>${result.team1.bowling}</strong></p><p>Role Balance: <strong>${result.team1.role_balance}</strong></p><p>Overall: <strong>${result.team1.overall}</strong></p>`;
    el.formTeam2.innerHTML = `<h3>${renderFlag(state.squads.team2, "title-flag")} ${result.team2.name}</h3><p>Batting: <strong>${result.team2.batting}</strong></p><p>Bowling: <strong>${result.team2.bowling}</strong></p><p>Role Balance: <strong>${result.team2.role_balance}</strong></p><p>Overall: <strong>${result.team2.overall}</strong></p>`;
    const xiWarn1 = result.xi_validation?.team1?.warnings?.join(" ") || "";
    const xiWarn2 = result.xi_validation?.team2?.warnings?.join(" ") || "";
    state.lastOutputs.form = result;
    el.formInsight.textContent = `Edge: ${result.edge} by ${result.gap} points. Win split: ${result.team1_win_chance}% vs ${result.team2_win_chance}%. ${xiWarn1} ${xiWarn2}`.trim();
    drawFormCharts(result);
  } catch (err) {
    el.formError.textContent = err.message;
  }
}

function numberOrNull(v) {
  return v === "" ? null : Number(v);
}

async function runDLS() {
  clearMessages();
  try {
    const stop = el.dlsStopOver.value !== "";
    const stopW = el.dlsStopW.value !== "";
    const rev = el.dlsRevOver.value !== "";
    if ((stop || stopW || rev) && !(stop && stopW && rev)) {
      throw new Error("For interruption mode, fill stoppage over, stoppage wickets, and revised total overs together.");
    }
    const maxOvers = state.meta.rules.max_overs;
    const firstScore = Math.max(1, Math.floor(toNum(el.dlsScore.value, 1)));
    const firstOvers = sanitizeOvers(el.dlsO1.value, maxOvers);
    const secondOvers = sanitizeOvers(el.dlsO2.value, maxOvers);
    const secondW = Math.min(10, Math.max(0, Math.floor(toNum(el.dlsW.value, 0))));
    el.dlsScore.value = firstScore;
    el.dlsO1.value = firstOvers;
    el.dlsO2.value = secondOvers;
    el.dlsW.value = secondW;
    const result = await api("/api/dls", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: state.format,
        first_innings_score: firstScore,
        first_innings_overs: firstOvers,
        second_innings_overs: secondOvers,
        second_innings_wickets: secondW,
        play_stopped_over: numberOrNull(el.dlsStopOver.value),
        wickets_at_stop: numberOrNull(el.dlsStopW.value),
        revised_total_overs: numberOrNull(el.dlsRevOver.value),
      }),
    });
    el.dlsTarget.textContent = result.target;
    el.dlsPar.textContent = result.par_score;
    el.dlsR1.textContent = result.resource_team1;
    el.dlsR2.textContent = result.resource_team2;
    state.lastOutputs.dls = result;
    if (el.dlsExplain) {
      const gap = Number(result.resource_team1 || 0) - Number(result.resource_team2 || 0);
      const harder = gap > 0 ? "Team 2 has fewer resources, so chase is harder." : "Team 2 resources are healthy for this chase.";
      el.dlsExplain.textContent = state.beginnerMode
        ? `Beginner view: Team 1 resource ${result.resource_team1}%, Team 2 resource ${result.resource_team2}%. ${harder}`
        : `Resource split T1 ${result.resource_team1}% vs T2 ${result.resource_team2}%. ${harder}`;
    }
    drawDLSCharts(result, firstScore);
    if (result.warnings?.length) el.dlsWarning.textContent = result.warnings.join(" ");
  } catch (err) {
    el.dlsError.textContent = err.message;
  }
}

function switchTab(tabId) {
  el.tabButtons.forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === tabId));
  el.tabPanels.forEach((panel) => panel.classList.toggle("hidden", panel.id !== tabId));
}

function wireEvents() {
  const liveWinUpdate = debounce(() => {
    if (bothXIReady()) runWinPrediction();
  }, 200);
  const liveScoreUpdate = debounce(() => {
    if (bothXIReady()) runScorePrediction();
  }, 250);

  el.fmtButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      el.fmtButtons.forEach((b) => b.classList.toggle("active", b === btn));
      state.format = btn.dataset.format;
      await loadMeta();
    });
  });
  el.modeManualBtn.addEventListener("click", () => setMode("manual"));
  el.modeAutoBtn.addEventListener("click", () => setMode("auto"));

  el.tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  el.scoreVenueRegion.addEventListener("change", () => {
    updateCountryOptions(el.scoreVenueRegion.value);
    updateVenueOptions(el.scoreVenueRegion.value, el.scoreVenueCountry.value);
  });

  el.scoreVenueCountry.addEventListener("change", () => {
    updateVenueOptions(el.scoreVenueRegion.value, el.scoreVenueCountry.value);
    liveScoreUpdate();
  });
  el.scoreVenue.addEventListener("change", liveScoreUpdate);
  el.scorePitch.addEventListener("change", liveScoreUpdate);
  el.scoreTossWinner.addEventListener("change", () => {
    liveScoreUpdate();
    liveWinUpdate();
  });
  el.scoreTossDecision.addEventListener("change", () => {
    liveScoreUpdate();
    liveWinUpdate();
  });
  el.scoreWeather.addEventListener("change", () => {
    liveScoreUpdate();
    liveWinUpdate();
  });
  el.scoreRuns.addEventListener("input", liveScoreUpdate);
  el.scoreWickets.addEventListener("input", liveScoreUpdate);
  el.scoreOvers.addEventListener("input", liveScoreUpdate);
  el.presetButtons?.forEach((btn) => {
    btn.addEventListener("click", () => applyScorePreset(btn.dataset.preset));
  });

  el.scoreBtn.addEventListener("click", runScorePrediction);
  el.liveIngestBtn.addEventListener("click", runLiveIngest);
  if (el.liveHelp) {
    el.liveHelp.textContent = "Paste one Cricbuzz match link. Open Advanced options only if needed.";
  }
  if (el.liveInningsView) {
    el.liveInningsView.addEventListener("change", () => {
      if (state.lastLive) {
        renderLiveDashboard(state.lastLive);
        if (state.livePack) renderLivePack(state.livePack);
      }
    });
  }
  if (el.liveManhattanMode) {
    el.liveManhattanMode.addEventListener("change", () => {
      if (state.lastLive) renderLiveDashboard(state.lastLive);
    });
  }
  el.reproPdfBtn.addEventListener("click", downloadReproPdf);
  if (el.scoreConfidenceBtn) el.scoreConfidenceBtn.addEventListener("click", refreshScoreConfidenceGauge);
  el.explainBtn.addEventListener("click", () => runExplainability(false));
  el.backtestBtn.addEventListener("click", runBacktest);
  el.winBtn.addEventListener("click", runWinPrediction);
  el.rrBtn.addEventListener("click", runRunRatePlot);
  el.formRefresh.addEventListener("click", refreshFormComparison);
  el.dlsBtn.addEventListener("click", runDLS);

  el.winTargetSlider.addEventListener("input", () => {
    el.winTarget.value = el.winTargetSlider.value;
    el.winScoreSlider.max = Number(el.winTargetSlider.value) + (state.format === "t20" ? 12 : 25);
    if (Number(el.winScoreSlider.value) > Number(el.winScoreSlider.max)) {
      el.winScoreSlider.value = el.winScoreSlider.max;
    }
    el.winRuns.value = el.winScoreSlider.value;
    liveWinUpdate();
  });
  el.winScoreSlider.addEventListener("input", () => {
    el.winRuns.value = el.winScoreSlider.value;
    liveWinUpdate();
  });
  el.winWicketsSlider.addEventListener("input", () => {
    el.winWickets.value = el.winWicketsSlider.value;
    liveWinUpdate();
  });
  el.winTarget.addEventListener("input", liveWinUpdate);
  el.winRuns.addEventListener("input", liveWinUpdate);
  el.winWickets.addEventListener("input", liveWinUpdate);
  el.winOvers.addEventListener("input", liveWinUpdate);
  if (el.winOverSlider) {
    el.winOverSlider.addEventListener("input", updateWinTimelineNote);
  }
  el.winChasingTeam.addEventListener("change", liveWinUpdate);
  el.winTossWinner.addEventListener("change", liveWinUpdate);
  el.winTossDecision.addEventListener("change", liveWinUpdate);
  if (el.beginnerToggle) {
    el.beginnerToggle.addEventListener("change", () => {
      setBeginnerMode(el.beginnerToggle.checked);
      if (state.lastOutputs.score) {
        renderInningsPlan(state.lastOutputs.score);
        drawTossSimulation(state.lastOutputs.score);
      }
      updateWinTimelineNote();
    });
  }
  el.presentationBtn.addEventListener("click", startPresentationMode);
  el.presentationNext.addEventListener("click", nextPresentationStep);
  el.presentationExit.addEventListener("click", stopPresentationMode);
}

async function checkBackend() {
  try {
    const data = await api("/api/status");
    el.backendStatus.textContent = `Connected: ${data.service}`;
  } catch {
    el.backendStatus.textContent = "Backend not reachable";
  }
}

async function loadMeta() {
  clearMessages();
  state.selectedTeams = [];
  state.squads = { team1: null, team2: null };
  state.selectedXI = { team1: new Set(), team2: new Set() };
  el.xiSection.classList.add("hidden");
  el.dashboard.classList.remove("hidden");
  state.meta = await api(`/api/meta?format=${state.format}`);
  renderTeamCards();
  await loadFixtures();
  updateDashboardVisibility();
}

async function init() {
  wireEvents();
  setBeginnerMode(el.beginnerToggle?.checked ?? true);
  initHero3D();
  await checkBackend();
  await loadMeta();
  await loadLiveProviders();
  setMode("manual");
}

init();
