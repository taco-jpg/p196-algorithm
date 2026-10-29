# X24 mixed-U6 phase-1 cell report

**Status: EXHAUSTED-NONE. Label: COMPUTED + PAPER PROOF; not Lean-verified.** Scope is one phase of the known 24-cycle: `U6_0=(7,7,9,11,11,9)` maps at phase 0 to `U6_1=(17,14,17,1,4,1)`. This is not an exclusion of every possible U6 cycle or every phase.

## Exact finite search

Reference width: `(q,k)=(24,100)`. The C++ local-collar engine enumerates every junction word with `|J|=3` or `4`:

- `J` count: `19^3 + 19^4 = 137,180`;
- U6 row: fixed `U6_1=(17,14,17,1,4,1)`;
- centre: not enumerated, because the proved U6 reset/cone bound isolates the boundary from every legal finite C.

For centre lengths 2..13, there are `546,254,940` legal palindromic coefficient centres, so the raw `(J,C)` product has `74,935,252,669,200` tuples. Both even and odd centres are included by centre independence; no odd-only modular gate is used.

## Exact 240-step semantics and all-width lift

The phase-1 U6 row returns after 240 steps, with 60 genuine overflows. The exact U6 cone over the 240-step epoch is `(left,right)=(299,239)`. At `k>=100`, 600 U6 coefficients separate J from C, so the centre cannot influence the tested collar. A 320-coefficient collar leaves 81 cells beyond the right cone.

The W9 loss over 240 steps is at most 181. At q=24, the W insertion cut after two W copies is 198 cells from the seam, leaving guard 17; inserting one W row there commutes with the 240-step dynamics. Inserting one U6 row after 55 copies uses a cut 330 cells from J, leaving guard 31 beyond the left cone. `verify_u6_phase1.py` checks both insertion identities through every `t=0..240` at `(q,k)=(24,100)` and `(40,160)`. These exact reset/insertion bounds lift the endpoint result to all `q>=24,k>=100` for this U6 phase row.

The local-collar transition is cross-checked against full pairword normalization, a fresh-buffer digit-array reverse-add, and Python arbitrary-precision integer reverse-add for 240 steps at `(q,k)=(40,100),(80,160),(160,320)`. The U6 24-cycle and 240-step return are checked directly.

## Exhaustive result

14 contiguous chunks cover `[0,137,180)` with no gaps or overlaps:

- tested: `137,180` junctions;
- clock failures: `0`;
- rooted-B endpoint mismatches: `0`;
- W9 endpoint failures: `137,180`;
- W9 endpoint restorations: `0`.

Thus the physical 240-step epoch-edge set is empty for this phase-1 U6 row and `|J|=3..4`; no fixed point or finite cycle can exist in this cell, regardless of changes to J, C, or the next U6 phase. This is a cell-local exclusion only, not a global result for the Lychrel problem. No ALERT is warranted because no candidate restores the required prefix.

## Reproduction

```sh
g++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/new_structures/X24/u6_strict_w9_cell_local.cpp -o /tmp/x24-u6
for s in $(seq 0 10000 130000); do
  /tmp/x24-u6 --start "$s" --limit 10000
done
python3 calculation/new_structures/X24/verify_u6_phase1.py
```

**Redirect:** this specific phase-1 U6 row is dead for `|J|=3..4`; next search a distinct mixed-U6 orbit/phase or the unresolved moving/growing seams. Do not rerun this exact cell.
