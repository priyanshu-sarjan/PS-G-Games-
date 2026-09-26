// test/sim.js - Headless Verification Engine for ECHO SHIFT
// Re-implements core tick/echo simulation and verifies all 5 levels are solvable.

const LEVELS = [
  {
    name: "Level 1: First Steps",
    grid: [
      "#######",
      "#S.P1.#",
      "#####.#",
      "#E.D1.#",
      "#######"
    ],
    doors: {
      D1: { requires: ["P1"], pos: { r: 3, c: 3 } }
    },
    plates: {
      P1: { r: 1, c: 3 }
    },
    start: { r: 1, c: 1 },
    exit: { r: 3, c: 1 },
    maxLoops: 1
  },
  {
    name: "Level 2: Two Hands",
    grid: [
      "#######",
      "#S.P1.#",
      "#.###.#",
      "#.P2D1E",
      "#######"
    ],
    doors: {
      D1: { requires: ["P1", "P2"], pos: { r: 3, c: 4 } }
    },
    plates: {
      P1: { r: 1, c: 3 },
      P2: { r: 3, c: 2 }
    },
    start: { r: 1, c: 1 },
    exit: { r: 3, c: 5 },
    maxLoops: 2
  },
  {
    name: "Level 3: Triangulation",
    grid: [
      "#########",
      "#S...P1.#",
      "#.#####.#",
      "#.P2.D1E#",
      "#.#####.#",
      "#....P3.#",
      "#########"
    ],
    doors: {
      D1: { requires: ["P1", "P2", "P3"], pos: { r: 3, c: 6 } }
    },
    plates: {
      P1: { r: 1, c: 5 },
      P2: { r: 3, c: 2 },
      P3: { r: 5, c: 5 }
    },
    start: { r: 1, c: 1 },
    exit: { r: 3, c: 7 },
    maxLoops: 3
  },
  {
    name: "Level 4: Branch Point",
    grid: [
      "#########",
      "#P1..P2.#",
      "#.#####.#",
      "#S..D1.E#",
      "#.#####.#",
      "#P3..P4.#",
      "#########"
    ],
    doors: {
      D1: { requires: ["P1", "P2", "P3", "P4"], pos: { r: 3, c: 5 } }
    },
    plates: {
      P1: { r: 1, c: 1 },
      P2: { r: 1, c: 5 },
      P3: { r: 5, c: 1 },
      P4: { r: 5, c: 5 }
    },
    start: { r: 3, c: 1 },
    exit: { r: 3, c: 7 },
    maxLoops: 4
  },
  {
    name: "Level 5: Temporal Relay",
    grid: [
      "#########",
      "#P1.D1.P3",
      "#.#####.#",
      "#S.....E#",
      "#.#####.#",
      "#P2.D2.P4",
      "#########"
    ],
    doors: {
      D1: { requires: ["P1", "P2"], pos: { r: 1, c: 3 } },
      D2: { requires: ["P3", "P4"], pos: { r: 5, c: 3 } }
    },
    plates: {
      P1: { r: 1, c: 1 },
      P2: { r: 5, c: 1 },
      P3: { r: 1, c: 6 },
      P4: { r: 5, c: 6 }
    },
    start: { r: 3, c: 1 },
    exit: { r: 3, c: 7 },
    maxLoops: 4
  }
];

class SimEngine {
  constructor(level) {
    this.level = level;
    this.rows = level.grid.length;
    this.cols = level.grid[0].length;
  }

  isPassable(r, c, openDoors) {
    if (r < 0 || r >= this.rows || c < 0 || c >= this.cols) return false;
    const char = this.level.grid[r][c];
    if (char === '#') return false;
    // Check if door at (r,c)
    for (const [doorId, door] of Object.entries(this.level.doors)) {
      if (door.pos.r === r && door.pos.c === c) {
        if (!openDoors.has(doorId)) return false;
      }
    }
    return true;
  }

  // Pathfinding BFS for entity to target
  findPath(startPos, targetPos, openDoors) {
    const queue = [[startPos.r, startPos.c, []]];
    const visited = new Set([`${startPos.r},${startPos.c}`]);
    const dirs = [
      { dr: -1, dc: 0, name: 'U' },
      { dr: 1, dc: 0, name: 'D' },
      { dr: 0, dc: -1, name: 'L' },
      { dr: 0, dc: 1, name: 'R' }
    ];

    while (queue.length > 0) {
      const [r, c, path] = queue.shift();
      if (r === targetPos.r && c === targetPos.c) {
        return path;
      }

      for (const d of dirs) {
        const nr = r + d.dr;
        const nc = c + d.dc;
        const key = `${nr},${nc}`;
        if (!visited.has(key) && this.isPassable(nr, nc, openDoors)) {
          visited.add(key);
          queue.push([nr, nc, [...path, d.name]]);
        }
      }
    }
    return null;
  }

  // Simulate a full multi-loop solution strategy
  verifyLevel() {
    console.log(`\nVerifying [${this.level.name}]...`);
    const echoes = []; // array of path strings
    let solved = false;
    let loopCount = 0;

    // We plan target plate for each loop
    const targetSequence = this.determineTargetSequence();

    for (let loop = 1; loop <= this.level.maxLoops + 1; loop++) {
      loopCount = loop;
      const liveTarget = targetSequence[loop - 1] || this.level.exit;
      
      const loopResult = this.simulateLoop(echoes, liveTarget);
      
      if (loopResult.reachedExit) {
        solved = true;
        console.log(`  ✓ SOLVED in Loop ${loop}! (Used ${echoes.length} echoes)`);
        break;
      } else {
        // Record live player's path as a new echo for next loops
        echoes.push(loopResult.recording);
        console.log(`  Loop ${loop}: Recorded echo #${echoes.length} (Target: ${liveTarget.name || 'Exit'})`);
      }
    }

    if (!solved) {
      throw new Error(`Failed to solve ${this.level.name} within max allowed loops (${this.level.maxLoops})`);
    }

    return { solved, loopCount };
  }

  determineTargetSequence() {
    if (this.level.name.includes("Level 1")) {
      return [{ ...this.level.plates.P1, name: "P1" }, this.level.exit];
    } else if (this.level.name.includes("Level 2")) {
      return [{ ...this.level.plates.P1, name: "P1" }, this.level.exit];
    } else if (this.level.name.includes("Level 3")) {
      return [
        { ...this.level.plates.P1, name: "P1" },
        { ...this.level.plates.P2, name: "P2" },
        this.level.exit
      ];
    } else if (this.level.name.includes("Level 4")) {
      return [
        { ...this.level.plates.P1, name: "P1" },
        { ...this.level.plates.P2, name: "P2" },
        { ...this.level.plates.P3, name: "P3" },
        this.level.exit
      ];
    } else if (this.level.name.includes("Level 5")) {
      return [
        { ...this.level.plates.P1, name: "P1" },
        { ...this.level.plates.P2, name: "P2" },
        { ...this.level.plates.P3, name: "P3" },
        this.level.exit
      ];
    }
    return [this.level.exit];
  }

  simulateLoop(echoes, liveTarget) {
    const openDoors = new Set();
    const livePos = { ...this.level.start };
    const echoPositions = echoes.map(() => ({ ...this.level.start }));
    const recording = [];
    const maxTicks = 120;

    let reachedExit = false;

    for (let tick = 0; tick < maxTicks; tick++) {
      // 1. Move Echoes according to their recorded paths
      for (let i = 0; i < echoes.length; i++) {
        const move = echoes[i][tick];
        if (move) {
          const np = this.getNextPos(echoPositions[i], move);
          if (this.isPassable(np.r, np.c, openDoors)) {
            echoPositions[i] = np;
          }
        }
      }

      // 2. Determine Live Player move towards liveTarget
      let liveMove = 'W';
      if (livePos.r === liveTarget.r && livePos.c === liveTarget.c) {
        liveMove = 'W';
      } else {
        const path = this.findPath(livePos, liveTarget, openDoors);
        if (path && path.length > 0) {
          liveMove = path[0];
        }
      }

      recording.push(liveMove);
      const nLivePos = this.getNextPos(livePos, liveMove);
      if (this.isPassable(nLivePos.r, nLivePos.c, openDoors)) {
        livePos.r = nLivePos.r;
        livePos.c = nLivePos.c;
      }

      // 3. Check active plates across all entities
      const activePlates = new Set();
      const allEntities = [livePos, ...echoPositions];
      for (const [plateId, platePos] of Object.entries(this.level.plates)) {
        for (const ent of allEntities) {
          if (ent.r === platePos.r && ent.c === platePos.c) {
            activePlates.add(plateId);
            break;
          }
        }
      }

      // 4. Update doors
      for (const [doorId, door] of Object.entries(this.level.doors)) {
        if (!openDoors.has(doorId)) {
          const reqMet = door.requires.every(p => activePlates.has(p));
          if (reqMet) {
            openDoors.add(doorId);
          }
        }
      }

      // 5. Check exit condition
      if (livePos.r === this.level.exit.r && livePos.c === this.level.exit.c) {
        reachedExit = true;
        break;
      }
    }

    return { reachedExit, recording };
  }

  getNextPos(pos, move) {
    if (move === 'U') return { r: pos.r - 1, c: pos.c };
    if (move === 'D') return { r: pos.r + 1, c: pos.c };
    if (move === 'L') return { r: pos.r, c: pos.c - 1 };
    if (move === 'R') return { r: pos.r, c: pos.c + 1 };
    return { r: pos.r, c: pos.c };
  }
}

function runAllTests() {
  console.log("==========================================");
  console.log("ECHO SHIFT: Automated Level Solvability Test");
  console.log("==========================================");

  let passed = 0;
  for (const level of LEVELS) {
    const sim = new SimEngine(level);
    try {
      sim.verifyLevel();
      passed++;
    } catch (err) {
      console.error(`  ✗ FAILED: ${err.message}`);
    }
  }

  console.log("------------------------------------------");
  console.log(`Results: ${passed}/${LEVELS.length} levels verified solvable.`);
  if (passed === LEVELS.length) {
    console.log("SUCCESS: All levels verified!");
    process.exit(0);
  } else {
    console.log("FAILURE: Some levels could not be solved.");
    process.exit(1);
  }
}

runAllTests();
