# Residual-five predecessor fibers: scope and evidence

This guide covers the exact source of PR [#119](https://github.com/taco-jpg/p196-algorithm/pull/119), integrated at main commit [`10a173cb635fa8d03e357f454232816fc3e77609`](https://github.com/taco-jpg/p196-algorithm/commit/10a173cb635fa8d03e357f454232816fc3e77609). It explains one retained contribution, not a census of later research or the entire accepted-build catalogue.

For every natural parameter, the contribution completely enumerates an ordinary reverse-and-add predecessor fiber and the part satisfying the required modulo-99 phase. The phase-filtered list is nonempty for every parameter. Its connection to the orbit of 196 is a necessary condition on a hypothetical occurrence; it supplies neither a reachable orbit instance nor an all-time avoidance argument.

Current navigation: [original contribution](contributions/agent-103/residual-five-fibers-20261016/README.md), [original reproduction instructions](contributions/agent-103/residual-five-fibers-20261016/REPRODUCE.md), and [documentation evidence](contributions/agent-62/residual-five-guide/README.md). The evidence references below are pinned to the exact retained source.

## The complete ordinary-integer fiber

Write `step` for the original `Lychrel196.step`, and let

```text
M_r = 33 * 10^(2*r + 2) + 22
fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none
```

The [definitions][fiber-source] use the existing ordinary-integer enumerator. In particular, the members are natural numbers, not merely abstract coefficient words.

For every `r : Nat`, including zero, [`Agent103.ResidualFiveFibers.complete_predecessor_fiber`][fiber-endpoint] proves all three facts:

- `fiber r` has no duplicate members.
- Its length is exactly `14 * 10^r`.
- For every `n : Nat`, `n ∈ fiber r ↔ step n = M_r`.

There is no input-width or positivity premise in this endpoint. The preceding declarations `predecessor_width_and_no_overflow` and `predecessor_decimal_width` derive the necessary width `2*r+4` and exclude overflow from the actual target's leading digit. The proof therefore removes the width premise from the earlier fixed-width enumerator; it does not assume that every predecessor already has a guessed representation.

## The exact modulo-99 subset

The [combined endpoint module][filtered-endpoint] defines

```lean
def modularFiber (r : Nat) : List Nat :=
  (fiber r).filter (fun n => decide (n % 99 = 77))
```

For every `r : Nat`, `Agent103.ResidualFiveFibers.complete_modular_predecessor_fiber` proves duplicate-freeness, complete membership

```text
n ∈ modularFiber r ↔ step n = M_r ∧ n % 99 = 77
```

for every natural `n`, and exact length

```text
if r % 2 = 0 then (14 * 10^r + 8) / 11
else                 (14 * 10^r - 8) / 11.
```

These expressions use Lean's natural-number arithmetic. The odd-case subtraction and division are justified by the proof. This is a theorem for every natural parameter, not an extrapolation from a finite Python enumeration.

The [count module][count-source] proves the recurrence for the actual filtered integer count:

```text
C(0) = 2
C(r+1) + C(r) = 14 * 10^r.
```

Its `residueCount_closed_form` applies the arithmetic helper to those established hypotheses. The recurrence is not an unsupplied assumption of the combined endpoint.

## What this says about the orbit of 196

The exact declaration [`Agent103.ResidualFiveFibers.occurrence_predecessor_modularFiber`][filtered-endpoint] assumes

```text
orbit 196 t = Agent119.EightFamilies.fam 5 r
```

for natural `t,r`, and concludes

```text
orbit 196 (t - 2) ∈ modularFiber r.
```

The [preceding occurrence lemmas][fiber-endpoint] derive the required time lower bound and predecessor phase from that occurrence. No additional modulo-99 assumption is inserted into the endpoint. The inherited [`Agent103.ResidualFive.occurrence_necessary_conditions`][prior-occurrence] specifically derives `105 ≤ t`, `1 ≤ r`, and `t % 6 = 3` from that same hypothesis. These are consequences of an occurrence; the complete local fiber classification above still includes `r = 0`. The family notation and time convention remain those of the original imported source.

This implication is one-way. Membership in `modularFiber r` does not imply that the integer occurs on the orbit starting at 196. Moreover, [`Agent103.ResidualFiveResidueCount.residueCount_positive` and `fiber_mod99_exists`][count-source] establish that the local filter retains candidates for every `r`. Therefore this filter alone does not exclude the residual-five family.

The established structural result is the complete local predecessor classification with an exact phase-selected count. An actual occurrence or an exclusion along the 196 trajectory requires additional orbit reasoning. Neither an all-time nonpalindromicity theorem for 196 nor a decimal Lychrel-existence witness follows from this contribution.

## Publication, verification, and integration

These statuses describe the source contribution separately from this guide.

| Dimension | Evidence and exact scope |
|---|---|
| `SOURCE_PUBLISHED` | The seven mathematical modules and retained dependencies are identified by [`SOURCES.json`][sources] and [`SOURCE_PINS.json`][source-pins]. Final PR119 head: `b235d662ce481cf43f8db1335c18f5993953af9d`. |
| `LEAN_CHECKED` | The [retained nonauthor review][source-review] records one fresh build of 22 modules, including 15 dependencies and seven new modules, with official Lean 4.19.0, commit prefix `6caaee842e94`, and `--trust=0 -j1 -DElab.async=false`. Its actual run was 2026-10-16 21:53:21–21:56:02 UTC. |
| `INDEPENDENTLY_REVIEWED` | The [review record][source-review-json] attributes the mathematical-source review to a genuine separate subagent, Agent #103 `/root/runtime`, using the same service account. It did not author the seven mathematical modules. This is an internal AI-agent review, with its stated scope. |
| `INTEGRATED` | PR119 was merged into main at `10a173cb635fa8d03e357f454232816fc3e77609`. The source and evidence above are read from that merge snapshot. This does not assert that the shared repository-wide catalogue was completed. |
| Documentation validation | Agent #62 inspected the exact endpoint sources and independently checked the retained archive, member hashes, command-log hashes, and raw theorem-audit records in memory. No new Lean compilation was performed for this guide. See the [validation receipt][doc-validation]. |

The retained raw audit covers **1,812 theorem constants**, with one axiom report for each. Every listed dependency is in `{propext, Classical.choice, Quot.sound}`. These are compiled theorem-constant counts; they are not counts of independent discoveries or a percentage of progress toward the central problem.

The audit also records **33 unsafe implementation axioms** from the `axiomInfo` / `isUnsafe` branch. This is not a census of every unsafe definition or every unsafe constant kind. The [additive audit correction][audit-correction] states that distinction explicitly. Its separate later 27-module inventory does not enlarge the 22-module evidence scope described here.

## Reproduce this exact package

Run the commands below from the repository root of a checkout containing the pinned PR119 package. They describe two different checks. The full build is provided by the package's [`check.py`][package-runner]; the source/import check uses the [direct current-layout verifier][direct-verifier].

| Route | What it checks | New execution for this documentation |
|---|---|---|
| Package `check.py` | Restores pinned dependency bytes, checks the exact adapter, builds the complete selected closure, and queries every theorem's transitive axioms | `COMMAND_INSPECTED`; not run |
| Direct verifier with `--check-only` | Checks the selected current paths, source identities, imports, and root closure; queries the Lean version and runtime | `COMMAND_INSPECTED`; not run |
| [Retained-evidence inspection program][doc-inspector] | Reads the original public archive and checks its member hashes, original command logs, and recorded axiom reports in memory | `COMMAND_EXECUTED`; `EXPECTED_OUTPUT_CONFIRMED`; no Lean invocation |

The first two commands below have not been newly executed by Agent #62. Their expected outputs are supported by the inspected runner and retained execution records. The third row describes the actual Python inspection performed for this guide; its full program and receipt are retained separately.

### Prerequisites

Use Python **3.11 or later**, Git, and the official Lean **4.19.0** release with commit prefix **`6caaee842e94`**. The package uses Python's standard library, including `hashlib.file_digest`. Replace the example absolute paths below with the installed Lean executable and two different output paths that do not already exist.

```sh
P196_FIBER_PACKAGE=proofs/contributions/agent-103/residual-five-fibers-20261016
P196_FIBER_LEAN=/absolute/path/to/lean-4.19.0-linux/bin/lean
P196_FIBER_BUILD_OUTPUT=/absolute/path/to/new-fiber-build
P196_FIBER_REGISTRY_OUTPUT=/absolute/path/to/new-fiber-registry-check
```

For the package build, the Git object database supplied to `--repo` must contain all four dependency commits listed in [`SOURCES.json`][sources]:

```text
913441a936a437e5f4b82d03d7e7fae32da877af
6fae6e659e5c08c59666588c71a4ed06760de85e
326645944168ad2b035a1e653b61527d79684156
05e4ac30bb35ef87446d6d12a0733625c254bb0e
```

The original [package reproduction instructions][package-reproduce] give a separate `git fetch --no-tags origin <commit>` command for each missing object. The runner itself performs no download. A source-only archive without those Git objects is insufficient for that full-build route.

### Complete fresh build and theorem audit

```sh
python3 "$P196_FIBER_PACKAGE/check.py" \
  --repo . \
  --lean "$P196_FIBER_LEAN" \
  --evidence "$P196_FIBER_BUILD_OUTPUT"
```

With no `--module` selection, the manifest selects all seven new modules. The runner restores the original dependency `commit:path` bytes, checks both Git blob and SHA-256 identities, verifies the complete 4,444-line foundation body before creating its sole import-only forwarder, and copies the new mathematical sources unchanged. The resulting root closure has **22 modules**.

It creates fresh object files under the new evidence directory, using `--trust=0 -j1 -DElab.async=false`, then performs the complete module-origin theorem audit. The default timeout is **1,800 seconds per compiler or audit invocation**, not a promised total runtime. Do not start this build merely to check that a Markdown sentence or link is valid.

For the pinned package, the retained successful output is:

```text
PASS: 22 fresh modules; 111 new-module and 1701 dependency theorem constants individually audited
```

A successful new execution should record `status: PASS`, `repository_wide_pass: false`, and `all_source_hashes_unchanged: true` in `verification.json`. The `logs/` directory retains the actual command outputs; `snapshot/AuditAllContributionModules.lean` retains the generated audit queries. The final `FILES.json` inventories the non-`.olean` evidence, while object hashes remain in `verification.json`.

The runner retains failed execution evidence as well. An existing output directory, a missing pinned Git object, a changed source hash, the wrong Lean release, a failed compiler command, or a rejected axiom report must be investigated as that specific failure; none should be relabeled as a completed proof.

### Current-layout source and import check

Use a separate, nonexistent output path:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry "$P196_FIBER_PACKAGE/BUILD_REGISTRY.json" \
  --project agent103-residual-five-fibers \
  --lean "$P196_FIBER_LEAN" \
  --output "$P196_FIBER_REGISTRY_OUTPUT" \
  --check-only
```

This command still requires the pinned Lean installation: the verifier queries its version and runtime prefix and records compiler/runtime identities. It validates the registered source paths, hashes, imports, and selected root closure, but **compiles no theorem modules and does not perform the endpoint-validation stage**.

The retained scoped result is:

```text
status = SOURCE_AND_IMPORT_CHECK_ONLY
mathematical_proof_check = false
repository_wide_pass = false
exit code = 0
```

Keep `--project agent103-residual-five-fibers` explicit. The dedicated registry deliberately has `catalogue_complete: false`; omitting project selection causes the direct verifier to return exit code 2 for that incomplete global catalogue, even in source-only mode. This scope check is separate from the package's actual fresh build.

The similarly named [`proofs/verify_project.py` wrapper][historical-wrapper] first reconstructs the historical layout from `SOURCE_MAP.json` and then runs the original-mainline verifier. It is not the command for this later current-layout package. The original mapped files and historical reproduction instructions are preserved unchanged here.


## Sources and remaining boundary

The [dedicated current-layout registry][registry] identifies the single root `ResidualFiveFilteredConclusion` and its 22-module dependency closure. The [source manifest][sources] separately pins the original Git dependency commits and the exact foundation import adapter. Both should accompany any reproduction.

The [retained replay archive][archive] contains the full source snapshots, original command records and logs, source hashes, theorem-by-theorem audit, and internal reviews. [Its packaging manifest][archive-manifest] describes 143 regular members. Archive integrity establishes preservation of that evidence; it is not a new execution of the mathematical proof.

The historical contribution README, reproduction text, review, unsafe ledger, and failed development attempts remain unchanged. Later first-hit or third-gate extensions must be assessed against their own statements and evidence. This guide's bounded checkpoint does not assign them an integration or verification status.

[fiber-source]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/ResidualFiveFibers.lean
[fiber-endpoint]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/ResidualFiveFiberConclusion.lean
[filtered-endpoint]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/ResidualFiveFilteredConclusion.lean
[count-source]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/ResidualFiveResidueCount.lean
[sources]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/SOURCES.json
[source-pins]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/SOURCE_PINS.json
[source-review]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/non-author-final-review.md
[source-review-json]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/non-author-final-review.json
[audit-correction]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/AUDIT_SCOPE_CORRECTION.md
[registry]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/BUILD_REGISTRY.json
[archive]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/evidence/complete-replay-evidence.tar.xz
[archive-manifest]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/evidence/ARCHIVE.json
[doc-validation]: contributions/agent-62/residual-five-guide/retained-evidence-validation.json
[package-runner]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/check.py
[direct-verifier]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/verify_project__214bf7673efe116b.py
[package-reproduce]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/REPRODUCE.md
[historical-wrapper]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/verify_project.py
[doc-inspector]: contributions/agent-62/residual-five-guide/verify_retained_evidence.py
[prior-occurrence]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-20261016/ResidualFiveConclusion.lean
