# Independent source semantic review: carry-free residue saturation

**Current decision: `PASS_SEMANTIC_REVIEW_COMPLETE_SCOPED_CLAIM`.** All four frozen new modules and all 22 selected registry endpoints pass independent nonauthor semantic review for the carry-free portion of the historical source's Theorem 3. There are no blocking semantic findings. The final extension below supersedes the earlier checkpoint coverage statements while preserving their evidence. This decision is tied to the exact source, contract, and registry hashes below; independent execution, full dependency-origin and axiom audits, and integration retain their separate acceptance gates.

## Initial decision and exact partial review set

**Decision: `PASS_SEMANTIC_REVIEW_PARTIAL_CHECKPOINT` for the two frozen sources below. No blocking semantic findings in this review set.** This is a review of the decimal construction and residue-parameter modules. It is not yet a complete review or proof-completion claim for Theorem 3: the literal coordinate bridge and final saturation modules remain outside this checkpoint.

Reviewer: Agent #14 / `spectral_semantics`, independently assigned and a nonauthor of every proof source under review. The reviewer read both complete files, all public theorem types and proof bodies, and the exact durable author contract. No Lean source was authored or modified, no candidate source was compiled by this reviewer, and no Git or remote mutation was performed.

| Frozen source read | SHA-256 |
| --- | --- |
| `/dev/shm/agent14-carryfree-d43e317f00d9/proofs/Agent14CarryfreeDigits.lean` | `ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9` |
| `/dev/shm/agent14-carryfree-residues-d43e317f00d9/Agent14CarryfreeResidues.lean` | `7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6` |
| `/dev/shm/agent14-carryfree-d43e317f00d9/proofs/contributions/agent-14/carryfree-residue-saturation-20261016/CONTRACT.md` | `ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb` |

The exact historical Theorem 3 source and its hashes are recorded in the companion `contract-review.md`. The source blob is `eac5b8f61385a615d9cc3e7796a4d698c66b716b`; its SHA-256 is `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`. This review uses the original definitions of decimal value, canonical representation, pair sums, computed carry, output, next step, and palindromicity previously inspected in the original decimal source, SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.

## Contract alignment

The durable author contract matches the previously reviewed mathematical obligations. The original positive-width and positive-leading-digit conditions are retained through `DecimalDigits.Canonical`. The final quantified targets require every odd width at least five and every even width at least two, without restricting zero residue classes. The integer interpretation of `Q(-1)/2` and the distinction between even-width alternating coordinate zero and the input's residue modulo 11 remain explicit.

The two modules reviewed here supply genuine supporting proofs for that contract. They do not define the desired saturation property to be true, add a residue-coverage premise, replace an arbitrary-width result with bounded testing, or assume a future palindrome in the construction.

## `Agent14CarryfreeDigits`: complete semantic assessment

### Literal digit functions and finite values

`threeDigits a b c L` has exactly the three source digits at `L-1`, `L-2`, and `L-3`, with zero elsewhere. `oneDigit a L` has exactly one leading digit. The separate `spike` definition denotes an ordinary indexed coefficient and is used only to express the source pair-polynomial formula.

The leading, second, third, prefix-zero, and units-zero lemmas have appropriate width hypotheses. The value and unweighted-sum lemmas prove the actual finite evaluations by reducing the zero prefix and expanding the remaining one or three positions. They retain all terms of the source input formulas and ordinary digit sum. In particular, the value lemma for the odd construction is not merely an equation postulated in a newly invented canonical predicate.

The generic value and sum lemmas work from width three for `threeDigits`, while its source-facing canonicality, nonpalindrome, and small-column results require `L>=5`. The one-digit value and sum lemmas work from width one, while the source-facing nonpalindrome family requires `L>=2`. These broader helpers do not accidentally assert the false nonpalindrome claim for a one-digit input.

### Bounds, canonicality, and initial nonpalindromicity

The three-digit bounds use `a<=9`, `b<=9`, and `c<=1`; the one-digit bounds use `a<=9`. Their canonicality theorems additionally require `a>=1`, giving an actual positive leading digit and the original exact evaluation equation.

The nonpalindrome proofs use the original numeric `palindrome_value_iff` theorem, then compare the units digit zero with the positive leading digit. They conclude nonpalindromicity of the represented **input integer**, not of the reciprocal pair-word. This is the required source distinction.

The nonpalindrome statements use `value` while the canonicality statements display the explicit positional input formula. The proved value equations connect these descriptions. The final assembly must make that connection for the same witnesses rather than treating the two forms as unrelated existences.

### Pair-polynomial coefficients and width five

`threeDigits_column_formula` proves the original `columnSum` equals the sum of six coefficient spikes:

- the two `a` spikes at 0 and `L-1`;
- the two `b` spikes at 1 and `L-2`;
- the two `c` spikes at 2 and `L-3`.

The right-hand side uses addition, so both contributions survive when the last two positions coincide. At `L=5` the center is exactly `c+c`, as required. The formula is proved without any coefficient bounds and is valid at each guarded index `i<L`.

`threeDigits_columns_bounded` independently proves that every actual column is at most 9. Its symbolic case analysis retains `L>=5`; it does not assume six distinct positions or silently exclude the central collision. The `c<=1` hypothesis handles the possible center `2c<=2`. At larger widths the relevant distinct-position cases also satisfy the bound.

The one-digit column formula has two distinct endpoint spikes under `L>=2`, and its bound includes `L=2`. Thus the family `a0` really has output coefficients `(a,a)` at the minimum width. No stronger width assumption has been introduced.

The repeated `omega`/`split` arguments are case analyses on symbolic index equalities. They prove the universal length and index statements; they are not an enumeration of widths or a computational certificate for a finite subset.

### Actual computed carries and next integer

`small_columns_actual_step` takes the original `Canonical n d L` and the actual bound `columnSum d L i<=9` for `i<L`. It instantiates `DecimalCarry.small_digit_sums_give_palindrome` with the original computed `carry` and `output`, the original pair-word symmetry theorem, the exact column equation, and the definitional initial carry zero.

Its all-carry result ranges over **every `i<=L`**, including the source's terminal carry. The terminal specialization then supplies the original `canonical_next_no_overflow` theorem and the original numeric `step_palindrome_iff_no_overflow` theorem. Rewriting the canonical value equation connects the result to `Lychrel196.step n` itself.

The conclusion is exactly the conjunction of all computed carries zero, canonical next output at the same width, and actual next integer palindromic. Neither terminal zero nor output palindromicity is inserted as an extra hypothesis. The original arithmetic bridge is therefore present, not replaced by an abstract transition statement.

## `Agent14CarryfreeResidues`: complete semantic assessment

### All 99 odd parameter pairs

`residue_parameters` quantifies over every `s<9` and `r<11`. It constructs parameters `1<=u<=10`, `b<=9`, and proves `(u+b)%9=s` and `(u+10*b)%11=r`.

The auxiliary target `(55*s+45*r)%99` has the requested two residues. Replacing its zero value with 99 retains both residues and supplies a positive integer between 1 and 99. Euclidean division of `x-1` by 10 gives the parameters and proves the exact identity `u+10*b=x`. Thus surjectivity is constructive and universal in both class parameters; it is not assumed or obtained from a finite experimental run.

The zero-target branch proves that both `s` and `r` are zero and preserves that case by choosing 99, not zero. At `(s,r)=(0,0)`, the construction gives `u=b=9`. Values with `u=10` are also retained, as required by the original family; they must not be excluded in the later `a=min(u,9), c=u-a` step.

The modulo-11 conclusion is deliberately written with the natural expression `u+10*b`. This is mathematically congruent to the signed expression `u-b` because their difference is `11*b`. It is an exact parameter interface, but **does not itself prove the signed `Q(-1)/2` bridge**. That bridge remains a required obligation of the later coordinate and assembly modules.

### All nine even parameters

`even_residue_parameters` explicitly uses `a=9` at `s=0` and `a=s` otherwise. Its conclusions preserve the nonzero leading-digit range `1<=a<=9` and the exact requested residue. No zero class is omitted.

### Exact power arithmetic

`ten_pow_mod99` has the correct parity-dependent remainder at every natural exponent. It retains the elementary proof of the original `AstraModular.ten_pow_mod99` fact, with explicit attribution explaining the separate `Std`-only helper. This supporting arithmetic is reused mathematics, not a new discovery or a second decimal core.

`odd_three_digit_mod99` preserves the literal positional input formula. Its width and oddness hypotheses justify the even/odd/even parities of `L-1`, `L-2`, and `L-3`. The conclusion gives exactly `(a+10*b+c)%99`, with no unnecessary coefficient bounds. Natural index subtraction is guarded by `L>=5`; no signed source quantity is encoded with natural subtraction here.

## Coverage and remaining assembly obligations

| Obligation | Status in this review set |
| --- | --- |
| Literal one-high-digit and three-high-digit witnesses | Proved by reviewed sources. |
| Original finite value and digit-word sum formulas | Proved by reviewed sources. |
| Canonical input and initial numeric nonpalindromicity | Proved for the stated parameter ranges. |
| Exact original pair-word coefficients, including `L=5` | Proved by reviewed sources. |
| Bound 9, all actual carries zero, next canonical width and numeric palindrome | Proved through the original arithmetic interfaces. |
| Every odd residue parameter pair and every even residue parameter | Proved constructively, including zero classes. |
| Source parameter split `a=min(u,9)`, `c=u-a` and its range/recombination facts | Still to be composed in the final construction. |
| Literal evaluations `Q(1)` and `Q(-1)` and exact half-coordinate interpretation | Not yet in this frozen review set. |
| Final every-width existence endpoints joining all conditions for the same witnesses | Not yet in this frozen review set. |
| Independent strict build, final module mapping, transitive axiom audit and integration | Separate verification gates; not certified by this source review. |

The source's quotient ideal and isomorphism, overflow saturation, carry charge `J`, and orbit or 196 conclusions remain outside this task. The two reviewed modules must not alone be described as completed Theorem 3 coverage before the pending coordinate and final existence obligations are checked.

## Proof policy and review limits

Full source inspection found no `sorry`, `admit`, new mathematical axiom, `native_decide`, unsafe oracle, or circular mathematical premise in these two modules. The proof bodies use ordinary recursion, original proved interfaces, arithmetic lemmas, symbolic case splits, `omega`, simplification, and kernel-checkable `decide` for elementary constants.

The coordinator reported successful strict author builds for the two frozen sources. This reviewer did not execute those builds or substitute source inspection for an independent clean build or transitive axiom audit. The final runtime evidence must verify the exact imported original decimal-source mapping and all relevant declarations. Any change to either reviewed source requires a new hash-specific review or an explicit review of the changed source.

## Extension: literal Coordinates module

**Decision: `PASS_SEMANTIC_REVIEW` for `Agent14CarryfreeCoordinates.lean` at SHA-256 `5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519`. No blocking semantic findings.**

The reviewer read the complete frozen file at `/dev/shm/agent14-carryfree-residues-d43e317f00d9/Agent14CarryfreeCoordinates.lean` and independently obtained this hash. The previously reviewed Digits and Residues source hashes were captured again and remain `ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9` and `7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6`, respectively. The earlier two-module checkpoint remains preserved above; this section records the additional coverage and supersedes only its statement that literal evaluation was still absent from the review set.

### Literal finite evaluation

`coefficientEval q L x` is defined by ordinary finite summation:

\[
\operatorname{coefficientEval}(q,0,x)=0,
\qquad
\operatorname{coefficientEval}(q,L+1,x)
=\operatorname{coefficientEval}(q,L,x)+(q_L:\mathbb Z)x^L.
\]

It is therefore exactly the source's finite polynomial evaluation `sum_(i<L) (q_i:Int)*x^i`, with least-significant-first coefficients. It is not a quotient projection, a normalized half-coordinate defined to meet the target, or an exterior-state alternating statistic. The argument `x` and all accumulated values are integers; indices and exponents are natural numbers.

`coefficientEval_congr` correctly restricts dependence to indices below the selected width. `coefficientEval_add` proves literal coefficient-wise additivity, using the natural-to-integer cast of an addition. `coefficientEval_spike` proves the exact monomial contribution when the position lies below `L` and zero otherwise. Its statement includes the empty-width case and does not assume that different spikes have distinct positions.

These facts justify evaluation of the source coefficient formulas already proved in Digits. In particular, splitting the sum of two coincident spikes remains valid: their contributions add instead of one coefficient overwriting the other.

### Evaluation at one and the ordinary digit sum

`eval_one` identifies the evaluation at one with the original `DecimalMass.wordSum`, cast into the integers. `columns_eval_one` then reuses the original `wordSum_columns` theorem to prove that evaluating actual pair columns at one gives twice the finite input digit-word sum.

`canonical_columns_eval_one` supplies the remaining numeric bridge. It uses the original canonical value equation and the canonical digit bounds to apply `DecimalMass.digitSum_value`, and proves

\[
Q(1)=2\,\operatorname{digitSum}(n).
\]

The canonical bound is essential to this numeric interpretation and is correctly supplied: the proof does not identify the ordinary decimal digit sum with the coefficient sum of an arbitrary unbounded positional word. No new definition of `digitSum`, `Canonical`, or `columnSum` is introduced.

### Odd alternating evaluation, including width five

`neg_one_pow_parity` proves the sign of `(-1:Int)^k` by ordinary induction for every natural exponent. `odd_columns_eval_neg_one` uses the original three-digit column formula together with finite evaluation congruence, additivity, and spike evaluation. Its `L>=5` and odd-width hypotheses justify the inclusion and signs of all six source monomials.

The exact conclusion is

\[
Q(-1)=2\bigl((a:\mathbb Z)-(b:\mathbb Z)+(c:\mathbb Z)\bigr).
\]

The subtraction is performed in `Int`. There is no truncated natural subtraction of the coefficient values. For example, `a=1,b=9,c=0,L=5` gives `Q(-1)=-16`, retaining the required negative half-coordinate `-8` for the later modular bridge.

At `L=5`, the two `c` spikes both occupy index 2. Additivity evaluates both, giving `2*c`, exactly as the original source requires. The proof does not assume six distinct indices. Its coefficient bounds are unnecessary for this algebraic identity and are correctly left to the separate physical-construction lemmas.

The later substitution `a+c=u` will turn the conclusion into `Q(-1)=2*((u:Int)-(b:Int))`. That substitution and the connection of the exact half to the input residue modulo 11 are not falsely claimed to have been proved in this module.

### Even alternating evaluation

`even_columns_eval_neg_one` evaluates the original two endpoint spikes under `L>=2` and even parity. The endpoint exponents have signs positive and negative, so it proves `Q(-1)=0` exactly, including `L=2`.

The statement concerns the actual pair polynomial and makes no assertion that the input integer is divisible by 11. It therefore preserves the essential difference between the source's even-width coordinate `r=0` and the initial integer's residue.

### Updated coverage and remaining gates

The literal coefficient-evaluation definition, its source-polynomial correspondence, `Q(1)=2*digitSum(n)`, the odd signed evaluation in terms of `a,b,c`, and the even exact zero evaluation now have reviewed source proofs. No repair to Coordinates is requested.

The final Saturation review must still check the source parameter split `a=min(u,9), c=u-a`, its bounds and identity `a+c=u`, exact division by two, the modulo-11 agreement of the signed half with the same constructed integer, and every-width existence endpoints that join all canonicality, nonpalindromicity, carry, width, output, and residue conditions for the same witnesses. In particular, the natural residue-parameter expression `u+10*b` must be related to the integer `u-b`, not silently treated as an identical expression.

All ten public declarations of Coordinates were read, including the finite-evaluation definition and nine supporting theorems. Source inspection found no forbidden proof placeholder, new mathematical axiom, compiler-trusted evaluation shortcut, or circular premise. The file's `#print axioms` commands are not execution evidence unless run; this reviewer did not compile the module or independently audit its transitive imported declarations. The source-level pass for all three reviewed hashes remains separate from the final strict build, dependency-origin verification, axiom audit, publication, and integration gates.

## Final extension: Saturation and the complete selected registry

**Decision: `PASS_SEMANTIC_REVIEW_COMPLETE_SCOPED_CLAIM`.** The complete frozen `Agent14CarryfreeSaturation.lean`, including its two definitions, thirteen theorem statements, and all proof bodies, has now been read. Together with the three modules reviewed above, it satisfies the durable contract for the carry-free portion of Theorem 3. The final every-width theorems and concrete controls have no blocking semantic defect. This is a source-semantic decision, not a report that this reviewer compiled the project or completed the independent runtime gates.

The exact contract remains SHA-256 `ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb`. Its scope and source correspondence were independently checked in `contract-review.md`, SHA-256 `205ccab182c0de6c05388786cae5a7c2f4e5f68f5c65a91bea1eae769f879b82`. The historical source remains SHA-256 `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`, blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`, byte-identical to the initial source pin recorded in that review. The final proof preserves the same ordinary decimal definitions and the same literal coefficient polynomial.

### Exact final source and manifest identity

All five project-module files in the final root `/dev/shm/agent14-carryfree-d43e317f00d9/proofs/` were independently rehashed. The hashes, Git blob identities recomputed directly from file bytes, and actual import declarations agree with the final registry and source-freeze manifest. The Residues and Coordinates copies in this root agree with the files reviewed earlier at their separate author root.

| Final project source | SHA-256 | Actual direct imports |
| --- | --- | --- |
| `LychrelDigitSums__0810ace083af80c5.lean` (module `LychrelDigitSums`) | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | `Std` |
| `Agent14CarryfreeDigits.lean` | `ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9` | `LychrelDigitSums` |
| `Agent14CarryfreeResidues.lean` | `7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6` | `Std` |
| `Agent14CarryfreeCoordinates.lean` | `5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519` | `Agent14CarryfreeDigits` |
| `Agent14CarryfreeSaturation.lean` | `2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a` | `Agent14CarryfreeResidues`, `Agent14CarryfreeDigits`, `Agent14CarryfreeCoordinates` |

| Project source, in the same order | Independently recomputed Git blob |
| --- | --- |
| Original decimal dependency | `8a865176625283648a8a20dd2411ed77670eb0a2` |
| Digits | `8b7f903a870c772d7c7e329f93931de3e4ab5fac` |
| Residues | `52526e5d8c400783bbf03220fd5937bb5153eb60` |
| Coordinates | `e06631541818a8ee8bf266193f35637a5a07bd21` |
| Saturation | `856d9a7b95e4b43501c0fb4b07955fc5279b8c26` |

The reviewed `SOURCE_FREEZE.json` has SHA-256 `5f8a120d796e8c765830f31e52939035708c95266ca1574c26cbafec4c7f3f32`. The reviewed `proofs/Agent14Carryfree.registry.json` has SHA-256 `0a8454b8dbcf7ece3c117a3bcb2f7d3cffbf562f7decdefafbb4e72fc842f53c` and Git blob `cf974d5d91fb0256cc99107e2a50f80e339d50e2`. These are the exact manifests covered by this decision. The registry's verifier path identifies `verify_project__214bf7673efe116b.py`; its repository copy was independently rehashed and agrees with the expected SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. This reviewer did not run that verifier.

The direct-import check establishes the five-module project dependency map. It does not replace the runtime check of actual module resolution, standard-library origin, or all declarations imported from `Std`. The full original decimal module was not newly subjected to a declaration-by-declaration semantic audit; its relevant definitions and bridge proofs identified above were inspected, and its full source bytes match the original dependency hash.

### Parameters and physical witnesses remain exact

`split_parameter` handles both sides of the source split. With `1 <= u <= 10`, it proves that `a = min u 9` lies in `1..9`, `c = u - min u 9` lies in `0..1`, and `a + c = u`. The subtraction used to construct `c` is legitimate natural subtraction with the required relation proved. The endpoint `u = 10` is retained as `a = 9, c = 1`; it is not silently truncated to an inadmissible leading decimal digit or removed from the residue coverage.

`oddSeed` and `oddDigits` instantiate the three literal high-position digits of the historical construction. `odd_seed_spec` joins their original canonical value equation, numeric nonpalindromicity, small pair columns, all computed zero carries, canonical next representation at the same width, palindromic next value, ordinary numeric digit sum `u + b`, and residue modulo 99. Its conclusions all concern this particular seed and this particular digit function. The proof uses the already reviewed physical lemmas and the original `digitSum_value` bridge; it does not replace ordinary decimal digit sum with a newly defined surrogate.

The projection of `odd_seed_spec` used in the modulo-11 bridge selects the actual modulo-99 statement. That statement gives the congruence of the seed with `u + 10*b`. Separately, the signed coordinate is `u - b` in the integers. The proof relates them modulo 11; it does not assert that the two expressions are equal.

`one_digit_seed_spec` supplies the same physical conclusions for `a*10^(L-1)` with `1 <= a <= 9` and `L >= 2`. The intermediate `even_carryfree_classes` does not need its parity hypothesis for these physical conclusions, since that family also works at odd widths. This unused intermediate hypothesis causes no semantic weakening. The final even source-coordinate theorem uses even parity where it is needed, in the proof that the alternating evaluation vanishes.

In both families, `Canonical` supplies positive width, bounded decimal digits, a positive leading digit, and the exact value equation. The existing `DecimalDigits.value_positive` therefore entails positivity of the witness even though a separate `0 < n` conjunct is unnecessary. Numeric nonpalindromicity of the initial value is explicit. The fact that the pair-column word is symmetric is not used as a substitute for the required assertion about the initial value.

### Exact halves and signed modulo-11 correspondence

The evaluation definition reviewed in Coordinates is the literal finite integer sum

\[
Q(x)=\sum_{i<L}(q_i:\mathbb Z)x^i,
\qquad q_i=\operatorname{columnSum}(d,L,i).
\]

`half_columns_eval_one` derives

\[
Q(1)/2=(\operatorname{digitSum}(n):\mathbb Z)
\]

from the original canonical representation and `canonical_columns_eval_one`. The theorem first divides an exactly even integer and then takes residues in the final endpoints. It does not divide a residue representative or interpret `/2` as an unsupported operation in a quotient ring.

For the odd seed, `odd_seed_eval_neg_one` substitutes the proved identity `a+c=u` into the literal alternating evaluation. `odd_seed_half_neg_one` then gives

\[
Q(-1)=2\bigl((u:\mathbb Z)-(b:\mathbb Z)\bigr),
\qquad Q(-1)/2=(u:\mathbb Z)-(b:\mathbb Z).
\]

The subtraction and the division here have type `Int`. Negative values are preserved. `odd_seed_half_mod_eleven` proves equality of the integer residue of this exact half with the natural residue `oddSeed u b L % 11`, cast to the integers. Its use of the seed's modulo-99 formula and integer arithmetic correctly implements `u+10*b` congruent to `u-b` modulo 11. There is no natural-number truncation of a negative half-coordinate.

### The two final source endpoints

`odd_source_coordinate_saturation` quantifies over every natural width `L` with `5 <= L` and `L % 2 = 1`, and over every `s < 9` and `r < 11`. It produces one pair of witnesses `n,d` satisfying all of the following together:

- The original `Canonical n d L`, explicit numeric nonpalindromicity of `n`, and original `FoldedDecimal.Admissible` for its actual pair columns.
- Every actual calculated carry equals zero for every index `i <= L`, including both the initial and terminal indices.
- The actual `Lychrel196.step n` is palindromic, and the original output digit function is a canonical representation of that same value at exactly the original width `L`.
- The ordinary numeric residues are `digitSum n % 9 = s` and `n % 11 = r`; every actual pair column below the width is at most nine.
- The literal evaluation obeys `Q(1) = 2*digitSum n`, the integer residue of `Q(1)/2` modulo nine is `s`, and the integer residue of `Q(-1)/2` modulo eleven is `r`.

The proof chooses the residue parameters once and then uses the corresponding `oddSeed` and `oddDigits` for every conjunct. In particular, the modular-coordinate conclusions and the physical reverse-addition conclusions are not established using unrelated witnesses. The use of the original `NormalizationBridge.canonical_admissible` is appropriate: it supplies the full existing admissibility predicate, including its symmetry, bounds, leading condition, and central parity requirement, from the same canonical input.

`even_source_coordinate_saturation` quantifies over every even `L >= 2` and every `s < 9`. It produces one physical witness pair with the same canonicality, nonpalindromicity, admissibility, all-carry, exact next-width, next-palindrome, and digit-sum conclusions. For this pair it proves both `Q(-1) = 0` exactly and `(Q(-1)/2) % 11 = 0`, alongside the evaluation-at-one and modulo-nine identities.

The even theorem does not claim `n % 11 = 0`. The source's even-width `r = 0` denotes the alternating pair-polynomial coordinate. For instance, the permitted width-two construction with leading digit one has input 10 and next value 11, while its pair polynomial has zero alternating evaluation. The final theorem preserves this distinction without adding an invalid restriction on the input residue.

These are genuine every-width existence statements: the source ranges give all 99 odd coordinate pairs at each allowed odd width and all nine even coordinate classes at each allowed even width. The proofs do not substitute a finite list of tested widths for either universal quantifier.

### Boundary and residue-zero controls

At the minimum odd width `L = 5`, the two `c` terms in the pair polynomial coincide at the central position. The reviewed Digits formula adds both contributions and the reviewed evaluation lemmas preserve their sum `2*c`. Since `c <= 1`, this central column remains within the carry-free bound. The source proof does not assume that all six displayed monomial positions are distinct. The positive leading digit and trailing zero also remain distinct positions at this width, supplying the nonpalindromic initial input.

At `L = 2`, the even family is the ordinary input `a0`, followed by `aa`. For the zero class modulo nine, the parameter selector uses `a = 9`, giving 90 followed by 99. It therefore supplies a positive canonical width-two witness for residue zero. Widths zero and one lie outside the final contract and are not accidentally used through saturated natural subtraction.

`negative_half_control` checks the actual final definitions at `u = 1, b = 9, L = 5`: the input is 19000, the exact integer half of the alternating evaluation is `-8`, and its residue modulo eleven is 3. This directly exercises the signed coordinate rather than merely a positive case.

`zero_classes_control` checks `u = 9, b = 9, L = 5`: the input is 99000, the actual next value is 99099, and both ordinary residues `digitSum n % 9` and `n % 11` are zero. The ordinary digit sum is supplied through the seed specification, not by a separate unconnected arithmetic model. These concrete controls corroborate the general construction and do not replace its universal proofs. Their small kernel `decide` uses are distinct from `native_decide`, which does not occur in the reviewed new sources.

### Exact registry endpoint correspondence

All 22 fully qualified names in the registry are unique and resolve, by source inspection, to the intended declarations in the exact files above. Every selected statement and its proof body were read. In the following table the common namespace `Agent14.Carryfree.` is omitted only for readability.

| Registry claim | Count | Selected endpoint suffixes |
| --- | --- | --- |
| `A14-CARRYFREE-RESIDUE-PARAMETERS` | 3 | `residue_parameters`; `even_residue_parameters`; `odd_three_digit_mod99` |
| `A14-CARRYFREE-ORIGINAL-DECIMAL-WITNESSES` | 8 | `threeDigits_canonical`; `threeDigits_not_palindrome`; `threeDigits_column_formula`; `small_columns_actual_step`; `odd_seed_spec`; `one_digit_seed_spec`; `odd_carryfree_classes`; `even_carryfree_classes` |
| `A14-CARRYFREE-LITERAL-SPECTRAL-COORDINATES` | 7 | `eval_one`; `canonical_columns_eval_one`; `odd_columns_eval_neg_one`; `even_columns_eval_neg_one`; `half_columns_eval_one`; `odd_seed_half_neg_one`; `odd_seed_half_mod_eleven` |
| `A14-CARRYFREE-SOURCE-THEOREM3-SATURATION` | 4 | `odd_source_coordinate_saturation`; `even_source_coordinate_saturation`; `negative_half_control`; `zero_classes_control` |

The four new source modules contain 55 explicit definition/theorem declarations: 26 in Digits, four in Residues, ten in Coordinates, and fifteen in Saturation. The 22 selected public endpoints therefore do not purport to enumerate every helper declaration, generated declaration, or imported declaration. The independent runtime audit must use its required full module/dependency audit scope, rather than treating the selected endpoint list alone as a complete axiom or safety inventory.

A static scan of the four new source files found no occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, or `extern`. Complete reading of their statements and proofs found no replacement of a source hypothesis by its desired conclusion, no newly introduced mathematical axiom, and no circular mathematical premise. These source observations do not claim a transitive runtime axiom audit of the original decimal dependency or `Std`.

The registry explicitly leaves `catalogue_complete` and `repository_wide_pass` false. Its selected claims and incomplete-global scope are consistent with the reviewed mathematical result. The reviewer has not independently verified repository-wide mutation metadata or remote integration status; this decision is attached to the exact bytes and declarations inspected locally.

### Author receipt provenance and independent execution boundary

The actual frozen target copied to `development/Agent14CarryfreeSaturation/attempt-004/source/Agent14CarryfreeSaturation.lean` was independently rehashed and equals SHA-256 `2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a`. Its only imports are Residues, Digits, and Coordinates as listed above. There is no self-import.

The inspected attempt-004 receipt records an author check with exit code zero, an empty-log hash, and a Lean command using `--trust=0 -j1 -DElab.async=false`. It also expressly describes cached author dependency reuse. Its broad `dependency_sources` and `dependency_objects` inventories include an earlier same-module source hash and same-module object. Consequently, those inventory arrays must not be read as the exact direct-import list for the final target or as evidence of a fresh independent build.

The coordinator explains that `develop.py` inventories the entire auxiliary object directory, including the earlier same-module object left by the physical-witness attempt. This explanation is consistent with the independently inspected final source bytes and imports. The historical receipt is preserved unchanged. Its inventory precision issue is a provenance limitation, not a semantic defect in the final source or registry. Only the separate clean independent compilations and their origin/audit evidence can discharge the corresponding execution gates; this reviewer has neither run them nor asserted their result here.

### Final scope and disposition

No source correction is requested. The exact four new source hashes, original decimal dependency identity, durable contract, and 22-endpoint registry receive a complete semantic pass for the selected carry-free construction in the historical Theorem 3.

The decision covers the canonical, positive, nonpalindromic ordinary inputs; all calculated zero carries through the terminal index; canonical palindromic actual next values at the same width; literal evaluations at one and minus one; their exact integer halves; and saturation of the specified residue classes at every permitted width. It preserves the original pair-polynomial definitions and the distinction between the even spectral coordinate and the input's modulo-eleven residue.

It does not certify the carry ideal, an ideal equality, a quotient isomorphism or cardinality, derivative coordinates, the overflow part of Theorem 3, any `U`/`S`/`J` construction, orbit reachability or persistence, or the 196 problem. It does not assert completion of the entire historical note, repository-wide Lean acceptance, remote publication verification, or integration. Those claims are outside this semantic review. The independent runtime and integration reviewers may append their separate decisions without changing the scope of this one.
