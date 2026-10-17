# PR101 strict certificate execution

## Result and scope

The isolated **104-module candidate closure passed Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`**, followed by a complete module-origin audit of every theorem, safe definition, and safe opaque declaration in that closure. The audit executed **2,660 actual `#print axioms` commands** and independently compared their declaration coverage with the environment inventory and `Lean.collectAxioms` results.

The verified closure consists of **17 exact historical dependency modules, 86 unchanged generator outputs, and one minimally repaired original WIP module**. The 103 dependency/generated modules were not edited. The WIP repair escapes four uses of Lean's reserved identifier `prefix` as `«prefix»`; the resulting declaration remains named `Agent117.C2641.prefix`.

This is verification of the pinned historical closure and generated candidate. It is not a statement that the candidate has been registered in the current accepted build, combined with the latest main tree, published to the source branch, marked Ready, or merged. The execution specialist performed no GitHub mutation.

| Pin | Value |
| --- | --- |
| PR | 101 |
| Original PR head | `361de9f7ee5190c8f486c2e5b91ba563cbb95cac` |
| Historical dependency commit | `a4d803f489c3104455555ec6e5d9156d61c3aa05` |
| Lean executable | `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean` |
| Lean version | 4.19.0, commit `6caaee842e94` |
| Executable SHA256 | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| Runtime files hashed before and after | 1,503, totaling 1,538,151,001 bytes |

Source provenance is in `../../source-closure/SOURCE_PINS.json`. Original generation was performed by the delivery owner and retained in `../generator-original-001/`; this specialist did not rerun the generator or finite Python enumeration.

## Compiled endpoint statements

The retained audit prints the following complete endpoint types:

```lean
Agent124.Cert117P2641K7.ancestry_2641 (A P t : Nat) :
  0 < A → Agent124.PrefixL.PalStartsL [2, 6, 4, 1] P →
  Lychrel196.orbit A t = P → t ≤ 6

Agent124.Cert117P2641K7.no_196_2641 (t : Nat) :
  ¬ Agent124.PrefixL.PalStartsL [2, 6, 4, 1] (Lychrel196.orbit 196 t)
```

Each endpoint's transitive axiom set is exactly `{propext, Classical.choice, Quot.sound}`. The ordinary-integer semantics and advertised scope are addressed by the separate independent semantic reviewer. The WIP target definitions remain definitions of propositions; the repair does not turn them into proved theorems.

## Execution and failure preservation

| Attempt | Actual result | Duration | Successful candidate module compilations |
| --- | --- | ---: | ---: |
| `attempt-001` | Failed on the seventh module at the initial 2 GiB virtual-memory cap | 35.062 s | 6 |
| `attempt-002` | All 103 dependency/generated modules covered | 558.716 s | 97 new; 6 reused from `attempt-001` |
| `supplement-001` | Original WIP failed to parse its reserved identifier | 3.781 s | 0 |
| `supplement-002` | Repaired WIP and complete axiom audit passed | 99.287 s | 1; plus the separate audit program |

The sum of recorded attempt durations is **696.846 seconds**. All substantive Lean commands had a 180-second limit. The build job had a 1,200-second bound; the final supplement had two sequential commands, each bounded at 180 seconds. Only one Lean process was run at a time.

### Initial resource failure

`attempt-001/logs/007-LychrelDigitSums.stderr.log` contains:

```text
INTERNAL PANIC: out of memory
```

The command exited 1 after 27.455 seconds, with a recorded maximum RSS of 1,615,448 KiB under the 2 GiB address-space cap. There was no preceding Lean proof error. The complete failed attempt, source copies, logs, manifests, and six successful object files are retained.

The corrected runner increased only the per-process virtual-memory cap to 3 GiB after resource inspection. It created an initially empty new object directory, checked the first attempt's successful source/object/runtime identities, and copied only those six successfully verified objects. It compiled the remaining 97 modules. This reuse is explicit in both the runner and receipt; it is not represented as a second clean rebuild of all 103 modules.

The largest recorded process RSS was 2,201,400 KiB. `LychrelDigitSums` then passed in 67.732 seconds; the longest completed candidate-module command was `A124117P2641K7Short` at 121.306 seconds. Retained cgroup observations show no increase in `oom` or `oom_kill` counters during these runs (34 and 4, respectively).

### Original WIP parser failure and repair

The first meaningful source error was:

```text
Agent1172641Targets.lean:17:3: error: unexpected token 'prefix'; expected identifier
```

Subsequent errors at the uses of `prefix` were parser cascades. `supplement-001` preserves the original source and complete error logs.

The isolated repair changes exactly four identifier occurrences:

```diff
-def prefix : List Nat := [2, 6, 4, 1]
+def «prefix» : List Nat := [2, 6, 4, 1]
 ...
-  entryOK 7 (R tree) (prefix, 5) = true
+  entryOK 7 (R tree) («prefix», 5) = true
 ...
-    PalStartsL prefix P → orbit A t = P → t ≤ 6
+    PalStartsL «prefix» P → orbit A t = P → t ≤ 6
 ...
-  ∀ t, ¬ PalStartsL prefix (orbit 196 t)
+  ∀ t, ¬ PalStartsL «prefix» (orbit 196 t)
```

All other bytes are unchanged. The exact patch is `repair/reserved-identifier.patch`, and the repaired source is `repair/Agent1172641Targets.lean`.

| WIP source | SHA256 |
| --- | --- |
| Original, 1,124 bytes | `408f14252ab599c39723b0deca031099ba32d7f081a4b7ca23b6c2b62d880c9b` |
| Repaired, 1,140 bytes | `961bd5aa6a6462443434b40b53da032236201d8e7a543c92d73841283881dd15` |

The repaired WIP passed in 0.416 seconds. The audit confirms the exact declaration name `Agent117.C2641.prefix` and audits all four WIP definitions with empty axiom sets.

## Full transitive axiom audit

`supplement-002/sources/AuditPR101.lean` imports the compiled endpoint and repaired WIP, then selects declarations by their actual imported module of origin. Namespace matching is not used as a substitute for module coverage.

For each selected theorem, safe definition, and safe opaque declaration, the audit:

1. Identifies its actual `ConstantInfo` kind and module index.
2. Computes `Lean.collectAxioms` over the kernel environment.
3. Rejects any transitive axiom outside `propext`, `Classical.choice`, and `Quot.sound`.
4. Executes an actual elaborated `#print axioms` command for the same declaration.
5. Records its identity and compares all resulting coverage sets after execution.

| Audit measure | Count |
| --- | ---: |
| Covered module origins | 104 |
| Total declarations inventoried from those origins | 29,808 |
| Theorems audited | 2,188 |
| Safe definitions audited | 472 |
| Safe opaque declarations | 0 |
| Total transitive audits | 2,660 |
| Actual `#print axioms` outputs | 2,660 |
| Disallowed axioms in those audited chains | 0 |

The union of all audited axiom sets is exactly `{Classical.choice, Quot.sound, propext}`. The raw audit completed with exit 0 in 95.440 seconds, under a recorded maximum RSS of 990,956 KiB. Its raw stdout is 3,403,608 bytes and is retained in full.

### Compiler implementation inventory

The environment also contains compiler-generated implementation declarations. The audit retains their actual kinds separately and does not misclassify them as safe mathematical definitions:

| Actual kind | Count |
| --- | ---: |
| Unsafe definitions | 26,990 |
| Unsafe implementation axioms | 70 |
| Partial definitions | 38 |

The unsafe definitions divide into 26,654 names ending in `._cstage2` and 336 ending in `._cstage1`. All 38 partial definitions end in `._unsafe_rec`. Of the 70 unsafe implementation axioms, 69 are compiler specializations with `._at.` and `._spec_` names; the remaining declaration is `OverflowCarryNormalization.iterPairs._elambda_1`.

The pinned compiler's `src/lean/Lean/Compiler/Old.lean` explicitly defines the eager-lambda-lifting `_elambda_` naming function and documents generation of `_unsafe_rec` auxiliaries for regular recursive definitions. The original `iterPairs` is an ordinary safe recursive definition in the pinned `LychrelDigitSums.lean`. The source scan found no authored unsafe declaration or axiom. None of these implementation axioms occurs in the 2,660 audited safe transitive axiom sets.

The independent semantic reviewer has qualified the complete inventory and final coverage evidence and reported no semantic blocker for this exact candidate and repair. The full inventory is retained in `supplement-002/module-origins.json` and in the supplement receipt; summary consumers should avoid printing the entire multi-megabyte receipt to chat.

## Isolation and identity checks

The inspected runners are standard-library Python. They invoke the pinned Lean executable directly, without a shell, network operation, Git command, generator, or project-provided executable. Subprocess environments are explicit whitelists containing only runtime paths, locale, the isolated `LEAN_PATH`, `LEAN_SYSROOT`, and an isolated temporary directory. No credential environment is inherited.

The source import graph was checked as closed over the 103 selected modules, with `Std` as the only external import. Full source bytes were checked against retained Git-blob/SHA256 identities. Every copied source used by the successful build was compared with those pinned original bytes before the supplement, and included in its before/after identity manifest. The four-token WIP repair is separately pinned. Runtime object/shared-library bytes, source inputs, reused objects, copied sources, and successful build objects remained unchanged throughout the successful checks.

The only non-runtime custom object files imported by the final audit were the files produced by these recorded strict builds. There was no import of another session's cached project objects.

## Evidence entry points

| Evidence | Relative path from this report |
| --- | --- |
| Compact result and resource summary | `SUMMARY.json` |
| Initial failure and six successful modules | `attempt-001/receipt.json` |
| Successful 103-module build and exact order | `attempt-002/receipt.json`, `attempt-002/build-order.json` |
| Build object identities | `attempt-002/object-manifest.json` |
| Original WIP failure | `supplement-001/logs/001-original-wip.stdout.log` |
| Exact source repair | `repair/reserved-identifier.patch` |
| Final WIP/audit receipt | `supplement-002/receipt.json` |
| Raw complete axiom audit and endpoint types | `supplement-002/logs/002-full-audit.stdout.log` |
| All safe audited declarations and axiom sets | `supplement-002/audit-declarations.json` |
| Complete environment-origin inventory | `supplement-002/module-origins.json` |
| Final input identities before/after | `supplement-002/input-before.json`, `supplement-002/input-after.json` |
| Resource observations | `resource-check-002.json`, `resource-check-003.json`, `resource-check-004.json` |

All failed attempts and original bytes remain present. No cleanup or source-branch overwrite was performed.

## Delivery handoff

Agent #10 remains the delivery owner through the parent integration agent. The separate semantic reviewer has approved the exact reserved-identifier repair, independently checked the 103-module build evidence, and qualified the complete final audit and compiler implementation inventory. The reviewer's durable supplement is recorded separately under `../../independent-review/`. The execution specialist hands off this completed strict verification packet and exact repair for the parent's publication, current-base combination, ownership, readiness, and integration actions. No merge or source publication is claimed by this report.

The original generation and first failed build are also preserved in the immutable checkpoint commit `a676d2c8ee41b1e76e9b7c9f98d83936fda18015`, under the parent's `pr101/checkpoint-001/` evidence prefix. The follow-on execution archive refers to that checkpoint rather than duplicating or rewriting it.
