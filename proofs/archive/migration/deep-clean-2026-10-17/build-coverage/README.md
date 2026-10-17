# Current-tree core build repair

Agent #3 / `agent-3-b09751a92b96`, campaign `deep-clean-2026-10-17`.
Original verifier, registry, mathematical source, and review attribution remain
retained in the exact original versions and execution records.

This packet repairs the current `proofs/verify_project.py` entry point and its
38-source `consolidation-core` registry. The runner reads the current flattened
source paths directly, enforces `--trust=0 -j1 -DElab.async=false`, audits all
kernel-safe constants, and checks a separately located consumer of its generated
`P196Project` aggregate. No Lean source or theorem statement changes.

## Preserved originals

`originals.tar.xz` has exactly five members: the four replaced files at baseline
`74a1c3922eb7af438fe40b23d2105ad07556e3f5`, plus the advanced `SOURCE_MAP.json`
at integration base `ed5202b2839b5fedf3d97309481ac7a4bd556675`. The other three
replaced paths have identical bytes at both bases. `originals-manifest.json`
records original paths, commits, modes, blob IDs, byte counts and hashes.

- Archive size: 521,940 bytes.
- Archive SHA-256: `1f68bca70456699749acb3930b1ab0f6d5331fdacd3ff99f97ba369a9f079c0f`.
- Independent fresh extraction and comparison to pinned Git originals: PASS.

The final `SOURCE_MAP.json` changes only the old registry's `current` selector to
`null`, so historical replay selects its exact archived original. PR160's
`REPORTS.md` selector stays intact. All 9,161 historical selections retain the
same bytes and modes; all 6,850 distinct selected blobs were SHA-256 checked.

## Actual scoped verification

`verification-evidence.tar.xz` preserves 286 files, including exact candidate
versions, staged sources, generated aggregate/consumer/audit sources, commands,
exit statuses, full logs, interface records, policy rejection evidence, and
independent review. Its outer manifest records every member hash.

- Archive size: 2,022,324 bytes; uncompressed member bytes: 43,121,763.
- Archive SHA-256: `caf02913c06737e526314dfde5b152b3b69d302ad36c16fa12fb66d21d16e5d5`.
- Actual full execution: 41 commands, all exit zero; 38 source modules.
- Audit: 3,491 theorems and 3,843 kernel-safe constants, with complete structural
  interface records and only `Classical.choice`, `Quot.sound`, and `propext`.
- Separate consumer: 25 public endpoints, matching historical printed signatures.
- Full historical theorem-name/module/axiom mapping: exactly equal.

The full execution used the initial candidate and registry. Later final changes
only repair legacy flag input compatibility, add declared/effective flag report
fields, and correct historical metadata. The effective mathematical build,
consumer and audit context is unchanged. The independent review explicitly
qualifies reuse; it does not relabel the first run as consuming final file bytes
or claim a second independently executed full build. The final installed entry
point also passed a separately recorded source/import check on the integration
base. See extracted `EVIDENCE.md` for exact identities, limitations, and replay.
The installed invocation's exact command and parent-observed process exit are
separately retained in `installed-entrypoint-receipt.json`, bound to the archived
report and file manifest. It is not presented as an independent second run.

Compiled project objects and Python caches are reproducible infrastructure and
are excluded. Exact mathematical inputs and substantive execution evidence remain
preserved. Existing failed and historical records are unchanged.

## Remaining scope

The registry still has `catalogue_complete: false` and its accepted-scope census
blocker. A scoped PASS does not establish repository-wide build coverage,
semantic source consolidation, branch retirement, or campaign completion.
The coordinator's external global backup upload was blocked by automatic approval
review when this packet was assembled. This isolated repair does not certify
that separate durable preservation gate. The coordinator's delivery ledger must
record actual publication and current-target readback.
