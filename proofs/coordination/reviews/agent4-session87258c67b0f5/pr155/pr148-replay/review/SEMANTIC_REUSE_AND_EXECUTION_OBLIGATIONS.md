# PR 148: existing semantic review reuse and missing execution obligations

## Disposition

**SEMANTIC_REVIEW_REUSE: QUALIFIED. NEW_EXECUTION_EVIDENCE: PENDING.**

The retained independent final semantic review applies to the exact five-module source closure at PR 148 head `7360b12a0a5889761c845a56a4b8d8a1df5f39b5`. It is a review of the implemented statements and proofs, not merely a preimplementation contract review. Its source hashes and reviewed task hash match the actual Git blobs at that head. A redundant new mathematical review is not required by the evidence inspected here.

The existing semantic review expressly leaves a fresh independent full-closure build as a separate acceptance gate. The missing complete historical execution corpus has not been recovered. The proposed work must therefore be labeled a **new exact-source reproduction**, not recovery of the original reported 117-result package and not an assertion that a historical execution occurred in this session.

This report qualifies existing evidence and specifies the uncovered verification obligations. It does not claim that the new replay has run, that PR 148 is integrated, or that any platform or target-write gate has passed.

## Role, authorization, and ownership

Reviewer: Agent #4's genuine independent nonauthor subagent `/root/pr155_independent_review`, operating in a narrowly delegated evidence-review role. The reviewer did not author the source contribution or the original semantic review and will not write the execution scripts or run Lean.

The delivery owner reported the following refreshed coordination facts:

- Agent #28 retains delivery of PR 148; its task explicitly permits nonexclusive read-only verification.
- Agent #51 retains the source scope; Agent #31 retains the main-write role.
- The scout found no other active replay at the checked coordination state `e0fcabbd...`, reported in comment `6230418026`.
- Agent #4's PR 155 task moved to `REPAIRING_DEPENDENCY_EXECUTION_EVIDENCE` at coordination commit `6cd993cac43234fe654fb19c6e171b6638b00941`, with the actual announcement in comment `6230444562`.

These coordination facts were supplied by the parent and are not represented as independent remote reads by this reviewer. Before that scope confirmation, this reviewer performed only local read-only source and identity inspection. The new report was saved only after the parent explicitly confirmed the scope. No ownership transfer, source mutation, remote write, or main integration is authorized by this review.

The full role safeguards previously read from `upload/Pasted text(20261017-045753).txt` continue to apply. The genuine independent review assignment remains separate from the parent's script authorship and compiler execution. The continuing subagent retains its creation configuration; the follow-up tool exposes no new reasoning-effort selector and no new configuration change is claimed.

## Examined evidence and exact identity

Read directly from Git at exact H148:

- `proofs/Agent51OverflowSaturation.registry.json`.
- `proofs/contributions/agent-51/spectral-overflow-saturation-20261016/review/FINAL_REVIEW.md`.
- The contribution README, retained task, dependency pin, and publication receipts.
- Full `Saturation.lean` and `OverflowWitness.lean`, to compare the source-facing statements and dependency interfaces with the existing review, without initiating a second full mathematical review.

The exact `OverflowDigits.lean` and `ResidueSums.lean` sources were already read in full and accepted in this reviewer's separate PR 155 review. Hash equality, rather than an assumption based on filenames, establishes their reuse here. The retained original spectral source report was also previously read in full; its hash was checked again at H148.

| Artifact | SHA-256 |
|---|---|
| Registry | `7622d9321f96acecb583ac1958cc72691fa5e3da92fc044908464d4d6fd767e3` |
| Existing `FINAL_REVIEW.md` | `a518fc3264ee25c719c5df954b9d51a7d24b094fc159b4f3239c8bb345dbe986` |
| Retained `evidence/task.json` | `26e1db864e187e33a40b7c3283f350121df47677d47624a903b2dac1356c38af` |
| Original spectral research source | `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09` |
| Unchanged canonical verification implementation | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |

The original research blob is `eac5b8f61385a615d9cc3e7796a4d698c66b716b`, retained at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md`. The selected claim is its overflow-saturation passage, lines 177–193, not the entire quotient classification.

All five module SHA-256 and Git blob values agree with the registry and with the existing review's explicit hash table:

| Module | SHA-256 | Git blob |
|---|---|---|
| `LychrelDigitSums` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | `8a865176625283648a8a20dd2411ed77670eb0a2` |
| `OverflowDigits` | `65adeb3ae7bea93e390a95fc5f8b58ec43f0f64f01ed9db3f51392657ba89a41` | `6ad7ea581c1ed9e6f8c4907dcb5ad73558423b97` |
| `OverflowWitness` | `fbf7568256e31948a20563e5d9e1335ce45b6859d2343917395180970114c901` | `b471a4805403a81180a4aef6d7bc1f78e565be17` |
| `ResidueSums` | `1333e156e2da6f02a18ff67f83e8ce36955e93c00e425cf67aff713f916140d4` | `f1e3c1c5e7cd780b28f6752d980158bd9b9c98b6` |
| `Saturation` | `e2379506a0b70c1502fea88e8daff4241282be73f6f11672effff182a10bc722` | `e426170f6eecdb35ee366b0262e551a7c6e099b2` |

The dependency path `proofs/LychrelDigitSums__0810ace083af80c5.lean` is intentionally copied to the fresh build's canonical local module filename `LychrelDigitSums.lean`; this is the registered import name and does not alter its bytes. No `OriginalLychrel` substitute or alternative foundation is authorized.

## Why the existing semantic review remains applicable

`FINAL_REVIEW.md` explicitly says its nonauthor reviewer read the four frozen contribution modules, verified their hashes, compared actual propositions and definitions against the original source and accepted contract, and inspected attributed author-run axiom logs. It records the foundation's exact pin and carefully separates its semantic PASS from fresh independent rebuilding and integration.

The implementation inspected at H148 matches that reviewed contract: `overflow_saturation` universally quantifies over every `L ≥ 18` and `s < 9` and supplies one common positive natural witness and canonical digit function satisfying nonpalindromicity, actual terminal carry one, palindrome next reverse-add output, exact canonical width L+1, and the literal divided polynomial residue coordinates. The even and odd corollaries retain the source thresholds 18 and 19. The witness module uses the original numeric canonicality, carry, and palindrome interfaces described by the review. No changed statement, hidden added premise, alternate residue definition, or source discrepancy was found in this comparison.

The retained review addresses the relevant boundary questions explicitly: disjoint digit blocks under `2*k ≤ L`, the boundary L=2*k, leading digits, actual input versus symbolic state, bounded coefficient equality, signed evaluation at −1, division before remainder, finite residue selection inside an unbounded-width proof, and common-witness quantifier order. None of those obligations needs to be reopened solely because execution logs are missing.

The retained task's historical status text predates completion and the existing review's publication discussion mentions an earlier partial checkpoint. Those historical labels are not evidence that H148 lacks its final modules: the actual H148 blobs now checked match every reviewed final hash. Nor do the historical labels establish the outstanding independent execution gate. They must remain accurately preserved rather than being silently rewritten into a new execution receipt.

## Registry coverage and reusable PR 155 evidence

The registry contains exactly 52 distinct explicit public declarations from the four contribution modules: eight in `OverflowDigits`, 28 in `ResidueSums`, eight in `OverflowWitness`, and eight in `Saturation`. A source declaration comparison found no missing, extra, or duplicate registry names. The three final endpoints are:

- `P196.Agent51.overflow_saturation`.
- `P196.Agent51.even_overflow_saturation`.
- `P196.Agent51.odd_overflow_saturation`.

The 52 count is **not** a claim that the entire five-module environment has only 52 public declarations. `LychrelDigitSums` is an unchanged substantial original foundation, 5,490 source lines in the pinned blob, with many historical declarations outside that new-interface list. Every theorem and every safe definition originating in that module must still be included in the module-origin audit. Namespace filtering only for `P196.Agent51` would miss that obligation.

PR 155's successful canonical003 run and supplemental002 audit already provide qualified exact-byte source and axiom evidence for `OverflowDigits` and `ResidueSums`. They do not compile or audit `LychrelDigitSums`, `OverflowWitness`, or `Saturation`, and therefore cannot by themselves discharge PR 148's full closure. Their source identity and the canonical verifier/launcher procedure can be reused without restarting the PR 155 review.

For the new canonical replay, compiling all five sources into a new directory is appropriate: the unchanged canonical implementation intentionally creates a fresh full selected closure. Recompiling the two small overlapping modules as part of that coherent replay is a scoped procedural choice, not a reason to claim that their previous evidence was invalid or to repeat its mathematical review.

## Concrete outstanding execution obligations

1. **Freeze exact inputs and context.** Use a detached checkout at H148, the exact registry above, all five source blobs, and the unchanged canonical verifier. Record actual checkout HEAD, clean tracked-source state, compiler binary/version/shared-library hashes, effective command and environment, and before/after source identities. No accepted source rewrite is needed.

2. **Compile the entire local closure from source.** The expected dependency order is `LychrelDigitSums`, `OverflowDigits`, `OverflowWitness`, `ResidueSums`, `Saturation`. Each invocation must have a real exit status and complete retained log, use Lean 4.19.0 commit `6caaee842e94`, and actually enforce `--trust=0 -j1 -DElab.async=false`. Failed, killed, or timed-out processes are not passes. Shipped Init/Std/Lean remain runtime dependencies; compiling five local modules does not mean rebuilding the compiler's complete standard library.

3. **Retain a coherent canonical report.** The original `proofs/verify_project__214bf7673efe116b.py` is byte-identical to the implementation already reviewed for PR 155. Its explicit selected-project mode may legitimately return a scoped PASS while `catalogue_complete` and `repository_wide_pass` remain false. Its inherited hardcoded agent metadata must not obscure who actually executed the new replay. Preserve all actual raw module and generated-audit logs, not merely a summary count or successful badge.

4. **Audit all module-origin theorem declarations.** The generated audit must select all five modules, including the large original foundation and generated/private proof declarations. It must reject safe custom axioms and any transitive theorem dependency outside `propext`, `Classical.choice`, and `Quot.sound`. Actual declaration rows, unique counts, final summary, and excluded unsafe implementation artifacts must be retained. No result count is presumed from the missing historical corpus.

5. **Audit the exact 52 public interfaces and all safe definitions.** The separate supplemental inspection should contain exact literal `#check` and `#print axioms` commands for those 52 registry names. Its module-origin traversal must inspect every safe definition and nonunsafe opaque declaration in all five modules, reject forbidden dependencies, and report unsafe/partial compiler artifacts separately. Its result cannot omit foundation declarations merely because their namespace differs. The already repaired PR 155 `eligible : Bool` annotation should be retained.

6. **Bind the supplemental result to the new objects.** Use only the fresh objects from the new successful canonical run. Record their hashes, source hashes, the audit source and driver hashes, actual `LEAN_PATH`, actual compiler argv/cwd/limits, exit and full output, and stable input hashes after inspection. Import-based audits inspect the freshly built environment; they do not themselves recheck proof bodies inside preexisting objects.

7. **Preserve and label the new evidence accurately.** Retain any failed new attempt and diagnose the exact cause before a corrective rerun. Do not overwrite the frozen PR 155 package. The original missing independent execution remains `NOT_RECOVERED`; a successful new replay may satisfy the current gate under its own provenance. Existing author compilation remains author evidence and the existing final semantic review remains the reused semantic review.

## Procedure reuse and next review boundary

The approved final PR 155 launcher has SHA-256 `a9d32e8bb8658a25b799d3bf2f466c8862a95e25b8fd2e44ab042af931b11dec`. An exact copy may be reused in the new evidence directory. It pins executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, adds explicit trust zero, rejects the inspected short/long trust and memory overrides, records actual compiler arguments, enforces a hard 4 GiB `RLIMIT_AS`, and preserves the actual exit through `execv`. The new location changes only where its relative launch log is stored. The previous 2 GiB import failure and `-M1024` incompatibility are known procedural facts already diagnosed in the PR 155 package; there is no reason to reintroduce those failing configurations.

### Pre-execution procedure inspection: approved

The reviewer subsequently read `prepare_inputs.py`, `run_canonical.py`, the copied `strict_lean.py`, the generated `PublicAndSafeAudit.lean`, and `source-freeze.json` in full. The concrete procedures are **APPROVED for the new bounded sequential attempt**. Independent read-only checks, retained in `preexecution-inspection.json`, confirm a clean real detached worktree at H148 and exact three-way equality between Git H148, the worktree, and the preserved snapshot for all 30 input files.

| Reviewed procedure/input record | SHA-256 |
|---|---|
| `prepare_inputs.py` | `d6c2024f38ffdb202aa78e1501c3d1e68585a2e1507692a2ba953b76e689022e` |
| `run_canonical.py` | `877a6930219af226071760fe626d00f9ba6ed2eda6c753d65ebedfe7d715d5bb` |
| `strict_lean.py` | `a9d32e8bb8658a25b799d3bf2f466c8862a95e25b8fd2e44ab042af931b11dec` |
| `PublicAndSafeAudit.lean` | `dba2697be8a32bc8b8543ec85a502addee82403910bd7b6fba758264d60da32d` |
| `source-freeze.json` | `3129d916d1e2ae22f98f5fdd523308522fbb624894e35914403e4da78b046454` |

The input preparation guards exact source HEAD and clean tracked state, copies rather than edits published evidence, independently checks all selected source bytes against Git, verifies the registered module pins, and retains the original `NEW_EXECUTION_NOT_ORIGINAL_ARCHIVE_RECOVERY` classification. It does not execute Lean. The new audit contains exactly the registry's 52 `#check` and 52 `#print axioms` commands in their correct order. Its actual `run_cmd` body is byte-identical to the previously successful PR155 audit after the sole five-module selection substitution; the fixed explicit Bool annotation and every axiom rejection remain intact. The root import is correctly changed to `Saturation`.

The execution driver rejects an existing attempt output/receipt/console, rechecks every frozen file and launcher, requires actual H148 and a clean tracked worktree, and invokes the unmodified canonical verifier. Its six-hundred-second external bound applies to a newly created process group; timeout cleanup targets that launched group, not unrelated jobs. Its observations traverse only the launched verifier's descendant processes and distinguish those observations from shared cgroup counters. It retains raw canonical logs and records the real process exit. On success it requires the canonical report's PASS, exact source commit, clean-source flag, and unchanged source inputs. It does not alter the mathematical acceptance criteria.

The 4 GiB process address-space cap is approved as a bounded attempt, **not certified as sufficient for the larger foundation**. The parent supplied a historical source-build observation of approximately 74 seconds and 2.35 GiB peak RSS under a 6 GiB address-space cap. RSS alone does not establish virtual-address sufficiency under 4 GiB. Any resource failure in the new attempt must remain a failed execution with a specific diagnosis and a justified bounded remedy; it cannot be treated as a source theorem failure or a pass. No speculative resource change or extra mathematical review is required before observing the actual attempt.

The subsequently supplied `run_supplement.py`, SHA-256 `35b63d169bbdd8bda97c4103bafd07e07be8bcae76a4fbab0adbfff2f404b581`, was read in full and is **APPROVED before execution**, contingent on a genuinely successful canonical attempt. It requires the canonical PASS, exact H148, clean-source flag and scoped rather than repository-wide classification; verifies the audit and launcher pins; checks canonical compiler/library identities before and after; sets `LEAN_PATH` to the chosen new canonical source/object directory; records all five source/object hashes; and preserves the actual log and exit in a new, nonoverwriting supplemental directory. Its 180-second timeout controls only its new process group. Output validity, unique counts, module coverage, axiom sets, source/object identity, and actual command binding will still be independently inspected rather than inferred from the driver status.

Root remains the script author and compiler executor. No Lean execution or script authorship is performed by this reviewer. Actual canonical/supplemental logs still require evidence inspection. Pre-execution approval does not populate their outcome.

Even a complete new source/axiom replay would establish only the selected PR 148 source closure. Prerequisite delivery ownership, current-main combination, platform requirements, main-write authorization, actual merge, and post-merge validation remain separate delivery obligations. No repository-wide acceptance or all-time 196 conclusion follows from this report.
