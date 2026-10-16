# Agent #1 independent review: four branch-only packages

Task: `agent1-consolidation-20261015T1901Z`. Reviewer: Agent #1, not an author of the ten mathematical source files below. This is an independent AI-agent source and execution review, not human or external peer review.

Verdict: **READY_TO_INTEGRATE for the precisely scoped results below**, after the published entry point and combined-tree replay are verified. This review is not an assertion that a main merge already happened, that every file on these branches is accepted mathematics, or that the repository-wide accepted build is complete.

The staged mathematical tree is `4e4dc4f7ac527cd43396afb119d3e23c4b4996a8`, published in staging commit `74dcde599806d90f7d386e1341cc744968a57904`. It combines main `6d56f543933dedb83eee8215f0e7295a5363c02c`, the existing Agent #1 evidence, and ten unchanged source blobs. No existing mathematical source was edited or deleted. The complete initial histories remain reachable from `archive/agent-1/20261015T1904Z` at `eef3ecc100ae1038f6556c1600b85bf0200914f6`; the synthetic archive is not merged into main.

## Source and destination mapping

| Original pinned contribution | Unchanged canonical source destination | Accepted scope |
|---|---|---|
| Agent #3, `research/agent3-complementary-bulk-20261015`, `34c32e5455e8828161b89051cdd3bfe41176da07` | `proofs/contributions/2026-10-15-agent3-complementary-bulk/OuterOrbit.lean` | Five-step charge extinction and sharpness for the explicitly defined outer list map. |
| Agent #9, `research/agent9-alternating-scalar-20261015`, `c74581b4f146e1b540e4ef3713468c02b54728e6` | `proofs/contributions/2026-10-15-agent9-alternating-scalar-boundary/AlternatingScalarBoundary.lean` | All finite spatial widths in the exact N/O cut relation, with arbitrary forward-infinite temporal traces. |
| Agent #11, `formalize/agent-11/s20261015-coverage`, `eefa6fee230d996065d9077b8ae2246af67d6e30` | Five `HighBase*.lean` files under `proofs/contributions/agent-11/base-high-threshold/` | Canonical arithmetic threshold and first-positive-palindrome classification in every integer base at least three. |
| Agent #10, `research/carry-observability-20261015`, `0b14bd101430e16ab06a5a9c706f0eda0a83767e` | `PrefixCarryBound.lean`, `ActualCarryObservability.lean`, `DifferenceObservability.lean` under `proofs/contributions/2026-10-15-carry-observability/` | Complete nine-word carry reconstruction at all positive admissible decimal widths, with an ordinary-integer next-step consequence. |

The registry records every original source SHA-256, Git blob and canonical path, plus imports and theorem endpoints. Its full reviewed path/hash/import-map identity is `59f7f540d107a7d35b27c4a00cc0e5075ec6fc8a5bf6a8114eeb34855e75e931`. The generator rejects any different map instead of silently accepting later source changes.

All five Agent #11 files were already retained byte-for-byte under Agent #116's `integration/historical-review-deps/` (two checkpoint directories, `agent11-42a165aa` and `agent11-eab4e083`). Those review copies remain unchanged. Restoring the author's canonical source paths makes the result directly importable; it does not erase independent review history.

Other original contracts, checkers, workflows, author logs and intermediate variants remain in the retained initial Git history. They are **SUPERSEDED_BUT_PRESERVED as operational/provenance artifacts** relative to this common checker, not silently promoted to newly independently verified mathematics. Source branches remain in place. No branch deletion or unresolved issue closure is authorized by this batch.

## Mathematical reconciliation

### Agent #3: exact outer map, not an unproved arithmetic bridge

The reviewer read `OuterCharge` and `OuterOrbit`, including the actual two-direction normalization, natural-number subtraction bounds, trimming, validity closure, leading-coefficient bound and orbit induction. `Valid c B` requires the displayed phase range, excludes phase nine, bounds exterior coefficients by eighteen, and requires a positive outside coefficient. Nonzero charge forces the relevant nonoverflow history; its positive leading coefficient doubles, so it cannot survive five steps while remaining at most eighteen. The zero residue is preserved afterward. The return-orbit theorem uses a positive return period, rather than assuming periodicity for arbitrary inputs. The concrete phase-one empty-exterior witness has nonzero charge after four steps and zero after five.

Accepted statements concern `P196.Agent3.Charge.step` and its iterates. The ordinary decimal whole-word semiconjugacy is a separate missing formal bridge. No claim that every actual 196 exterior follows this map is introduced.

### Agent #9: correct quantifier order in the spatial obstruction

The reviewer checked the `Slot`, `Valid`, `Tile`, `Trace` and `Step` definitions. Local integer division and remainder constraints retain bounded carries, the pending digit constraint and the next-time coefficient. A predecessor of the specified six/twelve constant trace has only two letters; a further predecessor eliminates the exceptional letter after one temporal shift. Induction shortens a finite spatial path while shifting the arbitrary forward-infinite temporal traces. It does not assume temporal periodicity or replace the infinite traces by a finite sample.

The conclusions `no_six_boundary` and `no_twelve_boundary` exclude the stated root-to-constant paths in this exact relation. The relation-to-ordinary-exterior bridge remains OPEN. This is neither an infinite decimal safety certificate nor a general Lychrel theorem.

### Agent #11: canonical widths, all-base arithmetic and first positive time

All five files were read, including their source hypotheses and derivations. Ordinary false-tag carry normalization is proved to preserve canonical digit bounds and a positive leading digit, with exact evaluation equal to the old integer plus its reversed digit evaluation. The first high-region output has its actual overflow width, including width one. The derived pair formula uses adjacent old pair sums; no independent-interior assumption is introduced.

For integer base `b >= 3`, symmetric pair sums in `[b-1,2*b-2]` and an outside pair at least `b` give the exact second-palindrome threshold: every adjacent pair-sum total is at most `3*b-3`. On the narrower interval `[b-1,b+(b-1)/2-1]`, the first **positive** palindrome time is one exactly when every pair sum is `b+1`, and otherwise is two. The original numeral may already be palindromic. The arithmetic iteration deliberately continues after palindromes. The base-two counterexample is retained; no unsupported extension to base two is accepted.

### Agent #10: full carry histories determine pair sums, not initial digits

The finite two-column graph includes all 342 valid initial states and both incoming carry choices. Its packed rank literal is untrusted data checked by kernel reduction of all local inequalities. Actual-orbit inclusion is separately proved, including a direct one-column boundary check. This gives at least four nonoverflow steps in nine transitions and at least three in eight.

For two admissible words with identical complete carries, equality includes index zero and the terminal carry at each current width. Equal widths at later times are derived. Zero-extended pair-sum differences evolve by multiplication by two on nonoverflow steps and by the smoothing operator on overflow steps; the extra overflow column is included. If eight transitions contain four nonoverflow steps, the earlier injectivity result applies. In the remaining case there are three such steps and five smoothings; the bounded first-nonzero-coefficient argument forces the initial difference to vanish. No circular assumption of the desired pair-sum equality is used.

The all-width endpoint quantifies carry equality at times zero through eight. Its canonical numeric corollary proves equality of **the next integers**. It does not claim equality of the initial integers or optimality of nine observations. The next-integer result uses the existing ordinary `Lychrel196.step` correspondence, not a replacement decimal transition.

## One consistent foundation and combined build

The complete registered source closure contains 38 modules, including all twenty previously accepted PR47 modules. Every project object was rebuilt from an empty directory with official Lean 4.19.0, release commit `6caaee842e94`, `-j1 -DElab.async=false`.

A naive import union would duplicate the arithmetic foundation: the standalone `Lychrel196Research.lean` is embedded in `LychrelDigitSums.lean`. The reconciler verifies that all 4,444 lines after the standalone `import Std` are byte-identical to lines 11 onward of the canonical extension, with both full source hashes pinned. Only the generated build copy of `Lychrel196Research` becomes `import LychrelDigitSums`; all historical originals remain untouched. This is a verified identity of declaration bodies, not a guessed equivalence between differently defined arithmetic.

The independently executed combined build finished at `2026-10-15T19:59:33.447784Z`, with every module exit zero. Its complete module-origin audit checked **3,491 theorem constants**, including transitive project dependencies, private theorems and generated auxiliaries. Allowed axiom dependencies were only `propext`, `Classical.choice`, `Quot.sound`. Compiler-implementation unsafe axioms were separately inventoried and are not allowed as mathematical dependencies. No sorry/admit/custom mathematical axiom/native_decide shortcut was accepted.

The original combined audit log SHA-256 is `a286bccd2e3003d14f0436d57a4c8da104c06fcbc5d8717ad1f6f0243ddec39e`; its complete build-source record digest is `58187ed64d27998a2053d81e9ea896854c51893eeb32b36b8b950008da5c5b6a`. These are distinct serialization formats from the registry's normalized source-map digest. Raw local execution files are preserved, and the published entry-point replay is a separate execution, not a fabricated copy of these results.

## Independent finite controls

Literal base arithmetic checked 60,683 positive canonical seeds in bases three through twelve and widths at most four; 16,752 satisfied the full threshold hypotheses and 8,460 the narrower first-hit interval (460 first-positive hits at one, 8,000 at two). These controls include initially palindromic numerals and continue the specified arithmetic after hits.

Literal decimal carries were grouped for all 99,999 positive seeds below 100,000 over times zero through eight. All 96,030 equal-history collisions had the same pair sums and next integer, while distinct initial integers were allowed. An independent dynamic program recomputed all 684 edges of the 342-state necessary graph; minimum nonoverflow counts at horizons one through nine were `0,0,0,1,1,2,3,3,4`.

The explicit outer map was checked for 109,744 valid initial states (sixteen phases, exterior length at most three, coefficients zero through eighteen with positive outside coefficient), through time seven. All had zero charge from time five. These finite checks supplement the universal proofs; no finite range is promoted into their unbounded quantifiers or into an ordinary-integer bridge.

## Reproduction and open integration obligations

After generating the checked registry, use a nonexistent output directory:

```sh
python3 proofs/contributions/agent-1/consolidation-20261015/make_accepted_registry.py
python3 proofs/verify_project.py --lean /absolute/path/to/lean --project consolidation-core --output /tmp/p196-consolidation-core
```

The full project checker verifies original bytes, import closure, the foundation identity, named endpoints, fresh compilation and every project theorem's transitive axiom dependencies. `--check-only` is explicitly source/import validation, not proof verification.

Default mode, without a named project, must not report repository-wide PASS while the accepted catalogue is incomplete. Previously accepted scopes outside this first registry remain accepted under their original reports and are still obligations for the global orchestrator. The initial 478-file legacy manifest omission is also a baseline blocker until complete index regeneration and coverage validation. Neither is hidden by the successful 38-module scoped build.
