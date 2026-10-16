# Correction: scope of the historical 112-name dependency audit

**The historical record proves a successful rebuild of ten unchanged modules and a generated axiom audit of 112 selected names. It does not establish that all declarations of those ten modules were individually enumerated in that audit.** Any earlier wording that described the 112-name audit as covering every declaration of the dependency closure must be read with this correction.

This correction leaves the historical driver, sources, manifests, generated audit, and successful and failed logs unchanged. It adds a reproducible source census. It reports no new Lean compilation or kernel audit.

## What the historical driver actually did

`build_independent.py` first compiled all ten modules in `order`. It then used **`for module in order[1:]:`**, explicitly excluding `LychrelDigitSums` from the generated name list. Within the remaining nine modules it used:

```python
r'^(?:noncomputable )?(?:def|theorem|abbrev)\s+([A-Za-z0-9_]+)'
```

This recognizes only declarations beginning at column zero with those forms. It does not in general handle indentation, private/protected modifiers, declaration attributes, structures, inductives, or compiler-generated constants. It also hard-codes the three Agent13 namespaces. The saved `IndependentDependencyAudit.lean` contains exactly the 112 names produced by that strategy, in the same order. The successful audit log remains evidence about those names and their transitive axiom dependencies.

In these exact nine selected sources there is **no additional indented `def`/`theorem`/`abbrev` declaration** missed by that expression. The explicit declaration missed there is `inductive CarryPath` in `CarryPath.lean`. The much larger omission is the complete exclusion of `LychrelDigitSums` from the generated name list.

## Exact retrospective counts

The new source census strips nested Lean block comments, line comments, and strings while preserving line positions, allows leading spaces and declaration modifiers, and counts the named source commands listed in `census_coverage.py`. This is a static source census, not an environment-origin inventory of all generated constants.

| Compiled historical module | Names in old generated audit | Comment-aware explicit source declarations | Absent from old generated audit |
| --- | ---: | ---: | ---: |
| `LychrelDigitSums` | 0 | 362 | 362 |
| `Trace` | 15 | 15 | 0 |
| `WholeWord` | 17 | 17 | 0 |
| `Safety` | 12 | 12 | 0 |
| `Indexing` | 12 | 12 | 0 |
| `FiniteWords` | 21 | 21 | 0 |
| `FamilyStates` | 9 | 9 | 0 |
| `Products` | 12 | 12 | 0 |
| `Obstruction` | 6 | 6 | 0 |
| `CarryPath` | 8 | 9 | 1 |
| **All ten** | **112** | **475** | **363** |
| **First seven, used by the final Incoming dependency closure** | **86** | **448** | **362** |

The other 26 old audit names come from `Products`, `Obstruction`, and `CarryPath`, which are outside the final seven-module historical dependency subset. The separately recovered `Lychrel196Research.lean` is provenance material, not an eleventh module in this historical build; its original text is incorporated into the pinned `LychrelDigitSums.lean`.

`LychrelDigitSums` contains 63 `def`, 296 `theorem` (including five private theorems), two `structure`, and one `inductive` source commands. The earlier provisional count of 447 for the seven-module subset omitted the real one-space-indented `witness_carries` at line 3289. The text `theorem decimal196` at line 253 is inside a comment and is not a declaration. Correcting both issues gives **448**, independently matched by the semantic reviewer's comment-aware count.

Several historical source files contain their own `#print axioms` commands; their output remains in the corresponding compilation logs. The “absent” column refers precisely to absence from the generated 112-name audit, and does not assert that every absent name was absent from every historical log.

## Verification limits and what remains valid

All ten historical compile commands and the generated audit command exited zero. Their saved commands **do not specify `--trust=0`**, and the historical wrapper adds no trust flag. This record must be described as the original default-mode compilation and selected-name axiom audit; it must not be relabeled an explicit trust-zero run.

The original source checks remain valid. In particular, the omitted `LychrelDigitSums` enumeration concerns the exact unchanged source at commit `12a32789056f5eec8247166564ac2ef745c3c9d6`, repository path `proofs/research/continuation/LychrelDigitSums.lean`, Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`, SHA256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. All per-module provenance remains in `source-map.json`.

This coverage correction does not change the separately checked Incoming source or the transitive `#print axioms` results for its audited theorems. The planned final 17-module environment-origin audit is a separate coverage expansion; its own commands, results, and scope must be reported from its actual output. This correction does not pre-claim that result.

## Reproduce the retrospective census

From this directory, with the recovered dependency directory available:

```bash
python census_coverage.py \
  --dependencies /workspace/scratch/b31b8818d547/agent108-dependencies \
  --output census-coverage-new.json
```

The output file must not already exist. The script verifies every original evidence-file hash recorded in `REVIEW_MANIFEST.json`, checks each source SHA256 against `source-map.json`, reproduces the 112-name list exactly, and records all explicit source matches with module, line, kind, and name. The executed report for this correction is `census-coverage.json`. These new files supplement the historical evidence without editing it.
