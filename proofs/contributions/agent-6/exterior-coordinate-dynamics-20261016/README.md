# Agent 6: exact exterior coordinate dynamics

Base source: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
Task claim: coordination commit `1b3935d7f0ad6aaff290a9c8baa883f60d572434`.

## First checked checkpoint: overflow threshold

`CoordinateThreshold.lean` proves that the actual right-end normalization carry equals `rhoNum c B / (9 * 10^B.length)` exactly for phases `c <= 17` with `c != 9`. The phase condition is also necessary for the identity to hold for every finite word. The zero-carry threshold needs no coefficient bound. Interpreting every positive carry as one requires coefficients at most 18; a checked counterexample retains that boundary. Empty words are included.

The unchanged definitions and normalization semantics belong to Agents 7 and 115. This contribution imports their existing results; it does not rename or re-prove the earlier factorization theorem. The first author build and all sixteen exported axiom reports pass under Lean 4.19.0 with `--trust=0`. The foundational axiom union is `propext`, `Classical.choice`, `Quot.sound`. Independent new-source review is in progress. Failed development source and compiler logs are retained separately.

## Reproduce the scoped build

From a repository checkout, with the official Lean 4.19.0 executable (commit `6caaee842e94`):

```sh
python3 proofs/verify_project__214bf7673efe116b.py --lean /absolute/path/to/lean --registry proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016/threshold.registry.json --project agent6-coordinate-threshold --output /absolute/new/output/directory
```

The source-pinned registry includes the complete four-module import closure and every new exported theorem. It does not modify the global accepted registry. The existing verifier retains its original Agent 1 field; actual executor identity belongs in the accompanying run receipt.

## Next active work

Derive the signed beta-coordinate increment and finite-chain telescope from Agent 115's preserved `ExteriorUpdateLaw.lean` at `fba03a902e0f6b198cbf8f42efa8d11f8f2ba7a6`, blob `db2f3c5ea38b8d49ef7da82631b2ed7a95a29bea`. That original update law was independently reviewed by Agent 113 at `7f7afcd799b9a6363be7a4ecb317b1557df3ab4b`. New work remains explicitly WIP until its own proof and audit complete.

No exterior cycle, safe return certificate, infinite ordinary integer orbit, or conclusion about 196 is supplied by this local threshold theorem.
