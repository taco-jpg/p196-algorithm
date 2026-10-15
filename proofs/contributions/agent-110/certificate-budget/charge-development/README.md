# Certificate charge development

`CertificateCharge.lean` connects Agent109's certificate checker directly to
Agent2Exterior's charge invariant. The normalization and raw exterior
definitions are proved compatible. Trimming need not be maximal: appending
any number of copies of the current phase leaves exterior charge unchanged.

The closed certificate result requires `Valid cert` (or `check cert = true`)
and `SixPhase (cert.st 0).c`. It proves the actual carry total is zero modulo
nine. A separate interface clock proves that the total `j1` and `j2` trims
have the same residue modulo nine. It does not assume a realizable ordinary
integer or the existence of an accepted certificate.

The interface calculation uses both normalizations of A, including their
different incoming carries. It proves `Ar.sum % 9 = (2*A.sum) % 9`, then
telescopes `inv9(c)*A.sum` around the certificate.

## Development evidence

- `attempt01.log`: rejected use of unavailable `List.sum_replicate`.
- `attempt02.log`: rejected `rfl` for the zero case of a replacement lemma.
- `attempt03.log`: successful charge compatibility and carry-count proof.
- `attempt04.log`: successful interface mass and cyclic trim-difference proof.
- `final.log`: complete checked source, including Boolean-checker wrappers.

The failed logs are retained as development evidence. Their `sorryAx`
reports are Lean's diagnostic placeholders following errors, not admitted
terms in the final source. The final source has no proof placeholders.

Compile from the repository root with the pinned Lean 4.19 runtime:

```sh
LEAN_PATH=/workspace/scratch/63e10b24caf2/dev-deps \
  /workspace/scratch/63e10b24caf2/runtime-audit/lean \
  proofs/contributions/agent-110/certificate-budget/CertificateCharge.lean
```

Every exported definition or theorem is covered by a `#print axioms` query.
The final report contains only Lean's standard `propext`, `Quot.sound`, and
`Classical.choice` axioms. No new axiom or native evaluation is introduced.
