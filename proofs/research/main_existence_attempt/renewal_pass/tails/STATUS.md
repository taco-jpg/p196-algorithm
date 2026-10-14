# Exact later first hits of the original six repair families

**Decimal Lychrel existence and the claim for 196 remain unproved.**
This result classifies five of the original six core families, apart from
four explicitly isolated small-spacer cases. It is a written finite
symbolic proof with an independent algebraic certificate checker, not a
Lean formalization or an all-time exclusion of the remaining family.

## Statement

For an integer r>=1 and one of the six original core pairs, put

    A = 1 0^r (u,v,v,u) 0^r 1,
    Q = (1+x) A.

The expression Q is coefficientwise polynomial addition, not digit
normalization. Its low-to-high pair word is exactly

    11 0^(r-1) u (u+v) (2v) (u+v) u 0^(r-1) 11.

It is canonical: it is symmetric, its coefficients are between 0 and 18,
its endpoints are positive, and its center coefficient is even. Every
positive decimal integer with these mirrored digit-pair sums has the same
first positive reverse-and-add output and hence the same positive first-hit
time. The statements below concern every such realization.

| Core (u,v) | Spacer domain | Exact first positive palindrome time |
|---|---|---|
| (1,5) | every r>=1 | 3 |
| (2,5) | every r>=1 | 4 |
| (2,6) | every r>=1 | 4 |
| (3,5) | every r>=1 | 4 |
| (1,6) | every r>=5 | 11 |

In particular, increasing the spacer in these five branches cannot turn
their two-step safe return into an infinitely safe return mechanism.
This does not exclude a different generalized outer context or core.

## Explicit palindrome endpoints

Adjacent decimal strings below mean concatenation, and 0^s means a run of
s zeros. The displayed strings are palindromes in either reading direction.

| Core | Domain | First palindrome |
|---|---|---|
| (1,5) | r>=1 | `44` · 0^(r-1) · `56265` · 0^(r-1) · `44` |
| (2,5) | r>=2 | `88` · 0^(r-2) · `1906091` · 0^(r-2) · `88` |
| (2,6) | r>=2 | `88` · 0^(r-2) · `1992991` · 0^(r-2) · `88` |
| (3,5) | r>=2 | `88` · 0^(r-2) · `1796971` · 0^(r-2) · `88` |
| (1,6) | r>=5 | `88088` · 0^(r-5) · `9359999539` · 0^(r-5) · `88088` |

At r=1, the three first-hit-four endpoints are respectively `899060998`,
`899929998`, and `897969798`. These are exact finite boundary cases, not
extrapolations from the displayed negative-length expressions.

## Proof and independent certificate

For a pair word Q(x), let C(x) record its outgoing carries when normalized
from the low decimal end. Each coefficient of C is 0 or 1. The polynomial
of the actual output digits, including an overflow digit when present, is

    D(x) = Q(x) + (x-10) C(x).

If L is the input width and h its final carry, the output width is W=L+h.
Writing rev_W(D)=x^(W-1)D(1/x), its next pair word is

    G(Q) = D + rev_W(D).

The ordinary output is a palindrome exactly when D-rev_W(D)=0.

`symbolic_tail_certificates.json` supplies every intermediate pair word,
actual digit word, reflection difference, and overflow flag. Every run
length has the form a*k+b for an arbitrary integer k>=0, with a>=0 and
b>=1. Its five certificates use r=2+k, 3+k, 3+k, 3+k and 6+k,
respectively. They have 3, 4, 4, 4 and 11 transitions. The overflow clocks
are all zero except for (1,6), whose exact clock is

    0,0,0,0,1,0,1,0,1,0,0.

The independent checker does not use the generator's run normalizer or
run-alignment code. It multiplies each run polynomial by x-1, obtaining
two sparse endpoints per run with affine exponents. It checks the two
identities above as formal sparse-polynomial identities, for every
transition. In each constant input run, coefficients <=8 kill carry,
9 transmits carry, and >=10 sets carry; the carry after the first column
therefore persists to the end of that run. This computes the exact carry
polynomial independently.

The retained digit coefficients lie between 0 and 9 and their leading
digit is nonzero. Thus their polynomial identity is the actual decimal
normalization, with exactly the stated width. The checker also verifies
the reflection-difference polynomial and its positive-length disjoint run
decomposition. Before the final transition, at least one of those runs
has a nonzero coefficient; at the final transition every coefficient is
zero. Positivity of all run lengths makes these first-hit assertions valid
for every k>=0, not just for sampled parameter values.

The finitely many missing lower boundary values are checked by ordinary
integer reversal and addition. Their exact seeds, first hits and endpoints
are retained in `symbolic_tail_audit.json`. Induction on the finite list of
verified transitions establishes the table. All realizations share the
same first output because evaluating their pair word at 10 equals
n+reverse(n), so the conclusion is independent of the chosen realization.

The checker independently verifies 26 symbolic transitions and 208
ordinary-integer transition controls, including k=1024. The unrestricted
parameter conclusion follows from the polynomial proof; the controls
audit its implementation. No infinite-time conclusion is inferred.

## Remaining cases and finite exploration

`finite_tail_census.json` records all 216 requested cases: six cores,
r=1,...,32,64,127,256,512, and a horizon of 512 additions. Every outcome is
retained, including UNKNOWN, along with the seed, last value, first-hit
time where found, and a hash of the checked trajectory.

- (1,6) with r=1,2,3,4 remains UNKNOWN within that horizon.
- (1,7) with r=3 first reaches a palindrome at time 11.
- Every other tested (1,7) case remains UNKNOWN within that horizon.

These finite UNKNOWN cases are not proved Lychrel numbers. No claim about
all spacer lengths in the remaining (1,7) family is made. Failed attempts
to certify too-small affine domains are retained in the symbolic JSON;
their failure is not a mathematical counterexample to a statement.

## Reproduction

From this directory:

    python3 -B finite_tail_census.py
    python3 -B symbolic_tail_certificates.py
    python3 -B check_symbolic_tails.py

The generator imports the preserved
`../../smart_pass/collision/orthant_runs.py`; the independent checker uses
only the Python standard library. No solver or Lean installation is
required for these checks.

## Concurrent research handoff

The other contribution stream announced gate-review work in commit
`8974c5a84ad38366b34316ee53f15e1da862e018`, under
`proofs/contributions/COORDINATION.md`. Its first-hit-four and possible
first-hit-eleven directions overlap the table above. These certificates
are supplied for independent review and reuse; no unobserved agreement,
external verification, or priority claim is asserted. The other stream's
schedule-sensitive run18 erosion and finite-horizon density proposals are
separate directions and remain proposals until their evidence is reviewed.
