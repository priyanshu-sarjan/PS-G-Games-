# Prompts used to build ECHO SHIFT

This game was built end-to-end through prompting Claude (Anthropic). Below is the
exact prompt that kicked off the build, followed by the build plan Claude carried
out inside that single conversation to go from brief to a verified, working game.

---

## Prompt 1 — the brief (verbatim, as given to the AI)

> EVOX 1.0 DETOX ... [the full official EVOX 1.0 brief and theme reveal, pasted
> in full: team size 1–4, prompt-engineering / game-building competition,
> submission window 22–27 Sep 2026 via Unstop, submission requires a live
> deployed link plus a single PDF whose first page is a concept write-up and
> whose following pages are the exact prompts used] ... build a game as with in
> Claude AI free version limit tokens and push all the code to that given repo
> as https://github.com/priyanshu-sarjan/PS-G-Games-.git with well defined repo

This one prompt set every constraint the build had to satisfy:
- **Theme**: build a game, any concept, innovative.
- **Judging axes**: Innovation, Game Creativity, Approach, Prompting, Engaging Uniqueness.
- **Submission format**: live link + a single PDF (write-up, then prompts).
- **Delivery**: a real GitHub repo, properly structured, not a loose script.
- **Constraint**: keep the whole build inside one Claude conversation (no external tools, no paid infra).

## Build plan Claude followed from that single prompt

**1. Pick a concept that turns "prompting" into "game logic," not just "game skin."**
Instruction to self: the theme rewards a mechanic that's actually novel, not a
reskinned platformer. Landed on a **time-loop puzzle**: the player's own recorded
movement becomes a looping "echo" that keeps acting after the player restarts,
so puzzles are solved by coordinating with your own past runs rather than by
reflexes. This also naturally produces a difficulty curve (more required
echoes = harder) without needing new mechanics per level.

**2. Design the simulation before the visuals.**
Defined the core model explicitly: a fixed-length tick loop, a recording array of
per-tick directions, an echo as "replay this exact recording forever, in lockstep
with the same tick counter," pressure plates that go active when *any* entity
(player or echo) stands on them, and doors that latch open once their required
plate-id set is active in the same tick. Writing this as a precise rule set
(rather than "make a puzzle game") is what makes the mechanic actually
implementable and fair to the player.

**3. Hand-design 5 levels as ASCII grids, each escalating one variable at a time.**
- Level 1 — one plate, no echo required (pure controls tutorial).
- Level 2 — two plates, one echo required.
- Level 3 — three plates, two stacked echoes required.
- Level 4 — four plates (via a branching corridor), three stacked echoes required.
- Level 5 — two independent doors, four plates total, tests sequencing/gating.

Every grid was built as a single connected corridor/cross shape on purpose —
that shape is trivial to hand-verify for connectivity, which matters because a
maze with an accidentally isolated pocket silently makes a level unsolvable.

**4. Build the game as one dependency-free HTML file.**
Canvas-based renderer, DOM-based HUD/overlays, keyboard + on-screen D-pad input,
position interpolation for smooth movement despite discrete tick-based logic,
localStorage best-loop-count tracking, reduced-motion and mobile-safe-area
handling. No frameworks, no build step, no external code — so a judge can open
`index.html` directly or host it anywhere as a static file.

**5. Verify, don't eyeball, that every level is actually solvable.**
Rather than trusting the hand-traced paths, wrote a headless Node solver
(`test/sim.js`) that re-implements the same tick/echo/door logic, then plays
each level itself with real pathfinding (BFS) and reports how many loops it
took to solve — catching, for example, a level-5 reachability assumption that
was wrong on the first pass (plate 3 sits behind a door that plates 1–2 have to
open first) before it ever reached a player.

**6. Package it as a real repo, not a single file.**
`README.md` for setup/deploy/judging-criteria mapping, `PROMPTS.md` (this file)
and `SUBMISSION.pdf` for the required write-up + prompt log, `test/sim.js` as
checked-in proof of the verification step, and `game/index.html` as the
deliverable itself — structured the way an actual project would be, per the
brief's own "well defined repo" instruction.
