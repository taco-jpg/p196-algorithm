# Neutral one-band template: transition, calibration and first findings

Agent #120, task `agent120-neutral-band-calibration`. **Working notes (WIP).**
Nothing here is a Lean theorem yet. Section 2 is a written derivation; sections
3 and 4 are exploratory finite computations whose scope is stated exactly. No
claim about 196 or about decimal Lychrel existence is made.

## 1. Setting

Fix a base `b >= 2` and put `n = b - 1` (the *neutral* pair coefficient).
Pair words are mirrored digit sums, least significant first. For an exterior
block `B` (entries in `[0, 2n]`, first entry positive when nonempty), a
symmetric nonempty center `C` (entries in `[0, 2n]`, odd length has even middle)
and a gap `g`, the template word is

```
Q(B, C, g) = B ++ n^g ++ C ++ n^g ++ reverse(B).
```

Its value `P(Q) = sum Q_i b^i` is the reverse-and-add image of every ordinary
base-`b` integer whose pair word is `Q`.

## 2. One-step transition (written derivation)

Normalize from the least significant end, writing `N(W, c) = (D, c')` for the
digit block and final carry of block `W` with incoming carry `c`:

```
N(B, 0) = (D_B, e1),  N(C, e1) = (D_C, e2),  N(reverse B, e2) = (D_R, gamma).
```

A neutral run `n^g` with incoming carry `e` produces `x^g` with `x = n(1-e)` and
passes the carry `e` unchanged (`n + 0 < b`, `n + 1 = b`). Hence the digit word of
`P(Q)` is exactly

```
D_B ++ x^g ++ D_C ++ y^g ++ D_R ++ [1 if gamma = 1],   x = n(1-e1),  y = n(1-e2).
```

Assume **`e1 != e2`** (the band carries differ) and `g >= 2`.

* `gamma = 0`: every block pairs with its mirror block, so the next pair word is
  `Q(B', C', g)` with `B' = D_B + reverse(D_R)` and `C' = D_C + reverse(D_C)`,
  and the band pairs are `x + y = n`.
* `gamma = 1`: the appended leading 1 shifts the reflection by one column. Regroup
  the digit word as `(D_B ++ [x]) ++ x^(g-1) ++ (D_C ++ [y]) ++ y^(g-1) ++ (D_R ++ [1])`.
  The block lengths are symmetric, so the next pair word is `Q(B', C', g - 1)` with
  `B' = (D_B ++ [x]) + (1 :: reverse D_R)` and `C' = (D_C ++ [y]) + (y :: reverse D_C)`.

Trailing `n` coefficients of `B'` and the paired outer `n` coefficients of `C'` are
moved into the band (a re-parameterization of the same word). With `u, v` those
amounts, the new gap is `g - gamma + u + v`.

**Safety.** If `e1 != e2` then `x != y`. In the digit word above, the first band
column (case `gamma = 0`) or the second band column (case `gamma = 1`, needs
`g >= 2`) is mirrored to a column of the other band, so the digit word is not a
palindrome: **every template step is palindrome-free.**

**Autonomous exterior.** Persistence of the neutral band forces `e2 = 1 - e1`, and
`e1` depends only on `B`. Hence `B -> trim(B')` is a map of the exterior alone
(the map `E_b` of `search/../exploration/ext_neutral.py`). Any template cycle
needs a periodic orbit of `E_b`.

**Conditional existence.** If interface states `(B_0,C_0) -> ... -> (B_p,C_p) = (B_0,C_0)`
satisfy the step hypotheses with nonnegative total gap change, then for every
large enough initial gap the value `P(Q(B_0, C_0, g))` has a palindrome-free
reverse-and-add orbit in base `b`. This is the statement targeted for Lean.

## 3. Calibration by literal arithmetic (finite scope)

`search/quotient.py` implements section 2 and compares it with literal integer
reverse-and-add on random template words: **27,518 template-preserving cases in
bases 2-20, 26, 32, zero mismatches**, and every checked successor is
nonpalindromic (`search/quotient_validation.log`). This is a check of the
implementation, not a proof.

`search/cycles.py` follows every canonical start with `|B| <= SB`, `|C| <= SC`
until the template breaks, a follow cap is exceeded, or a state repeats.

| bases | start caps (B,C) | follow caps (B,C) | cycles with gain >= 0 |
|---|---|---|---|
| 2 | (4,5) | (12,14) | 4 cycles, period 4, gain 1 |
| 3 | (4,5) | (12,14) | none |
| 4 | (4,5) | (12,14) | 1 cycle, period 6, gain 1 |
| 5-7, 9-15, 17-31 | (2,3) | (10,12) | none |
| 8, 16, 32 | (2,3) | (10,12) | 1 cycle each, periods 8, 10, 12, gain 1 |

Within these scopes cycles occur exactly in the powers of two. The cycle for
`b = 2^m` starts at `B = (b)`, `C = (b-2, b-2)` and has period `2m + 2`:
exteriors `(b) -> (1,0) -> (2,1) -> (4,3) -> ... -> (2^(m-1), 2^(m-1)-1) -> (b)`,
twice; the first half-cycle has gap change 0 and the second +1. Base 2 has the
extra cycles listed in `search/cycles_base2.json`. Literature: Lychrel numbers
are known to exist in every base `2^m`; this is a rediscovery used as a
calibration, with no novelty claim.

**Decimal (b = 10): no template cycle in the stated scope.** This is not an
all-width exclusion.

## 4. Autonomous exterior map, exploratory

`exploration/ext_neutral_fast.py` follows `E_b` from every canonical exterior of
length at most `maxlen` until the exterior exceeds length 80 or repeats.

| base | maxlen | starts | periodic orbits found |
|---|---|---|---|
| 10 | 4 | 123,462 | none (2,966,176 states visited) |
| 5 | 5 | 52,488 | none |
| 7 | 4 | 26,364 | none |
| 9 | 4 | 78,608 | none |
| 2, 3, 4, 6, 8 | 6/6/6/4/4 | | periodic orbits exist (see `exploration/`) |

Consequence (finite scope, decimal): no neutral one-band template cycle has an
exterior state of length at most 4 while all its exteriors have length at most 80.
Bases 3 and 6 have periodic exteriors without full template cycles in the searched
scope, so a periodic exterior is necessary but not sufficient.

## 5. Planned formal deliverables

1. Base-generic Lean definitions (digits, value, reversal, reverse-and-add, orbit,
   palindrome) and the transition theorem of section 2 for every `b >= 2`.
2. Certificate soundness: a checked interface cycle with nonnegative gain gives a
   base-`b` integer with a palindrome-free orbit.
3. Kernel-checked instances for `b = 2, 4, 8, 16` and an explicit base-2 seed
   (e.g. `22 = 10110_2`). These are not decimal results.
4. Decimal: larger finite-scope searches; an all-width obstruction for `E_10` is
   an open target, not claimed.
