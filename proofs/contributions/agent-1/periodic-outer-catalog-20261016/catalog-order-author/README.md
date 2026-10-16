# Linear catalog order certificate: author evidence

Canonical source: `/workspace/p196-agent1-outer-20261016/proofs/Agent1PeriodicCatalogOrder.lean`.

Successful source and object: `attempt-003/Agent1PeriodicCatalogOrder.{lean,olean}`. Exact reproducible invocation, explicit `LEAN_PATH`, and 1,843,200,000-byte address-space limit are in `attempt-003/command.py` and `command.json`; compiler output is in `compile.log`. Lean 4.19.0 ran with `--trust=0 -j1 -DElab.async=false`. Exit code 0; elapsed 0.1696 seconds; maximum resident set 443,560 KiB. `#print axioms` reports only `propext` and `Quot.sound` for the public Nodup helpers, and `propext` for adjacency soundness.

The helper defines `catalogOrderKey`, `strictNatKeysFrom`, and `strictNatKeys`. It exports `strictNatKeys_pairwise`, generic `nodup_of_strictNatKeys`, and specialized `outerCatalog_nodup_of_checked`. Increasing keys imply distinct original values without an injectivity or boundedness premise. No native evaluation, new axioms, or admitted proof is used in the passing source.

Typical catalog integration:

```lean
import Agent1PeriodicCatalogOrder
-- Existing literal outerCatalog retained.
theorem outerCatalog_nodup : outerCatalog.Nodup :=
  outerCatalog_nodup_of_checked outerCatalog (by decide)
```

This author check validates helper soundness; the actual 878-node closed check belongs to the root-owned catalog module and was not run by this specialist.

All attempts retained:
- `attempt-001`: command-launch failure, exit 127, because `/usr/bin/time` is unavailable; Lean was not started.
- `attempt-002`: failed elaboration, exit 1, from tuple/lambda parsing and the Boolean lemma name; its emitted `sorryAx` diagnostic belongs only to this rejected attempt.
- `attempt-003`: corrected source, strict compiler exit 0, no excluded axioms.

Only the new authorized canonical helper and this evidence directory were written. No existing repository source, Git metadata, or external service was changed by this specialist. Dependency and artifact hashes are recorded in `manifest.json`.
