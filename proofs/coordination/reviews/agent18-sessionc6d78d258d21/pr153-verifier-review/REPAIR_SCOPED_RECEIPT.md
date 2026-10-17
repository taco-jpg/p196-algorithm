# Independent receipt for the exact printer-options repair

## Result

**PASS for this exact repair hunk and its neutral literal-audit execution.**
The coordinator's repaired copy resolves the independently reproduced Lean
4.19.0 option-name defect. This receipt is supplemental defect-and-repair
evidence; it is not a full review or launch approval of the later verifier.
Agent #20 remains the sole editor of the author verifier, and a different
genuine reviewer is assigned to the whole current verifier.

## Exact inputs

The coordinator supplied the files from
`/workspace/scratch/c6d78d258d21/evidence/pr153-verifier-fix/`. Before assessing
them, I copied their exact bytes under this review's `repair-inputs/`.

| Input | SHA-256 |
| --- | --- |
| Before script | `2eae51ee30e805c976314d8533345c9fd45fbbdfb6bb76befc1bffd6e439e37f` |
| Repaired script | `5841e26c12f2ceefa672b5d5ef7ae18243fc0872ec2a52d7eb9083d3335e0f06` |
| Patch | `083743141e30f86497eb1363bb312a32e254bc6d21a53ffeb5ab93cb6c0c4d54` |
| Coordinator repair manifest | `39e276847d4adcd7bc3e66e0e706965e70b9ff76816c051db4c7e4b522a22ed4` |

`REPAIR_SCOPED_INPUT_CHECK.json` records an independent exact-byte comparison:
the repaired script equals the before script after precisely one occurrence of
one Python string line is replaced. Python AST parsing succeeds.

The generated Lean prologue changes:

```diff
-set_option pp.width 160
-set_option pp.maxDepth 100000
+set_option format.width 160
+set_option pp.deepTerms true
```

`pp.all true`, `pp.maxSteps 10000000`, `maxRecDepth 100000`, and
`maxHeartbeats 0` remain in the exact repaired generation block. No proof source,
endpoint, closure rule, accepted axiom, or compiler trust flag is changed by this
hunk. The replacement option names are supported by the inspected, pinned
Lean 4.19.0 runtime and source.

## One bounded exact recheck

The earlier corrected neutral fixture had already shown that these two option
substitutions let the literal census print private numeric-component Names,
generated theorems, and safe definitions correctly. To remove any ambiguity
about the later script's retained printer budget, I performed exactly one
additional literal invocation. I extracted the generation statements from the
exact repaired script, adapting only the imported project module to
`NeutralFixture`, the already completed fixture's module/endpoint/census inputs,
and the generated filename.

The resulting `fixtures/LiteralAuditExactRepair.lean` ran with the same official
Lean executable and shared-library pins, serial `--trust=0 -j1
-DElab.async=false`, 3 GiB address-space bound, 100/110-second CPU bounds, and
120-second timeout used by the earlier fixture. **Exit code was 0.** There was
one completion marker, all 29 endpoint markers, all 33 inventoried theorem
axiom results, all 16 safe definition/opaque axiom results, and no `⋯` truncation
marker. No PR153 source, Mathlib source, or neutral module needed recompilation.

Evidence: `check_exact_repair.py`, `repair_literal_generation_fragment.py`,
`REPAIR_SCOPED_RESULT.json`, the `exact-repaired-literal` record in
`FIXTURE_RESULTS.json`, and both raw files
`fixture-logs/exact-repaired-literal.stdout` and `.stderr`.

## Applicability limit

The original complete frozen-input assessment concerned script
`8895d1261b7e70a00b061ed70b6aeb48580f541f3d4192bc0d34c81140c0f548`.
The repair's before script has a different hash and includes unrelated later
changes. This receipt assesses only the exact one-line option repair and its
generated neutral literal stage. It does not silently extend the earlier
review over those unrelated changes, assert that the author adopted the patch,
or claim a successful thirteen-module verification. No author file was modified.
