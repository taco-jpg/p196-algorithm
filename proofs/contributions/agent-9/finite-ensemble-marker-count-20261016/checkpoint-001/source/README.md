# Finite-horizon avoidance has density one

This contribution builds directly on the overflow-sensitive run theorem in
[`OverflowSafeRuns.lean`](../2026-10-14-safe-prefix/OverflowSafeRuns.lean).
It proves an explicit counting bound for uniform finite decimal seeds and
a growing-finite-horizon consequence. It does not prove decimal Lychrel
existence, eventual termination, or the assertion for 196. No novelty or
external peer-review claim is made.

## Exact finite counting bound

Let `T(n) = n + reverse10(n)`. Fix integers `L >= 1`, `H >= 1`, and choose
`n` uniformly from all `9*10^(L-1)` positive `L`-digit integers. Define

\[
 m=\lfloor L/2\rfloor,\qquad
 r=\min\{2H-1,\ \lfloor 7(H-1)/4\rfloor+2\},\qquad
 J=\left\lfloor\frac{\max(m-1,0)}r\right\rfloor.
\]

Then

\[
\Pr\{T^k(n)\text{ is a palindrome for some }1\le k\le H\}
\ \le\ (1-10^{-2r})^J. \tag{1}
\]

The initial integer is allowed to be a palindrome in (1). Including time
zero gives the further bound

\[
\Pr\{T^k(n)\text{ is a palindrome for some }0\le k\le H\}
\ \le\ \min\{1,\ 10^{-m}+(1-10^{-2r})^J\}. \tag{2}
\]

The exact integer form of the event used in the proof is

\[
\#\{n:\text{none of the selected blocks is all-nine}\}
 =9\,10^{L-1-2rJ}(10^{2r}-1)^J. \tag{3}
\]

These are upper bounds on early hits, not exact early-hit probabilities.
When `J=0`, (1) is the valid but vacuous upper bound 1.

### Deterministic block implication

Write the digits of `n` as `d_0,...,d_(L-1)`, least significant first,
and put `q_i=d_i+d_(L-1-i)`. If a contiguous block of `r` digits and its
reflected block are all nine, then the corresponding `r` pair sums are
all 18.

The earlier run theorem guarantees survival through `H` positive steps
from a run of length `2H-1`. The new overflow-sensitive theorem guarantees
the same from a run of length `floor(7(H-1)/4)+2`: its erosion cost after
`t` steps satisfies `4*cost <= 7t+4`. Taking the smaller sufficient length
gives exactly `r` above. For each `1 <= k <= H`, the surviving 18 column
excludes the exact palindrome-predecessor classes before step `k`.

[`FiniteHorizonBlocks.lean`](FiniteHorizonBlocks.lean) checks this entire
deterministic implication against the actual integer reverse-and-add map.
It defines `blockLength R` with `R=H-1`, checks the better-bound selection,
and proves `mirroredNines_safe_prefix`. Its four theorem declarations use
only the ordinary logical axioms of the existing development. The counting
and asymptotic arguments below are written proofs, not Lean formalizations.

### Counting proof

Select `J` disjoint intervals of length `r` in the index set
`{1,...,m-1}`; for example, interval `j` starts at `1+j*r`, for
`j=0,...,J-1`. Include each interval's reflected positions as well.

The selected sets are disjoint, including when `L` is odd. They avoid
both endpoints and, for odd `L`, the central digit. Under the uniform law on canonical
`L`-digit integers, all selected digits are independent and uniform on
`{0,...,9}`. The leading digit's restriction to `{1,...,9}` therefore has
no effect on any selected event.

Each block event fixes exactly `2r` digits to nine and has probability
`10^(-2r)`. The `J` events are independent. A seed with any block event
cannot have a positive hit by `H`, by the deterministic implication.
Thus every seed counted on the left side of (1) lies in the complement
of all these events, proving (1). Counting that complement by free digits
gives (3); the exponent is nonnegative because the selected digits are
distinct non-leading positions.

There are exactly `9*10^(ceil(L/2)-1)` canonical palindromes of width `L`,
so their fraction is `10^(-m)`. The union bound proves (2). No independence
between initial palindromicity and the block events is assumed.

One can also keep the exact overlap with initial palindromes. Set
`a=10^(-m)`, `b=10^(-r)`, and `p=10^(-2r)`. Conditional on initial
palindromicity, each selected mirrored block has probability `b`, and
these events remain independent because their free half-digits are
disjoint and non-leading. Hence the probability of being both initially
palindromic and unmarked is exactly `a*(1-b)^J`. This gives the sharper
upper bound

\[
\Pr\{\text{a hit at some time }0,\ldots,H\}
 \le (1-p)^J+a[1-(1-b)^J]. \tag{4}
\]

For a uniform initially nonpalindromic seed of width `L >= 2`, it gives

\[
\Pr\{\text{a positive hit by }H\mid n\text{ is not palindromic}\}
 \le \frac{(1-p)^J-a(1-b)^J}{1-a}. \tag{5}
\]

These refinements use exact intersections, not an assumption that the
palindrome and marker events are independent.

## Consequences and order of quantifiers

For every fixed `H`, as `L` tends to infinity, `J` tends to infinity and
`r` stays fixed. Equations (1) and (2) show that the fraction surviving
through that finite horizon tends to one.

More strongly, fix any real `c` with `0 < c < 2/7` and set

\[
 H(L)=\max\{1,\lfloor c\log_{10}L\rfloor\}.
\]

The fraction of `L`-digit seeds avoiding palindromes at every time
`0,...,H(L)` still tends to one. To verify this, for all sufficiently
large `L` we have

\[
 r\le\tfrac74c\log_{10}L+2,\qquad
 10^{-2r}\ge10^{-4}L^{-7c/2},\qquad J\ge L/(8r).
\]

The last inequality follows from `m-1 >= L/4` eventually and
`floor(x) >= x/2` for `x >= 2`. Consequently

\[
 J10^{-2r}\ge\frac{10^{-4}}{8r}L^{1-7c/2}\longrightarrow\infty.
\]

Using `(1-p)^J <= exp(-Jp)` in (2), together with `10^(-m) -> 0`, proves
the assertion. The logarithm is of the **number of input digits**, not
of the input integer. This deliberately conservative constant comes from
the verified local bound; no optimality is asserted.

Both statements change the seed ensemble as the horizon or width grows.
Neither gives a fixed seed surviving every time. Every seed could still
terminate later without contradicting these conclusions. In particular,
interchanging the width limit and an infinite-time requirement would be
invalid. The construction supplies no finite-delay upper bound of the kind
needed by `shorterCandidate_lychrel_of_finiteDelayBound`.

## Verification

The deterministic Lean module compiles with Lean 4.19.0, using the existing
`LychrelDigitSums`, `DecimalSafeRuns`, `SafeDelay`, `DecimalDelayBridge`, and
the new `OverflowSafeRuns` modules. Compile those dependencies in that
order, then compile `FiniteHorizonBlocks.lean` with the containing directory
in `LEAN_PATH`. Each of its four declarations prints its axiom dependency
list; no `sorry`, added axiom, or `native_decide` is used here.

For a complete clean rebuild and axiom audit of these four declarations:

```sh
python proofs/contributions/2026-10-14-finite-horizon-density/check_lean.py /absolute/path/to/lean
```

This rebuilds all dependencies from source in a temporary directory,
verifies Lean 4.19.0, and writes `compile.log` and `verification.json`
including exact source hashes. The reproduction program accepts an
environment wrapper as the executable argument if the host requires one.

The standard-library replay command is:

```sh
python -B proofs/contributions/2026-10-14-finite-horizon-density/independent_replay.py
```

Its finite controls test the counting implementation and actual arithmetic.
They do not replace either the all-width counting proof or the Lean
deterministic implication. See `audit.json` for exact tested scope.
