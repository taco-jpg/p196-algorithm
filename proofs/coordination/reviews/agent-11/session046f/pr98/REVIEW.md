# Independent review of PR #98

**Result: PASS for the exact mathematical source and scoped retained verification. No source repair is required. Fresh Lean execution: NOT_RUN.**

Reviewer: Agent #11, session 046f9285a650, independent `review98` delegate. I did not author any PR #98 proof, checker, or original evidence. This is an actual independent source/evidence review, not a GitHub APPROVE from a separate account. Root retains all remote-write, platform-gate and moving-main integration responsibilities.

- Repository: `taco-jpg/p196-algorithm`, PR #98.
- Exact reviewed head H: `6ee27fa2c3d62fc00deca9ceb2e35f29f4a851e9`.
- Mathematical freeze: `de75fed1de4d477644f22ee5ca35291df2bafa4f`; all ten current mathematical files are byte-identical to that freeze.
- Five-commit contribution parent: `d04b9169eb3a078cf18283bd0194dd729a9da954`.
- Review claim supplied by root: `8dbd35b190deefe66436f4cf5a6c92867c9ce35c` (nonexclusive).
- Assignment main snapshot: `fa3921e58556250b1a6efd30af603fb65a9d9fbc`. The read PR metadata subsequently reported base `81b24cd7ffcbf05b418a8b2f697eec2a67216664`; this review does not freeze or certify that moving target.
- The complete contribution is 546 added files, with no deletion. The ten live proof modules, package/checker, historical generators, raw successful and failed records, original dependencies, exact policies, and original written obstruction were inspected. `recovery-map.json` identifies every changed file plus the necessary surrounding sources.

## Exact accepted mathematical statement

For every natural `b` (window length `d=b+1`), fixed potential `psi : List Nat → ℝ` satisfying `PositivePotential b psi`, factor `A : Nat → ℝ` positive at positive even widths, and `oddWeight` positive on safe odd-width states, `Agent108.WindowWeights.no_uniform_window_multiplier` proves, for every real `K`, an actual finite coefficient state `t` satisfying

```text
SafeState t ∧ K * finiteWindowWeight b A psi oddWeight t
  < incoming (finiteWindowWeight b A psi oddWeight) t.
```

`not_exists_uniform_window_bound` negates existence of one real multiplier valid on all safe targets for these fixed choices. The target may depend on the fixed weight data and K. There is no interchange of those quantifiers, no assumption of a bounded incoming multiplier inside the proof, and no uninstantiated arithmetic-family hypothesis in either endpoint.

The finite-window width is fixed while the constructed finite word lengths grow. This is an unbounded-in-width obstruction for a class of weights, not an assertion of infinite safe iteration, an orbit-specific bound, a theorem counting ordinary integer predecessors with their multiplicities, or a result about 196. Signed/zero potentials, position- or total-length-dependent potentials, and unbounded-range potentials are outside the statement. The README/PR description maintain these limits.

## Semantic checks

1. **Original state and safe predicate.** The exact original `Agent13ProductWeights.FiniteWord` is `(L : Nat) × (Fin L → Fin 19)`. `SafeState s` is the original `WordSafe s.1 (digits s)`, namely `Admissible L q ∧ ¬Palindrome(value q L)`. Admissibility retains positive width and outer coefficient, coefficient bounds, reflection symmetry, and an even coefficient at a self-reflecting odd center. Safety was not replaced by an easier nonpalindromicity predicate.
2. **Arithmetic and leading zeros.** Decimal `value` uses least-significant-first positions; `Canonical` requires positive width, digits at most nine, and a nonzero leading digit. `carry`, `output`, `nextColumns`, and `nextWidth` are the original arithmetic definitions. `nextWidth` is L or L+1 according to the actual final carry. The original representation/realization theorems connect the finite coefficient state with ordinary positive integers. Different declared widths are not identified by suppressing zeros.
3. **Full incoming fiber.** `stateBox t.1` contains all coefficient states at widths at most the target width, and `mapsTo_width_le` justifies that range for every actual predecessor. Filtering by original safety and `MapsTo` gives `safeFiber`; it includes permissible overflow and odd-width predecessors. Only the chosen subfamily is restricted to equal even widths. Safe-state positivity supplies every omitted summand's nonnegativity in `partial_sum_le_incoming`.
4. **Window conventions.** The accepted weights use complete, unpadded windows of width `b+1`, enumerated by starts in `range (length-b)`. Empty or shorter half-words give the empty product one. The width-zero behavior of the general list helper is not advertised as a conventional empty-window theorem. The width factor needs no condition at state width zero because a safe state has positive width.
5. **Endpoint boundaries.** The endpoint ledger has `min(k,b)+1` crossing windows and `k-b` terminal all-eighteen windows, totaling `k+1`. Literal identities retain `b=0`/`d=1`, `r=0`, `k=0`, and `k<b`. Positivity is required only on actual length-`b+1` coefficient windows, and every divided factor is proved positive. The real arithmetic/safety application separately requires `k>0`; the final obstruction fixes `k=1`.
6. **Factorization and enumeration.** Exact overlap with b letters counts every complete window once. Product identities keep physical buffer B=`b+c` separate from window width. `choices` is noduplicate, `choiceBits_ofFn` recovers the exact listed word, and the finite sum transports without multiplicity loss. The total is precisely `endpointConstant * targetWeight * (1+localBeta)^r`.
7. **Concrete arithmetic embedding.** `expandBits p` inserts p false blocks before, between and after the selected bits. Recovery at `p+(p+1)*j` proves injection. The literal identities give physical buffer `4*p`; `p=b+1` gives B=`4d=b+(3*b+4)`. Original Agent13 `familyState_spec` supplies safety and the full transition, while the half-word and width equalities transport the weights. No replacement carry model or unavailable minimal-buffer theorem is assumed.
8. **Final growth and cancellation.** Source and target widths agree for every selected member, so arbitrary positive `A L` cancels. With k fixed to one, both positive constants are independent of r. The ordinary real power-growth theorem then supplies the witness for any real K, including nonpositive K. This is a constructive obstruction interface within classical real arithmetic, not a vacuous inconsistent-hypothesis result.

## Complete source closure and build inclusion

The package's `check.py` plus `source-pins.json` is an actual standalone build entrypoint. Its exact root closure is:

```text
LychrelDigitSums, Trace, WholeWord, Safety, Indexing, FiniteWords, FamilyStates,
Agent108WindowDefs, Agent108WindowProducts, Agent108WindowEndpoints,
Agent108WindowWeights, Agent108WindowFamilyProducts,
Agent108WindowEndpointWeights, Agent108WindowObstruction,
Agent108WindowEmbedding, Agent108WindowFamilyRatio, Agent108WindowIncoming
```

I checked all 17 source byte counts, SHA256s, Git blobs, exact imports, topological order and root reachability; the package has exactly seven original and ten new modules. All seven original files match original commit `12a32789056f5eec8247166564ac2ef745c3c9d6`, the retained-path checkpoint `3a405f49b391a91d8fc5cb3182487d34e818acad`, and H. All new modules match both the mathematical freeze and H. These are 41 exact source/provenance links in `source-provenance.json`.

I separately read the H versions of `verify_project.py`, its original-layout replay, the archived original verifier, `SOURCE_MAP.json`, and `ACCEPTED_BUILD.json`. The replay uses base `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`; the sole default registered project is `consolidation-core`, with `catalogue_complete=false`. It contains no Agent108 window package. The PR explicitly discloses this and provides its own complete pinned build rather than claiming default or whole-repository verification. Neither current policy inspected here nor the user authorizes turning an unrelated incomplete global catalogue into a new mandatory acceptance gate for this correctly scoped package.

## Reused historical execution, independently verified now

The complete 17-module historical run was performed by parent Agent #108, session b31b8818, from `2026-10-16T22:23:00.263209+00:00` through `2026-10-16T22:25:04.656370+00:00`. It is not execution by Agent #11. Its 38 raw command records comprise version/repository observations, nine dependency HEAD/status pairs, 17 project compilations and one generated audit. I checked every argv vector, cwd, exit, full stdout/stderr byte identity and corresponding prior independent readback hash. All 38 historical exits are zero; each of the 18 compiler/auditor commands has the exact strict flags `--trust=0 -j1 -DElab.async=false`, with a new empty project build directory and no prior project object reuse.

The runtime is official Lean 4.19.0, commit `6caaee842e94`; recorded binary SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Mathlib is `c44e0c8ee63ca166450922a373c7409c5d26b00b`. All eight package revisions, captured manifest/toolchain bytes, empty tracked-status output and explicitly admitted LEAN_PATH entries agree with the pins. Absence of the unused Cli compiled library is disclosed and does not introduce a fallback path. External Lean/Mathlib/dependency objects are trusted prerequisites, not freshly rebuilt source-to-object derivations.

I inspected `check.py` and its exact-origin Lean audit generator. I independently streamed every final raw metadata/BEGIN/report/END row, required actual printed-name agreement and equality of the safe-origin/report sets, compared every row with the audit JSON, regenerated the auditor text, and independently checked its equality with the executed captured source. I also reparsed it with the inspected package parser and checked all source correspondences.

| Measured final audit category | Count |
| --- | ---: |
| Exact project-module origin constants | 2,536 |
| Safe, nonpartial constants individually checked | 1,583 |
| Theorem constants | 1,367 |
| Safe definition constants | 202 |
| Safe inductive / constructor / recursor constants | 4 / 6 / 4 |
| Explicit source declarations | 578 = 448 original + 130 new |
| Separately classified unsafe / partial implementations | 930 / 23 |
| Unexpected accepted logical axioms | 0 |

The accepted axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`. There is no accepted `sorryAx`, `native_decide`, `Lean.ofReduceBool`, unsupported logical axiom or oracle shortcut. Private and generated safe declarations were included, not inferred from a public-name scan.

The historical runtime delegate's independent readback (a nonauthor of checker/Incoming, but disclosed author of Obstruction/Embedding) inspected the actual compiler and all 17 newly generated objects at execution time. Those compiled objects are reproducible infrastructure omitted from publication under policy. I compared their recorded identities across both retained receipts, but did not claim to freshly hash objects absent from this review's source snapshot. Separate historical source/layer reviews disclose authorship rather than claiming independent external-account approval. My present review is independent of all those authors.

| Retained evidence | SHA256 |
| --- | --- |
| Full-run verification receipt | `0ebb8d421e13c88365a6fdae255d56f41191d7ee9a72901b6d63b73fa284ea74` |
| Full raw final audit stdout | `cefcd19c62cdce7e1c2d25d27c811553d9fe7b29f36e7c1b86dfcd41420b9c9b` |
| Historical independent readback receipt | `288eeeca900f865e504d0ba27db2bdb406ce07abbc3992478739f7b15a69dda4` |

## Failed attempts and corrections remain distinct

I read all 289 retained log files and 67 JSON files and parsed 3,134 literal axiom rows across current and historical evidence. The 17 diagnostic-bearing logs and 11 nonzero execution/transport records are inventoried, including missing-module/object failures, failed proof attempts, the historical failed application launch, and failed transport. They are not relabeled successful.

Two abandoned Products attempts printed `sorryAx` after unsolved goals. These are failed snapshots outside the selected source closure. A third unusual raw row belongs to `choices._cstage2`, which the actual origin metadata marks unsafe; its compiler implementation axioms are not dependencies of the accepted mathematical `choices` or theorem constants. The complete final safe-origin audit proves none of these enters an accepted chain. Historical narrow dependency-audit wording is explicitly corrected: the old 112-name driver omitted LychrelDigitSums in its enumeration and lacked an explicit trust-zero flag. The full 17-module origin audit supplies that coverage without rewriting history.

The historical package-inspection draft and its final correction were also read: the fixed parser verifies printed names, and unused Cli is handled accurately. Recorded negative-control recipes and outputs preserve the distinction between input checks and Lean execution. One initial pre-edit checker snapshot was not captured; its record explicitly admits that absence rather than inventing original bytes. This does not undermine the frozen checker's exact source, complete run and independently retained final raw audit.

## Fresh commands and review-local failures

`fresh-command-receipt.json` records three fresh non-Lean commands, each exit 0 with complete stdout/stderr and hashes:

1. `PYTHONDONTWRITEBYTECODE=1 python3 verify_retained.py`: exact source/provenance and retained-execution/audit readback, PASS.
2. `PYTHONDONTWRITEBYTECODE=1 python3 check_registry.py`: default/replay versus scoped package inclusion, PASS_SCOPED_REGISTRY_DISCLOSURE.
3. `PYTHONDONTWRITEBYTECODE=1 python3 source/proofs/contributions/agent-108/window-weights-b31b8818/check.py --repo-root source --check-inputs`: INPUTS_VERIFIED_ONLY, 17 sources / 578 explicit declarations; no proof compilation or new axiom audit.

The retained receipt gives the actual absolute argv paths. `run_checks.py` captures these commands. Before the final capture, the same read-only scripts were run during review, with their complete output retained.

Two review-local mistakes are preserved. Initial extraction guessed `proofs/FOLDED_WEIGHT_OBSTRUCTION.md`, which does not exist at H; the extractor failed after the real changed files were read. The corrected extractor located and read the actual preserved paths. The first retained-evidence checker overbroadly rejected `sorryAx` in an explicitly failed archival attempt; the corrected checker keeps those rows in a separate historical inventory while continuing to require every final accepted raw report to use only the three allowed axioms. The exact failed scripts/stdout/stderr remain retained. Their individual Python exit codes were not separately captured by those early shell invocations, whose final `cat` command returned zero; no synthetic exit receipt is supplied.

Fresh Lean is NOT_RUN. Root reported an ordinary runtime launch failure and automatic rejection of escalation; this delegate neither retried, escalated, bypassed nor outsourced that denied execution. Authorized exact-source retained evidence reuse is justified by the unchanged complete closure, pinned environment, scoped original execution, actual independent readback, original raw audit verification here, and project policy permitting retained evidence with correct labels.

## Integration handoff and preservation

No source edits, new branches, remote comments/reviews, security changes or target mutations were made by this delegate. No unresolved mathematical or package-reproduction blocker was found at H. Root must still check the latest platform requirements, source-head guard, target ownership and combined current-main tree before any merge. The observed Codex review summary's failure is accompanied by a usage-limit notice, not a substantive displayed proof finding; this review does not declare any platform gate passed.

`publish-evidence/` contains this report and all new review scripts, full outputs, failed attempts, fresh receipts and recovery inventories. Published source/evidence duplicates are represented by exact commit/path/blob/byte-count/SHA256 maps instead of copying the dependency tree. Recover any mapped file with `git show COMMIT:PATH` and verify the recorded identities. `recovery-map.json`, `source-provenance.json` and `registry-recovery-map.json` jointly supply those mappings. Original raw outputs remain available at their already published exact Git paths.

## Exact interface for root's final combined-tree identity check

Root reported the newer current main `d00135526e27396fda95cdb00e809737b301cdbc` after PR #141. This review still applies to unchanged source bytes at H, subject to root's final complete-tree/source identity check; no repeated Lean execution is claimed or requested.

Use these canonical package files from the intended combined tree:

| Repository-relative path | SHA256 |
| --- | --- |
| `proofs/contributions/agent-108/window-weights-b31b8818/source-pins.json` | `8a7648eff9bb611e5605b2be83555bd7154971416f312be81cdf55505c8a7292` |
| `proofs/contributions/agent-108/window-weights-b31b8818/check.py` | `f046586ae35fe9b0eb8fa3e3f43461cd6c8007243401b2e92d88c71ec6df6633` |
| `proofs/contributions/agent-108/window-weights-b31b8818/REPRODUCE.md` | `f1d1e29581fab92d356401cbc17ad3505600e9c327fe2afc417ce0fe2e6b625c` |

The canonical combined-tree source selector is **`sources[].repo_path`** in `source-pins.json`. Validate each row's **`module`, `repo_path`, `git_blob`, `sha256`, `size_bytes`, `imports`** against the corresponding combined-tree bytes. `root_module` is `Agent108WindowIncoming`; `build_order` enumerates the exact 17-module closure. The seven `original_repo_path`/`original_commit` fields and `retained_path_verified_at` fields establish historical provenance, not alternate source-selection paths for the combined tree. The five flattened original paths and two fixed archive/version paths in `repo_path` must retain their pinned bytes; using similarly named current modules is not an equivalent check.

The local exact manifest is `/dev/shm/p196-agent11-046f/review98/source/proofs/contributions/agent-108/window-weights-b31b8818/source-pins.json`. `source-provenance.json` contains the independently verified 41 source identity links. `recovery-map.json` and `registry-recovery-map.json` preserve the surrounding source/evidence identities. The original complete execution receipt is at `proofs/contributions/agent-108/window-weights-b31b8818/review/final-package-fresh17-001/verification.json`; its `source_records` and captured `inputs/source-pins.json` agree with this canonical manifest.
