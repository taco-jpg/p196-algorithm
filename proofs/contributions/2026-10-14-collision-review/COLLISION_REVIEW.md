# Zero-gap safety, exact reset recognition, and a universal driver audit

This review concerns canonical symmetric decimal pair words. It proves
two structural statements and gives a third explicit obstruction. It
does not prove infinite safety for the remaining `(1,7)` gate family or
for 196. The new statements below are written proofs, not new Lean
formalizations.

## 1. The exact palindrome test survives zero spacer

Let `B,H` be nonempty canonical symmetric pair words, and let `g >= 0`.
Write `N(W)` for ordinary decimal normalization of the coefficients,
including its final overflow digit, and write `e(W)` for that overflow
bit. Then

    N(B 0^g H 0^g B) is palindromic
    iff N(B) and N(H) are palindromic and e(B)=e(H).

In particular, this equivalence remains true when `g=0`, even though
independent normalization of adjacent blocks can fail at zero spacer.

Proof: the repository's exact `BadWord` criterion has just two disjoint
cases. The first says every coefficient is at most 9; normalization is
palindromic with no overflow. The second says the outside coefficient
is 11 and every coefficient belongs to `{0,11}`; normalization is
palindromic with overflow. Applied to the concatenated word, the first
case is exactly the first case for both `B,H`. In the second case,
positivity of both block endpoints forces both outside coefficients
to be 11, so it is exactly the second case for both blocks. Conversely,
either matching pair of cases immediately gives the corresponding
whole-word case. The inserted zero coefficients affect neither case.

This is a safety test for one next iterate. It makes no assertion that
the blocks can still evolve independently after contact.

## 2. Complete recognition of a renewed separated representation

For any canonical symmetric word `Q=(q_0,...,q_(L-1))`, all decompositions

    Q = B 0^g H 0^g B^R,   g>=1,

with nonempty canonical symmetric `B,H`, can be found as follows.

1. Choose a proper prefix length `b` with `1 <= b < L/2`.
2. Require that `Q[:b]` is canonical and symmetric, and that `q_b=0`.
3. Let `j>b` be the first subsequent nonzero index. Require `2j<L`.
4. Set `B=Q[:b]`, `g=j-b`, and `H=Q[j:L-j]`.

These conditions are necessary and sufficient. Necessity follows from
the positive endpoints of `B,H`: the gap must be the whole zero run
immediately following the prefix. Conversely, whole-word symmetry
reflects the left prefix and gap into the required right blocks. The
middle word has positive endpoints, inherits symmetry and coefficient
bounds, and inherits the even-center condition whenever it has a center.
Thus it is canonical. There is no unexamined split or gap length.

This exact recognition criterion shows that counting zeros alone is
insufficient: a reset also requires a canonical palindromic prefix
immediately preceding a suitable zero run.

## 3. No universal three-step reset rule for arbitrary collisions

For every `L>=3`, take the canonical zero-gap word `Q_0=18^L`.
It can be written `B H B` with `B=(18)` and `H=18^(L-2)`.
Let `G(W)` be the pair word of `N(W)`. Then direct decimal carrying gives

    Q_1 = (9) 18^(L-1) (9),
    Q_2 = (10,8) 18^(L-2) (8,10),
    Q_3 = (1,9,17) 18^(L-3) (17,9,1).

Here powers denote repetition, and a zero repetition is empty. To verify
the identities, the normalized digit words, in least-significant-first
order, are

    N(Q_0) = (8) 9^(L-1) (1),
    N(Q_1) = (9,8) 9^(L-2) (0,1),
    N(Q_2) = (0,9,8) 9^(L-2) (0,1).

Pairing each displayed digit word with its reversal yields the formulas.
Every coefficient in `Q_0,...,Q_3` is positive. Therefore none admits
a decomposition with a positive zero spacer, under any choice of block
widths. All four words also lie outside both `BadWord` classes, so lack
of a reset is not itself a palindrome event. This excludes a proposed
reset within three updates for every arbitrary canonical collision; it
does not exclude a special reset theorem for the `(1,7)` trajectory.

## 4. Finite short-reset observations for the remaining gate

`structural_controls.py` enumerates every decomposition from Section 2
for the first zero-gap state and its next three pair updates, for each
`r=1,...,32` of the `(1,7)` gate. It preserves the complete pair words in
`structural_controls.json`.

A blanket claim of no resets is false. For example, `r=4` admits a
reset after two updates with exterior `(4,4)` and gap 1. The `r=31`
collision admits a reset after one update with exterior `(10)` and gap 1.
Conversely, `r=1` has no zero coefficient at any of the first four tested
states, so it has no positive-spacer reset in that window. The observed
resets have not been proved to recur, and their occurrence supplies no
all-time invariant.

## 5. Universal separated-driver search

The exact separated transition defines one parameter-independent driver
starting with

    B_0=(1,1),  H_0=(1,8,14,8,1).

Let `delta_t=max(e(B_t),e(H_t))` and `S_t=sum_(j<t) delta_j`. For every
`r >= S_t+2`, the original gate still has a positive spacer at time `t`
and has pair word `B_t 0^(r-1-S_t) H_t 0^(r-1-S_t) B_t`.
Thus a simultaneous matching predecessor event in this driver would
prove a palindrome at the same time for every sufficiently large `r`.

`driver_search.py` checked every driver state `t=0,...,9999`. No matching
event occurred. The exterior alone belongs to `BadWord` exactly at

    t = 0,1,2,3,9,10,16,26,33,

and the central block alone belongs to it exactly at `t=5`, within this
tested window. Every event is in the nonoverflow case. At the final
tested state, `S_9999=5077`, `|B_9999|=4131`, and `|H_9999|=6030`.
The scope is a finite driver certificate, not a claim that either block
avoids the predecessor classes at every later time. In particular,
the absence of events after time 33 in this trace is not an invariant.

A targeted attempt to reduce the exterior driver to the 196 orbit also
remained inconclusive. The exterior driver is the pair-word orbit starting
from the integer 10. Exact state sets for the integer seeds 10 and 196,
each at times 0 through 1000, had empty intersection. This finite result,
retained under `exploratory_merge_check` in the structural controls, neither
excludes a later merger nor gives an independent all-time safety argument.

The full coefficient trace is `driver_trace.bin.gz`; `driver_summary.json`
contains its SHA-256, exact schema, category counts, checkpoints, and all
ten exceptional states. The gzip header is deterministic. Replay with

```sh
python -B proofs/contributions/2026-10-14-collision-review/driver_search.py --steps 10000
python -B proofs/contributions/2026-10-14-collision-review/structural_controls.py
```

The structural controls include 128,547 ordinary-integer tests of the
Section 1 equivalence, the explicit positive family for all widths
3 through 200, and the 32 short collision windows. The all-width proofs
are the arguments above, not an extrapolation from those controls.
