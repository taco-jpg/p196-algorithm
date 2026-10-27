# Agent 8 — T2.p18.g6 independent full-width exterior test

**Status: COMPUTED, not LEAN-VERIFIED.** Task: #289, T2.p18.g6. No decimal Lychrel number or base-10 neutral-band certificate is claimed. Every base-10 B-side cycle of **period exactly 18** whose overflow word has exactly **six** ones is excluded by an uncapped exhaustive finite-state transfer. All other periods and p18 overflow weights (notably weight seven) remain outside this result.

## Exact scope and method

For a hypothetical `Agent120.Neutral.cycleOK 10` cycle, `Hyp` forces the center normalization carry to be `e2 = 1 − e1`, making the exterior B transition autonomous. For a fixed cyclic overflow word `g` and fixed period `p`, the possible coefficient words B of **any length** can be examined column by column. At each scan boundary, keep the p-entry carry-in word `L`, the p-entry required partner carry word `H`, and partner low digits `Y` only at overflowing time positions. Each state is a finite tuple; successive B columns are exact local time-closed digit trajectories, not a guessed upper bound on B length.

Given B coefficient x_t at time t (0≤x_t≤18), incoming low carry L_t, and guessed partner carry h_t∈{0,1}, require `floor((x_t+h_t)/10)=H_t`. Then

```
x_(t+1) = (x_t + L_t)%10 + (g_t ? Y_t : (x_t+h_t)%10).
L'_t    = floor((x_t+L_t)/10).
H'_t    = h_t.
Y'_t    = (x_t+h_t)%10   (for g_t=1).
```

Close `x_p=x_0` at each spatial column. At the initial outermost scan interface, `L=0, H=g, Y=1`, and its first B coefficient is nonzero. An accepting end interface must satisfy `L_t+H_t=1` for all t and `Y_t=9 L_t` at every g_t=1 (the neutral band). Every genuine B cycle induces an accepting finite path. An exhaustive search with zero accepting boundary thus excludes such a B cycle regardless of its coefficient-word length. This is a sound **necessary overapproximation**; it can admit spurious B traces, but cannot exclude valid ones if its arithmetic is correct.

Cyclic phase rotations of `g` correspond to reindexing a cycle, so enumerating binary necklaces checks all length-18 overflow words with six ones. There are exactly **1,038** such representatives. No state/depth cap was reached in the completed census.

## Reproduction

No third-party Python modules; requires C++17 compiler.

```sh
c++ -O3 -std=c++17 calculation/agent-8/p18_fixed_g.cpp -o /tmp/a8_p18
python3 calculation/agent-8/p18_weight6_census.py /tmp/a8_p18
```

Expected status (wall time hardware-dependent):

```
P18_WEIGHT6 {'EXHAUSTED': 1038} total_word_states 818161 max_states (808563, '000100011000100011') max_depth (37, '000100011000100011')
POSITIVE_CONTROL ACCEPT g=11100010000 depth=29 states=11133 arcs=11148 L=10100110011
POSITIVE_CONTROL ACCEPT g=100010001000 depth=53 states=100330 arcs=100545 L=100101011010
```

The full census ran in 16.7 seconds in the sandbox. It explored 818,161 distinct `(overflow necklace, transfer state)` pairs in total. The single hard word `000100011000100011` consumed 808,563 of these states, and its BFS exhausted at depth 37; no state cap (5,000,000) or depth cap (450) was hit. A separately written pure-Python transfer enumerator independently exhausted the other 1,037 words but hit its 300,000 state cap on the hard word. The independent C++ transfer therefore resolved precisely that previously **UNDECIDED** case; a subsequent C++ full rerun of all 1,038 words corroborated the Python negatives. Both known p11 and p12 positive B streams were accepted by the *same C++ binary* with the expected carry words and depths.

## What is not claimed

- No base-10 B-cycle of exact period 18 with exactly six overflows, **COMPUTED** only, subject to review of the two implementations and their relationship to Lean `nextB`.
- **Not** all period-18 B cycles: other overflow weights are not excluded here.
- **Not** a center C obstruction or a joint `(B,C)` cycle result.
- No decimal Lychrel certificate, no Lean theorem, no call to `python3 tools/verify.py --changed` in this environment. Keep PR **DRAFT / UNVERIFIED / DO NOT MERGE** pending repository-level review and verification.