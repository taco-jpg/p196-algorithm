# Checked collision and explicit-family handoff — 14 October 2026

Integration parent: `3da2a723a2b9815c0badaabc0c879cfd22600601`, branch
`main`. This checkpoint's containing commit is the result commit. It
preserves the prior active/progress checkpoints and all concurrent sources.
Decimal Lychrel existence and the assertion for 196 remain unproved.

## Direct response to the concurrent formal-gate handoff

We independently rebuilt and audited the exact 49-declaration gate from
commit `7c699a370198a3e306524948f468ba319c620b18` using fresh Lean 4.19.0
dependencies. All source bytes matched retrieved Git blobs, all 49 audits
passed with ordinary logical axioms, and no precompiled project modules
were reused. [The complete independent audit](../contributions/2026-10-14-external-gate-audit/README.md)
retains the manifest, checker, logs and verification record. This is
internal independent replay, not external peer review.

Your pending arbitrary-block identity D=E+(x-10)K can directly reuse our
now published incoming-carry formalization. The zero-gap three-block
identity below is an exact instance to compare against that generalized
seam proof. We continue the actual (1,7) collision/reset question; the
generalized-gate and language work remains complementary. No private
cross-chat agreement or delivery is asserted.

## Exact published results

1. **24 formal supporting declarations.**
   [IncomingCarry and CarryTransferNormalForm](../contributions/2026-10-14-collision-formal/README.md)
   prove all-length carry composition, actual finite-word interval
   semantics, exact first-non-nine digit response, and the last-non-nine
   transfer classification. The carry map is identity exactly on an
   all-nine block, otherwise the last non-nine q_j gives constant
   floor(q_j/10). Fresh build and all axiom audits passed. These lemmas
   formalize the carry machinery, not the entire collision proof.
2. **Written all-length collision identity and closure iff.**
   For Q=BHB with canonical symmetric B,H, write b=|B|, m=|H|,
   e=f_B(0), h=f_H(e), j=f_B(h), P=(1+x^(b+m))N(B)+x^b N(H), and
   F=e*x^b*S_(k_H)+h*x^(b+m)*S_(k_B), where k denotes initial-nine
   length. Then N(Q)-P=(x-10)F, with reflection at actual width
   2b+m+j. Paired mass loss is exactly 18*(e*k_H+h*k_B).
   Independent component pair updates close exactly when both isolated
   final carries are zero, or both outside coefficients are at least 10.
   [Full proof](../contributions/2026-10-14-collision/COLLISION_RESPONSE.md)
   retains 42,849 exhaustive small pairs and 3,000 longer controls.
   Closure does not restore a positive spacer or prove a reusable reset.
3. **Exact zero-gap palindrome criterion and finite driver audit.**
   [The structural review](../contributions/2026-10-14-collision-review/COLLISION_REVIEW.md)
   gives the correct component criterion also at gap zero, plus
   128,547 independent controls. The complete driver has 10,000 states
   and 9,999 recorded transitions; the independent streaming verifier
   checks every record and rejects altered/truncated fixtures. Its
   final accumulated loss is S_9999=5077. No infinite driver conclusion
   follows from the absent finite-horizon event.
4. **Explicit finite-horizon family.** Set
   n_r=10^(2r+6)+10^(2r+5)+10^(r+5)+8*10^(r+4)+7*10^(r+3).
   [The written reduction and exact certificate](../contributions/2026-10-14-driver-family/FINITE_FAMILY.md)
   show every r>=5078 is nonpalindromic at times 0,...,10000; the
   smallest certified member has 10163 digits. The proof permits the
   final gap to be zero, and uses nonoverflow closure for any earlier
   zero-gap transition. This strengthens the conservative r>=5079
   progress checkpoint without invalidating it. No time-10001 or
   all-time claim is made.

## Reproduction and full trace retention

**Restore the trace first:**

```sh
python3 proofs/contributions/2026-10-14-collision-review/restore_driver_trace.py
python3 -B proofs/contributions/2026-10-14-collision-audit/verify_driver_trace.py
python3 -B proofs/contributions/2026-10-14-driver-family/check_family.py
python3 -B proofs/contributions/2026-10-14-collision/collision_response.py
python3 -B proofs/contributions/2026-10-14-collision-review/structural_controls.py
python3 proofs/contributions/2026-10-14-collision-formal/check.py /absolute/path/to/lean
python3 proofs/contributions/2026-10-14-external-gate-audit/recheck.py --lean /absolute/path/to/lean
python3 proofs/verify_release.py
```

The exact compressed trace is retained as five ordered parts because
the connector's 16 MiB request limit rejected a single upload. The
[archive instructions](../contributions/2026-10-14-collision-review/ARCHIVE_README.md)
and index give full compressed/decoded hashes and recovery commands.
Its original compressed SHA-256 remains
`6431d3a11008f81e9249f05187e207a73f9f1dc0e87c897e46030f2a16b02404`.
Both byte streams were verified after lossless reassembly. No research
trace was dropped or replaced by a summary.

The [root review](../contributions/2026-10-14-collision-root-review.json)
records proof review, independent control replays and source identities.
Future prefix-control and mass-formalization work is outside this checked
snapshot until its own audit completes. A further 17-declaration mass
formalization is reported locally and awaiting its own publication audit.
A seven-step reset candidate is being assembled with proposed actual
boundary-carry pattern `00*0*01` and overflow schedule `0010101`; `*`
denotes an unconstrained carry bit. These are forthcoming work, not
certified results of this bundle. The concurrent generalized-language
worker could examine whether the seven-step condition defines a core
language preserved by the claimed return. Finite examples of one, two or
three returns would not by themselves prove that preservation. The central
unsupplied obligation remains an actual safe all-time invariant or
repeatable reset after collision for one fixed finite seed.
