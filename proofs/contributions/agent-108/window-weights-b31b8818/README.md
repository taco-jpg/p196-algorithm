# Agent #108: positive finite-window weights cannot bound safe incoming mass

Task: `agent108-buffered-window-weights-b31b8818`.
Contribution branch: `research/agent-108/window-weights-b31b8818-20261016`.
Pull request: [#98](https://github.com/taco-jpg/p196-algorithm/pull/98).

The final theorem is
[`Agent108.WindowWeights.not_exists_uniform_window_bound`](../../../Agent108WindowIncoming.lean).
For every fixed positive window length, every strictly positive potential
on legal coefficient windows, every positive even-width normalization,
and every positive odd-width extension, there is **no finite real uniform
multiplier** for the original full safe incoming operator.

The final Incoming source has passed author compilation and a distinct
agent's fresh ten-module rebuild and transitive axiom audit. The complete
portable repository build, including rebuilding the seven original
dependencies, is the final packaging gate; its command and actual outcome
are recorded separately in `REPRODUCE.md` and the final build evidence.
Main integration is a separate serialized action.

## Exact model and conclusion

The state space, `SafeState`, `MapsTo`, `safeFiber`, and `incoming` are
the unchanged Agent13ProductWeights definitions from original commit
`12a32789056f5eec8247166564ac2ef745c3c9d6`.
They describe finite folded coefficient profiles with coefficients in
`{0,...,18}`, their actual decimal reverse-add transition, and the
complete finite safe predecessor fiber. `SafeState` retains the original
`WordSafe` meaning; it is not replaced by a new nonpalindromicity predicate.
The prior decimal realization and correspondence theorems are reused.

For even width `L`, `finiteStateHalf s` lists the first `L/2`
coefficients in their original low-index-to-center order. With `d=b+1`,
the weight is

\[
w(s)=A_L\prod_{\text{complete consecutive }d\text{-windows }v
                         \text{ of the half-word}}\psi(v).
\]

There is no padding. A word shorter than the window has the empty product
one. `PositivePotential b psi` asks for positivity only when a list has
length `b+1` and all its entries are at most 18. The width factor is
required positive only at positive even widths. Odd safe states receive
an arbitrary positive extension `oddWeight`.

The stronger witness statement `no_uniform_window_multiplier` is:

\[
\forall K\in\mathbb R\;\exists t,\quad
\operatorname{SafeState}(t)\ \land\
K\,w(t)<\sum_{s\in\operatorname{safeFiber}(t)}w(s).
\]

The sum uses every actual safe predecessor admitted by the original
finite fiber, across all allowed predecessor widths. It is not a
fixed-width replacement for that operator. The selected family is
proved injective and included in the full sum.

## Exact finite-window calculation

Write `a^m` for a repeated letter in this paragraph. Set
`U=[9,9,9,9]`, `V=[14,14,4,4]`, and let the buffer length be any
`B=b+c`, independently of the physical window width `d=b+1`. The literal
source half-word for choices `e_1,...,e_r` and its target are

\[
H_e=[5]9^B\prod_{i=1}^r(M_{e_i}9^B)[14]18^k,
\qquad
R=[11]9^{r(B+4)+B+1}18^k.
\]

Here the product notation in the word formula means concatenation, with
`M_false=U` and `M_true=V`. Let `P` be the complete-window product and
`q=psi(9^d)`. The proved constants are

\[
\beta=\frac{P(9^bV9^b)}{q^{b+4}}>0
\]

and

\[
C_{b,k,\psi}=
\frac{\psi([5]9^b)}{\psi([11]9^b)}
\prod_{j=0}^{\min(k,b)}
\frac{\psi(9^{b-j}[14]18^j)}
     {\psi(9^{b-j}[9]18^j)}>0.
\]

[`inputHalf_exact_total`](../../../Agent108WindowFamilyRatio.lean) proves

\[
\sum_e P(H_e)=C_{b,k,\psi}\,P(R)(1+\beta)^r.
\]

All natural `b,c,k,r` are retained in the literal formula, including
`d=1`, `r=0`, `k=0`, and `k<b`. The endpoint ledger splits the `k+1`
legal starts into `min(k,b)+1` crossing windows and `k-b` all-eighteen
windows. This avoids requiring a long terminal tail. The extra-buffer
factors have exponent `c*(r+1)` and cancel against the corresponding
target factors. Neither `C` nor beta depends on `r` or `c`.

## Reusing the actual arithmetic family

The arithmetic closure does not assume the unfinished original
minimal-buffer interface. It chooses `B=4d` and restricts the **already
verified** original unbuffered binary family by the exact bit embedding

\[
e\longmapsto \mathrm{false}^{d}
\mathbin{+\!+}\operatorname{concat}_i
        ([e_i]\mathbin{+\!+}\mathrm{false}^{d}).
\]

The encoded length is `d+(d+1)*r`. Original bits are recovered at positions
`d+(d+1)*j`, so the restriction is injective.
[`Agent108WindowEmbedding`](../../../Agent108WindowEmbedding.lean) proves
the literal half-word identities, identical actual source/target widths,
and safety and transition facts by direct use of Agent13's original API.
It introduces no replacement carry model.

With `p=d=b+1`, the literal product theorem uses `c=3*b+4`.
`actual_window_family_total` incorporates the arbitrary common width
factor. `incoming_window_lower_bound` then uses the original partial-sum
inclusion. Fixing `k=1` and letting `r` grow proves the final obstruction
from the strictly positive constants and the proved real power-growth
theorem. The result concerns this class of weights on the full folded
safe state space; it is not a theorem about infinite avoidance by the
orbit of 196.

## Source and review map

| Module | Role |
|---|---|
| `Agent108WindowDefs` | Literal words, blocks, buffers, complete windows and binary enumeration |
| `Agent108WindowProducts` | Exact overlap, range-of-starts and window count |
| `Agent108WindowWeights` | Legal-window positivity and elementary products |
| `Agent108WindowEndpoints` | Exact endpoint list partition for every boundary case |
| `Agent108WindowEndpointWeights` | Explicit endpoint ratio and positive constant |
| `Agent108WindowObstruction` | Binary weighted sum and geometric growth |
| `Agent108WindowFamilyProducts` | Product factorization for independent window and buffer lengths |
| `Agent108WindowFamilyRatio` | Pointwise ratio and exact total over binary choices |
| `Agent108WindowEmbedding` | Injective long-buffer restriction of the actual original family |
| `Agent108WindowIncoming` | Equal-width weight transport, full-fiber lower bound and final theorem |

Author and independent evidence are kept separately. Relevant independent
records are `review/independent-combination-5bc7f457/`,
`review/independent-family-products-d4449500/`,
`review/independent-family-ratio-051dcb4/`,
`review/independent-embedding-1acb5964/`, and
`review/independent-window-incoming/`. The final Incoming source SHA256 is
`8929758722b9d66c327654bb182c011b072be6aec100f801349e70040a65b5f6`.

All accepted mathematical transitive axiom reports are restricted to
`propext`, `Classical.choice`, and `Quot.sound`. Compiler-generated
unsafe/partial declarations are separately inventoried, never promoted
to logical axioms. Failed source attempts and actual logs remain in
their development directories and outside the accepted build roots.

This extends section 3 of the original `FOLDED_WEIGHT_OBSTRUCTION.md`
(Git blob `6979703055d0f61b7997355b5e00a92a66ed3ce7`). The original
family, arithmetic, scalar-product result and their authorship remain
attributed to Agent13. The historical checkpoints and their narrower
verification statuses are retained in `CHECKPOINT_02.md`,
`CHECKPOINT_03.md`, and the prior Git commits.
