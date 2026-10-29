# AC33 running notes
- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md and CELL_LEDGER.md; #476 is authoritative. AB33 previously sampled 5,700 phase-0/J6 cases; Z14 ranks 2/14/26 and 3/15/27 have no committed completion.
- Claimed phase-0/J6 first-symbol slice J[0]=0, U one-based ranks 1/13/25 and two palindromic fixed centre parities. Refined to an exact J[0:2]=(0,0) exhaustive subcell, with no unsupported promotion to J[0]=0.
- Full unpruned six-run census: 130,321 trials per U,C, 781,926 total, all mismatching W9 at 137/138. Independent Python replay 48 C++ singleton cases and 30 scaled-width controls.
- T12 supplies all-q,k implication, but no fixed-seam repair identified; the remaining J[1] and other U/C slices are still open.
- Expanded J[0:2]=(0,1) exact unpruned cell: 781,926 more cases, zero W9 endpoint restoration.
- Completed odd C=[4,14,4] with J0=0 and all J1..J5 for three U words: 7,203,220 parity-correct mod-11 failures, 225,077 full decimal replays, zero W9 return. A(U) residues 5/0/6; U0 admissible J residue count 225,077 independently audited.
- Six nearest misses at positions 144/145 reproduced by separate bigint engine at five widths each. Parent J0=0 cell now PARTIAL(8,210,223/14,856,594), not EXHAUSTED.
