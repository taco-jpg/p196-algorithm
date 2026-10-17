# PR 174 scout preservation recovery: bounded negative result

## Decision

The original `nines-extra-control-scout` bundle was **not located in the inspected accessible paths**. This does not establish that it is absent from the author's environment, another machine, ignored/hidden paths, archives, or inaccessible directories. The original preservation gap remains open. This package records recovery searches and a newly established public-source mapping; it does not replace the original scout bundle.

No Lean, build, mathematical experiment, new mathematical review, remote mutation, claim, or author-source edit was performed. Author Agent #1 remains the source owner. All writes made by this recovery task were confined to this output directory.

## Missing original material

The published `scope/source-census.md` and byte-identical `review/scope-report-snapshot.md` state:

- Line 7: full exact 245 task records and API readbacks were retained; the census identifies coordination commit `4c9e6e7aa08147f3798ffad8657c08512e7774c8`, two branch-list pages covering 162 branches, and issue 61 comments through 6228357838.
- Line 21: the complete Git-tree source search at `c42dd0b6accedd27424a9511f8c06b651d21779e` produced 3334 matching lines in 245 files; the raw output, initial incorrect colon/argv split, and corrected index were retained.
- Line 49: eleven selected source snapshots, Git blobs, and SHA256 values were in `nines-extra-control-scout/source-pins.json` and `source-files/`.

No original bundle, eleven-file manifest, original task/API archive, historical raw search output, or failed/corrected historical index was recovered. No historical failure was recreated or represented as recovered evidence. The seven principal pin hashes and the separately reported center-source hash remain directly available in the published report.

## Bounded local search

The exact recorded argv, working directories, exit statuses, output sizes, and SHA256 values are in `search-commands.json`; complete recorded stdout/stderr are under `raw/`. `scripts/search.py` is the exact executed recorded-search helper.

1. Filename-only searches used `rg --files` on `/workspace` and `/tmp`, including exact scout directory/name patterns and the report/pin/scout filenames. They used ripgrep's normal hidden-file, ignore, and symlink behavior and explicit exclusions for node_modules, vendor, and cache paths. They did not search arbitrary file contents throughout these roots.
2. Both filename searches exited **2** because `/tmp/codex-daemon-0` was inaccessible (`Permission denied (os error 13)`). The positive filename results were retained. No matching original scout bundle was among those results. The inaccessible directory was not bypassed.
3. Content searching was restricted to the already published PR 174 research evidence directory. Public receipts authenticate references to `/workspace/p196-agent1-session-20261016`, `/workspace/p196-agent1-nine-control-20261017`, and `/workspace/p196-agent1-nine-center-20261017` as historical workspace paths used by the author's work. Probes of those exact directories all returned `No such file or directory` in this environment.
4. `/workspace/p196-agent1-session-20261016/nines-extra-control-scout` was probed only as an explicitly labeled **inference** from those historical references. No inspected public receipt authenticated that exact absolute scout path. The probe returned `No such file or directory`.
5. The PR 174 evidence agent's preexisting `scout-path-search.json` records a complete H-tree path search over 16,665 paths with only `scope/source-census.md` matching its scout/census pattern. This recovery report does not infer absent committed content from the partial worktree or index. That prior search is attributed to the evidence qualification package, not claimed as a new independent full-tree census here.

Initial reconnaissance commands were displayed through execution tools; some displayed output was truncated. The subsequent recorded searches retained complete stdout/stderr and exact commands. They are recorded executions, not asserted byte-identical substitutes for earlier tool-display output.

## Public provenance correction

GitHub's immutable commit readbacks establish that `c42dd0b6accedd27424a9511f8c06b651d21779e` is the **source** commit titled `lean(agent-1): prove exact maximal center-strip wrapper identity`, with parent `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`. Its tree is `02899f94d687aa09bcbe893367fb8333abaf0621`.

The coordination checkpoint is `4c9e6e7aa08147f3798ffad8657c08512e7774c8`, titled `coord(agent-105): preserve checkpoint and record corrected WIP`, with tree `1956c527dd28622f5af4e3b4f03f6e240724e479`. These are distinct source and coordination roles. The original census itself distinguishes them correctly.

Raw GitHub tool responses for both commits and the c42 diff are retained. Public task paths use `proofs/coordination/tasks/`, as the published `registry-preflight/claim-read.json` demonstrates. This identifies a concrete immutable source for a newly labeled reconstruction of task contents; it does not recover the original HTTP/API readbacks or prove their historical coverage.

## Newly verified source mapping

`public-pin-mapping.json` contains read-only local Git tree/object attempts. Lazy fetch was disabled. Seven principal source paths have identical Git blob identifiers at base `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`, published source `bfa0247b78845558d087eec08e113e91decaaddb`, and H `790ee166caf3c60c7176d53209e3e755e7ed9a9d`.

Four local blob reads succeeded. Three failed because their object bytes were not cached; those errors and empty stdout files are retained as failed attempts, not valid source snapshots. Four subsequent public GitHub blob reads succeeded: those three missing local blobs and the separate locally observed center source. Git object SHA1 was recomputed from the exact UTF-8 bytes and Git blob header, and all four matched their requested object IDs. Their SHA256 values also matched the report. Thus all seven principal report pins have matching public bytes.

| Principal report pin | Repository path | Git blob |
| --- | --- | --- |
| Guard | `proofs/Agent1PeriodicGuard.lean` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` |
| Digits | `proofs/Agent1PeriodicDigits.lean` | `6a6f02ae17d7aaa8e728a6588edf080c9ffd7ad5` |
| CenterStrip | `proofs/Agent1PeriodicCenterStrip.lean` | `bfcfd913cfd7b4063c9b632f2b0461aafd9ca437` |
| Quotient | `proofs/Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` |
| Nines | `proofs/Agent1PeriodicNines.lean` | `fc4b17311a291870b122ff97e3618fb7452e978e` |
| CenterControls | `proofs/contributions/agent-1/periodic-block-strip-20261016/center-author/CenterControls.lean` | `d9fa552d701444c1150f67f88161cb602ddc86c1` |
| SafetyBoundary | `proofs/Agent1PeriodicSafetyBoundary.lean` | `6120d6930d9e2e306aaacb233ebd3f1a369e54ea` |

The c42 source commit's authenticated parent and complete 28-file REST diff show only additions, with none of those seven paths changed. **Inference:** those seven public bytes are therefore also the bytes at c42. This is source-identity reasoning, not a repetition or confirmation of the historical 3334-match source search.

The report's separately observed `Agent1PeriodicNinesCenter.lean` blob `e6f1850b5e2e1f56491f88fbe92d587b9c739e77` is publicly retrievable and matches report SHA256 `7d6d27081c480345e796c6b8e950c08a5ce0d7207e4030d24e504db4abde695e`. Its canonical path is absent from the queried base/source/H trees. No publication-tree location, scout selection membership, or c42 presence is asserted for it.

`public-pin-mapping-supplement.json` contains successful public readback identities and the c42 inference. The missing eleven-file original manifest is still required to establish the complete eleven-file selection, its original filenames, and snapshot provenance. The seven principal pins plus the separate center pin do not justify guessing the remaining selection.

## Recovery-process failures retained

- Filename-search permission failure and exact-path ENOENT probes: `search-commands.json` and corresponding raw stderr.
- Local c42 object probe and three uncached local blob reads: `public-pin-mapping.json` and corresponding raw stderr. No missing committed source was inferred from these cache misses.
- The first supplement script incorrectly expected raw GitHub REST blob JSON; the connector actually supplied decoded UTF-8 content. This produced `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` on the initial invocation (execution chunk `84c21e`, exit 1). The original helper is retained as `scripts/public_mapping_supplement.attempt-001.py`. A second unchanged invocation preserved full stdout/stderr and exit 1 under `raw/public-mapping-supplement.attempt-002.*`. The corrected third invocation passed and has its own complete output and exit record. These are new recovery-process failures, not the missing historical colon/argv failure.

## Concrete next step

The most direct closure is for author Agent #1 to supply the original `nines-extra-control-scout` directory, or an already published immutable commit/path that contains it. Preserve exact original bytes, filenames, modes where available, source paths, and SHA256 values; include all 245 task/API readbacks, original raw source-search output, both historical postprocessing attempts, and the eleven-file manifest and snapshots.

If the original bundle cannot be recovered, publish an explicit preservation-gap correction identifying the missing materials and retaining the existing report as historical. A separately labeled reconstruction could retrieve the immutable coordination task tree and source checkpoint, but it would be **new evidence**. It cannot reproduce historical branch-list state, original HTTP responses, or the original failed-index output by assertion. No such expanded reconstruction or hundreds of source/API queries was started by this task.
