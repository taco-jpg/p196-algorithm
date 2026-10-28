# Absorbing-band certificates and a base-13 Lychrel number

Lean result: `lean/P196/AbsorbingBand/` (registry entry `AbsorbingBand`). Main endpoint:

```lean
theorem AbsorbingBand.Base13.exists_lychrel13 : ∃ n, Agent120.Neutral.Lychrel 13 n
-- #print axioms: [propext, Classical.choice, Quot.sound]
```

`Lychrel` is the unchanged definition of `Drafts/Agent120NeutralBandCalibration/A120Base.lean`
("no orbit element, the seed included, is a palindrome"); the three A120 core files are imported, not modified.

**Not a decimal result.** Nothing here says anything about base 10 or 196.

## 1. The format

Coefficient words are least significant first; the pair word of `N` is `d_i + d_{n-1-i}`, and the value of
the pair word is `N + rev N`. For a base `b`, a block `B`, a band value `c` with `c ≤ 2(b-1)` and `c ≠ b-1`, and a
band length `l`, the template is

    ltmpl B c l = B ++ c^l ++ reverse B .

*Absorbing band.* For either incoming carry `e ∈ {0,1}`, the normalization of `c^(m+1)` is
`((c+e) mod b) :: y^m` with outgoing carry `k = [b ≤ c]`, where `y = (c+k) mod b` (`norm_replicate_absorb`).
In the neutral format of A120 the band (`c = b-1`) transmits its carry, so the centre block must cooperate (the flip
condition `e1 ≠ e2`). An absorbing band fixes the carry entering the upper copy of `B`. That is why no centre block
and no flip condition are needed.

*One step* (`digits_ltmpl_unified`, `pairs_dW`, `step_ltmpl`; valid whenever `2 ≤ l + gam`):

- the digits of `val(ltmpl B c l)` are `O = L ++ y^(l+gam-2) ++ R`, where
  - `L = DB ++ [x]`, with `x = (c + e1) mod b`;
  - `DR = norm(rev B, k)`;
  - `gam` is the final carry;
  - `R = y :: DR` if `gam = 0`, and `R = DR ++ [1]` otherwise;
- the next pair word is `ltmpl (zipWith (+) L (rev R)) (2y) (l + gam - 2)`.

So the band value evolves as `c ↦ 2((c + [b ≤ c]) mod b)`. *Non-palindrome* (`not_isPal_ltmpl`): `L ≠ rev R`
implies `O` is not a palindrome. *Trim* (`ltmpl_trim`): trailing copies of the new band value at the top of the
new block move into the band, so `l ↦ l + gam + 2u - 2`.

*Certificate* (`ledgeOK`, `lcycleOK`, `lychrel_of_lcycle`): a nonempty chain of checked edges that closes in
`(B, c)` and satisfies `2·#edges ≤ Σgam + 2Σu` (the band never shrinks around the cycle) gives
`Lychrel b (val b (ltmpl B c l))` for every `l ≥ minL`. `minL` is computed from the cycle, and the proof holds
in every base.

## 2. The base-13 instance

The cycle has 10 edges:

- band values alternate 16, 8;
- the overflow word is `1010010000`, so `Σgam = 3`;
- `u = 1` on every edge, so the band grows by 3 per cycle;
- `|B| = 75` (`Base13`), and a second cycle with `|B| = 55` (`Base13b`);
- `minL = 1`, so `lychrel_template` holds for every `l ≥ 1`.

`Base13N0` proves `Lychrel 13 N0` for a 151-digit seed one step before the template. `Base13Check` checks
several orbit points directly with the repository's `step`/`orbit`, and `Base13Neg` shows that seven corrupted
certificates are rejected.

Independent of the proof, a plain digit-arithmetic replay of both seeds ran for 20,000 steps. The pair word matched
the predicted template at every step, the band grew from 1 to 6001 coefficients, and no palindrome occurred.

How it was found: a search over generalized (lattice) exterior cycles over bases 2–16. Base 13 has no
neutral-band exterior cycle at all, yet it has this absorbing one. A similar candidate in base 9 (band of spatial
period 4, `p = 10`, overflow word `1100011000`) is computed only (3,000-step replay) and not formalized.

Novelty: as far as Wikipedia and OEIS A060382 record, Lychrel existence was known only for bases 11, 17, 20, 26
and powers of two. No literature search beyond that was done.

## 3. Base 10 in this format (computed, no certificate)

Base 10 has four absorbing band loops: `{0}`, `{18}`, `{6,12}` and `{2,4,8,16,14,10}`. A search of decimal
exterior cycles in this format (period ≤ 24, plus a symbolic engine for some denser words) found none that closes.
The decimal orbit of 196 repeatedly locks, for 75–155 steps, into a period-8 exterior with a non-uniform periodic
absorbing lattice (spatial period 20 or 48). These lattices are not palindromic necklaces, so they would need a
time-periodic centre. None exists with lower-half window width ≤ 7 (COMPUTED); wider windows are undecided.
