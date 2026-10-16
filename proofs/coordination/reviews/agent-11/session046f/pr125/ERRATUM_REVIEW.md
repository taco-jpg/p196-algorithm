# Independent review of the additive Lean 4.19 evidence erratum

Reviewer: Agent #11, session 046f9285a650, independent nonauthor review task `/root/review125`.

**Verdict: PASS for the exact candidate text.** Adding this text to PR125 resolves the evidence-interpretation issue identified in `REVIEW.md`. Final approval of a changed PR head remains subject to verifying that the published delta contains exactly this addition and preserves every pre-existing blob. This record does not claim that the addition has already been committed.

## Exact candidate

- Supplied file: `/dev/shm/p196-agent11-046f/integration/Agent11Lean419VerificationErratum.md`.
- Byte length: 7,365.
- SHA-256: `a516f682dc643f68647224d4ba2b9a31016c12b246197b30787a3cd60acbb350`.
- PR125 evidence head: `71fa669acdff9ee203ef28d7db7e31e2f9b5b4af`.
- Complete mathematical source checkpoint: `686cac2696e4e4e059c1b9d6a313f5519f6f4176`.

The reviewer read the complete candidate without modifying it. Independent ordinary `sha256sum` and `wc -c` commands returned the identity above, both with exit code 0. No Lean command was attempted or executed in this review session.

## Findings

The candidate correctly distinguishes the original fresh 18-module source compilation and its nineteenth ProjectAudit command from the separate explicit `--trust=0` audit. The original commands omitted `--trust=0`; the subsequent command used it and completed in 57.486 seconds. The candidate does not relabel the original argv and does not invent a second fresh build.

The implementation interpretation is supported by independently inspected official Lean `v4.19.0`, commit `6caaee842e9495688c1567e78c0e68dbb96942aa`. In `src/Lean/Environment.lean`, `importModules` and `finalizeImport` construct the imported environment without replaying every imported proof through the declaration checker. In `src/kernel/type_checker.cpp`, `infer_constant` returns a referenced declaration's instantiated type after the applicable checks; it does not recursively recheck that declaration's proof. The retained ProjectAudit program performs endpoint checks and a transitive-axiom audit, without a separate proof replay loop. Thus the candidate correctly withdraws the stronger historical interpretation of the import audit.

The candidate also correctly preserves the original current-source kernel-checking evidence. The actual synchronous compilation argv, source closure, source snapshots, output directories, verifier configuration, and absence of a source or option bypass were checked. The `AddDecl`/`addDeclCore` route and `src/kernel/environment.cpp` theorem checking support ordinary declaration checking during these separate compilations. The conclusion does not rest on command-line help. Exact official source files, blob identities, hashes, and the detailed call-chain review are retained in the original review package.

The PR125 theorem, endpoint, and unsafe implementation inventory counts, the archive identities, the affected-file list, and the limited mathematical scope in the candidate agree with this review's independent checks. The candidate preserves old logs, scripts, reports, archives, and labels while expressly correcting how those labels are interpreted. It requires neither a mathematical change nor a redundant build. Present-session fresh Lean execution remains **NOT_RUN**.

PR138-specific statements were independently confirmed by the PR138 reviewer `/root/review138`, who reported a separate PASS on this same exact candidate: evidence head `40670be3636e4ee7e3158e0d1577d26472a4a2a0`, mathematical checkpoint `bc178ab8735e9503ab25b325e5a8dc82bf1f1e37`, 21 source compilations plus one audit, all 22 exits 0, strict elapsed time 55.834794998168945 seconds rounded to 55.835, 2,661 theorem rows, 22 new endpoints, and archive SHA-256 `3c858e22b045a338b041b06114050cdbf6e60421da9b0e073433ed49ab86c821`. This review does not silently substitute that specialist's checks for an independent PR138 source review of its own.

## Preservation and remaining gate

The earlier report and receipt remain unchanged as historical records of the pre-correction review. The initial `publish-evidence.tar.xz` checkpoint remains 95,188 bytes, SHA-256 `a42b496c8a5e1ca9f942adc6107c0a1c4c8c3ccd63ec99d86a803638169fee88`. This addendum supplements it.

Only the exact new-head delta confirmation remains within this review's scope. Current-main integration, ownership coordination, platform state, and merge gates remain the root writer's separate responsibility.
