# AC32: phase-11 length-five odd-centre necessary-return obstruction

**Label: COMPUTED.** This is **not** a decimal Lychrel certificate, nor an unrestricted phase-11 or even-centre endpoint census.

**Exact conditional no-go lemma.** For rooted p12/m9 phase 11, |J|=5, any of 30 charge-zero U3 rotations, and fixed palindromic C=[4,14,4], there is no exact 120-step decimal return P(q,k)->P(q,k+5) with unchanged B11,W11,J,U,C for *all* independently sufficiently large q,k **provided the team's T12 protected-cut/reset-cone lemma reduces any such return to (q,k)=(14,100)**. The result does not independently establish the T12 premises.

**PAPER PROOF, all-width necessary gate:** Let A(X)=sum (-1)^i X_i, LSD first. At phase 11 A(B11)=6, A(W11)=-12, A(C)=-6 (phase-0 values are not interchangeable). For odd C, direct concatenation gives
`A(P(q,k))=2A(B)+2(q mod 2)A(W)+2(-1)^q A(J)-2(-1)^q(k mod 2)A(U)-(-1)^(q+k)A(C)`.
The four parity cases are `18+2A(J)`, `-18-2A(J)`, `6+2A(J)-2A(U)`, `-6-2A(J)+2A(U)`. Uniform returning P(q,k+5) must vanish mod 11 in all four parities: a canonical rooted orbit with the required overflow clock encounters an even-digit source, whose next reverse-add value is divisible by 11, and every subsequent value remains divisible by 11. Thus **A(J)=2 (mod 11), A(U)=5 (mod 11)**. Exactly U=[9,0,18] or [18,0,9] survive. Digit DP counts exactly **225,117** of 19^5 J with the required residue. Thus 450,234 of 74,282,970 odd-centre all-width candidates survive this *necessary* gate. The other 73,832,736 are rejected by the uniform parity requirement, **not** by finite-reference replay.

**COMPUTED exhaustive reference-width check, over only those 450,234 survivors:** Genuine 120-step decimal digit arrays, canonical physical source, endpoint-only comparison, no strict-per-phase W9 pruning. At q=14,k=100, all 450,234 fail before W9 cut index 160; **0 endpoint returns, 0 W9-prefix survivors, 0 endpoint length mismatches**. First differing coefficient index histogram, at t=120, LSD first:

|Index|Count|Index|Count|
|---:|---:|---:|---:|
|135|3779|136|25725|
|137|54515|138|287194|
|139|41758|140|18750|
|141|14973|142|2195|
|143|1047|144|115|
|145|151|146|3|
|147|21|148|8|

Histogram totals 450,234. It is by endpoint coefficient **position**, not per-temporal-step survivor count. Reference-only endpoint outcomes for the 73,832,736 eliminated by the all-width gate were **not** replayed; even C=[4,4] also remains **UNDECIDED**.

**Reproduction:**
`python3 calculation/new_structures/AC32/mod11_gate.py`
`g++ -O3 -std=c++17 calculation/new_structures/AC32/census.cpp -o /tmp/ac32`
`/tmp/ac32 14 100 148565940 0 1` (last flag = sound *all-width* odd-C gate)
`python3 calculation/new_structures/AC32/verify.py`

Independent Python unbounded-integer and separate digit-array engines agreed on **every** one of 120 steps in 20 cases: four J/U/C examples at q,k=(14,100),(20,20),(40,40),(80,80),(160,160). Additionally 45 randomized reference tuples were matched to the compiled engine via a separate local Python digit-array implementation. No positive all-time certificate is claimed. A carry-correct, endpoint-only finite-state automaton or exhaustive even-centre search remains necessary.
