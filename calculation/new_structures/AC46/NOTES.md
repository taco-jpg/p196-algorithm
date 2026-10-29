# AC46 running notes (2026-10-29 UTC)

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM, CELL_LEDGER, audits, live #476 and pi185/AC45/AC37/AC35 work; claimed the endpoint-only arbitrary-J/C decision, building on (a), (r), (t).
- z3, pysat and SAT solver binaries were unavailable in the execution container; bounded-SAT unrollings would not decide unrestricted J. Instead used a sound two-carry CEGAR over-approximation retaining genuine gamma and all temporary W9 damage.
- Computed the exact phase-0 root overflow clock, guaranteed 69-site prefix and nonpalindrome guard.
- Exhausted 331,470 U/C centre-collar constraints for all 30 U and C lengths1..6 with zero matches, arbitrary J and all q>=14,k>=100 via the two-carry proof.
- Crosschecked with 294 independent canonical bigint / schoolbook orbits = 35,280 genuine decimal steps; q/k five widths, both centre parities, J up to 311, plus a planted true toy one-step target.
- Full arbitrary-C marked-fold emptiness remains UNDECIDED; this is only its fixed-short-centre excluded sublanguage.
