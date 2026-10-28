# Periodic-lattice absorbing-band certificates and a base-9 Lychrel number

Lean result: `lean/P196/LatticeBand/` (registry entry `LatticeBand`). Main endpoints:

```lean
theorem LatticeBand.Base9.exists_lychrel9  : ∃ n, Agent120.Neutral.Lychrel 9 n
theorem LatticeBand.Base9b.exists_lychrel9 : ∃ n, Agent120.Neutral.Lychrel 9 n
-- #print axioms: [propext, Classical.choice, Quot.sound]
```

`Lychrel` is the unchanged definition of `Drafts/Agent120NeutralBandCalibration/A120Base.lean`.

**Not a decimal result.** Nothing here says anything about base 10 or 196.

## Format

Coefficient words are least significant first. For a block `B`, a period block `W` and a band length `l`,

    tm B W l = B ++ band W l ++ reverse B ,   band W l = first l entries of W W W ...

`W` is *absorbing* if `norm W 0` and `norm W 1` leave the same carry `cs`. Then for `l = |W|(q+1) + ρ`
(`ρ < |W|`) the digit word of `val (tm B W l)` is `Lw ++ (Y^q ++ Rw)` (`digits_tm`), and the pair word is again a
template (`pairs_lattice`, `step_tm`): the new block is `W2 = gen Y d`, the new `B2` comes from the ends,
the band length becomes `l + gm` (`gm ∈ {0,1}` the overflow, so the length never shrinks) and the phase
becomes `(ρ + gm) mod |W|`. `not_isPal_tm` shows the value is not a palindrome.

A cycle of edges `⟨B, W, ρ, B2, W2⟩` is checked by the Boolean `lcycleOK` (sound by `ledgeOK_sound`,
`ledge_step`, `lchain_run`); `lychrel_of_lcycle` gives `Lychrel b (val b (tm B W l))` for every `l ≥ 2|W|` with
`l mod |W| = ρ`.

## Base 9 instance

Data: `calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json` and `cert_b9_rec1.json`
(10 edges each, `|W| = 4`, `|B| = 61`, overflow word `1100011000`).

| file | start phase ρ0 | phases along the cycle | seed band length |
|---|---|---|---|
| `Base9.lean`  | 2 | 2,3,0,0,0,0,1,2,2,2 | 10 |
| `Base9b.lean` | 0 | 0,1,2,2,2,2,3,0,0,0 | 8 |

`cert_ok : lcycleOK 9 cert B0 W0 ρ0 = true` is closed by `decide +kernel` (about 2 s). `cert_wrong_phase` shows the
checker rejects the same data with a wrong start phase. A corrupted digit in `W3` makes `decide` fail
(tested once, not kept in the repository).

## Status

- LEAN-VERIFIED: `exists_lychrel9` (both files).
- COMPUTED (outside Lean): the two certificates were first validated in Python (all 10 edges of each cycle).
- Not claimed: anything for base 10; the family `b ≡ 1 (mod 3)`; novelty beyond the Wikipedia/OEIS A060382 list
  (no literature search was done).

## Search in other bases (COMPUTED, not Lean)

Tool: `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp` (position automaton, state cap 3,000,000), then
`replay_sym.py` (big-integer replay) for each SCC with `m | S` and a palindromic lattice word.

- Controls reproduced: base 9 `g=1100011000` gives `m = 4`, `|B| = 61`; base 13 `g=1010010000` gives `|B| = 75, 55`.
- Bases 5, 6, 7, 8, 11, 12, 14 to 31, all overflow necklaces of length `p ≤ 12`: every SCC that satisfies `m | S` with a
  palindromic lattice is a *neutral* band (all entries `b-1`); these need a centre and the big-integer replay fails at
  step 1. No further absorbing self-mirror lattice was found. A few streams hit the state cap (for example
  base 11, 17, 18, 24, 27: one each; base 20: two).
- Bases 7, 19, 22, 25, `13 ≤ p ≤ 16`: no candidate among decided streams; capped streams: base 7 `p=15 100100100100100`,
  `p=16 1100110011001100`; base 19 `p=15 101001010010100`; base 22 `p=13 1010001010000`, `p=15 100001000010000`;
  base 25 `p=16 1010101010101010`.
- So bases 9 and 13 are the only ones with a certificate of this kind in the covered range; there is no evidence yet for a
  general family `b ≡ 1 (mod 3)`. UNDECIDED.
