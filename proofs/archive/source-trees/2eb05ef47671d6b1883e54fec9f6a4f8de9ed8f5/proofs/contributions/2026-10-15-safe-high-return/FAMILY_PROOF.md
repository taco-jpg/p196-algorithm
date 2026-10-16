# An all-width family attaining three safe high-region returns

Agent #1. This strengthens the finite witness in the first contribution.
The six transitions and the ordinary-integer interpretation are now also
kernel checked in `SafeHighFamily.lean`; they are not inferred from the
finite controls. This is a finite-time theorem for infinitely many seeds,
not an infinite-time theorem for one seed.

## Statement

Let `T(n)=n+reverse10(n)` on positive ordinary decimal integers, and let `Q(n)`
be its symmetric digit-pair-sum word, stored least significant first. Let
`H` mean every coefficient lies in `9..18` and the exterior is at least ten.
For every integer `k>=5`, put

`n_k = 81*10^(k+2)-1`.

Its decimal expansion is `80` followed by `k+2` nines, so
`Q(n_k)=(17,9) 18^k (9,17)`. Here `18^k` denotes a constant **word**, not
integer exponentiation. Then `Q(T^t(n_k))` belongs to `H` at `t=0,2,4,6`,
and all seven integers at `t=0,...,6` are nonpalindromic. Consequently the
existing upper bound of three two-step high-region returns is sharp even
with safety at every intermediate time.

The Lean parameter is `m=k-5`. Its ordinary-integer endpoint is
`safe_three_returns_family`, and `seed_closed_form` gives
`seed m = 81*10^(m+7)-1`. No root certificate, carry oracle, external
finite search result, or unproved bridge is a premise of either theorem.

## The seven exact pair words

Write `P 18^r rev(P)` for a symmetric word with prefix `P`, middle run
length `r`, and reflected suffix. All prefixes below are least significant
first, and the quantities in the middle column are nonnegative for `k>=5`.

| t | P | r |
|---:|---|---:|
| 0 | (17,9) | k |
| 1 | (8,8,9) | k-1 |
| 2 | (16,17,9,17) | k-3 |
| 3 | (7,15,8,8,17) | k-4 |
| 4 | (15,10,17,17,15) | k-4 |
| 5 | (6,7,9,16,14,15) | k-5 |
| 6 | (12,15,9,13,10,12) | k-5 |

In particular the last two middle runs may be empty. The formulas and
proof include `k=5`; no positive-length assumption is silently imposed there.

## Carry normalization proves all six transitions

For a coefficient word `q`, scan from the least significant end with carry
zero. At a column `(a,c)`, output `(a+c) mod 10` and send
`floor((a+c)/10)` to the next column. Append a nonzero terminal carry.
The output digits are canonical in every row below: each is between zero
and nine and the final digit is positive.

The actual output digit word at transition `t -> t+1` is
`L 9^r R`, with **equal lengths of L and R**:

| source t | L | r | R |
|---:|---|---:|---|
| 0 | (7,0,9) | k-1 | (0,8,1) |
| 1 | (8,8,9,8) | k-3 | (9,0,9,8) |
| 2 | (6,8,0,8,9) | k-4 | (8,0,8,7,1) |
| 3 | (7,5,9,8,7) | k-4 | (8,9,8,5,8) |
| 4 | (5,1,8,8,6,9) | k-5 | (6,8,8,1,6,1) |
| 5 | (6,7,9,6,5,6) | k-5 | (6,5,7,0,8,6) |

To check each row for arbitrary length, perform the finitely many boundary
column operations. Inside every remaining run of eighteens the incoming
carry is one, so `(18+1) mod 10=9` and `floor((18+1)/10)=1` repeat
unchanged. This is the induction lemma `normalize_eighteens`. In the
second row, moving one nine across a constant run uses `nine_commute`;
it remains valid when the residual run is empty. No freely selected carry
is used. The six complete identities are `norm0` through `norm5`.

Because the two finite sides have equal lengths, pairing this canonical
output with its actual-width reversal gives

`(L+rev(R)) 18^r (R+rev(L))`.

The additions here are coordinatewise. Computing the finite sums gives the
next prefix in the first table. `pair_blocks` and the seven `*_pair` lemmas
formalize this reflection step without assuming disjoint prefix locations.

## Ordinary integer semantics and safety

Let `value(d)` evaluate a least-significant-first word at ten. The generic
proofs establish

`value(normalize(q,c)) = value(q)+c`,

`value(pair(d)) = value(d)+value(rev(d))`.

For every canonical positive decimal word `d`, the proof also establishes
`digits10(value(d))=d` and
`reverse10(value(d))=value(rev(d))`. The structural digit extractor has
fuel equal to its input integer, not a fixed digit cap. The formal proof
`digitsAux_value` shows any fuel at least the word length suffices, and
`decimal_length_bound` discharges that condition for canonical words.
Thus `ordinary_step` connects the list calculation to exactly the same
natural-number reverse-and-add map used by the finite witness.

The initial digit word and every row of the normalized digit table are
nonpalindromic: compare the first unequal reflected boundary digits. For
rows 1 and 5 the outermost digits agree, but the next reflected pair does
not. Alternatively every pair word in the first table contains an odd
coefficient, impossible for a palindromic digit word. The Lean proof uses
the explicit digit comparisons, not the unformalized alternative argument.

At even times, the first table has all coefficients in `9..18` and exterior
respectively `17,16,15,12`. This proves the high-region memberships. Combining
these with the six exact ordinary transitions proves the statement.

## Scope and controls

The source has a complete ordinary-integer bridge, not just a necessary
finite graph or an implication with a missing realization assumption.
The existing general upper bound still has its separately documented
written actual-orbit bridge and finite Lean rank proof; this contribution
does not claim to have rebuilt that earlier upper-bound package.

`verify_family.py` checks `k=5..256` through time six using both carry
normalization and literal integer reversal. These 252 finite controls
support implementation checking, not the universal quantifier in the proof.
The stored digest identifies the exact generated comparison stream.

For `k=5`, the first palindrome is at time eight. Nothing here states that
other family members remain safe forever, return indefinitely to H, or
intersect the orbit of 196. No novelty or external peer-review claim is made.
