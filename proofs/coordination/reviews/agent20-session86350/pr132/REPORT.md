# PR132 Existing Evidence Validation

## Decision and scope

**PASS_REUSE_EXISTING_EVIDENCE.** The published replay evidence is byte intact and binds the complete 27-module source closure to the preserved successful build records and all 1,881 actual theorem-axiom outputs. No uncovered proof obligation requiring another Lean build was found in this evidence-validation assignment.

Reviewer: Agent #20, session `86350e418736`, genuine specialist `/root/pr132_evidence`. This specialist did not author or edit the four Lean modules, the upstream reproduction driver, or the historical audit. The present work is executable integrity and evidence-binding validation; it does not claim a newly executed Lean proof check.

- Repository: `taco-jpg/p196-algorithm`, PR132.
- Publication head checked: `43219b02c191325d0263b4ad2fa1f4ebb1470a5c`.
- Frozen four-module source commit: `1908a7e91d4c45c9ce455235f40d4b627af7e4d9`.
- Contribution: `proofs/contributions/agent-103/residual-five-firsthit-two-20261016/`.
- Fresh Lean execution in this assignment: **NOT_RUN**.
- Remote writes, review requests, merges, retargeting, coordination mutations: **NONE**.
- Source edits or proof weakening: **NONE**.

AGENTS.md and `proofs/PUBLICATION_POLICY.md` were read at the pinned head. An initial root-level PUBLICATION_POLICY.md lookup returned 404; the correct proofs path was then read successfully. That failed lookup is retained under retrieval. No authentication material was accessed.

## Published files and archives

All 24 paths returned by GitHub's complete PR changed-file list were fetched at the exact head. For every path, the local bytes were hashed with the Git blob framing and matched the connector's blob identity. Binary XZ responses were requested as base64 and decoded losslessly. Their base64 transfer forms are retained.

| Archive | Compressed bytes | Regular members | File payload bytes | Uncompressed tar bytes |
|---|---:|---:|---:|---:|
| complete-replay-evidence.tar.xz | 189180 | 203 | 3107160 | 3266560 |
| development-evidence.tar.xz | 15096 | 33 | 68219 | 102400 |

Complete archive SHA-256: `b8fdab43cb48d3d507e52143e90e634d65ce7c7c1080f58c34f08881c42a6fef`.

Complete archive Git blob: `e6cb64f9de5cc5a86c7e67d5fc6f2a935d5c3b41`.

Complete decompressed tar SHA-256: `3181f023b0183a02f53d2c4759856ffaa5e624ccaf6d7053afda6e78425bca3c`.

Development archive SHA-256: `3d4a257cecf4b787383c2987533e3b1bfcdf259b553e04856af5b08fd75daf14`.

Development archive Git blob: `65d1a382374f6222fed42f414ae1631ea518f98a`.

The complete archive contains exactly the 202 paths indexed by its FILES.json plus FILES.json itself. Every indexed size and SHA-256 matched. Its embedded FILES.json is byte-identical to the published top-level FILES.json. Member names are unique, relative, sorted, and contain no traversal. All are regular files; no links or objects were extracted. The complete archive also matches the advertised deterministic tar metadata: 0644, zero uid/gid/mtime, empty owner names, no PAX headers.

The development archive contains its 32 indexed original files plus FILES.json. Every member matches the development manifest and the corresponding `author-history/` member of the complete archive. The published development manifest also exactly matches the preserved `author-history/DEVELOPMENT_ARCHIVE.json`.

The 86 entries in the nested full-verification FILES.json and 28 entries in the nested registry-check FILES.json were independently size/hash checked. Fifteen same-named published/archive root files are byte-identical, including the driver, SOURCES, registry, final reviews, safety ledgers, and all four new Lean modules; the separately published vendored Agent101PalindromeFibers also matches its archived source.

## Exact source map and input closure

The source manifests, original snapshots, compiled snapshots, build report, and published registry agree on exactly **27 modules: 23 dependencies plus four new modules**. Their import graph has one root, `ResidualFiveFirstHitConclusion`, reaches all 27 entries, has no unused manifest dependency, and matches the recorded successful compile order.

A further **49 independent GitHub commit:path lookups** matched immutable Git blob pins: all 23 original dependency sources, 22 published-head dependency paths not already included in the 24 changed-file fetches, and the four new modules at the frozen mathematical commit. The four head sources and newly vendored dependency are bound by the initial 24-path fetch. Original source bytes and compiled snapshot bytes were independently SHA-256 and Git-blob hashed.

The only source transformation is the documented foundation compatibility forwarder. The original foundation after its exact `import Std\n` prefix has 177451 bytes and 4444 lines. It occurs uniquely in LychrelDigitSums at byte offset 329, starting line 11. The compiled compatibility source is exactly `import LychrelDigitSums\n`, with SHA-256 `13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011`. All other original and compiled module bytes are identical.

The complete commit/path/blob/SHA/import map is retained in EVIDENCE_BINDING.json and `retrieval/remote-source-bindings.json`. Module-origin theorem counts independently recovered from the raw audit are:

| Module | Group | Theorem constants |
|---|---|---:|
| `LychrelDigitSums` | dependency | 986 |
| `PrefixInverse` | dependency | 45 |
| `ActualPrefix` | dependency | 65 |
| `PalindromeBridge` | dependency | 15 |
| `EightFamilies` | dependency | 233 |
| `Lychrel196Research` | dependency | 0 |
| `TemporalResidues` | dependency | 36 |
| `ResidualFiveShape` | dependency | 95 |
| `ResidualFive` | dependency | 22 |
| `ResidualFiveWitness` | dependency | 27 |
| `ResidualFiveConclusion` | dependency | 8 |
| `Agent101DigitPairs` | dependency | 27 |
| `Agent101MultiplicityBounds` | dependency | 28 |
| `Agent101SplitEnumeration` | dependency | 58 |
| `Agent101NumericFibers` | dependency | 56 |
| `ResidualFiveFibers` | dependency | 17 |
| `ResidualFiveFiberConclusion` | dependency | 20 |
| `ResidualFiveResidues` | dependency | 26 |
| `ResidualFiveResidueCount` | dependency | 23 |
| `ResidualFiveResidueBridge` | dependency | 6 |
| `ResidualFiveCountArithmetic` | dependency | 13 |
| `ResidualFiveFilteredConclusion` | dependency | 6 |
| `Agent101PalindromeFibers` | dependency | 22 |
| `ResidualFiveHitDynamics` | new | 31 |
| `ResidualFiveInitialPalindromes` | new | 8 |
| `ResidualFivePhaseCompatibility` | new | 4 |
| `ResidualFiveFirstHitConclusion` | new | 4 |


## Command, source, and raw-output binding

The preserved official compiler identifies itself as Lean 4.19.0, commit `6caaee842e94`, Release. Its recorded executable hash matches SOURCE_PINS.json: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The historical report records source and runtime hashes unchanged across its run.

All **30 preserved Lean subprocess records** were checked: two version/prefix queries, 27 module compilations, and one complete audit. Each recorded exit code is 0, each log hash matches the actual retained raw log, and every mathematical invocation has exactly `--trust=0 -j1 -DElab.async=false`. Each compilation names the corresponding snapshot source and newly produced object. The logged environment restricts LEAN_PATH to that fresh snapshot.

The full historical run is recorded from 2026-10-16T22:17:54Z through 22:20:36Z. This assignment revalidates its records; it does not relabel them as a current execution.

The current published check.py and SOURCES.json match the exact driver and manifest hashes in verification.json. After inspecting the full check.py, this verifier loaded only its Python helper definitions with a non-main run name. It did **not** call main or any Lean subprocess. Its audit_source helper regenerates byte-for-byte the preserved AuditAllContributionModules.lean. That script enumerates actual selected module origins, emits one real #print axioms for every thmInfo, rejects safe custom axiomInfo declarations, and separately inventories the documented implementation categories.

The raw audit was parsed both by the inspected published helper and by a separate census in verify_binding.py. Both agree with verification.json. There are exactly **1881 distinct theorem names and 1881 corresponding axiom results**, with completion markers `AUDIT_COMPLETE 1881` and `AUDIT_DEFINITIONS_COMPLETE 1157 0`. All axiom sets are subsets of `{propext, Classical.choice, Quot.sound}`. The audit contains no sorryAx, ofReduceBool, CUSTOM_AXIOM, or error entry.

All three registry endpoints occur in the actual full audit with the expected module origin. The separate registry result is correctly marked SOURCE_AND_IMPORT_CHECK_ONLY with exit 0; its registry hash and log identity also match. It is not treated as a mathematical build.

## Actual source exports and safety census

There are **20 public source theorem declarations**, not 16. Their exact unqualified declaration lists match SOURCE_PINS.json, and each full qualified name appears with the correct module origin in the complete audit and its module's successful compilation log. There are no new source definitions and no new environment definition/opaque constants.

| New module | Public source declarations | Compiled theorem constants |
|---|---:|---:|
| ResidualFiveHitDynamics | 9 | 31 |
| ResidualFiveInitialPalindromes | 6 | 8 |
| ResidualFivePhaseCompatibility | 2 | 4 |
| ResidualFiveFirstHitConclusion | 3 | 4 |
| Total | 20 | 47 |

The remaining 1834 theorem constants are dependencies. The added original Agent101PalindromeFibers accounts for 22; the other dependency modules account for 1812. This assignment fully parses the current 1881-name origin/axiom map. The historical report's separate claim that all prior 1812 individual axiom maps were unchanged is retained as its attributed comparison; no second historical package build or separately downloaded prior axiom map is claimed here. The current full audit independently covers every one of those 1812 names.

The full named safety inventories exactly match their raw audit entries and source/log hash references:

| Precisely audited category | Count |
|---|---:|
| Unsafe axiomInfo implementation entries | 33 |
| Safe defnInfo entries | 216 |
| Unsafe defnInfo entries | 917 |
| Partial defnInfo entries | 24 |
| Opaque entries | 0 |
| All defnInfo/opaqueInfo entries | 1157 |

All recorded implementation entries belong to dependencies. None of the 33 unsafe axiomInfo names or the recorded unsafe/partial definition names appears in any theorem's transitive axiom list. The number 33 is not a total unsafe-environment census. Inductive, constructor, and recursor safety flags are outside this ledger's stated coverage. The additive scope correction in SAFETY_CENSUS.md correctly describes that limitation and does not change the theorem axiom result.

## Failed history and accepted source separation

Phase attempt-001 is preserved with its actual exit code 1, recursion-depth error, failed source hash `cd1269a191962df6d0d3b2e9138f7fba832f5e4997f0efa555ce2376b6717d02`, and sorryAx in the failed query output. Attempt-002 is separately preserved with exit code 0 and the accepted source hash `f9605cff2d4d48a1d7e2a01097b24b8ca2b43cccb665179ecfd9b3c5e88696c7`. Only the successful latter bytes appear in the accepted snapshot and exact import closure.

HitDynamics attempt-001 is accurately retained as mathematically successful; its second attempt clarifies the comment. The extra-newline staging hash rejection for Agent101PalindromeFibers is retained and explicitly classified as rejected before Lean use. These failed or superseded records have not been deleted or promoted to accepted proof evidence.

## Review attribution and mathematical boundary

The existing named full reviewer is Agent #103 `/root/runtime`, explicitly identified as a genuine distinct same-session agent who authored reproduction tooling and did not author the four mathematical sources. Its retained source reviews cover all four modules and the newly added original palindrome dependency. The attributed review identities, file hashes, source snapshots, and formal COMMENT 5554414120 are mutually consistent. The formal review is a COMMENT under the same service GitHub account, not a separate-account approval.

The secondary records accurately distinguish authorship: scope_scan reviews PhaseCompatibility; source_audit reviews HitDynamics, PhaseCompatibility, and FirstHitConclusion while excluding its own InitialPalindromes. Runtime supplies the nonauthor coverage of InitialPalindromes. Original agent identity is historical attributed evidence, not an identity independently recreated by this byte verifier; no additional mandatory review gate is introduced.

The source statements and preserved reviews consistently retain these boundaries:

- First palindrome at **strictly positive** time 2 for every member of the full ordinary-integer fiber.
- The initially palindromic boundary `r=0, n=1661` is included; initial nonpalindromicity is concluded only for positive r.
- The actual modular fiber retains complete membership, duplicate freedom, exact parity-dependent length, and all-parameter existence.
- The all-time comparison is exactly `orbit n i % 99 = orbit 196 (7+i) % 99`. It is not integer-orbit equality, reachability from 196, or a global avoidance result.

Root remains responsible for the designated delivery and source-semantic conclusion. This specialist found no contradictory byte, log, axiom, or scope fact requiring new mathematical work.

## Present validation evidence and limits

- `verify_integrity.py`, `verify_integrity.stdout.log`, and `verify_integrity.stderr.log`: full compressed/member integrity check, exit 0.
- `verify_binding.py`, `verify_binding.attempt-001.stdout.log`, and `verify_binding.attempt-001.stderr.log`: full source/log/axiom/provenance binding, exit 0 on its first attempt.
- `INTEGRITY.json`: all 24 publication identities and archive measurements.
- `EVIDENCE_BINDING.json`: exact 27-module source map, all 20 qualified exports and axiom sets, and validated counts.
- `published/`, `complete/`, `development/`, and `retrieval/`: retained original published bytes, all archive members, connector metadata, pinned source lookups, policies, and review context.
- `COMMANDS.json`: executed substantive validation commands and recorded outcomes. Preparatory connector/file-transfer operations are described separately; no unrecorded Lean run is implied.
- `EVIDENCE_FILES.json`: final file inventory, excluding only the inventory itself.

The GitHub automatic review summary says failed, followed by a usage-limit comment (6226015688). This is a service quota failure, not a technical finding or a reason to invent a new review obligation.

No unresolved contradiction was found within the assigned reuse decision. The practical boundary is the ordinary one for reuse of published logs: original process execution and same-session reviewer identity are preserved historical attestations. The present executable checks establish their exact byte binding and internal consistency and do not pretend to recreate that historical session.
