# All-width non-erasure of strictly contiguous one-step defects in the decimal p12 lattice

**PAPER PROOF.** Scope: base 10, the *specific reachable* period-12 spatial-period-9 lattice in `lattice_input.txt`, and the nine zero-overflow temporal phases t=1,2,3,5,6,7,9,10,11. This excludes a nonempty, connected interval of **lower-half pair coefficients every one of which differs from its baseline value** (with reflected upper-half changes), wholly within the spatially periodic bulk, from leaving the complete next pair word unchanged. The exterior and centre must be fixed; both sides of the interval must have sufficient unmodified bulk columns to reset incoming/outgoing carries. This is not a multistep centre nonexistence theorem, nor does it concern overflow phases t=0,4,8.

## Exact local equations

Write `P_i = P_(n-1-i) = q` for a palindromic pair coefficient word. Decimal normalization of P yields digits `O` with outgoing binary carry. At lower-half site i let `a` be the incoming carry on the lower side and `b` the carry **out** of the symmetric upper site. Choose new coefficient `x in {0,...,18}` and incoming upper carry `u in {0,1}`. The outgoing upper carry condition is `b = floor((x+u)/10)` and normalized pair sum at output position i is `(x+a)%10 + (x+u)%10`. In a no-overflow phase, preserving the *complete* successor pair word requires this sum to equal the baseline sum `s_i`. The next outer-to-inner cut state is `(a',b')=(floor((x+a)/10),u)`.

For a **strict** nonbaseline interval, require `x != q` at EVERY site, not merely the first. The coefficient q, the baseline output s, and the entering cut carries are nine-periodic in spatial index r=(i-34) mod 9; direct full normalization of each stored lattice row confirms the period on both input parities. Thus all possibilities form a graph of at most `9 * 2 * 2 = 36` vertices `(r,a,b)`, with every allowed `x` and `u` enumerated by the equations above. An arbitrary-length interval starting at a baseline cut with both boundary carries restored would give a directed path of *positive* length from `(r,a0(r),b0(r))` to a baseline cut `(r',a0(r'),b0(r'))`.

## Finite exhaustive certificate and completeness

The primary BFS explores every edge reachable after **at least one** mandatory changed coefficient, across all 81 temporal-phase/spatial-residue entry states. Every search exhausts its graph without reaching a baseline cut; no depth, time or state cap is applied. Reachable nonreturn-state counts for residues r=0..8 are:

| t | r=0,1,2,3,4,5,6,7,8 |
|---|---|
|1|0,0,0,0,3,0,0,1,0|
|2|0,0,0,0,6,0,0,5,0|
|3|0,0,0,0,0,0,0,0,0|
|5|0,3,0,0,1,0,0,0,0|
|6|0,6,0,0,5,0,0,0,0|
|7|0,0,0,0,0,0,0,0,0|
|9|0,1,0,0,0,0,0,3,0|
|10|0,5,0,0,0,0,0,6,0|
|11|0,0,0,0,0,0,0,0,0|

Because every possible positive-length path either revisits one of at most 36 states or terminates, the exhausted BFS proves **every finite length**, not just the inspected widths. Conversely, any input perturbation satisfying the stated hypotheses creates exactly one path: unchanged exterior fixes the initial cuts; full one-step output equality imposes the local equal-sum equation at every changed column; eventual unchanged columns and the non-neutral periodic cells restore both carries at the far cut. Since no such accepting path exists, the proposed strictly contiguous one-step erasure is impossible. The data are a finite proof certificate to this conditional statement. No claim is made about perturbations that may contain one or more unchanged cells inside their overall span.

## Independent reproduction and sensitivity controls

From the repository root, execute:

```
python3 calculation/decimal_frontier/lattice_kinks/strict_contiguous_gamma0/run_checks.py
```

This runner requires only Python 3 and the **snapshot of the exact lattice input committed in this result**, and invokes:
1. `classify.py`, direct BFS over tuple states with all 19 coefficients and both upper carries, matching the committed 9x9 `counts.json` table.
2. `independent_check.py`, a separately implemented 36-bit integer adjacency-matrix closure (no import from the primary program), for all 81 roots, for both n=800 and n=801. It independently constructs ordinary canonical positive integers, computes `N+reverse(N)` using Python large integers, and tests all 100 interior periodic columns in each time phase.
3. **Positive controls:** t=1 seven-column baseline `[4,5,10,14,13,12,9]` -> replacement `[9,5,0,15,3,12,14]`; t=2 baseline `[9,11,1,10,8,5,9]` -> `[14,10,11,9,18,5,4]`. Their entire successor pair words agree by independent ordinary integer arithmetic at both n=800 and 801, but they have unchanged internal cells. **Negative control:** all 18 different one-site substitutions at t=2,r=7 fail one-step pair-word equality.

Expected terminal lines: `STRICT_CONTIGUOUS_ALL_WIDTH_EXCLUSION_PASS 81 rooted start states`, `INDEPENDENT_MATRIX_81_ROOTS_EVEN_ODD_PASS`, `CANONICAL_BIGINT_7_COLUMN_POSITIVE_CONTROLS_PASS`, `CANONICAL_BIGINT_18_SINGLE_SITE_NEGATIVE_CONTROLS_PASS`, `FULL_TWO_ENGINE_REPRODUCIBILITY_PASS`. No external solver, Lean file or external data download is required. The mandatory base-9/base-13 automaton controls apply to **new exterior censuses**, which this result is not.

The prior `Agent5P12BulkCollisionTransfer` found positive finite-support collisions with some coefficient positions unchanged. This new theorem identifies a stricter all-width obstruction and does not re-publish those positive collisions or assert any periodic centre obstruction.
