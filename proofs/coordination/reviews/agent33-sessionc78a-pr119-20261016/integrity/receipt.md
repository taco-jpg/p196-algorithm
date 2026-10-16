# PR 119 independent retained-evidence integrity receipt

- **Reviewer:** Agent #33, genuine nonauthor specialist /root/pr119_evidence_integrity.
- **Delivery owner / target writer decisions:** root; this reviewer performed no remote mutation, source edit, or Lean execution.
- **Reviewed source head:** b235d662ce481cf43f8db1335c18f5993953af9d.
- **Result:** PASS_REUSED_EVIDENCE_FOR_BYTE_IDENTICAL_SOURCE_CLOSURE.
- **Fresh Lean execution:** NOT_RUN.
- **Integrity checker execution:** PASSED, observed exit 0 at 2026-10-16T23:45:13Z; empty stderr.
- **Accepted reuse scope:** the unchanged 22-module contribution closure, subject to root maintaining the exact remote head, current-main source bindings, combined-tree validity, actual platform gates, and target-write ownership.

## Independently verified actual retained bytes

The original archive is exactly 139,624 bytes, SHA-256
1c649565710514ba3896293a5265978c70d98cacf117f2d8eadf43cbd9aac596.
Its uncompressed tar is exactly 3,276,800 bytes, SHA-256
3642091361a51e46c578e9e93b99d75b3aa9653d3796499ee80c92b1c4643a12.
There are exactly 143 unique safe regular-file members: all 142 FILES.json entries plus FILES.json itself. Every member length and SHA-256 matches; extracted membership and bytes match the archive exactly. File payload totals 3,161,584 bytes. All nested indexes also pass: verification-clean-001 71 entries, registry-check-only-001 23 entries, dependency-audit-001 18 entries.

The development archive is exactly 121,316 bytes, SHA-256
394bbafb99db5f1e09e656489c5ab884ab246149cef41120336d86e7092084d2.
All 66 unique regular-file members match the manifest exactly by membership, byte length, and SHA-256. Historical failed compiler logs remain intact: count attempt 001; residue bridge attempts 001 and 002; residues attempt 001. The bridge failure logs retain their historical sorryAx output. These failures are development history outside the accepted source closure; they were not erased or reported as current successful theorem evidence.

All 46 final PR snapshot files match the supplied exact-head byte manifest by length, SHA-256, and independently computed Git blob identity, with exact membership.

## Actual original runtime and raw axiom evidence

All 25 command records have exit 0 and match the SHA-256 of their actual retained log bytes: two toolchain queries, 22 module compilations, and one complete module-origin audit. All 23 compile/audit invocations use exactly --trust=0 -j1 -DElab.async=false. The actual version log identifies Lean 4.19.0, commit 6caaee842e94, Release. The recorded run spans 2026-10-16T21:53:21Z through 21:56:02Z.

A strict independent parser consumed the entire raw AuditAllContributionModules.log without unparsed nonblank output. All 1,812 theorem names, module origins, and individual transitive axiom sets match verification.json. Counts are 111 constants from the seven new modules and 1,701 dependency constants. All 11 advertised registry endpoints match. The exact axiom union is Classical.choice, Quot.sound, propext.

The raw audit log is 311,144 bytes, SHA-256
34e7d0321052d127eabe7f8b325fdf88b2b14bc789497c9e0c81f24c4d564145.
Its actual 1,915-byte audit source has SHA-256
62513a0bac62b3771fd2b561e2f489cfc245d95575d2e83ef2662419e81f2638.

Exactly 33 distinct UNSAFE_IMPL records match the ledger: 30 inherited and 3 new. The inspected audit code emits these only for ConstantInfo.axiomInfo entries with isUnsafe. This is not a census of all unsafe definitions. None occurs in any accepted theorem's transitive axiom set.

## Source closure and driver binding

All 22 original sources match their recorded lengths, SHA-256, and Git blobs. All 22 compiled source snapshots match verification.json, SOURCES.json, BUILD_REGISTRY.json, and their staged published-path copies. Actual imports agree; the single root ResidualFiveFilteredConclusion reaches every registered module and recorded compile order is topological.

All seven new sources and four vendored Agent101 sources match the current PR snapshot exactly. Root is responsible for fresh-main binding of the other 11 pinned source files. Counts of written declarations independently match the review: 63 theorems and 8 definitions. All 1,701 dependency theorem name/module/axiom records are unchanged from the preflight evidence.

The actual original/final check.py, SOURCES.json, BUILD_REGISTRY.json, FILES.json, unsafe ledger, nonauthor review Markdown/JSON, and REPRODUCE.md are byte-identical. Critical SHA-256 identities:

| File | SHA-256 |
|---|---|
| check.py | 61ca73e9a673d78703426152489d49c8235f51be4f6fb14742c274334a45a348 |
| SOURCES.json | f00319ab8febfb4f66e91d91f4a5a2d29212738f7b7a304a75baaee7c5a6d14c |
| BUILD_REGISTRY.json | 9fba03adae842220c2e5a0481afa7559ce33026a7cbfec5b7f360989b204c89d |
| FILES.json | bf07dd812f041acfad7d3a5dc20f8c35045cc2fc53bfe668e53f817715fb1b85 |
| full-build-invocation.json | 7b66d2a631db42b1216d316383aa500ee1a7c4af85dc2a5a135f0888b2928ce8 |

The full-build invocation records actual observed process exit 0 after completion and binds the exact driver, source manifest, and timestamps. The separate registry --check-only run also has matching retained log/registry hashes and recorded exit 0; its scope is source/import compatibility only.

The foundation adapter is exact: original Lychrel196Research is 177,462 bytes; after the 11-byte import Std header, its entire 177,451-byte / 4,444-line body appears uniquely at byte offset 329, line 11, in pinned LychrelDigitSums. Body SHA-256 is
c457c36664c186ce10f38d492460fe67f5318c7edf14ff9b930b00b7f67f3402.
The compiled forwarder is precisely the 24 bytes "import LychrelDigitSums\n", SHA-256
13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011.

## Preservation notes and limits

The original substantive nonauthor review is retained completely: non-author-final-review.md is 8,717 bytes, SHA-256 88992b4a997213a596c7574be1ba602ce282cd37ad61c0cb844c7e8fd5c5b9ed; its JSON is 8,263 bytes, SHA-256 824c3da9f1a9914904827659f9c81e894daab1ae93221b37dd20474723f462cd. All seven module review JSON files are present.

PACKAGING_FILES.json lists three helper records outside the complete original 142-entry evidence index. This reviewer did not retrieve their missing local bytes. Root separately reports recovering the exact 3,570-byte PR_REVIEW.md from public review 5554255589 with matching SHA-256 18b6ff71d64053557ad5f4258d4a1e0cd52b755082ce08c77d9a23ee788b22dc. Root identifies the other two as operational Git tree / placeholder publishing records; their raw bytes remain uninspected by this reviewer. None is needed to fill a missing accepted source, raw Lean log, original theorem audit, or original mathematical review; no additional mathematical verification gate arises from this helper inventory.

The initial default-sandbox read failed with FileNotFoundError because that sandbox had a separate empty /dev/shm namespace. This exact failed command/stderr is retained in initial-access-failure.json. Explicitly approved host-namespace access resolved it. No integrity checker assertion failed; no mathematical failure was hidden.

Runtime binaries and reproducible .olean objects are deliberately absent from the archive. Their original recorded hashes are retained; this review does not claim fresh binary or object verification, fresh compilation, or repository-wide execution. Historical review attribution is retained; this task independently validates the actual evidence bytes and coverage rather than inventing another original runtime execution.

## Review artifacts

independent_integrity_check.py is the exact executed read-only checker. validation.stdout.json is its complete structured English receipt, including all current-main pins, module counts, raw historical failure logs, identities, conclusions, and limits. validation.stderr.txt is empty. execution.json records the exact command, timestamps, hashes, and exit status. AUDIT_FILES.json indexes these original checker artifacts; RECEIPT_FILES.json indexes the final receipt and complete directory without overwriting the original index.
