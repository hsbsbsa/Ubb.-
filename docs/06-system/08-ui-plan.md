# UI Plan

Korean-first UI for text-heavy screens; English available. Manuscript views default to a **mobile-width
column** (≈ 380 px, 16–17 px Korean font, generous line height) because webnovels are read on phones.

## 1. Navigation

```
Workspace ▸ Projects
  Project
   ├ Overview        (status, canon version, spend, next actions, attention items)
   ├ Requirements    (spec: hard/soft/assumptions; directions timeline)
   ├ Concept         (candidates, comparison)
   ├ Bible           (characters | speech profiles | world | power system | factions | locations | glossary | style profile)
   ├ Plan            (blueprint | seasons | arcs | chapter contracts board)
   ├ Chapters        (list, batch controls, review queue)
   │   └ Chapter     (manuscript | scorecard | issues | candidates | trace | canon delta)
   ├ Canon           (timeline | entities/state | knowledge matrix | relationships | promises | commits/stale)
   ├ Jobs            (running, paused, attention; SSE progress)
   ├ Costs           (dashboards, budgets, predictions)
   └ Export
Workspace settings (members, providers/privacy, budgets, audit log)
```

## 2. Key screens

### Requirements & Assumption Review
Two-column: left = grouped requirement cards with kind badge (필수/선호/가정) and provenance; right = detail
with edit, confirm/reject for assumptions, conflict banners. Bulk actions. Direction composer with scope
picker and re-plan preview (which contracts become stale).

### Concept Compare
Side-by-side cards; judge verdicts in both orders shown transparently ("A>B in order 1, A>B in order 2");
merge mode with per-field picker.

### Bible
Entity list + editor. Speech profile editor: matrix of counterpart → speech level/address terms with
validity (e.g., "ch.87부터 반말"). Style Profile page: overlays (chips), overrides (numeric with sane ranges),
forbidden expressions, **compiled Style Block preview** per role, exemplar bank manager (provenance labels).
Lock toggles with lock icon; locked facts listed in a "Locked canon" panel.

### Plan
Blueprint page (promise, conflict, arcs, ending, endgame requirements with satisfaction status). Season
board (columns) → arc cards → chapter contract chips (status colors: draft/validated/approved/stale/
realized). Contract editor with validation panel (canon/plan/style checks) and cadence strip (last 10
chapters' ending/payoff types).

### Chapter Review (the most-used screen)
Left: manuscript (mobile column) with paragraph IDs, inline issue highlights (color by severity), patch diff
toggle, version selector. Right tabs: **Scorecard** (dimension scores, tier threshold), **Issues** (grouped;
each with claim, span jump, conflicting canon item, canon evidence quote + deep link to earlier chapter,
repair suggestion, actions: patch / override / dismiss), **Candidates** (side-by-side + verdicts),
**Canon delta preview** (facts/events/knowledge/relationships/promises to be committed, with evidence,
single-source flags, adjudications), **Trace** (packs, calls, costs). Footer actions: Approve · Request
changes (text box) · Reject · Regenerate. Keyboard shortcuts for queue review.

### Canon Inspectors
- **Timeline**: horizontal story clock; lanes per timeline; frame filters; click → event detail w/ evidence.
- **Entity state**: attribute table with validity ranges and evidence; "as of chapter k" slider; history.
- **Knowledge matrix**: rows propositions (search/filter secrets), columns knowers (characters + narrator +
  reader); cells stance icons (✓ knows, ? suspects, ✗ believes false + tooltip value, 🎭 pretends, — unaware);
  slider "as of chapter k".
- **Relationships**: graph with directed edges; pair drawer (axes, address terms, speech level, history).
- **Promises**: board by status; due windows; overdue badges; link to setup/payoff evidence.
- **Commits & stale**: commit list with delta viewer; stale artifacts with reasons and actions (revalidate/
  regenerate/dismiss).

### Jobs & Attention
Job cards with step progress, spend vs budget, ETA; attention queue with failure class and recommended
actions; trace view for retries.

### Costs
Charts by role/model/chapter; cost per accepted chapter & per 1,000 chars; predictions; budget editor with
hard/soft limits.

### Export
Scope/format/options; history with signed links; disclosure text editor.

## 3. Interaction principles

- Every warning shows **evidence** and a **jump link**; no bare "inconsistent" messages.
- Approvals are explicit; auto-approvals are labeled and reversible via rollback (latest) or regeneration.
- Destructive actions (reject, retcon, rollback, delete) require confirmation with impact summary.
- Progress is live (SSE) with per-step costs.
- Korean typography: proper quotation marks, no widows for dialogue lines in preview.

## 4. Accessibility & i18n
Keyboard-first review; ARIA on issue lists; i18n via message catalogs (ko default, en); dates in user
locale; Korean text never auto-translated.
