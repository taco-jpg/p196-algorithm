# Agent 8 — T2.p19.g7: exact all-width period-19 exterior B census, weight seven

**Status: COMPUTED; not LEAN-VERIFIED.** Task coordination #289, independent disjoint scope `T2.p19.g7`. No base-10 Lychrel existence or universal B-cycle nonexistence claimed.

## Result

All **2,652** binary rotation necklaces of length 19 with precisely seven overflow steps were exhausted by a fresh 128-bit fixed-g time-first exact B positional-transfer solver. Every run returned `EXHAUSTED`: **0 ACCEPT / 0 CAPPED / 0 TIMEOUT**. Total 55,140 `(g, transfer-state)` records, maximum 30,217 states and depth 12 for `g=0000111000110001001`. Wall clock ~19.45 seconds for the complete subprocess batch in the sandbox.

This is an exact **all-B-width** computation: local scan interfaces encode carry and partner digits, not the B word length. Each genuine B-only cyclic word of this fixed g induces an accepted finite transfer path. The solver is the 128-bit upgrade of the independently written and tested 64-bit positional solver from Agent 8 draft PR #321; the new 128-bit code uses a full 128-bit key and a hash of both 64-bit halves, with equality always comparing the entire key, so hash collisions cannot merge states. Since p=19 and Σg=7 needs `2*p+4*Σg=66` bits, a 64-bit implementation would have silently truncated valid states. This version guards inputs requiring over 120 bits and never truncates the p=19 case.

## Reproduce

```sh
c++ -O3 -std=c++17 calculation/agent-8/p19_fixed_g_wide.cpp -o /tmp/a8_p19w
python3 calculation/agent-8/p19_weight7_census.py /tmp/a8_p19w
```

Expected key output (time machine-dependent):

```
P19_WEIGHT7 {'EXHAUSTED': 2652} total_states 55140 max_states (30217, '0000111000110001001') max_depth (12, '0000111000110001001')
POSITIVE ACCEPT g=11100010000 depth=29 states=11133 arcs=11148 L=10100110011
POSITIVE ACCEPT g=100010001000 depth=53 states=100330 arcs=100545 L=100101011010
```

The p11 and p12 positive B examples were accepted by this exact compiled 128-bit binary. The same independently written 64-bit binary returns the same accepted positive boundary details and coinciding counts; cross-language Python 64-bit and C++ counts matched in the separately completed Agent 8 T2.p18.g6 study for its noncapped classes.

## Boundaries

- **COMPUTED:** No B-only cycle of exact temporal period 19 with exactly seven overflows.
- Does **not** exclude p19 cycles with **eight or more** overflows, other temporal periods, or existence of a compatible center C.
- Does not produce any accepted base-10 Lean `cycleOK`, a decimal Lychrel witness, or a Lean theorem. `python3 tools/verify.py --changed` was not run from a full repository checkout in this environment; review PR must remain **DRAFT / UNVERIFIED / DO NOT MERGE**.