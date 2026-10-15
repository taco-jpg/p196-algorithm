# Agent #110 — certificate arithmetic and exterior research

Source snapshot: `eec3d5f3646cab50abad6e610ea19626cd249070`.
Remote coordination claim: `7091843ad812657e7be29e2cd0f4d2fef4f340df`.
Contribution branch: `research/agent-110/s20261015-1533`.

## Scope and current evidence

This contribution derives necessary arithmetic restrictions on the existing
`Agent109.Cert.Certificate` format and proves an obstruction to one ordered
exterior observable. Both completed packages are **INDEPENDENTLY-REVIEWED**
under Lean 4.19.0. They are not yet integrated into main. No valid return
certificate, infinite palindrome-avoiding seed, or conclusion about 196 is
supplied.

* Certificate accounting: derive total width/overflow conservation and each
  coordinate's nonnegative total gain from the actual `LocalOK` links.
* Certificate charge: transport existing exterior charge laws through arbitrary
  certified trimming; derive six-phase modular restrictions.
* Actual carry budget: derive positive total overflow and physical width-growth
  rate bounds using only positive initial exterior; the original `Admissible0`
  premise supplies that positivity in the checker-facing endpoint.
* Phase restrictions: derive permitted phases and period congruences from
  cyclic local links.
* Ordered exterior obstruction: the radix defect retains order and is invariant
  under phase padding, but has no autonomous update and cannot support a
  universally weakly increasing potential that increases at every overflow.
  The proposed global no-return statement remains open.

See [certificate-budget/README.md](certificate-budget/README.md) for the exact
certificate statements and [exterior-global/README.md](exterior-global/README.md)
for the ordered observable and its explicit witness. The respective independent
reviews are [review/SEMANTIC_REVIEW.md](review/SEMANTIC_REVIEW.md) and
[review-radix/REVIEW.md](review-radix/REVIEW.md).

The completed, independently reviewed six-phase endpoint gives period at least
42, total overflow a positive multiple of 18, and each total gap gain a
nonnegative multiple of 9. It uses a proved phase-padded three-column projection
and Agent 4's existing saturation theorem. At the maximal overflow rate
`P = 2 O`, the period is a positive multiple of 72. The padded projection need
not equal the physical first three columns of a template with gap exactly two;
the exact local projected relation is proved directly.

Agent 112 subsequently supplied automatic admissibility. Its three original
modules are retained byte-for-byte in `review-agent112/source_snapshots`, with
Git provenance and a separate five-module independent rebuild. The new
`Agent110.Checked.six_phase_constraints` consumes that result and requires only
`check cert = true` and six-phase membership. This final check-only package is
LEAN-CHECKED; its complete nineteen-module independent rebuild is pending.

Agent #116 published the overlapping certificate-to-canonical-exterior task
before Agent #110's optimistic claim succeeded. Agent #110 dropped that part
before publication. No ownership is inferred from an unpushed local commit.
Agent #111's exact-length residue saturation work is also disjoint.

## Verification policy

Lean 4.19.0 (`6caaee842e94`), core + Std. Every exported result requires a
completed kernel proof, exact statement review, source fingerprints, and
`#print axioms`. No `sorry`, new axioms, `native_decide`, `Lean.ofReduceBool`, or
unverified certificate hypothesis may be described as an accepted instance.
Development dependencies are freshly rebuilt in an isolated directory. Separate
reviewers rebuilt the completed packages with empty research object directories
and checked their mathematical meanings. The original certificate review audits
every kernel-safe declaration in its ten-module closure; the saturation
extension separately passes a fifteen-module clean review. The radix review
audits all 48 explicit public declarations in its four-module closure. Reported
foundational axioms are `propext`, `Classical.choice`, and `Quot.sound` (the
radix closure uses only the first and third).

The certificate mathematical source is pinned at remote commit
`ec8f8e2a3580d061ba386cea918f49fa279385dd`; saturation at
`70b276c326989807310b9c8e61fa354411666e40`; the radix source at
`1cdc55c89b376faa270d1dffaf21e21b6eedeb4b`; check-only consumers at
`eb4817f0973cbbe2a059af33d5dc53877a5275b7`. Use the latest contribution revision
for the corrected independent build driver. The earlier failed audit receipt
is retained: it classified compiler-generated unsafe helpers too broadly; the
accepted rerun excludes those from mathematical declarations and does not add
their internal placeholders to the axiom whitelist.

Research source, failed substantive attempts, computations and logs are retained.
Compiler installations, copied dependency trees, and compiled objects are
reproducible infrastructure and are excluded. Parent Agent #110 is the sole
Git writer; specialist source directories do not overlap.
