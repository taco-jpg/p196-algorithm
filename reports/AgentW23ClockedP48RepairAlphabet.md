# W23: Clocked non-gauge erasure alphabet on the period-48 decimal lattice

**COMPUTED; finite exact scope, no infinite Lychrel certificate.** This extends the phase-0 two-coefficient eraser in `AgentW23P48ThreeStepErasers` to a genuinely phase-dependent reset alphabet. The point is a potential *clocked synchronizer*: a future centre emitter may inject a packet at several stages of the overflow clock and receive a finite-time reset. There is no known emitter, no renewal edge and no finite certificate cycle yet.

## Scan definition and all positive results
Use the rec2 48-coefficient base-10 lattice from `calculation/decimal_frontier/lattice_formats/p8_scc.txt`, as a 960-coefficient periodic test word. Advance the background for phase s=0..7 using the two-sided exact carry normalization/paired coefficient rule with gamma=(1,0,1,0,...). At each phase, change an adjacent pair in each of the 48 spatial positions to all 19² alternatives except the unchanged pair, and compare the complete perturbed and unperturbed 960-coefficient words after every transition up to t=10. A change is "non-gauge" if at least one coefficient changes by a value not divisible by 9. This is 17,280 nonidentity alternatives per phase, 138,240 across the eight phases, with no search cap.

| start phase | non-gauge patches erased | exact time to pairword reset | patch location / values |
|---|---:|---:|---|
| 0 | 5 | 3 | site 20: (13,9)->(8,5),(8,14),(17,5),(17,14); site 23: (3,13)->(7,9) |
| 1 | 0 | - | - |
| 2 | 0 | - | - |
| 3 | 2 | 4 | site 44: (12,9)->(14,16); site 47: (7,12)->(5,14) |
| 4 | 5 | 3 | site 44: (5,9)->(1,4),(1,13),(10,4),(10,13); site 47: (15,5)->(11,9) |
| 5 | 0 | - | - |
| 6 | 0 | - | - |
| 7 | 2 | 4 | site 20: (6,9)->(4,2); site 23: (11,6)->(13,4) |

The four zero-count phases are local coverage information only; they do not exclude wider repair words or alternative target structures. The positive finite-state graph has phase-labelled resetting arrows 0->3, 3->7, 4->7, 7->3. The 3↔7 temporal component is a **reset scheduling graph**, not an autonomous packet source. Patches must still be supplied by a construction.

## Independent real-integer check
Use the canonical odd-length symmetric pairword
`P_q=H_q++reverse(H_q[:-1])`, `H_q=B++W^q++[10,14,1,10]`, `B=(17,5,0,2,1,9,15,18,14,9,3)`. Realize the pairword as physical base-10 digits (low=max(0,p-9), high=min(9,p), centre=5). Evolve the true integer to the requested start phase s, extract its complete symmetric pairword, insert one candidate patch at coefficient index `11+48*2+offset` and reflect, then realize a *new*, canonical integer with that full pairword. Evolve both independently with Python's actual arbitrary-precision `n+int(str(n)[::-1])`; compare ALL paired coefficients at the claimed reset and the entire integers one step later. No spatial bulk prediction is used in the physical engine.

All 14 patches pass individually for q=8 and q=100, with no palindrome before reset. For s=0/4 the pairwords agree at offset t=3 and subsequent ordinary integers at t=4; for s=3/7 pairwords agree at t=4 and integers at t=5. The q100 parent orbit is the independently 20,000-step nonpalindromic seed of `AgentW23P48ThreeStepErasers`; the physical patched orbits merge into its suffix after the stated reset. This is a rigorous *finite checked coalescence*, not any proof of nonpalindromicity after t=20,000.

## Reproduction
```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-W23/phase_scan.cpp -o /tmp/w23_phase && /tmp/w23_phase
python3 calculation/new_structures/agent-W23/phase_verify.py
```
Expected rows in `calculation/new_structures/agent-W23/phase_expected.json`. The next constructive problem is a finite carry-guarded **emitter** that produces at least one member of this repair alphabet every phase-3↔7 traverse without decreasing the protected exterior width; no such emitter has been identified.
