# Independent runtime 和 semantic gate

**PASS — Agent #9/runtime-audit independently reviewed 和 rebuilt the frozen one-step ordinary digit-sum collapse source.** The author is Agent #9/horizon-safety. This packet records one independent fresh run after the author's source freeze. The author's successful second attempt 和 failed first attempt remain in the separate `development/` subtree.

## Result

The exact six-module project closure compiled with official Lean 4.19.0, explicit `--trust=0`, `-j1`, 和 `-DElab.async=false`. The output directory was newly created with zero project objects. All selected source bytes, the source registry, 和 the recorded runtime snapshot remained unchanged during the run.

| Module origin | Theorem constants | Safe definitions |
| --- | ---: | ---: |
| `LychrelDigitSums` | 986 | 148 |
| `IncomingCarrySensitivity` | 84 | 9 |
| `RawSymmetryObstruction` | 136 | 17 |
| `IntrinsicSeam` | 29 | 2 |
| `SeamAnnihilation` | 64 | 7 |
| `Agent9OneStepDigitSumCollapse` | 21 | 0 |
| **Total** | **1,320** | **183** |

The new module's ten public theorems 和 eleven generated theorem declarations are all covered. Every public export has both a literal type report 和 a literal `#print axioms` report. All six module origins were visited. The complete transitive axiom union is `propext`, `Classical.choice`, 和 `Quot.sound`.

The audit separately retains 13 unsafe implementation axiom constants 和 807 unsafe implementation definitions emitted for the unchanged original project closure. These implementation records are distinct from the theorem/safe-definition census. Every audited theorem 和 safe definition has only the three allowed standard axioms in its transitive closure. There is no source-level placeholder, new axiom declaration, `native_decide`, or recorded kernel-bypass token in the selected source closure.

## Semantic finding

For every canonical ordinary-decimal realization of `framedNine (2*r)` at width `2*r+2`, including `r=0`, the source proves initial digit sum `9*r+10` 和 next digit sum exactly two. Positive witnesses use the existing `even_family_realized` theorem with `r>0`. Choosing `r=B+1` supplies one positive integer 和 its actual canonical width with both `B < digitSum n` 和 `B < L`, including threshold zero.

The existing family, realization, exact step value, two-step palindrome results, 和 decimal mass bridges are reused unchanged. The result formalizes the scalar consequence already stated in the original manuscript. Its scope is the quantified one-step family; it adds no conclusion about a fixed infinite orbit.

Read `SEMANTIC_REVIEW.md` for the complete independent reasoning, quantifier checks, parameter boundaries, 和 reuse analysis. Exact new-source SHA-256:

```text
d9cb44e04c4f4bdbda42d7f877afeabd6e0c59cb085dfc023598707c7d0177db
```

## Evidence map

| File or directory | Contents |
| --- | --- |
| `FINAL_REVIEW.json` | Final attributed review result 和 evidence hashes. |
| `SEMANTIC_REVIEW.md` | Complete mathematical semantics 和 source-reuse review. |
| `source-registry.json` | Exact six sources, import closure, historical origins, 和 all ten endpoints. |
| `verify.py` | Independent portable verifier actually used for this run. |
| `inputs/` | Exact manuscript, frozen new Lean source, 和 both reviewed contract versions. |
| `provenance.json`, `provenance-logs/` | Original preparation receipt 和 exact Git read commands/results. |
| `PRECOMPILE_SEMANTIC_STATUS.json` | Timed precompile status; deliberately preserves its then-pending build status. |
| `SOURCE_FREEZE_RECEIPT.json` | Author freeze 和 independent start receipt, recorded before the independent result. |
| `runs/full-001/verification.json` | Unmodified raw independent report, including exact command lines, timings, runtime hashes, source pins, 和 unchanged-input checks. |
| `runs/full-001/logs/` | Every raw independent command log, copied byte for byte. |
| `runs/full-001/PUBLIC_EXPORTS.log` | Exact extracted literal type 和 axiom reports for all ten public theorems. |
| `runs/full-001/MODULE_ORIGINS_AND_TOTALS.log` | Complete wrapped module-origin list 和 census totals. |
| `runs/full-001/NEW_MODULE_DECLARATIONS.log` | Exact axiom records for all 21 new-module theorem constants. |
| `runs/full-001/AUDIT_SUMMARY.json` | Parsed complete multiline origins/axiom lists, module counts, 和 every new declaration. |
| `runs/full-001/CollapseIndependentAudit.lean` | Exact generated Lean audit source. |
| `runs/full-001/original-run-FILES.json` | Original run's complete file hashes, including reproducible objects. |
| `runs/full-001/RETENTION.json` | Exact retained/omitted mapping 和 recovery command. |
| `EVIDENCE_FILES.json`, `MANIFEST.sha256` | Hash index of the actual retained review files. |

The original preparation contract's section heading was later corrected by root. Both exact bytes remain in `inputs/`; the formal target 和 hypotheses are unchanged. Historical receipts retain their actual earlier wording 和 status. `FINAL_REVIEW.json` is the final review decision.

## Replay

From a repository checkout containing the registered source files 和 historical Git objects:

```bash
python3 proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/review/runtime-audit/verify.py \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --output /fresh/output/directory \
  --auditor 'Actual replay operator'
```

The output directory must be absent before the command. `--repo`, `--package-root`, 和 `--manifest` support alternate checkout locations. The verifier includes the truthful operator argument in the raw report. Exact historical blob checks require the recorded Git objects, in addition to the preserved project source bytes.

The actual local invocation used `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean` 和 `/workspace/scratch/8dcaf4a67fa4/agent9-runtime/collapse-full-001`. The runtime's version was `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`. Local execution needed the approved escalated runtime launch because this runtime cannot launch in the default sandbox. All generated files stayed inside the assigned scratch output.

## Scope 和 retention

This gate covers exactly the selected project closure. Official prebuilt `Init`, `Std`, 和 `Lean` runtime modules are supplied as part of the identified Lean 4.19.0 installation; the run does no independent compiler/runtime rebuild or repository-wide build.

Every raw independent log 和 report is retained. Reproducible project `.olean` outputs 和 redundant isolated source copies are omitted from the publication packet with their exact hashes in the original manifest. The five original dependency source bytes are also present in the `*-original-source.log` files; the frozen new source is present in `inputs/`. `RETENTION.json` explains recovery. The reviewer performed no deletion, truncation, mathematical-source edit, Git mutation, or external publication.
