# Z11 running notes

- Registered in issue #475 as comment 6492122244: phase-zero |J|=5, lexicographic U ranks 11 and 23; build on T12 cut/insertion, epoch seam-map dynamics, and the existing phase-zero short-J census.
- Read the current AGENTS.md, docs/FOCUS_SWARM.md, OPEN_PROBLEMS.md, AUDIT_N.md, AUDIT_Nseries.md, FORMATS.md, and the latest page of #475 comments. Agent-Z03's result covers disjoint U ranks 3/15/27, so this route remains disjoint.
- Implemented a 32-lane AVX2 carry cone. Each lane tracks its own known-prefix mask, so trailing-9 resets are exact per candidate rather than using a common truncation or an unsafe strict-W9 prefilter.
- C++ --selftest passed for 2 U rows × 32 J samples × 4 centres × 120 phases against the full pairword recurrence.
- Full exhaustive run completed: 2,476,099 J words for each U, 4,952,198 total. All clocks are exact, every lane retains the W band prefix through index 159, and every lane has a W9 mismatch at t=120.
- Independent Python replay passed 40 genuine decimal cases across q=14,20,40,80,160 with k=100,100,200,400,800 and even/odd legal centres. At each step, Python arbitrary-precision integers, LSD-first digit arrays, and pairword recurrence agree.
- Negative scope redirects fixed-seam work away from these two U rows. It does not decide moving/growing seams or the all-time existence question.

- After committing slice 11/12, read the latest 40 #475 comments and claimed the wrap-adjacent phase-zero slice 1/12 (ranks 1/13/25) in comment 6495790923. The source and report are under slice01/.
- Slice 1/12 is exhaustively complete: all 7,428,297 J/U pairs fail W9 restoration, with exact clocks and no unresolved prefixes; 30 independent genuine-decimal controls pass. See slice01/REPORT.md.
