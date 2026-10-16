# Repeated-block normalization: author evidence

Author: genuine Agent #1 specialist `symbolic_scope`.
Claim: `2cb89418916f1d0a22813028d5fea623e80900ad` on coordination, with publication receipt https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224749698 .

Source: `proofs/Agent1RepeatedBlock.lean`.
SHA-256: `4dc552677e5b7f1484fa2c765378bae02236033a4c5d42858f84b258a9f30d12`.
Git blob: `4adf4bd714be87ef5d95f0e6d33632fe36075ca4`.
Parent Agent #1 owns Git publication and the separate context module.

The source proves an exact list-to-indexed-carry bridge, idempotence of bounded block carry transfer, and exact terminal carry, fixed-digit, and full normalization formulas for every positive repetition count. It reuses the original `IncomingCarry.carryIn_transfer_trichotomy` and `Agent8.fixedDigits_append`. Incoming carry is a bit and block coefficients are at most 18. The empty block and all-nine identity-transfer block are included. The first copy's normalized digits may differ from subsequent copies; the theorem retains that transient explicitly.

## Actual verification

All five exact dependency modules built freshly in the author's isolated build directory. Attempt 001 failed only at a `change` using `1 + xs.length` instead of the definitionally matching `xs.length + 1`; its complete source and output remain in `attempt-001/`. Lean's generated `sorryAx` diagnostics in that failed attempt are retained as failure evidence and are not part of the accepted source chain. No source `sorry` or `admit` was introduced.

Attempt 002 succeeded. The final source was then replayed from a new, empty build directory with **`lean --trust=0` for all six modules**, including the five dependencies. All six exited zero. `clean-001/` stores exact source hashes, command/exit/timing records, complete logs, and the five literal theorem-axiom prints. The axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. There are no new axioms, `sorryAx`, or `Lean.ofReduceBool` dependencies in the final exports.

These are author checks. Independent fresh replay and semantic review are separate obligations handled by the parent; this directory does not claim them completed.

## Reproduce

From the repository root, choose a build directory and evidence directory that do not already exist:

```sh
python3 proofs/contributions/agent-1/repeated-block-20261016/author/replay.py \
  --build-dir /tmp/p196-repeated-block-fresh \
  --evidence-dir /tmp/p196-repeated-block-evidence \
  --lean /path/to/lean-4.19.0-linux/bin/lean
```

The replay script verifies every dependency and new source against pinned SHA-256 values before compiling. It stages unchanged sources under their original logical module names, uses a fresh `LEAN_PATH`, preserves command failures, and checks that all five explicit axiom reports contain only the standard whitelist. It does not mutate repository sources or use preexisting project `.olean` files.

This interface supports the normalization portion of the preserved periodic guard-period argument. It does not establish its complete mirrored-pair extraction theorem, a safe return cycle, an infinite ordinary integer orbit, decimal Lychrel existence, or a result about 196.
