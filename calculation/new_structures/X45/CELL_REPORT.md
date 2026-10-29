# X45 CELL_REPORT: phase-0 cross-cell moving seam

**Status: PARTIAL.** This report proves an all-width necessary condition and a conditional all-width edge-lifting lemma. It does not exhaust the cross-cell graph and does not claim a decimal Lychrel certificate.

## Scope

Rooted decimal p12/m9 family
`P(q,k;J,U,C) = H ++ C ++ reverse(H)`, `H = B34 ++ W9^q ++ J ++ U^k`,
with `q>=14`, `k>=100`, 30 primitive charge-zero U3 words, `|J|,|J'| in {3,4}`,
and palindromic coefficient centres of lengths 2..13 (both parities). The candidate endpoint is
`P(q,k+5;J',U',C')` after 120 genuine ordinary decimal steps, with the same B34/W9 exterior and q fixed.

## Lemma 1: exact length ledger

The rooted clock is `(1000)^30`, so the decimal length grows by exactly 30. The source and target template lengths differ by
`30 + 2(|J'|-|J|) + (|C'|-|C|)`.
Consequently every exact endpoint transition must satisfy
`2|J'|+|C'| = 2|J|+|C|`.
The centre length therefore changes by two when the seam length changes by one, and its parity is preserved. For a cross-cell edge `J3 -> J4`, source centre lengths 4..13 map only to target lengths 2..11; the reverse edge maps 2..11 to 4..13. The shared invariant values are `2|J|+|C| = 10..19`.

## Lemma 2: U3 phase-locking across a moving seam

Let `delta=|J'|-|J|` be +1 or -1. The T12 protected-cut theorem supplies a three-coefficient block of the source U3 bulk at
`c = |B34| + 9q + |J| + 165`,
after 55 complete U3 copies. At phase 120 this block is exactly U again, since `U_120=U_0`; the reset-cone bound leaves at least 13 protected coefficients on both sides of this cut. Thus the actual successor has `P_120[c+r]=U[r]` for `r=0,1,2`.

In the target, the same absolute index is `165-delta` coefficients past the start of `U'^(k+5)`. Endpoint equality therefore requires
`U[r] = U'[(r-delta) mod 3]` for all `r=0,1,2`, equivalently
`U' = rotate_left(U, delta mod 3)`.
This is an all-width necessary condition, not a sufficient transition criterion.

## Lemma 3: phase-shifted insertion lifts a moving-seam edge

For each phase t, the cyclic bulk map `F_gamma` commutes with rotation, so
`U'_t = rotate_left(U_t, delta)` whenever `U'_0=rotate_left(U_0,delta)`.
T12's insertion theorem inserts `U_t` into the source orbit at
`c = |B34|+9q+|J|+165` and inserts `U'_t` into the target orbit at
`c' = |B34|+9q+|J'|+165 = c+delta`.
Both cuts lie in the same protected periodic U-run of the common endpoint.
Inserting one whole period at c or inserting its phase-shifted rotation at c+delta
produces the same word. On the reflected high side the cut displacement is -delta;
reversal turns `rotate_left(U,delta)` into the corresponding opposite rotation of
`reverse(U)`, so the mirrored insertion is aligned as well. Therefore, if the exact 120-step edge holds at one admissible
width, inserting one U copy on both sides preserves the edge. The W9 insertion cut is
the same on both sides, so inserting one W9 copy also preserves it. By induction,
an edge verified at `(q,k)=(14,100)` lifts to every independent `q>=14,k>=100`.

This is the missing moving-seam pumping bridge: unlike the stationary T12 theorem, it
handles the one-column offset between the source and target U insertion cuts. It remains
conditional on an exact finite edge; it does not assert that any such edge exists.

## Consequences and exact reduced search space

- If the T* family keeps the same U orientation, no exact 120-step transition can change `|J|` between 3 and 4.
- If U is allowed to change along a moving-seam orbit, its next rotation is uniquely determined by `delta`; no edge can change the underlying oriented three-cycle class. The 30 U words split into 10 oriented rotation classes of 3 words each.
- Before this lemma there are 30x30=900 possible ordered U-to-U' pairs per seam-width direction. The lemma leaves exactly 30 possible pairs for each direction, or 60 across `delta=+1` and `delta=-1`. Centre *values* and actual seam edges remain unsearched.
- A cycle may still alternate `J3 -> J4 -> J3` with U rotating left once and then right once. The lemma does not exclude that cycle.
- A finite cycle in the reduced graph at `(14,100)` would lift edge-by-edge to all q,k and, with the T12 rooted odd-coefficient guard, give an all-time nonpalindromic orbit. The finite graph itself has not been exhausted.

## Independent arithmetic controls

Run `python3 calculation/new_structures/X45/phase_lock.py` from the repository root. The script reads the published `lat_p12m9.txt` root rows and independently computes each source orbit with (i) a fresh-buffer LSD-first digit-array reverse-add engine and (ii) Python arbitrary-precision `n + reverse(n)`. It covers all 30 U words, q in {20,40,80,160}, k=100, and both seam-width directions with even and odd centres: 480 trajectories and 57,600 step-by-step engine comparisons. Every clock equals `(1000)^30`, every checked state is nonpalindromic, the protected U block is correct at every phase, and the predicted rotated target block aligns while the unrotated block does not. The script also checks the phase-shifted insertion identity for all 30 U words and all 120 bulk phases.

These controls validate the concrete arithmetic only. The all-width statements follow from the T12 insertion theorem plus the exact index/rotation argument above, not from sampling. The script does not test a full endpoint return, and no centre-value enumeration or SCC closure decision has been completed.