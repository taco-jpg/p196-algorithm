# Variable overlap: exact one-step classification and a safe delayed repair

This follow-on supplies an exact all-length **two-step delayed repair**.
It does not supply a recurrent construction, a finite Lychrel witness, or
a proof for 196. The earlier `STATUS.md` and its checked identities are
unchanged.

Write Phi_s(A)=(1+x^s)A for the coefficientwise sum of a symmetric pair
word A and its shift by s>=0. There is no normalization in Phi. When
0<s<|A| it is a variable-depth overlap; s=|A| is concatenation. Only a
canonical whole input Phi_s(A) is used as an ordinary pair word.

## 1. Allowing the overlap depth to change: an exact iff theorem

Let A be canonical, Q=Phi_s(A) canonical, and D the actual digit word
obtained by normalizing A, including its final overflow digit if present.
Thus G(A)=D+reverse(D). Let C be the number of outgoing carries when the
redundant digit word D+x^s D is normalized. Count a final outgoing carry
too; each carry is 0 or 1.

The exact mass identity is

    mass(G(Q)) = 2 mass(G(A)) - 18 C.                 (1)

Consequently, for any proposed new shift s'>=0,

    G(Phi_s(A)) = Phi_s'(G(A))

holds **if and only if** C=0 and s'=s. In particular, choosing a different
overlap depth cannot absorb a carry interaction while the two motifs
continue to evolve independently. In a closed step the physical shift
stays fixed; the overlap depth grows only by the component's own width
increment.

Proof: evaluating the pair-word polynomial Q at 10 gives exactly
(1+10^s) times the value of A. Therefore the ordinary whole successor is
the normalization of D+x^sD. Its digit sum is twice that of D minus 9C.
Pair mass is twice digit sum, proving (1). Every candidate Phi_s'(G(A))
has mass exactly twice mass(G(A)), regardless of s'. Equality forces C=0.
Without carries, the successor digits are literally D+x^sD; pairing them
gives Phi_s(G(A)). Its positive outer coefficients fix its width, so s'=s.
This also proves sufficiency, including the case s=0.

At a closed step the whole ordinary successor is palindromic exactly when
the component's ordinary successor is palindromic. Indeed, the digit
polynomial is (1+x^s)D and its reflection is
(1+x^s)reverse(D). Cancellation in the polynomial ring gives the claimed
equivalence. Thus a stepwise closed variable-depth embedding preserves
the component's positive first-hit times. This conclusion does not apply
when an intermediate seam error is allowed and later erased.

## 2. An all-length safe two-step delayed repair

For every integer r>=1 and

    (u,v) in {(1,5),(1,6),(1,7),(2,5),(2,6),(3,5)},

equivalently u>=1, 5<=v<=7, u+v<=8, put

    A = 1 · 0^r · (u,v,v,u) · 0^r · 1,
    Q = Phi_1(A).

Every word here is finite. Both A and Q are canonical. Define

    A' = 4 · 0^r · (4u+1,4v-19,4v-19,4u+1) · 0^r · 4.

Then exactly

    G^2(A) = A',
    G^2(Q) = Phi_1(A').                              (2)

Both positive ordinary iterates of every realization of Q are
nonpalindromic. At the intermediate step independent overlap **fails**:

    G(Q) - Phi_1(G(A))
      = 0^(r+2) · (1,-20,1) · 0^(r+2).              (3)

All words in (3) have width 2r+7; the displayed correction has that same
width. The formal target Phi_1(G(A)) contains a central coefficient 4v>18
and is not a canonical pair word. It is used as a redundant coefficient
polynomial, never as an asserted finite decimal pair-word realization.

The component's first ordinary successor is a palindrome, since A itself
is a symmetric digit word with all coefficients below 10. The whole Q
avoids that palindrome, undergoes a genuine carry interaction, and then
recovers the overlap relation in (2). This is therefore outside the
one-step palindrome-preserving embedding theorem above.

### All-parameter carry proof and boundary conditions

Put z=u+v, so 6<=z<=8. The ordinary normalization of A has no carries, hence
G(A)=2A. In Q, all adjacent sums are below 10 except the central 2v. Its
carry enters a neighboring coefficient z<=8 and resets there. The outside
coefficients and zeros have zero outgoing carry. Taking the mirrored sums
gives (3): the central triple (2z,4v,2z) of the formal target becomes
(2z+1,4v-20,2z+1).

On the next normalization the coefficient immediately before this triple
is 2u<=6. Thus incoming carry is exactly zero, for every r. The two triples
normalize as follows, each leaving carry one:

| Triple being normalized | Three retained digits |
|---|---|
| (2z,4v,2z) | (2z-10,4v-19,2z-8) |
| (2z+1,4v-20,2z+1) | (2z-9,4v-19,2z-9) |

The digit difference is (1,0,-1). The following coefficient 2u resets the
common carry. All other normalized digits agree. The global outside
coefficient is 2, so neither normalization has a final overflow. The
triple is centered in their common full digit width; its antisymmetric
digit difference disappears when mirrored sums are taken.

Finally, normalizing 2A gives the core digit word

    (2u, 2v-10, 2v-9, 2u+1)

between the unchanged zero runs and outside digits 2. Adding this digit
word to its shift by one has no carries: its central adjacent sums are
2z-10, 4v-19, 2z-8, all between 0 and 9; the other sums are at most 7.
Thus the paired formal target on the second step is exactly Phi_1(G^2(A)).
Pairing the component digits gives A', completing (2), with all outside
and seam carries accounted for.

### Safety, mass, and why the return is not recurrent

Initially Q contains the central coefficient 2v in {10,12,14}; this
excludes both exact palindrome-predecessor classes. At the intermediate
state G(Q), the flanking coefficients 2z+1 are in {13,15,17}, again excluding
both classes. This proves safety through the return for every r.

The pair masses at the three phases are exactly

    4+4z,       8z-10,       16z-56.

Both steps increase mass for z in {6,7,8}. The increase is finite; it is
not an infinite renewal theorem.

The spacer r is unchanged. The outside coefficient changes from 1 to 4,
and the returned core parameters are

    (u',v') = (4u+1,4v-19).

None of the six returned pairs is in the starting domain. Indeed u'>=5;
if v'>=5 then u'+v'>=10, and if v'<5 the lower v bound fails. Therefore
this exact gate cannot immediately be reused with its stated hypotheses.
For (u,v)=(1,5), the returned whole word has every coefficient at most 9,
so its **third positive ordinary iterate is a palindrome for every r**.
For each of the other five pairs, the returned whole word still has a
coefficient greater than 9 and different from 11, so the third iterate is
nonpalindromic. No assertion is made about all later times.

To obtain a recursive existence construction one still needs an exact
later identity that restores an eligible core and its outside context,
with an unbounded supply of a usable parameter and safety throughout the
reset. Equation (2) supplies neither growth of r nor such a reset. No
amount of repeating the present two-step statement alone establishes an
infinite safe orbit.

## 3. Checks and finite discovery scope

Run from this directory:

    python -B variable_overlap.py
    python -B delayed_overlap_gate.py

The classification checker covers every canonical component of width at
most four and every admissible shift 0,...,|A|: 1,363 whole input cases.
It also uses 3,000 deterministic longer inputs. Ordinary integer reversal
and addition independently verify the actual outputs, exact mass loss,
the iff criterion, forced unchanged shift at every closed step, and the
palindrome equivalence there.

A bounded eight-step discovery scan on that same small catalog found 336
post-departure equality records, 44 with no whole palindrome through the
recorded return. Those are finite discovery records, not recurrent-family
certificates or proof that any catalog branch is safe forever. The simpler
two-step family (2) was extracted and then proved algebraically above.

The gate checker independently verifies 396 ordinary-integer instances:
all six core parameter pairs, r=1,...,64,127,256. It checks both component
and whole updates, the exact central defect, the returned parameter word,
the failure of immediate same-domain reuse, component palindromicity at
step one, whole safety through step two, and the stated third-step outcomes.
These controls audit the implementation; the unrestricted r claim follows
from the carry proof, not extrapolation. No new Lean theorem is asserted.
