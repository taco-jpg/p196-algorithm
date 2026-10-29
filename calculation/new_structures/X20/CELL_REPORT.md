# CELL_REPORT — rooted p12/m9 U6 240-step short-junction cell

**Status: EXHAUSTED-NONE**  
**Label: COMPUTED**  
**Scope:** only the fixed U6 motif `U=(3,3,9,15,15,9)`, phase-0 rooted `B34/W9`, junction lengths `|J|=3,4`, and 240-step macro `P(q,k;J,C) -> P(q,k+5;J,C)`. This is not a proof that decimal Lychrel numbers do not exist.

## Exact statement

For every `q>=24`, `k>=100`, every ordered junction word `J` of length 3 or 4 over coefficients `0..18`, and every physically realizable palindromic coefficient centre `C` (either parity, with an even middle coefficient when `|C|` is odd), the rooted family

`P(q,k;J,C) = H C reverse(H)`, `H=B0 W0^q J U^k`,

with the published phase-0 p12/m9 exterior and `U=(3,3,9,15,15,9)`, **does not** return after 240 genuine decimal reverse-and-add steps to `P(q,k+5;J,C)`. At the macro endpoint, the rooted `B0 W0^q` prefix is never restored. The result is specific to this U6 motif and `|J|=3,4`; other U6 words, longer junctions, moving seams, and the U3 target remain open.

## All-width reduction

The actual rooted overflow clock is `gamma_t=1` iff `t mod 4=0`, so the 240-step clock is exactly `(1000)^60`. The cyclic two-ended carry map sends `U` back to itself after 240 phases, with a half-rotation at phase 120. Every phase row has sum 54 and no adjacent 9s. Since `T_x(c)=floor((x+c)/10)` forgets the incoming carry at every `x!=9`, the exact 240-phase boundary-cone losses for the six spatial rotations are `(299,240)`, `(300,240)`, `(300,239)`, `(299,240)`, `(300,240)`, `(300,239)`. Hence the maximum junction-side loss is 300 coefficients and the maximum centre-side loss is 240.

Place the U6 insertion/cut 330 coefficients into the band, after 55 U6 copies. For `k>=100`, its distances to the junction and centre are at least 330 and 270, leaving 30 pure coefficients beyond each cone. This makes the entire prefix through that cut independent of every admissible centre `C` throughout all 240 phases. The rooted W9 prefix loses exactly 181 coefficients in 240 phases. At `q=24`, its initial length is 250 and its protected endpoint is 69; the W insertion cut at index 52 leaves 17 coefficients, enough for one full W9 period and a reset guard. The W and U6 insertions commute with every true decimal step, and both bands return to their initial phase at t=240. Therefore, for each fixed `J,C`, the 240-step return predicate is invariant under `q->q+1` and `k->k+1`, reducing every `q>=24,k>=100` return question to the single width `(q,k)=(24,100)`. The rooted B prefix has an odd coefficient at every phase, giving a non-palindrome guard for any hypothetical return.

## Complete finite computation

At `(q,k)=(24,100)`, the exact low-prefix engine tracks `B0 W0^24 J U^55` (length `|B|+9q+|J|+330`) plus one six-coefficient U6 lookahead. Each phase computes the low carry from the LSD, then the high carry backward from the first non-9 in the lookahead. That high carry is exact because the coefficient is non-9; all prefix outputs are therefore exact. The six coefficients at the end of the tracked prefix are asserted to remain the next U6 bulk row, and the rooted overflow clock and odd-coefficient guard are asserted at every phase.

The exhaustive domain is exactly

- `19^3 = 6,859` junctions of length 3;
- `19^4 = 130,321` junctions of length 4;
- total `137,180` junction words, with **no** mod-11, SAT, MDD, or other pruning.

Assertion-enabled compiled scan result:

- W9-prefix restorations at t=240: **0 / 137,180**;
- complete-prefix returns: **0 / 137,180**;
- first mismatch indices: **202 through 213** (LSD-first; the W9 endpoint is index 250);
- mismatch distance from the W9 endpoint: 37–48 coefficients for every junction.

Mismatch-distance histogram (distance -> junction count): `37:2, 38:54, 39:64, 40:541, 41:366, 42:5051, 43:7404, 45:63817, 46:54998, 47:3601, 48:1282`. Counts sum to 137,180. Since every junction loses the rooted W9 prefix at the reference width and that mismatch is invariant under the two paired insertions, no candidate in the stated all-width cell can return.

## Independent controls and reproduction

`u6_240.py` compares the local prefix recurrence against full arbitrary-precision `n + reverse(n)` at every one of 240 phases, with a separately coded LSD digit-array oracle. Controls cover `q=20,24,40,80,160` and scaled `k=100,100,160,320,640`; paired W/U6 insertions are also checked at q=24,40,80,160 and both centre parities. All controls pass. The repository's `parametric_verify_r30.py` is explicitly U3-only, so it cannot validate this U6 lane; the independent full-integer and digit-array engines are used instead.

Reproduce from the repository root:

```sh
python3 calculation/new_structures/X20/u6_240.py
g++ -O3 -std=c++17 calculation/new_structures/X20/scan_u6.cpp -o /tmp/scan_u6
/tmp/scan_u6 24
```

**Redirect:** do not spend more search on this exact U6/short-J cell; investigate other U6 bulk cycles, `|J|>=5`, or genuinely moving/phase-changing seams. No global no-go or Lychrel certificate is claimed.
