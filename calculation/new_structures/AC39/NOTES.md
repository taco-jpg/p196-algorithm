# AC39 running notes

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, CELL_LEDGER.md, phase-6 original lattice, R30 checker, and AB39's #476 CELL.
- Claimed phase=6, J=6, endpoint-only with exact carry-aware computation on #476, building on (a) T12 and (t) the strict-phase/endpoint distinction.
- AB39 claimed every tested physical return first mismatched at index 12 (0 versus expected 1). Independent integer replay for J=[0]^6, U=(9,0,18), even C had first mismatch 136 and index12=1; unrelated odd centre and other U showed the same correction.
- Constructed two-ended carry cone allowing BOTH upper carry inlets. It certifies an all-interior 120-step first-70 preservation with 30 genuine overflows.
- 68 physical controls, including all 30 U rotations and both centre parities at q14, plus q20/40/80/160, matched independent integer and schoolbook engines for all 8,160 transitions.
- No complete template return found in those controls; **not** an exhaustive J census. Prefix shielding consumes 90 known positions and cannot itself pump indefinitely.
