# W04: a decimal simultaneous two-band rebound with a twelve-edge carry certificate

**PAPER PROOF** for all-width (two independent counters) finite twelve-step propagation and exact first-six-step simultaneous growth. **PAPER PROOF conditional on full finite-state trace** for 20,000-step independently padded seeds. **COMPUTED** for two completely separate 20,000-step ordinary-number engines and a complete machine-checked finite carry proof object. **UNDECIDED** at infinite time; neither a base-10 Lychrel number nor a Lean proof is claimed.

## Constructive root and exact positive drift

For arbitrary **independent** integers `m,n >= 10` let the least-significant-first *half* of the symmetric pair-coefficient word be

    H0(m,n) = [11,9,8,17] ++ 8^m ++ [17,7] ++ 16^n ++ [8].

The complete initial pairword is `H0 ++ reverse(H0)`. Every coefficient is between 0 and 18 and the first coefficient 11 is positive. Realize the **literal decimal integer** by splitting each coefficient `p` into high-side digit `min(p,9)` and low-side digit `p-min(p,9)`; its most-significant digit is 9. The pairword contains odd entries so it cannot be a palindrome.

**NEW simultaneous replenishment identity, for EVERY independent m,n>=10:** After exactly SIX genuine reverse-and-add steps the whole folded pairword is

    H6(m,n) = [15,6,17] ++ 8^(m+1) ++ [6,10] ++ 16^(n+1) ++ [8].

The source has **exact** two ordered bulk lengths `(m,n)` and the target has exact bulk lengths `(m+1,n+1)`; this is a literal gain of one in each repeated band, **not** a spurious gain from counting a pre-existing adjacent 8 or 16. It is driven by a finite outer/coupling interface, not by guessing a stationary p8 kink. The source centre `[17,7]` and exterior `[11,9,8,17]` are both transformed, so the interface is NOT reproduced. This is compatible with earlier p8 short-centre exclusions, which assumed an invariant exterior and a return cycle.

## All thirteen explicit halfwords (each exact independently pumpable two-counter cylinder)

Write `H_t(m,n)=L_t ++ x_t^(m+a_t) ++ J_t ++ y_t^(n+b_t) ++ R_t`. The flags `odd` and `gamma` are the exact parity of the whole source pairword at t and its overflow on the step t→t+1. All entries are *coefficient values* (0..18), not decimal digits. The following table is fully encoded in `rebound_witness.json` and independently reconstructed by `rebound_pdr.py`:

| t | L | x | a | J | y | b | R | odd | gamma |
|---:|---|---:|---:|---|---:|---:|---|---:|---:|
| 0 | 11,9,8,17 | 8 | 0 | 17,7 | 16 | 0 | 8 | 0 | 1 |
| 1 | 2,1,18 | 16 | +2 | 15 | 14 | 0 | 15,16 | 1 | 0 |
| 2 | 4,3,17 | 14 | +2 | 12 | 10 | 0 | 12,14 | 1 | 0 |
| 3 | 8,7,15 | 10 | +2 | 6 | 2 | 0 | 6,10 | 1 | 0 |
| 4 | 16,15,11 | 2 | +1 | 1,13 | 4 | 0 | 13,0 | 1 | 1 |
| 5 | 7,13,8 | 4 | +1 | 3,5 | 8 | +1 | 4 | 0 | 0 |
| 6 | 15,6,17 | 8 | +1 | 6,10 | 16 | +1 | 8 | 0 | 1 |
| 7 | 6,12,14 | 16 | +1 | 14,7,8 | 14 | 0 | 15,16 | 1 | 0 |
| 8 | 13,5,10 | 14 | +1 | 9,15,17,9 | 10 | −1 | 12,14 | 1 | 1 |
| 9 | 4,9,6,6 | 10 | 0 | 5,6,14,8,1 | 2 | −2 | 4,8 | 0 | 0 |
| 10 | 8,18,12,13,1 | 2 | −2 | 1,11,13,8,17,2 | 4 | −2 | 8,16 | 0 | 0 |
| 11 | 17,17,6,7,3 | 4 | −2 | 3,3,7,18,14,5 | 8 | −2 | 17,13 | 0 | 1 |
| 12 | 8,16,14,13,10,7 | 8 | −3 | 7,6,10,16,14,10,13 | 16 | −2 | 12,8 | 1 | — |

Overflow itinerary: `1,0,0,0,1,0,1,0,1,0,0,1`. All phases have at least one fixed odd coefficient within L or J independent of m,n; their even uniform bulk symbols preserve odd witnesses. Thus all thirteen represented ordinary integers are nonpalindromic. The physical seed and twelve integer steps are confirmed by 99 independently parameterized Python big-integer controls.

**Where the regenerative mechanism fails** is now exact: after the SECOND six-step block the full halfword is

    H12(m,n) = [8,16,14,13,10,7] ++ 8^(m-3)
                ++ [7,6,10,16,14,10,13] ++ 16^(n-2) ++ [12,8].

Relative to the peak at t6, the two counters lose **four** and **three**. Relative to t0, the twelve-step drift is `(-3,-2)`. Additionally L, J, R have not returned, so the positive six-step transportation law cannot simply be iterated. The constructive target is a second interface restoring `[11,9,8,17]` and `[17,7]`, or some finite graph of interfaces, with nonnegative total drift. No such return is asserted.

## Why the finite checker proves this for ALL independent m,n >= 10

At a folded input coefficient p with an exact base-10 decimal reverse/add normalizer, define two-ended transducer state `(a,z,h)` with a∈{0,1} the low incoming carry, z∈{0,1} the outgoing high carry, and h∈{0,...,9} the previously normalized high digit. The first position has a fixed overflow initialization. For guessed high incoming carry r∈{0,1}, check

    z = floor((p+r)/10),
    a' = floor((p+a)/10), z' = r, h' = (p+r) mod 10.

The target folded coefficient is `(p+a)%10 + h'` on a nonoverflow edge, or `(p+a)%10 + (1 if first column else h)` on overflow. At the centre, check low/high carry meeting and the odd/even terminal equation. The 40 possible ordinary states produce an exact *sound and complete* relation for the entire physical arithmetic step, not a heuristic finite-horizon trajectory.

For each of the 12 edges at **m=n=10**, `rebound_pdr.py` checks the entire source and target folded halfwords against the independently calculated complete digit-normalized result, verifies every carry-state component/transition, and finds two distinct ordered column positions strictly within the respective **aligned** source and target uniform bands where `(a,z,h)` is unchanged. The complete positions, states and source/target symbols for all 24 loops are stored in `rebound_witness.json`. These particular loops are not a universal *guess*: their state equality is checked using actual source carry vectors and target output digits, and corrupted certificate state bits are rejected.

Inserting `q>=0` extra copies at the first loop and `r>=0` at the second leaves the exact accepted transducer path unchanged outside the inserted columns; since both source and target letters at each loop are their corresponding uniform-band symbols, the source and target become exactly `H_t(10+q,10+r)` and `H_(t+1)(10+q,10+r)`. The loops are disjoint and independently pumpable; no forced `m=n` synchronization is present. Decimal normalization is deterministic, so every accepted edge is the true arithmetic edge. This proves **all m,n>=10** for each of twelve edges, and induction proves the thirteen-phase theorem. This is a fully explicit **finite paper certificate plus executable checker**, not a Lean-kernel theorem.

The positive charge-transfer is not merely a source digit-splitting or a carry-mask erasure from N28: its source **pairword itself** has two uniform runs that simultaneously grow by one in the sixth successor, with a different finite interface. The short-lived nature of the emitter is separately quantified at t12.

## 20,000-step independent rectangular family, conditional finite-trace proof

For the m=n=15000 reference seed, `rebound_20k.cpp` advances a **real ordinary decimal digit vector** with schoolbook low-to-high carries for every t=0,...,20000. Every state is checked for palindrome and both ordered phase-six bulk runs. Every **single** one of the 20000 edges is also checked for two disjoint *complete two-ended carry-state self-loops*, one in each aligned ordered bulk. Source and target matched runs overlap by at least 1,785 and 1,777 coefficients, and a fixed odd coefficient exists at every state (observed minimum 2). All repeated bulk coefficients are even, so separately extending each run cannot remove these nonpalindrome witnesses.

By exactly the same independent self-loop pumping induction as above, this *finite-horizon trace certificate* proves:

    For EVERY independent m,n>=15000 and EVERY 0<=t<=20000,
    the real decimal orbit of H0(m,n) is nonpalindromic and has
    the exact reference folded pairword extended independently
    by (m-15000) and (n-15000) aligned bulk cells.

This is a finite-horizon **PAPER PROOF conditional on complete reproducible COMPUTED witness**, NOT infinite-time PDR closure. The independent counter resources do eventually erode; nothing is claimed at t>20000.

For a genuinely off-diagonal control seed m=15000,n=16000, two **unrelated arithmetic kernels** compute **all 20001 ordinary decimal integers** through t20000:

- `rebound_20k.cpp`: individual decimal digits stored as bytes and direct decimal digitwise carries; every step checks 2 independent band pumps and odd witnesses as well as no palindrome.
- `rebound_limbs.cpp`: independent base-10^9 big-integer *limbs* with carries on each 9-digit word; reverse the full decimal representation, reparse as limbs, and add as ordinary arbitrary-precision integers; every step checks no palindrome and the ordered bulk bands. This is not an adapter around the digit-vector kernel or pairword normalizer.

They agree on **all 20001 lengths and run-length metadata** via the same running digest, and independently compute matching **full-number FNV64** on five checkpoints:

| t | digits | first run | second run | full-number FNV64 |
|---:|---:|---:|---:|---|
| 0 | 62,014 | 15,000 | 16,000 | `37cd5281dcdae7fc` |
| 5,000 | 64,077 | 11,712 | 12,731 | `e10d533a81710d70` |
| 10,000 | 66,123 | 8,420 | 9,450 | `1edfd3ab27898378` |
| 15,000 | 68,217 | 5,083 | 6,106 | `1ef37074d9b6576d` |
| 20,000 | 70,307 | 1,785 | 2,777 | `a2f2c583292cc46` |

At t20000 the complete 20001-state metadata digest is `6f3ff2b0df7482b0`. On the diagonal reference the last value is 68,307 decimal digits; minimum aligned overlap widths 1785,1777; last full-number FNV `2e1b5c25c2f3f496`. A separate GMP/mpz_class control independently matched the off-diagonal digit engine through t10000 but reached an execution limit on a 20k run; we do not claim it completed all 20k. Instead the dedicated base-10^9 integer kernel completed the entire 20k independently. All expected data and a deliberately corrupted-fingerprint rejection are encoded in `rebound_checkpoints.json`.

### Reproduction and precise scope

From the repository root:

    bash calculation/new_structures/agent-W04/run_rebound.sh

This regenerates the independent finite 12-edge witness, 99 Python big-integer small controls, and the two full 20k off-diagonal decimal integer traces (plus the full diagonal baseline for the universal pumping rectangle); verifies the 24 carry-loop tiles, parity/overflow words, 20000 two-counter pump edges, exactly five full-number checkpoints and a negative corrupted-certificate/fingerprint control. Successful exit prints `AGENT_W04_REBOUND_ALL_CHECKS_PASSED`. All code and data are in the **same result commit** under `calculation/new_structures/agent-W04/`, using Python3 and a C++17 compiler, without GMP or external Python modules. `python3 tools/verify.py --changed` was unavailable because local shell GitHub cloning could not resolve; no Lean verification is claimed.

## Why this matters for the infinite certificate problem

This supplies a **concrete two-resource replenishing interface tile** in base 10, whereas the prior N19 six-phase interface had cumulative vector `(-5,-2)` and the N28 mask quotient erased rather than emitted repeated cells. The new finite tile has exactly `( +1,+1 )` over six steps. The second six-step computation proves that the ambient interface lacks renewal, losing `(-4,-3)` from the peak and changing the overflow itinerary. A plausible next successful PDR state needs **at least two interface types** with an accepted return path whose net two-counter drift belongs to the nonnegative cone. Search the exact sixteen/twelve-phase exterior carry graph or a growing-centre grammar; a single short centre with fixed p8 exterior is not implied. This positive emitter is a reusable witness for that synthesis, not an infinite orbit.