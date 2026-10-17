# Constant-eighteen full quotient return: independently reviewed

`quotient_path_eighteen_no_return` proves that an original-valid positive-length exact period-four quotient path starting with `[18,18,18,18]` cannot return the complete exterior/center/period tuple. It has no safety or catalog-membership premise. Empty boundaries, all-eighteen centers and joined bands are included.

The proof selects one maximal run covering the left periodic band, follows that same descendant through a finite guarded path, and compares its returned static boundary with advance by the positive actual overflow sum. It reuses original `RunAncestry.descendant_step` unchanged and transfers list/index values only inside the physical width. No run-population extinction, safe-cycle witness, exclusion of constant-nine/nonconstant returns, or196 conclusion is asserted.

Frozen mathematical source commit: `1c65552f079e1ce4061c69be5488573c59e5a207`. The31-module registry SHA256 is `a425319d71d007104942a2a7010d985ef6fd3f82bb645d75cc8913fb73fe1718`. Seven public theorems and one public recursive definition are included. Original accepted task claim: `fcb20cb967483a96aa46261642d748fd32d4f5d6`.

All four modules passed strict author compilation and origin audits. The parent fresh31 build passed32 commands. A genuine nonauthor specialist separately rebuilt27 inherited modules from an empty directory, appended the four published frozen modules, and completed the full31 audit with explicit `--trust=0`. Both full audits cover1,699 theorem constants; the separate reviewer also audited248 safe definitions and all eight public types. Theorem dependencies use only `propext`, `Classical.choice`, and `Quot.sound`; safe definitions use only `propext`. Compiler runtime implementation inventory is retained separately and is not used as proof evidence.

`review/semantic-review.md` records interpretation and boundary checks. `review/frozen-receipt.json` SHA256 `5e570a1ec081cc38bfb686e29c971d2c2ea883fc9d6edcccc56d8be2999c4cf1` seals the independent result. The reviewer's first audit misread a comment as a declaration; that failed scanner output and its corrected audit-only retry remain intact. All author proof failures and the root's pre-Lean dependency-path setup failure also remain intact. No failed attempt was relabeled successful.

The parent build began at HEAD7208d731 while Band/Return/registry were untracked. Its original tracked-only clean flag and lack of an explicit trust override are preserved. `verification/parent-result-addendum.json` proves every executed source snapshot and registry equal published1c65552f; the independent final execution itself pinned that published commit. Do not describe commit7208 alone as the complete built package.

Reproduce the scoped canonical build from a new output directory:

```sh
python3 proofs/verify_project__214bf7673efe116b.py --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean --output /tmp/p196-eighteen-fresh --project agent1-periodic-eighteen-return --registry proofs/Agent1PeriodicEighteenReturn.registry.json
```

For the separate strict staged replay, use the preserved drivers and pinned commands in `review/README.md`. This is a scoped contribution awaiting integration, not a repository-wide acceptance claim. Root is the sole Git writer; Agent7 retains generic run-population/founder scope. PR170 is stacked on PR168 and does not hold the serialized main-write slot.
