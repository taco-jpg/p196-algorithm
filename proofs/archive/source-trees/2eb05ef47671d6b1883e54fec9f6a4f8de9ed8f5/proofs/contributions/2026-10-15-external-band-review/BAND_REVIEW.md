# Independent review of the external two- and four-band formulas

**Result: PASS, written/source review.** This review concerns the exact
all-gap identities and conditional cycle arguments in external commit
[`60d4348349a80c513008df9263905e7955b4ce79`](https://github.com/taco-jpg/p196-algorithm/commit/60d4348349a80c513008df9263905e7955b4ce79).
It read both method notes and their symbolic transition implementations.
It did not rerun the finite graph searches or claim new Lean verification.
The existing independent finite-verification reports were inspected as
supporting records, not represented as newly reproduced results.

## Two neutral bands

The empty exterior block is correctly included. Its isolated carry is
zero; mixedness forces the carry after the middle block to be one; the
empty reflected exterior then passes that carry through. Thus this case
necessarily overflows. The overflowing formula gives a one-coefficient
raw exterior and retains the appropriate shifted central block.

No positivity assumption on the outside of the middle block is needed.
Zero endpoints legitimately reset a carry. The calculation normalizes
the actual consecutive blocks and therefore does not appeal to a
positive-canonical-component theorem outside its domain.

Without overflow the digit blocks align. With overflow, the leading
terminal digit shifts the reflected block by one place: the raw exterior
has length (|B|+1), the central digit block has length (|H|+1), and
each retained neutral band has length (g-1). These lengths and the
displayed coefficientwise sums give the stated identity for every
(g\ge2).

If the raw middle is all 9s, the central separator disappears into the
neutral bands, so the specified two-band mechanism has ended. Otherwise
the maximal outer pairs of 9s can be removed without emptying the middle.
Trailing 9s may remove the entire raw exterior; the remaining word still
has positive outside coefficient 9. The gap change is exactly
(u+v-\gamma), and the physical-width identity accounts for every
absorbed column.

## Four neutral bands

The overflowing raw middle-interface formula uses

\[
 (D_A\mathbin{\|}z_1)+(z_3\mathbin{\|}\operatorname{rev}D_{RA}).
\]

The use of (z_3), rather than an inner-band digit, is correct: it is the
high outer-band digit exposed by the one-place reflection shift. The
central raw block is the pair word of (D_C\mathbin{\|}z_2). Raw exterior,
middle-interface, and central lengths grow by 1, 1, and 1 under overflow;
the four neutral bands each lose one place. The net width increase is
therefore exactly one.

Leading and trailing trims of the raw (A) block cannot overlap unless
that block is entirely 9, which is checked as a merge before trimming.
The same all-9 check protects the central symmetric trim. Empty (B)
and zero endpoints in (A) or (C) remain valid. The two gap changes are
correctly separated:

\[
 \delta_g=u_B+v_A-\gamma,\qquad
 \delta_h=u_A+v_C-\gamma.
\]

A merge or loss of either mixed condition terminates only the tracked
four-band mechanism. It need not imply an ordinary palindrome or the
absence of other active seams. If both kinds of merge occur, the
implementation's first matching exit classification affects reporting
only, not the identity or the exclusion's mathematical scope.

## Safety and the cycle condition

A mixed neutral band has one actual incoming carry equal to one and the
opposite incoming carry equal to zero. Since a 9 preserves a carry, the
one must originate at a high non-9 coefficient. At least one orientation
therefore has an active high-to-9 adjacency. Reflection of the canonical
whole pair word supplies the low-to-high orientation used by the intrinsic
seam safety theorem. Hence every tracked source certifies that its next
ordinary output is nonpalindromic. Also, the source pair word contains
the odd coefficient 9, so none of its ordinary realizations can itself
be a palindrome.

Summing the exact width identity on a finite interface cycle gives twice
the total gap gain equal to the total overflow count. This count is
strictly positive: otherwise the positive outside pair coefficient at
least doubles at every actual no-overflow step and cannot return. Empty
exteriors supply no exception, since their outer mixed condition forces
overflow.

For one gap, its total gain is consequently positive. For two gaps,
positive total gain is insufficient: **each coordinate must have
nonnegative gain** to repeat the same cycle indefinitely. A negative
coordinate eventually violates the minimum-gap premise, regardless of
how large its finite initial value was. Choosing both initial gaps above
all within-cycle deficits is sufficient when each total coordinate gain
is nonnegative. The state must return with the same finite interfaces
and their assigned outer/inner roles.

These are valid conditional finite-seed constructions. Neither note
asserts that a qualifying cycle was found. The finite DAG results apply
only to the specified reachable initial-interface families and the
tracked mechanism; the all-gap interpretation uses the written identities,
not extrapolation from the reported sample gaps.

## What changing band number leaves open

The recorded DAGs stop at mixedness loss or band merge. An actual orbit
may remain safe at such an exit and later generate neutral bands from
old 4/14 columns or nonneutral neighbors. Consequently a larger exact
state system may include transitions between band architectures. The
current DAGs do not exclude it.

Such a system must retain an actual safety certificate during every
intervening update. It must also derive exact transformations of all
gap parameters. A merge can combine two gap lengths and the finite
separator width; a birth can introduce a finite new gap. Relabeling
these as arbitrary independent growing gaps would not be justified.
A return across architectures generally has an affine parameter map,
not merely the fixed-coordinate translation proved in these notes.
Its invariant parameter domain and all intermediate minimum-gap bounds
would require a new proof. No positive instance or unbounded search is
claimed by this review.

## Exact source attribution

Paths below are relative to
`proofs/research/main_existence_attempt/continuation_pass/` at the pinned
external commit.

| Method note | Git blob SHA-1 | SHA-256 |
| --- | --- | --- |
| `seam_persistence/METHOD_AND_PROOF.md` | `28f976ab2dae4fa5657f7ffde265e8d2be9bc0a2` | `c3ed634ba0bbf21c127837ecefd5883ec935dcea5d807e29e4a77b29bd724943` |
| `safe_language_followup/METHOD_AND_PROOF.md` | `bcffa804ebeffe38c7aa1aa1a6bef3ac16252044` | `28747a7fa9ef82673fb9f143efb93d2279a54c6056e113867a51df6cc9157a69` |

`review_sources.json` pins the method notes, transition implementations,
result files, and observed verifier reports. Existing sources were not
modified.
