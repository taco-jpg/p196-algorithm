# Z10 running notes

- Read the mission and current focus instructions, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, reports/audit_2026-10-28/AUDIT_N.md, reports/audit_2026-10-28/AUDIT_Nseries.md, calculation/decimal_frontier/lattice_formats/FORMATS.md, the current #475 feeds, and the available historical #474 FEED/COMBINE/BREAK context.
- Registered claim in #475 as comment 6492135352; route is rooted phase-0 p12/m9, |J|=5, slice 10/12, lexicographic U ranks 10 and 22.
- Built scan.cpp, an exact bit-sliced 64-candidate-lane pairword/carry engine. It enumerates every J word directly; no MDD pruning or other candidate pruning is used. Every lane must pass the exact 120-bit overflow clock before its W9 prefix is tested. The mismatch histogram is checked to partition all clock-valid candidates.
- Full reference scans completed at (q,k)=(14,100) for both U rotations. Each of the 2,476,099 J words has the exact 30-overflow clock; none restores the required B34 W9^14 prefix. First mismatch offsets from the cut range from -25 through -12 for rank 10 and -25 through -13 for rank 22. The histogram accounts for the entire search space, with zero survivors.
- Since there are no first-epoch W9-prefix survivors, no 240-step survivor transition exists to advance. The endpoint obstruction already rules out a uniform same-J/C 120-step return for this U slice at the T12 reference width.
- Independent replay_controls.py uses Python arbitrary-precision integers and the literal operation n + reverse10(n). Its first-64-J histograms match the bit-sliced engine exactly for both U rotations. Thirty additional bigint controls (two seam examples per U, q=14/20/40/80/160 with k=100 at q=14 and k=4q otherwise) all reproduce the rooted overflow clock through 240 steps, the reported cut offsets, no full 120/240 template return, and no palindrome.
- Existing T12 cut/insertion theorem lifts failure of the reference uniform-return obligation to all independent q>=14,k>=100 for each fixed J,C,U. Its reset-cone bounds give C-independence of the W9-prefix result at the reference: 300 U coefficients minus at most 152 junction-side and 122 centre-side coefficients leaves 26 protected coefficients.
- This is a scoped negative result. It is not a decimal Lychrel nonexistence proof, and it does not claim every individual width fails; it excludes the required uniform all-width fixed-seam return for the two U rotations in this slice.


## 2026-10-29 — phase-0 J5 slice 11/12

- Claimed neighboring route in #475 comment 6495138761: ranks 11 and 23 in the fixed lexicographic ordering, U=(9,0,18) and (12,6,9), all 19^5 junctions per U.
- Compiled bit-sliced scan exhausted 2,476,099 J words per U at (q,k)=(14,100). All 2,476,099 per U passed the rooted 120-step overflow clock; 0 per U restored the required B34 W9^14 prefix. The mismatch histograms partition the entire candidate domain.
- No R02/V48 MDD prefilter was used; the compiled scan directly covered all junctions. No candidate survives the necessary first-epoch prefix gate, so the second-epoch template check has no candidates to advance.
- Independent arbitrary-precision decimal replay checked 40 controls (4 J values per U at q=14,20,40,80,160; k=100,100,200,400,800 respectively). All controls matched the 120/240 overflow clocks, all failed the full template return, and none reached a palindrome through step 240. At q=14 the independent first-mismatch offsets match the bit-sliced scan for all chosen controls.
- Independent first-64-J big-integer histograms exactly match the C++ bit-sliced histograms for both U rotations: U=(9,0,18): -23:29,-22:35; U=(12,6,9): -23:27,-22:37.
- The existing T12Rooted120CutPumping theorem plus the 26-coefficient protected interval lifts the reference prefix failure to the required uniform all-width fixed-J/C return exclusion for this U slice. This is a scoped negative result, not a global decimal Lychrel nonexistence theorem.


## 2026-10-29 — phase-0 J5 slice 12/12

- Claimed adjacent route in #475 comment 6495393976: U ranks 12 and 24, U=(9,2,16),(12,9,6), all 19^5 J words per U.
- Compiled bit-sliced scan exhausted 2,476,099 J words per U at (q,k)=(14,100). All cases passed the rooted 120-step overflow clock; 0 restored the B34 W9^14 prefix. Histograms account for every candidate.
- Independent arbitrary-precision replay checked 40 controls at q=14,20,40,80,160 with k=100,100,200,400,800. All 120/240 clocks matched; no full return or palindrome occurred in these controls. First-64-J big-integer mismatch histograms match the C++ engine for both U words.
- T12 protected-cut insertion/reset-cone result lifts the reference prefix obstruction to a fixed-J/C uniform all-width return obstruction in this slice. No candidate passes the first-epoch W9 prefix, so there is no 240-step candidate to advance.


## 2026-10-29 — phase-0 J5 slice 9/12

- Claimed next neighboring route in #475 comment 6495550606: U ranks 9 and 21, U=(8,9,10),(10,8,9), all 19^5 J words per U.
- Compiled bit-sliced scan exhausted 2,476,099 J words per U at (q,k)=(14,100). All cases passed the rooted 120-step overflow clock; 0 restored B34 W9^14. The full mismatch histograms partition every candidate.
- Independent arbitrary-precision replay checked 40 true-integer controls at q=14,20,40,80,160 with k=100,100,200,400,800. All 120/240 clocks matched; no full return or palindrome occurred in these controls. First-64-J bigint mismatch histograms exactly match the C++ engine.
- T12 protected-cut insertion/reset-cone result lifts the reference prefix failure to a uniform all-width fixed-J/C return obstruction in this slice. No candidate passes the first-epoch prefix gate, so no candidate remains for a two-epoch restoration test.
