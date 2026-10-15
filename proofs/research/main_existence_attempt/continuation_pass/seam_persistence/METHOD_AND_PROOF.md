# Adaptive seam certificates and an exact neutral-band return map

No persistent decimal safety invariant or finite Lychrel witness is established here.
The new results are an intrinsic characterization of every attainable seam mask,
exact typed transport and birth laws, an all-width annihilation family, and a
variable-clock neutral-band map whose cycles would be genuine persistent safety
certificates. Its complete reachable graph from a specified small-interface
family has no cycle; this last exclusion does not cover arbitrary interfaces.

All coefficient words below are low-to-high. A canonical whole pair word is
symmetric, has entries in `0,...,18`, positive outside entries, and an even
central entry when its width is odd. Write `G(q)` for the pair word of the
ordinary output obtained by normalizing `q`. Write `a_i` for its incoming
forward carry at column `i`, so `a_0=0`, and write `beta_(i+1)` for the incoming
carry from the other direction at that column. Both streams start with zero
outside the whole word. The actual final carry is `gamma`.

## 1. Partitions do not enlarge the set of active columns

For an arbitrary finite coefficient word, call a maximal run of coefficient 9
**active** if its immediately preceding coefficient exists and is at least 10.
If its positions are `[u,v)`, let its length be `ell=v-u`.

**Theorem 1.** A nonempty consecutive partition with nonzero seam mask exists
if and only if the word contains an adjacent factor `(h,9)` with `h>=10`.
The singleton partition gives the largest possible mask, namely

`Kmax_i = 1` exactly when `q_i=9` and its nearest preceding non-9 coefficient
is at least 10. It is zero at every other column.

Every attainable mask is obtained by choosing, independently for each active
maximal 9-run, an empty set or a terminal suffix of that run. Therefore, if
the active run lengths are `ell_1,...,ell_s`, then

`number of distinct masks = product_j(ell_j+1)`,

and the attainable masses are exactly all integers from 0 through
`ell_1+...+ell_s`.

**Proof.** A coefficient at most 8 resets either incoming carry to 0; one at
least 10 resets either incoming carry to 1; coefficient 9 preserves the bit.
Consequently the actual carry entering a maximal 9-run is 1 exactly in the
stated active case. Within such a run, the isolated carry agrees with the
actual one until the first partition cut in the run. That cut resets the
isolated carry to 0, and every later 9 in the run has actual carry 1 and isolated
carry 0, including after further cuts. The next non-9 coefficient coalesces
the two streams. Thus the mask on the run is exactly a terminal suffix.

Conversely, cut at the initial column of each desired nonempty suffix, and
make no additional cuts inside the other active runs. These choices are
independent because every intervening non-9 resets the two carry streams
together. Cutting before every column gives every active run in full. The
formula for the number of masks follows from independent suffix lengths;
the sums of integer intervals `[0,ell_j]` fill `[0,sum ell_j]`. ∎

For a symmetric whole word, factors `H9` and `9H` are equivalent by reflection.
Combined with the prior active-seam safety theorem, Theorem 1 eliminates all
partition search: adaptive choice of a partition certifies the next output
exactly when at least one `H9` adjacency exists. Adaptation cannot recover a
certificate from a word with no such adjacency.

This last statement concerns this sufficient seam certificate, not safety
itself. Many safe words have no 9 at all.

## 2. Defect mass and density can disappear at once

For every `r>=1`, put

`Q_r = (10), 9^(2r), (10)`.

This is a canonical whole pair word. All carries after the first column are 1,
so the maximal mask has mass `2r` and density `2r/(2r+2)`. Its normalized
digits and next pair word are exactly

`N(Q_r) = 0^(2r+1),1,1`,

`G(Q_r) = 1,1,0^(2r-1),1,1`.

The latter has every coefficient at most 9. Hence every partition has zero
seam mask there, and the next ordinary output is a palindrome. A concrete
realizing seed and its first two outputs are

`n_r = 10^(2r+2) - 10^(r+1) + 1`,

`T(n_r) = 11*10^(2r+1)`,

`T^2(n_r) = 11*(10^(2r+1)+1)`.

Indeed, the decimal word of `n_r` is `9^(r+1) 0^r 1` in high-to-low order,
which has pair word `Q_r`; adding its reversal proves the formulas. For
`r=1`, this is `9901 -> 11000 -> 11011`.

Thus no positive lower bound on seam mass or seam density alone can provide
persistence, even when partitions may change arbitrarily. The obstruction
holds at arbitrarily large widths, masses, and densities approaching 1.

The formal branch has independently compiled
[`IntrinsicSeam.lean`](../lean/IntrinsicSeam.lean) and
[`SeamAnnihilation.lean`](../lean/SeamAnnihilation.lean). The formal results
include intrinsic `H9` activity, exact singleton mass for the arbitrary-run
family, its exact next word, zero defect for every next partition, even-run
admissibility, existence of ordinary realizations, first-palindrome time 2,
and exact first output `11*10^(k+1)`. The displayed closed formula for `n_r`
and the exact numeric second-output formula are written arguments here;
they are not claimed as separately formalized Lean statements. See the
formal branch's [`STATUS.md`](../lean/STATUS.md) for the fresh-build audit.

## 3. Exact typed transport of a mixed 9-run

Consider an internal maximal factor

`h, 9^ell, l`, with `h>=10`, `l<=8`, and `ell>=1`.

Every forward incoming carry in its 9-run is 1, and every backward incoming
carry is 0. Call this a **mixed** run. Let `a` be the forward incoming carry
at the left flank `h`, and let `b` be the backward incoming carry at the
right flank `l`.

**No overflow.** The corresponding output factor, at the same positions,
is exactly

`(2h-20+a), 9^ell, (2l+1+b)`.                       (1)

In particular, a new active seam is guaranteed if `h>=15`, or `l>=5`, or
`l=4,b=1`. A new 9 can extend the run across the left flank precisely when
`h=14,a=1`; it can extend across the right flank precisely when `l=4,b=0`.
If neither flank is 9, these local formulas determine whether this run
remains mixed, becomes bracketed by two low coefficients, or becomes bracketed by two
highs. If a flank becomes 9, the full new maximal run can extend into the
surrounding word; that extension must be inspected before assigning its type.

**Overflow.** The corresponding output factor, starting at the first old 9
column, is exactly

`(h-10), 9^(ell-1), (l+10)`.                      (2)

It is independent of the two exterior carry bits. Thus for `ell>=2` the
run remains mixed with reversed orientation and loses one neutral column.
Since the whole output pair word is symmetric, the high-right adjacency
has a reflected `H9` adjacency and certifies the next update's safety.
For `ell=1`, formula (2) is only a low-high adjacent pair and supplies no 9
certificate by itself.

**Proof.** Let the normalized digit at column `i` be
`r_i=q_i+a_i-10a_(i+1)`, and let its reversed-direction version be
`u_i=q_i+beta_(i+1)-10beta_i`.
Without overflow, `G(q)_i=r_i+u_i`. On the 9-run this is `0+9=9`.
At its left flank the backward incoming carry is 0, giving
`(h-10+a)+(h-10)`; at its right flank the forward incoming carry is 1,
giving `(l+1)+(l+b)`. This proves (1).
With overflow, the interior formula is `G(q)_i=r_i+u_(i-1)`.
At the left edge it gives `0+(h-10)`; in the surviving run it gives `0+9`;
at the right edge it gives `(l+1)+9=l+10`. This proves (2). ∎

Two unrestricted failure families prevent overreading these transport laws.
For every `ell>=1`,

`(1),9^ell,(10),9^ell,(1)`

maps without overflow to

`(3),9^ell,(0),9^ell,(3)`,

which has all coefficients at most 9. Thus even an arbitrarily long mixed
run can lose every active seam in one update.

Likewise,

`(8),9^ell,(18),9^ell,(8)`

maps first to `(17),9^ell,(16),9^ell,(17)`, which remains active, and then to

`(8,8),0^(ell-1),(7,7),0^(ell-1),(8,8)`,

which has all coefficients at most 9. This example satisfies a strong
one-step transport guard, but its 9-runs become high-high and annihilate on
the following overflow. These are exact all-length identities.

## 4. Birth laws include old 4 and old 14 columns

On a no-overflow step, at every old column `i`,

`G(q)_i=9  iff  q_i in {4,9,14} and a_i != beta_(i+1)`.       (3)

For `q_i!=9`, both outgoing carries at that coefficient equal
`H_i=[q_i>=10]`, so

`G(q)_i=2q_i+a_i+beta_(i+1)-20H_i`.

Setting this equal to 9 forces incoming sum 1 and `q_i=4` or 14.
For `q_i=9`, its two outgoing carries are its respective incoming carries,
and the value is `18-9(a_i+beta_(i+1))`; it equals 9 exactly when the bits
differ. This proves (3).

On an overflow step, if the two adjacent old coefficients `q_(i-1),q_i`
are both different from 9, set `f(z)=z-9*[z>=10]`. Then

`G(q)_i=f(q_(i-1))+f(q_i)`.                         (4)

Indeed, their reset carries determine the shared incoming bits, and these
cancel in `r_i+u_(i-1)`. This is independent of more distant coefficients.
In particular an old non-9 triple can create a new `H9` adjacency when its
two successive `f`-sums are at least 10 and exactly 9, respectively.

There is therefore no conserved population of old seam columns: active
9s can annihilate, inactive 9s can activate, and new 9s can be born at 4/14
columns or between old non-9 coefficients. A useful persistence induction
must track these types and births rather than just choose new partitions.

## 5. A gap-independent neutral-band quotient with free clocks

Let

`Q(B,H,g) = B,9^g,H,9^g,reverse(B)`, with `g>=2`.

Here `H` is a nonempty symmetric coefficient word with even central entry
when odd; `B` may be empty, but otherwise has positive first coefficient.
All entries are in 0,...,18. Trim the representation so that the last entry
of `B`, if present, and the outside entries of `H` are not 9. In particular
the whole word is canonical even when `B` is empty.

Normalize `B` from carry 0, obtaining its original-width digits `D_B` and
outgoing bit `e`. Normalize `H` from carry `e`, obtaining `D_H` and bit `h`.
Require the mixed-band condition

`h=1-e`.                                              (5)

Normalize `reverse(B)` from carry `h`, obtaining `D_R` and whole final
carry `gamma`. When `B` is empty, this normalization has empty digits and
returns its input carry. Put `x=9(1-e)`, `y=9e`, so `x+y=9`.

The actual output digits, including an optional terminal carry, are

`D_B, x^g, D_H, y^g, D_R, [gamma if gamma=1]`.         (6)

All these blocks and bits are independent of `g`, because a 9 transmits its
incoming carry unchanged. Pairing (6) gives the following exact formulas.

If `gamma=0`, define

`B_raw = D_B + reverse(D_R)`,

`H_raw = D_H + reverse(D_H)`.

If `gamma=1`, define

`B_raw = (D_B appended x) + (1 prepended reverse(D_R))`,

`H_raw = pair(D_H appended y)`.

Every plus sign here is coefficientwise between equal-width lists. Then

`G(Q(B,H,g)) = B_raw,9^(g-gamma),H_raw,9^(g-gamma),reverse(B_raw)`.  (7)

For `gamma=1`, the first `|B|+1` low digits in (6) are `D_B,x`, and the
corresponding reversed high digits are `1,reverse(D_R)`. The central
`|H|+1` digits are `D_H,y`; pairing them gives `H_raw`. Every remaining
neutral position pairs `x` with `y`. This proves the overflowing case;
the no-overflow case pairs the aligned blocks directly. Thus(7) is an
all-gap identity, not an inference from testing a few large gaps.

If `H_raw` consists entirely of 9s, the two bands merge and condition (5)
cannot be represented by a remaining non-9 center. Otherwise strip `u`
trailing 9s from `B_raw` and `v` outer 9-pairs from `H_raw`, obtaining
`B',H'`. Formula (7) becomes

`G(Q(B,H,g)) = Q(B',H',g+delta)`,

`delta=u+v-gamma`.                                   (8)

The next mixed condition is checked using actual normalization of `B',H'`.
This transition does not prescribe an overflow clock; it computes the clock
from the entire current finite interface. Neither symmetric `B` nor positive
outside entries of `H` are assumed. In particular it does not misuse the
positive-canonical-component collision theorem on padded zero middles.

## 6. Why a quotient cycle would be a persistent certificate

Writing `b=|B|`, `m=|H|` and similarly for the next state, actual width gives

`2b'+m'+2delta = 2b+m+gamma`.                         (9)

Suppose a nonempty finite cycle of valid mixed quotient states is found,
with gap shifts `delta_j` and actual overflow bits `gamma_j`. Summing (9),

`2*sum delta_j = sum gamma_j`.                       (10)

The right side is strictly positive. Otherwise all its updates have no
overflow, and the positive outside pair coefficient at least doubles at
every step; it cannot return to itself. If a cycle state has empty `B`,
its low outside coefficient is 9 and mixed condition (5) forces overflow
directly, so this case creates no exception. Consequently

`sum delta_j >= 1`.

Choose the initial `g` so that `g+sum_(j<t)delta_j>=2` for every prefix of
the cycle. Formula (8) then follows every edge exactly. On completing the
cycle the gap has grown by at least 1, so the same lower bounds continue
to hold on every repetition. Induction gives an actual infinite canonical
orbit with a mixed 9-band at every time. Each state has an active seam and
therefore certifies its next ordinary output as nonpalindromic. Since its
pair word contains 9, its starting ordinary realization is nonpalindromic
as well. A genuine cycle would therefore prove finite decimal Lychrel
existence, including a concrete parameter threshold and ordinary seed.

This is a valid conditional construction method, not an instantiated proof.
No cycle has been found in the finite domain below.

## 7. Complete finite exclusion for a stated initial interface family

`neutral_quotient.py` starts with every mixed state having `|B|=1` or 2,
positive first coefficient and non-9 last coefficient, and with `H=(c)`
for every even `c` from 0 through 18. There are exactly 1,705 such states.
It follows the symbolic transition (8) until mixed carry is lost or the
bands merge; there is no interface-width or iteration cap.

The complete reachable graph has 4,083 states, 2,784 transition edges,
1,146 mixed-carry-loss terminal states, and 153 band-merge terminal states.
No cycle occurs. The maximum strict DAG rank is 22; among seed states,
1,489 terminate by mixed-carry loss and 216 by band merge. The largest
interfaces reached have `|B|=11` and `|H|=9`.

Initial gaps `g>=10` suffice for every recorded seed trajectory to maintain
gaps at least 2 until its terminal update. Therefore, for every such gap,
this entire initial family loses the specified two-band mixed mechanism
within 22 actual updates. A loss of this mechanism does not imply an
ordinary palindrome, and the statement does not exclude later regeneration
with different band number, bulk coefficient, or interfaces.

`verify_neutral_quotient.py` imports no search code. It reconstructs each
transition through ordinary integer evaluation and decimal conversion,
verifies the complete initial-state set and all graph targets, reconstructs
reachability, and assigns a strict DAG rank. Its result is
`neutral_quotient_verification.json`. The all-gap bridge is the written
identity (7); finite integer checks serve as independent arithmetic controls.

## 8. Reproducibility and scope

Run from any working directory:

```
python seam_transport.py
python neutral_quotient.py
python verify_neutral_quotient.py
```

`seam_transport.py` checks every canonical word of widths 1 through 7:
75,447 words, including 7,439 active ones. It additionally checks all 58,221
partitions for widths 1 through 5, the exact attainable-mask sets and masses,
3,473 mixed-run transport instances, and 19 named family controls. Among
the active short words, 5,468 lose all seams in one update and 1,050 enter
the immediate-palindrome-predecessor class in that update. These are finite
descriptive counts; the unrestricted theorems are proved above.

Full transport/family controls are saved in `seam_transport_controls.json.gz`.
The complete quotient graph and every seed path are in
`neutral_quotient_controls.json.gz`. Both result files pin decompressed
payload SHA-256 hashes, and the independent graph verifier pins the same
quotient hash.

The main unresolved step is now concrete: find an actual cycle or another
indefinitely closed path in the mixed quotient, or enlarge the model to
track band loss and later birth while proving safety during every intervening
phase. Neither unlimited defect mass nor arbitrary partition adaptation
discharges that obligation. Uniform digit-sum escape does not provide it.
