# W11: three-state central phase synchronizer for bivariate packets

**PAPER PROOF** (base-independent conditional phase theorem for the exact formal four-corner recurrence). **COMPUTED** (base-10 first 20,000 symbolic steps, plus genuinely independent b-ary ordinary-integer controls). This is not a base-10 infinite orbit certificate.

## Definitions and finite-edge precondition

In base b>=2, let len(M) be the ordinary base-b digit length of positive M and R(M) its reversal with leading zeroes discarded. A formal four-corner state is the coefficient array (C,M1,M2,A), offset array (s0,s1,s2,s3) and independent symbolic exponents (q2, q1=q2+delta). It represents `C*b^s0 + M1*b^(q2+s1) + M2*b^(q1+s2) + A*b^(q1+q2+s3)`. Offsets may be negative provided q2,delta make all actual exponents nonnegative. The standard exact polynomial packet step reflects corner j into 3-j with reflected offset `E-sj-len(pj)`, `E=s3+len(A)`, and adds the two terms after choosing their smaller offset. This is the true reverse-add edge **only while the four support intervals are disjoint**. Outside that domain it remains a well-defined algebraic formal recurrence, not necessarily the actual integer orbit.

Assume the canonical outer offset s0=0, C>0, A>0 and synchronized middle corners M1=M2=M>0, s1=s2=s. The canonical condition is preserved: reflection of the top A starts at offset zero and the existing bottom starts at zero. Define the central phase `theta=E-2*s-len(M)` and the guard `G(theta,M): theta in {-1,0,1} and (theta != 1 or M mod b != 0)`.

## Theorem: G is an invariant of the formal recurrence

**PAPER PROOF.** The two synchronized middle corners have exactly the same two summands under the packet step, so the updated packets and offsets remain identical. The new top is the sum of the previous top contribution and the reversed bottom contribution, each fitting within the previous overall E-column extent (the bottom begins at zero); the previous top has an E-digit leading extent. Thus the top extent changes by gamma=E'-E in {0,1}.

For theta=-1: new middle packet `M'=b*M+R(M)`, new offset `s'=s-1`. Since b*M has len(M)+1 digits and R(M)<b^len(M), new length is `len(M')=len(M)+1+c`, c in {0,1}. Its units digit is the nonzero leading digit of M.

For theta=0: `M'=M+R(M)`, s'=s; its length is `len(M)+c`, c in {0,1}. If M' has zero units digit, the first and last digits of M sum to b (otherwise the units digit cannot be zero); the leading column therefore carries out, hence c=1.

For theta=1, the guard ensures M has nonzero units digit and hence R(M) has full length len(M). Then `M'=M+b*R(M)`, s'=s, `len(M')=len(M)+1+c`, c in {0,1}; its units digit is the nonzero units digit of M.

In **all three cases**, exact substitution gives `theta'=gamma-c in {-1,0,1}`. If theta'=1 then gamma=1 and c=0; in the theta=0 case the preceding zero-units implication rules out M' ending in zero, and in the other two cases M' already has nonzero units digit. So the guard holds inductively **for every formal iterate**, with **no bound on len(M)**. This theorem holds for every base b>=2 and does not claim that a fixed finite q2,delta keeps packet supports separated forever.

## Seed and computed verification

For base 10, begin with (C,M1,M2,A)=(75,3,0,88) and offsets (0,2,0,3). At t=1 the state becomes (163,3,3,145), same middle offsets s1=s2=2; E=6, len(M)=1, theta=1 and M mod 10=3. The theorem applies to all later formal iterates. The independent `four_corner_replay.cpp` from W11's preceding commit already replays these edges as actual decimal reverse-add through 20,000 steps for q2=delta=14000, with full GMP controls.

The standalone `phase_synchronizer.cpp` checks exact middle update equations, both digit-length carry bits, the phase recurrence and nonzero-units guard on t=1..20000. Counts: theta=-1: 1849 states; theta=0: 12578; theta=1: 5573. Of these 20,000 states, 471 have middle units digit zero, **none** when theta=1. Final middle length: 11953 digits. All 19,999 phase edges have `theta'=gamma-c`; exact edge-count table stored in `phase_transitions.txt`. A deliberately invalid guard at theta=1, M=10 is rejected.

The **independent** standard-library Python `phase_base_controls.py` does not import the C++ checker: in bases 2,3,4,9,10,13,16,26 it compares the corner recurrence with full ordinary-integer reverse-and-add on all 90 steps and independently checks the synchronized phase guard. Every control passes, including states with trailing-zero middle packets.

Reproduce from repository root:
```
g++ -O2 -std=c++17 calculation/new_structures/agent-W11/phase_synchronizer.cpp -lgmpxx -lgmp -o /tmp/w11_phase
/tmp/w11_phase 20000
! /tmp/w11_phase 10 --bad-guard
python3 calculation/new_structures/agent-W11/phase_base_controls.py
```
Compare first program output to `calculation/new_structures/agent-W11/phase_transitions.txt`.

## Why this matters and remaining gap

The full, unbounded decimal middle packet does **not** require an expanding phase alphabet: a three-state clock and one units-digit guard suffice, even though packet length reaches 11,953 digits by t=20,000. This is an exact simplification for future finite-state regenerative central templates. It does not force positive drift of either spatial gap. An actual infinite base-10 Lychrel certificate still requires a renewed, all-time separated exterior or another sound treatment of collided packets. A possible Lean theorem factors this statement into the four-corner reflection lemma, `gamma <= 1`, three digit-length cases, and the guard preservation induction; no Lean code or LEAN-VERIFIED claim is supplied.
