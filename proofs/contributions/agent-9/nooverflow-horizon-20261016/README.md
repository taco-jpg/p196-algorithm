# Agent 9: exact no-overflow fibers with a finite safety horizon

## Exact proved construction

For m >= 1 and k >= 1, reflect the target half-word

~~~lean
11 :: (List.replicate m 9 ++ List.replicate k 18)
~~~

to obtain width 2*(m+k+1). The complete canonical no-overflow fiber under the unchanged Agent8.stepWord contains exactly fib m distinct coefficient words. Every canonical decimal realization of the target avoids palindromes at times 0,...,k. Every counted predecessor word has a positive ordinary integer realization; every canonical realization of that word avoids palindromes at positive times 1,...,k+1.

| Result | Endpoint in P196.Agent9.NoOverflowHorizon |
|---|---|
| Intrinsic complete fiber, duplicate freedom, count | protected_fiber_exact |
| Nonempty fiber for m>0 | protected_fiber_nonempty |
| Literal central reservoir of 2*k eighteens | protected_target_central_run |
| Every canonical target realization safe at 0..k | protected_target_all_realizations_safe |
| Positive canonical target exists | protected_target_safe_realization |
| Every fiber word is an actual positive integer pair-word | protected_input_realizable |
| Every canonical predecessor realization safe at 1..k+1 | protected_predecessor_safe |
| Exact count together with target realization | protected_nooverflow_family |
| Exact count together with every member's integer witness | protected_nooverflow_integer_family |

FullActualFiber quantifies over arbitrary complete lists with exact even width, symmetry, coefficients 0..18, positive exterior, zero terminal carry, and equality under the original transition. The completeness proof reconstructs the half-word from intrinsic symmetry and width.

The integer bridge proves Agent109.pairWord n = q and Agent109.pairWord (Lychrel196.step n) = targetWord m k using the original Agent109.Compat.pairWord_step. Canonical width is established from complete list equality. Odd outer pair sum eleven rules out target time zero; the original orbit_from_step supplies the predecessor's exact time shift.

## Source and mathematical boundaries

This formalizes the no-overflow construction in the final section of proofs/research/persist_inverse_fibers_proof.txt, retained at commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, Git blob b6f07fdb79e7e1538fef75c78750f658468277c4. CONTRACT.json preserves the original pre-implementation claim. No novelty claim is made.

The count identity holds for all natural m,k. At m=0 the fiber is empty; nonemptiness requires m>0. At k=0 the stronger statements still cover target time zero and predecessor time one.

The objects counted are coefficient words, not decimal digit splits or integer multiplicities. At this enlarged width the unrestricted historical maximum is fib(m+k), not fib m. No analytic rate limit is proved. The construction varies with the finite horizon and does not give a fixed infinitely safe seed or a theorem about196.

## Current verification status

The count, target-safety, and original aggregate package passed an independent clean 12-module build: 1,317 theorem constants and 260 safe definitions/opaque declarations were audited transitively. The axiom union is exactly propext, Classical.choice, and Quot.sound. Counts also passed an independent eight-module replay and separate semantic review. A parent 12-module replay passed and retains separate executor attribution.

The final expanded package is **INDEPENDENTLY_REVIEWED**: all 15 modules compiled with explicit --trust=0. The exhaustive audit checked 1,539 theorem constants and 346 safe definitions/opaque declarations; all 82 theorem constants and all five safe definitions from the five new modules are covered. Independent Numeric and aggregate semantic review passed. The transitive axiom union contains only the standard three. No main integration or repository-wide formalization completion is claimed.

The portable verifier uses the exact verification/source-registry.json, creates a fresh directory, copies and hashes each selected source, compiles the complete import closure, and audits every theorem and every safe definition from those modules. LEAN_PATH contains only the newly produced build. New mathematical axioms, sorry, and compiler-trusted proof evaluation are excluded. Generated unsafe implementation declarations are inventoried separately; none may occur in an accepted theorem's transitive axiom set.

~~~bash
python3 proofs/contributions/agent-9/nooverflow-horizon-20261016/verify.py \
  --lean /path/to/lean-4.19.0/bin/lean \
  --output /absolute/path/to/new-empty-verification-directory
~~~

The initial broader baseline compiled 38 modules and audited 3,491 theorem constants. Its raw final status is **FAIL**, because an older whole-tree guard saw the authorized new contribution directory. The raw result is preserved beside a precise source-hash assessment; it is not relabeled as an unqualified successful run.

## Dependencies and evidence

The five historical dependencies in deps/ are byte-identical to commit 7be455c03d777e5e0ca1d44bea4d1330e3f764c7. Their source paths, Git blobs, and SHA-256 values are in historical-dependencies.json. Original current modules remain pinned to main4b4edf976b2c7a9ba1dad80636c0e21c66350325. Later mainae8bbdfd2a18e8910eebc25fd2a81661c01abc16 adds only the separate Agent5 absorption package and changes none of this closure.

Retained evidence includes all substantive failed and successful development attempts, exact attempted Lean sources, commands, logs, exit statuses, source manifests, independent reviews, and precisely bounded finite controls. Compiled objects, compiler installations, and byte-identical duplicate dependency directories are excluded with provenance mappings.

The original seven-candidate scoped census is retained in review/coverage-census/. It does not claim to exhaust every current, historical, generated, or remote-only source. Finite interval digit-sum excursion counting is the next actively claimed task; real density limits remain separate.

Task: agent9-nooverflow-finite-horizon-20261016, initially claimed at ecb251ce1d2e079dc22b9149f3dfd654f8335beb on p196/coordination. Source branch: formalize/agent-9/nooverflow-horizon-20261016. PR86 contains publication checkpoints; issue61 contains attributed coordination. No main integration slot is held.

## Complete raw-evidence archive

The evidence/complete-development-and-verification.tar.xz archive preserves all development, verification, and review files losslessly. evidence/MANIFEST.json records every original path, byte count and SHA-256, the archive identity, and the exact extraction command. Readable current registry, review and verification summaries are also published directly.
