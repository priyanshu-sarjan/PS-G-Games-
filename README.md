# ECHO SHIFT

A browser-based time-loop puzzle game built for **EVOX 1.0 — DETOX** (theme: *Build a Game, Any Concept, Any Type*).

**Play it live:** _add your deployed link here after publishing (see Deploying below)_

## The idea

You control one body, but every time a loop ends, that run is kept as a translucent **echo** that repeats itself forever. You start the next loop from scratch while your echoes keep moving in the background.

Some doors only open when several pressure plates are held down **at the same instant** — something one body physically cannot do alone. The puzzle is figuring out which loop should do what, and layering your echoes until, together, they can.

5 hand-built levels ramp from a plain walk (learn the controls) up to a level with **two independent doors and four echoes working at once**.

## Controls

| Action | Key | Touch |
|---|---|---|
| Move | Arrow keys / WASD | on-screen D-pad |
| End the current loop early | `L` | "↻ Loop" button |
| Restart the level | `R` | "Restart" button |

## Project structure

```
echo-shift/
├─ game/
│  └─ index.html      ← the entire game (HTML + CSS + JS, no build step, no dependencies)
├─ test/
│  └─ sim.js           ← a headless Node script that re-implements the core
│                          simulation and verifies every level is solvable
│                          before shipping (run: node test/sim.js)
├─ PROMPTS.md           ← the prompts used to design and build this game
├─ SUBMISSION.pdf        ← the write-up + prompt log, formatted for the Unstop submission
└─ README.md
```

## Running it locally

No build step, no dependencies. Just open the file:

```bash
open game/index.html        # macOS
# or
xdg-open game/index.html    # Linux
# or just double-click it / drag it into a browser tab
```

## Verifying the levels

Every level's grid, plate placement, and door requirements are checked by a small
headless solver before anything ships — it plays each level itself (pathfinding
with BFS, standing on plates, letting doors open, walking to the exit) and confirms
it's solvable within the intended number of loops:

```bash
node test/sim.js
```

## Deploying (for the "Live Deployed Link" submission requirement)

The game is a single static HTML file, so any static host works. The two fastest options:

**GitHub Pages** (uses this repo directly, no extra account needed):
1. Push this repo to GitHub (see below).
2. Repo → Settings → Pages → Source: `Deploy from a branch` → Branch: `main`, folder: `/game` (or move `index.html` to the repo root and select `/root` if your Pages setup requires that).
3. Your live link will be `https://<your-username>.github.io/<repo-name>/`.

**Netlify / Vercel drop**: drag the `game` folder onto netlify.com/drop for an instant link — no account required for Netlify Drop.

## Pushing this repo to GitHub

```bash
git init
git add .
git commit -m "Echo Shift: a time-loop puzzle game for EVOX 1.0"
git branch -M main
git remote add origin https://github.com/priyanshu-sarjan/PS-G-Games-.git
git push -u origin main
```

## Why this fits the brief

- **Innovation / Engaging uniqueness** — the "echo" mechanic turns a normal grid puzzle into a coordination problem with your own past selves; the difficulty comes from timing and planning, not reflexes.
- **Game creativity** — 5 levels escalate from 1 plate/no echo to 4 plates + 2 independent doors needing 3 stacked echoes.
- **Approach** — the design was scoped, drafted level-by-level with hand-traced grid connectivity, then verified with an automated headless solver (`test/sim.js`) rather than eyeballed.
- **Prompting** — see `PROMPTS.md` and `SUBMISSION.pdf` for the exact prompts used end-to-end.
