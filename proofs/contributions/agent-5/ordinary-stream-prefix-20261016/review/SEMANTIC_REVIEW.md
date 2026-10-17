# Independent review: one ordinary step and its raw coordinate-stream prefix

**Verdict: PASS for the six exact exported statements. No blocking semantic defect found.**

Reviewer: Agent #5's independent semantic reviewer, `/root/semantic_review`. The reviewer authored none of the Lean theorems. The parent supplied claim commit `e981de251ef29b24578dfe8bd79cdd2ba36c24f4` and the two frozen source hashes. This review is confined to the new ordinary-stream-prefix contribution's `review/` directory.

The new result identifies exactly the first `B.length + 1` coefficients of `paired (reverseAddDigits D)` using the previously proved coordinate streams. These are the mirrored-sum coefficients formed from the output digits; they are not the output digit prefix itself. The raw coefficients can exceed 9. A separate one-theorem wrapper retains the original `reverseAddDigits_correct` conclusions about decimal digits, a positive most-significant digit, and numerical value.

The shape hypothesis is explicit, the actual two-column minimum for each band is preserved, and no subsequent-step or all-time shape claim is inferred.

## Frozen source identity

| Module | SHA-256 | Git blob |
|---|---|---|
| `RawPrefixStreams` | `348bd1acf180a35b4cc60a805d417f7ee07a949fcf91761232f682aa5f5ddee6` | `b08d00b2968756de4b3fd4d7e19bbc00d130052e` |
| `OrdinaryStreamStep` | `ef186b6f9f631231cbd7fcb7d074f2ad6461783f25bb11672577eb3b29c38177` | `67af969daeabc5975f0c6d1feb60badf3f89dc1d` |

`semantic-source-inventory.json` records the exact six theorem contracts, all fifteen source hashes and Git blobs, and the complete import closure. The reviewer-generated registry snapshot has SHA-256 `c8359a77e9bb90027a8956961d430056ef027b5f6f1810fcc3e992c1f05da736`. This scoped review registry does not replace the parent's final canonical registry.

The nine existing coordinate modules retain their reviewed source bytes. The additional original Agent #6 arithmetic dependencies are:

| Module | SHA-256 | Main interface used |
|---|---|---|
| `ExteriorCore` | `4f4f31795a5198bffccf86ba1b7beed33da43e93063dfd0253266e8d1626d8e2` | Natural-word normalizer `norm` |
| `ExteriorBridge` | `16df0afa2e9dee53884e9c6c4239a72d9b449cff98a83e96207217f8a2b0cde1` | Coefficient bounds, nonneutral phases, `surrounded`, and exact normalization |
| `ExteriorProjection` | `ca40c03dc8a2769af74961a943069fc05e7d5a2fcfafe1cbdc0782f1e64ed43f` | `paired` and `surrounded_raw_exterior` |
| `ExteriorArithmetic` | `eaf374cf37d4dc13697d8fe6cf61fb62aaa98561a911ce01d552bebabb89c6fb` | `numeral`, `DecimalDigits`, `PositiveLast`, and `reverseAddDigits_correct` |

The current `ExteriorCore__a7a354ad633a456c.lean` used by the author and the separately inspected `ExteriorCore__d173de5907bec8eb.lean` have identical bytes. No substitution of a different normalizer or arithmetic function is involved.

## Exact raw-prefix statement

All words are lists of natural numbers in least-significant-position-first order. Define

\[
Q(D)=\operatorname{zipWith}_{+}(D,\operatorname{reverse}(D)),
\qquad T(D)=\operatorname{normalizedDigits}(Q(D)).
\]

These are exactly the existing `paired` and `reverseAddDigits` definitions. The latter performs actual carrying with initial carry zero and appends the final carry when it is nonzero.

For an exterior word `B`, middle `W`, phase `c`, and natural parameter `gap`, the required hypothesis is

\[
Q(D)=B\mathbin{++}c^{\mathrm{gap}+2}\mathbin{++}W
\mathbin{++}c^{\mathrm{gap}+2}\mathbin{++}\operatorname{reverse}(B).
\]

Here the superscript denotes a repeated list, not multiplication or a power of an integer. In particular, `gap = 0` still provides two copies of `c` on each side of `W`. The coefficient word has length

\[
2|B|+2(\mathrm{gap}+2)+|W|.
\]

Let

\[
n=|B|,\quad
a=\operatorname{zValue}(c,B)-c
 =9\operatorname{lowValue}(B)-c10^n,
\quad r=\operatorname{rhoNum}(c,B),
\quad \Delta=9\cdot10^n,
\quad \varepsilon=\mathbf 1_{\Delta\le r}.
\]

Under `nonneutralPhase c`, `Coefficients B`, `Coefficients W`, and the shape equality, the new coordinate-only conclusion is

\[
\operatorname{take}_{n+1} Q(T(D))=
\operatorname{zipWith}_{+}\left(
\operatorname{adicNumeratorDigits}(n+1,a),
\operatorname{fractionDigits}(n+1,r,\Delta10^{\varepsilon})
\right).
\]

The low numerator remains an integer, including when it is negative. The phase predicate is the unchanged eight-element set `2, 4, 6, 8, 10, 12, 14, 16`. The coefficient predicates mean that every entry is at most 18. The denominator and the incoming and outgoing carries are fixed by the existing definitions; no independent carry witness is selected.

This is equality of untrimmed lists. It does not apply `trim` or `stripSuffix`, and it does not replace the actual prefix by its exterior equivalence class. The q-parameter of both previously proved exterior digit identities is specialized to zero, giving exactly `n + 1` stream entries.

## Review of all six exports

All names below have prefix `Agent5.OrdinaryStreamPrefix.`

| Export | Exact interpretation |
|---|---|
| `normalize7_eq_norm6` | For every natural word and initial natural carry, the Agent #7 `normalize` result equals the original Agent #6 `norm` result, including both the list and final carry. The proof is structural induction over the two unchanged recursions. |
| `nonneutralPhase_nonneutral6` | The eight stream phases satisfy Agent #6's `0 < c ∧ c ≤ 17 ∧ c ≠ 9`. This correctly includes the positive-phase premise required by the ordinary projection. |
| `ordinary_raw_prefix_from_normalized_streams` | The exact raw-prefix equation above, first using the actual Agent #7 right-scan carry in the high denominator. It assumes only phase, coefficient, and shape hypotheses. |
| `ordinary_raw_prefix_from_streams` | The same equation with the previously proved coordinate threshold replacing that carry. |
| `ordinary_raw_prefix_from_streams_quotient` | The same equation with exponent `rhoNum c B / (9 * 10^B.length)`, using Agent #6's exact quotient identity. |
| `ordinary_reverse_add_from_streams` | The coordinate-threshold raw-prefix equation conjoined with all three original `reverseAddDigits_correct` conclusions, additionally assuming `DecimalDigits D` and `PositiveLast D`. |

The raw proof obtains the exact low and high digit-list identities at q = 0, unfolds the original `reverseAddDigits`, rewrites the given shape, and applies the original `surrounded_raw_exterior`. The two normalizers are connected by the new adapter, whose target is the correct Agent #6 definition. Agent #109's adjacent adapter has a different endpoint and is neither assumed nor silently reused.

The threshold and quotient variants are rewrites of that raw result. The arithmetic wrapper obtains the three conclusions directly from `reverseAddDigits_correct` and adds the imported raw-prefix equality. It does not reprove, redefine, or weaken the original value theorem. There is no dependency cycle or assumption of the desired prefix equality in a premise.

## Canonical numeral interpretation and boundary cases

`DecimalDigits D` says every entry is below 10. `PositiveLast D` says that `D = front ++ [last]` for some strictly positive `last`. Since the words are low-first, this is positivity of the most-significant digit. It rules out an empty input, zero, and a leading high zero. It allows a zero least-significant digit.

With both predicates, `D` is a canonical positive decimal numeral. Its reversed list can have leading high zeros when the original number ends in zero; evaluating that list by `numeral` correctly ignores those zeros. The existing numerical conclusion is precisely

\[
\operatorname{numeral}(T(D))=
\operatorname{numeral}(D)+\operatorname{numeral}(\operatorname{reverse}(D)).
\]

The new wrapper preserves that formal endpoint. It introduces no new theorem about a separately defined integer or natural-number orbit map; those correspondence lanes remain separate.

The raw theorem intentionally omits the two canonical-input predicates. Under its structural hypotheses, it remains an equality for the literal word functions. One must not identify an arbitrary such input list with its canonical integer expansion without the additional predicates. The following checked examples make that distinction concrete.

| Boundary control | Result |
|---|---|
| Too-short bands: `D = [1,9,1]`, `B = []`, `c = 2`, `W = [18]`, one band column | The paired input is `[2,18,2]`, representing the ordinary step from 191. Output digits are `[2,8,3]`; their raw paired prefix is `[5]`, whereas the stream sum is `[4]`. This word does not satisfy `surrounded` for any natural `gap`. The two-column minimum is substantive. |
| Too-long requested prefix: `D = [1,1,9,1,1]`, `B = []`, `c = 2`, `gap = 0`, `W = [18]` | Every actual theorem hypothesis, including canonical input predicates, holds. The required first coefficient is `[4]` on both sides. The next coefficient depends on the finite middle: actual two-entry prefix `[4,5]` differs from stream sum `[4,4]`. |
| Positive-last premise removed: `D = [0,1,1,1,1,0]`, `B = [0]`, `c = 2`, `gap = 0`, `W = []` | The shape and decimal-digit hypotheses hold, and the structural stream equality holds. The literal word computation has value 22220. Canonical numeric reverse-and-add for `numeral D = 11110` gives 12221. The high zero is the defect. |
| Decimal-digit premise removed: `D = [10,6,6,2]`, `B = []`, `c = 12`, `gap = 0`, `W = []` | The shape and positive-last hypotheses hold, and the structural stream equality holds. The literal output has value 13332, whereas canonical numeric reverse-and-add for `numeral D = 2670` gives 3432. |
| Zero least-significant digit: `D = [0,1,1,2]`, `B = []`, `c = 2`, `gap = 0`, `W = []` | This is a permitted canonical input representing 2110. The reverse contributes 112, and the output is 2222. Both the prefix equation and positivity conclusions hold. |
| Unbounded middle: `D = [1,1,1500,1,1]`, `W = [3000]`, `B = []`, `c = 2`, `gap = 0` | The shape holds, but the middle coefficient bound fails. The actual raw prefix is `[5]` and the stream sum is `[4]`. The raw theorem needs its carry-control premises. |
| Neutral phase: `D = [4,4,5,5]`, `B = []`, `c = 9`, `gap = 0`, `W = []` | Canonical input and shape hold, but the phase is excluded. The actual raw prefix `[18]` differs from the coordinate-threshold stream sum `[10]`. |

Empty `B` and empty `W` are nonvacuous. For every one of the eight phases, the canonical input `D = [c/2,c/2,c/2,c/2]` realizes `B = []`, `W = []`, `gap = 0`. For example, phase 12 realizes the step from 6666 to 13332 and yields raw prefix `[3]`. At phase 2 the raw prefix is `[4]`, even though stripping the successor phase 4 would remove it entirely. This illustrates why the new raw statement adds information beyond the earlier stripped exterior equality.

A nonempty `B` whose first coefficient is zero can occur in the raw structural theorem using a leading-zero input word. It cannot occur under the canonical wrapper's `PositiveLast` and shape hypotheses: the first paired coefficient is the sum of the input's least- and most-significant digits and is therefore positive. No positive-head premise is silently added; this restriction follows from the existing canonical interpretation. Untrimmed exterior words remain permitted.

The shape hypothesis also does not assert that every arbitrary middle word can be realized as `paired D`. For example, `paired D` is symmetric. The imported whole-word normalization identity works for arbitrary bounded middles, while the new ordinary statements retain the actual equality with `paired D` as a premise.

## Independent finite controls

`boundary_controls.py` and `boundary-controls.json` preserve the preceding examples and these successful finite checks:

| Check family | Cases |
|---|---:|
| Bounded coefficient words, all exterior words of lengths 0–2 with coefficients 0–18, all eight phases, three gap parameters, seven middle patterns | 64,008 |
| Canonical positive decimal input realizations within those cases, checked against ordinary integer reversal and addition | 51,984 |
| Longer word patterns, exterior lengths 7 and 40 | 384 |
| Included structural zero-head cases | 3,360 |
| Included empty-exterior cases | 168 |
| Included empty-middle cases | 9,144 |
| Included negative adic-numerator cases | 32,592 |

These are exact-integer computations. The general coefficient-word family includes some words that are not symmetric and hence are not asserted to be paired canonical inputs. The separately counted canonical family constructs valid decimal words and verifies the shape explicitly. The computations are supplemental boundary evidence; the universal theorem evidence is the Lean compilation and audit below.

## Independent two-module compilation and axiom audit

The reviewer freshly compiled only `RawPrefixStreams` and `OrdinaryStreamStep`. Thirteen dependency objects were inherited from the source-matched author stage: nine published coordinate modules and four arithmetic dependencies previously compiled by the runtime sibling. The reviewer checked all thirteen source/object pairs against their source hashes and the recorded provenance, verified the nine preexisting object hashes, rehashed the four arithmetic build logs, and recorded all thirteen object hashes at import. No inherited object is presented as independently rebuilt in this run.

The official compiler was Lean 4.19.0, commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Both modules and the exhaustive audit ran with `--trust=0 -j1 -DElab.async=false`; all three commands exited 0. Version and runtime-prefix preflights also exited 0. The authorized supported tool execution mode was `require_escalated`.

The audit checks all six fixed new exports and enumerates theorem declarations by all fifteen selected module origins, including generated declarations. It found **267 theorem declarations**, every transitive axiom set contained in `{Classical.choice, Quot.sound, propext}`. The breakdown is 179 declarations from the existing coordinate context, 79 from the four arithmetic modules, eight from `RawPrefixStreams`, and one from `OrdinaryStreamStep`.

The source scan found no `sorry`, `admit`, `native_decide`, custom axiom, unsafe source declaration, or kernel-check bypass in the fifteen registered modules. Three generated unsafe implementation declarations are separately inventoried: the existing `highValue` fold specialization, the Agent #7 `Outer` representation specialization, and the Agent #6 `Exterior` representation specialization. None appears in any mathematical theorem's axiom dependencies.

| Evidence artifact | SHA-256 |
|---|---|
| `strict-replay-01/verification.json` | `3c08d98fb198270d4a347f34818ab3b2454060eb2102750a3851a5663c56466c` |
| `strict-replay-01/logs/ProjectAudit.log` | `e88d8b7a819c3528fc69862f5cf385ac189112cb7e49730236bb8f438b3e8549` |
| Exhaustive audit source | `9383d1c8429c90b25c78e9bfa1f2dac3386defc6b274389ec89c9cc26c2e638c` |

All 29 files listed in the replay's `FILES.json` were rehashed after completion. Exact source copies, the scoped registry, baseline provenance, raw logs, commands, and exit codes are retained. The private temporary compiled objects were removed after completion, so no author stage or compiled cache is required to interpret the saved evidence.

The local HEAD recorded by this review was `fff2ca0a7ecbb2ee50eccf4cdc80f07b274e50e2`. The new module hashes and source copies identify what was reviewed; this receipt does not assert that the new sources already belonged to a clean published commit. Parent Agent #5 owns the separate fresh full fifteen-module canonical replay and publication.

The shared disk reached zero free bytes after the successful compilation. All completed receipts and their inventories were intact, and further writes were held until the parent freed reproducible cache space. There was no failed or repeated Lean build in this review, and the storage event is not classified as a theorem or compiler failure.

## Proved and unproved scope

The contribution proves a one-step structural raw-prefix identity under the existing surrounded-word hypothesis and bundles it with the original canonical numeral conclusions under explicit input predicates. It does not prove that the output has another surrounded shape, that a longer prefix is independent of the middle, that any gap persists, or that these hypotheses remain available for a second or subsequent step. It proves no infinite safe orbit, all-time finite integer realization, palindrome avoidance, or conclusion about 196 or Lychrel numbers.

Agent #4, #16, #216, and #110 ownership boundaries remain untouched. The reviewer changed only new review artifacts and performed no Git or remote write.
