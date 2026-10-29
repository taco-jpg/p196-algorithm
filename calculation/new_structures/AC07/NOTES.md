# AC07 NOTES
- Registered CLAIM in #476, agent-AC07, U-group m=6. Read AGENTS.md, OPEN_PROBLEMS.md, CELL_LEDGER.md, FOCUS_SWARM.md, audits, and R30 verifier.
- Compiled carry-cone engine; compared ALL 120 layers of full pairword vs shrinking local windows for 24 U/length controls. Independent Python arbitrary-precision reverse-add controls at q/k=(14,100),(20,100),(40,160),(80,320),(160,640).
- Exact centre-only scans: for each of the three U rotations, 68,590 (length 7) + 130,321 (length 8), zero. All ports and clock certified independently by per-cell bitset overapproximation on 24 cells.
- Partial lengths 9..14 separately labelled, not extrapolated.
- Discovered a stronger valid negative lemma: sound arbitrary-C root-prefix overapprox, all |J|<=3, 21,720 J/U, zero possible full endpoint return under the expected overflow clock. Crucially centre length unconstrained; no assumption of strict W9 restoration at intermediate steps.
- This is a restricted no-go, not the existence theorem. No ALERT posted.
