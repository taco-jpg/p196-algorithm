# Agent 8 — T2 period-19 B cycles with five or six overflows

**Status: COMPUTED; NO LEAN-VERIFIED new result.** Coordination #289. Two disjoint research slices claimed as `T2.p19.g5` and `T2.p19.g6`. No base-10 one-band Lychrel certificate produced.

## Result

For the exact exterior `B`-only recurrence of `Agent120.Neutral`, under the `Hyp` complementary-carry condition and allowing arbitrary B word lengths and terminal neutral-band trims, a closed period-19 base-10 B cycle cannot have exactly **five or six** overflow steps. There are **612** cyclic binary overflow-necklaces of length 19 and weight 5, and **1,428** of weight 6. Every one was exhaustively rejected by the exact time-first position-transfer solver introduced in draft PR #321; no accepting state, runtime cap, or state cap was encountered. This statement does **not** rule out period-19 cycles with seven or more overflows (and by the preexisting first-coordinate necessary inequality P≤4Σg, four or fewer are already excluded separately).

## Exact command (after dependency PR #321 has been merged / source made available)

```sh
c++ -O3 -std=c++17 calculation/agent-8/p18_fixed_g.cpp -o /tmp/a8_fixed_g
python3 calculation/agent-8/p19_g5_g6_census.py /tmp/a8_fixed_g
```

Pure stdlib Python enumerates **all** weight-5 and weight-6 19-bit combinations, keeping exactly one lexicographically minimal phase rotation of each, and calls the exact transfer C++ solver with explicit caps. To avoid byte-identical duplicates forbidden by `AGENTS.md`, this PR **depends on draft PR #321** for the solver source. Don't merge this PR first or treat its report as independently runnable on `main` until the earlier solver lands.

Expected output fields (wall clock varies):

```
P19_WEIGHT5 statuses={'EXHAUSTED': 612} states_total=644 max_states=(33, '0001000100010001001') max_depth=(2, '0001000100010001001')
P19_WEIGHT6 statuses={'EXHAUSTED': 1428} states_total=9312 max_states=(5693, '0000111000100010001') max_depth=(6, '0000111000100010001')
POSITIVE ACCEPT g=11100010000 depth=29 states=11133 arcs=11148 L=10100110011
POSITIVE ACCEPT g=100010001000 depth=53 states=100330 arcs=100545 L=100101011010
```

Actual runs in sandbox: 4.85 seconds (weight5), 10.99 seconds (weight6), no cap. Known p11 and p12 positive B-only controls accepted in the same solver, with correct carry streams.

## Scope / proof status

Every true B cycle of the fixed overflow word would correspond to a finite accepting positional path; that's the paper justification for the finite enumeration. This result is **COMPUTED**, not a Lean proof. The C++ source currently belongs to draft PR #321 and is still under review. There is no universal p19 exclusion, no C-side center compatibility result, no full decimal Lychrel theorem and no run of `python3 tools/verify.py --changed` from a full repository checkout. The proposed PR must remain **DRAFT / UNVERIFIED / DO NOT MERGE** until its dependency and verification pass.