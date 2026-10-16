# Agent #2 overflow-fiber maximum: reproduction receipt

## Exact scope

For every natural input width `L >= 2`, the complete canonical coefficient-word overflow fiber of `Agent8.stepWord` has at most `2 ^ (L / 2 - 1)` members. The explicit target `5 :: (List.replicate (L - 1) 10 ++ [5])` attains the bound. Its next normalization equals `5 :: 0 :: (List.replicate (L - 2) 1 ++ [6])`.

`Canonical q` requires symmetry, coefficients in `0..18`, a positive outer coefficient, 和 an even center at odd input width. `ActualOverflowFiber` additionally requires exact width, computed final carry `1`, 和 the actual original `Agent8.stepWord` image.

The theorem counts coefficient words. Individual integer digit splittings, longer avoidance times, 和 an infinite orbit from 196 remain outside its scope.

Main endpoint:

```lean
P196.Agent2.OverflowFibers.actual_overflow_sharp_maximum
```

The exact-membership bridge `actualOverflowPreimages_membership` identifies the duplicate-free enumerator with the complete fiber. The bound applies to both input parities, including `L = 2` 和 `L = 3`.

## Source provenance

Proof author: Agent #2. Integration reproduction mapping 和 independent verification: Agent #11 specialist `/root/review80`.

Reviewed proof head: `302791955bf40ab34b7d702c713b2f8bf79862a0`.
Reviewed base: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.

The seven-module registry pins every source by SHA256 和 Git blob. Its `PeriodObstructions` module resolves to the preserved source `proofs/PeriodObstructions__70ce034b31b5b218.lean`, Git blob `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119`. The mapping copies those exact bytes into an isolated module path.

The original source argument remains attributed to `persist_inverse_fibers_proof.txt` at commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob `b6f07fdb79e7e1538fef75c78750f658468277c4`.

## Reproduce

Use the official Lean 4.19.0 release, commit prefix `6caaee842e94`. Set `P196_REVIEW_LEAN` to the installed Lean executable 和 `P196_REVIEW_OUTPUT` to a fresh output path. From the repository root:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent2OverflowFibers.registry.json \
  --project agent2-overflow-fibers \
  --lean "$P196_REVIEW_LEAN" \
  --output "$P196_REVIEW_OUTPUT"
```

The unchanged repository verifier checks source identities 和 the import closure, rebuilds every selected module into the fresh directory, checks the advertised endpoints, 和 audits transitive axioms for every theorem originating in the seven-module closure. The report remains explicitly scoped to `agent2-overflow-fibers`.

## Independent checks

The independent Agent #11 review rebuilt the seven exact source modules with `--trust=0`, then printed transitive axioms for all 93 new named source declarations: 81 theorems 和 12 definitions. Every invocation passed. The theorem dependency union contains only `propext`, `Classical.choice`, 和 `Quot.sound`.

A separate exhaustive module-origin audit checked 276 theorem declarations, including generated/private theorems 和 the 69-theorem dependency closure. It found the same permitted axiom union. The audit records ten compiler-generated unsafe implementation constants for list operations; none enters a theorem dependency chain.

The Lean executable SHA256 for the independent replay was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Original proof files 和 retained research logs remain unchanged by the additive reproduction mapping.
