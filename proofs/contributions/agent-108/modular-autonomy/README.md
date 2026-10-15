# Agent #108 — exact modular autonomy

## Mathematical result

For every positive modulus `M`, the following are equivalent:

1. Beyond one finite width threshold, the residue of ordinary `reverse10 n` is determined by `n mod M` and the exact decimal width of positive `n`.
2. The same eventual determinism holds for the actual reverse-and-add step `n + reverse10 n`.
3. `M` divides `99`.

The final equivalences are `ModularAutonomy.eventual_reverse_residue_determinism_iff` and `ModularAutonomy.eventual_step_residue_determinism_iff` in `ModularAutonomy.lean`. The previously written necessity from `proofs/research/astra_modular_fixed_modulus_theorem.md` section 6 is now formally proved. Sufficiency reuses `AstraModular.reverse10_mod_of_dvd99` from the integrated research source (the old sidecar calls its namespace `DecimalModular`). No mathematical discovery priority is claimed.

A stronger quantitative endpoint is proved in `CounterexampleBound.lean`: for any **single** width `L >= 3` satisfying `M + 10 < 10^(L-1)`, determinism on that exact width is equivalent to `M | 99`. Thus every excluded modulus has same-width, same-residue finite integer inputs with different next-step residues at **each** width satisfying this explicit bound. The bound is sufficient, not asserted optimal.

The central statements are about all finite positive decimal inputs at a width. They do not assert a palindrome-free invariant, rule out every invariant using modular information, or settle the orbit of 196. Extra digit state or width-varying moduli are outside this classification.

## Proof structure

- `AutonomyDefs.lean`: exact predicates, with a uniform eventual threshold.
- `AutonomyBasic.lean`: the existing sufficiency branch and equivalence of reversal/step determinism.
- `DigitPerturbation.lean`: actual canonical digit increments, including the single-trailing-nine carry case.
- `LeadingWitness.lean`: constructs equal-width multiples of M with leading digits one and two; rules out factors two and five.
- `Necessity.lean`: compares two actual neighboring pairs, derives `M | 99 * 10^k`, then cancels the power using coprimality.
- `ModularAutonomy.lean`: full classification and arbitrarily wide actual-step counterexamples.
- `CounterexampleBound.lean`: the fixed-width quantitative strengthening and counterexamples at every admissible width.

## Verification status

**INDEPENDENTLY-REVIEWED.** All seven new modules compiled under Lean 4.19.0. A separate reviewer completed a source-clean rebuild, semantic review, and exhaustive theorem dependency audit; see `review/clean/REVIEW.md`. The 39 explicitly written theorems and all 146 exported contribution theorem constants (including generated auxiliaries), together with the complete local foundation, use only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, new logical axiom, `native_decide`, or compiler-trusted reduction is used in the accepted chain. Counts are audit coverage, not independent major-result counts. No default-branch integration is claimed.

The adapter-free official GitHub build also **PASSED** at source commit `671dfbdd436a17155bc56d428c6fe78a550fabe2`: [run 38684866203](https://github.com/taco-jpg/p196-algorithm/actions/runs/38684866203). It began with zero old oleans and rebuilt the foundation and all seven modules together. Every compilation, dynamic transitive audit, and actual `#print axioms` command exited 0. Downloaded full reports are retained under `review/clean/github-official-20261015T050512Z-0fbdb2fc/`; `review/HOSTED_VERIFICATION.json` pins the run, source commit and downloaded archive hash.

`SOURCE_MANIFEST.json` pins all seven source hashes and the exact existing dependency. The complete accepted build entry point includes every module:

```sh
python3 proofs/contributions/agent-108/modular-autonomy/verify.py   /absolute/path/to/lean-4.19.0-linux/bin/lean   --build-root /absolute/path/to/disposable-build
```

This always uses a fresh build directory and recompiles the original research dependency. A nonzero exit is failure. `review/clean/` retains command vectors, exact exit codes, full logs, toolchain/source hashes, exported-theorem inventories and transitive axiom checks. `development/` retains failed attempts outside the accepted build. Compiler-generated unsafe specialization declarations are recorded separately from logical proof dependencies; every theorem's transitive axioms must still belong to the three-element allowlist.

## Runtime and independent evidence

The local container has a PID namespace inconsistent with its `/proc` mount. Local execution uses the unchanged official Lean distribution plus the retained `runtime/proc_self_readlink.c` adapter, which redirects only the current process's own numeric exe path to `/proc/self/exe`. No Lean kernel, library, source or olean bytes are patched. This is an additional runtime component, explicitly reported rather than called unadapted execution. Add `--preload /absolute/path/to/libproc_self_readlink.so` only in this environment. The source compiles with `gcc -shared -fPIC -o libproc_self_readlink.so proc_self_readlink.c -ldl`.

The contribution-branch GitHub workflow repeats the complete build using the checksum-pinned official distribution without this adapter. Its successful run and downloaded audit evidence are recorded above; this is actual execution, not a proposed workflow or inferred result.

An independent semantic reviewer read and recompiled the six core modules (reusing a hash-matched base olean), recorded actual exits in `review/compile-check.json`, and checked the Canonical, width, carry, arithmetic and quantifier meanings. That reviewer reached an execution usage limit before producing a concluding prose report. The separately assigned clean reviewer completed the full source rebuild, quantitative extension audit and mathematical review, and wrote `review/clean/REVIEW.md`. These scopes are distinct and neither is described as external human peer review. The reviewer's workflow-proposal file is historical; root separately installed and successfully ran the actual workflow.

## Coordination and preservation

Task: `agent108-modular-autonomy`, remotely claimed at `d16c60a52c516a531084881ee503c43633fbfc89`. Contribution branch: `research/agent-108/s20261015-0442`. Root Agent #108 is the only Git writer. The earlier local, unpublished normalization proposal reserved nothing and was abandoned when Agent #109 published ownership.

All substantive new source, proof attempts, failure logs, runtime diagnostics and verification evidence are retained. Compiled objects, runtime binary copies, cache files and duplicate disposable build trees are reproducible infrastructure and are excluded. Shared default-branch indexes are reserved for the integration owner; this package does not silently promote older evidence labels.
