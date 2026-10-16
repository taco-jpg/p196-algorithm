# PR122 independent integration review

**Verdict: qualified acceptance; no source-level blocker found at exact head `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a`.** Fresh Lean execution is **NOT_RUN**. This verdict combines independent source/semantic review, newly executed identity and finite diagnostic checks, and explicitly authorized reuse of the retained original independent trust-zero compilation/audit. It is not a claim of a new kernel run or external peer review.

Reviewer: Agent #11 integration specialist `/root/review122`, session `046f9285a650`, at the requested ultra review effort. The reviewer authored none of the mathematical modules, made no source/main/remote write, and did not spawn another reviewer. The original author specialist and this reviewer are distinct agents using the same account; account identity supplies no external-review claim. Root owns all final main refresh, integration and Issue61 communication.

## Exact contribution and integration basis

- PR: https://github.com/taco-jpg/p196-algorithm/pull/122
- Reviewed head H: `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a`.
- Mathematical source commit: `d1392154bcd67996045fa4779c23985ab87455cd`.
- Prerequisite PR111 head: `bf4ff749000a6995e1755e37b59988ef362bae16`.
- Initial comparison main: `1ee9123344dbe17e9bda224ff8af5b1cbb2b64e4`.
- Post-PR111 comparison main: `61ac3b85eb3049805ae25260dbd628f007187e59`.

The full contribution delta from PR111 is additive: 127 paths, comprising three new Lean modules, their scoped registry and 123 contribution/evidence paths. No prerequisite arithmetic definition, original validity predicate, existing source, checker, global accepted registry or history is overwritten. At the post-PR111 main, all fourteen prerequisites are byte-identical to the retained seventeen-module checked closure; H supplies the remaining three. None of the 127 added paths collides with that main. The root reported a later independent PR124 merge; this reviewer does not substitute the `61ac3b85...` comparison for root's final current-main gate.

The three new modules contain eleven public theorems and one private helper theorem, with no new executable definitions or replacement predicates. Module SHA256 values are:

| Module | SHA256 |
|---|---|
| Agent1PeriodicParity | `8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129` |
| Agent1PeriodicPositivity | `481768dfb0d8884d61c038a886d5fc05131fc085286869c32190f80691e0b3d6` |
| Agent1PeriodicValidity | `4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52` |

`validation.json` and the recovery maps retain exact paths, source commits, blob IDs, SHA256 and byte counts. All seventeen current files match both the mathematical-source commit and the parent frozen sources. Every Agent1 reviewer snapshot matches its current file. All fourteen prerequisites match the exact PR111 head. The registry is precisely the transitive root closure of `Agent1PeriodicValidity`, with standard-library imports only beyond those seventeen modules; `catalogue_complete=false` remains appropriate.

## Meaning and proof review

The original Python `valid(s)` and Lean `ValidPeriodic` were read directly. Nat coefficients supply Python's nonnegativity requirement. The seven unchanged fields are bounds 18 on B/H/w, period length 4, center reversal symmetry, even middle coefficient at odd center length, and positive head of `B ++ w`. Empty exterior and center are permitted. The condition is not replaced by `CanonicalPair`, which lacks the center parity requirement.

The proof chain was inspected through the original `Agent8.Word = List Nat`, `zipAdd`, `pair`, decimal carry normalizer, `stepWord`, `Bounded`, `CanonicalPair`, `canonical_step` and its kernel `decide` exterior certificate. The carried digit/normalization bridge, repeated-block idempotence, exact raw slices, carry displacement, complete-block stripping and quotient definitions are unchanged. The raw blocks are literal slices of the exponent-three image, with center length `H.length + 8 + rawGamma`; both actual carry cases remain present.

1. **Center parity.** At odd width, reverse indexing selects the same middle input coefficient, so the actual pair map doubles it. `middle_append_eq` assumes equal exterior lengths and an odd center, not exterior symmetry. `stripPeriodCenter_even` uses exact reconstruction and removes twice the same period length; it therefore retains the indexed middle value. It includes the defined empty-period convention. `raw_center_even` obtains the literal raw center from the already-proved paired zipper center, rather than assuming the output parity.
2. **Exterior positivity.** `periodicWord_canonical` explicitly requires a positive repetition count; when B is empty, the first period coefficient is the outside coefficient. Period length four excludes an empty period. The proof builds all actual list fields of `CanonicalPair` and obtains the normalized-and-paired positive head from `canonical_step` at exponent three. `raw_outer_positive` takes a nonempty prefix. `stripPeriodSuffix_outside` preserves the head of residual-plus-period, which correctly handles an entirely stripped exterior. Its private append-head helper includes the formerly failing empty-period case with an actual induction.
3. **All original fields.** `raw_valid` places the inherited boundedness tuple's outer/period/center facts into the predicate's outer/center/period order correctly, and explicitly supplies length, symmetry, parity and positivity. `strip_valid` supplies all seven fields for the exact executable stripping operations. It derives period nonemptiness from length four; the symmetry proof is not used as a substitute for odd-center parity. `quotient_valid` is exactly this composition at `quotientOuter`, `quotientCenter`, and `rawPeriod`.
4. **Exact transition scope.** For every `ValidPeriodic B H w` and `3 ≤ k`, `valid_quotient_transition` proves successor validity, the exact existing `stepWord` equality, and target exponent at least one. It discharges the historical Python `valid(target)` assertion even without the Python transition's additional safe-input assertion. It does not prove target exponent at least three, safe-state closure, a return cycle, integer realization or infinite avoidance. A fresh diagnostic case actually reaches target exponent one. Decimal Lychrel existence and the claim for 196 remain unproved.

No `sorry`, `admit`, `sorryAx`, `native_decide`, custom `axiom`, `ofReduceBool`, `skipKernelTC`, `extern`, `implemented_by` or `unsafe` occurs in code of the accepted seventeen-module closure under the comment/string-aware scan. The complete new source and necessary definitions were also read. The static scan is a supplemental check, not a substitute for the retained transitive theorem audit. No arbitrary additional all-safe-definition census is imposed; there are no new definitions here, and the existing complete theorem audit traverses proof dependencies.

## Retained original execution: validated, not rerun

The original separate specialist's `review/replay.py` creates a fresh empty build and copies exact source bytes, including all prerequisites; it does not copy project compiled objects. Its eighteen recorded commands comprise seventeen module builds plus `ReviewAudit`. Every command explicitly includes `--trust=0 -j1 -DElab.async=false`, every exit code is zero, and every complete log hash was independently checked against the retained bytes. A representative command is:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicValidity.olean Agent1PeriodicValidity.lean
```

The retained compiler is official Lean 4.19.0, commit `6caaee842e94`, Release, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. New read-only hashing of the supplied local binary and four shared libraries matches the original parent compiler inventory. This is an identity check, not successful execution of that binary in this session.

The full audit source enumerates constants by actual originating module, rejects custom safe axioms, and calls `Lean.collectAxioms` on every theorem constant in all seventeen modules. It requires each module to be audited. The newly parsed full log has exactly **1,367 distinct theorem rows**, including all eleven new public theorems, the private helper, and generated theorem declarations. Counts are audit metadata, not 1,367 independent results. Multiline axiom lists are parsed fully. Every theorem's transitive axioms are a subset of `{propext, Classical.choice, Quot.sound}`, and the full union is exactly that set.

There are **13 inherited unsafe compiler implementation metadata entries** originating in `LychrelDigitSums`; the complete list is in `validation.json`. None occurs in any audited theorem's transitive axiom set. They are not misreported as absent, additional logical axioms, or proof shortcuts. No custom safe axiom or excluded theorem dependency was found.

The separate parent canonical verifier has another eighteen successful logged commands and the identical ordered 1,367 theorem audit rows. Its argv does **not** explicitly contain `--trust=0`; this report does not relabel that run as the explicit trust-zero execution. The actual canonical checker was inspected, including its source/hash/import checks and audit. Its parent report names the prior Git head because execution preceded mathematical-source publication. Exact frozen source-byte comparisons to both `d1392154...` and H resolve that provenance mismatch; the prior-head string is not treated as proof that new files already existed in the older commit. The ordinary `--check-only` path itself launches the runtime, so it was not used to hide a known execution limitation.

The three new modules' retained `#print axioms` outputs cover all eleven public theorem names. The scoped registry lists ten main endpoints, omitting the auxiliary public `middle_append_eq`; that auxiliary is present in source and the complete theorem audit. These are distinguished from public type printouts: the source statements were independently read, and the parent audit includes `#check` for its ten registered endpoints.

The final `EVIDENCE.json` verifies all 122 listed retained files. Historical `CHECKPOINT001.json` verifies all 34 entries against its actual `d1392154...` checkpoint, including the older README, rather than incorrectly requiring those historical hashes to equal the final README. The parent `FILES.json` verifies all 37 entries. The complete contribution remains available by exact Git recovery pins, including attempted and failed work. The stale running-review wording in the retained rolling queue is a historical status artifact; the completed receipt and exact checked sources determine this review's status.

The positivity author's first attempt is retained with its actual exit 1, full source and failure log. Its empty-period helper goal was unsolved and its dependent theorem diagnostic contained `sorryAx`. The accepted second source adds the missing induction; it and the final independent clean closure are different evidence. The failed attempt is neither deleted nor counted as accepted proof.

## New execution and boundary

The new identity validator and current-combination validator both exit zero. Fresh execution of the already-inspected diagnostic script against its exact pinned original Python module also exits zero: 16 valid inputs, 10 invalid-field controls and 48 transitions at k=3,4,7; actual carry values 0 and 1; seven valid-but-unsafe inputs; four empty quotient exteriors and five empty quotient centers; minimum target exponent one. All seven raw and stripped predicate fields are checked. Full new JSON output and stderr are retained. These selected finite diagnostics are not universal proofs or new all-time conclusions.

Fresh Lean is **NOT_RUN**: root instructed the reviewer not to repeat the already observed standard-launch failure `error: failed to locate application`; a prior escalation had been automatically rejected. This reviewer read the retained PR111 runtime failure, made no launch attempt, requested no escalation and attempted no bypass. The original independent Lean evidence is reused under the user's exact-source reuse authorization. The new read-only binary hashes do not upgrade this limitation.

No source repair is requested. Integration remains conditional on root confirming the final remote H and main, preserving these classifications and the complete evidence, and applying the existing serialized integration policy. This receipt establishes neither repository-wide catalogue completion nor external peer review.

## Artifact coverage and recovery

`ARTIFACT_INVENTORY.json` inventories every new retained artifact in this compact folder; its own identity is supplied by publication Git, avoiding recursive self-hashing. `RUNS.json` records actual new commands and exits. `operational-failures.json` preserves the two preliminary read/extraction failures and the dependent read failure; none is a Lean run. The executed new scripts are included byte-for-byte. To replay them, place each script one directory above its intended `publish-evidence/` output directory and make the read-only Git repository available at its documented `REPO` path, or adjust that operational path explicitly before recording a new run. The diagnostic script is recovered at its exact H path rather than recopied as new source.

`SOURCE_RECOVERY.json` maps all inspected/reused original objects to immutable commits, repository paths, blob IDs, lengths, SHA256 and argument-array recovery commands. `CURRENT_MAIN_SOURCE_RECOVERY.json` adds the fourteen exact prerequisite pins at `61ac3b85...`. Use `git show <commit>:<path>` in a repository holding that commit, redirect to the desired reconstruction path, and verify the stated byte count and SHA256. Duplicate snapshots, repository copies, runtime installations, caches and compiled objects are excluded from this compact publication folder as reproducible infrastructure. No new substantive source, result, failure or validation output is omitted.
