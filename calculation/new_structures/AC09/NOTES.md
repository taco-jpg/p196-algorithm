# AC09 investigation log, 2026-10-29

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, docs/CELL_LEDGER.md, phase-0 lattice and R30 parametric checker. CLAIM registered in issue #476.
- Verified A(B)=-11, A(W)=-22, assigned U alternating sums -5/23/9.
- Fixed a right-side U collar-index bug in preliminary C++ before exhaustive scans. Discarded early 1,000-case runs.
- Final full-width physical folded scan: C8 uid0 130321 tested, zero centre-window hits, zero wrong clocks (64.36s); uid1 same (71.50s); uid2 same (66.66s).
- The optimized compare was audited against the literal target in 960 random tests at two width settings. Separate Python true-bigint checked all 3,600 steps over 30 controls at five widths. Python/C++ 28-coefficient centre windows match for three U sample controls.
- Odd-C all-length obstruction is a direct specialization of the known Q39 modular necessary gate; even C10/12/14 remain UNDECIDED. No all-time decimal certificate.
