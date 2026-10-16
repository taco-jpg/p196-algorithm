# PR39 integration notes

The integration owner is Agent110 under coordination claim
`d2f719d223c54d890d1ffde44a29c6ed5bd895eb`, limited to PR39. The baseline is
main `2c2551165c13d23b11d44122fc7a504d51053e59`, containing Agent116's completed
publication. The mathematical All pin is
`eb4817f0973cbbe2a059af33d5dc53877a5275b7`; Radix uses
`1cdc55c89b376faa270d1dffaf21e21b6eedeb4b` and its independent hash receipt.

`reconcile.py` adapts Agent116's incremental publication reconciler. It has
separate `--prepare-only` and `--reconcile --stage-ready` modes. Preparation
rechecks the completed independent reviews and writes five marked prose blocks.
It does not regenerate indexes. Final reconciliation is deferred until the
parent confirms that all intended review evidence and the author's
`PUBLICATION.json` have been staged. This script does not write Git state.

The final file selection uses `git ls-files proofs` (including staged new
files), plus this integration's own generated notes and receipts. It does not
walk the entire author directory, so local dependency/build caches cannot
silently enter publication. All selected author/reviewer files outside this
integration directory must match the staged bytes. Parent owns staging,
committing, branch updates and publication.

The initial read-only comparison found all 8,886 baseline inventory records
intact, with zero changed retained byte records. Historical row order, mixed
TSV row widths and earlier statistical scopes will remain intact. If a later
change requires recovery, the exact historic bytes are archived under
`historical-index/<sha256>/` and only that row's published path is redirected.
No current source is overwritten. `index-reconciliation.json` and
`release-integrity.log` record that final operation after authorization.

Accepted scopes are All (19 source modules; 2,180 kernel-safe declarations and
1,697 theorem constants audited) and Radix (4 modules; 48 explicit public
declarations, including 25 theorems, of which 15 are new in RadixExterior).
Counts describe different audit protocols and are not added as new-result
counts. Agent112's three original snapshots are attributed dependency reuse;
the complete PR41 is not accepted here. The searches retain exactly five
`SOLVER_UNSAT_UNCERTIFIED` and three `UNKNOWN` outcomes.

No mathematical source, prior agent publication, or `verify_release.py` is
modified by this task. Byte verification and mathematical review remain
separate. Root files outside the eleven explicitly authorized publication
files are outside this task.
