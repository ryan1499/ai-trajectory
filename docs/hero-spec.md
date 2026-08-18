# AI Takeoff Tracker — Hero Design Spec (Round 4 tournament)

> The single source of truth for this build. The Planner keeps it current; the Generator builds only
> what's here; the `design-eval` Evaluator grades against it. If reality and this file disagree, fix
> this file first.

## Goal

A 100vh hero section that makes a first-time visitor FEEL, before reading a word: (1) AI is an
exponential technology on a fast takeoff curve, (2) that takeoff decomposes into six named,
measurable forces, (3) the forces feed back into each other in a compounding loop, and (4) this
site measures each force against published forecasts and scores the forecasters. This is a
tournament round: each candidate must be a genuinely different design philosophy answering the same
brief — candidates that resemble each other are a failure of the round, not a safe choice.

## The project (grounding for every generator)

We track and measure the total AI capability takeoff. The takeoff decomposes into six forces —
COMPUTE (raw training runs), ALGORITHMS (efficiency per FLOP), CAPABILITY (autonomous task horizon),
AUTOMATION (AI speeding up AI research — the loop's hinge), CAPITAL (hyperscaler spend), PHYSICAL
(chips, power, datacenters) — which feed back into each other: more compute → better models → AI
helping build AI → more money and megawatts → more compute. Down the page, each force has its own
section with a measured series and named forecasters' claims scored against reality (27 forecasts
tracked: resolved-true / ahead / on-track / behind / pending). The hero sits above that scoreboard.

## 1. Content source of truth

> ALL wording in the build must match these strings exactly. Never fabricate, paraphrase, or alter.

- Wordmark (mast left): `AI TAKEOFF TRACKER`
- Mast right: `FORECAST SCOREBOARD · SEED DATA PREVIEW`
- Eyebrow (optional to include): `Reality, set against the forecasts`
- H1 (required, verbatim): `How fast is AI actually taking off?` — the word "actually" set in
  signal-red italic.
- Lede (required, verbatim): `Six measurable forces feed the takeoff loop. We track each one and
check the predictions against what actually happened.`
- The six force names (exact, uppercase when set in mono): `COMPUTE`, `ALGORITHMS`, `CAPABILITY`,
  `AUTOMATION`, `CAPITAL`, `PHYSICAL`.
- Optional real data available for use (no other numbers may be invented): the tally line
  `27 forecasts tracked — 1 resolved true · 1 ahead · 14 on-track · 4 behind · 7 pending`
  (verified against `data/scoreboard/claims.seed.json` resolution statuses); per-force
  verdict one-liners (verbatim from `data/scoreboard/metrics.seed.json`, curly apostrophes
  included): COMPUTE `Record frozen 12 months — bulls running behind`; ALGORITHMS `No
formal re-measurement in 28 months`; CAPABILITY `~16 hrs, doubling ~105 days; eval-gaming is the
new caveat`; AUTOMATION `0 of 5 rungs resolved; the 2x speedup fight is live`; CAPITAL `All four
forecasts on-track — the bulls’ best stage`; PHYSICAL `First resolved-true on the board:
Leopold’s ~1 GW rung`.
- Time markers if a timeline appears: 2023 … NOW (mid-2026) … open future (`?` allowed).

## 2. Asset manifest

No image assets exist. Everything visual must be code-drawn (inline SVG / CSS / canvas). Any
`<img>` tag or external URL is a fidelity fail. Google Fonts links for the three families are the
only permitted external references.

## 3. Section list

A single hero section, filling ~100vh, containing:

1. Mast — wordmark left, scoreboard label right, hairline rule.
2. Headline block — h1 (+ lede; eyebrow optional).
3. The visual thesis — the candidate's own invention (see Design direction).

Below-the-fold content is out of scope; the hero may hint at it (scroll cue optional).

## 4. Banned AI tells

> Grep the CSS/markup and reject on sight. Presence = fidelity fail.

- Dark-glow / neon gradients, glassmorphism, blurred color blobs, purple-to-cyan anything.
- Generic centered hero with a button row; stock "dashboard screenshot in a browser frame".
- Even 3-column feature-card grids with icons.
- Emoji, icon fonts, external images.
- **Project-specific traps (each caused a prior rejection — treat as banned):**
  - Forecast markers floating in chart space where the y-position carries no meaning. If forecasts
    appear plotted, their vertical position must MEAN something stated; otherwise represent
    forecasts non-positionally (counts, labels, a register, a scoreboard strip).
  - A loop/ring motif placed BESIDE a chart as decoration. Any loop motif must be structurally
    integrated (the curve grows out of it, through it, or is built from it) — or absent.
  - Labels on the curve that duplicate a legend elsewhere in the hero.
  - More than ~4 distinct line strands in any one graphic (connectors + fans + grid lattices = the
    confusion that killed rounds 1-3).

Allowed exceptions (functional, not decorative): a subtle paper-tint legibility scrim where text
overlaps a graphic; one draw-in animation respecting prefers-reduced-motion.

## 5. Design direction

- North star: an editorial measurement instrument — The Economist graphics desk, Edward Tufte,
  a metrology lab's wall chart. Serious, precise, quietly confident. NOT a startup landing page.
- Type: Bitter 900 for display; Source Serif 4 for running text; JetBrains Mono for labels/data.
  Typography may itself be the visual thesis in a candidate.
- Color / ground: paper `#eef0e9`, ink `#1c2b28`, moss `#3c5c48`, moss-deep `#24392d`, signal
  `#b5432a`, gold `#a8863a`. Stage colors in order COMPUTE→PHYSICAL: `#24392d`, `#3c5c48`,
  `#5d7a5e`, `#88936f`, `#a8863a`, `#b5432a`. Dark-ground candidates are permitted if they stay
  within this family (e.g. ink/moss-deep ground with paper type).
- The signature move: EACH CANDIDATE MUST DECLARE ITS OWN in a code comment at the top of the file
  ("SIGNATURE: ..."), and the five signatures must be different in kind, not degree. Candidate
  philosophies must span at least four of these axes: (a) curve-led composition, (b) typography-led
  (the six forces as typographic architecture), (c) diagram-led (the feedback loop as the hero
  object), (d) data-led (real verdicts/tally as the visual), (e) abstract/field (pattern, texture,
  or generative field expressing compounding), (f) split/asymmetric editorial layout. No two
  candidates may share an axis.
- Feedback-loop integration test (applies to any candidate using a loop motif): cover the loop with
  your hand and the composition should feel amputated, not cleaner. If it feels cleaner, the loop
  was decoration — fail.
- Responsive: composed for ~1440×900 primarily; must not break at 1280; graceful single-column at
  ≤900 (no clipped labels, no horizontal scroll).
- Technical: self-contained index.html per candidate, HTML+CSS+vanilla JS only, no dependencies
  beyond Google Fonts. Hero ≈100vh including mast.

## Open / unverified

- Whether the eyebrow survives — candidate's call; evaluator should not penalize either way.
- Motion budget beyond one draw-in — candidate's call, prefers-reduced-motion required.
- The tally line's placement (in-hero vs below) — candidates may use or omit it.
