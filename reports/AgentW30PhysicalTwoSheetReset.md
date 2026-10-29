# W30: a physically clocked, minimal rank-two complement reset for the decimal five-site centre

Status: **COMPUTED** for exact finite graph transitions, the rooted overflow-prefix witness and finite-time centre-front tracing; **PAPER PROOF** for the general carry-complement identity and its rank-two lower bound. This is **not** a Lean-verified or infinite base-10 Lychrel certificate.

## Context and actual integer source

The preceding W30 results construct a canonical 54,078-digit decimal integer with palindromic least-significant-first pairword

```
P0 = B0 ++ W0^300 ++ (17,3,14,3,17)^8400
   ++ reverse(W0^300) ++ reverse(B0),
```

where B0 has 39 coefficients and W0 has 20 (the previously published p8/m20 decimal exterior). This particular integer's true overflow sequence has `gamma_t=1` at even t and `gamma_t=0` at odd t through edge 26,709; at edge 26,710, the expected 1 switches to actual 0. The earlier W30 independent arbitrary-precision/digit-array replay verifies the *entire true number* and *entire true pairword* at all 50,474 states t=0..50,473. Accordingly, every overflow bit used here through t=27,390 is physically realized, not selected in an abstract automaton only.

For the local five-site row r of pair coefficients, the preceding `AgentW30AdaptiveCarryFibre50473` proof/report defines the unique forward/backward cyclic carry fibres `cl,ch` (provided r is not all9) and the two labelled transitions:

```
F_gamma(r)_i = ((r_i + cl_i) mod 10)
             + ((r_(i-gamma) + ch_(i-gamma)) mod 10)
```

with palindrome-axis residue `delta -> delta+gamma (mod 5)`. Its closed reachable graph has 1,800 states, 360 per axis, and zero ambiguous carry fibres. The new result concerns **set dynamics** (abstract uncertainty) on this exact closed graph, rather than one additional fixed-centre census.

## General 18-complement equivariance: exact algebra

Define `C(r)_i = 18-r_i`, leaving the mirror axis delta unchanged. For any coefficient `p∈{0,...,18}` and carry `c∈{0,1}`, its paired complement has `(p',c')=(18-p,1-c)`, and

```
p'+c' = 19-(p+c),
floor((p'+c')/10) = 1-floor((p+c)/10),
(p'+c') mod 10 = 9-((p+c) mod 10).
```

The quotient identity holds for all `p+c` from 0 through 19 (including p=9 and boundary carry changes). Thus if `cl,ch` solve the cyclic carry equations for r, their bitwise complements solve those for C(r). Uniqueness of the carry solution (every reached row has a coefficient unequal to 9) gives the *actual* complementary cyclic carry fibres. The two normalized digits of each pair complement to 9 each, hence

```
F_gamma(C(r)) = C(F_gamma(r))   for gamma=0 and gamma=1.
```

The reflection-axis condition is also preserved by C. A row equal to its own C image would have all coefficients exactly 9, but **that row is absent** from the closed 1,800-state component (and would have nonunique cyclic carries). Therefore every nonempty complement-closed set is an even-cardinality union of disjoint pairs. Its image under either gamma remains complement-closed, stays inside the component, and contains **at least two** states. This proves a *universal rank-two lower bound* for every finite or infinite binary clock applied to any such initial language. When an exact finite prefix produces **two** states, its images remain exactly two complementary states for all subsequent binary clocks. This is an **infinite invariant of the interior abstraction only**; its survival in a finite complete decimal number additionally requires boundary-protection conditions.

## A ten-edge 32-state lasso followed by a physically realized 680-bit reset

Take the whole set S0 of all 360 states of the closed 1,800-state SCC with mirror axis delta=4, which contains the actual W30 seed row. Apply the alternating clock `10` repeatedly. An exhaustive exact-set computation gives:

```
|S0|   = 360
|S8|   =  46
|S20|  =  32
S30    = S20,  when the intermediate 10 bits are 1010101010.
```

Consequently S_(20+10k)=S20 for **every k>=0** under that ten-bit schedule, by elementary induction on sets. Since 26,710=20+10*2,669, the same exact set of 32 rows is the abstract centre language at the first real exterior clock break. No need to extrapolate 26,710 individual abstract steps: the entire long preperiod has a **finite ten-step set-lasso certificate**.

From t=26,710 through t=27,389, take the **680 actual overflow bits** computed from the explicit canonical W30 decimal orbit. They are stored verbatim (plus SHA-256) in `sync_physical.json`, along with all 32 lasso states. Applying these 680 bits to that 32-state set yields ranks 30,26,22,20,16,14,12,10,8,6,4,2 at increasing prefix lengths; the **first rank-two image** is at exact time **t=27,390**. At that time, delta=0, and the two rows are:

```
A = ( 6,  7,  8,  8,  7)
B = (12, 11, 10, 10, 11) = 18 - A.
```

Under **either possible future overflow bit at each future time**, the set remains exactly `{r_t, C(r_t)}` because the map commutes with C, the whole component is closed, and C has no fixed point there. So this word achieves the *globally minimal nonzero set rank*, independent of future overflow scheduling. Its novelty is the **physical source of the synchronizing word and the precise two-sheet closed abstraction**, not a claim that complement duality itself is new or that its word is forced forever.

The 680-step rank-two reset is independently checked by `reset_checker.py` using a different cyclic-carry routine: for each row it simulates **12 full spatial laps** of the forward or backward carry recursion from both initial bits, rather than using the original one-lap root enumeration. It validates all 32 input rows, the 10-edge lasso, every intermediate set, the exact first rank-two time, complement closure, and both terminal rows. `sync_physical.py` independently reconstructs the source from all 360 reachable rows and the real seed's overflow stream generated by the standalone C++ `extract_gamma.cpp`. The witness is compact: 32 rows, one 10-bit lasso word, and one 680-bit reset word, with no giant integers or trace logs embedded.

## What happens at the physical boundary

The **interior automaton remains closed** forever under arbitrary binary labels, but the *finite real seed's* periodic region does not. This distinction is essential. A separate `adaptive_windows.cpp` probe performs exact pairword normalization for the same seed, tracks the continuing two-sheet row chosen by actual gamma at every step, and monitors nested centred windows. The first deviation in the window of radius R is:

| radius R | first actual pairword mismatch |
| ---: | ---: |
| 5000 | 39,671 |
| 2000 | 47,731 |
| 1000 | 50,473 |
| 500 | 51,817 |
| 200 | 52,634 |
| 100 | 52,898 |
| 20 | 53,105 |
| 0 (midpoint) | 53,164 |

The centre boundary disturbance moves inward over a long span, with variable speed; 88-step sampled drifts are not constant and this is not asserted to be an exact 88-step glider. The centre at t=53,164 need not follow the unperturbed rank-two row. This is the **specific physical obstruction** to promoting the infinite two-sheet *abstract* invariant to an infinite decimal number certificate.

The same pairword-only C++ propagation visits t=0..85,000 with **at least one odd coefficient in the entire exact pairword at every state**, a sufficient arithmetic witness for nonpalindromicity because a palindromic decimal number has only even mirror-pair sums. This last **85,000-step claim is a single exact pairword implementation**, not an independently completed base-10^9 whole-integer replay; the three-engine full-integer check was completed only through t=50,473 in the earlier W30 commit. The final exact pairword length is 91,649 coefficients at t=85,000. These finite horizons do not prove nonpalindromicity beyond the stated t, even if the abstract two-sheet machine remains closed.

## Reproduce and constructive next direction

```
sh calculation/new_structures/agent-W30/run_sync.sh
sh calculation/new_structures/agent-W30/run_reset.sh
```

The first command builds the true-pairword gamma extractor, traverses the exact 1,800-state graph under the actual 60,000-bit gamma prefix, produces/verifies `sync_physical.json`, and independently checks the compact 32-state/680-bit reset and its infinite complement closure lemma's finite hypotheses. The optional second additionally does the 85,000-step parity/front probe (including the first centre loss); it can take longer under heavy shared CPU load. Compact deterministic data are `sync_physical.json` and `front_contacts.json`, and the code is alongside the earlier W30 sources in `calculation/new_structures/agent-W30/`.

The next actual *certificate* target is an absorbing/recharging **outer interface** that keeps a nonempty finite-width representative of the rank-two carrier away from its boundary while supplying a persistent odd coefficient or stronger palindrome-excluding witness. The local automaton now tolerates every real overflow switch and needs just one binary centre-state bit after a real 680-step reset, but neither the external safety witness nor a nondepleting interface has been proved. Nothing here establishes or refutes a base-10 Lychrel number, and no Lean proof is claimed.