# Review of the external finite-seed extraction obstructions

Root read the complete written proof at external commit
`e52125515490b668d14e95b0cf8d31767bcde7c4`, path
`proofs/research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md`,
Git blob `a56603a78845cb2371137050ea095a2a0d69adad`.
The mathematical arguments pass this review. This is a written-proof review;
no additional finite audit or Lean build was performed here.

The terminating countermap has disjoint cases: chain nodes have outside
pair sum10, so none lies in the preserved immediate-palindrome predecessor
set B. Labels are recoverable from width and the remainder10a+9. All
nonterminal artificial outputs are nonpalindromic; the final b(a) lies in
B and retains the true update. Thus every individual seed reaches a
palindrome, while the generic first positive hit time is ell(L)+3.
The word "positive" correctly excludes a possibly palindromic initial seed.

The numeric bound <11n and the one-digit maximum growth follow from the
stated tail inequalities. Every artificial step outside B increases width,
so five steps without width growth would all be genuine no-overflow steps;
the trailing-digit doubling contradiction justifies the preserved five-step
width lower bound. The sparse exceptions have vanishing relative density.
The conclusion is **for every prescribed finite horizon function, there is
a terminating map with density-one survival through that horizon**. It does
not interchange this into one map surviving every horizon, or one finite
seed surviving indefinitely.

The pair-word quotient strengthening also checks: at fixed width, the digits
encoding a occupy one interior half without overlap, so equal pair words
recover the same label. Enlarging exceptional nodes to full fibers keeps
them outside B and replaces the sparse-node exception by a polynomial-size
exception. The true update on B already factors through the pair word.
The countermap still does not preserve the actual numeric update outside B;
that limitation is explicit and essential.

The actual reverse-and-add fiber construction is separate from the model.
For n_A=A||99||complement(reverse(A)), mirrored sums are9 except for the
two central18 columns. Their common target is the stated y_m, and the
9*10^(m-2) canonical choices of A give distinct smaller safe inputs. Any
positive weight nonincreasing with input size therefore gives incoming
weight at least9*10^(m-2) times the target's weight. This correctly excludes
a uniform finite pointwise multiplier for that weight class, not all
weighted or aggregate arguments.

Finally, the fixed-target inverse bound follows from genuine growth:
1+floor(t/5)<=M implies t<=5M-1, and strict integer growth separately gives
t<=p-1. This prevents an unbounded inverse tree at one fixed finite target;
it does not settle forward survival when targets vary.

These results identify insufficiency of specified hypotheses. They neither
assert actual reverse-and-add termination nor resolve decimal Lychrel
existence. The construction and quantifier stream remains the other team's
work; this review acknowledges its exact scope and avoids restarting those
already excluded extraction arguments.
