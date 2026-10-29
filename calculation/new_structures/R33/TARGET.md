# R33 exact target and parity-complete missing gate

Goal (UNDECIDED): Find genuinely canonical rooted p12/m9 decimal pairwords
P(q,k)=H(q,k) C rev(H(q,k)), H=B34 W9^q J U3^k, whose complete
120-step reverse-and-add image is P(q,k+5) for ALL independent
q,k>=threshold, with every intermediate integer nonpalindromic, fixed
exterior exponent q, complete physical carry/overflow, and a nondepleting
interface. A finite replay is NOT a certificate.

RED-TEAM PAPER PROOF (parity-specific prerequisite):
Write A(X)=sum_i(-1)^i X_i, indices least significant first.
For any palindromic centre C, h=|H|, c=|C|,
 A(H C rev(H)) = 0 when c is even;
 A(H C rev(H)) = 2A(H)+(-1)^h A(C) when c is odd.
In the even case A(C)=0 automatically; there is NO nontrivial mod-11
restriction on J or U arising from the endpoint coefficient word.
For the published B34 and W9, A(B34)=-11 and A(W9)=-22.
For odd c, all independent q,k mod-11 zero constraints ARE equivalent
to Q39's two equations A(U)=A(C) and
2A(J)+(-1)^|J| A(C)=0 (mod 11).
Those two equations cannot be applied without the odd-c hypothesis.

Why the mod-11 zero condition matters: any even-digit decimal N has
N+rev(N) divisible by 11. Odd-centre P has odd length, with B[0]=10
so N1 has even length; N2 is therefore 0 modulo 11. For any exact,
repeatable 120-edge return (which shifts the exponent by +5),
N121 is 0 modulo 11, and uniformity in all sufficiently large k
propagates the zero condition back to P(q,k). With even c the same
zero condition is automatic from N0's even length.

Finite controls closing THIS audit (not the all-time existence problem):
  python3 calculation/new_structures/R33/audit.py
The script tests parity algebra, all 12 exterior two-sided gates,
90 temporal-period-10 inner words, and genuine integer/digit-list
120-step overflow at q=k=20,40,80,160. It does not prove a regenerative
seam; that exact return remains the missing all-time lemma.
