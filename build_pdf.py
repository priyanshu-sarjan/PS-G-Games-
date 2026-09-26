from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.enums import TA_LEFT

styles = getSampleStyleSheet()

title_style = ParagraphStyle('TitleX', parent=styles['Title'], fontSize=26, spaceAfter=4, textColor=colors.HexColor('#12121f'))
subtitle_style = ParagraphStyle('SubtitleX', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#4ea8de'), spaceAfter=18)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#12121f'))
h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11.5, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#2a2a45'))
body = ParagraphStyle('BodyX', parent=styles['Normal'], fontSize=10.2, leading=15, alignment=TA_LEFT, spaceAfter=6)
body_muted = ParagraphStyle('BodyMuted', parent=body, textColor=colors.HexColor('#555'))
quote = ParagraphStyle('Quote', parent=body, leftIndent=14, textColor=colors.HexColor('#333'),
                        borderColor=colors.HexColor('#4ea8de'), borderWidth=0, backColor=colors.HexColor('#f3f6fa'))
mono = ParagraphStyle('Mono', parent=body, fontName='Courier', fontSize=9, leading=13, backColor=colors.HexColor('#f4f4f8'))
label = ParagraphStyle('Label', parent=body, fontSize=8.5, textColor=colors.HexColor('#888'), spaceAfter=2)

doc = SimpleDocTemplate("/home/claude/echo-shift/SUBMISSION.pdf", pagesize=LETTER,
                         topMargin=0.9*inch, bottomMargin=0.8*inch,
                         leftMargin=0.9*inch, rightMargin=0.9*inch,
                         title="ECHO SHIFT — EVOX 1.0 Submission", author="Team submission — EVOX 1.0")

story = []

# ---------------- PAGE 1: WRITE-UP ----------------
story.append(Paragraph("ECHO SHIFT", title_style))
story.append(Paragraph("A time-loop puzzle game — submitted for EVOX 1.0 (DETOX), \"Build a Game\"", subtitle_style))
story.append(HRFlowable(width="100%", color=colors.HexColor('#ddd'), thickness=1))

story.append(Paragraph("Concept", h2))
story.append(Paragraph(
    "Echo Shift is a browser-based puzzle game built around a single idea: your own past "
    "actions don't disappear when a loop ends — they keep happening. Every time a timed loop "
    "finishes, the run you just made is kept as a translucent <b>echo</b> that repeats those exact "
    "movements forever, tick for tick, while you start the next loop from the beginning with a "
    "clean slate.", body))
story.append(Paragraph(
    "The puzzles are built from that one rule. Certain doors only open when several pressure "
    "plates are held down at the same instant — something a single body cannot do. So the "
    "player has to plan across loops: one loop to place an echo on plate A, a second to place "
    "another echo on plate B, and a final loop where the live player reaches plate C while both "
    "echoes are still replaying their parts, all lining up on the same tick. The challenge is "
    "entirely about sequencing and timing, not reflexes.", body))

story.append(Paragraph("Gameplay & progression", h2))
story.append(ListFlowable([
    ListItem(Paragraph("<b>Level 1 — First Steps:</b> one plate, no echo needed. Pure movement tutorial.", body)),
    ListItem(Paragraph("<b>Level 2 — Two Hands:</b> two plates, one door. Requires exactly one echo.", body)),
    ListItem(Paragraph("<b>Level 3 — Triangulation:</b> three plates. Requires two stacked echoes plus the live player.", body)),
    ListItem(Paragraph("<b>Level 4 — Branch Point:</b> four plates reached via a branching corridor. Requires three stacked echoes.", body)),
    ListItem(Paragraph("<b>Level 5 — Two Doors:</b> four plates behind two independent, sequential locks — tests planning order, not just echo count.", body)),
], bulletType='bullet', start='circle'))
story.append(Paragraph(
    "Controls are arrow keys / WASD to move, <b>L</b> to end a loop early, and <b>R</b> to restart. "
    "A touch D-pad and on-screen buttons make it playable on mobile as well.", body))

story.append(Paragraph("Approach", h2))
story.append(Paragraph(
    "The mechanic was designed as an explicit rule set before any code was written: a fixed-length "
    "tick loop, a recorded direction per tick, an echo that replays its recording in lockstep with "
    "the same tick counter every loop, and doors that latch open the moment their required plate-ids "
    "are all simultaneously active. Levels were hand-authored as simple connected corridor/cross-shaped "
    "grids specifically because that shape is easy to verify by hand has no isolated, unreachable pockets.", body))
story.append(Paragraph(
    "Rather than trusting that by eye, every level was additionally checked with a small headless "
    "solver script that re-implements the same simulation and plays each level itself with real "
    "pathfinding — confirming each one is actually solvable within its loop budget before it was "
    "considered finished. That check caught a real sequencing bug on Level 5 during development "
    "(a plate that was assumed reachable immediately actually sits behind the first door).", body))

story.append(Paragraph("Tech", h2))
story.append(Paragraph(
    "Single self-contained HTML file — vanilla JavaScript and the Canvas API, no frameworks, no "
    "build step, no external runtime dependencies (only Google Fonts for typography). This keeps "
    "it trivial to host as a static page (GitHub Pages, Netlify, Vercel) and trivial for a judge "
    "to run locally by opening the file directly.", body))

story.append(Paragraph("Team", h2))
story.append(Paragraph("Team size: 1–4 (per competition rules). Repository: "
                        "github.com/priyanshu-sarjan/PS-G-Games-", body))

story.append(PageBreak())

# ---------------- PAGE 2+: PROMPTS ----------------
story.append(Paragraph("Prompts used to build this game", title_style))
story.append(Paragraph("Exact prompt log, as required by the submission guidelines", subtitle_style))
story.append(HRFlowable(width="100%", color=colors.HexColor('#ddd'), thickness=1))

story.append(Paragraph("Prompt 1 — the brief (verbatim, as given to the AI)", h2))
story.append(Paragraph(
    "The build began from a single prompt to Claude (Anthropic) that pasted the full official "
    "EVOX 1.0 brief and theme reveal in full — team size 1–4, the prompt-engineering / "
    "game-building competition format, the 22–27 Sep 2026 Unstop submission window, and the "
    "requirement for a live deployed link plus a single PDF (concept write-up, then exact "
    "prompts) — followed by this instruction:", body))
story.append(Paragraph(
    "&ldquo;build a game as with in Claude AI free version limit tokens and push all the code to "
    "that given repo as https://github.com/priyanshu-sarjan/PS-G-Games-.git with well defined "
    "repo&rdquo;", quote))
story.append(Paragraph(
    "That single prompt set every constraint the build had to satisfy: an innovative game judged "
    "on Innovation, Game Creativity, Approach, Prompting and Engaging Uniqueness; a live link plus "
    "a two-part PDF; delivery as a proper GitHub repository rather than a loose file; and the whole "
    "build done inside one AI conversation, without external paid tooling.", body))

story.append(Paragraph("Build plan carried out from that prompt", h2))

story.append(Paragraph("1. Pick a concept where the mechanic itself is the prompt-engineering payoff", h3))
story.append(Paragraph(
    "Decided against a reskinned platformer or quiz in favor of a mechanic where the core loop "
    "is genuinely new: a time-loop puzzle in which the player's own recorded movement becomes an "
    "\"echo\" that keeps acting after the player restarts. This also produces a natural, reusable "
    "difficulty curve — more required echoes — without inventing new mechanics per level.", body))

story.append(Paragraph("2. Design the simulation rules before any visuals", h3))
story.append(Paragraph(
    "Wrote out the exact rule set: a fixed-length tick loop; a per-tick recording array; an echo "
    "that replays its recording in lockstep with the same global tick counter every loop; pressure "
    "plates active when any entity (player or echo) occupies them; and doors that latch open "
    "permanently the instant their required plate-id set is simultaneously active. Precise rules, "
    "not a vague description, are what make an emergent mechanic actually fair and solvable.", body))

story.append(Paragraph("3. Hand-design 5 levels as ASCII grids, escalating one variable at a time", h3))
story.append(Paragraph(
    "Level 1 (one plate, no echo) &rarr; Level 2 (two plates, one echo) &rarr; Level 3 (three plates, "
    "two echoes) &rarr; Level 4 (four plates via a branching corridor, three echoes) &rarr; Level 5 "
    "(two independent doors, four plates, tests sequencing). Every grid was deliberately built as a "
    "single connected corridor/cross shape, which is trivial to hand-verify for connectivity — a maze "
    "with an accidentally isolated pocket would silently make a level unsolvable.", body))

story.append(Paragraph("4. Build the game as one dependency-free HTML file", h3))
story.append(Paragraph(
    "Canvas-based rendering, a DOM-based HUD and overlays, keyboard and on-screen D-pad input, "
    "position interpolation for smooth motion on top of discrete tick logic, localStorage best-run "
    "tracking, and reduced-motion / mobile-safe-area handling. No frameworks or external code, so "
    "the file can be opened directly or hosted anywhere as a static page.", body))

story.append(Paragraph("5. Verify every level is solvable — don't just eyeball it", h3))
story.append(Paragraph(
    "Wrote a headless Node script (test/sim.js) that re-implements the same tick / echo / door "
    "logic and plays each level itself using real breadth-first-search pathfinding, reporting how "
    "many loops it took to solve. This caught a real bug on the first pass: Level 5's third plate "
    "sits behind a door that plates 1 and 2 must open first, which an upfront \"is every plate "
    "reachable from the start\" check flagged incorrectly as unsolvable. The check was corrected to "
    "verify reachability against live door state at the moment each plate is targeted, and all five "
    "levels then verified as solvable within their intended loop budgets.", body))

story.append(Paragraph("6. Package it as a real, well-defined repository", h3))
story.append(Paragraph(
    "README.md for setup, deployment and a mapping to the judging criteria; this document "
    "(PROMPTS.md / SUBMISSION.pdf) for the required prompt log; test/sim.js checked in as proof of "
    "the verification step; and game/index.html as the deliverable itself — structured as an actual "
    "small project rather than a single dropped file, per the brief's own \"well defined repo\" "
    "instruction.", body))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", color=colors.HexColor('#ddd'), thickness=1))
story.append(Paragraph(
    "Full prompt log and reasoning are also kept in PROMPTS.md in the repository root for reference.",
    body_muted))

doc.build(story)
print("PDF built.")
