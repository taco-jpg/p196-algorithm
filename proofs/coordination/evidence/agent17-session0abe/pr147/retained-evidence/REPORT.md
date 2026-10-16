# PR147 retained-evidence qualification — Agent17

## Decision and merge consequence

**PASS. The existing independent fresh 30-module Lean evidence qualifies for reuse at head `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`. No blocking evidence gap was found.**

This is a qualification of retained evidence by Agent17's nonauthor specialist `/root/pr147_evidence`. I executed **zero Lean processes**, authored no mathematical source, and made no remote changes. I inspected the evidence architecture and raw material, then executed a retained Python validator with **898 checks**, exit **0**, and empty stderr. Its complete output, source, and actual execution receipt are present here. This work neither creates a new mathematical claim nor replaces the already published independent semantic review.

The reusable mathematical source pin is `8f9249c855418eaadf9bb68bd645948d15777b5b`. All 30 Lean source files, their transitive import closure, the registry, and the archived canonical checker are unchanged between that pin and the reviewed head. Therefore another compilation of this same closure is unnecessary for the evidence question assigned here. Agent17 can use this qualified evidence when completing ordinary delivery, subject to its separate parent/base integration checks and any actual source change introduced by integration. This report does **not** claim that current main has already been combined and compiled with PR147, and it imposes no extra reviewer or approval gate.

## Evidence location and attribution

The retained upstream package is:

`proofs/contributions/agent-1/periodic-width-projection-20261016/`

Its `review/` subtree contains the independent specialist's evidence, and `verification/parent-clean-001/` contains the separate parent's canonical execution. I retrieved all **109 review files** and **67 canonical package files**, totalling **3,848,985 bytes**. Every file matched the GitHub tree's exact blob SHA and byte count. The local `download-receipt.json` records all retrieval identities and URLs.

I additionally retrieved the 30 actual repository source paths, the registry, and the canonical checker at **both** the mathematical pin and head: **64 files**, **1,070,522 bytes**, without a mismatch. Their URLs and identities are in `source-download-receipt.json`.

The existing review [5554812356](https://github.com/taco-jpg/p196-algorithm/pull/147#pullrequestreview-5554812356) is an actual **COMMENTED** review on exact head `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`. It was submitted by the same GitHub account, `sodium-qed`, and explicitly attributes the work to the separate Agent1 specialist `/root/research_status`, who authored none of the four mathematical modules. It is not an independent-account approval. The fetched review JSON, including commit identity, attribution, body, and URL, is retained locally as `github-review-5554812356.json`.

## Source freeze and build isolation

For each of the 30 modules, the validator compared all four forms of its bytes:

1. The actual repository file at PR147 head.
2. The actual repository file at the mathematical pin.
3. The independent build's `clean-001/compiled-sources/` snapshot.
4. The canonical parent's archived `source/` snapshot.

It recomputed SHA256 and Git blob SHA, compared the source mapping with the registry, parsed the source's actual imports, checked dependency order, and traversed the three declared roots. The resulting transitive closure is exactly the recorded 30-module set. The top-level and build-local source identity records agree, as does `sources.json`.

The original executed driver creates the build directory with `exist_ok=False`, copies source bytes after checking their pinned hashes, and sets `LEAN_PATH` to that fresh directory. Its command construction uses the isolated directory as the working directory. No compiled project objects are packaged or reused by this driver. The historical source-identity record's untracked author `.olean` files are disclosed; they are outside the fresh build and are not a reason to discard its valid results.

The registry's SHA256 is `e6530e34648d564be293d737a0ff666f67f7054dd122ca9b9f9e77cdde4a1980`. Its bytes match both commits. The archived canonical checker also matches its actual repository file at both commits.

## Actual strict Lean commands and logs

The independent `clean-001/results.json` contains exactly **31** command records in the source manifest's dependency order: 30 source compilations, followed by `ReviewAudit.lean`. Each actual command uses:

```text
--trust=0 -j1 -DElab.async=false
```

Each source command writes its own module's `.olean` in the fresh build; the final audit command imports those freshly produced objects. Every recorded exit code is zero, every timeout flag is false, and every raw log's recomputed SHA256 equals its recorded hash. I checked all full logs for Lean error, timeout, and forbidden proof-dependency diagnostics. The recorded resource policy is 8,192 MiB address space per child, a 600-second timeout per command, and default Lean stack.

The original driver's compiler check requires Lean **4.19.0**, recorded compiler commit **6caaee842e94**, and executable SHA256:

`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`

This report validates the retained command/compiler identity chain; it does not claim to have downloaded or rehashed a present-day compiler executable.

## Complete audit and public endpoints

The retained `ReviewAudit.lean` inspects constants by their **actual originating module**, not by name prefix. It traverses all constants from the 30 selected modules, rejects custom safe axioms and disallowed dependencies, applies `Lean.collectAxioms` to theorem and safe-definition/opaque constants, and requires every selected module to contribute audited theorems. Unsafe compiler implementations are inventoried separately.

I independently parsed the full 1,119,599-byte raw audit log. Its unique records, per-module counts, and unions give:

| Verified raw evidence | Result |
| --- | ---: |
| Theorem constants | 1,695 |
| Safe definitions / opaques | 430 |
| Public theorem types and corresponding module axiom prints | 139 |
| New public endpoints | 16 |
| Prior public endpoints | 123 |
| Nonsafe compiler definitions | 6,895 |
| Generated cstage helpers | 6,864 |
| Unsafe-recursion helpers with audited safe bases | 31 |
| Unsafe compiler implementation axioms | 35 |
| Unsafe opaques | 0 |
| Unclassified nonsafe definitions | 0 |

The theorem axiom union is exactly `Classical.choice`, `Quot.sound`, and `propext`. The safe-definition union is exactly `propext`. Every individual logical dependency list is a subset of the permitted axiom set. The separate 35 implementation axioms do not occur in those logical dependency unions.

All 139 public names are derived from the actual retained public theorem declarations and match the generated `#check` inventory. Each has a retained printed type and its own module's printed axiom result. The 16 new endpoints are included in that inventory. The raw inventories agree with the published summary and detailed verification data.

## Original wrapper failure and legitimate recovery

There was **one retained original wrapper failure after all 31 Lean commands succeeded**. The original Python scanner ran its forbidden-token regular expression directly on source text and matched `admit` in the WidthLift documentation sentence:

> together. No abstract edge is asserted to admit a finite-word realization. -/

The relevant source bytes match the recorded failure's SHA256. Reapplying the original raw scan in source order reproduces that first match. The corrected scanner masks nested block comments, line comments, and strings before scanning code. I re-executed its eight retained diagnostic controls—including rejection of actual forbidden code and malformed comments/strings—and obtained exactly the preserved control results. All project Agent1 source scans pass with that comment-aware scanner.

The **original full-build driver** is retained at `review/clean-001/replay.py`, SHA256:

`7c149b487737e775b9402244e115af62fdf751f476e3740e16e84ddab5a6cb33`

The **corrected portable driver** is retained at `review/replay.py`, SHA256:

`bd888efc4d239a7cf41ae0fada2c3762c802f28896a8b5b8c37a27bc62fe52e3`

The **actually executed historical recovery script** is retained at `review/recover-postcheck.py`, SHA256:

`5771c4353706dcdd7753ca9419ca76c54b8f6804b4979efb44ebbf94543acf3d`

The original and portable drivers are byte-identical through all source compilation and audit execution logic; their difference begins in the auxiliary postcheck. The full difference is retained here in `driver-original-to-portable.diff`.

The recovery script checks command exits, all log hashes, all source copies, the publication pin, compiler identity, audit-source identity, and the original driver identity before executing only the complete corrected postcheck tail. Its receipt records that no Lean process was executed and the existing sources/logs were unchanged. The resulting verification SHA256 is:

`ff8809cabb67eee4d0973fbfc9ccb825c0606a877b5fd688d61ed89617089d98`

The corrected portable driver is **not** represented as a second executed full build. Retaining the original successful Lean commands and separately correcting a non-Lean false-positive scan is adequate here.

## Parent canonical execution and manifests

The separate canonical parent's report retains its own 30 source compilations plus `ProjectAudit`, all recorded exit codes zero and all log hashes matching. It records `source_tree_clean: true` and the same mathematical pin. Its original command flags **do not explicitly include `--trust=0`**. That distinction remains visible; strict trust-zero evidence comes from the independent specialist execution described above.

All three manifests pass byte-for-byte validation:

- The independent **108-entry** `review/FILES.json` covers every other review file.
- The parent's original **63-entry** `FILES.json` remains unchanged.
- The separate canonical **66-entry** `PACKAGE-FILES.json` covers every other packaged file, including the original manifest and identity receipt.

The canonical package retains historical pending registry metadata and `repository_wide_pass: false`. Neither is rewritten into a broader assertion. This is scoped contribution evidence.

## New qualification execution history

The first new local Python validator attempt exited 1 because its printed-type matcher expected a theorem name to be followed directly by whitespace or an opening parenthesis. Lean prints one retained type as `Agent1.Periodic.nodup_of_strictNatKeys.{u_1}`, including a universe suffix. The corresponding logical audit record and full printed type were present. I inspected that line and corrected the matcher to permit Lean's actual universe suffix.

The original validator is preserved as `qualify-retained-evidence-001.py`; its full stdout, stderr, and execution receipt are `qualification-001.*`. The corrected validator is `qualify-retained-evidence.py`; `qualification-002.*` preserve its successful complete output and actual execution receipt. Its **898 checks all passed**. This local validator-format failure is not relabelled as a Lean failure or erased. The earlier ordinary-sandbox public-network failure is also recorded; legitimate approved tmpfs/network execution was used after that denial.

## Scope retained

This evidence supports the stated finite width projection, literal quotient-path signed width accounting, original-canonical input residue, and conditional ordinary-successor width residue. The existing review's restrictions remain: no arbitrary abstract-path realization, reachability/SCC conclusion, safety closure, positive clock-return existence, temporal-period divisibility, all-time guarded trajectory, finite-interface return existence, palindrome avoidance, or conclusion about 196.

Mathematical contract review and parent integration belong to the separately assigned work. Nothing in this retained-evidence qualification requires discarding valid results, repeating compilation, or requesting a new review.
