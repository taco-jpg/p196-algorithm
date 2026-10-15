# Agent 104: scoped shared publication reconciliation

This directory prepares the shared release records for the reviewed 739 theorem
and the separately retained Agent 4 bridge review. Root holds the explicitly
published PR 28 integration claim `8bfcfe69fe240be33fb2ae0e08b289c9bfffb53b`.
The merged source candidate is `4bdd59bdc8f3e8f0556c3decb0898e6c6f271b29`, based
on main `5bd98567b259659fd3195f5aa61617422aa80914`. Its mathematical sources are
byte-identical to the accepted source pin `957efa326b4b980391046598a0143cb7a7060242`.

The original contribution's independent 383-module build and exact endpoint
review passed. The assigned reviewer has now frozen the independent fresh
merged-source PASS: 383 sources and all 7,469 theorem constants, with unchanged
source pins. The current candidate state is in
`proofs/coordination/agent104-739-integrated.json`; a byte-index PASS is never
substituted for the mathematical execution gate.

`reconcile_release.py` reads the published prepared inventory checkpoint
`7216a20efaeb08daebbd3a8556ee609e042bf598`, separately from the mathematical
build candidate. It
preserves its mixed six-/seven-field TSV rows. It appends all unindexed tracked
proof files with a source-specific evidence label. Agent 104's sources and all
substantive histories, failures, reviews and logs are indexed. Other concurrent
tracked files get byte coverage only, without a new mathematical review.
If an old retained record no longer matches its current path, the helper recovers
its exact original bytes from Git into `historical-index/` and records the
relocation instead of discarding history or reverting the current document.

The helper runs no Lean compiler and performs no Git mutation. It writes only
the assigned shared publication files, the scoped coordination record, and this
directory. It refreshes inventories and manifest, runs `proofs/verify_release.py`,
retains that exact result, and reruns until the final metadata is byte-consistent.
The `release-integrity.log` PASS checks current published bytes and local source
presence. It does not prove any theorem.

From the repository root, reproduce the final verified snapshot with:

```sh
python3 -B proofs/contributions/agent-104/seven-column-kernel/release-integration/reconcile_release.py --merged-evidence-confirmed
```

The flag requires actual merged-candidate PASS reports, unchanged source pins,
and complete final evidence hashes. It is not a way to bypass the execution gate.
The unconfirmed invocation is reserved for preparation before any PASS record.
Once the current snapshot records merged-source PASS, omitting the flag exits
before any write and asks for the confirmed invocation; it cannot silently
downgrade an accepted record to PENDING.
The shared documentation remains additive. Earlier "not Lean-formalized" status
and pending preflight reports remain historical and are superseded only for the
named 739 result. No P196, optimality-of-39, or unrestricted all-time safety
claim follows.

`infrastructure-exclusions.json` records source-copy/object/runtime exclusions
from retained build reports. The secondary review has its own exact exclusion
table. Compiled products, runtime binaries, caches and copied build trees are
reproducible infrastructure; original sources, compiler pins and substantive
logs remain retained. Gzip research files are indexed with both compressed and
decoded identities and recovery commands.
