# Independent audit-coverage report

Preservation note: this document preserves the specialist's complete pre-execution source/design report. Its `NOT_RUN` statements describe that initial review phase. The subsequent review of Agent #2's executed evidence is recorded separately in `EXECUTED_EVIDENCE_REVIEW.md`.

**Conclusion:** The published templates can be extended to this exact thirteen-module contribution without changing any mathematical source or weakening the forbidden dependency policy. **Changing only the selected-module list is insufficient.** The executable audit must also include the equality/palindrome solvers, extensional certificate checker, and eight quantified decision functions.

This is a **read-only source and audit-design review**. I did not run Lean, reuse compiler output as fresh evidence, modify files, contact GitHub, or perform a build. The fresh proof checks remain owned by Agent #2; the combined semantic/integration review remains owned by Agent #11.

## 1. Sources inspected and identity results

I read the entire role safeguard file, all thirteen registered Lean modules, the registry, the full published `LiteralAudit.lean`, both published seven-module audit templates, and the relevant verifier implementation.

Base directory for the following references:

`/workspace/scratch/acfe54025bfc/pr140/source/proofs/`

All thirteen local module files match **both** registry hashes:

- SHA-256: **13/13 match**
- Git blob hash: **13/13 match**
- Declared import sequence: **13/13 match**
- Registry root dependency closure: **13 modules, no unreachable registered module**
- External direct imports of the contribution: **`Std` only**

The registered root `Agent102ParameterSetControls` transitively imports all thirteen modules.

These are byte-identity and source-closure checks against the local registry. The parent must retain its separate provenance evidence tying the registry and files to the frozen PR head and tested base.

## 2. The 140 literal endpoints are complete

The published literal audit contains exactly **140 distinct `#print axioms` targets**. Their set is exactly:

- The registry's **138 claim endpoints**, plus
- Its **two `literal_audit_extra_endpoints`**.

That set also exactly matches the **140 explicitly written theorem declarations** in the thirteen module sources. There are no missing names, duplicate targets, or extra literal targets.

| Module | Explicit theorem declarations |
|---|---:|
| `Agent102RunDefs` | 0 |
| `Agent102AffineArithmetic` | 17 |
| `Agent102RunWord` | 26 |
| `Agent102RunEndpoints` | 14 |
| `Agent102AffineRuns` | 18 |
| `Agent102ParameterIntervalDefs` | 0 |
| `Agent102ParameterIntervalAlgebra` | 14 |
| `Agent102ParameterIntervalCompact` | 5 |
| `Agent102AffineInequalityIntervals` | 2 |
| `Agent102PiecewiseCounts` | 6 |
| `Agent102AffineRunParameterSets` | 8 |
| `Agent102ParameterSetDecisions` | 10 |
| `Agent102ParameterSetControls` | 20 |
| **Total** | **140** |

The two names containing `?` are:

```text
Agent102.getElem?_word_of_mem_spansFrom
Agent102.getElem?_word_of_covers
```

They are explicitly declared at `Agent102RunWord.lean:158` and `:178`, and explicitly audited in the published literal audit.

The verifier's endpoint parser excludes `?` because its `NAME` expression accepts only identifier components built from `[A-Za-z_]` and `\w` (`verify_project__214bf7673efe116b.py:24`). Its generated endpoint checks use only `claims[].endpoints` (`:169–171`); the two extras are not automatically added there. **The separate 140-target literal execution therefore remains a real, necessary part of the stated verification packet.**

A successful literal audit proves the requested targets resolved and their reported axiom dependencies were obtained. Its output must still be checked against the allowed axiom policy; `#print axioms` alone does not reject disallowed dependencies.

The module-origin theorem total should **not** be forced to equal 140: it can additionally include Lean-generated theorem declarations.

## 3. Module-origin selection is appropriate, with clear boundaries

Published template:

`contributions/agent-102/affine-parameter-intervals-20261016/independent-piecewise/final-001/source/ModuleOriginAudit.lean`

Its selection is based on the declaration's originating imported module:

```lean
if let some idx := env.getModuleIdxFor? name then
  let mod := env.allImportedModuleNames[idx.toNat]!
  if selected.contains mod.toString then
```

This is the right selection method for the requested audit. It does not depend on an `Agent102` namespace prefix or an endpoint-name regular expression, so it covers relevant imported generated theorem declarations and names containing `?`.

The outer module selection controls **which theorem declarations are audited**. Each call to `Lean.collectAxioms name` then inspects that theorem's transitive axiom dependencies; that call is not restricted to the selected-module list.

For the new audit:

1. Replace `import ReviewerControls` with:

   ```lean
   import Agent102ParameterSetControls
   ```

2. Select exactly the registry's thirteen contribution modules:

   ```lean
   let selected : List String := [
     "Agent102RunDefs",
     "Agent102AffineArithmetic",
     "Agent102RunWord",
     "Agent102RunEndpoints",
     "Agent102AffineRuns",
     "Agent102ParameterIntervalDefs",
     "Agent102ParameterIntervalAlgebra",
     "Agent102ParameterIntervalCompact",
     "Agent102AffineInequalityIntervals",
     "Agent102PiecewiseCounts",
     "Agent102AffineRunParameterSets",
     "Agent102ParameterSetDecisions",
     "Agent102ParameterSetControls"
   ]
   ```

3. Preserve the allowed axiom list exactly:

   ```lean
   [``propext, ``Classical.choice, ``Quot.sound]
   ```

4. Keep the audit in a separate file that **imports the freshly compiled modules**. The current-file declarations do not receive imported module-origin selection through this pattern; pasting mathematical source into the audit file would change its coverage.

5. Verify selected-module presence and log completeness. The original template has no explicit check that every selected module was imported and can otherwise produce a vacuous or incomplete summary after an accidental selection/import error.

The `.axiomInfo` branch rejects safe custom axioms, but **logs** unsafe implementation axioms (`ModuleOriginAudit.lean:17–19`). Thus an honest result must retain those records; it must not summarize the template as "rejecting every axiom declaration." The theorem dependency allowlist remains enforced independently.

## 4. Exact executable roots recommended

The old executable template audits only five roots (`ExecutableDependencyAudit.lean:11–13`). Those roots cover the piecewise count-comparison machinery, but they do not reach definitions introduced later merely because later modules are imported.

Retain those five roots and add eleven public entry points, for **sixteen total roots**:

```lean
for root in [
    ``Agent102.ParameterSets.CountExpr.pieces,
    ``Agent102.ParameterSets.comparisonRegion,
    ``Agent102.ParameterSets.ltRegion,
    ``Agent102.ParameterSets.leRegion,
    ``Agent102.ParameterSets.eqRegion,
    ``Agent102.ParameterSets.equalityRegions,
    ``Agent102.ParameterSets.palindromeRegions,
    ``Agent102.ParameterSets.equivalentRegions,
    ``Agent102.ParameterSets.hasEqualParameter,
    ``Agent102.ParameterSets.hasUnequalParameter,
    ``Agent102.ParameterSets.everyParameterEqual,
    ``Agent102.ParameterSets.everyParameterUnequal,
    ``Agent102.ParameterSets.hasPalindromicParameter,
    ``Agent102.ParameterSets.hasNonpalindromicParameter,
    ``Agent102.ParameterSets.everyParameterPalindromic,
    ``Agent102.ParameterSets.everyParameterNonpalindromic
  ] do
```

The additional roots correspond to the advertised interfaces:

| Interface | Source |
|---|---|
| Equality solution intervals | `Agent102AffineRunParameterSets.lean:88–91` |
| Palindrome solution intervals | `Agent102AffineRunParameterSets.lean:100` |
| Extensional interval-set certificate checker | `Agent102ParameterSetDecisions.lean:25–27` |
| Four quantified equality/inequality decisions | `Agent102ParameterSetDecisions.lean:52–60` |
| Four quantified palindrome/nonpalindrome decisions | `Agent102ParameterSetDecisions.lean:87–93` |

The equality root transitively reaches `widthExpr`, `spanExprs`, `spanExprsFrom`, `agreementRegion`, `overlapRegion`, and the interval/count machinery. Separate roots for those helpers are unnecessary to establish the advertised entry-point coverage.

An optional seventeenth root is:

```lean
``Agent102.ParameterSets.test
```

This covers the standalone interval-membership API. It is useful if the report explicitly claims executable coverage of that API; it is not reached merely by auditing the sixteen roots above.

### Preserve the forbidden list without exceptions

```lean
let forbidden : List Name := [
  ``List.range,
  ``List.replicate,
  ``Agent102.word,
  ``Agent102.wordAt,
  ``Agent102.ParameterSets.CountExpr.value
]
```

Do not exempt a forbidden dependency because it appears in a newly selected module. Do not remove a root after a failure merely to obtain a clean summary.

## 5. What the existing traversal establishes—and what it does not

The traversal checks every encountered constant name against the forbidden list **before** the selected-module expansion test (`ExecutableDependencyAudit.lean:22–26`). For selected project declarations, it then follows constants from both the declaration's type and its available value (`:29–31`).

That supplies a useful **source-level declaration dependency audit** of the selected project closure.

Its limits require accurate reporting:

### It stops at nonselected modules

Constants outside the selected modules are encountered and name-checked, but their bodies are not recursively expanded. Consequently, the result is not an unrestricted transitive audit of all `Std`, `Init`, `Lean`, or runtime implementations.

For these exact sources, the registry's closure check and inspected import graph establish that there is no omitted contribution module: all noncontribution imports come through the trusted pinned standard library. The minimal sound report should state that boundary explicitly.

If a report instead claims an unrestricted dependency closure, the traversal would need to follow external declaration bodies too. Merely extending the selected list to thirteen does not create that stronger result.

### It is not an extracted runtime call graph

The audit follows declaration types and available theorem bodies as well as executable definitions. That makes it a conservative syntactic dependency check within its selected boundary, not a precise account of proof-erased compiled execution.

Conversely, it does not inspect arbitrary compiler replacements or external implementations. No project `implemented_by`, `extern`, `unsafe`, `partial`, or custom executable extension was found in the thirteen inspected sources.

### The generic comparison callback is an input

`comparisonRegion` accepts:

```lean
atom : Affine → Affine → Interval
```

(`Agent102PiecewiseCounts.lean:94`).

An arbitrary caller-supplied callback could perform operations absent from the generic function's own declaration closure. Therefore, the audit of `comparisonRegion` alone cannot establish "no enumeration for every possible callback."

The concrete `ltRegion`, `leRegion`, `eqRegion`, and advertised higher-level solver roots fix the relevant callback implementations and are the appropriate closed interfaces for that claim.

### Add small coverage assertions

Without changing the traversal's mathematical obligation, I recommend checking:

- Every selected module appears in the imported environment.
- Every requested root exists and originates in a selected module.
- Every root visits at least one project constant.
- Exactly one final success record is present for each of the sixteen requested roots.
- Any failed lookup, forbidden dependency, unexpected project boundary, or failed command remains a failure in the retained evidence.

These assertions prevent a missing root or accidentally incomplete selection from becoming a misleading `forbidden=0` result.

## 6. Do not extend the "no word expansion" claim to all definitions

The thirteen-module contribution also contains older tail-decision functions that intentionally expand words:

```lean
def equalOnTail (A B : List RunSpec) : Bool :=
  decide (wordAt A (equalityCutoff A B) = wordAt B (equalityCutoff A B))
```

Source: `Agent102AffineRuns.lean:137–138`.

`palindromicOnTail` calls that function (`:166`).

Those are legitimate existing functions with separately stated tail specifications. They are **not** among the new interval solver's no-expansion entry points. Adding every definition in all thirteen modules as an executable root would correctly encounter forbidden `wordAt` dependencies.

Accordingly, use this scope:

> All thirteen modules were included in the fresh build and module-origin axiom audit. The sixteen named interval-construction, certificate, and quantified-decision entry points received the forbidden dependency audit.

Avoid:

> Every executable definition in all thirteen modules avoids word expansion.

The latter is contradicted by the source.

## 7. Pre-execution source safety review

No project-source occurrence was found of:

- `run_cmd`, `#eval`, or `#reduce`
- `initialize` or `builtin_initialize`
- Custom `elab`, `macro`, or `syntax`
- `IO` operations
- `unsafe`, `partial`, `opaque`, `implemented_by`, or `extern`
- `sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, or `skipKernelTC`

The source commands present are `#print axioms` and the controls' resource settings:

```lean
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
```

(`Agent102ParameterSetControls.lean:15–16`).

The controls use kernel-checkable `by decide` certificates. Source inspection of those proofs is not a substitute for compiling them.

The two audit templates do contain `run_cmd`, but their inspected bodies perform environment inspection, dependency collection, logging, and failure reporting. I found no external execution, network access, credential access, or file mutation in those bodies. Their `maxHeartbeats 0` warrants retaining the parent's external process timeout; it does not weaken kernel proof checking.

## Final disposition

**Source/audit-design result: suitable for the proposed fresh checks, with the coverage extensions and reporting boundaries above.**

A simple controlled extension is sufficient:

- Import the thirteen-module root.
- Select all thirteen registry modules.
- Retain the full axiom allowlist and forbidden dependency list.
- Extend executable roots from five to sixteen.
- Execute the complete existing 140-target literal audit.
- Check nonvacuity and output completeness.
- Preserve the distinction between all-module theorem auditing and named solver executable auditing.

**Executed Lean proof verification by this specialist: NOT_RUN.** No source repair was required or implemented.
