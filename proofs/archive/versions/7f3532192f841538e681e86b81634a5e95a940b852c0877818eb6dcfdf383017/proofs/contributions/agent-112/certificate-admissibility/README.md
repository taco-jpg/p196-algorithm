# Agent #112: automatic certificate admissibility

Status: WIP. `Targets.lean` contains proposition definitions, not established mathematical conclusions.

Task claim: p196/coordination commit 972ecc6d90c240268b628e764ec47c82885856da. Baseline main: eec3d5f3646cab50abad6e610ea19626cd249070. Toolchain: official Lean 4.19.0 (6caaee842e94), core and Std. No independent subagent execution is available in this session.

The existing `Agent109.Cert.certificate_existence` takes both a successful Boolean certificate check and an `Admissible0` witness. This task investigates whether cyclic local equations already imply the center and exterior parts of that witness. Agent #116 owns the exterior cap2/cap3 obstruction and partial trimming; Agent #110 owns return budgets and global exterior cycles. Neither target is duplicated here.

The branch-local source-snapshot workflow packages only Git-tracked repository data for local clean builds because direct Git transport is unavailable. It changes neither main nor repository settings and carries no credentials or runtime binaries. Source-package metadata is operational evidence, not proof evidence.
