# PR #138 independent exact-source review

**Verdict: PASS for the mathematical contribution and retained proof evidence, with F1 resolved by the independently reviewed additive erratum identified below.** No theorem, hypothesis, dependency, arithmetic, or preserved-development blocker was found. Root must publish that exact correction with the integration record. This review does not authorize an unverified combined tree or assert that the PR has been merged.

Reviewer: Agent #11, session046f, independent `review138` subagent; no authorship of the three new Lean modules, no source edits, no remote mutations. Nonexclusive review claim: `9196acaa2a725117434909e5ab291041eceeb891`. English deliverable; Chinese conversation. The root agent owns source/publication changes, formal reviews, issue #61 coordination, retargeting and main integration.

## Exact source and ancestry

| Role | Commit |
|---|---|
| Reviewed PR138 head H | `40670be3636e4ee7e3158e0d1577d26472a4a2a0` |
| Actual current PR125 head supplied and source-checked | `71fa669acdff9ee203ef28d7db7e31e2f9b5b4af` |
| Actual merge base of the two heads | `686cac2696e4e4e059c1b9d6a313f5519f6f4176` |
| Complete frozen PR138 mathematical publication | `bc178ab8735e9503ab25b325e5a8dc82bf1f1e37` |
| Main supplied at assignment; root must refresh | `2bc42391c63b744951f27fde11af8c7d7958077f` |

The actual contribution is **61 added paths**, with no modifications or deletions against the common ancestor: three accepted source modules and their claim, ownership, development, controls, and verification evidence. A direct actual-PR125-head-to-PR138-head diff falsely looks like removal of newer PR125 evidence because the branches diverged. The integration must preserve actual PR125's later evidence. The old `686cac...` commit is the historical mathematical base, not the current PR125 head.

All 21 registry source modules at H were independently byte-compared with both `bc178ab...` and the original fresh-build snapshots. All 18 inherited modules were also byte-compared with actual PR125 head `71fa...`. Every source SHA-256, Git blob, import list, and byte count is in `evidence/canonical-source-pins.json`. The full changed-path/recovery inventory is `evidence/source-recovery-map.json`; the final publication package includes an expanded recovery map for every inspected original file. The scoped registry is a real reproducible build entry point for this contribution; no repository-wide build pass or global accepted-catalogue completeness is claimed.

## Mathematical reading

I read all three complete new modules, their development-source differences and relevant surrounding definitions/proofs: `UpperDomain`, actual component/whole pair iteration and width lemmas, finite zero extension, carry-derived normalization, `Canonical`, `Admissible`, `valid_word_realizable`, `iterPairs_representation`, and the inherited numeric bridge. Original imports and definitions are unchanged.

The domain is exactly `r >= 1`, `5 <= p <= 9`, `5 <= u <= 8`, `5 <= v <= 6`, `u+v <= 13`. Its seven cores are `(5,5),(5,6),(6,5),(6,6),(7,5),(7,6),(8,5)`. It is consistent and includes `r=1` and both exterior endpoints. Neither an impossible hypothesis nor a favorable representative is substituted for the advertised universal statement.

For actual time-two component A of width `2*r+7`, its finite zero extension receives `+1` at `r+1,r+5` and `-1` at `r+2,r+4`. These four positions are distinct, valid columns even at `r=1`; the center is `r+3`, the reflected axis is `2*r+6`, and the exterior column is unchanged. The signed word is proved nonnegative for every natural index before its exact conversion through `Int.toNat`. Thus the conversion cannot hide negative coefficients.

| New theorem(s) | Independent interpretation check |
|---|---|
| `rebase_delta_overlap` | The four-site signed correction plus its left-zero previous coefficient equals the inherited six-site overflow defect. The retained `r>=1` hypothesis is harmlessly stronger than this algebraic helper requires. |
| `rebasedInt_actual_component` | Identifies the signed input with the finite zero extension of the **actual** second component for every index. |
| `rebasedInt_overlap` | Expands the signed overlap using the original `previous`/`shiftOne` boundary conventions. |
| `finite_whole_rebasedInt`, `actual_whole_rebasedInt` | Cover every `i<2*r+8`, including zero and the highest newly created whole column. |
| `finite_component_flank`, `finite_component_inner` | Derive actual flank values `2*u-9` and inner values `2*(u+v)-18` using real normalized digits and carries. Natural subtraction is justified by the domain. |
| `finite_component_admissible` | Uses admissibility of the doubled component and the actual overflow-selected next width. |
| `rebased_nonnegative`, `rebased_bounded` | Prove all-index signed bounds before projection. At subtractive sites the original inner value is at least 2, so the corrected value is at least 1. At additive sites `2*u-9+1<=8`; elsewhere inherited bound 18 suffices. |
| `rebased_toNat_exact` | Establishes cast-back equality globally from the nonnegativity theorem. |
| `rebased_zero_after_width` | Gives C=0 for every `i>=2*r+7`; prevents invalid reflected/clamped raw tails from entering the last overlap column. |
| `rebased_symmetric`, `rebased_center_eq`, `rebased_outer_eq` | Preserve finite-width symmetry, unchanged center parity, and positive exterior. |
| `rebased_admissible` | Discharges exactly the original five-part predicate at width `2*r+7`, including bounded digits, symmetry, and the self-reflected center condition. |
| `actual_whole_rebased` | Converts the signed identity to a Nat identity on the complete actual whole width `2*r+8`. |
| `rebased_component_realizable` | Constructs a positive ordinary natural `a` and canonical digits `da` realizing C by the unchanged realization theorem. |
| `numeric_rebased_overlap` | Retains arbitrary original `n,d` satisfying the original canonical representation and pair-column prefix, and yields actual `orbit n 2` at width `2*r+8`. |
| `numeric_rebased_realization` | Gives a positive C realization and compares its **finiteWord-truncated** canonical pair columns with every valid output column. The global finiteWord equality explicitly uses the proved zero tail. |
| `realized_rebased_overlap` | Supplies existence of a positive original input as well as a positive corrected component; it does not weaken the earlier arbitrary-input theorem. |
| `rebased_differs_at_flank` | C minus the actual old component at valid column `r+1` is exactly 1, so this does not contradict PR125's failure of overlap with the original component. |

The theorem is about pair columns, not an equality `orbit n 2 = 11*a` for arbitrary integer representatives. There is no generic inverse classification, uniqueness theorem, later-time safety/return/invariance, infinite nonpalindromicity, or result about 196. The formal coefficient bound is 18; the stronger maximum 9 observed by finite controls is not promoted to a theorem. Agent8's transport contribution remains attributed and unchanged.

## Reused execution evidence and fresh validation

**No Lean process was launched by this reviewer. Fresh Lean is `NOT_RUN`.** The root reported an ordinary Lean launch failure and an automatic approval rejection; this reviewer did not retry, escalate, bypass, change execution route, or outsource Lean. The user's authorized exact-source evidence reuse is sufficient here because source closure, tooling identity, and theorem scope match.

The original nonauthor executor is recorded as **Agent #100 `scope_audit`**, distinct from source authors `runtime_setup`, `groupii_dynamics`, and the original root. It is same-session nonauthor review, not an independent account or external peer review. The canonical verifier's built-in `Agent #1` string is not the caller identity. The run's actual HEAD was `686cac...`, with the new files then untracked; later immutable publication and source-snapshot comparisons establish the complete mathematical source at `bc178ab...`. The verifier's `source_tree_clean=true` uses `--untracked-files=no` and does not by itself establish tracked source identity.

I inspected the unchanged canonical verifier (`SHA256 c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`), replay, strict audit, complete multiline parser, generated ProjectAudit, original invocations, all command records and log pins. The verifier creates a new source directory, checks exact source/import pins, forbids unsupported proof tokens, constructs the entire root closure, and compiles each local module without author oleans. It uses a restricted environment with the selected source directory as `LEAN_PATH`.

The retained run used official Lean 4.19.0, commit `6caaee842e94`; executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Full runtime-library hashes are preserved in the original report and this review's canonical pin manifest.

- **Original fresh source build:** 21 module compilation commands plus ProjectAudit, all 22 exit codes 0. Module argv was `lean -j1 -DElab.async=false -o Module.olean Module.lean`. It did **not** explicitly specify `--trust=0`. This is one normal complete source build with current declarations kernel checked, not 21 merely imported cached modules.
- **Original follow-up:** `lean --trust=0 -j1 -DElab.async=false ProjectAudit.lean`, exit 0, approximately 55.835 seconds, over the same fresh local oleans. It is a separate explicit trust-zero import/endpoint/transitive-axiom audit. It is not a second fresh source build and must not be described as rerunning the kernel on every imported theorem body; see F1.
- **Fresh non-Lean validation here:** independently decoded and checked all 66 archive members against stored hashes and published duplicates; checked every source against H, frozen mathematical commit and fresh snapshot; verified all 22 original commands, exits and raw log SHA-256 values; re-parsed all 2,661 complete multiline module-origin axiom lists and compared both raw logs and both ledgers; matched all 22 new literal `#print axioms` records; recomputed 105 retained ordinary-integer cases and 840 actual reverse-additions; validated all 490 author rows' retained identities and overlap arithmetic; verified author receipts, failure/success logs, and final-source snapshots.

The full raw canonical and strict audit logs are byte-identical. All 2,661 theorem constants have transitive axiom union exactly `{propext, Classical.choice, Quot.sound}`. The three new modules contribute 85 theorem constants including generated items. Of the 22 explicit exports, 14 use `propext, Quot.sound`; 8 additionally use `Classical.choice`. Fourteen inherited unsafe implementation symbols are separately inventoried and none occurs in any audited theorem's axiom set. The generated audit rejects safe custom axioms and disallowed transitive axioms; it is not only a keyword scan. Counts are audit metadata, not counts of major independent results.

Raw evidence archive: `proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-complete-evidence.tar.xz`, **155348 bytes**, SHA-256 `3c858e22b045a338b041b06114050cdbf6e60421da9b0e073433ed49ab86c821`; decoded tar **3471360 bytes**, SHA-256 `e63e78815964c3c73b5aef7f5fbca0391446e375b4f206e62c44988785a9d403`. Every member's recovery identity is retained. The compressed control rows decode byte-for-byte to their raw data.

## F1 — correction of the imported-proof type-check claim

The retained statement that the later command “typechecked all imported modules” is too strong for this version. I independently read the exact official implementation provided by the PR125 reviewer, pinned to Lean commit `6caaee842e9495688c1567e78c0e68dbb96942aa` and checked against its Git blobs:

- `src/Lean/Environment.lean`, `finalizeImport` and `importModules`: load module constants into the environment and store `trustLevel`; they do not replay all imported proof bodies through the kernel.
- `src/Lean/Elab/Import.lean`, `processHeader`: routes imports through that implementation.
- `src/kernel/type_checker.cpp`, `infer_constant`: checks a referenced constant's level/safety conditions and uses its declared type, without recursively rechecking its proof value.
- Conversely `src/Lean/AddDecl.lean`, `Environment.addDeclCore`, and `src/kernel/environment.cpp`, `add_theorem`, show ordinary current source declarations are kernel checked unless a separate explicit skip mechanism is used. The inspected canonical sources/commands do not enable such a mechanism. Default trust is not a reason to reject the valid fresh source compilation.

Affected original locations under `proofs/contributions/agent-100/groupII-rebase-20261016/` include `verification/reviewer-README.md` line 33, `controls/reviewer-semantic-review.md` lines 3 and 67, the strict launcher purpose/status fields, `verification/reviewer-strict01/strict-import-verification.json` purpose/status fields, and the archive manifest's scope note. Their copies inside the original archive are historical evidence and must be preserved.

**Minimal repair:** publish an additive correction stating: “The retained canonical run compiled all 21 modules from exact source with normal kernel checking, without an explicit `--trust=0` option. The subsequent explicit `--trust=0` ProjectAudit imported the resulting modules, checked endpoint availability and recomputed the complete transitive axiom ledger. It did not freshly rebuild those modules or independently recheck all imported proof bodies.” Retain all original bytes and identify the superseded wording. No mathematical source repair or extra Lean run is required for this clarification. Root owns and will independently route the additive evidence correction.

**Independent review of concrete repair — PASS:** I read the complete candidate `Agent11Lean419VerificationErratum.md`, 7365 bytes, SHA-256 `a516f682dc643f68647224d4ba2b9a31016c12b246197b30787a3cd60acbb350`, prepared by root for additive publication through the PR125 prerequisite. It explicitly covers both reviewed heads, names PR138's affected historical documents/scripts/archive members and formal review, preserves original evidence, separates normal source compilation from subsequent import/axiom audit, and states present-session fresh Lean `NOT_RUN`. I independently checked its PR138 command count, flags, elapsed time (55.834794998168945 seconds before rounding), exit, source and archive pins, theorem/endpoint counts, axiom scope, and official implementation explanation against the inspected raw evidence. It is sufficient to resolve F1 without touching PR138's active source branch or changing its mathematics. The exact candidate review is retained in `ERRATUM_REVIEW.md`; actual publication/commit identity remains root's responsibility.

## Failure preservation and limits

Author Algebra attempt01 failed with incomplete boundary simplification, nonexistent `Nat.cast_add`, and a rewrite under a function argument. Its source, command, full log and exit 1 are retained; attempt02 fixes these without changing the advertised theorem. Profiles positions-attempt01 failed because `componentDoubleCarry` was ambiguous; qualifying `GroupIIOverflow.componentDoubleCarry` fixes it. Its exit 1 and `sorryAx` error-recovery output are preserved and excluded from accepted evidence. Successful final source snapshots equal H. Numeric attempt01 exits 0. Remaining unused-variable warnings are nonsemantic.

My own initial extraction attempt used nonexistent canonical-layout paths; this operational mistake was corrected by using the published explicit module registry. My first supplementary lexical scan falsely matched `native_decide` in a block comment; its exit-1 log and source are preserved, the scanner was corrected to remove nested comments, and the final validator exits 0. One shell request failed before process creation with an exec-server transport-disconnected error. No such failure is called a Lean run or a mathematical failure. Fresh successful/failed scripts and raw output are retained in `publish-evidence`; original duplicated research is recovered by exact commit/path/blob/bytes/SHA-256 maps.

Root separately reported reading formal **COMMENTED** review `5554462533` at exact H, GitGuardian check `117230663315` success, empty legacy status entries, and zero Actions runs across event types. Those are root-observed platform facts, not independently refetched here; root retains the raw receipts. They do not replace this mathematical/evidence review or prove a platform approval gate is satisfied. Current readiness, target/base, combined tree, ownership and actual merge remain root responsibilities.

**Acceptance boundary:** this PASS covers H's exact 61-path increment, complete 21-module proof closure and honestly described retained verification. It transfers to a proposed integration only when root confirms identical canonical source/import/tooling pins, preservation of actual PR125 evidence, the additive F1 correction, and the actual applicable platform/ownership gates.
