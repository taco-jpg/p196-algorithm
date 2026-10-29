# Agent-N22: decimal rec2 drifting centre, an exact 20,000-step candidate

## Result and limitations
**COMPUTED, finite horizon only.** This is a constructive decimal orbit family, not a finite certificate of an infinite Lychrel orbit, and not a statement about 196. A specially chosen odd centred seam maintains a long period-8 exterior. A central defect invades that lattice at a measured mean rate of 1.16 **pairword sites per eight steps** across 20,000 steps; it has not disappeared or settled into a finite glider cycle. At 33,062 steps the rooted outer period-8 word first fails (phase 6, coefficient 10). Thus the seed is explicitly **not certified to be Lychrel**.

## Exact seed and claimed evolving shape
All words below are least significant coefficient first. Let `B_t` be row `t mod 8` of `B.csv` (width 11), `W_t` row `t mod 8` of `rows.csv` (spatial period 48), and `A_q = B_0 ++ W_0^q ++ [10,14,1,10]`. The palindromic pairword seed is `P_0(q) = A_q ++ reverse(A_q[:-1])` (odd length, centre coefficient 10). Construct ordinary decimal integer `N_0(q)` by decomposing each pair coefficient `p_i` into most-significant-side digit `min(9,p_i)` and least-significant-side digit `p_i-min(9,p_i)`; the centre digit is 5. This construction is deterministic, with no leading zero.

For each `t=0..20000` of `N_{t+1}=N_t+rev_10(N_t)`, define the lower-half pairword `p_t(i)=digit_i(N_t)+digit_{n_t-1-i}(N_t)`. For **q=100** the independent verifiers check `p_t[:11]=B_t`, then `p_t[11:11+L_t]=W_t^infinity[:L_t]`, where `L_t` is the *maximal* consecutive prefix match. At every step `L_t >= 1900`. They also check no palindrome, and `n_{t+1}-n_t = (t+1)%2` (overflow pattern 10101010). The whole remaining interval is an unconstrained, symmetric, *growing* central defect `C_t`, whose length need not be periodic. This is the new structure, not a narrow stationary kink.

## Drift and growth measurements
The length is 9,629 at t=0 and 19,629 at t=20,000. The interface `11+L_t` moves from pairword site 4,811 to site 1,911; at the same time the half-length increases from 4,815 to 9,815. The central defect half-width thus increases **4 -> 7,904** (full central word 7 -> 15,807). Across 2,500 eight-step clock cycles the net interface displacement is -2,900 sites, while centre half-growth is +5,000 sites. This is an observed net drift, **not** an exact constant-speed glider. Each phase's first 11 coefficients recur every eight steps until the front arrives.

A short centred-seam transient is unusual: for `q=100`, `L_0=4800`, while the first 136 steps lose at most two bulk sites. Afterwards the drift becomes steadily negative, including fluctuations. Controlled shorter specimens (same seam, q=1,2,3,4,8,10,20) first lose the rooted B clock at t=456, 790, 1110, 1422, 2736, 3390, 6656. A diagnostic run for q=100 finds the first B violation at **t=33,062** (coefficient 10 of phase 6), so finite survival cannot be promoted to an infinite certificate. This failure redirects the search toward a **positive-speed phase-locked centre interface** or a centre repair automaton, not another fixed-width exclusion.

## Independent arithmetic and reproduction
Run from repository root:

```
bash calculation/new_structures/agent-N22/run.sh
```

- `replay_digits.cpp`: exact native decimal digit-vector addition, checks **all** 20,001 pairword prefixes, whole-number palindrome, all 20,000 overflow bits and the maximal lattice match. Its output checks full-number checkpoints at 18 selected times.
- `replay_gmp.cpp`: independently constructs the seed as a decimal string, then uses `mpz_class` arbitrary precision **integer addition and decimal-string reversal** at each of 20,000 steps, checking no palindrome, the exterior B11 and W128 at every step, all overflows, and exact equality of all 18 whole-number checkpoints produced by the digit-vector oracle.
- `replay_bigint.py`: third, ordinary Python-int confirmation of the first 100 steps (full checkpoints) and the exterior contract, deliberately time-bounded because Python decimal integer conversions are expensive.
- Controls: decimal seed 89 first reaches a palindrome after exactly 24 steps; a corrupted `W_0[0]` is rejected; q=100 first loses exterior at 33,062. `stats_sample.csv` provides the digit-oracle snapshots (every 80 steps and initial steps).

**Scope warning:** the seed can be generated for every q, but the 20,000-step statement was checked at **q=100 only**. The experimental front trajectory does not prove persistence for any unbounded time. No Lean theorem or new decimal Lychrel number is claimed.
