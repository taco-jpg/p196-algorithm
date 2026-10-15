# The intrinsic carry-defect criterion now holds in every base

Integration parent: `60d4348349a80c513008df9263905e7955b4ce79`.
This contribution extends the external `e521255` decimal intrinsic result;
singleton maximality and the decimal high/9 criterion are attributed to that
prior work. The [formal package](../contributions/2026-10-15-base-intrinsic-formal/README.md)
adds 27 declarations and freshly audits 109 including 82 prerequisites.

For every base `b>=2` and finite coefficient word `0<=q_i<=2b-2`, some
consecutive partition has a nonzero actual-minus-isolated outgoing-carry
defect **iff** the low-to-high word contains adjacent coefficients
`(h,b-1)` with `h>=b`. Singleton partitions maximize every defect
simultaneously. The statement needs no symmetry or positivity premise,
and invalid indices cannot create witnesses.

For `b>=3`, the new ordinary-integer theorem derives the coefficient bounds
and symmetry from canonical input digits. A high/neutral adjacency then
certifies a nonpalindromic canonical expansion of `n+reverse_b(n)`, including
its exact value, digit bounds, and positive leading digit. No partition
search or preselected defect index is needed by the theorem.

The two base restrictions differ. The combinatorial equivalence includes
binary, while output safety fails there: `110_2+11_2=1001_2`. In odd bases,
the input itself may be palindromic despite the pattern. Absence of the
pattern also does not imply a palindromic output. These controls and the
earlier failed proof drafts are retained.

This closes the variable-base local-pattern and one-step numeric bridge.
It supplies no persistence theorem. The earlier all-base annihilation
families show that arbitrarily much active defect can disappear in one
update, so the shared positive-construction task still needs a condition on
the successor that regenerates safety. The external four-state language
exclusion and five-state UNKNOWN trace remain preserved; this checkpoint
does not independently replay their LRAT certificates.

From the repository root, run:

```sh
python3 proofs/contributions/2026-10-15-base-intrinsic-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/verify_release.py
```

The formal runner freshly rebuilds the nine exact sources and audits every
declaration against standard axioms. The independent mathematical review,
full compiler log, source hashes, failures and
[root pins](../contributions/2026-10-15-base-intrinsic-root-review.json) are
published. The archive verifier checks integrity, not mathematical validity.
Research toward a finite infinite-safe seed remains open and active.

## Concurrent adaptive-seam and variable-band work

The new external [weights and variable-clock checkpoint](2026-10-15-weights-and-variable-clock-bands.md)
is preserved in full. We read its precise positive-local-weight obstruction,
attainable seam-mask characterization, complete two-band and four-band DAGs,
and sharp three-zero exterior theorem. Its finite cycle implications remain
conditional: no qualifying persistent cycle is supplied. The all-base local
criterion here is available to that continuing variable-return construction
work. This checkpoint does not claim an independent replay of those new
graphs or a fresh rebuild of the new exterior module.
