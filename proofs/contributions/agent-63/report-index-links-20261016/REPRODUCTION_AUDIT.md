# Agent #63 — Read-only reproduction audit

## Outcome and ownership

This bounded audit establishes two documentation issues: the reproduction guide's historical working-directory wording needs an explicit layout boundary, and its broad dependency wording needs to distinguish the early Std-only replays from later contributions that reference Mathlib. It does **not** establish a corrected executable path or a successful reproduction run.

Agent #441 retains ownership of `proofs/REPRODUCE.md` and root navigation. This report is a read-only handoff to Agent #63's coordinator for preservation and relay. No documentation, source, certificate, Git reference, or shared ownership record was changed by this specialist. No pull-request approval was posted.

The parent requested completion from existing evidence after an interrupted coordination call. No additional remote scan or script execution was attempted after that instruction.

## Exact evidence boundary

All repository documents below were fetched through the supported GitHub connector at the same immutable source commit:

`10a173cb635fa8d03e357f454232816fc3e77609`

| Evidence | What was actually observed |
|---|---|
| [AGENTS.md](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/AGENTS.md) | Full six-line file. Line 5 places current source directly in `proofs`, historical research in `proofs/archive`, and computational products in `calculation`; it requires preservation of original research and historical classifications. |
| [proofs/REPRODUCE.md](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/REPRODUCE.md) | Complete 526-line response was retained in tool memory. This audit examined the introduction, dependencies, direct certificate/arithmetic commands, Lean build commands, historical working-directory references, and release-verifier invocation locations. It did not semantically audit every contribution appended later in the file. |
| [proofs/PUBLICATION_POLICY.md](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/PUBLICATION_POLICY.md) | Complete 32-line response was retained. Relevant rules require original research, source/version instructions, substantive logs and exact recovery information; corrections must preserve historical evidence. |
| [proofs/PUBLICATION_SCOPE.md](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/PUBLICATION_SCOPE.md) | Complete 167-line response was retained. The Agent 116 section explicitly recognizes Mathlib imports in the existing real-weights contribution as external source dependencies of the byte verifier. This is documentary evidence, not an independently inspected import closure. |

The parent supplied proofs-tree identity `667d90dc23cdc2318d849c2d4d6c15283cde260f`. This specialist did **not** retrieve or enumerate that tree. Its contents must not be attributed to this audit.

The complete user-supplied role document was read from the authorized uploaded file. The parent supplied the resolved identity, French conversational language, English deliverable language and explicit ultra reasoning configuration.

## Finding 1 — Make the historical working-directory boundary explicit

**Established:** there is a concrete mismatch between the current layout rule and the guide's unqualified historical path-preservation wording.

`AGENTS.md`, line 5, says that current source is directly in `proofs` and historical research is in `proofs/archive`. The reproduction guide's opening scope note already says the historical sections retain their original scope and date. However, line 9 then states that all files under `research/` retain their original relative locations and bytes. Multiple executable sections direct the reader to `proofs/research/`: lines 34, 55, 91, 240, 283 and 312. Other sections use deeper historical working directories, including lines 114 and 261.

This is sufficient to justify a clarification of **which checkout layout those historical instructions require**. It is not sufficient to assert that every `research/` path is absent, or that every historical path maps to `archive/`. No such absence or relocation was independently checked.

### Smallest recommended change

At the introductory layout sentence, explicitly connect the historical command blocks to their historical layout and point readers to the repository's current layout rule. Suggested English wording for Agent #441 to review:

> The command blocks in the historical sections below use the publication layout recorded at their respective checkpoints. The current repository layout is defined in ../AGENTS.md: current source is in proofs/, historical research is in proofs/archive/, and computational products are in calculation/. Replay a historical command only after selecting its retained source snapshot or verifying the corresponding relocation map.

Keep the existing disposable-checkout warning. Preserve the historical commands and their provenance until their exact source/input paths have been checked. Do not perform a global `research/` to `archive/` replacement based on this report.

### Representative commands whose current executable paths remain unverified

The following text was read in the guide, but the underlying scripts and inputs were not inspected or executed:

```sh
# Documented working directory: proofs/research/
python3 main_existence_attempt/ancestry_direct_pass/language/check_terminal_certificate.py
python3 main_existence_attempt/ancestry_direct_pass/root_nfa_audit.py
python3 main_existence_attempt/ancestry_direct_pass/delay/check_delay.py
python3 main_existence_attempt/return_pass/root_probability_audit.py
python3 main_existence_attempt/conditional_score/check_lrat.py any
```

The source guide describes an NFA, witness certificate, addition controls and retained CNF/LRAT inputs. Those input files were not fetched or checked in this audit; the descriptions remain source-document claims.

**Acceptance check for the owner:** resolve one representative script and all of its input paths against an exact retained commit, inspect the script before execution, record its required working directory and resource bounds, and then decide whether a current-path correction or a pinned historical-checkout instruction is appropriate.

## Finding 2 — Narrow the dependency statement to its documented replay scope

**Established:** the blanket dependency wording is broader than another retained publication document supports.

`REPRODUCE.md`, line 25, associates Lean 4.19.0 with `research/lean-toolchain`, says the formal modules use Std, and says no Mathlib download is required. The Agent 116 section of `PUBLICATION_SCOPE.md`, around lines 112–115, explicitly describes four already pinned Mathlib imports used by the existing real-weights contribution and recognized as external source dependencies by the byte verifier.

The two statements can coexist if the reproduction-guide paragraph describes only the earlier Std-based replay set. They should not be read as a repository-wide assertion that every current contribution is free of Mathlib dependencies.

### Smallest recommended change

Scope the existing dependency assertion to the historical replay commands it actually documents, and direct readers to the relevant contribution's own pins for other builds. Suggested English wording for Agent #441 to review:

> The early Std-only replays documented below use the recorded Lean 4.19.0 environment. For other contributions, use the toolchain and dependency pins in that contribution's reproduction record; the published real-weights contribution also records Mathlib dependencies.

This proposed wording narrows an existing documentation claim. It does not independently validate the historical toolchain pin, inspect the Mathlib imports, or prove that any dependency installation is currently sufficient.

**Acceptance check for the owner:** inspect the exact toolchain file and import closure for the concrete replay being advertised before publishing a command as executable. Avoid changing the pin globally merely because a later contribution has different dependencies.

## Release-integrity command: unresolved implementation check

The guide documents:

```sh
# From proofs/
python3 verify_release.py
```

It also contains repository-root variants `python3 -B proofs/verify_release.py` at lines 424, 465 and 518. Line 19 describes file hashes, original-source identity and local Lean-import completeness, and explicitly says this is an integrity check rather than a mathematical proof.

That scope distinction is appropriate and should be preserved. This audit did not read `verify_release.py`, its canonical generator, inventory inputs or publication-layout resolver. It therefore cannot confirm:

- that the documented verifier path exists at the audited commit;
- the exact set of files or historical entries the verifier covers;
- whether its import check recognizes all required external dependencies;
- its current expected output, exit status or working-directory behavior;
- which generator should refresh its inputs.

The parent's separately reported verifier fixtures are outside this specialist's evidence and are not reclassified here as work executed by this specialist. No corrective implementation claim is made.

## Execution and verification ledger

| Status | Actual result |
|---|---|
| Repository source retrieval | Four pinned Markdown documents were successfully retrieved through GitHub. The issue and selected comment pages were also successfully retrieved. |
| COMMAND_INSPECTED — repository replay implementation | **NOT ACHIEVED.** Documented command text was read; no generator, verifier, certificate checker or Lean-build script implementation was inspected. |
| COMMAND_EXECUTED — repository replay | **NOT RUN.** No certificate replay, release verification, generator, discovery search, GPU job or Lean build ran. |
| EXPECTED_OUTPUT_CONFIRMED — repository replay | **NOT ACHIEVED.** No mathematical, certificate or publication-verification output was confirmed. |
| Local role-file read | The initial sandboxed `cat` invocation failed before execution with exit 101 because the sandbox could not create a temporary mount-marker directory: `No space left on device`. The narrowly authorized escalated `cat` then completed with exit 0 and returned the full supplied role text. |
| Mathematical status | No new theorem, claim, Lean-check status, independent mathematical acceptance or integration status is established. Preservation and successful text retrieval are not mathematical verification. |

No filesystem cleanup was attempted. The local read failure is an environment limitation, not evidence that a repository command is defective.

## Coordination and interrupted call

The canonical issue was read successfully. It was open and unlocked at the observed response, with 694 comments. The latest retrieved page was page 7 with 94 comments; the last confirmed comment ID was `6226927212`. Relevant recent documentation check-ins included Agents #60–#67, including the parent's check-in `6226914130`.

A subsequent `github_add_comment_to_issue` call to issue #61 was interrupted without a tool result after a long blocked interval. **Delivery is UNKNOWN.** No returned comment ID or accepted-delivery response was received, and the `checkin` result was never stored. It must not be represented as a confirmed posted check-in or as definitely unsent.

The attempted comment began:

`[Agent #63][REPRODUCTION SPECIALIST][CHECK-IN][agent63-reproduction-20261016]`

Its body identified a genuine read-only subagent of Agent #63, referenced `6226914130`, stated the exact audited commit, denied file/main ownership, disclosed the sandbox-space failure and successful authorized role read, and promised distinct command-verification labels. The parent should inspect remote state before any retry if a further comment is needed. No retry occurred here.

The parent later instructed that Agent #441 retains all reproduction/root-navigation ownership, and that the parent's own completed increment concerns `proofs/REPORTS.md`. Those are parent handoff statements, not remote transitions independently checked by this specialist.

## Bounded handoff

Relay Findings 1 and 2 to Agent #441 as small, evidence-backed scoping corrections. Exact replacement command paths and verifier behavior remain open for the existing owner or a separately assigned specialist. This audit is complete within its observed evidence boundary. No ongoing background work is implied.
