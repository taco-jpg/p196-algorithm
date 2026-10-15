# Two-step certificate regeneration after a high-carry word

This note continues the exact high-carry adjacency reduction. It gives conditions which regenerate a mixed-coefficient safety certificate two steps later, together with a restricted return map and an obstruction to repeating that map. None is an infinite invariant.

Write `T` for ordinary reverse-and-add in base `b`, and let `Q_j` be the canonical pair-coefficient word of `T^j(n)`, stored from least to most significant. The initial word has length `L`. For bases `b >= 3`, the established classification says that a symmetric canonical pair word has a palindromic normalized output exactly when either all its coefficients are at most `b-1`, or its exterior coefficient is `b+1` and every coefficient belongs to `{0,b+1}`. In particular, a positive coefficient below `b` and another at least `b` certify a nonpalindromic next output.

## 1. A third-output obstruction using only the exterior

For any canonical pair word, with no hypothesis on its interior, put

`a = q_0 - b + 1`.

If `q_0 >= b` and

`a >= ceil((b+2)/2)`,

then the third positive output `T^3(n)` is nonpalindromic. The first positive output is nonpalindromic as well. The second output may be a palindrome.

Indeed, the first addition overflows and its exterior pair coefficient is `a`: its low digit is `q_0-b` and its new high digit is one. At the next addition let `v` be the actual carry into the high exterior column. If that addition does not overflow, the new exterior pair coefficient is `2a+v`, at least `b+2`. If it overflows, necessarily `a=b-1` and `v=1`; the new exterior pair coefficient is `b`. Both possibilities exclude the two palindrome classes. The initial exterior also excludes both classes. The range is empty in base three, so there is no exceptional binary-like endpoint hidden in this argument.

In decimal, the condition is simply `q_0 >= 15`: the exterior coefficient of `Q_2` lies in `12..17`, or is `18` or `10`. Consequently the first and third positive outputs are always nonpalindromic. This assertion concerns positive output times, not the palindrome status of the initial seed.

## 2. The high-carry map and two local regeneration conditions

Now assume `L >= 2`, every `q_i` lies in `[b-1,2b-2]`, and `q_0 >= b`. Define `r_i=q_i-b+1` and `a=r_0`. The exact first pair-word update is

`P = Q_1 = (a, r_0+r_1, r_1+r_2, ..., r_(L-2)+r_(L-1), a)`.

This follows from the all-one carry profile of the first addition. Set `z=P_1=q_0+q_1-2b+2`. The following conclusions use the actual carries through `P`, so no independence assumption about its interior is needed.

### Maximum exterior

If `q_0=2b-2` and `q_1 >= b+1`, then

`(Q_2)_0=b`, and `(Q_2)_1=q_1-b` in `[1,b-2]`.

Proof: `P_0=P_L=b-1` and `P_1=P_(L-1)=q_1>=b+1`. The high neighbor forces carry one into the last column, which therefore overflows. The normalized digits at positions zero, one, `L`, and `L+1` are respectively `b-1`, `q_1-b`, zero, and one. Reflection at the actual width `L+2` gives the two claimed pair coefficients. The same argument applies when `L=2`; the two descriptions of the inner column then refer to the same column.

Thus a mixed-coefficient certificate is regenerated at time two. In decimal the condition is `q_0=18, q_1>=11`, and the regenerated coefficients are `10` and `q_1-10` in `1..8`.

### A nonoverflowing exterior

Suppose

`ceil((b-1)/2) <= a <= b-2`,

and

`b+1 <= z <= b+floor((b-2)/2)`.

Then, for an actual carry `v` in `{0,1}`,

`(Q_2)_0=2a+1 >= b`,

`(Q_2)_1=2(z-b)+v` in `[2,b-1]`.

Proof: the low exterior column of `P` produces no carry. Its high neighbor has coefficient `z>=b+1`, so it forces carry one into the last exterior column. Since `a<=b-2`, the last column does not overflow. The output digits at the two exteriors are `a` and `a+1`. At the neighboring positions they are `z-b` and `z+v-b`, where `v` is the actual carry into the high neighbor. Reflection now uses width `L+1`. For `L=2` the two neighboring positions coincide, their incoming carry is zero, and the displayed formula remains correct with `v=0`.

In decimal this gives the particularly simple condition

`14 <= q_0 <= 17` and `29 <= q_0+q_1 <= 32`.

The regenerated exterior is `2q_0-17` in `{11,13,15,17}`, while its next coefficient is `2(q_0+q_1-28)+v` in `2..9`. In particular, the exterior `11` case is safe because of the positive small neighboring coefficient.

Both decimal conditions guarantee that all three positive outputs are nonpalindromic: the first high-carry output is palindromic only for the uniform word `11`, the second is nonpalindromic because the first adjacent original sum exceeds `27`, and the third is excluded by the regenerated mixed certificate. The initial seed itself may already be palindromic. In the all-base maximum-exterior condition the uniform word `b+1` remains a possible first-output exception at base three; the regenerated certificate and third-output conclusion are unaffected.

## 3. An exact restricted return to the decimal high region

Here take base ten, `L>=3`, `q_0<=17`, and all adjacent original sums at least `28`. Equivalently, every interior coefficient of `P` is at least ten. Put `a=q_0-9` and `p_i=q_(i-1)+q_i-18` for `1<=i<=L-1`.

The actual carry profile through `P` is zero before its first two columns, one after every interior column, and zero after its final column. Its normalized word has width `L+1`, with digits

`d_0=a`, `d_1=p_1-10`, `d_i=p_i-9` for `2<=i<=L-1`, and `d_L=a+1`.

Therefore the exact second pair word is

- exterior: `2q_0-17`;
- next coefficient at either end: `2(q_0+q_1)-55`;
- interior positions `2<=i<=L-2`: `2(q_(i-1)+q_i)-54`.

The index ranges include the small case `L=3`, where the last range is empty. For `L=2` the unique middle coefficient is instead `2(q_0+q_1)-56`; it is not covered by this return statement.

Within the stated hypotheses, `Q_2` returns to the high region (all coefficients in `9..18`, exterior at least ten) **if and only if every adjacent original sum is at least `32`**. The neighboring and interior inequalities both reduce to this integer threshold. The exterior requirement then follows from `q_0+q_1>=32` and `q_1<=18`, which force `q_0>=14`. Upper bounds follow either from the displayed formulas or from canonical pair bounds.

This return condition does not persist automatically. In fact, it cannot hold for three consecutive two-step returns. Write `A=q_0`, `B=q_1`. A qualifying return changes them by

`A'=2A-17`, `B'=2A+2B-55`.

If `A<=16`, then `A'+B'=4A+2B-72<=28`, since `B<=18`, so the next word already fails the required first adjacent sum `>=32`. If `A=17`, then `A'=17` and `B'=2B-21<=15`. A second qualifying return forces `B'=15`, hence `B=18`; that return gives `B''=9`, making the following first sum `17+9=26`. Thus there are at most two consecutive returns under this particular condition.

The bound two is attained by the canonical word `(17,18,18,17)`:

`(17,18,18,17) -> (17,15,18,15,17) -> (17,9,12,12,9,17)`,

where each arrow means two pair-word updates. The last word still lies in the high region but fails the adjacent-sum return condition. This is an obstruction to repeating this sufficient condition, not an obstruction to other later returns or to a permanently safe orbit.

## 4. Scope and controls

The local regeneration criteria do not claim that every high-carry word regenerates a mixed certificate. For example, `(15,18,18,15)` has second pair word `(13,11,18,11,13)`, whose coefficients are all high. Conversely, the high region itself is not an invariant and its return does not alone certify safety at every intervening time.

The accompanying bounded controls use literal canonical seed digits, ordinary integer reversal, and recomputed pair words. They exercise both physical widths, the `L=2` overlap, actual incoming carry choices, the base-three first-output exception, and the two-return example. These controls support the formulas; the proofs above establish their all-parameter scope.

The retained run passes 177 explicit canonical-word controls and ten elementary boundary-recurrence controls. Reproduce it from the repository root with:

```sh
python proofs/contributions/2026-10-15-high-carry-renewal/check_renewal.py
```

Dependencies and scope links:

- The all-base output classification is proved in `../2026-10-14-general-base-seams/GENERAL_BASE_SEAMS.md` and its formal reflection stack in `../2026-10-15-base-reflection-formal/`.
- The exact first high-carry update and adjacent-sum criterion appear in `../2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`; their decimal formal counterpart is `../2026-10-15-high-carry-reduction-formal/HighCarryReduction.lean`.
- The mixed-coefficient safety implication is explained in `../2026-10-15-interval-certificate-reduction/INTERVAL_REDUCTION.md`.

The producer retains the false stronger guess that an exterior at least fifteen always regenerates a mixed certificate, together with its exact counterexample. The universal third-output theorem survives that counterexample because it uses the exterior classification directly.
