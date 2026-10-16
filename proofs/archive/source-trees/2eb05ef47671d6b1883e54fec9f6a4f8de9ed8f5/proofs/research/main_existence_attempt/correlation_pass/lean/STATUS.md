# Exact finite-delay bridge and arbitrary decimal safe prefixes

Decimal Lychrel existence remains **unproved**. This branch supplies a
kernel-checked bridge that previously existed only as a mathematical
argument, and discharges the arbitrary-length safe-prefix construction.
It does not prove that finite terminating delays are bounded or unbounded.

## Exact definitions and equivalences

`FirstPositiveHit n d` means `d>0`, the actual integer `orbit n d` is a
palindrome, and no positive earlier iterate is a palindrome. The initial
value may itself be a palindrome. `FiniteDelayBound D` means that every
finite positive first-hit delay of every positive integer is at most D.

The pair-state definitions use the existing exact decimal operations:

    Valid (L,q) = Admissible L q
    G (L,q) = (nextWidth q L, nextColumns q L)
    B (L,q) = BadWord L q
    S_0 = Valid
    S_(r+1) = { G(s) : s in S_r and s not in B }
    K_r = S_r minus B.

The target of a safe-ancestry chain is not tested until an additional
condition is imposed. In particular these are the predecessor-tested
sets from the original language discussion, rather than the separate
`HasSafeAncestor` convention that tests both endpoints.

`PairDelayBridge.lean` proves, with the actual numeric realization:

    S_r intersects B
      iff some positive integer has first positive hit r+1;

    S_r is disjoint from B
      iff every finite positive first hit is at most r;

    K_r is forward closed
      iff every finite positive first hit is at most r+1.

All finite attained positive delays form an initial segment: a trajectory
with delay d provides one with any delay k satisfying 1<=k<=d by starting
at its (d-k)-th iterate. Consequently unbounded finite terminating delays,
attainment of every positive delay, and `S_r intersects B` at every depth
are equivalent. None of these equivalent assertions is proved true.

The generic logical recurrence is in `SafeDelay.lean`. The ordinary
integer specialization is in `DecimalDelayBridge.lean`; the pair-word
specialization independently discharges admissibility, realizability,
finite-prefix agreement, and changes of width using existing theorems.

## Unconditional finite safe segments

For every natural D define the ordinary finite integer

    C_D = 2 * (10^(2D+1) - 1).

Its decimal form is a leading 1, then 2D copies of 9, then 8. For example,
C_0=18, C_1=1998, and C_2=199998. The checked theorem
`DecimalDelayBridge.candidate_safe_prefix` proves

    for every k<=D, orbit(C_D,k) is not a palindrome.

This is an all-D theorem, not finite experimental evidence. Its proof is
in `DecimalSafeRuns.lean`: a run of m+2t consecutive pair coefficients 18
leaves a run of at least m after t actual transitions, in either overflow
branch. A coefficient 18 excludes both exact palindrome-predecessor
patterns. The initial representation is the integer with 2D+1 nines,
whose first D+1 positive iterates are safe; shifting once gives C_D and
includes the candidate's time-zero state in the safety conclusion.

No theorem says that C_D eventually terminates. Long finite safe segments
alone do not prove unbounded *finite terminating* delays.

## Concrete conditional existence and the remaining gap

`DecimalDelayBridge.candidate_lychrel_of_finiteDelayBound` proves

    FiniteDelayBound D -> IsLychrel C_D.

The safe family is already proved; it is not an additional hypothesis.
The pair-cutoff theorem gives `IsLychrel C_r` from `S_r` disjoint from B.
The closed-kernel theorem gives `IsLychrel C_(r+1)` from forward closure
of K_r. These use the existing actual decimal `IsLychrel` definition,
which excludes palindromes at every index including zero.

The unconditional theorem `existence_or_unbounded_finite_delays` proves

    DecimalLychrelExistence OR UnboundedFiniteDelays.

This is a nonexclusive disjunction and does not select a branch. In
particular, if decimal Lychrel existence were false then every positive
finite delay would be attained. There is no proof here that a finite
delay bound exists, that any particular K_r is closed, or that terminating
delays are unbounded. The 196 conjecture is not resolved.

## Nonempty finite depths do not produce one fixed infinite-depth target

The exact pair kernels are descending and nonempty at every finite depth.
The proof of nonemptiness uses the explicit safe family above. Yet their
intersection over all finite depths is empty: membership of a fixed
finite target (L,q) in S_r implies r<=4L by the established decimal width
growth theorem. The theorem `nonempty_depths_empty_intersection` states

    (for every r there exists s in K_r)
      AND NOT (there exists s belonging to every K_r).

This does not rule out a safe infinite forward orbit, whose target changes
with time. It rigorously prevents swapping these quantifiers in a proposed
finite-word compactness argument.

## Reproduction and audit

From the project root run:

    python main_existence_attempt/correlation_pass/lean/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker copies the unchanged `continuation/LychrelDigitSums.lean` and
all four new modules into `fresh_build/`, removes their previous compiled
outputs, and rebuilds them with Lean 4.19.0. It then compiles generated
`AllAxioms.lean`, auditing every one of the 63 new theorem declarations
transitively. The only permitted axioms are Lean's standard `propext`,
`Classical.choice`, and `Quot.sound`. New sources are also screened for
proof placeholders, custom axiom declarations, and `native_decide`.

`compile.log` records compiler output, and `verification.json` is written
only after all source compilations, the full axiom audit, and before/after
source-hash checks succeed. No older research source is modified.

Fresh rebuild result: **PASS**. The dependency compiled in 51.26 seconds,
the four new modules in 3.23 seconds total, and the complete 63-theorem
audit in 1.91 seconds. Every audited theorem uses only the standard
logical axioms listed above. Exact source hashes are in `verification.json`.
