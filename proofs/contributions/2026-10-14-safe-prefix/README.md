# Shorter explicit decimal safe prefixes

This contribution strengthens the finite safe-prefix construction in
`research/main_existence_attempt/correlation_pass/lean/DecimalSafeRuns.lean`.
It proves neither decimal Lychrel existence nor the 196 conjecture.

## Main unconditional theorem

For every natural number R, put

\[
\ell_R=\left\lfloor\frac{7R}{4}\right\rfloor+1,
\qquad C'_R=2(10^{\ell_R}-1).
\]

Then the actual decimal reverse-and-add orbit of C'_R is nonpalindromic
at every index k with 0 <= k <= R. This is the Lean theorem
`OverflowSafeRuns.shorterCandidate_safe_prefix`.

The previous construction used exponent 2R+1. The new exponent is
strictly smaller for every R>0, with an asymptotic reduction of 12.5%.
For R=0 the candidate is 18; for R=1 it is 198. The construction does
not require the input itself to be a palindrome: it shifts the all-nines
seed by one actual reverse-and-add operation.

## Why the stronger estimate works

Let W_t be the actual pair-word width after t transitions, starting with
width L. Let N_t count the nonoverflow transitions among those t steps,
and define the erosion budget E_t=t+N_t.

* A nonoverflow transition preserves the interior of a run of 18s after
  discarding its first and last columns: a run of m+2 supplies a run of m.
* An overflow transition needs only two adjacent input columns equal to
  18. It discards only the first column: a run of m+1 supplies a run of m.

The second fact is new here. Reflection moves from index L-1-i to L-i
when the width increases, so only the adjacent pair at i-1 and i is
required. Both normalized output digits are nine.

Induction gives the schedule-sensitive statement

\[
\operatorname{HasRun18}(q,L,m+E_t)
\Longrightarrow
\operatorname{HasRun18}(q_t,W_t,m).
\]

The exact accounting identity is

\[
E_t+W_t=L+2t.
\]

The existing width-growth potential p satisfies

\[
t+4L\le4W_t+p(q_0),\qquad 0\le p(q_0)\le4.
\]

Combining the two gives

\[
4E_t\le7t+p(q_0).
\]

For an all-nines seed, every initial pair coefficient is 18 and p(18)=0.
Thus E_t <= floor(7t/4). Starting with floor(7R/4)+1 copies of nine
leaves at least one coefficient 18 at every t<=R. Such a coefficient
excludes both exact palindrome-predecessor patterns, so the next integer
is not a palindrome. Shifting once gives the claimed result for C'_R.

For arbitrary canonical decimal inputs, `safe_prefix_of_uniform_run`
also proves that an initial run of

\[
1+\left\lfloor\frac{7R+4}{4}\right\rfloor
\]

pair coefficients equal to 18 certifies every positive time 1 through
R+1. `iter_not_palindrome_of_run_bound` retains the smaller exact initial
outer-column potential when available.

## Conditional consequences and scope

* If C'_R has a finite first positive palindrome time d, then d>R.
  Its eventual termination is not established.
* If all finite first positive palindrome times of all positive integers
  are bounded by R, then C'_R is a decimal Lychrel number. The global
  finite-delay bound is an explicit, unproved hypothesis.
* These theorems supply a different finite integer for each horizon.
  They do not produce one fixed integer avoiding palindromes forever.

## Reproduction

From this directory, run:

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

An environment-specific Lean wrapper is also accepted. The checker
copies the exact current sources into a fresh temporary directory,
rebuilds all four dependencies plus the new module, and audits all 20
new theorem declarations. The permitted axioms are only `propext`,
`Classical.choice`, and `Quot.sound`. It also rejects proof placeholders,
custom axiom declarations, and `native_decide` in the new source.

`compile.log` contains the full compiler output. `verification.json`
is created only after successful rebuilding, a complete axiom audit,
and confirmation that source hashes did not change during the run.
It records both SHA-256 and Git blob hashes for the exact checked sources.

`python -B check_arithmetic.py` separately checks the actual ordinary
integer candidates for R=0,...,128, including all 8,385 claimed states.
Its exact finite scope is recorded in `arithmetic.json`; it is an
independent arithmetic control, not the proof of the all-R statement.
