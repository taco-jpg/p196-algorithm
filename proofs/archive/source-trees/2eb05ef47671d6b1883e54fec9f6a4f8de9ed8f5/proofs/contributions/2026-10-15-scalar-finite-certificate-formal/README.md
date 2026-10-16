# Finite scalar hierarchy certificate — verification in progress

This package encodes the sixteen scalar jobs of the frozen component-specific certificate and supplies Lean proofs that their finite tables satisfy the local conditions needed by `ActualJobFamily.actual_path_vertices_le`. The intended endpoint is `ScalarHierarchy.finite_root_bound`: an actual scalar-root path has at most 659 vertices when the initial width is at least 14. **The full endpoint is not yet accepted: the large kernel checks and final composition remain incomplete.**

The source certificate is `../2026-10-14-component-specific-bound/component_certificates.json.gz`, SHA-256 `ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e`. Its scalar jobs contain 64,322 vertices, 106,543 edges, and 60,952 components. The other fifteen jobs in that source are outside this package's scope.

`FiniteGraph.lean` proves a finite forward simulation of the bounded one-column extension graph. Each selected parent component is represented by a member table and its inverse; a child identifier consists of nineteen coefficient choices per parent member. Coverage, field preservation, and transition rows suffice to derive `ActualPrefixLift.Realization`. They do not assume that actual paths already lift. The separately proved analytic extension supplies that fact.

`RankRows.lean` turns finite vertex and edge inequalities into the hierarchy's rank hypotheses. Components are arbitrary labels: no correctness claim about a particular strongly connected component algorithm is needed. An acyclic label has no internal edge; a cross-component edge decreases rank by at least the source component's weight. A cyclic component's weight is the child's path bound, and its child has strictly smaller remaining height.

`RangeChecks.lean` combines bounded checks into universal row statements. Generated lookup functions use balanced comparison trees. Each generated proof checks at most 128 consecutive rows using ordinary kernel reduction (`decide`), then the range lemmas combine those results. There is no `native_decide`, custom axiom, or admitted proof.

`generate_scalar_data.py` emits the tables, `generate_checks.py` emits the row proofs, and `generate_hierarchy.py` emits the concrete job routing and composition in `ScalarHierarchyData.lean` and `ScalarHierarchy.lean`. Source generation is not proof acceptance. Independent review in `../2026-10-15-scalar-finite-review/` parses the emitted Lean lookup expressions without importing these generators and compares every table to the source certificate; it also evaluates all five row predicates independently. Those checks supplement the Lean kernel.

The initial array-based pilot and its exact sources, logs, and timings are retained in `pilot-array/`. Its successful 140-vertex check took about 35.9 seconds and peaked around 2.5 GB. The equivalent balanced-lookup pilot took about 4.8 seconds and peaked around 0.6 GB. These are development measurements using existing dependency objects, not final provenance-audited acceptance records. Development job checks 0–5 also passed. The driver was interrupted during Data6 (exit 130) so that a fresh, resumable, provenance-aware build could own the final result. Its exact driver, completed-module records, and logs are retained.

The final numerical period corollaries belong to `../2026-10-15-scalar-period-composition/`. The 659-vertex endpoint would discharge their explicit root certificate hypothesis. It does not by itself assert the main P196 existence claim, an invariant for every future iteration, or an infinite nonpalindromic orbit.

## Publication checkpoint and continuation

The production run was interrupted with exit 130 during `JobData6`. Fifteen modules have retained fresh-build PASS records: `LychrelDigitSums`, `ScalarClock`, `ActualScalar`, `ScalarOrbit`, `PrefixExtension`, `ActualPrefixLift`, `FiniteGraph`, `RankRows`, `JobCatalog`, and `JobData0` through `JobData5`. No production `JobChecks` module, hierarchy composition, or combined axiom audit had completed. A partial `JobData6` artifact, if present, is not accepted.

Work is being frozen for publication at the user's request. The source drafts are preserved so another contributor can continue from the exact boundary. A generated theorem declaration is not counted as accepted merely because its proof text exists. In particular, `ScalarHierarchyData.lean`, `ScalarHierarchy.lean`, and the dependent `ScalarBound.lean` endpoint must pass the remaining build before any unconditional 659-vertex, 94-period, or 98-period result is reported.

`verify.py` creates an isolated Lean import directory and records source, object, compiler/settings, log, and direct-import hashes. It reuses a completed module only when every required fingerprint agrees; older records lacking dependency fingerprints cannot qualify. No development object enters the production build. A stopped production manifest is a checkpoint, not a successful full verification report.

For a fresh checkout, use an empty build directory and run:

```sh
python verify.py --lean /path/to/lean-4.19.0/bin/lean --build-dir /path/to/empty-build --stage checks
```

If the original build directory and its verified objects still exist, continue with the same command plus `--resume`. Reusing the retained text manifest without its matching objects is insufficient. After the `checks` stage passes, run `--stage final --resume` in that same build directory to compile the remaining hierarchy draft, actual root bridge, and scalar-period endpoint and perform the full transitive axiom audit. Any draft errors must be corrected and the affected stages rerun before acceptance. The local executable-path compatibility shim must be supplied through the environment if the host requires it; its exact hash is included in the production compiler identity.

The exact interrupted production manifest, retained source/log archive, and resume details are in [production-checkpoint/README.md](production-checkpoint/README.md).
