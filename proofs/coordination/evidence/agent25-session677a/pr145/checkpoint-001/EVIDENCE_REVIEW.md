# PR145 retained-evidence audit

## Disposition

**PASS_RETAINED_AUTHOR_EVIDENCE. Independent final origin-audit evidence remains pending publication at the examined checkpoint.**

Repository: `taco-jpg/p196-algorithm`  
PR: `145`  
Examined head: `e8d706dc8a67248e1531b0b828fbe05ff50052ed`  
Contribution: `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/`  
Auditor: Agent #25 / `pr145_evidence`, a nonauthor delegated evidence auditor  
Delivery owner: Agent #25 root session `677aa81c663a`  
Source writer: Agent #15 session `43cf6e114472`, unchanged by this audit

This audit reads and validates retained evidence. It does not report a newly executed Lean build, does not substitute for the separate semantic source review, and makes no remote mutation. No retained scripts or compiler binaries were executed. A small independent Python validator checks exact byte identities, dependency coverage, log coverage, exit records, and printed axiom evidence. Its actual execution returned exit 0.

## Readiness update from the delivery owner

After this evidence audit, the root delivery owner reported an actual Ready transition and remote readback of `draft=false` at the unchanged head `e8d706dc8a67248e1531b0b828fbe05ff50052ed`. That readiness transition does not complete the pending independent module-origin evidence gate. This auditor did not repeat the transition or poll the PR. The root reported publishing the verified author-evidence facts in comment `5554711846`, without claiming new Lean execution.

## Exact source pins

| Module | Bytes | SHA256 | Git blob |
| --- | ---: | --- | --- |
| SpectralWeights | 4445 | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` | `40afa93196976972e5c0f6772a18e50c1e635a3f` |
| BinaryCode | 2655 | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` |
| ChargeSymmetry | 3240 | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` | `f69efd4bc0642759dddf99834d5d093c929761a5` |
| SourceFormula | 5059 | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` |
| ChargeControls | 1104 | `bb23522ad6792dcf6b30ef010837eb1703f7eba59f4448e355282f8eb27f668c` | `b7a1c9f7d0d175fb3f2abea93fcd23bd5eb082f8` |

The actual source bytes, `BUILD.json` source pins, copied author source pins, author verification receipt, and final retained source snapshots agree for all five modules. The import chain is exactly `Std` → `SpectralWeights` → `BinaryCode` → `ChargeSymmetry` → `SourceFormula` → `ChargeControls`. There are no other project mathematical imports in these five sources.

The canonical `check.py` was read in full. It creates a new output directory with `exist_ok=False`, copies the five sources, isolates `LEAN_PATH` to those copies, compiles each module in dependency order, generates the public print/axiom audit, retains combined stdout/stderr and exit codes, checks that source and compiler hashes are unchanged, and rejects unexpected public axioms or incomplete public coverage. Its documented limitation is that the textual explicit-public export scan requires a separate module-origin audit for private and generated declarations.

## Author archive preservation and identity

The retained archive is `evidence/development-evidence.tar.gz`:

- Bytes: `1476920`.
- Git blob: `df4e4050cfdb17d2bc9409c00aa4ff3b065b9f9a`.
- SHA256: `9c041aff895f9fda757d1c9a9894f91eb25cbad743401b1bf8c6ede26c0e6859`.
- Adjacent manifest Git blob: `548d9b4e4531106391ec45dd2b2cfcbe42c8171e`.
- Adjacent manifest SHA256: `5543fda5268d363d58befa083646872e8bdb5786191d72c38ea87eaac1b1e174`.

All **342 archived regular files**, totaling **6,449,385 uncompressed bytes**, match their manifest paths, lengths, and SHA256 hashes. No extra or missing regular file, duplicate archive entry, absolute path, parent traversal, symbolic link, hard link, or special file was accepted. Extraction was restricted to the auditor's private directory after these checks. The complete original archive remains preserved.

The manifest explicitly lists 20 omitted regenerable compiler objects. The historical cleanup receipt records five removed baseline/fixture objects, their hashes, retained source identities, and scope. The earlier manifests remain untouched historical records; the audit does not infer that omitted compiler objects remain available. No source or substantive log is silently substituted by an omitted object.

The binary fetch connector returned empty content for the large archive and its blob endpoints rejected binary UTF-8 decoding. A credential-free public raw GitHub GET retrieved the exact pinned archive instead; its length, SHA256, and Git object hash were checked before use. This was an encoding fallback, with no authentication or permission bypass.

## Retained executions and complete logs

| Author attempt | Retained result | Actual stopping point or scope |
| --- | --- | --- |
| 001 | FAIL | `SpectralWeights`, exit 1; retained arithmetic-index failure log and source |
| 002 | FAIL | `BinaryCode`, exit 1; retained arithmetic-index failure log and source |
| 003 | PASS | Three-module closure plus public audit; all recorded exit codes 0 |
| 004 | FAIL | `SourceFormula`, exit 1; retained even-length finite-sum normalization goal and source |
| 005 | PASS | Four-module closure plus public audit; all recorded exit codes 0 |
| 006 | PASS | Complete five-module closure plus public audit; all seven recorded commands exit 0 |

All six attempts retain source copies matching their own recorded pins and logs for every recorded command. Failed attempts retain actual error output. Earlier passing attempts are correctly treated as narrower historical stages and do not substitute for final five-module coverage.

The final version log reports Lean 4.19.0, commit `6caaee842e94`. All five compilation commands and the public audit use `--trust=0 -j1 -DElab.async=false`. The receipt records compiler SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` and shared-library SHA256 `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d`. The checked package imports no baseline decimal project objects.

The four published `author-*` JSON files are byte-for-byte copies of attempt 006's corresponding archive files. `PublicAudit.log` is 51,329 bytes, SHA256 `8b1d9826b419c13b3dbce777a22af42dab62c7f3002d920721b2416695088b70`. Its 69 unique axiom-result records agree exactly with the generated 69 `#print` directives, 69 `#print axioms` directives, source export enumeration, and published axiom JSON. The axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`; some exports are axiom-free.

The separately retained weights author history includes the failed attempt, corrected attempt, and fresh 29-export audit. Its final source matches the frozen contribution, both audit commands record exit 0, and all 29 printed axiom results use permitted foundations only. This author check is not relabeled independent review.

## Exact pending obligation and permissible reuse

Issue #61 comment `6226548547` reports two nonauthor reviews and a fresh five-module build with 174 origin-audited declarations. At the examined head, the README, BUILD metadata, and PR body still mark final independent evidence as pending, and no independent final archive is included in the evidence tree. The comment is a coordination receipt, not a replacement for actual origin-enumeration source, classification, full logs, exit records, source hashes, and reviewer attribution.

The precise remaining evidence obligation is to inspect the forthcoming nonauthor execution package and confirm:

1. Its five source snapshots match the hashes above, its fresh closure and compiler records are complete, and its command logs/exit codes support its result.
2. Its origin inventory covers safe definitions and theorem declarations, including private/generated declarations and controls, and its `#print axioms` results cover the inventory with only allowed foundational axioms.
3. Its source audit and execution reviewer remain nonauthors as recorded in the task attribution.
4. Its full archive matches its declared identity and file manifest and retains unsuccessful review-infrastructure attempts under accurate labels.

A final head that changes only documentation/evidence may reuse the unchanged mathematical-source reviews. Compare final source Git blobs/SHA256 and dependency imports rather than launching another identical Lean build. Changed mathematical bytes or dependencies require review of the affected obligation. Base compatibility and the final guarded merge belong to the root delivery owner.

## Reproduce this evidence audit

Run `python3 validate_author_evidence.py` beside the preserved `source-e8d706dc/` snapshot. The script does not invoke Lean, execute repository scripts, access the network, or modify the source snapshot. It emits `author-evidence-validation.json` and returns a nonzero exit on a failed assertion. This audit's recorded result is `PASS_RETAINED_AUTHOR_EVIDENCE`, exit 0.

Preserved working packet: `/dev/shm/p196-agent25-677aa81c663a/pr145-evidence/`.

Source reference: https://github.com/taco-jpg/p196-algorithm/tree/e8d706dc8a67248e1531b0b828fbe05ff50052ed/proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472

Coordination receipt: https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6226548547
