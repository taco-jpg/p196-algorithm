# Independent review of the coordinate-only digit-stream extension

**Verdict: PASS for the exact local exterior statements. No blocking semantic defect found.**

Reviewer: Agent #5's independent semantic reviewer, `/root/semantic_review`. The reviewer authored none of the reviewed Lean theorems. This extension review adds to the frozen four-module, 25-export core review. It does not replace or revise that earlier record.

The five new Agent #5 theorems correctly reuse Agent #6's published overflow interface to remove the normalization scan from the digit formula's high denominator. The resulting right-hand side depends on the phase, exterior length, `zValue`, and `rhoNum`. The exact abstract `outerNext` function remains the target. The existing phase and coefficient hypotheses remain necessary to the proved digit reconstruction.

## Source identity and scope of the review

| Source | SHA-256 | Git blob |
|---|---|---|
| `CoordinateThreshold.lean`, Agent #6's original contribution path | `c50a07ee9dc4d3eff6e25b623235037850bc5a883ec057655503cc7a6cd068d8` | `34ddc74962d8bbef954f1626a80593de60906215` |
| `CoordinateOnlyStreams.lean`, Agent #5's fifth module | `e35e191a0aa7a848bcc7ec752f09db6081c9065c33a20c035a3d764622f09540` | `ededd5c92fe852d19bfe61bac7a6acd803e65240` |

The extended registry snapshot is `registry.json`, SHA-256 `eda9491e6b1fc3ededc1df8a44629d6da8b82f418fc1e619443b89ef8c4213c8`. It contains nine modules and 30 distinct Agent #5 exports. The source inventory pins every imported module and records the exact contracts of all 16 written public theorems and three definitions in Agent #6's module, plus all five new Agent #5 theorems.

All seven earlier source files match both the original semantic inventory and the source copies from the reviewer's independent fresh strict core replay. All 29 files listed by the immutable core review manifest were rechecked unchanged. That manifest retains SHA-256 `d12ec173d5d132d379b36e732d4dabe0bab73648ba8da393e1d574d6e556247f`. No core proof or review file was edited for this extension.

## Meaning of the imported Agent #6 interface

Write

\[
n=|B|,\qquad H=\operatorname{highValue}(B),\qquad
k=\mathbf 1_{10\le c},\qquad r=9H+c,\qquad D=9\cdot10^n.
\]

The actual outgoing carry is the final carry of `normalize B.reverse k`. Agent #6 proves the unconditional scan formula

\[
g=\left\lfloor\frac{H+k}{10^n}\right\rfloor.
\]

For natural phases satisfying `c ≤ 17` and `c ≠ 9`, the phase carry satisfies `k = c / 9`. Natural division is Euclidean division here, and the positive denominator is explicit. Consequently,

\[
\left\lfloor\frac{9H+c}{9}\right\rfloor=H+k,
\qquad
g=\left\lfloor\frac{r}{D}\right\rfloor.
\]

The second equality uses the exact natural-division identity for successive division by 9 and by `10^n`. It needs no coefficient bound, no parity condition, and no positive or nonempty head. The zero-carry equivalence `g = 0 ↔ r < D` has the same weak hypotheses and likewise allows arbitrary natural coefficients.

The coefficient bound `∀ x ∈ B, x ≤ 18` is used to show `g ≤ 1`. This follows from the existing carry bound because the initial carry is always at most one. It converts the positive-carry criterion to the precise bit selector

\[
g=1\quad\Longleftrightarrow\quad D\le r.
\]

The additional bound `r < 2D` follows from the same quotient and bit facts. Agent #6's `empty_word_quotient_iff` and `quotient_identity_forall_iff` establish that `c ≤ 17 ∧ c ≠ 9` is exactly the phase domain on which the quotient identity works for every natural word: evaluating at the empty word already forces it. These contracts are substantive, with explicit failing examples at phases 9 and 18. They do not assume the identity in order to conclude it.

The bound excludes neither `c = 0` nor odd phases in the Agent #6 interface. The new Agent #5 endpoints intentionally use the stronger existing eight-phase predicate. Its values are `2, 4, 6, 8, 10, 12, 14, 16`, and the first wrapper theorem supplies the two weaker Agent #6 hypotheses by direct arithmetic.

## Exact interpretation of the five new Agent #5 exports

All names below have prefix `Agent5.ExactDigitStreams.`

| Export | Exact content and hypotheses |
|---|---|
| `nonneutralPhase_coordinate_bounds` | From `nonneutralPhase c`, conclude `c ≤ 17 ∧ c ≠ 9`. No word is involved. |
| `overflow_eq_coordinate_selector` | For `nonneutralPhase c` and all coefficients of `B` at most 18, the actual final right scan carry equals `if 9 * 10^B.length ≤ rhoNum c B then 1 else 0`. |
| `outerNext_from_coordinates` | Under those two hypotheses and `B.length + 1 ≤ cut`, reconstruct the exact `outerNext` structure using two streams of length `cut`, with the threshold selector in the high denominator. |
| `outerNext_from_coordinates_quotient` | The same exact reconstruction and hypotheses, replacing the threshold exponent by the natural quotient `rhoNum c B / (9 * 10^B.length)`. |
| `fractionDigits_coordinates_digits_lt_ten` | Under the phase and coefficient hypotheses, every entry of every requested high prefix is below 10 using the coordinate-selected denominator. No lower bound on the requested prefix length is needed. |

More explicitly, let

\[
a=\operatorname{zValue}(c,B)-c,
\qquad
\varepsilon=\mathbf 1_{D\le r},
\qquad
c'=\operatorname{bulkPhase}(c).
\]

For each `cut ≥ n + 1`, the successor exterior word is

\[
\operatorname{stripSuffix}_{c'}\left(
\operatorname{zipWith}_{+}\left(
\operatorname{adicNumeratorDigits}(\mathrm{cut},a),
\operatorname{fractionDigits}(\mathrm{cut},r,D\,10^{\varepsilon})
\right)\right).
\]

The quotient version uses `ε = r / D`. The low numerator remains an integer and may be negative. The streams, word orientation, natural subtraction in the original update, and stripping rule are unchanged from the independently reviewed core.

The proofs are thin rewrites of `outerNext_from_streams_of_cutoff` and the existing high-digit bound. They do not define a substitute successor, silently normalize the input word, add a canonical-head condition, or weaken the conclusion to equality of coordinates. The result is equality of the complete `Outer` structures. The dependency graph has no cycle: both the core factorization dependency and the new threshold module precede the wrapper.

The quotient theorem's weaker arithmetic hypotheses do not justify dropping `hB` from the quotient-based digit endpoint. The core identity still relies on the carry being a bit; the original successor inserts the single leading digit 1 whenever that carry is nonzero.

## Boundary evidence and nonvacuity

The extension's independent exact-integer controls passed 9,945 instances of the unrestricted-coefficient quotient and zero-carry criterion, 57,920 bounded eight-phase selector states, 9,144 sufficient-cutoff prefix cases checked against both coordinate endpoints, and 100 empty-word phase-characterization cases. These computations supplement the source and kernel review; they are finite checks rather than a substitute for the universal Lean theorems.

The principal boundary checks are:

| Control | Result and implication |
|---|---|
| `c = 12`, `B = []` | `r = 12`, `D = 9`, selector and quotient both 1, scaled denominator 90, and low numerator −12. At cutoff 1 the low digit is 2 and the high digit is 1, giving exact successor `(6, [3])`. The empty high-phase case is included and is not vacuous. |
| `c = 0`, `B = [10]` | `r = D = 90` and actual carry 1. This is in Agent #6's phase domain and checks the inclusive threshold boundary. It is outside Agent #5's eight-phase endpoint domain. |
| `c = 9`, `B = []` | Actual carry 0 but quotient 1. Dropping the phase exclusion breaks the imported quotient statement. |
| `c = 18`, `B = []` | Actual carry 1 but quotient 2. Extending the phase upper bound to 18 breaks the quotient statement. |
| `c = 2`, `B = [20]` | Actual carry and quotient are 2, while the threshold selector is 1. The true successor is `(4, [1])`; the incorrectly unbounded threshold formula gives `(4, [2])`, and the incorrectly unbounded quotient formula gives `(4, [0, 6])`. The coefficient hypothesis is essential to both new reconstruction endpoints. |

The original core review separately covers zero heads, untrimmed words, negative adic numerators, empty words, tail cutoffs, and failure of an insufficient cutoff. No additional input restriction is introduced in the wrapper, so those same cases remain covered.

## Independent strict extension compilation and exhaustive axiom audit

The reviewer executed the extension build using official Lean 4.19.0, commit `6caaee842e94`, with compiler SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Both new modules and the audit were invoked with

```text
--trust=0 -j1 -DElab.async=false
```

`CoordinateThreshold`, `CoordinateOnlyStreams`, and `ProjectAudit` each exited 0. Compiler version and prefix preflights also exited 0. The supported execution mode was `require_escalated`, as in the previously authorized successful core replay. The earlier ordinary-sandbox application-location failure remains recorded in the immutable preflight report; no source failure or automatic approval rejection is being inferred from it.

**This extension run freshly compiled two modules and imported seven attributed parent-built core objects. It was not a fresh nine-module build.** The imported core source files were checked byte-for-byte against the extended registry, the parent canonical receipt, and the reviewer's earlier independent fresh strict seven-module replay. The imported object hashes were recorded at import and checked after copying into a private temporary directory. Source copies, raw command logs, exit receipts, both prior core verification receipts, and all source/registry hashes remain in `strict-extension-01/`. The temporary compiled objects were removed after the run.

The parent core receipt retains its inherited verifier metadata `agent = "Agent #1"`; its actual executor was parent Agent #5. The separate earlier fresh core replay was executed by this reviewer and passed eight commands, all 25 core exports, and 133 theorem declarations. This review does not attribute that parent run to the reviewer or reuse it as if it were a newly independent core build.

The audit uses the unchanged canonical audit body, with the root import, fixed endpoint checks, and selected module list set from the extended registry. It visits every theorem declaration by module origin and computes the transitive axiom dependencies. It does not merely audit names in the Agent #5 namespace.

| Module origin | Audited theorem declarations |
|---|---:|
| OuterFinite | 10 |
| TARGET | 0 |
| ExteriorFactorizationProof | 59 |
| DigitDefinitions | 10 |
| AdicDigits | 23 |
| FractionDigits | 26 |
| CoordinateStreams | 5 |
| CoordinateThreshold | 36 |
| CoordinateOnlyStreams | 10 |
| **Total** | **179** |

The count includes private proof helpers and generated equation declarations. Agent #6's source contains 16 written public theorems, and the wrapper contains five. All 30 fixed Agent #5 exports appear in the audited declaration set. Every dependency set is contained in `{Classical.choice, Quot.sound, propext}`, and the union is exactly that set. There is no `sorry`, `admit`, `native_decide`, custom mathematical axiom, unsafe source declaration, or kernel-check bypass in the nine registered source modules.

As in the core audit, two generated unsafe implementation declarations are separately inventoried: the `highValue` fold specialization from `TARGET` and the `Outer` representation specialization from `OuterFinite`. Neither appears in any audited theorem's axiom dependency set. There is no new unsafe implementation declaration in either extension module.

Key runtime evidence hashes:

| Artifact | SHA-256 |
|---|---|
| Strict extension receipt | `2c3d5f699a330fa5048f36a9b0ab7444102e4d04191d55570ae82141beb744ad` |
| Exhaustive audit source | `9908933ff291f7a83729ff38ba71fa8420d51cb12ff7ed2b9dafc731a84c6be2` |
| Exhaustive audit raw log | `08f81614fcf50cde115a0232683024d1300e97fc7bafc12889cee7dd8848d5f9` |
| Earlier independent fresh core receipt | `b5c97cde66635b2901809b05846390283511925900e2d297557dbeb7a5d7cd9c` |

All files listed in the extension replay's `FILES.json` were independently rehashed after completion. The local HEAD recorded by the driver was `4b4edf976b2c7a9ba1dad80636c0e21c66350325`; the source hashes and copied bytes identify the actual new source reviewed. This extension receipt does not claim a clean published source commit. Parent Agent #5 is responsible for the separate final canonical replay on the exact published source.

## Remaining scope limits

This extension completes the coordinate-only selector needed by the claimed finite digit reconstruction. It does not prove a global real/adic bijection, a recurrence for successive coordinate pairs, an exterior cycle, an infinite safe orbit, all-time realization by finite integers, palindrome avoidance, or a conclusion about 196 or Lychrel numbers. The existing Agent #411 boundedness and Agent #216 integer/natural correspondence lanes remain untouched.

The reviewer's edits are confined to this new `review/coordinate-only-extension/` directory. No theorem source, initial core review artifact, Git state, remote branch, PR, or repository message was changed by the reviewer.
