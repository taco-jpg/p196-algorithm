# Agent #1 saturated quotient-path author evidence

Claim: `8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2`.
Author: `/root/research_status/cap4_existing_theorems`.
Canonical source: `proofs/Agent1PeriodicSaturation.lean`.
Frozen SHA-256:
`032cba5f7a393e842bf3ab393b4a63559eb8b9349614521e9b88bbfed1cb46b6`.

The first mathematical source compiled successfully and remained byte-identical
through all three recorded runs. This is strict **incremental author** evidence;
38 existing dependency objects were reused after exact source and object hash
inventory. It is not a fresh complete-closure build or independent review.

## Checked interfaces

`Agent1.Periodic.quotient_return_saturated_profile` accepts the original
`QuotientPath`, initial `ValidPeriodic`, complete endpoint tuple equality, and
`2 * quotientClockSum = N`. It returns a cyclic offset `r : Fin 8` such that
every `i < N` has the original `cycleState (r+i)` physical prefix and actual
`rawGamma = (r+i)%2`. The `N=0` case remains vacuous.

`Agent1.Periodic.quotient_return_saturated_outside` adds `0 < N` and concludes
that the initial physical outside coefficient is 8 or 17. Neither endpoint
assumes a catalog, safety, a guarded ordinary orbit, or local edge tightness.

The proof uses the already checked
`Agent2.SaturatedProfile.saturated_overflow_profile` without reclassifying the
eight states. The actual input bit is `inputThree (periodicWord ... 3)`, supplied
by the local Prefix module. The private sum adapter identifies the existing
natural prefix-model total with the actual `quotientClockSum`.

The saved alternating outside-17/8 witness remains compatible. No false
odd-control balance is used, no finite exterior/center return is constructed,
and Agent418's multiblock consistency work is outside this source.

## Execution record

All commands used official Lean 4.19.0, commit `6caaee842e94`, with
`--trust=0 -j1 -DElab.async=false`, a 4 GiB address-space limit, and a ten-minute
command timeout. Exact commands, times, compiler hash, source snapshots,
dependency source/object hashes, complete logs, and exit codes are retained
under each `attempt-*` directory.

- `attempt-001`: mathematical source compile PASS. The first audit stopped on
  a generated safe match splitter because it expected only theorem constants.
- `attempt-002`: same mathematical source compile PASS. The revised audit
  checked the safe splitter, then stopped on a compiler-generated runtime
  implementation because it still prohibited all unsafe implementation entries.
- `attempt-003`: same mathematical source compile PASS; complete new-module
  audit PASS. It checked all 14 theorem constants and the one safe generated
  definition, with only `propext`, `Classical.choice`, and `Quot.sound` in the
  union. The safe splitter itself has no axioms. Both public endpoint types
  and axiom reports are present in the logs.

Exactly three generated runtime implementation constants were inventoried
separately. All have the common name prefix
`_private.Agent1PeriodicSaturation.0.Agent215.Saturated8.cycleState.match_1.splitter`
and suffixes `._rarg._cstage2`, `._cstage1`, `._cstage2`. There is no naked
`._rarg` entry. The auditor rejects any nonsafe definition outside this exact
generated-helper prefix, and rejects any nonpermitted axiom in every theorem
and safe definition. The mathematical source introduces no unsafe definition,
custom axiom, `sorry`, `admit`, or native evaluation proof.

The two unsuccessful audit versions and their exact diagnostics are retained;
they are not proof failures and have not been overwritten or relabeled PASS.
The final passing receipt is `attempt-003/result.json`.

## Dependency reuse and reproduction

Historical aliases are resolved through the exact current
`Agent1PeriodicReturnClock.registry.json` and
`Agent2SaturatedProfile.registry.json`, requiring identical hash/import records
on overlaps. The new Prefix source is SHA
`591c10a3f34c75d0dc058fc64db5b3934c1345b6f4fa9015eb64a3586dec8377`.
Its first passing object is from `prefix-author/attempt-002`, and its author
subsequently reported a complete new-module audit without source changes.

Invoke the canonical `saturation-author/run.py` from the repository root,
passing a new attempt name and the Prefix object's directory:

```
python3 proofs/contributions/agent-1/periodic-prefix-saturation-20261016/saturation-author/run.py attempt-004 /absolute/path/to/prefix-author/attempt-002
```

The script verifies every reused dependency source against the registry and
canonical source, records object hashes, compiles the unchanged root, and runs
the full new-module auditor. Existing attempt directories are refused.
For a fresh complete-closure build, use the parent's combined registry and
strict verifier instead. That later independent evidence is not claimed here.

`manifest.json` inventories all retained source and evidence files. Compiled
objects are reproducible runtime products, excluded from that source-evidence
manifest and publication; their hashes are separately retained in
`runtime-objects.json` and the dependency inventories.
