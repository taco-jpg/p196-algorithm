# Correlation and finite-delay pass — 14 October 2026

**Decimal Lychrel existence and the claim about 196 remain unproved.** This
pass contains checked supporting theorems, exact construction identities,
specific invariant obstructions, and explicitly incomplete positive searches.
No novelty, external peer review, or solution claim is made.

## The main formal advance

For every natural D define the finite positive decimal integer

    C_D = 2 * (10^(2D+1) - 1).

Four new Lean modules prove that C_D is nonpalindromic at every orbit index
0 through D, without an unproved growth or safety hypothesis. They then prove

    FiniteDelayBound D -> IsLychrel C_D,

where the hypothesis says that every finite positive first-palindrome time
of every positive integer is at most D. The safe family is proved; no value
of D satisfying the bound is supplied. The existence-or-unbounded-finite-
delay disjunction is unconditional and nonexclusive, and does not select
either branch.

The exact safe-image recurrence S_(r+1)=G(S_r minus B), its safe kernel K_r,
and their connections to first-hit times are also formalized for actual
numeric and admissible pair-word dynamics. In particular, K_r is closed
exactly when all finite positive delays are at most r+1. Every finite K_r
is nonempty, but no fixed finite pair word belongs to every K_r. These
statements retain the correct predecessor-tested endpoint convention.

The fresh Lean 4.19.0 dependency rebuild and all 63 new theorem axiom audits
pass. Root independently recompiled the four mathematical modules and the
complete audit against that freshly checked dependency. Only `propext`,
`Classical.choice`, and `Quot.sound` occur. See `lean/STATUS.md`, source,
`verification.json`, and `root_verification.json`.

## Correlations retained beyond terminal-flag selection

The language branch retains complete NFA configurations, including
nonaccepting residual states, and combines them with exact observation
residuals through depth ten. It produced 146 explicit class collisions with
terminating words on the first 101 states of the 196 trajectory. Both the
branch checker and root replay verified every saved collision and ordinary
integer first-hit time. This excludes accepting those entire classes in a
safe closed language, not arbitrary refinements or all possible witnesses.

At depth ten, the class of the 196 trajectory at position 69 also contains
364699330000, which reaches its first palindrome after 13 additions. Any
safe closed language using exactly that class information cannot include
the position-69 state or an earlier state on the same trajectory. Entering
an invariant at a later state is not excluded.

The literal closure candidate S2 intersect first-eleven-output safety fails
at 9948 -> 18447. The 65,170-entry incomparable-configuration snapshot is
independently checked, but its 90-second exploration did not complete.
Global configuration closure and global positive synthesis remain UNKNOWN.
See `language/STATUS.md` and `METHOD_AND_PROOF.md`.

## Exact seam arithmetic and recursive closure

The construction branch replaces the previously failed independent motif
concatenation with an exact endpoint-overlap identity, including the full
neutral-run correction and its mass loss. The identity applies to arbitrary
eligible symmetric motifs in a reflection-symmetric list. It also proves
why a bounded spatial repair radius cannot cover every seam, and why
independent stepwise evolution with fixed overlaps and a duplicated positive
component must fail within five updates. These restrictions do not exclude
coupled seams or return identities at selected times.

Root replayed the 7,296 arbitrary-motif controls, 67 long-radius controls,
and 384 constant-family controls using ordinary integer reversal/addition.
The all-parameter proof is the written carry calculation; the finite tests
audit its implementation.

The variable-overlap follow-on proves an exact two-step delayed repair for
every spacer length r >= 1 and six eligible core pairs. With
A = 1 0^r (u,v,v,u) 0^r 1 and the one-place overlap Phi(A) = (1+x)A,
both positive iterates of Phi(A) are nonpalindromic and
G^2(Phi(A)) = Phi(G^2(A)). The intermediate state leaves this overlap form;
an antisymmetric normalization discrepancy disappears in the second update.
The identity has a written carry proof and 396 ordinary-integer controls,
all replayed independently. It is not claimed as a Lean theorem.

This is a finite return identity, not a recurrent safe family: the spacer
length stays fixed and every returned core leaves the eligible starting
domain. The (u,v) = (1,5) branch reaches a palindrome at its third positive
iterate for every r. A later return to an eligible core with compatible
context and safety remains unproved. See
`constructive/VARIABLE_OVERLAP_AND_GATE.md` for the identity, the exact
one-step variable-shift classification, and the remaining return obligation.

## Free-clock positive construction search

Candidate clocks were generated from actual prefix carry equations rather
than imposed independently. Sampling spatial periods five and seven
produced ten one-column and three four-column candidates at period five.
An independent 19-state extension relation proves that nine of these
prescribed prefix schedules cannot accommodate even one further column
through a complete cycle. This is an exact finite arithmetic obstruction
for those schedules, not a general clock exclusion.

For the remaining alternating period-five bulk, cyclic inverse languages
include every temporal repetition. Forward and reverse bisimulation improve
the completed depth from 8 to 16; the final graph has 16,039 vertices and
104,091 edges. No root cycle or recurrence was obtained before the raw
one-million-element cap. The unrestricted-width question remains UNKNOWN.
The quotient preserves periodic traces up to positive powers, not exact
single periods; the report states the lifting and repetition conditions.

The local arithmetic passes 14,400 prefix cases and 4,418 bulk cases with
109,211 interior comparisons against ordinary integer arithmetic. Solver
timeouts, truncated reverse searches, and the cyclic graph cap retain their
original UNKNOWN scope. See `free_clock/STATUS.md`.

## What is still required

A successful proof still needs an actual nonempty safe forward invariant
or a different all-time argument for a finite positive seed. The new
conditional witness theorem provides one precise route: establish a
universal finite terminating-delay bound. Neither the finite safe family,
the disjunction, the listed obstructions, nor an incomplete search provides
that bound. No source file contains a verified decimal Lychrel witness.
