# Agent 10: nine complete carry observations are necessary and sufficient

For ordinary decimal reverse-and-add iteration, **nine is the exact uniform observation threshold** for determining every active initial pair coefficient, and also for determining the next integer, when the initial width is shared. Eight observations are insufficient. The complete sixteen-module source closure is Lean checked and independently validated.

The two main endpoints in [Agent10NineCarrySharp.lean](Agent10NineCarrySharp.lean) are:

```lean
uniform_pair_reconstruction_iff (K : Nat) :
  UniformPairReconstruction K ↔ 9 ≤ K

uniform_next_integer_reconstruction_iff (K : Nat) :
  UniformNextIntegerReconstruction K ↔ 9 ≤ K
```

The result combines the unchanged repository nine-word upper bound with a new direct certificate of an eight-word collision. The observation threshold concerns unrestricted continued iteration. The explicit witness first reaches a palindrome at time four; that fact is itself kernel certified.

## Exact domain and observations

Digits are indexed from the least significant position. At width `L`, a pair coefficient is `q i = d i + d (L-1-i)`. An admissible pair word has positive width, coefficients at most eighteen, reflection symmetry, positive exterior coefficient, and the appropriate even central coefficient. Canonical ordinary inputs use their actual decimal width and have a nonzero leading digit.

The incoming carry starts at zero and satisfies

\[
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor.
\]

A **complete carry word** includes every index from zero through the current width, including the terminal overflow carry. At time `t`, the current width and coefficients are those of the unchanged `iterPairs` recursion. The numeric representation theorem connects this recursion to ordinary integer reverse-and-add.

`UniformPairReconstruction K` quantifies over every two admissible words `q,r` at one common initial width `L`. Equality of their complete carry words at every `t < K` must imply `q i = r i` for every active index `i < L`. It does not constrain function values outside that finite width.

`UniformNextIntegerReconstruction K` quantifies over canonical representations of two ordinary integers at one common initial width. The same observation hypothesis must imply `Lychrel196.step n = Lychrel196.step m`. It does not assert equality of the initial integers or of their individual digit splittings.

Thus nine observations mean the words at times `0,...,8`; the certificate below matches the eight words at `0,...,7` and separates at time eight. Observations and transitions have different endpoint conventions.

## The certified eight-word collision

[Agent10EightCarryCounterexample.lean](Agent10EightCarryCounterexample.lean) proves the following exact facts:

| Quantity | Left input | Right input |
| --- | --- | --- |
| Initial integer | `90000000560706169` | `90000000806235169` |
| Canonical initial width | 17 | 17 |
| Initial active pair coefficient at index 3 | 6 | 5 |
| Next integer | `186160707060706178` | `186153261606235178` |
| Carry at time 8, index 4 | 1 | 0 |
| First palindrome time | 4 | 4 |
| First palindrome value | `16999899899899899961` | `16989989999998998961` |

The initial symmetric pair words are:

```text
q = [18,6,1,6,0,7,0,6,10,6,0,7,0,6,1,6,18]
r = [18,6,1,5,3,2,6,0,16,0,6,2,3,5,1,6,18]
```

Their difference is the coefficient-six smoothing witness with three zeros added at each end:

```text
[0,0,0,1,-3,5,-6,6,-6,6,-6,5,-3,1,0,0,0]
```

The source proves `eight_complete_carries`, with precisely the quantifiers `∀ t, t < 8 → ∀ i, i ≤ currentWidth → ...`. The current widths at times zero through eight are `[17,18,19,20,20,20,20,21,21]`. Independent ordinary decimal replay compared all **163 carry positions** in the eight matching observations, as well as all nine retained integer trajectory rows.

The first differing initial coefficient is active: index three is below seventeen. The next integers differ as literal natural numbers. The ninth observation has an in-range mismatch at index four. Consequently, the example defeats both proposed uniform reconstruction tasks at eight observations.

The source also proves that neither input is a palindrome at any time below four and that both are palindromes at time four. This prevents a stronger, unsupported interpretation of the counterexample: it does not establish an eight-word failure among trajectories required to remain nonpalindromic throughout the observation window.

## Why the certificate is a proof of an actual trajectory

The module records nine finite pair rows for each input. Finite kernel decisions verify the initial rows against the canonical digit functions, every adjacent row against the original `nextWidth` and `nextColumns`, every width bound, and every carry in the eight matching observations. The maximum width is twenty-one, and `Fin 22` includes its terminal carry index.

An induction uses the existing finite-prefix congruence theorem to transport these row certificates to the original `iterPairs` recursion. The existing canonical-representation bridge supplies ordinary numeric orbit semantics. The proof therefore concerns the repository's original arithmetic operations, rather than an unconstrained prefix automaton or a separate simulator.

All six finite certificates in the Eight module are axiom-free. Its complete module-origin audit covers forty-eight theorem declarations, including generated helpers; its sixteen public endpoints are checked individually. The module's theorem axiom union is `{propext, Quot.sound}`.

The C++ search and its computational prefix filter do not occur in this proof's dependency chain. Once the explicit integers and rows are supplied, their validity is checked directly by Lean.

## From one counterexample to the exact threshold

The upper direction directly applies the preserved [DifferenceObservability](DifferenceObservability__302efefb5b9eab49.lean) theorems `nine_carry_words_determine_pair_sums` and `nine_carry_words_determine_next_integer`. If `9 ≤ K`, the first nine observations are available by restricting the length-`K` history.

For the lower direction, any natural `K < 9` satisfies `K ≤ 8`. The concrete eight-word history can therefore be restricted to its first `K` observations. Uniform reconstruction at `K` would identify either the unequal active coefficient or the unequal next integers, a contradiction. This argument includes `K = 0` without an extra positive-count assumption.

The pair-word lower bound derives both admissibility hypotheses from the certified width-seventeen canonical inputs. The numerical lower bound uses those same canonical representations directly. The final endpoint `nine_is_exact_uniform_threshold` combines both equivalences.

The new Sharp module adds nine public theorem endpoints and twelve theorem declarations when generated helpers are included. Its direct first compilation passed with `--trust=0`; the final fresh canonical closure checks it again together with all dependencies and predecessor modules.

## Earlier results retained in the same closure

| Result | Checked source |
| --- | --- |
| Every admissible width has at least three nonoverflow steps among its first seven transitions | [Agent10SevenStepCount.lean](Agent10SevenStepCount.lean) |
| Eight complete observations recover all pair coefficients when the initial step has no overflow, or under the stated coefficient-difference bound | [Agent10EightCarry.lean](Agent10EightCarry.lean) |
| Eight complete observations recover the first two active pair coefficients at every admissible width | [Agent10ThreeColumnCarry.lean](Agent10ThreeColumnCarry.lean) |
| Four-smoothing rigidity is sharp at coefficient bound five; a symmetric finite witness defeats bound six | [Agent10SmoothingBoundary.lean](Agent10SmoothingBoundary.lean), [Agent10SmoothingBridge.lean](Agent10SmoothingBridge.lean) |
| Explicit ordinary integer collisions for six and seven observations | [Agent10SixCarryCounterexample.lean](Agent10SixCarryCounterexample.lean), [Agent10SevenCarryCounterexample.lean](Agent10SevenCarryCounterexample.lean) |

The Eight witness begins with an overflow and has equal first two pair coefficients, so it is consistent with both positive eight-observation results. Earlier checkpoint reports and scoped registries remain preserved. Their former open question about unrestricted full eight-word reconstruction is resolved negatively by the new certificate.

## Discovery computation and its limits

The final exact scan completed **21,961,212** width-seventeen candidates selected by the five-coordinate necessary-prefix computation and found **32** eight-word matches. Surviving candidates after the filter and zero through eight actual complete observations were:

```text
21961212, 1864832, 696818, 515311, 282685,
156113, 41090, 1094, 32
```

The five-coordinate filter examined all 1,871,424 valid initial prefixes and retained 1,326. Each retained prefix has 16,562 admissible symmetric completions. The CSV's stored sample bit string was never used to constrain the actual full-word trajectories.

The four- and five-coordinate projection inclusions are computationally checked, not formalized in Lean. Negative search conclusions remain limited to their specified candidate sets and assumptions. The positive witness used by the theorem is independent of filter completeness and of the exhaustive search count. Complete sources, inputs, outputs, commands, and hashes are preserved in the [calculation delivery](../calculation/agent10-nine-carry-sharp-20261016/README.md).

## Verification and provenance

| Final canonical gate item | Value |
| --- | --- |
| Tested source commit | `f156ea95f4f64609da218632820f71378c815411` |
| Scoped registry | `Agent10NineCarrySharp.registry.json` |
| Registry SHA-256 | `01cac4b7bf8094d50a368e3798fefa548b85b911c3bab58a788e8d3f9ee5ab72` |
| Fresh source-module compilations | 16 |
| Successful Lean commands, including exhaustive audit | 17 |
| Audited theorem declarations, including inherited/private/generated declarations | 1,345 |
| Registered endpoint types and exhaustive axiom records | 122 |
| Additional matching explicit source axiom prints | 120 |
| Canonical report SHA-256 | `a2c608c48f132f355e89b1889f22b6230342cbc20c6b03893ac07cb7dbb9f5d2` |
| Independent validation receipt SHA-256 | `338d7bfad379503ada5d1630f502445cae06340781d46b20bd5acf324c5132ce` |

The unchanged canonical verifier compiled every selected module in a new empty output directory. Its exhaustive audit covers all theorem declarations whose origins are in the sixteen-module closure. The allowed theorem axiom union is exactly `{Classical.choice, Quot.sound, propext}`. No custom theorem axioms or forbidden proof shortcuts occur in the audited sources.

The thirteen unsafe implementation-specialization declarations inherited from the original foundation are separately inventoried and are absent from every theorem axiom dependency. The two endpoints without explicit source prints, `observedBit3_value` and `state3_valid`, are fully covered by the exhaustive audit. The count 1,345 includes inherited theorems and generated declarations; it is not a count of newly authored results.

Agent 10's parent executed the final canonical gate. The formalization specialist independently validated all thirty-five manifest entries, source/commit/build byte identities, successful command logs, complete endpoint types, and exhaustive axiom records. Non-author specialists separately reviewed the Seven and Eight certificates and the parent-authored Sharp composition. These are internal reviews, not external GitHub approval or main integration.

The original checker retains its historical `Agent #1` field. Correct executor and validator identities are recorded separately. Earlier failed development attempts, corrected attribution receipts, prior successful source revisions, and complete checkpoint archives remain retained.

## Reproduce

Apply the supplied final additive patch to its pinned original baseline, or use the complete extracted source snapshot. With the pinned official Lean 4.19.0 runtime, run from the repository root and choose a new output directory:

```bash
python -B proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent10NineCarrySharp.registry.json \
  --project agent10-nine-carry-sharp \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-agent10-nine-carry-build
```

The final patch is additive and preserves the four original dependency files, the original verifier, every earlier Agent 10 proof, and all preceding scoped registries. The evidence archive also supplies the complete prior thirteen-module checkpoint and the later certificate, review, and execution records.

The remaining mathematical boundary is distinct from this completed theorem: the package establishes no threshold for an observation window containing no palindrome, no infinite palindrome avoidance, and no resolution of the 196 conjecture.
