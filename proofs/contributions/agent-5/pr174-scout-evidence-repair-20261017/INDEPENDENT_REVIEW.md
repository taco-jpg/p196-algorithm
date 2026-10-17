# Independent review of PR 174's fresh scout replacement supplement

## Disposition

**PASS for the frozen fresh data-only replacement supplement. Historical original scout preservation remains NOT_RECOVERED.**

The accepted supplement meets the currently reconstructible immutable task, named-source, and explicitly specified replacement-search obligations. Its new results are inspectable, repeatable and correctly bounded. It does not recover the historical branch/API transactions, original eleven-file selection, original search query/output or original failed/corrected index. It therefore cannot support a statement that the original archive was recovered, that the historical 3,334/245 query was reproduced, or that complete historical preservation compliance has been established. The package's `publication_gap_closed: false` is accurate.

This review was performed by `/root/pr174_scout_independent_review`, a separate nonauthor reviewer for Agent #5, session `d4d5258160f7`. The supplement author is `/root/pr174_scout_reverification`. I inspected the complete new checker and other package scripts, README/FINDINGS, completed manifests/results, retained failures, necessary exact task/source passages and the inherited qualification. I did not author or modify the candidate. I performed exactly one independent execution of its frozen data checker. No Lean, mathematical candidate evaluation, duplicate original semantic review, repository checkout, index change, source-branch mutation, coordination write, remote publication or network operation occurred in this review.

Acceptance is for the precise candidate inventory below. The parent delivery owner must preserve byte identity when packaging it, append an explicit historical preservation-gap correction, and bind the additive evidence to the eventual source head. This review creates no current ownership or merge authorization, and does not require a third-party platform APPROVE solely because project agents use the same GitHub account.

## Frozen candidate and provenance

The author explicitly confirmed by direct message that the final package contains **333 payload files / 50,376,696 bytes**, plus the two control files `FILES.json` and `SEAL.json`, and that no further edits are pending. I independently inventoried all **335 files**, checked exact path coverage, byte lengths, SHA256, Git blob-style content identity, local filesystem modes and intended Git modes against that inventory, rejected symlinks/duplicate paths and copied the inspected checker/human claims/control files into this review's `frozen-candidate/`. The full candidate remained unchanged after the independent run.

| Accepted item | SHA256 |
| --- | --- |
| Candidate `FILES.json` | `13067478dd7d8dad718ce042c8c0adc499116b7fd3ebd202388e83cb46c7dc91` |
| Executed `scripts/check.py` | `da0622e9fd38b6259955502c3d9ec2389e1fc54d25dd43d7cd9793bd6a743243` |
| Candidate `README.md` | `8fc4bd5b8a00e316ac5d722ca9b2e68a5d959225a457f3872787f489898c63b8` |
| Candidate `FINDINGS.md` | `62d1266a1b4706893fffff8b0636c4e9d4a5fd43187727314d68e2bb9c707f8d` |
| Inherited `EVIDENCE_REVIEW.md` | `1e37ed0cb5b921c2dd6a7ffee2a2de8e4887b2dc9458572e433699531a5df9af` |

`candidate-inventory.json` supplies every accepted filename and identity, including the manifest/seal themselves; the candidate seal is checked against the independently computed manifest hash. The inherited report is byte-identical to `agent5/pr174-evidence/EVIDENCE_REVIEW.md`, 18,625 bytes, and is correctly attributed as preexisting qualification rather than a new mathematical execution.

## Immutable inputs and complete selection

| Role | Commit | Verified tree | Recursive paths |
| --- | --- | --- | ---: |
| Historical coordination, COORD | `4c9e6e7aa08147f3798ffad8657c08512e7774c8` | `1956c527dd28622f5af4e3b4f03f6e240724e479` | 14,841 |
| Historical source checkpoint, SOURCE | `c42dd0b6accedd27424a9511f8c06b651d21779e` | `02899f94d687aa09bcbe893367fb8333abaf0621` | 16,536 |
| Original reviewed PR 174 head, H | `790ee166caf3c60c7176d53209e3e755e7ed9a9d` | `81ff4f9223331c35ab9424654a826e50a87b868f` | 16,665 |

The checker obtains and hashes the actual commit bytes, uses the pinned COORD and SOURCE trees for their distinct roles, and reads full recursive NUL-delimited Git tree listings. It never infers committed content from the intentionally partial worktree/index. Tree-path uniqueness is enforced, selected paths must be ordinary `100644` or `100755` blobs, and output paths reject absolute paths and parent traversal. The actual selected paths are canonical and collision-free. Git blob bodies are read with exact length/header checks and recomputed Git blob hashes; missing or malformed objects fail the run.

All **245** recursive COORD task paths are retained as exact bytes. Every selected task is strict UTF-8 and parses as a JSON object; my separate artifact audit also found no duplicate JSON object keys anywhere in those retained task records. Counts are observed, not forced to 245 by the checker. The nine-center task has the report-named blob `3208a10bccdcdcaa3556d683eff7bb9cc6afefe7`.

The search corpus is exactly every case-sensitive `.lean`, `.py` or `.md` path in SOURCE: **7,744 paths / 3,800 unique blobs**. All are decoded strictly as UTF-8 and checked for binary NULs. No undecodable/binary selected file was skipped. Shared blobs are read once for searching, while repeated archive/evidence paths remain separately represented in the output indexes and match counts. The API query applies only to the **6,757** `.lean`/`.py` paths; all **987** Markdown corpus paths still have explicit API-index rows marked unsearched. Files outside these extensions are outside the declared corpus; no broader completeness is claimed.

The seven principal SHA256 pins explicitly printed in the historical census are checked against their exact SOURCE path/blob bytes, with the same blob at H. Two further sources are plainly labeled NEW supporting selections: canonical `proofs/Agent1PeriodicCenterWrap.lean` and `proofs/periodic_word_quotient__8404d0a63dd1fa13.py`. Their addition yields nine new source copies, not a claim to know nine or eleven original scout members. The separately reported `Agent1PeriodicNinesCenter.lean` blob is not counted among either category. Its public recovery belongs to the sibling recovery package; no missing canonical path or original selection membership is invented here.

The published census itself is read from H as blob `aaf62e85c2a8f9ba272e3fdf79de0350b523cbe4`, 8,579 bytes, SHA256 `f233d4b20ab3c5010d0fb8e21e59d680e07057fd8ca2ca3bef39aa78d2031bec`. Its assertions about the missing original archive remain intact as historical source text.

## Checker safety and exact runtime

The checker uses explicit `require` failures for its validity conditions and refuses optimized Python before creating output. There is no removable `assert` protecting PASS. It requires a previously nonexistent output directory; the author's retained `-O` and existing-output guard attempts both exit nonzero, with appropriate error text. Inspection of the code and those retained receipts resolves these guard obligations; I did not add duplicate guard executions.

Source files are treated solely as bytes/text. The checker imports only standard-library modules. Its subprocess calls are immutable `git cat-file` and `git ls-tree` operations, without shell interpolation, repository source imports, execution of retained Python, Lean invocation or checkout. It sets `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0` and `LC_ALL=C`. One Python data-processing process runs with at most one sequential Git subprocess. The checker sets hard and soft `resource.RLIMIT_AS` to **402,653,184 bytes (384 MiB)**; the shell driver independently sets `ulimit -v 393216` before launch. No missing object or network retry occurred.

Exact independent checker command, preserved inside `scripts/run_once.sh`:

```text
python3 /workspace/scratch/d4d5258160f7/agent5/pr174-scout-independent-review/frozen-candidate/scripts/check.py --repo /workspace/scratch/d4d5258160f7/agent5/repo --output /workspace/scratch/d4d5258160f7/agent5/pr174-scout-independent-review/run-001
```

| Execution fact | Observed value |
| --- | --- |
| Start UTC | `2026-10-17T06:03:50.889190878Z` |
| End UTC | `2026-10-17T06:03:53.399851455Z` |
| Python | 3.12.14, `sys.flags.optimize=0` |
| Git | 2.51.1 |
| Checker exit | 0 |
| Checker stderr | Empty |
| Immutable Git invocations | 7, all exit 0; all stderr empty |
| Batched blob responses | 4,046 = 1 historical report + 245 task records + 3,800 distinct corpus blobs |
| Independent run count | Exactly 1 |

Full runtime stdout/stderr, exit, timestamps, limits and environment metadata are preserved at this review's root. The checker preserves its actual Git argv, exits, raw commit/tree outputs, batch requests and full response identity records under `run-001/`. The exact source/task copies, full matches and manifests remain lossless. This review's full **290 run files, including `run-001/FILES.json`, are byte-for-byte identical to the author's run**, not merely equal summary counts. `audit-results.json` enumerates every comparison.

Independent run manifest SHA256: `c6ab2ee6aab3fdcad51d95f62f521fb6e1ed680743bba73a7794db2df4745c82`.

Runtime stdout SHA256: `24bc9aaf2332b7e6ec62c11b2e6f9b031eaa70abdbfa7e22a94f0cc239ae77e9`.

Runtime stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Search results and counting semantics

| Fresh declared search | Searched paths | Matching paths | Complete matches |
| --- | ---: | ---: | ---: |
| Fixed-substring OR of 19 API/control terms | 6,757 | 650 | 9,104 matching lines |
| Exact `[9,9,9,14,18,18,14,9,9,9]` | 7,744 | 0 | 0 matching lines |
| Same coefficients with inter-coefficient whitespace/newlines | 7,744 | 0 | 0 occurrences |

The full query constants, strict decoding, extension selection, case sensitivity, comments/string/archive inclusion and ordering are explicit in both the frozen checker and `search-specification.json`. API hits are emitted once per split line per path, retaining all matched terms. The whitespace search uses whole-file `re.finditer` and counts occurrences rather than lines. The API line convention is explicitly Python `str.splitlines`; it should not be described as a universal LF-only `grep` convention. Exact H contains no newlines, and the supplemental query covers whitespace spanning lines. Neither query covers alternative algebraic syntax, aliases or semantic equivalence.

I independently parsed every raw JSONL match and every index row to check full path coverage, unique index paths, per-path eligibility, blob identity, exact line lists, per-path counts, total counts and matching-path totals. No truncation or colon/argv splitting occurs: paths, lines and object IDs occupy separate JSON fields. The two zero-result streams are retained as empty files, with complete negative indexes; absence of a match stream is not being used as a negative result.

These are genuinely new query results under a specified reproducible selection. **9,104/650 does not reproduce, correct or authenticate the unknown historical 3,334/245 query.** A zero textual result cannot establish comprehensive theorem novelty or exhaustive non-overlap.

## Bounded ownership and source-claim review

The declared discovery patterns select **87** task candidates. Exactly **five** match the narrower center-strip / extra-removal / strip-bound / closest-control / fixed-H groups; the report identifies those five plus four explicit adjacent validity/cycle/path scopes. I checked the relevant target, dependency, status and exclusion text against the retained exact task bytes. The report does not claim that all 87 broad matches were semantically adjudicated. No task text matches the declared whitespace-tolerant H pattern; that remains a raw-text observation, not a current ownership conclusion.

The central nine-center claim at COORD concerns the arbitrary wrapper identity and actual mixed-nine raw/residual-center formula with an existing inner count plus one. Its explicit exclusions preserve no descent/no-return and no affirmative-cycle search. The block-stripping task certifies the literal maximal algorithms while excluding full validity/safety/cycles/lifts. The safety task expressly disclaims safe-successor closure. Agent #6's carry-accounting claim expressly excludes Agent1 periodic stripping; Agent #61's task concerns documentation and replay navigation. The adjacent validity, guarded-path and cycle-adapter scopes remain conditional on their stated supplied inputs. The retained fields support the bounded comparison without granting a new present-day claim or releasing any historical lane.

I also inspected the exact relevant source declarations and literal implementation passages, without proving or evaluating the PR 174 candidate:

- `CenterControls.lean` displays the arbitrary `[1,2]` two-pair statement and the separate edge controls. Its statement contains no original-valid normalized-nine raw-image assertion.
- `Agent1PeriodicSafetyBoundary.lean` displays the period-ten input, actual quotient residual `[2]` and `centerPeriods = 1`.
- `Agent1PeriodicCenterStrip.lean` uses original center-length fuel, adds one per complete mirrored boundary pair and states decomposition/maximality/length. The inspected general interfaces do not state a universal one-pair bound on actual transitions.
- `Agent1PeriodicCenterWrap.lean` displays the existing count plus one, for nonempty `w`, and is accurately distinguished from the separately recovered NinesCenter blob.
- Guard, Digits, Quotient and Nines declarations support the report's original seven-field validity predicate, actual carry scans, raw slice offsets and common strip-result projections.
- The retained Python lines 42–59 contain the maximal center `while` loop and `absorbed_center_pairs=v`. Neither that function nor the historical traversal in `main` was executed. Its dependency blob is corroborated by the block-stripping task.

These checks support the replacement report's factual source comparison. The inherited mathematical qualification remains the basis for the fixed tuple's proof and its finite boundary. This review adds no proof of tuple return, infinite safe continuation, center descent/no-return, reachability from 196 or resolution of the 196 problem.

## Failure preservation and unresolved historical evidence

The candidate preserves the actual new acquisition chain: initial commit-fetch proxy failure (exit 128), successful approved retry (exit 0), initial selected-blob proxy failure (exit 128), failed promisor negotiation (exit 1, `bad revision` / missing necessary objects), and successful final fetch with the corrected no-negotiation flags (exit 0). Both helper versions, exact OID list, commands and captured streams are retained. The two earlier cache probes are explicitly transcript-derived observations because their original raw streams were not captured. The pipeline's zero status is correctly distinguished from the unrecorded Git exit. Those limitations are not concealed or relabeled as complete raw transaction retention.

My independent checker and output audit had no failures. A preliminary file-list command mentioned the not-yet-created review directory, and a later inspection command used mistaken `selected-blobs` filenames plus the wrong directory for `runtime.limits.txt`; those read-only inspection errors are retained as transcript-derived observations in `inspection-observations.json`. Correct paths were then read. They did not alter any candidate file or trigger another checker execution.

The following remain **NOT_RECOVERED**, and this independent PASS does not change that status:

1. Original task/API readback transactions and HTTP response archive, including issue 61 readbacks through proposal 6228357838.
2. Original two branch-list pages for the 162 historical branches.
3. Original unknown-query 3,334-line / 245-file search, initial colon/argv index failure and corrected original index.
4. Original eleven-file `source-pins.json`, exact membership and original snapshot layout. Seven named pins and two new selections cannot identify the missing four original selections.

Fresh immutable task bytes establish historical committed content; they do not establish the original API transaction. Fresh source matches establish this new query's complete results; they do not reconstruct an unknown original query. The accepted additive remedy is therefore **new verified evidence plus an explicit preservation-gap correction**, preserving the original report unchanged. Source-owner recovery remains preferable if its exact original locator becomes available, but this review invents no indefinite author-permission gate.

## Delivery handoff

The frozen author inventory and this review package are accepted as a lossless additive evidence pair under the stated limited interpretation. No candidate code defect requiring repair or extra test gate was found. The parent should publish the full author package and this independent review package, preserve both inventories/seals, and verify their bytes against the eventual additive Git tree. The original 157-file proof/registry evidence and accepted mathematical qualification remain unchanged by this review. Source write claims, current ownership refresh, delivery dependencies, source-head binding and actual merge disposition remain with the parent.

Primary review artifacts are `candidate-inventory.json`, `frozen-candidate/`, `run-001/`, `audit-results.json`, `environment.json`, `runtime.*`, reviewer scripts, this report and the outer `FILES.json`/`SEAL.json`. The run's own manifest is retained unchanged; the outer manifest supplies exact coverage of the complete review package with explicit self/seal exclusions.
