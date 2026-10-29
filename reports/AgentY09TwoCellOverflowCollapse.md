# Exact two-cell bulk-collapse obstruction for a regenerative decimal band

**PAPER PROOF**, all radices `b>=2` and any temporal overflow itinerary with at least one `gamma=1`. This result is deliberately about the *bulk update*, not a rooted decimal certificate; it complements the published base-9 spatial-m4 absorbing certificate and the base-50/146/1286 neutral ones. No claim of a decimal Lychrel number.

## 1. The algebraic bottleneck

A pair-coefficient `p_i` lies in `0..2(b-1)`. On the least-significant side, normalisation uses incoming carry `c_i∈{0,1}`, digit `u_i=(p_i+c_i) mod b`, and outgoing carry `c_{i+1}=floor((p_i+c_i)/b)`. The mirrored, most-significant side uses the same coefficients with its own incoming carry `h_{i+1}`, digit `v_i=(p_i+h_{i+1}) mod b` and descending outgoing carry `h_i=floor((p_i+h_{i+1})/b)`. In a spatially periodic *interior* (far from ends and finite defects) these carry streams must themselves be cyclic. The exact reverse-add bulk pair update with whole-number overflow `gamma∈{0,1}` is

`p'_i = u_i + v_(i-gamma mod m)`.

This is the bulk rule used in the repo's lattice and band-first checkers, with the mirrored partner shifted by `gamma` if the number gains a leading digit. For an exact periodic domain, the rule follows by ordinary schoolbook addition and reflection, without a finite-horizon approximation.

Let `m=2`, `W=(a,d)`, and write the low cyclic incoming carries as `(c0,c1)`. They solve

`c1=floor((a+c0)/b)`, `c0=floor((d+c1)/b)`.

If `W ≠ (b-1,b-1)`, these equations have **exactly one** cyclic solution: the binary carry map of a coefficient `x` is the identity precisely when `x=b-1`, and otherwise is constant. The descending cyclic carries `h0,h1` solve

`h0=floor((a+h1)/b)`, `h1=floor((d+h0)/b)`.

Thus uniqueness forces `(h0,h1)=(c1,c0)`, and the two normalised periodic digit sequences agree:

`(u0,u1)=(a+c0-b*c1, d+c1-b*c0)=(v0,v1)`.

When `gamma=1`, the mirrored pair shift exchanges the only two coordinates:

`p'_0=u0+v1=u0+u1`, `p'_1=u1+v0=u1+u0`.

Hence **every** nonneutral two-cell periodic bulk collapses in one overflow step to the *uniform* two-cell word `(s,s)`, where

`s=u0+u1 = a+d-(b-1)(c0+c1)`.

For the exceptional neutral word `(b-1,b-1)`, the lower cyclic carry may be constantly `0` or `1`, as may the independent upper cyclic carry; each of `u_i` and `v_i` is separately constant in `i`, so their sum is again uniform. This covers all carry choices, with no hidden uniqueness assumption.

Finally, **uniformity is forward-invariant**: for a uniform coefficient word `(s,s)`, both cyclic low and high digit streams are constant in space (even when `s=b-1` and their carries may differ), hence every `gamma=0` or `1` produces a uniform successor. By induction, after the first overflow no primitive spatial-period-2 bulk can ever reappear under the exact stationary-carry bulk map. The argument is independent of time period, physical centre width, and radix.

## 2. What this decides and what it does not

The missing lemma of the attempted *one primitive two-digit absorbing-band repair* route is whether the same spatial-period-2 absorber can survive one necessary growing overflow and reappear as a phase of a finite regenerative temporal cycle. The answer is **NO for every radix and every temporal period**, by the identity above. Any closed growing template consisting of a fixed finite exterior/centre plus one returning **primitive two-cell stationary bulk** requires a positive total overflow; then it contains a `gamma=1` edge, contradicting the primitive recurrence. This specifically redirects the search to (a) primitive spatial periods at least three, (b) neutral bands, or (c) a finite central/junction interface which continuously emits new nonuniform material. A centre or junction that invades the bulk can escape this *bulk-only* theorem; no wider-centre exclusion is implied.

This explains why simply replacing the base-50/146/1286 single neutral coefficient `b-1` by a primitive two-digit absorbing block cannot by itself cure the decimal carry obstruction. It does **not** explain the base-10 p8/m20 or p12/m9 front erosion, which remains the open renewal problem. The base-9 Lean-verified certificate uses `m=4`, so this theorem is compatible with it; the decimal `m=4` periodic *unrooted* bulk `(9,18,9,0) -> (10,8,8,10)` under `gamma=1` proves the length-two threshold is sharp as a local obstruction.

## 3. Independent checks

`python3 calculation/new_structures/agent-Y09/check_two_cell.py` exhaustively compares the two-sided cyclic carry equations across **288,156** cyclic-carry combinations for every two-cell coefficient row in bases `2..60`. It checks collapse at `gamma=1`, carry matching except for the neutral row, and uniform forward invariance. A separate digit-array-to-integer oracle independently constructs 720 canonical integer seeds in bases `3,4,9,10,11,13,26,50,146,1286`, performs ordinary big-integer reverse-and-add, and checks a deep physical pairword window against the cyclic bulk prediction at its *actual* observed whole-number overflow bit. Finally the same bulk checker reproduces the known b9 m4 witness `(1,1,15,15)->(8,2,8,14)` and decimal W25 m4 witness `(9,18,9,0)->(10,8,8,10)` for `gamma=1`, both nonuniform; no claimed all-time decimal seed is hidden in these controls.