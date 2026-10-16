# An explicit infinite family with a certified finite delay

Status: **finite-horizon theorem**, conditional only on the accompanying
finite trace being verified. This is not an all-time invariant or a proof
that any fixed seed is Lychrel.

Let `F(n) = n + reverse(n)` in base ten. For every integer `r >= 1`, set

\[
n_r=10^{2r+6}+10^{2r+5}+10^{r+5}+8\,10^{r+4}+7\,10^{r+3}.
\]

All five exponents are distinct for `r >= 1`. Thus this is an ordinary
decimal integer of width `2r+7`, with leading digit 1 and trailing digit 0.
In particular, `n_r` itself is not palindromic.

## Reduction to one driver

Write pair-coefficient words least significant column first. Directly
pairing the digits of `n_r` gives

\[
Q_r=(1,1)\,0^{r-1}\,(1,8,14,8,1)\,0^{r-1}\,(1,1).
\]

This identifies an explicit integer seed, rather than just an abstract
admissible word. Put `B_0=(1,1)`, `H_0=(1,8,14,8,1)` and `S_0=0`.
For any finite coefficient word `W`, let `N(W)` be its ordinary decimal
normalization, retaining its final carry when present. Let `e_t` and
`h_t` be the final carry bits of `B_t` and `H_t`, respectively, and put
`delta_t=max(e_t,h_t)`. The established separation formula gives

\[
\begin{aligned}
B_{t+1}&=N(B_t)+\operatorname{rev}N(B_t),\\
H_{t+1}(x)&=x^{\delta_t-e_t}N(H_t)(x)
 +x^{|H_t|+\delta_t-1}N(H_t)(x^{-1}),\\
S_{t+1}&=S_t+\delta_t.
\end{aligned}
\]

Here addition in the first line is coefficientwise at the actual
normalized width. None of these definitions depends on `r`.

For any `T >= 1`, suppose that the driver records `t=0,...,T-1` are
verified, and that there is no time in that range when `B_t` and `H_t`
are simultaneously palindrome predecessors with matching final carry
bits. Then

\[
\boxed{r\ge S_{T-1}+1\quad\Longrightarrow\quad
F^k(n_r)\text{ is nonpalindromic for every }0\le k\le T.}
\]

**Proof.** The digit computation above handles `k=0` and establishes the
initial pair word. Because `S_t` is nondecreasing, the assumed parameter
bound gives `g_t=r-1-S_t >= 0` for every checked time. At a positive
gap, the exact separated-block update applies. At a zero gap with
`t < T-1`, the inequalities `S_t=r-1` and `S_(t+1)<=S_(T-1)<=r-1`
force `delta_t=0`. Both blocks therefore normalize without overflow.
The zero-gap closure theorem then gives the same driver update, with
zero gap and unchanged block widths. Induction identifies the pair word
of `F^t(n_r)` as `B_t 0^{g_t} H_t 0^{g_t} B_t` for `0 <= t < T`.
The palindrome criterion, valid also at zero gap, says that normalizing
this word is palindromic
exactly when its two component blocks are palindrome predecessors with
matching carry bits. The verified absence of that event proves that
`F^{t+1}(n_r)` is nonpalindromic for every checked `t`. This proves the
claim, including the final time `T`. No separated-block update beyond
the last checked state is needed. ∎

## The recorded certificate

The independent streaming audit of
`../2026-10-14-collision-review/driver_trace.bin.gz` checks all 10,000
records and all 9,999 recorded transitions. At the final recorded time
`t=9999`, the exact accumulated spacer loss is `S_9999=5077`.
There is no simultaneous matching palindrome-predecessor event.
Consequently, **every `n_r` with `r >= 5078` has no palindrome at
times `0,...,10000`**. The smallest member covered by this certificate
has `2*5078+7 = 10163` digits. Allowing the final gap to be zero improves
the earlier conservative handoff threshold `r>=5079`; that weaker claim
remains valid.

The compressed trace SHA-256 is
`6431d3a11008f81e9249f05187e207a73f9f1dc0e87c897e46030f2a16b02404`.
The adjacent `check_family.py` independently checks the explicit integer
realization, the indexing of the reduction, and ordinary integer orbits
for small parameters. It also extracts the final record and checks the
claimed threshold without regenerating or replacing the trace.

This does not assert that `n_5078` survives time 10001, that all larger
parameters have any common infinite behavior, or that the original seed
196 has been settled. Extending a finite horizon requires additional
evidence; proving all-time survival requires an invariant not supplied
here.

## Dependencies

- [Exact separated-block dynamics and exhaustion](../2026-10-14-overlap-gate/SEPARATION_EXHAUSTION.md).
- [Zero-gap independent closure](../2026-10-14-collision/COLLISION_RESPONSE.md).
- [Zero-gap palindrome criterion](../2026-10-14-collision-review/COLLISION_REVIEW.md).
- [Recorded driver](../2026-10-14-collision-review/driver_search.py).
- Independent complete trace verification in `../2026-10-14-collision-audit/`.

This corollary is a written proof with independently checked finite
evidence. It has not itself been formalized in Lean.
