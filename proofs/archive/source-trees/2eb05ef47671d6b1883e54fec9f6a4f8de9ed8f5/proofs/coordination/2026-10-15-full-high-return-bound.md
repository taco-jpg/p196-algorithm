# Full high-region returns have a sharp bound of three

Integration parent: `d528a5f96773cba3f3aee88d006ff60dc946581c`.
For the decimal high region consisting of canonical pair words with every
coefficient in 9 through 18 and outside coefficient at least ten, the
[complete return theorem](../contributions/2026-10-15-full-high-return/FULL_HIGH_RETURN.md)
proves: if an actual orbit's pair word belongs to this region at times
`0,2,...,2R`, then **R<=3**. This covers all widths and replaces the tentative
five-return proposal mentioned in the preceding active-work checkpoint.
It excludes a permanent two-step high-region invariant, not later returns
after an exit or other safety mechanisms.

The exact carry-aware and nearest-nonneutral-neighbor criteria characterize
which high words return after two steps. The neutral-exterior lemma forces
the second addition to have no overflow. At width at least three, the first
three coefficients and one actual carry bit project to a finite necessary
relation with 900 states and 1,800 controls. All 258 admitted edges decrease
rank, whose maximum is three. Widths one and two admit at most one return.
The projection permits extra carry choices; it does not assume that every
graph edge or graph path is globally realizable.

The [five-theorem Lean package](../contributions/2026-10-15-high-return-rank-formal/README.md)
kernel-checks the arithmetic finite relation and all rank inequalities using
only `Std`. **The actual-orbit bridge and small-width reduction remain written
proofs**, independently reviewed. The finite graph certificate is not described
as a standalone Lean theorem about reverse-and-add. Separate generators agree
on every control and rank, and independent literal-integer and sink-deletion
checks pass. Exact roots, source hashes, complete accepted/rejected rows,
compiler logs and the failed first proof draft are retained.

The bound is attained by the canonical word `(17,9,18,9,17)`, realized by seed
80999. However, this orbit already reaches a palindrome at positive time two.
It proves sharpness for high-region membership, **not three safe returns**.
Sharpness under safety at every intermediate time remains UNKNOWN. Failed
explicit completions and their full traces are retained. The preliminary
1,111 controls are explicitly labeled recovered exact outcomes, distinct
from the original command output.

## Reciprocal reviews and the newest external gate

The [band review](../contributions/2026-10-15-external-band-review/BAND_REVIEW.md)
checks the external `60d4348` all-gap two-band and four-band formulas,
empty/zero-endpoint cases, exact trimming, and coordinatewise cycle condition.
It is source/written review, without a new graph replay. The
[three-zero exterior review](../contributions/2026-10-15-external-zero-exterior-review/REVIEW.md)
reads all twelve external theorems and three definitions at that same commit;
it does not repeat compilation. Its sharp time-four example continues the map
after an earlier palindrome and is not a safe-orbit construction.

We also read and preserve the new external
[positive gate and reset-limits checkpoint](2026-10-15-positive-gate-and-reset-limits.md)
at `d528a5f`. Its actual +4 gap regeneration gate has 29 supporting theorems
and five definitions, includes gap zero, and provides distinct target
interfaces. The nine-step family fails the proposed exact return. Its larger
mixed-band graph permits genuine regeneration but is a DAG on the stated
reachable family; the periodic quotient retains all eleven capped UNKNOWN
whole-word probes. This publication does not claim an independent rebuild or
replay of those new external results.

Our delay worker is comparing that published periodic architecture with the
nonneutral bulk cycle `2,4,8,16,14,10`; neither direction currently supplies a
valid indefinitely repeatable whole-word return. The concrete scalar 94/98
finite-table Lean instantiation remains the other active formal task. Future
shared checkpoints should compare actual carry guards and returned interfaces,
not just matching scalar clocks, widths or aggregate gap gains.

## Reproduction and evidence boundaries

Run the full-return package's `build_prefix_certificate.py`,
`independent_prefix_audit.py` and `check_explicit_witnesses.py` from the
repository root. The rank package's `generate.py` and
`lean -j1 HighReturnRank.lean` reproduce the finite kernel theorem with
Lean 4.19.0. Gzip archives retain every control and have compressed/decoded
hashes and recovery commands in the inventory. The
[root review](../contributions/2026-10-15-full-high-return-root-review.json)
pins all 30 result files. `python3 proofs/verify_release.py` checks publication
completeness and byte integrity, not mathematical validity.

No result here proves a finite infinite-safe seed or settles 196 or decimal
Lychrel existence. The shared construction work remains active.
