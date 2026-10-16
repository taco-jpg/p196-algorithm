# Agent 105 / 9df76b: final numerical decoder verification

## Verdict and frozen scope

**PASS for the selected `agent105-numeric-decoder-9df76b` project.** Both the unchanged repository verifier and a separate explicit `--trust=0` replay compiled all 12 selected modules and ran the same exhaustive module-origin audit. Each run checked 29 registered public endpoints and audited 1,096 theorem declarations, including private and generated auxiliary theorems. The two complete maps from theorem names to axiom dependencies agree.

The source checkpoint is `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`. The registry is `proofs/Agent105NumericDecoder9df76b.registry.json`, SHA-256 `10aa02456c15914a8dd00a1b3bf639a7e9f129262c54ef7bd894ec635eec9f52`. The first verifier and this final check both observed that exact HEAD and a clean tracked worktree. Verification artifacts are new files, so “clean” here accurately refers to tracked files; it does not claim that there are no untracked artifacts.

This report covers the executable one-step inverse decoder at a prescribed actual source width. It does not establish an infinite-time result for 196. The accepted repository catalogue is incomplete, so neither receipt claims a repository-wide pass.

## Two actual complete runs

| Run | Result | Commands | Elapsed time | Receipt SHA-256 |
|---|---|---:|---:|---|
| Unchanged repository verifier | PASS, exit 0 | 12 module compilations and 1 audit | 101.94 s | `edf5973278f714ad07d0e038e5707b0918da9bbd9748058dedd625900a7fe191` |
| Explicit `--trust=0` replay | PASS_EXPLICIT_TRUST_ZERO, exit 0 | official help, 12 module compilations, and 1 audit | 96.19 s | `23a4cb57f89f83f11e1fd4817e35cb85552f5771f1f9827b5ce1f1c57b59e639` |

The unchanged checker is `proofs/verify_project__214bf7673efe116b.py`, SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. Its source and policy were not modified. It checked the registry, pinned source SHA-256 and Git blob identities, exact import closure, prohibited proof shortcuts, official compiler identity, all registered endpoints, and every selected module's theorem dependencies. It also checked that source snapshots and compiler files remained unchanged during the run.

Its recorded Lean command lines do **not** contain `--trust=0`. The official compiler's retained help says `trust level (default: max)`. The supplemental run therefore explicitly added `--trust=0` to every module compilation and to `ProjectAudit.lean`. It used a second initially empty directory, copied the exact original source snapshots, and rebuilt every selected local module. It reused the original generated audit byte for byte and did not change the registry or allowed-axiom policy.

The exact driver commands and exit records are in `fresh-scope105-001.driver.json` and `strict-scope105-001.driver.json`. Their full terminal logs are retained next to them. Module logs and source snapshots are under the corresponding run directories. Reproduction requires a new, previously nonexistent output directory for each run.

The supplemental helper is copied unchanged from the already reviewed earlier inverse-boundaries contribution. Its SHA-256 is `5836600e3e5a70bc891e1c3e393c4314eb27d08a0e5674a11819c94b5b7c7e6f`. It supplements the unchanged verifier; it does not replace it.

## Exhaustive module-origin audit

Both audits select declarations by `env.getModuleIdxFor?`, inspect every selected `.thmInfo`, and apply `Lean.collectAxioms`. The observed axiom union is exactly:

```text
[Classical.choice, Quot.sound, propext]
```

No selected theorem depends on an axiom outside those three. No custom safe axiom was accepted. The exact generated audit source is identical in both runs, SHA-256 `2b09bd716fc3964f4e33988c3b0acef3842479e1f7b190ce4feb1850ece8d56b`.

| Source module | Audited theorem declarations |
|---|---:|
| Lychrel196Research | 787 |
| Agent101DigitPairs | 27 |
| Agent101MultiplicityBounds | 28 |
| Agent101SplitEnumeration | 58 |
| Agent101NumericFibers | 56 |
| Agent105WidthSupport9df76b | 8 |
| Agent105CrossWidthWitness9df76b | 20 |
| Agent105DecoderLocal9df76b | 27 |
| Agent105DecoderTarget9df76b | 7 |
| Agent105DecoderScan9df76b | 66 |
| Agent105NumericDecoder9df76b | 6 |
| Agent105DecoderControls9df76b | 6 |
| **Total** | **1,096** |

The five new decoder/control modules account for 112 of those declarations and contain the 29 registered public endpoints. The public count and audit count measure different things: the audit also includes private and generated auxiliary theorems.

The unchanged audit separately records 22 existing unsafe implementation declarations: 13 in the foundation, 3 in Agent101DigitPairs, 1 in Agent101MultiplicityBounds, 4 in Agent101SplitEnumeration, and 1 in Agent101NumericFibers. None is introduced by the five new decoder/control modules. Their presence is distinct from theorem axiom dependencies: all audited theorem dependencies remain within the three allowed logical axioms. Both audits list exactly the same 22 declarations; the complete names are retained in both receipts and this report's JSON companion.

## Statement and boundary review

For a canonical ordinary decimal target `Y` represented by `e` at target width `W`, `decodeNumerical e W L` succeeds exactly when there is a positive ordinary integer predecessor with actual canonical input width `L` whose reverse-and-add step is `Y`. A successful result specifies the complete finite symmetric column-coefficient profile of such a predecessor.

The numeric wrapper makes the two possible width branches explicit. When `W = L`, it requires final carry zero. When `W = L + 1`, it requires final carry one and the leading target digit to be one. Other widths fail. The general width results and the finite realization bridge justify these branches. Source width zero is rejected by the underlying positive-width guard.

The lower-level `decodeAtWidth` correctness theorem has the explicit hypothesis `he : ∀ i, i < L → e i ≤ 9`. This hypothesis is necessary for identifying the solved column equations with the actual decimal carry/output recurrence. The canonical numerical target supplies it. The raw function is deliberately also defined on arbitrary natural-number input functions; it is not claimed to satisfy the physical decimal-output specification outside that hypothesis.

After removing an overflow digit, the remaining low payload is not required to be canonical. In particular, `5 → 10` has one-digit low payload `[0]`; requiring that payload to have a nonzero leading digit would wrongly reject this case. The decoder's canonicality condition is instead the appropriate positive outer coefficient for the realized input.

The local solver uses truncated natural subtraction only to propose candidates, then checks the complete equations. The full scanner checks the carry meeting condition for an empty center, the even-coefficient condition for a singleton center, and the positive outer coefficient. The decoder returns a coefficient profile; this contribution does not enumerate all numerical predecessors or establish a recurrence property over infinitely many steps.

## Kernel boundary controls

The six public controls were compiled as part of both complete final runs. The earlier targeted `controls/kernel-attempt-001` is also retained, but it is separate from the two complete final closure checks.

| Control | Kernel-checked behavior |
|---|---|
| `five_to_ten` | `step 5 = 10`; width 1 with carry 1 decodes to `[10]`; the width 2 zero-carry branch fails. |
| `one_to_two` | `step 1 = 2`; width 1 zero-carry branch returns `[2]`; width zero fails. |
| `boundary_121` | `29` and `110` both step to `121`; the width 2 and width 3 branches return `[11, 11]` and `[1, 2, 1]`. |
| `retained_nonpalindromic_1197801` | `200799` and `1098900` both step to the nonpalindromic `1197801`; both respective coefficient profiles are returned. |
| `truncated_subtraction_rejects` | Impossible edge and center equations are rejected despite truncated natural subtraction. |
| `output_digit_bound_contract` | The raw decoder can return `[10]` for the out-of-domain digit `e 0 = 10`, while its actual decimal output/carry are `0`/`1`; this explains why `he` belongs in the theorem. |

The nonpalindromic cross-width profiles with common value 1197801 were already recorded in retained research prose. The integers 200799 and 1098900 are concrete canonical realizations formalized in this work; this report does not label the underlying example a newly discovered counterexample. Large reverse-and-add equalities reuse the previously verified canonical/reversal witness bridge instead of expanding a huge `reverseFuel` computation.

## Source identity and review independence

For all 12 modules, the current file, the published Git object at the source checkpoint, and both build snapshots are byte identical. The registry's SHA-256 and Git blob identities all agree. The full 12-module identity map is in `scope105-final-review.json`.

| New source module | Frozen SHA-256 |
|---|---|
| Agent105DecoderLocal9df76b | `820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872` |
| Agent105DecoderTarget9df76b | `2c2cbf18088e0a281ff78547cc3b2aa465050504c9139fc2839fb70e86db7c9d` |
| Agent105DecoderScan9df76b | `4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d` |
| Agent105NumericDecoder9df76b | `9a63eb03cb04d9e7fb3294216ab770893ac227c089ddba6d864d73d949229db5` |
| Agent105DecoderControls9df76b | `3159c9ddfe55b141e56d5181240bd696b3677d3061a2f8aaf317b6bce5c8b7c5` |

The earlier four inverse-boundaries mathematical modules also remain unchanged. They were not subjected to an unnecessary repeat of their already completed nine-module validation scope.

| Earlier source module | Unchanged SHA-256 |
|---|---|
| Agent105WidthSupport9df76b | `3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7` |
| Agent105CrossWidthWitness9df76b | `57d7fad87d320eddf13c32f35f2ab1cf11e2c318073c1cf2466e265baea73252` |
| Agent105CrossWidth9df76b | `a8fe89a91d79809bb3452a39775eb0cc9a06241d37e37c7ef916bf20f265d7a2` |
| Agent105PalindromeImage9df76b | `029bcf37c74d0d6a2b226cf60011ba7d66a3daee40087833f039b13be0e6cce6` |

`scope105` authored the six decoder controls. The mathematical decoder modules have separate nonauthor semantic reviews: Target and Scan by runtime105, Local and Target by scope105, and Numeric by both scope105 and structure105. These reviews examine the mathematical statements and interfaces. This report records the actual independent full closure replay and exhaustive module-origin audit; it does not substitute an author's compile log for either activity. The earlier incremental review explicitly records that Scan was then unfinished; the present final validation uses the frozen completed Scan hash shown above.

The frozen semantic evidence remains at:

- `controls/incremental-semantic-review.{md,json}`
- `controls/decoder-controls-result.{md,json}`
- `controls/numeric-wrapper-semantic-review.{md,json}`
- `local/target-semantic-review.{md,json}`
- `local/scan-semantic-review.{md,json}`
- `numeric/semantic-review.{md,json}`

Their content hashes are recorded in the JSON companion. Existing development and semantic-review files were not edited during final validation.

## Shared resource observations

The two complete runs were sequential within this session. No other session's process was stopped. These are shared cgroup observations, not per-job memory attribution. Memory could approach the shared limit while a large portion remained file cache. The observed OOM and OOM-kill counters stayed at 152 and 5 throughout the recorded interval.

| UTC observation | Current GB | Anonymous GB | File cache GB | OOM / killed |
|---|---:|---:|---:|---:|
| 2026-10-16T22:05:08.761128+00:00 | 5.877 | 1.131 | 4.067 | 152 / 5 |
| 2026-10-16T22:06:28.539230+00:00 | 8.590 | 3.275 | 4.529 | 152 / 5 |
| 2026-10-16T22:07:41.940431+00:00 | 7.524 | 1.049 | 5.766 | 152 / 5 |
| 2026-10-16T22:08:59.113835+00:00 | 6.436 | 2.518 | 3.257 | 152 / 5 |
| 2026-10-16T22:10:38.391176+00:00 | 5.503 | 0.916 | 3.950 | 152 / 5 |

The individual `resource-*.json` files retain memory limits, dirty/writeback bytes, memory events, and available process-name/RSS snapshots. Both final jobs exited zero. After the second run, only read-only source/audit comparison and evidence packaging were performed; no additional Lean test was started.

## Evidence inventory

`scope105-final-review.json` is the machine-readable summary. The primary receipts are `fresh-scope105-001/verification.json` and `strict-scope105-001/strict-verification.json`. Each run retains all compiler/audit logs and exact source snapshots. The generated audit sources and complete theorem-dependency maps agree across the two runs.

`scope105-evidence-manifest.json` hashes every final evidence file under this verification directory, except the manifest itself and reproducible compiled `.olean`/`.ilean`/`.o` outputs. It also records the pinned published source identities. All mathematical sources and complete logs remain available; no failure log or earlier development record was removed.
