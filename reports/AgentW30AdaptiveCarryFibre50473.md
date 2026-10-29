# Agent W30: arbitrary-overflow cyclic carry fibres and the decimal 50,473-step centre

**Status: COMPUTED**, with an elementary **conditional one-step soundness argument** below. No infinite decimal orbit is established, and nothing here is Lean-verified. Follows directly from W30's committed `AgentW30OddFiveCarrier` and `AgentW30MirrorLockedCarrier26710` results, using the *same* explicit seed.

## Why this is not the old 40-phase pump

The alternating overflow clock required by the first two W30 constructions fails at step 26,710 (actual bit 0 rather than 1). Nevertheless, an interior five-periodic coefficient wave persists in the real reverse-and-add orbit. Its subsequent rows include coefficients equal to 9, so the previous 9-free radius-one rule does **not** apply. Many phases have no odd coefficient, so an odd-carrier safety proof does **not** apply either. The new structure is an exact **two-sided cyclic carry-fibre automaton**, which accepts *both* actual overflow bits without treating 9 as absorbing.

For the least-significant-first, palindromic coefficient word `P_i=d_i+d_(n-1-i)` of a canonical decimal integer, put `c_(i+1)=floor((P_i+c_i)/10)`, with `c_0=0`, and `a_i=(P_i+c_i)%10`. The next pairword is `Q_i=a_i+a_(n+gamma-1-i)` where `gamma=c_n` is the *actual* overflow bit. This identity is exact, including when a high extra digit is produced.

## Period-five cyclic carry-fibre map

Let `r=(r_0,...,r_4)` be a 5-periodic interior row of coefficients in `0..18`. Define `cl_i` (forward cyclic carry) and `ch_i` (backward cyclic carry) by the simultaneous finite equations, subscripts modulo 5:

```
cl_(i+1) = floor((r_i + cl_i)/10)
ch_(i-1) = floor((r_i + ch_i)/10)
```

We require exactly one carry solution in each direction, with all carries 0 or 1. For any r with at least one symbol unequal to 9, both circular systems have a unique solution: a digit p<9 maps either carry to 0, p>9 maps either carry to 1, whereas p=9 transmits it. Every traversal of five positions thus coalesces both initial carries. In contrast, a row consisting entirely of 9s has two solutions, and the checker **rejects** that state rather than silently freezing its carry.

The phase-independent, piecewise-affine local row map for the actual global overflow `gamma∈{0,1}` is:

```
F_gamma(r)_i = ((r_i + cl_i) mod 10)
             + ((r_(i-gamma) + ch_(i-gamma)) mod 10).
```

An interior coefficient at output position i depends on a high mirrored digit shifted by gamma sites. This is why the second term uses the reverse-direction carry fibre and `i-gamma`, instead of the naive same-carry or same-position formula. If `r` is also physically compatible with a palindromic interval about an axis `delta` (that is, `r_i=r_(delta-i)`), then the new axis is `delta+gamma (mod 5)`.

**Conditional local soundness.** Suppose a true finite palindromic pairword has a periodic interval with row r and mirror-compatible axis delta, and that a target position lies at least five sites inside the interval on *both* relevant mirrored sides. Every length-five interior source segment contains a coefficient different from 9, which erases dependence on an unknown incoming carry by the end of the segment. Low-side and high-side normalized digits therefore follow their unique cyclic carry fibres. Pairing the actual normalized digits, with the true global overflow bit gamma, yields exactly `F_gamma(r)` at each such target position. A five-site margin at each end is a conservative sufficient bound. Reflection gives the axis update. Iterating this implication is sound for as long as the shrunken periodic interval remains nonempty, regardless of how the *global* overflow word changes. This is **not** a replenishment rule: the finite interval can be eaten by incoming boundary defects, and an unbounded instance would need a separate nondepletion certificate and a palindrome-excluding witness.

## Closed 1,800-state semigroup component

Starting at `(r,delta)=((17,3,14,3,17),4)`, follow *both* `F_0` and `F_1` and update `delta` accordingly. `fibre_graph.py` constructs the entire reachable graph using exact small-integer arithmetic. There are **exactly 1,800** reachable `(row,delta)` states, **3,600** labelled transitions, **zero** undefined/ambiguous transitions, and one strongly connected component of all 1,800 states. Every state is mirror-compatible with its current axis, and every successor remains in the same set. Thus **the five-site bulk can be driven by any binary overflow sequence**, without relying on a periodic clock. This is an unrooted interior statement, not a claim that an arbitrary overflow schedule is realizable by a complete decimal integer orbit.

State statistics: 360 states in each of the five reflection-axis classes; 190 states have at least one coefficient equal to 9; 1,290 have at least one odd coefficient and **510 have only even coefficients**. The last statistic explicitly prevents promotion of this local closed graph alone to a nonpalindromicity certificate.

`test_adaptive_graph.py` independently verifies every one of the 3,600 edges. For each state it makes a palindromic periodic coefficient word with an even length and a one-site symmetric cap: coefficient 1 forces no overflow, coefficient 17 forces overflow. It constructs an actual positive canonical decimal integer, independently computes `n + int(str(n)[::-1])`, and compares **every safely interior coefficient** against `F_0`/`F_1`. That totals **298,800** independently checked coefficient identities, with no mismatch. It also determines both carry fibres by a **different** calculation (12 serial spatial periods starting from carry zero), compares every carry, and confirms the 1,800-state SCC by iterative Kosaraju rather than reusing the forward traversal routine.

## Independent full-integer replay and exact first window break

Use the identical earlier W30 seed:

```
P0 = B0 ++ (W0)^300 ++ (17,3,14,3,17)^8400
   ++ reverse((W0)^300) ++ reverse(B0).
```

Here `B0` is the length-39 and `W0` the length-20 decimal p8/m20 exterior from `calculation/new_structures/agent-N10/phase.json`; both literal blocks are also included in W30's self-contained `replay.cpp`. The canonical seed has 54,078 digits. At *every* time t, compute gamma from the true pairword addition, apply the appropriate `F_gamma` to the five-site row, and compare the 2,001 coefficients centered at `floor(n_t/2)` to the phase-independent periodic prediction.

`adaptive_replay.cpp` independently advances (1) a pairword-normalization engine, (2) ordinary decimal digit-array addition, and (3) a separate arbitrary-precision base-10^9 limb integer that reverses **its own canonical string** and adds its own limbs. It checks the **entire true integer string** and **entire true pairword** at every one of **50,474 states**, checks for a palindrome at every state, and checks all 2,001 centre positions at every t from 0 through 50,472. The actual gamma is used throughout; no forced clock remains. At t=50,473 exactly one coefficient, at offset +1,000 from the midpoint, first disagrees with the predicted 5-period row (its reflected partner is immediately outside the sampled 2,001-site window). This is a **local boundary disturbance**, not a palindrome. The full integer is still nonpalindromic there.

Selected deterministic checkpoints `(t, decimal length, cumulative overflows)`:

```
(0,     54078,     0)
(20000, 64078, 10000)
(26710, 67433, 13355)
(30000, 68801, 14723)
(40000, 72943, 18865)
(45000, 75037, 20959)
(50000, 77133, 23055)
(50473, 77328, 23250)
```

The first departure from the old fixed clock is the edge at t=26,710; the first centre phase with all-even coefficients is t=26,712; the first with coefficient 9 is t=26,716. Every row remains carry-unambiguous and reflection-compatible up to the 50,473-window failure. A 50,473-step computation is finite evidence only: the unknown next-centre structure after the disturbance is not asserted to remain five-periodic.

## Reproduction and next constructive question

From repository root run:

```
sh calculation/new_structures/agent-W30/run_adaptive.sh
```

The script first exhaustively traverses the finite two-labelled graph and executes **both** overflow controls against real Python integers, then compiles the full replay with `g++ -std=c++17 -O3 -Wall -Wextra` and runs 50,473 true additions with exact whole-number and whole-pairword checking. It generates a deterministic graph summary `adaptive_graph1800.json`; `adaptive_50473.json` records full-number checkpoints and exact failure. `fibre_graph.py` is intentionally standalone and can be reused to explore shorter safe SCC subgraphs or candidate interface compatibility conditions.

The precise missing ingredient is now a **refillable seam/outer boundary** that feeds this arbitrary-clock, closed 1,800-state centre without consuming the finite guard. Because 510 centre states are all-even, such an interface must also supply a persistent external nonpalindrome witness (or a stronger invariant than oddness). No negative conclusion about the existence of decimal Lychrel numbers follows. No Lean files were written: Lean 4.19.0/full `tools/verify.py --changed` were not available from the container checkout.