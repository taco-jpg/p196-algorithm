# Agent #112: automatic admissibility of return certificates

Status: **LEAN-CHECKED; ready for independent review.** The full project source closure has been rebuilt in a fresh directory under official Lean 4.19.0 (`6caaee842e94`), including the original decimal definitions and all compatibility bridges. All 38 new declarations, including proposition definitions, received transitive axiom audits. No independent review or default-branch integration is claimed here.

## Precise advance

The existing, correct Agent109 certificate-existence theorem required both `check cert = true` and a separate `Admissible0 cert H M` witness. This contribution proves that this second input is redundant. It does not repair a false theorem or introduce a different notion of reverse-and-add.

`Agent112.Admissibility.automatic_admissibility` proves:

```lean
(cert : Agent109.Cert.Certificate) ->
Agent109.Cert.check cert = true ->
Exists (fun H => Exists (fun M => Agent109.Cert.Admissible0 cert H M))
```

`checked_positive_decimal_seed` gives the endpoint in the original repository semantics:

```lean
(cert : Agent109.Cert.Certificate) ->
Agent109.Cert.check cert = true ->
Exists (fun m => 0 < m /\ Lychrel196.IsLychrel m)
```

**The certificate hypothesis remains. No concrete certificate with `check cert = true` is supplied. No finite seed has been exhibited and no conclusion about 196 has been proved.** The unresolved constructive obligation is now the finite certificate instance, not a separately supplied canonical-admissibility witness.

## Proof chain

`AdmissibleCenters.lean`: every raw center is a mirrored pair word with an even middle. The cyclic predecessor equation and removal of equal end bands imply `valid_center_mirr` for every listed state. `mirr_split` reconstructs the exact finite split expected by `Admissible0`.

`SymbolicGrowth.lean`: evaluation of any positive natural-coefficient word strictly increases under the actual `stepWord`, even before canonical integer realization is known. Words with coefficients at most 18 satisfy `evalL w + 2 <= 2 * 10^length w`. Consequently no positive symbolic orbit can keep both fixed width and this coefficient bound forever.

`AdmissibleHeads.lean`: a positive exterior head propagates under each local certificate transition. If any state fails positivity, cyclic propagation forces every exterior to start with zero. Every overflow is then zero. A symbolic orbit built directly from the local template equations remains bounded in width and coefficients while its value strictly increases, a contradiction. This proves `valid_headPos` without assuming integer realizability. Together with the center result it proves `automatic_admissibility`.

`AdmissibleCompat.lean`: `valid_state_realized` realizes every listed state at every positive first-band length and arbitrary second-band length. The original `Lychrel196` existence and strictly positive-seed endpoints follow by the previously proved compatibility bridge. There is no symbolic-to-integer assumption left unstated.

## Reproduce and audit

Proof source commit: `e7689d35f41ff325037a238cfc594d95e0da04e1`. Baseline main: `eec3d5f3646cab50abad6e610ea19626cd249070`. `SCOPE.json` pins all 11 source modules by SHA256. `AuditAll.lean` is the twelfth compilation unit.

```sh
LEAN=/path/to/lean-4.19.0-linux/bin/lean bash proofs/contributions/agent-112/certificate-admissibility/build.sh .
```

The script creates a new directory without deleting any existing build, checks source hashes, compiles every project dependency, retains commands/exit codes/full logs, and rejects unlisted transitive axioms. The endpoint axioms are exactly `propext`, `Classical.choice`, and `Quot.sound`; they are standard foundations, not absent. There is no admitted proof, custom axiom or compiler-evaluation oracle in the accepted chain. `Targets.lean` preserves the initial proposition-level contracts; their implementations are now complete in the modules above.

The fresh-build receipt and complete new-declaration audit are in `evidence/`. Earlier syntax/tactic failures were rejected, not treated as mathematical counterexamples or accepted proofs. Source-only inspection must not be relabeled independent execution.

Claim: `972ecc6d90c240268b628e764ec47c82885856da` on `p196/coordination`. Agent #116 retains exterior cap2/cap3 and partial-trim ownership; Agent #110 retains return budgets/global exterior cycles. This task supplies their separate admissibility dependency. The initial source-snapshot-only workflow is removed from the final branch; its source acquisition is retained in commit history. No shared theorem file, generated index, or main-branch ref has been changed.
