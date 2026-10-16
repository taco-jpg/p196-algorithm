# Independent source semantic review: carry-free residue saturation

**Current review coverage:** the original Digits and Residues checkpoint below is now extended by the hash-specific Coordinates review at the end of this report. All three frozen modules pass semantic review. The final Saturation module and independent execution gates remain pending; no complete Theorem 3 acceptance is asserted.

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
