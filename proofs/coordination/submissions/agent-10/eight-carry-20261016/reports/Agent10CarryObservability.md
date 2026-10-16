# Agent 10: eight-carry reconstruction and six-carry obstruction

This package strengthens the existing ordinary-decimal carry-observability results. It removes the extra counting hypothesis from eight-observation reconstruction under a small initial difference, proves that initial nonoverflow supplies that difference bound, recovers the exterior pair sum from eight observations without the nonoverflow hypothesis, and certifies two ordinary integers that remain indistinguishable for six complete observations.

The eleven-module source closure is **LEAN_CHECKED** with Lean 4.19.0. This is a scoped proof package, not a repository-wide verification result or a proof of the 196 conjecture. Source integration and external acceptance are separate from the recorded local checks.

## Exact meanings

Digits and pair coefficients are indexed from the least significant end. For a canonical width-`L` digit function `d`, the pair coefficient is `q i = d i + d (L - 1 - i)` for `i < L`. The unchanged `Admissible L q` predicate includes positive width, positive exterior coefficient, coefficients at most 18, reflection symmetry, and an even coefficient at an odd-width center.

A complete observation at time `t` is every incoming carry at indices `0` through the actual current width, inclusive. Thus the final overflow carry is included. Eight observations mean `t = 0,...,7`: seven transitions followed by their endpoint observation. Both inputs start at the same canonical width; matched terminal carries synchronize their subsequent widths.

The conclusions recover pair sums, or the next reverse-and-add integer. Different initial digit splittings can have the same pair sums, so initial-integer equality is not a claimed conclusion.

## Principal checked results

| Result | Hypotheses beyond the indicated domain | Conclusion | Source endpoint |
| --- | --- | --- | --- |
| Seven-transition count | `Admissible L q`, including `L = 1` | `3 <= orbitCount q L 7` | `Agent10SevenStepCount.actual_seven_step_count_all_widths` |
| Eight-observation reconstruction with small difference | Two admissible words at common initial width; eight equal complete carry words; zero-extended initial coefficient difference in `[-5,5]` | `q i = r i` for every `i < L` | `Agent10EightCarry.eight_carry_words_determine_pair_sums_of_small_difference` |
| Eight-observation reconstruction from initial nonoverflow | Two admissible words at common initial width; eight equal complete carry words; initial terminal carry zero | Equality of all initial pair sums in range | `Agent10EightCarry.eight_carry_words_determine_pair_sums_of_initial_nonoverflow` |
| Ordinary-integer consequence | Canonical representations of `n,m` at common initial width; the same carry hypotheses and initial nonoverflow | `Lychrel196.step n = Lychrel196.step m` | `Agent10EightCarry.eight_carry_words_determine_next_integer_of_initial_nonoverflow` |
| Universal exterior reconstruction | Two admissible words at common initial width; eight equal complete carry words | `q 0 = r 0`, without an initial-nonoverflow premise | `Agent10PrefixExclusion.eight_carries_determine_exterior_pair` |
| Concrete six-observation obstruction | Two explicitly proved canonical width-eleven inputs | Six complete carry words agree, but initial exterior pair sums and next integers differ | `Agent10SixCarryCounterexample.six_carry_counterexample` |

The existing nine-observation theorem in `DifferenceObservability` remains the general full-reconstruction result. This package does not replace it with an unconditional eight-observation theorem for every interior coefficient.

## Why the eight-observation proof works

The seven-transition count proof checks the finite exterior state potential and transports it through the unchanged actual prefix dynamics. A separate finite check handles singleton widths, with finite-prefix congruence avoiding any assumption on irrelevant function tails.

Let `f` be the initial difference, extended by zero beyond the width. The inherited matched-history formula expresses the difference after seven transitions as a power of two times a binomial smoothing of `f`. If at least four of those transitions do not overflow, the existing endpoint injectivity theorem already applies.

Otherwise the new count bound forces exactly three nonoverflows. The difference at time seven is then `8 * smoothPow 4 f`. Its complete carry observation bounds each coefficient between -9 and 9, so integer arithmetic bounds each coefficient of `smoothPow 4 f` between -1 and 1. The inherited Agent 10 theorem proves that this forces `f = 0` when `f` is bounded by five. Initial nonoverflow together with the first two matched observations supplies the stronger input bound four. Neither combined reconstruction endpoint assumes the nonoverflow count separately.

For the unconditional exterior result, the initial complete carry word supplies the general bound nine. If `f 0` were nonzero, the first four smoothed coefficients force the leading difference to be `(1,-3)` or `(-1,3)`. `Agent10PrefixWitness` exhaustively excludes all 272 valid starting pairs with the positive orientation after seven observations, over every shared Boolean inner-carry path. The negative orientation follows by exchanging the inputs.

`Agent10PrefixExclusion.actual_history_survives` proves the essential semantic inclusion: every actual matched history generates a path in that graph. The graph is only a necessary projection. No claim that an arbitrary graph path has an ordinary-integer realization is used. The singleton boundary is discharged using the zero extension.

## Concrete ordinary integers

| Quantity | Left input | Right input |
| --- | ---: | ---: |
| Initial integer | 80000571539 | 70000817069 |
| Initial canonical width | 11 | 11 |
| Exterior pair sum | 17 | 16 |
| Next reverse-and-add integer | 173518071547 | 166072617076 |
| Incoming carry at time 6, index 1 | 1 | 0 |

The actual widths at times zero through six are `[11,12,12,13,13,14,14]` for both inputs. All 81 carry positions over observations zero through five agree, including each terminal carry. The seventh observation differs.

The Lean source proves both canonical digit representations and checks each adjacent recorded coefficient row against the original `nextWidth` and `nextColumns`. Finite-prefix congruence then transports the rows to `iterPairs`. The ordinary-numeric orbit representation is derived from the existing representation theorem; the example is not merely an abstract coefficient trajectory.

The initial difference is `[1,-3,5,-6,6,-6,6,-6,5,-3,1]`. Its maximum absolute coefficient is six, and both initial additions overflow. It realizes the inherited coefficient-six smoothing witness for six observations. It separates at observation seven and therefore establishes neither seven- nor eight-observation insufficiency.

## Verification and provenance

- Tested source commit: `9f5a2c1e19057b02193e95bdfc50421e89f53094` in the isolated Agent 10 checkout.
- Original main baseline: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
- Exact registry: `Agent10CarryObservability.registry.json`, SHA-256 `9635ed407369a8ba6b3ecd03a1a9027f440951b95e26e478fe67f453859a75d2`.
- Unchanged canonical verifier: `verify_project__214bf7673efe116b.py`, SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
- Clean build: eleven source modules plus `ProjectAudit`, twelve successful commands, 1,122 distinct theorem-origin records, and 49 registered endpoint types. The count includes inherited, private, and generated theorem declarations.
- Canonical report SHA-256: `830adbc8762485817a90a8b26e4d93d5ab1950162cab6cfae8ada96545d234fb`.
- The complete theorem axiom union is exactly `{propext, Classical.choice, Quot.sound}`. Thirteen inherited unsafe implementation-specialization declarations are separately inventoried; none appears in any theorem's transitive axiom set. No new-module unsafe axiom occurs.
- All 25 canonical manifest entries, source bytes, command-log hashes, 49 endpoint types, and corresponding printed axiom lists were independently checked against the retained report. The inherited verifier's fixed `Agent #1` metadata is preserved; the actual expanded build executor is Agent 10's parent, and the receipt validator is the separate `formalization_scout` specialist.
- A non-author internal specialist, `lean_runtime`, reviewed the five new count/reconstruction/prefix/counterexample modules and recorded 31 semantic checks with no blocking findings. This is internal independent review, not a separate GitHub identity, maintainer approval, or CI run.

The original `Agent10EightCarry.registry.json` and its eight-module verification checkpoint are retained unchanged. `Agent10SmoothingBoundary.lean` and `Agent10SmoothingBridge.lean` are byte-identical to the inherited Agent 10 checkpoint. Their original failed-execution and later successful evidence remain distinguished.

Authorship: the parent authored `Agent10EightCarry`; `formalization_scout` authored the count and concrete counterexample modules; `eight_carry_semantics` authored the prefix graph and actual-history exclusion modules. The proof sources retain the attribution of imported results.

## Reproduce

Apply the supplied additive patch to the stated baseline, or to a later main commit after `git apply --check` succeeds. Use the official Lean 4.19.0 release, commit `6caaee842e94`. The runtime archive SHA-256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; the Linux `bin/lean` SHA-256 used here is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

From the repository root, using a new output directory:

```bash
python -B proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent10CarryObservability.registry.json \
  --project agent10-carry-observability \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-agent10-build
```

The explicit project selection is intentional: this registry is scoped and does not assert a complete repository census. The verifier stages the exact pinned source files under their module names, compiles from an empty directory, audits every theorem whose origin is in that closure, and emits `verification.json`, full logs, generated audit source, and `FILES.json`.

This closure uses the standalone `Lychrel196Research` foundation. If combining it with a chain importing `LychrelDigitSums`, use the repository's verified embedded-foundation compatibility mechanism; importing duplicate foundation definitions directly is not a valid integration.

## Remaining mathematical boundary

Unconditional recovery of every interior pair coefficient from eight observations remains outside this package. The separately checked `Agent10TwoPairReconstruction.md` extension recovers the first two active coefficients; it retains its own expanded registry and verification scope. The next general obstruction is temporal consistency of the omitted common prefix and boundary carries: unconstrained local control paths can survive even when they have no actual full-word lift.

Finite scans and their exact scopes are retained under `calculation/agent10-carry-observability-20261016`. They guide theorem selection and supply examples; their classifications remain distinct from the Lean proofs. No result here establishes infinite palindrome avoidance, an optimal universal observation count, or that 196 is Lychrel.
