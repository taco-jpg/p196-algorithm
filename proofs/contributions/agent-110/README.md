# Agent #110 — certificate arithmetic and exterior research

Source snapshot: `eec3d5f3646cab50abad6e610ea19626cd249070`.
Remote coordination claim: `7091843ad812657e7be29e2cd0f4d2fef4f340df`.
Contribution branch: `research/agent-110/s20261015-1533`.

## Scope and current evidence

This contribution develops necessary arithmetic restrictions on the existing
`Agent109.Cert.Certificate` format, rather than postulating the numerical
restrictions as assumptions. The initial tasks are WIP. No new mathematical
result is established by this README, no valid return certificate is supplied,
and no conclusion about 196 or decimal Lychrel existence follows.

* Certificate accounting: derive total width/overflow conservation and each
  coordinate's nonnegative total gain from the actual `LocalOK` links.
* Certificate charge: transport existing exterior charge laws through arbitrary
  certified trimming; derive six-phase modular restrictions.
* Actual carry budget: derive positive total overflow and physical width-growth
  rate bounds using a canonical starting state.
* Phase restrictions: derive permitted phases and period congruences from
  cyclic local links.
* Global exterior investigation: seek an order-sensitive all-width obstruction
  or a genuine return counterexample. The proposed global no-return statement
  is an open target, not an accepted theorem.

Agent #116 published the overlapping certificate-to-canonical-exterior task
before Agent #110's optimistic claim succeeded. Agent #110 dropped that part
before publication. No ownership is inferred from an unpushed local commit.
Agent #111's exact-length residue saturation work is also disjoint.

## Verification policy

Lean 4.19.0 (`6caaee842e94`), core + Std. Every exported result requires a
completed kernel proof, exact statement review, source fingerprints, and
`#print axioms`. No `sorry`, new axioms, `native_decide`, `Lean.ofReduceBool`, or
unverified certificate hypothesis may be described as an accepted instance.
Development dependencies are freshly rebuilt in an isolated directory; a
separate reviewer will rebuild final sources with empty research objects.

Research source, failed substantive attempts, computations and logs are retained.
Compiler installations, copied dependency trees, and compiled objects are
reproducible infrastructure and are excluded. Parent Agent #110 is the sole
Git writer; specialist source directories do not overlap.
