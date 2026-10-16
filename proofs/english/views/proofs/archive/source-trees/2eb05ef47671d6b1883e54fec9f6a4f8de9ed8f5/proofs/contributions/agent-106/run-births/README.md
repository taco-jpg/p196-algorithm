# Agent #106: births of actual extreme coefficients and population obstructions

This contribution proves that one decimal reverse-and-add step can simultaneously create arbitrarily many 0 and 18 coefficients from a pair-coefficient word containing neither 0 nor 18. It also constructs arbitrarily many mutually separated new runs with integer realizations. This gives an explicit birth obstruction to controlling all extremes using only the lifetimes of old runs.

Task: `agent106-run-births-formal`; branch: `research/agent-106/20261015-0442`. The source checkpoint for the nine completed modules is **`ac08faa3a873945dbd192f40ff136d8b17d0d015`**. Status: **INDEPENDENTLY-REVIEWED**, not yet marked INTEGRATED. See [checkpoint.json](checkpoint.json) and the [final review](review/coordinator-clean/REVIEW.md) for exact source hashes, commands, and results.

A coefficient means `q i = d i + d (L-1-i)`, ordered from low to high digits. The value 18 is a sum of mirrored digits, not a decimal digit. The update uses the repository's existing actual carries and `FoldedDecimal.nextColumns`. Integer correspondence uses `DecimalDigits.Canonical` and `Lychrel196.step n = n + reverse10 n`.

| Completed module | Exact role and scope |
|---|---|
| [NoOverflowBirths.lean](NoOverflowBirths.lean) | Necessary-and-sufficient 0/18 classification, fresh-birth classification, and central parity restrictions for the actual nonoverflow branch. |
| [OverflowBirths.lean](OverflowBirths.lean) | Complete adjacent-column/carry classification for overflow interiors; fresh extremes must touch an old 9; neither endpoint can be 0/18. |
| [BirthFamily.lean](BirthFamily.lean) | An actual parametric birth family for every `g≥2`, positive-integer realization, and finite nonpalindromicity of the input and first two steps. |
| [BaseBirths.lean](BaseBirths.lean), [ActualBaseBirths.lean](ActualBaseBirths.lean) | General-base local classification and the actual-integer bridge with canonical digits, ordinary carries, and no overflow. |
| [PopulationObstructions.lean](PopulationObstructions.lean) | Kernel `decide` verification of step 5→6 from 196: counts of 0/18 columns and runs change from `(0,0,0,0)` to `(1,2,1,2)`, excluding globally nonincreasing potentials with positive integer linear weights on those four quantities. |
| [UnboundedBirths.lean](UnboundedBirths.lean) | An actual one-step family for arbitrary `k,r : Nat`, exact extreme positions, and ordinary positive-integer realization. |
| [PopulationGrowth.lean](PopulationGrowth.lean) | Full physical-width counts of `2r` new zero columns and `2k` new 18 columns, totaling `L−6`. `simultaneous_integer_births_unbounded` and `no_uniform_integer_total_bound` explicitly quantify actual integers and arbitrary constant bounds. |
| [RepeatedBirths.lean](RepeatedBirths.lean) | Each length-ten block creates one maximal length-two zero run and two maximal singleton 18 runs. `arbitrarily_many_separate_birth_runs` supplies an explicit injection for arbitrarily many distinct runs and nonextreme neighbors; `numeric_family_realized` supplies the integer bridge. A separate List `runCount` equality is not proved. |

The simultaneous-birth family is `(1,9^k,1,10,9^(2r),10,1,9^k,1)` → `(2,18^k,3,1,0^(2r),1,3,18^k,2)`, with width `L=2k+2r+6`. Powers mean repetition; the proof includes `k=0` and `r=0`. Separated new runs use finite repetitions of block `(1,9,1,10,9,9,10,1,9,1)`, whose successor block is `(2,18,3,1,0,0,1,3,18,2)`. These parameters vary input size, not infinite time along one orbit.

## Verification and reproduction

The final empty-directory rebuild compiled nine new modules and seven source dependencies, then audited 288 declarations; every command exited with code 0. Only subsets of the project's permitted `propext`, `Classical.choice`, and `Quot.sound` occurred; some finite certificates depend on no axioms. No `sorry`, new axiom, or `native_decide` was accepted, and transitive dependencies were audited.

At the repository root, use Lean **4.19.0** and a new empty build directory:

```sh
python3 -B proofs/contributions/agent-106/run-births/check.py \
  --lean /absolute/path/to/lean \
  --build-dir /absolute/path/to/empty-build \
  --evidence-dir /absolute/path/to/new-evidence \
  --modules NoOverflowBirths OverflowBirths BirthFamily BaseBirths \
    ActualBaseBirths PopulationObstructions UnboundedBirths \
    PopulationGrowth RepeatedBirths
```

The runner explicitly includes all nine modules, rebuilds local dependencies from original source, pins foundation source hashes, and prints transitive axioms for newly exported theorems and definitions. The foundation commit is `496db91fbd927f34a5396fb558f3a045df607608`; main at `7a05c34` did not change those dependencies when synchronized. The environment's path-discovery correction is in [runtime_readlink_self.c](runtime_readlink_self.c); an ordinary Lean installation does not need it.

Independent evidence is in `review/independent/`, `review/nooverflow-reviewer/`, `review/allbase-reviewer/`, and `review/base-reviewer/`. The latter's execution-quota interruption and missing machine summary are explicitly recorded; the complete coordinator rebuild supplies the remaining verification. Agent #103 separately downloaded the official compiler at commit `dc6c2ab51b5f69f63266bf6732389b39618ac6dd` and reviewed two modules from the early `8aa86f52...` checkpoint; the final review specifies the exact version scope.

## Preservation scope and next obligation

`development/` retains available failed sources, compiler logs, and API probes, outside the accepted module list. `population_results.json` retains the complete finite enumeration; it and the Python controls support discovery and cross-checking, while the universal conclusions come from Lean. [INVENTORY.json](INVENTORY.json) records file-level preservation and infrastructure exclusions. Git history preserves historical states, updated by this description and the final review. Shared indexes remain the integration owner's responsibility.

A regeneration mechanism that repeatedly triggers along one actual orbit, maintains valid width, and avoids palindromes is still missing, as is a global invariant controlling all newborn runs. This contribution proves neither existence nor nonexistence of such a mechanism. Agent #102's old-run ancestry and lifetime task remains separate. Analogues with positive real/rational weights were not formalized separately; the accepted weight theorem has scope `Int`.

The infinite nonpalindromicity of 196, existence of a decimal Lychrel seed, and an infinitely safe orbit remain unproved here. Different AI executors performed the independent reviews; these are not external human peer review or claims of literature novelty.
