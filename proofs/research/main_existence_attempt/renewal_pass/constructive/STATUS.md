# Wider overlap gates, an actual repeated return, and the next boundary obstruction

The construction now has **four infinite spacer families with two genuine delayed returns**, at times 2 and 4. Every ordinary output through time 4 is nonpalindromic. All four fail the proposed next return at time 6, by the exact outer-coefficient mismatch 14 versus 15. No infinite safe recurrence, finite decimal Lychrel witness, or theorem about 196 is proved.

The positive formulas below have direct carry proofs. The exhaustive exclusions within the stated finite core classes use exact affine run arithmetic, including uniformly positive mismatch witnesses. They are not Lean theorems; the sibling `../lean/DelayedOverlapGate.lean` formalizes the earlier six-core gate with outer parameter 1 through 4.

## Notation and conventions

Words are low-to-high decimal pair sums. A canonical word is symmetric, has coefficients 0 through 18 and positive outer coefficient, and has even central coefficient if its length is odd. Every such word is realized by an ordinary positive integer. Write `N(W)` for normalization to ordinary decimal digits, including the terminal carry when present, and

\[
G(W)=N(W)+\operatorname{rev}N(W),\qquad \Phi_s(W)=(1+x^s)W.
\]

For an integer with pair word W, G(W) is the pair word of its reverse-and-add successor. A statement that a step is safe means that the *ordinary output of that step* is nonpalindromic. The coefficient representation of `Phi` is never normalized implicitly.

A genuine two-step repair means

\[
G(Q)\ne\Phi_1(G(A)),\qquad G^2(Q)=\Phi_1(G^2(A)),\qquad Q=\Phi_1(A).
\]

The first inequality is essential: these are departures followed by repairs, not merely consecutive ordinary commutations.

## 1. Twenty central gates instead of six

Put

\[
A=p\,0^r(u,v,v,u)0^r p,\quad Q=\Phi_1(A),\quad j=r+1.
\]

For **every r>=1 and p in {1,2,3,4}**, each of the following 20 core pairs gives a genuine safe two-step repair:

| Group | Parameter domain | Count | Returned component G²(A) |
|---|---|---:|---|
| I | 1<=u<=3, 5<=v<=7, u+v<=8 | 6 | `4p 0^r (4u+1,4v−19,4v−19,4u+1) 0^r 4p` |
| II | 5<=u<=8, v in {5,6}, u+v<=13 | 7 | `4p 0^(r−1) (1,4u−19,4v−18,4v−18,4u−19,1) 0^(r−1) 4p` |
| III | 10<=u<=13, v in {5,6}, u+v<=18 | 7 | `4p 0^(r−1) (2,4u−39,4v−17,4v−17,4u−39,2) 0^(r−1) 4p` |

In all rows `G²(Q)=Phi₁(G²(A))`. The center widens by two columns in groups II and III and consumes one zero on each side. The total component width does not grow in these two steps.

### Carry proof, including the boundaries

The first component output has outer coefficient 2p. Its center is:

* Groups I and II: `(2u,2v,2v,2u)`, still between r zeros.
* Group III: `(1,2u−20,2v+1,2v+1,2u−20,1)`, between r−1 zeros.

The first whole-word defect `delta=G(Q)−Phi₁(G(A))` and the next normalized-digit defect `e=N(G(Q))−N(Phi₁(G(A)))` are:

| Group | delta | e |
|---|---|---|
| I | `x^(j+1)(1−20x+x²)` | `x^(j+1)(1−x²)` |
| II | `x^j(1−19x−18x²−19x³+x⁴)` | `x^j(1+x−x³−x⁴)` |
| III | `x^(j+1)(1−20x+x²)` | `x^(j+1)(1−x²)` |

These follow by normalizing the displayed central columns. For completeness, the relevant consecutive digits in `N(G(A))` are:

| Group | Position of first displayed digit | Digits |
|---|---:|---|
| I | j | `(2u, 2v−10, 2v−9, 2u+1)` |
| II | j | `(2u−10, 2v−9, 2v−9, 2u−9, 1)` |
| III | j−1 | `(1, 2u−20, 2v−9, 2v−8, 2u−19, 1)` |

Group II's last `1` is its carry into the next zero column. Group III's surrounding `1` columns already came from the first normalization. Every other central-adjacent column is zero, apart from the stated exterior.

Adjacent sums in these normalized digit words are at most 9. The potentially largest sums are `2(u+v)−8` in I, `2(u+v)−18` in II, and `2(u+v)−27` in III; their stated domains bound these by 8, 8, and 9. All remaining sums have the same immediate digit bounds. At r=1 in III, the outer coefficient 2p and the adjacent 1 sum to at most 9. Thus there is **no extra carry** in `Phi₁(N(G(A)))`, including the shortest allowed boundary. Consequently

\[
G(\Phi_1(G(A)))=\Phi_1(G^2(A)).
\]

The displayed e is antisymmetric under reversal in the old whole-word width. Neither second normalization has a terminal carry, since 2p<=8 and any incoming carry is at most 1. Hence e cancels with its reversal, proving the return. Pairing the digit rows gives exactly the three returned-component rows in the first table.

Safety also follows from the columns. Initially Q has central coefficient 2v>=10 and outer coefficient p!=11. In `G(Q)`, group I has a column `2(u+v)+1>=13`; II has `2u+1>=11`; III has `2(u+v)−18>=12`. Their outer coefficient is 2p!=11. The exact pair-word palindrome criterion therefore excludes a palindrome on both ordinary outputs. All words and returned overlaps remain canonical.

## 2. A general overflow transport law

Let two equal-width coefficient words have normalized digit difference e in their old L columns, with the same terminal carry h in {0,1}. Suppose

\[
\operatorname{rev}_{L-1}e=-e.
\]

The equal appended carry contributes no difference. Reflection in the new width gives

\[
\operatorname{rev}_{L-1+h}e=x^h\operatorname{rev}_{L-1}e=-x^h e,
\]

so their paired-output difference is exactly

\[
\boxed{(1-x^h)e.}
\]

With h=0 the defect cancels. With h=1 it becomes `(1−x)e`, which is nonzero whenever e is nonzero. This is an equality of integer polynomials; it makes no assumptions about the length of a future orbit.

For **p=5,...,9, r>=2**, all twenty central motifs above have the same first delta and digit defect e, but the common second terminal carry is 1. The independent-overlap normalization still has no additional adjacent-digit carry. Therefore

\[
G^2(Q)-\Phi_1(G^2(A))=(1-x)e\ne0.
\]

For groups I and III the central defect becomes `(1,−1,−1,1)`; for II it becomes `(1,0,−1,−1,0,1)`. This proves a local reason the same repair does not survive that overflow phase.

The restriction r>=2 matters. For example `(p,r,u,v)=(9,1,10,5)` has first component clock 0 but first whole clock 1: the shortest overlap lets a carry reach the adjacent outer 9. This counterexample is retained in `gate_formula_controls.json`; the formula is not asserted there. The complete four-column classification below separately handles every small boundary.

## 3. Four actual two-gate handoffs

The returned domain is wider than the original six-core family. In particular, original `(u,v)=(1,6)` returns with `(p,u,v)=(4,5,5)`, which is group II of the new gate. Thus the earlier `return_not_in_domain` result for the *original* six cores does not prohibit this handoff.

For the following starting words with **p=1**, the exact overlap relation fails at times 1 and 3 and holds at times 2 and 4. All four ordinary outputs are nonpalindromic:

| Initial (u,v) | Valid r | Component core at time 2 | Component at time 4 |
|---|---|---|---|
| (1,6) | r>=1 | `(5,5,5,5)`, with r zeros each side | `16 0^(r−1) (1,1,2,2,1,1) 0^(r−1)16` |
| (5,6) | r>=2 | `(1,1,6,6,1,1)`, with r−1 zeros | `16 0^(r−1) (4,5,5,5,5,4) 0^(r−1)16` |
| (6,6) | r>=2 | `(1,5,6,6,5,1)`, with r−1 zeros | `16 0^(r−1) (5,1,6,6,1,5) 0^(r−1)16` |
| (10,6) | r>=2 | `(2,1,7,7,1,2)`, with r−1 zeros | `16 0^(r−1) (8,5,9,9,5,8) 0^(r−1)16` |

In every row the whole word at time 4 is `Phi₁` of the displayed component.

The first row is direct composition of groups I and II. For the other rows, write the time-2 component as `4 0^R C 0^R 4`, with R>=1. Its next output doubles its digits. The following table gives all local carry data for the next normalization:

| C | Normalized digits of 2C | Their paired sum | Digit defect in the seven-column overlap center |
|---|---|---|---|
| `(1,1,6,6,1,1)` | `(2,2,2,3,3,2)` | `(4,5,5,5,5,4)` | `(0,0,1,0,−1,0,0)` |
| `(1,5,6,6,5,1)` | `(2,0,3,3,1,3)` | `(5,1,6,6,1,5)` | `(0,1,1,0,−1,−1,0)` |
| `(2,1,7,7,1,2)` | `(4,2,4,5,3,4)` | `(8,5,9,9,5,8)` | `(0,0,1,0,−1,0,0)` |

Each adjacent digit sum in the normalized middle column is at most 9. The outer normalized digits are 8, separated from the displayed core by R>=1 zeros. The digit defects are antisymmetric and the terminal carry is 0, proving all three repairs with their full boundaries. The relevant whole pair words contain coefficients at least 10 at each step; their outer coefficients are 4 and 8, so the two further ordinary outputs are safe.

The r=1 exclusions in the last three rows are real. At time 4 their defect from `Phi₁(component)` is exactly

`(1,−20,1,0,0,0,1,−20,1)`.

No such boundary counterexample is omitted or absorbed into the theorem.

## 4. The proposed third gate fails for all four families

Let B be any of the four time-4 components above. All have outer coefficient 16 and satisfy `whole=Phi₁(B)`. After two more updates:

\[
[G^2(B)]_0=14,\qquad [G^2(\Phi_1(B))]_0=15.
\]

Both words have undergone the same clock sequence `(1,0)`, so the only possible overlap shift is still 1. This outer mismatch proves

\[
G^6(Q)\ne\Phi_1(G^6(A)).
\]

Here is a direct boundary proof. If the spacer `R=r−1` is at least 1, the time-4 component begins and ends `(16,0,...)`. Its next paired word begins and ends `(7,7,...)`. The time-4 whole word begins and ends `(16,16,...)`, so its next paired word begins and ends `(7,14,...)`. Interior carries cannot change these entries: the nearest zero in the component resets the carry, whereas the repeated 16 in the whole word forces it. At the following normalization the component's penultimate 7 cannot produce a carry even if it receives one; the whole word's penultimate 14 must produce a carry. The final digits are therefore 7 and 8, while both low digits are 7. Their outer pair sums are 14 and 15.

The sole allowed R=0 case is initial `(u,v,r)=(1,6,1)`. Its time-4 component is `(16,1,1,2,2,1,1,16)`. The next component and whole boundaries are `(7,8,...)` and `(7,15,...)`. The same reset/force argument again gives 14 versus 15. Thus the shortest boundary is covered directly.

A useful correction to an exploratory guess is retained in `ATTEMPTS.json`: original `(1,6)` actually preserves the overlap at time 5 (ordinary commutation through overflow), then loses it at time 6. The other three families already depart at time 5. The result excludes the proposed third two-step reuse, not all possible later returns.

The original `(1,6)` branch is known to terminate at time 11 for r>=5 by the independent all-r tail certificates in `../tails/`. Repeated finite gates alone do not establish infinite safety.

## 5. Exhaustive classes and exact computational scope

`padded_core_classification.py` classifies all 2,430 triples

`p=1..18, u=1..18, v=0..9, u+v<=18`

for exactly two updates, with all integers r>=1 covered. Its affine domain is `r=5+k`, k>=0. All r=1,2,3,4 are checked independently by literal integer reverse-and-add. The output table contains every case, clocks, forced shifts, return flags, and safety flags. **The only genuine two-step delayed returns in this entire class are precisely the 80 gates in section 1.** There are 111 small-spacer changes to the detailed signatures, all at r=1; none changes membership in that genuine-return classification.

`return_composition.py` takes the exact 80 gate images and classifies a second two-step repair through time 4. It uses `r=9+k` and checks r=1..8 separately. The only genuine second repairs are exactly the four rows in section 3, with their stated minima. It retains 12 detailed small-spacer exceptions, all at r=1; three remove the invalid shortest cases of the last three positive rows.

`third_gate_check.py` checks the four valid double-return families through time 6, with affine domain `r=13+k` and all smaller valid spacers independently checked. The direct outer proof in section 4 is stronger and simpler than its negative witnesses.

**Uniform negative verification.** Structural inequality of affine run lists was identified during root review as insufficient: two different affine lengths can coincide at a special parameter. The three pre-correction source versions are retained in `superseded_pre_uniform/`. The current `closed_overlap` routine subtracts complete run words using coefficientwise-certified boundary comparisons. Every negative conclusion exhibits a nonzero coefficient on a run whose length is strictly positive for all k>=0. A comparison that cannot be certified is an error. No new parameter splits were required on replay. This correction leaves the positive identities and case table unchanged.

| Exact replay | Comparisons | Uniform negative witnesses | Literal parameter instances |
|---|---:|---:|---:|
| Four-column class | 4,860 | 3,099 | 14,580 |
| Second-gate image class | 320 | 194 | 800 |
| Third-gate check | 24 | 15 | 53 |

All 5,204 comparison records are retained in the three `*_comparisons.json.gz` archives (16,689 compressed bytes total). `capture_witnesses.py` regenerates the complete streams without modifying the audited classifiers, resets their affine bases to 5, 9, and 13, and verifies every uncompressed hash against its corresponding result JSON. `capture_witnesses.json` records both archive and content hashes. Witness stream hashes are also recorded in the corresponding classifier JSON files. The complete main CSV has SHA-256 `ead408bca8caa806bad6cf08eb3555c6d4f6d4ed2ebf5789a201c754c1f86b5d`.

Independent literal formula controls in `gate_formula_controls.py` cover 2,800 first-gate cases, 3,400 overflow-transport cases, and 137 double-return cases. Their spacer set is 1 through 32, 64, 127, 256, restricted as stated by each formula. These controls support the written all-r carry proofs; their finite extent is explicit.

A separate bounded experiment, `overflow_core_probe.py`, exhausts 43,788 inputs: p representatives 5 and 10, spacer 8, symmetric even core lengths 2,4,6,8, half coefficients 0..18, positive first coefficient, last half coefficient <=9, and every adjacent sum <=18. It finds no genuine two-step return through clock `(0,1)` or `(1,0)`. The complete deterministic outcome stream is retained compressed in `overflow_core_probe.json` (889 compressed bytes), along with all configuration, counts, and checksum. This is **not** an all-core theorem and does not exclude longer cores or later repair times.

The initially unsuccessful affine base `r=3+k`, the corrected uniform-negative proof obligation, and the false time-5 subclaim are preserved in `ATTEMPTS.json` and the superseded-source directory. No substantive counterevidence has been deleted.

## Reproduction

From the project root, run each command separately:

```
python main_existence_attempt/renewal_pass/constructive/padded_core_classification.py
python main_existence_attempt/renewal_pass/constructive/return_composition.py
python main_existence_attempt/renewal_pass/constructive/third_gate_check.py
python main_existence_attempt/renewal_pass/constructive/gate_formula_controls.py
python main_existence_attempt/renewal_pass/constructive/overflow_core_probe.py
python main_existence_attempt/renewal_pass/constructive/capture_witnesses.py
```

Each writes its complete compact JSON result beside its source. The main class additionally writes `padded_core_cases.csv`. Existing completed logs and root replay logs are retained separately.

## Remaining recurrence obligation

A successful construction must carry the returned exterior `16` and the generated boundary defect into a new safe parameterized family, and prove an exact later return with repeatable parameters. The present two-gate family supplies a real finite handoff and an exact next obstruction, but no map that resets this exterior or consumes/replenishes context indefinitely. Neither the finite class exclusions nor the bounded overflow probe resolves that obligation.
