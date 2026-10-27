# Agent 2 / T2.p23–24.weight7: two all-width B exclusions

Status: COMPUTED, **not Lean verified**. Coordination issue #289; no base-10 decimal Lychrel claim. Disjoint from Agent 4's 21–24 weight-six research and Agent 2's earlier PRs #309/#317/#322.

## Scope and results

Exactly base 10, one-band exterior B, overflow count k=7, periods P in {23,24}, arbitrary exterior lengths. For P=23, all **10,659** binary necklaces were checked by the sound necessary first-head automaton and **64** survived. All 64 exact B positional automaton searches terminated EXHAUSTED with zero ACCEPT, no caps; largest search had 62,497 states at g=00001110001000100010001 and maximum depth 10.

For P=24, all **14,421** binary necklaces were checked by the same necessary graph; **32** survived. All 32 exact B positional searches exhausted with zero ACCEPT, no caps; max 4,161 states at g=000100010001000100010011 and maximum depth 3.

Independent pure-Python positional BFS separately reproduced the hardest P23 and P24 cases, matching the state counts (62,497 and 4,161), depths (10 and 3) and zero accepted states. These two-language checks are by the same agent; a genuinely independent second-agent full-scope audit remains pending.

## Mathematics and soundness

With x denoting the effective first exterior coefficient, 1<=x<=18, and unknown reverse incoming carry h in {0,1}, a necessary B-step condition is g=0 ⇒ x+h<10 and x'=2x+h; g=1 ⇒ x+h>=10 and x'=(x mod10)+1. The freedom to choose h makes this graph an overapproximation. No true B cycle is lost by requiring a closed head walk. Cyclic rotations of overflow words correspond to changing the starting time, so enumeration by binary necklaces is complete.

The existing exact all-width column-transfer automaton in calculation/neutral_band/structure/bauto.cpp tracks forward carries L, reverse carries H and overflow partner digit vector Y across arbitrary coefficient-column depths. Exhaustion without an accepting neutral boundary is a COMPUTED exact fixed-g B exclusion. All head-surviving words exhausted, so the scope is completely excluded within this model.

## Reproduce

From a repository checkout:

    g++ -O2 -std=c++17 calculation/neutral_band/structure/bauto.cpp -o /tmp/p196-bauto
    python3 calculation/agent-2/p23_p24_weight7.py --bauto /tmp/p196-bauto --cap 100000 --seconds 20

Expected:

    period 23 necklaces 10659 first-head 64
    RESULT 23 {'EXHAUSTED': 64}
    period 24 necklaces 14421 first-head 32
    RESULT 24 {'EXHAUSTED': 32}

Independent hardest-case Python position solver was provided for review at issue #294 and in Draft PR #309:

    python3 calculation/agent-2/bauto_py.py 00001110001000100010001
    python3 calculation/agent-2/bauto_py.py 000100010001000100010011

This establishes NO claim for P=23,24 with overflow weights other than seven, other periods, center C cycles, or general one-band impossibility. No cycleOK base-10 certificate exists in this result, no Lean file was written, and python3 tools/verify.py --changed has NOT been executed in a full checkout. **UNVERIFIED / DO NOT MERGE.**
