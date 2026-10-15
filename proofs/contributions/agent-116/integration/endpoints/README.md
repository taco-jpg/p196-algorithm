# Agent 116 affected-root endpoint integration

**PASS.** Every one of the 137 accepted source hashes matches the independently reviewed fresh-build manifest and its source snapshot. The reviewed remote mathematical commit is `c0bca37913df5b52963c484ef20cbeb5b3838a32`; its observed Git tree is `22d91671e98a7c4283ee920470ec249a1c7c6c74`, the same tree as the review's local source commit `0bb18e90701b318168672e22ece8be6ae25de5b8`.

This integration execution freshly compiled `Agent116All.lean` and `EndpointAudit.lean`, with both commands exiting zero. It explicitly reused 135 byte-identical dependency objects from the independently fresh 137-module review build. It did **not** perform another full dependency rebuild. The separate review manifest records 1,991 audited theorem constants; this endpoint run checks nine exact-type aliases plus the four principal original exports.

The endpoint axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx` or `Lean.ofReduceBool` in the compiled endpoint reports. Toolchain executable, wrapper, shim-source and shim-binary hashes are pinned in `verification.json` and were checked against the independent review before execution.

The actual-orbit endpoint retains every original assumption: bounded B/A/C, valid even phase, initial exterior length at most three, both initial bands at least 18, and the exact initial pair-word template equality. Its conclusion is the growth of the **specified maximally trimmed exterior coordinate**, within nine genuine `Lychrel196.orbit` additions, with an exact resulting template representation and equality to the `outerIterate` exterior. It does not assert a palindrome hit, exit from every possible template representation, or an infinite safe orbit.

The exact aliases additionally check acceptance-only certificate obstruction, normalized/raw cap-three rejection, the valid nine-step outer bound, the unrestricted ten-step outer bound, complete base-19 encoding, and both sharp first-exit witnesses. `EndpointAudit.lean` contains the complete theorem types; `EndpointAudit.log` contains actual type and transitive axiom output.

## Artifacts

- `verification.json`: result, actual compiler commands, exit codes, source/object/toolchain hashes, original reviewed commit/tree, and endpoint axiom sets.
- `source-comparison.json`: all 137 accepted source comparisons, including the separately selected canonicality counterexample root.
- `dependency-reuse.json`: every one of the 135 reused object hashes and the explicit reuse disclosure.
- `Agent116All.log`, `EndpointAudit.log`: actual successful compiler output.
- `EndpointAudit.lean`: the nine exact endpoint aliases.
- `run_endpoint_integration.py`: the repeatable verifier; it requires the independently verified dependency directory and a new or empty scratch directory.

Original invocation:

```sh
python proofs/contributions/agent-116/integration/endpoints/run_endpoint_integration.py \
  --repo /workspace/scratch/b9ccc76d924e/p196-agent-116 \
  --review /workspace/scratch/b9ccc76d924e/review-build116/final \
  --scratch /workspace/scratch/b9ccc76d924e/integration116-endpoints \
  --lean /workspace/scratch/b9ccc76d924e/toolchain-116/lean
```

For a replay, select a different new/empty `--scratch` directory. The verifier checks the review PASS status, all source pins, allowed theorem axioms, release/shim identities, remote tree, dependency copy identities, actual zero exits, all endpoint axiom sets, and unchanged source/object hashes after execution. It refuses to present dependency reuse as a new full build.
