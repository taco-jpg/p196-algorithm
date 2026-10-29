# W26 running notes

## Route and inputs
- Registered CLAIM agent-W26 in issue #475: rooted phase 0, U=(9,4,14), odd palindromic C length 3..13, |J|=3..4.
- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, reports/audit_2026-10-28/AUDIT_N.md and AUDIT_Nseries.md, FORMATS.md, current #475 FEED/COMBINE/DONE/ALERT material, and the relevant read-only #474 history.
- Reused the exact all-width rooted 120-step cut/insertion lemma in calculation/new_structures/T12/TARGET.md and NOTES.md. At q>=14,k>=100, return is equivalent to return at (q,k)=(14,100). For U=(9,4,14), the 120-phase reset-cone bound is 152 columns from the J side and 121 from the centre side, leaving 27 of the 300 U coefficients untouched. Thus the t=120 B/W prefix is independent of the value and length of the odd centre C.

## Exact search
- Implemented search.cpp: exact LSD-first pairword normalization and reflection, no SAT/MDD or modular pruning.
- Enumerated every J word in [0,18]^3 and [0,18]^4: 19^3+19^4=137,180.
- At the single reference width q=14,k=100, use the canonical legal representative C=[0,0,0]. For every J, replay 120 exact coefficient steps and check the full B ++ W^14 prefix and overflow clock.
- All 137,180 candidates have the exact clock (1000)^30; zero restore B ++ W^14. The first mismatch is always inside W, at coefficient 135..147 (zero-based), while the expected B/W prefix ends at index 160.
- Histogram: 135:1510, 136:3311, 137:64526, 138:54240, 139:6269, 140:6333, 141:472, 142:454, 144:35, 145:22, 146:3, 147:5. Total 137,180.
- Because the prefix is independent of C by the T12 reset-cone argument, this covers all 496,595,400 legal odd centres across lengths 3..13 without enumerating their Cartesian product with J. No mod-11 filter was used.

## Independent controls
- independent.py checked 60 ordinary-decimal 120-step replays at (q,k)=(14,100),(20,100),(40,160),(80,320),(160,640), using two different J representatives and all six odd centre lengths.
- Each step matched a pairword engine, a fresh-buffer schoolbook digit-array engine, and Python arbitrary-precision n+reverse(n); every clock was (1000)^30 and every endpoint failed the required W-prefix equality.
- The full repository verify.py was not run in this connector-only environment. The standalone C++ search was compiled and all three exhaustive index ranges were run separately.

## Next
- This cell is exhausted. Do not generalize it to other U words or centre parities. Continue only on a separately claimed, unowned route; longer-centre phase-zero cells are already covered by another agent.