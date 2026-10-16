# Folding does not rescue positive local incoming-weight bounds

15 October 2026. **No decimal Lychrel witness is proved.** This is an
exact obstruction to a specified incoming-weight estimate on the actual
folded reverse-and-add dynamics. It is not a statement about a forward
contraction, and no arbitrary-future-safety assertion is needed.

The prior `persist_inverse_fibers_proof.txt` already gives sharp
unweighted Fibonacci and binary overflow fiber rates. The prior
`astra_counting_safe_image_fibers.txt` retains binary rate after two safe
incoming layers; `main_existence_attempt/decimal_counting_return_notes.txt`
proves a smaller rate for certain constant-rho fibers with three incoming
image layers. Those are existing results. This note supplies a different
obstruction: arbitrary **strictly positive coefficient-product weights**,
and more generally fixed finite-range positive weights, cannot turn the
safe incoming operator into a uniformly bounded pointwise operator.

## 1. State space and one exact binary family

A canonical even-width pair word has the form `q=H || reverse(H)`, where
the half-word `H` uses coefficients in `{0,...,18}` and its first
coefficient is positive. Such words are realized by ordinary positive
decimal integers. Let `G(q)` be the pair word of

    E(q) = sum_i q_i * 10^i.

This is the actual pair-word dynamics: if an integer `n` has pair word
`q`, then `T(n)=E(q)` and `Q(T(n))=G(q)`.

Call a pair word safe when `E(q)` is nonpalindromic. The exact predecessor
classification says that the unsafe words are precisely the all-small
words, and words using only `0,11` with outside coefficient 11. A
coefficient 18 excludes both classes.

Fix integers `r>=0`, `k>=1`. Define one target half-word

    R(r,k) = (11, 9^(4r+1), 18^k),

where superscripts mean repetition, and reflect it to obtain the full
target. For each binary word `epsilon` of length `r`, take blocks

    U = (9,9,9,9),        V = (14,14,4,4),

according to its bits and define the predecessor half-word

    H_epsilon = (5, M_1,...,M_r, 14, 18^k),
    M_i = U or V.

Then every one of these `2^r` distinct reflected canonical words has
the **same no-overflow G-image**, namely the reflection of `R(r,k)`.
Both source and target have width `2(4r+k+2)` and contain the same
central block of `2k` coefficients equal to 18. In particular both
are safe. Their odd outer coefficients 5 and 11 also ensure that every
ordinary decimal realization is initially nonpalindromic.

### Complete carry proof

In the no-overflow inverse calculation, a state `(a,b)` records the low
incoming carry and high outgoing carry. If `x` is the predecessor
coefficient and `b'` the next high carry, the exact equations are

    a' = floor((x+a)/10),
    b  = floor((x+b')/10),
    s  = ((x+a) mod 10) + ((x+b') mod 10).

Here `s` is the target coefficient and the next inverse state is
`(a',b')`. Every needed edge is listed below and can be substituted
directly into these three equations.

| Current state | Target `s` | Emitted `x` | Next state |
|---|---:|---:|---|
| `00` | 11 | 5 | `01` |
| `01` | 9 | 9 | `01` |
| `01` | 9 | 14 | `11` |
| `11` | 9 | 14 | `10` |
| `10` | 9 | 4 | `00` |
| `00` | 9 | 4 | `01` |
| `11` | 18 | 18 | `11` |

The initial state is `00`, as there is no incoming low carry and no
final overflow. Reading the outer target 11 emits 5 and reaches `01`.
The block `U` consists of four self-loops at `01`; the block `V`
traverses the four-edge cycle

    01 -> 11 -> 10 -> 00 -> 01.

Both emit four target nines. The final 14 emits one further target 9
and reaches `11`. Each central 18 emits 18 and stays at `11`. The
equal carries at the even center are exactly the condition permitting
reflection to a whole canonical word. Thus the construction uses
actual ordinary addition at every column, not merely a prefix path.

For `r=0`, the empty block list gives `(5,14,18^k)` and target
`(11,9,18^k)`, with exactly the same proof. This convention will also
be used below.

## 2. Every strictly positive coefficient-product weight fails

Choose arbitrary positive real numbers `a_0,...,a_18` and arbitrary
positive width factors `A_L`. On **even-width canonical words**, define

    w(H || reverse(H)) = A_(2|H|) * product_(x in H) a_x.

Each reflected coefficient pair is counted once, through its half-word.
The coefficients `a_x` are fixed across positions and widths; they need
not decrease with `x` or with the represented integer.

For a safe target `q`, let

    (L_safe w)(q) = sum_{p safe, canonical, G(p)=q} w(p).

One may include odd-width predecessors in this operator, with arbitrary
positive weights. Our subset of even-width predecessors already gives
the following lower bound. Summing only the displayed binary family,

    sum_epsilon w(H_epsilon || reverse(H_epsilon))
      = A_L * a_5*a_14*a_18^k * (a_9^4+a_14^2*a_4^2)^r.

The target weight is `A_L*a_11*a_9^(4r+1)*a_18^k`. Consequently

    (L_safe w)(R || reverse(R)) / w(R || reverse(R))
      >= (a_5*a_14)/(a_11*a_9)
           * (1+(a_4*a_14/a_9^2)^2)^r.                 (1)

The width factors and the fixed central block cancel exactly. The base
in (1) is strictly larger than 1 for **every** strictly positive choice
of coefficient weights. Letting `r` grow proves:

> No finite constant `C` can satisfy `L_safe w <= Cw` at every canonical
> safe target for any such positive product weight.

This remains true with arbitrary width-only normalization. In particular,
folding away the ordinary-digit complement multiplicities and choosing
nonmonotone positive coefficient weights do not remove the obstruction.
This does not negate the prior restricted incoming-image estimates:
the present family is not claimed to have any prescribed number of
earlier image layers.

## 3. Any fixed finite-range positive potential has the same obstruction

Fix a window length `d>=1` and a **translation-invariant** function

    psi : {0,...,18}^d -> positive real numbers.

The function is fixed across word lengths. For a half-word `H` with
`|H|>=d`, define

    w(H || reverse(H))
      = A_(2|H|) * product_(i=0,...,|H|-d) psi(H_i,...,H_(i+d-1)),

where again `A_L>0` is any width-only normalization. These are products
over the complete unpadded length-d windows of the half-word.

Set `b=d-1`, fix any `k>=1`, and use the buffered predecessor

    H_epsilon = (5, 9^b, M_1, 9^b, ..., M_r, 9^b, 14, 18^k).

The corresponding target half-word is

    R_d(r,k) = (11, 9^(r(d+3)+d), 18^k).

For `r=0`, the predecessor is `(5,9^(d-1),14,18^k)` and the target
is `(11,9^d,18^k)`. The extra nines are inverse self-loops at state
`01`, so the same carry proof shows that all `2^r` words map to this
one target without overflow. Source and target remain safe and have
the same width.

Compare each predecessor with the all-`U` predecessor. Replacing one
`U` by `V` changes precisely the `d+3` windows meeting that four-letter
block. Its surrounding `d-1` letters on each side are all nines. Put

    Z = 9^(d-1) || (14,14,4,4) || 9^(d-1),
    beta = product_(i=0,...,d+2) psi(Z_i,...,Z_(i+d-1))
               / psi(9,...,9)^(d+3).

Strict positivity gives `beta>0`. No length-d window meets two inserted
blocks, because the intervening `d-1` nines separate their changed
positions. The initial and final buffers likewise separate every block
from the changed endpoint neighborhoods. Therefore

    w(H_epsilon || reverse(H_epsilon))
      = w(H_all-U || reverse(H_all-U)) * beta^(number of V blocks).

The all-`U` predecessor and its target differ only at their first
coefficient, 5 versus 11, and at the coefficient just before the 18
block, 14 versus 9. Those two neighborhoods are also separated, even
when `r=0`. Their weight ratio is the positive constant

    C_(d,k) = psi(5,9^(d-1)) / psi(11,9^(d-1))
       * product_(j=0,...,min(k,d-1))
           psi(9^(d-1-j),14,18^j) / psi(9^(d-j),18^j).

The upper limit handles the unpadded end when `k<d-1`. This constant is
independent of `r`. Summing all binary choices yields the exact subset
weight ratio

    sum_epsilon w(H_epsilon || reverse(H_epsilon))
       / w(R_d(r,k) || reverse(R_d(r,k)))
      = C_(d,k) * (1+beta)^r.                           (2)

For `d=1`, the buffers are empty,
`C_(1,k)=a_5*a_14/(a_11*a_9)` and
`beta=a_14^2*a_4^2/a_9^4`, recovering (1). For `r=0`, (2) simply
states the endpoint ratio, as required.

Since `beta>0`, (2) rules out every finite uniform pointwise bound for
the safe incoming operator under **any** positive, translation-invariant,
fixed finite-window product weight of this form.

The scope matters. Position-dependent potentials, potentials depending
on the total word length, unbounded-range weights, and factors allowed
to vanish are not covered. Nor is an estimate restricted to a sufficiently
deep actual image support. Establishing a positive invariant or a useful
all-time first-hit estimate within one of those other settings remains a
separate obligation. These results do not constitute a search failure
for every possible weighting scheme.

## 4. Exact finite controls

Run from the project root:

    python main_existence_attempt/continuation_pass/finite_seed/check_folded_weights.py

The checker uses ordinary decimal digit realization, reversal and
addition. It does not import the earlier inverse automaton code.

- For `r=0,...,10` and `k=1,2,3`, it checks all 6,141 displayed
  predecessors, the common image, no overflow, and both source/target
  safety. It checks the exact summed-weight identity for three strictly
  positive coefficient assignments, including the all-one assignment.
- For `d=1,...,5`, `k=1,3`, and `r=0,...,6`, it checks all 1,270
  buffered predecessors. A positive translation-invariant range-d
  potential and a nonconstant width factor are used. Every insertion
  ratio, every endpoint constant, and (2) are checked as exact rational
  equalities, including `r=0`, `d=1`, and the `k<d-1` boundary cases.

Every check passed. `check_folded_weights.json` retains the parameter
records, rational ratios, counts and hashes of the literal controls.
The all-parameter claims have the written carry and factorization proofs
above. This branch supplies no additional Lean theorem and makes no
external peer-review or novelty claim.
