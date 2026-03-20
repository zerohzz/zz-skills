# Visualization Patterns

Detailed implementation guidance for each interaction model.
Read the section matching your `blueprint.json` `interaction.model` value.

---

## step-sequencer

**Use when:** Tutorial, how-to, implementation walkthrough, numbered process.

**Core behavior:**
Steps are hidden by default. User reveals them in sequence.
A sticky progress indicator tracks position. Completed steps show a visual marker.
Final step triggers a completion state (subtle celebratory moment).

**Minimum viable pattern:**
```javascript
let currentStep = 0;
const steps = document.querySelectorAll('.step');
const total = steps.length;

function goTo(n) {
  steps[currentStep].classList.remove('active');
  steps[n].classList.add('active', 'seen');
  currentStep = n;
  document.getElementById('prog-fill').style.width = ((n + 1) / total * 100) + '%';
  document.getElementById('step-counter').textContent = `${n + 1} / ${total}`;
}

document.getElementById('btn-next').addEventListener('click', () => {
  if (currentStep < total - 1) goTo(currentStep + 1);
  else handleComplete();
});
```

**CSS pattern for step reveal:**
```css
.step { display: none; }
.step.active {
  display: block;
  animation: slideIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes slideIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**UX notes:**
- Allow backward navigation, but mark forward steps as "revisiting"
- On mobile: single column, full-width step cards
- Code blocks within steps: syntax-highlight and add copy button

---

## scroll-journey

**Use when:** Opinion essay, narrative, long-form argument, case study with story arc.

**Core behavior:**
Content sections reveal as user scrolls. A floating table of contents highlights the active section.
Pull quotes appear with typographic weight. Progress bar fills at top.

**Scroll reveal pattern:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      // Update ToC
      const id = entry.target.id;
      document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('active'));
      document.querySelector(`.toc-link[href="#${id}"]`)?.classList.add('active');
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -100px 0px' });

document.querySelectorAll('.section').forEach(s => observer.observe(s));
```

**Floating ToC:**
```css
.toc {
  position: fixed;
  top: 50%;
  right: 2rem;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.3s ease;
}
.toc.visible { opacity: 1; }
.toc-link { display: block; padding: 4px 0; font-size: 12px; }
.toc-link.active { color: var(--accent); font-weight: 600; }
```

**UX notes:**
- ToC appears after 200px scroll
- Pull quotes should use display font at italic weight
- Section transitions: fade + translate, not slide

---

## concept-explorer

**Use when:** Framework post, layered concept model, capability levels, mental models.

**Core behavior:**
3–7 key concepts are presented as cards or accordions. Each expands to reveal deeper explanation.
An optional "relationships" view shows how concepts connect.

**Accordion pattern:**
```javascript
document.querySelectorAll('.concept').forEach(concept => {
  const header = concept.querySelector('.concept-header');
  const body = concept.querySelector('.concept-body');

  header.addEventListener('click', () => {
    const isOpen = concept.classList.contains('open');
    // Close all
    document.querySelectorAll('.concept').forEach(c => {
      c.classList.remove('open');
      c.querySelector('.concept-body').style.maxHeight = null;
    });
    // Open clicked
    if (!isOpen) {
      concept.classList.add('open');
      body.style.maxHeight = body.scrollHeight + 'px';
    }
  });
});
```

**UX notes:**
- Each concept should have a short label (2–4 words) and a 1-sentence summary visible before expanding
- Color-code concepts if they represent distinct categories
- Include a "how they connect" callout at the bottom

---

## comparison-matrix

**Use when:** Tool review, technology comparison, tradeoff analysis, "which should I use" content.

**Core behavior:**
Options are shown as columns. Criteria are rows. Scores or indicators fill the grid.
Optional: filter criteria by importance. Bottom section: overall recommendation.

**Matrix render pattern:**
```javascript
const options = ['Option A', 'Option B', 'Option C'];
const criteria = [
  { label: 'Performance', scores: [5, 3, 4] },
  { label: 'Ease of use', scores: [3, 5, 4] },
  { label: 'Cost', scores: [4, 4, 2] }
];

function renderMatrix() {
  const table = document.getElementById('matrix');
  // Header row
  let html = '<tr><th></th>' + options.map(o => `<th>${o}</th>`).join('') + '</tr>';
  // Data rows
  criteria.forEach(({ label, scores }) => {
    html += `<tr><td>${label}</td>`;
    html += scores.map(s => `<td><span class="score score-${s}">${'●'.repeat(s)}${'○'.repeat(5-s)}</span></td>`).join('');
    html += '</tr>';
  });
  table.innerHTML = html;
}
```

**UX notes:**
- "Winner" or recommended option should be visually highlighted (border accent, not background flood)
- On mobile: show one option at a time with swipe/tap navigation
- Tradeoffs summary below the matrix: "If you care most about X, choose Y"

---

## timeline-experience

**Use when:** History, evolution, before/after, chronological progression.

**Core behavior:**
Events on a visual time axis. Click an event to expand its detail panel.
Era/period groupings where relevant. Optional: animated "journey" through events on load.

**Timeline render pattern:**
```javascript
const events = [
  { year: '2020', label: 'First event', detail: 'What happened and why it mattered.' },
  { year: '2022', label: 'Second event', detail: 'What changed.' }
];

function renderTimeline() {
  const container = document.getElementById('timeline');
  events.forEach((event, i) => {
    const el = document.createElement('div');
    el.className = 'event';
    el.innerHTML = `
      <div class="event-marker"></div>
      <div class="event-label">${event.year}</div>
      <button class="event-title" onclick="expandEvent(${i})">${event.label}</button>
      <div class="event-detail" id="detail-${i}">${event.detail}</div>
    `;
    container.appendChild(el);
  });
}

function expandEvent(i) {
  document.querySelectorAll('.event-detail').forEach((d, j) => {
    d.style.maxHeight = i === j ? d.scrollHeight + 'px' : null;
    d.closest('.event').classList.toggle('active', i === j);
  });
}
```

**UX notes:**
- Time axis can be horizontal (desktop) or vertical (mobile/long timelines)
- Use visual weight to indicate significance: larger markers for major events
- Color-code eras if chronology has clear phases

---

## architecture-explainer

**Use when:** System design, technical architecture, component flows, integration diagrams.

**Core behavior:**
A high-level diagram shows all components. Clicking a component highlights its role.
A "flow walkthrough" steps through how requests/data move through the system.

**Component highlight pattern:**
```javascript
document.querySelectorAll('.component').forEach(comp => {
  comp.addEventListener('click', () => {
    const id = comp.dataset.id;
    document.querySelectorAll('.component').forEach(c => c.classList.remove('focused'));
    comp.classList.add('focused');
    document.getElementById('component-detail').innerHTML = getDetail(id);
    document.getElementById('component-detail').classList.add('visible');
  });
});
```

**UX notes:**
- System diagram can be pure CSS/SVG — avoid external diagram libraries
- Flow walkthrough: numbered steps that highlight components in sequence
- Include a "tradeoffs" section: what this architecture optimises for and at what cost
- Code examples in context of relevant component

---

## data-dashboard

**Use when:** Statistics-heavy post, research results, benchmark data, metric-driven analysis.

**Core behavior:**
Large animated KPI numbers. Charts inline. Hover tooltips on data points.
Methodology collapsed at bottom.

**Count-up animation:**
```javascript
function animateCount(element, target, duration = 1500, suffix = '') {
  const start = performance.now();
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const value = Math.round(eased * target);
    element.textContent = value.toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// Trigger on scroll entry
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const target = parseInt(e.target.dataset.target);
      const suffix = e.target.dataset.suffix || '';
      animateCount(e.target, target, 1400, suffix);
      observer.unobserve(e.target);
    }
  });
});
document.querySelectorAll('.stat-number').forEach(el => observer.observe(el));
```

**Chart pattern (pure CSS bar chart):**
```css
.bar-chart { display: flex; align-items: flex-end; gap: 8px; height: 160px; }
.bar {
  flex: 1;
  background: var(--accent);
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.bar::after {
  content: attr(data-label);
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
}
```

**UX notes:**
- font-variant-numeric: tabular-nums on all stat numbers
- Tooltips on hover: show exact value + context
- Methodology always collapsed by default — show on expand only
