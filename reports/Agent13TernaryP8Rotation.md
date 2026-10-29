# Eight-step complementary-rotation obstruction for a decimal ternary automatic centre

**PAPER PROOF** with a complete finite-state enumeration and independent arithmetic checks. This extends the distinct earlier result `Agent13TernaryP8PhaseReturn` from overflow word `10101010` to its complementary phase `01010101`. It is not a certificate for a decimal Lychrel number, not a general kink impossibility theorem, and is not Lean-verified.

## Exact theorem and limits

Let `x` be the infinite fixed word for `μ(0)=01, μ(1)=02, μ(2)=00`. Take any palindromic decimal pair-coefficient template whose lower interior contains an arbitrarily shifted factor of `x` of length 32, coded injectively by three distinct coefficients `A_0,A_1,A_2 ∈ {0,...,18}`. Suppose the interval and its reflected partner stay strictly away from the literal exterior and centre boundaries during eight ordinary reverse-and-add steps with overflow bits `01010101`. Then its aligned final length-28 coefficient interval **cannot** be an injectively re-encoded length-28 factor of `x`, at any shift. There are no restrictions on the seven intermediate pairwords or their alphabets.

This excludes only this ternary factor endpoint format and overflow phase. It does not address noninjective endpoint coding, other substitutions, shifts outside the aligned local transition, shorter input intervals, other overflow schedules, general base-10 cycles, or the integer 196.

## Carry transducer and soundness (PAPER PROOF)

All pair-coefficient words are least-significant-first and palindromic. For a lower interior interval `w` of length `L`, normalize it from an arbitrary incoming left carry `cL∈{0,1}` to decimal digits `lo`. Independently normalize `reverse(w)` from an arbitrary right entering carry `cR∈{0,1}` and reverse the resulting digits to obtain `hi`. All actual global carry states are among the four pairs. If overflow `γ=0`, the next local pair coefficients are `q_i=lo_i+hi_i`, `0≤i<L` (length `L`). If `γ=1`, they are `q_{i-1}=lo_i+hi_{i-1}`, `1≤i<L` (length `L-1`). All coefficients remain in 0..18. Every actual orbit follows one trajectory in the nondeterministic finite transition that allows **all four** boundary-carry pairs at every step. Thus an empty reachable intersection is a rigorous no-go; a surviving local word is only a necessary-condition candidate.

The eight-step word `01010101` has four overflows, hence a length-32 input yields length 28. The *prefix-cropping lemma* holds at each step: crop a longer input to a shorter left prefix, retain its left incoming carry, and choose the cropped right incoming carry to equal the actual carry after the omitted right-hand part; the corresponding output left prefix equals that of the long transition (with one fewer position for `γ=1`). Induction gives inclusion of eight-step reachable prefix words. Therefore every candidate at length32→28 would have a candidate length28→24 with the same source coefficient table. No assumption of centre periodicity is needed for this implication.

## Exhaustive short-window classification (COMPUTED sublemma)

An exact terminating factor-language recurrence follows from the two-uniform substitution: `L₂={00,01,02,10,20}`; for `n≥3`, `L_n` is the set of length-`n` offset-0 and offset-1 factors of substituted `L_ceil((n+1)/2)`. It gives `|L₂₄|=64`, `|L₂₈|=72`, `|L₃₂|=80`. The primary C++ engine instead generates all factors from the 65,536-letter substitution prefix; a separate Python checker confirms equality of these languages, not merely matching their counts.

The primary engine enumerates every one of `19·18·17=5,814` ordered distinct coefficient triples and all 72 length-28 source factors: **418,608** exact start cases. It propagates every carry possibility through all eight steps and deduplicates full base-19 packed states, not hash keys alone. State cap is 50,000; **zero runs capped**, with maximum observed **1,260** states. Exactly **72** source-factor matches remain at length28→24, on **18** distinct coefficient tables, four source factors per table; all other **5,796 tables** have zero matches. The full 18-table compact exact data, including per-table state maxima, is in `exceptions.tsv`. The raw 5,814-row run is reproduced outside the repository and checked for index/order/completeness; no partial census or log is committed.

## Complete exceptional-case elimination and independent checks

For each of the 18 exceptional input tables, a separate Python tuple-based engine enumerates all **80** exact length-32 factors of `x`, all incoming carry choices at all eight steps, and every resulting length-28 equality pattern. Exactly **0** endpoint factors are compatible for each table: **1,440** exact longer-factor/table checks in total. An independently implemented Python replay agrees with each table's four short-window matches. By the prefix-cropping lemma, all other tables were already excluded at length 28→24, so the theorem holds for the full stated length32→28 scope.

Further independent checks: **3,000** ordinary big-integer digit/reverse-add cases (both overflow parities), **5,000** randomized prefix-cropping controls, and complete language comparison `L24/L28/L32`. The mandatory known positive base-9 control `g=1100011000, |B|=61` and both base-13 controls `g=1010010000, |B|=75,55` are independently replayed using the previously committed control engine. These are validation controls, not newly found certificates.

## Reproduction

From the repository root, with a C++17 compiler and Python 3, no other dependencies:

```sh
sh calculation/decimal_frontier/ternary_p8_rotation/run.sh /tmp/agent13-ternary-p8-rotation
```

The runner compiles `p8_nfa_rotated.cpp`, runs a resumable single-process nicened exact census in 500-table shards, writes the full TSV to the specified external directory, runs `verify_rotation.py` with independent checks in fresh subprocess batches, and performs the base-9/base-13 positive controls. Source, independent checker, compact exception data, and exact commands are committed together in `calculation/decimal_frontier/ternary_p8_rotation/`. The full `python3 tools/verify.py --changed` could not run in the local environment (no checkout/Lean), so this result claims PAPER PROOF and finite exact computation, not LEAN-VERIFIED.

**No claim that a decimal Lychrel integer exists or cannot exist is made.**
