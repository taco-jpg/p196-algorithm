# A ternary automatic-centre obstruction at one overflowing reverse-and-add step

**PAPER PROOF** (finite 100-case lemma checked by two independent programs). This rules out a precisely defined one-step centre-to-centre map for the primitive length-two substitution `μ(0)=01, μ(1)=02, μ(2)=00` in **every base**. It is not a Lean proof or a decimal Lychrel result.

## Statement

Let `x=lim μ^k(0)` and `b>=2`. In a symmetric palindromic **pair-coefficient word** `P` (least-significant coefficient first), suppose an interior interval in its lower half is a length-eight factor of `x` encoded by three distinct source coefficients `a_0,a_1,a_2` in `[0,2b-2]`, none equal to `b-1`. The interval is separated from both ends and the midpoint so that the six interior positions have both neighbors inside the interval. Suppose the ordinary reverse-and-add step has overflow one, i.e. the canonical digit word of `val_b(P)` has length `|P|+1`. Then its next pair word, on those six interior positions, cannot be an injective three-coefficient encoding of **any** length-six factor of `x`, regardless of source/target factor shifts, coefficient relabellings or symbol collisions induced by normalization.

Consequently a symmetric `x`-coded centre with a long nonneutral interior cannot map in **one overflow-one step** to another symmetrically `x`-coded centre with injective target encoding and the same aligned six positions. This says nothing about overflow-zero steps, neutral source coefficients, an unconstrained intermediate centre, other substitutions, or an eventual multistep cycle.

## Exact arithmetic reduction (no sampled lengths)

For each nonneutral coefficient `a` define `h(a)=0` for `a<=b-2` and `h(a)=1` for `a>=b`; these are the only possibilities. In the lower interior the incoming carry at a coefficient is `h` of its previous coefficient, independently of more distant digits. Set `f(a)=a mod b+h(a)`, an integer in `[0,b-1]`. For an overflow-one step the mirror of original position `i` in the output digit list is at index `|P|-i`, carrying the previous lower-side coefficient `a_{i-1}`; its incoming carry is `h(a_i)`. Therefore, with `s_i` the source symbol at position `i`, the next pair coefficient is exactly

`Q_i = f(a_{s_i}) + f(a_{s_(i-1)})`.

The substitution language has exactly the five digrams `00, 01, 02, 10, 20`; in particular **every adjacent pair contains 0**. Consequently the output depends only on one of **three** unordered pair types `00, 01/10, 02/20`, with values `2 f(a_0)`, `f(a_0)+f(a_1)`, `f(a_0)+f(a_2)`. Their equality pattern is one of the five partitions of three elements, even when some numerical values coincide. No assumption about their magnitudes or the base is needed in the following check.

## Exact finite-language lemma

`L_n` denotes the set of length-`n` factors of `x`. The complete digram set is `L_2={00,01,02,10,20}`: `01,02,00` occur within substitution images, and `10,20,00` across image boundaries, and all occur in `x`. For `n>=3` put `k=ceil((n+1)/2)`. Each length-`n` factor begins at offset `0` or `1` in the image of some `k`-letter factor, and conversely all such images occur, so `L_n` is **exactly** the union of those length-`n` windows of `μ(L_k)`. Since `k<n`, this is a terminating recurrence, not a prefix heuristic.

The recurrence gives `|L_8|=20` and `|L_6|=16`, with 13 distinct equality patterns among the target factors. For each of the 20 source factors, form the six pair types `(s_0,s_1), ...,(s_5,s_6)`. For every one of the **five** equality partitions of the three pair types, canonically rename equal values in order of first appearance. None of these `20×5=100` equality patterns belongs to the 13 target patterns. Since an injective target coefficient coding preserves equality and inequality of letters, there can be no matching target factor. This concludes the proof.

## Reproducibility and controls

From repository root, with Python 3 and no dependencies:

```sh
python3 calculation/decimal_frontier/ternary_overflow/proof.py
python3 calculation/decimal_frontier/ternary_overflow/independent.py
```

`proof.py` constructs the factor languages by the exact recursion and checks 100 canonical partition instances. `independent.py` separately generates a 65,536-symbol prefix of the substitution word (the complete `L_6/L_8` sets are independently confirmed), tests **all 27 raw mappings** of the three pair types to three output letters on all 20 source factors (540 incompatible cases), and compares the local equation to 2,500 ordinary big-integer reverse-and-add operations with base-`b` digit extraction in bases 2..29, alternating overflow-zero/overflow-one controls. It also replays the mandatory published base-9 `g=1100011000` exterior with `|B|=61` and both base-13 `g=1010010000` exteriors with `|B|=75,55`, first 30 overflow bits and 500 palindrome-free ordinary integer steps each. These controls are preexisting and are not new certificates.

**Limitations:** the theorem excludes only the stated length-eight nonneutral ternary source against an injectively coded length-six destination at one overflowing step. Its proof is paper-level, not kernel-checked in Lean; it does not establish that a particular decimal orbit is Lychrel or rule out a quasi-periodic centre that changes language on intermediate steps.