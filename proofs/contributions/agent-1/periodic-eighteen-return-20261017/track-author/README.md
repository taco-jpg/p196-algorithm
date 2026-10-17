# Finite selected-run tracking author receipt

Accepted claim: `fcb20cb967483a96aa46261642d748fd32d4f5d6`.
Worktree: `/workspace/p196-agent1-eighteen-return-20261017`.
Author: Agent1 specialist `/root/research_status/cap4_existing_theorems`.
Root remains sole Git writer and issue61 relay.

## Frozen source and exact scope

- Canonical source: `proofs/Agent1PeriodicEighteenTrack.lean`.
- SHA256: `370b027129211a29cbb1f10e1c7ac2756452de81196936a7745f914b92899f17`.
- Git blob identity (read-only hash): `609c440ce9d11ddedc3d92fc29f4288913583a04`.
- Direct imports: `Agent1PeriodicGuardedPath`, `Agent1PeriodicReturnClock`, `RunAncestry`.
- Original logical alias RunAncestry maps to unchanged `proofs/RunAncestry__5f2702512ad8719e.lean`, SHA256 `6c8041050576a142949376818a2e37997031ce40b99a7908a763396ee702a9eb`.

The public definition `quotientEighteenTrack` follows ONE supplied maximal
18 run through the original `RunAncestry.descendant` operation. The public
`quotient_eighteen_track` assumes an exact guarded finite quotient path,
original validity at its initial state, one initially maximal18 run, and a
fixed anchor I with a0+N≤I and I+N<b0. A supplied cumulative C must start at
zero and increase by the actual indexed carry of each full source word.

For every t≤N the theorem proves successor maximality of that same tracked
run, a_t≤a0+t, b0≤b_t+t, a0+C_t≤a_t, and anchor containment. It does not
assume intermediate phases remain constant18. It does not prove population
coverage, birth classification, extinction, or the final full-return
contradiction. It reuses unchanged descendant_step for maximality. The list
successor transfer uses only in-range equality, including the boundary
clauses of MaximalRun; it makes no whole-function equality claim outside
width.

## Retained execution

All source snapshots and logs are immutable under their attempt directories.

- `run-ancestry-dependency-001`: strict fresh compile of the unchanged original
  RunAncestry alias; PASS. Its existing LychrelDigitSums dependency object was
  reused and is pinned in every main attempt's dependencies.json.
- `attempt-001`: failed compile. Three rewrites required exposing beta-reduced
  list lookup applications. The log contains Lean's automatically generated
  `sorryAx` dependency for those rejected goals; no `sorry`/`admit` was added
  to source and this attempt is not accepted.
- `attempt-002`: strict source compile PASS. No origin audit was run yet.
  Its source and object are byte-identical to the final attempt.
- `runtime-inventory-001`: PASS, enumerates every safe and nonsafe generated
  definition in the completed module before fixing the exact audit inventory.
- `attempt-003`: final strict source compile and full module-origin audit PASS.
  Compile 0.6160 seconds, 461468 KiB maximum child RSS; audit 1.6190 seconds,
  757132 KiB maximum child RSS. Both commands exited 0. Lean4.19.0 commit
  6caaee842e94, `--trust=0 -j1 -DElab.async=false`; 4GiB address-space cap.

Compiler SHA256:
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Final object SHA256:
`8122537ac368d3e4a3ec4d81d21df149acbfcd24efd3e5b01b10c5addaea8eff`.

The final audit enumerates all declarations by module origin: 27 theorem
constants, 4 safe axiom-free definitions, and 8 exact inventoried compiler
runtime implementations. It rejects custom axioms, nonstandard theorem or
safe-definition axioms, unknown constants, and unknown nonsafe definitions.
The theorem axiom union is exactly propext, Classical.choice, Quot.sound.
The one public theorem is explicitly required to occur. The safe recursive
definition, its safe unfolding, match function and splitter are audited
independently from the generated recursive/cstage runtime entries.

The author increment uses 26 pinned dependency objects:25 prior dependency
objects reused after source/hash checks and1 unchanged RunAncestry object
freshly compiled here. This is NOT a fresh whole-closure verification or an
independent review. Parent fresh compilation/audit remains separate.

`manifest.json` hashes every retained text/script/evidence file and records
all local .olean hashes separately. No Git mutation or external message was
performed by this author.
