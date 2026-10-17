# Independent semantic review of the exact coordinate digit streams

**Reviewer:** Agent #5's independent semantic reviewer. **Date:** 2026-10-16.

**Semantic verdict: PASS.** All 25 exported theorem statements in the four final modules, including both assembled successor endpoints, have passed independent mathematical review. No blocking defect, circular premise, unjustified truncation, or missing boundary hypothesis was found within the stated domain. This verdict is for the exact source identities below. At this review checkpoint, this reviewer has executed exact finite controls, not a Lean compiler replay; compiler verification remains separately attributed to its actual executor and receipt.

This is a review of the claimed digit-stream task at coordination commit `f944d0af99dad4218ce322af9bae70c926ff5977`, as supplied by the parent. The task is the explicit finite digit formula for the existing exterior map. No specialist's proof file was modified. All artifacts produced for this task are in this contribution's `review/` directory.

## Final source identities

| Module | Theorem declarations | SHA-256 |
|---|---:|---|
| `DigitDefinitions.lean` | 2 | `4bdedd6d992a3207645d5dd21478a66c2e1c2465f75111b86b294caee903739a` |
| `AdicDigits.lean` | 7 | `f8b8b5ded9e85cf8840a329950fe95f1f6e2e3bb2ad8c8e3e1f1513080e09a6b` |
| `FractionDigits.lean` | 13 | `d6232d1f20221b1a2f09f3670f6078d2fe0c6558a439c9c0ac25c4e04e119732` |
| `CoordinateStreams.lean` | 3 | `c1409584ac12282f5b3097284a88194687b335f14d5864f258afa40f0d920a20` |

The two new stream definitions and all theorem declarations are inventoried in `semantic-source-inventory.json`, together with the registry and exact three-module dependency identities. The executable controls were run while proof assembly was in progress; their recorded snapshot hashes identify that stage. The final source inventory above supersedes those stage-specific source identities for this semantic verdict. The stream recursions and mathematical formulas tested by the controls are unchanged.

## Exact intended statement

Use the existing `P196.Agent7.Finite` exterior map and the existing `Agent115.ExteriorFactorization` coordinates. Let the phase `c` belong to `{2,4,6,8,10,12,14,16}` and let every natural-number coefficient of the finite word `B` be at most 18. No positive-head, nonempty-word, or canonical-trimming hypothesis is needed for the proposed formula.

Write `n = B.length`, `k = if 10 ≤ c then 1 else 0`, and `t = c - 9*k`. Let

\[
L=\operatorname{normalize}(B,0),\qquad
R=\operatorname{normalize}(\operatorname{reverse}(B),k),\qquad g=R.2.
\]

The exact coordinate numerator and high rational data are

\[
a=Z(c,B)-c=9\operatorname{lowValue}(B)-c10^n,\quad
r=\operatorname{rhoNum}(c,B)=9\operatorname{highValue}(B)+c,\quad
D=9\cdot10^n.
\]

For every `q : Nat`, set `N = n+1+q`. The two literal finite streams should satisfy

\[
\operatorname{adicNumeratorDigits}(N,a)
=L.1\mathbin{++}[c+L.2-10k]\mathbin{++}[t]^q,
\]

\[
\operatorname{fractionDigits}(N,r,D10^g)
=
\begin{cases}
\operatorname{reverse}(R.1)\mathbin{++}[t]\mathbin{++}[t]^q,&g=0,\\
[1]\mathbin{++}\operatorname{reverse}(R.1)\mathbin{++}[t]^q,&g=1.
\end{cases}
\]

Pairwise addition and removal of the final copies of `2*t` then recover precisely the `B` field of `outerNext (c,B)`. The successor phase is `2*t`. The first `n+1` positions contain every boundary contribution; extra positions contribute only copies of that same successor phase.

## Low-stream review

The recursion chooses `d = ((-a) % 10).toNat` and replaces `a` with `(a-9*d)/10`. The remainder is already in `[0,9]` before the conversion to a natural number. This is essential: the source does not truncate the possibly negative numerator itself. Since `9 ≡ -1 (mod 10)`, the chosen digit makes `a-9*d` exactly divisible by ten. Thus the recursion encodes the low decimal digits of the quotient by nine in the adic direction, including negative numerators.

The exact one-column statement is correct for every `x : Nat` and `z : Int`: a numerator `9*x+10*z` emits `x%10` and leaves `9*(x/10)+z`. The intermediate `adicNumeratorDigits_normalize` theorem correctly needs no coefficient bound and allows an arbitrary signed phase numerator `c : Int` and arbitrary natural incoming carry `e`. Its residual numerator is `9*finalCarry-c`, not a guessed phase tail.

At a permitted phase and an incoming carry at most one, the next digit is precisely the boundary digit `c+e-10*k`; the next numerator is `-t`. The constant-numerator theorem correctly shows that `-t` emits only copies of `t` when `t<10`. The actual phase domain has `1≤t≤8`, so the specialization is within that range.

The exterior theorem uses `zValue c B - c`, which is the numerator of the original note's `β`, not `zValue` alone. It retains the boundary digit before adding the constant tail. The generic digit-bound theorem and prefix-consistency theorem are correct for every signed starting numerator. No overflow-existence, orbit, moment, or arithmetic-realization assumption is used.

## High-stream review

The `fractionDigits` recursion is ordinary long division. It is a total natural-number function, but unrestricted arguments do not automatically represent a proper decimal fraction: if `r≥D`, the first output may be at least ten; at `D=0`, division is only Lean's totalized arithmetic. The proper-fraction digit-bound theorem explicitly assumes `r<D`, which also gives `D>0`.

The scalar-invariance theorem correctly requires a positive scaling factor. Its algebraic equality remains meaningful even for a zero denominator, without claiming that such inputs represent a rational number. The repeating-tail theorem correctly requires `t<9`. The value nine must be excluded on the real side: `fractionDigits 1 9 9 = [10]`, rather than `[9]`. This is consistent with the low adic theorem allowing a constant digit nine; the two number systems have different boundary behavior.

Let `A = reverse(R.1)`. Exact normalization conservation gives

\[
\operatorname{highValue}(A)+10^n g
=\operatorname{highValue}(B)+k.
\]

The phase decomposition is `c=9*k+t`, with `t<9`, and bounded coefficients give `g≤1`. If `g=0`, this yields `r=9*highValue(A)+t`. The high-value expansion lemma therefore returns `A` followed by the repeating digit `t`; choosing one additional tail digit supplies the boundary `[t]` in the exterior formula. If `g=1`, it yields `r=9*highValue(1::A)+t`, and the denominator is exactly `9*10^(n+1)`. These are precisely the two alignments used by the original exterior map.

The high exterior theorem scales by the actual normalization carry, using denominator `(9*10^n)*10^g`. It does not replace that carry by an assumed threshold predicate. Its arbitrary-prefix digit-bound corollary is noncircular: it uses the already established complete-prefix formula and the independent prefix-consistency theorem. The main formula itself was proved through normalization conservation and long division, not through that corollary.

## Constant-tail and cutoff review

The helper `strip_zip_append_replicate` is correct. Equal-length base lists ensure their appended tails align with each other in `zipWith`; every appended sum is `t+t=2*t` and disappears under `stripSuffix (2*t)`. The equality-of-length premise is substantive. Without it, `a=[0]`, `b=[]`, `t=1`, `q=1` gives left side `[1]` and right side `[]`.

The safe cutoff is `n+1`, with arbitrary additional `q≥0`; it is not uniformly `n`. For `c=2`, `B=[10]`, the true successor is `(4,[1,3])`, while using only one digit from each stream yields `(4,[1])`. Empty words also require the one boundary position in the high-phase case.

The final `outerNext_from_streams` theorem is an equality of complete `Outer` structures, not merely a relation on observations. Both streams have length `n+1+q`; the proof derives the equal lengths of the two original scan lists and rewrites the already established low and high stream formulas. Removing the aligned constant tails then leaves exactly the existing `outerNext` definition. The corrected length proof splits on the actual outgoing high carry; it introduces no extra premise or modified definition.

The final `outerNext_from_streams_of_cutoff` theorem replaces `n+1+q` with any `cut : Nat` satisfying `n+1≤cut`. Its witness `q=cut-(n+1)` is justified by this explicit inequality, so natural-number subtraction does not silently shorten the requested prefix. Both aggregate endpoints retain exactly the nonneutral-phase and coefficient-bound premises. They do not require an overflow, positive head, canonicality, or a nonempty word.

## Boundary controls and concrete failures outside the scope

`boundary_controls.py` implements the original natural-number exterior map separately from the two stream recursions, using exact integer arithmetic and exact rational display values. Its assertions check each individual scan formula, digit bounds, the adic congruence, high overflow scaling, and the trimmed successor for three different tail lengths. These are finite regression checks, not substitutes for universal proofs.

The run passed on 57,920 exhaustive states: all eight permitted phases, every word of widths zero through three, and every coefficient in `[0,18]`. That includes 29,020 negative adic numerators, all eight empty-word phases, 3,048 zero-head states, and 3,048 words ending in their phase. Eighty additional structured words of widths seven and forty exercise long carry and phase-tail patterns. There were 174,000 complete stream-prefix checks at tail lengths `q=0,1,4`, plus 4,788 instances of the intermediate adic normalization theorem with unrestricted coefficient/carry examples and signed phase numerators.

| Control | Exact interpretation |
|---|---|
| `B=[]`, `c=12` | `a=-12`; low stream `2,3,3,…`; `g=1`; normalized high value `12/90`, with stream `1,3,3,…`; sums trim at six to `[3]`, exactly the exterior successor. |
| Empty high phase without scaling | Expanding `12/9` directly starts with output 13, so it is not a decimal digit stream and does not give the exterior alignment. |
| `c=2`, `B=[10]`, cutoff `N=n` | Loses the final coefficient three; the full `n+1` prefix is required. |
| Neutral phase `c=9`, `B=[0]` | The real tail would be digit nine, whose alternative terminating expansion changes the canonical long-division digits. The proposed formula fails, as expected outside the stated phase domain. |
| Out-of-range coefficient `c=10`, `B=[19]` | The high scan has carry two. The original map's nonzero branch inserts one, while a denominator scaled by `10^2` gives a different stream. The coefficient restriction cannot simply be dropped. |
| Unequal base lengths in the stripping helper | Appended tails can align with old digits instead of one another, so the helper's length hypothesis is required. |

The exact traces and counts are retained in `boundary-controls.json`. No counterexample was found inside the specified domain.

## Relationship to the original written note and remaining scope

The inspected original note is `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-115/exterior-factorization/NOTE.md`, SHA-256 `e1a63fa17f325aba0a055ba761e55866583a2946000f54836282fc65e6124954`. Its finite digit formula uses the same `β=(Z-c)/9`, high coordinate `ρ`, overflow scaling, boundary position, and constant tail. The new source extends that written formula beyond canonical words by using only coefficient bounds and the inherited nonneutral-phase predicate. The control suite explicitly includes zero heads and untrimmed words to check that extension.

The formal deliverable is an equality of executable finite prefixes and a finite list expression for the existing abstract successor. It does not construct a topological adic-number library, a global bijection between all real and adic digit expansions, or a new autonomous coordinate-update theorem. The original note's broader informal `Φ`/`Ψ` discussion and cycle claims are not established by these finite stream identities.

No all-time concrete integer realization, gap-continuation guarantee, palindrome-avoidance theorem, exterior no-return theorem, or conclusion about 196 follows. Adjacent Agent #6 scope remains separate. The independent review and finite controls record mathematical confidence; any compiler/axiom status must be attributed to the actual executor and exact final source receipt.
