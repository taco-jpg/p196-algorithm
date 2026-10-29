# Closing the decimal ternary automatic-centre overflow-one case

**PAPER PROOF** using a finite exhaustive lemma, independent big-integer replay, and all-boundary-carry verification. Extends the already committed `Agent13TernaryOverflowObstruction` from nonneutral ternary coefficient tables to **all pairwise-distinct decimal tables**, including those containing `9`. It does not give a decimal Lychrel number or exclude multistep phase-changing centres.

## Scope and theorem

Let `μ(0)=01, μ(1)=02, μ(2)=00`, `x=lim μ^k(0)`, and let `P` be a palindromic base-10 pair-coefficient word. Suppose an interior length-16 factor of its lower half is an injective coding `a(x_i)` of an arbitrary factor of `x`, where `a_0,a_1,a_2` are pairwise distinct in `[0,18]`. Suppose ordinary reverse-and-add on `val_10(P)` has overflow `γ=1`, and suppose the six output pair coefficients aligned with interior positions `i=5,...,10` are required to be some length-six factor of `x` under an injective target coefficient coding. **These conditions are inconsistent.** Source/target factor shifts are arbitrary, and the literal exterior may be arbitrary as long as these positions stay interior and the stated overflow occurs.

The earlier `Agent13TernaryOverflowObstruction` proves the stronger base-generic statement for all input tables with no neutral coefficient. The new case is exactly the `3·18·17=918` injective decimal coefficient tables containing `9` (the only neutral coefficient). Together, the two results cover all `19·18·17=5814` injective three-coefficient decimal input tables at an overflowing step.

## Why a finite core window is enough

For decimal coefficients in `[0,18]`, the outgoing carry map of coefficient `a` on incoming bits `c∈{0,1}` is constant `0` if `a≤8`, the identity if `a=9`, and constant `1` if `a≥10`. The exact factor language of `x` has **no run of four identical letters**, as checked from the complete `L_4` with the substitution recurrence in the previous result. For a table with exactly one neutral symbol, any four consecutive positions include a nonneutral coefficient, so the four-column carry map is independent of its entering carry. This works in both low-to-high (lower half) and reflected high-half directions.

Consequently, with a five-symbol guard at each end of an arbitrary length-16 source factor, the six interior output coefficients at positions 5 through 10 depend only on that factor, not on the unknown carries or on more remote words. For `γ=1` the opposite output digit partner of lower original position `i` lies over source coefficient position `i-1`. To compute its digit, normalize both the source factor and its reversal with either entering carry 0 or 1. Let `L_i` be the forward digit and `R_j` the reversed-factor digit; then the exact interior coefficient is `Q_i=L_i+R_(16-i)`. The four arbitrary choices of two incoming carries must yield the same six-word; the checker verifies this for **every** source factor and coefficient table, and the carry-reset argument proves it for every context.

## Exhaustive factor-language exclusion

The terminating exact factor recurrence is `L_2={00,01,02,10,20}` and, for `n>=3`, `L_n` is the collection of offset-0/1 windows of length `n` within `μ(w)` for all `w∈L_ceil((n+1)/2)`. It gives `|L_16|=40` and `|L_6|=16`. A target injective relabelling preserves the equality pattern of the target word, so compare each six-word to the equality patterns of all 16 target factors.

`neutral_proof.py` enumerates exactly `918×40=36,720` source/table cases, each under **all four pairs of incoming carries**, for `146,880` exact finite carry computations. Every four-way output agrees, and **zero outputs** have an equality pattern compatible with a target factor. The finite enumeration has no solver, resource cap, or probabilistic sampling. This establishes the stated negative theorem. It does not rule out overflow zero, phases with different intermediate languages, centres containing non-injective source codings, or the base-10 Lychrel existence question.

## Independent checks and reproduction

Run from repository root, Python 3 standard library only:

```sh
python3 calculation/decimal_frontier/ternary_neutral/neutral_proof.py
python3 calculation/decimal_frontier/ternary_neutral/neutral_independent.py
python3 calculation/decimal_frontier/ternary_neutral/controls.py
```

The independent checker derives `L_16` and `L_6` from an actual 65,536-symbol substitution fixed-word prefix, not the primary factor recursion. For each of the 36,720 inputs, it creates a palindromic pair word with overflow one, performs **ordinary Python big-integer base-10 digit extraction and reverse-and-add**, computes the exact next pair word, and independently rejects the same 36,720 cases. The required published positive controls for base 9 (`g=1100011000`, `|B|=61`) and base 13 (`g=1010010000`, `|B|=75,55`) plus the prior all-base nonneutral lemma are run by the `controls.py` script using existing committed source within this repository, with no machine-local data.

**Limitations:** `PAPER PROOF`, not `LEAN-VERIFIED`; the asserted theorem concerns a single overflow-one centre-to-centre step for this one ternary substitution, and its negative conclusion does not transfer to general quasi-periodic/automatic centres or to decimal 196.