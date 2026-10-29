# AgentS12EvenCentre101Projection
**PAPER PROOF, modulo-101 structure for every even-centre rooted T* pairword, all q,k. NOT a decimal Lychrel certificate.**

Set X=B34 W9^q J U3^k C_left and P=X reverse(X), where C is
even-length palindromic. Define E(X)=sum_r(-1)^r X_(2r),
O(X)=sum_r(-1)^r X_(2r+1) mod101. Then
V(P)=9(O-E) when |X| is even and V(P)=11(E+O) when |X| is odd.
Inserting five U3 copies (15 sites) to obtain k+5 rotates the
shifted half-centre moment (E,O)->(O,-E), switching these two channels.
For U=(9,a,18-a), a even, the five copies contribute moments (a-9,a).

**Complete legal junction residue table:** at length j, the ordered
mod101 moments of J and reverse(J) attain exactly
min(101,18*ceil(j/2)+1)*min(101,18*floor(j/2)+1) classes; for j>=12
all 101^2 occur. Palindromic even centres of length c attain
min(101,9*c+1) mod101 values, all 101 for c>=12.
Modulo11 places no junction restriction for even C (R33/R07
correction); modulo9 charge matches the 120-step k->k+5 target
because sum(U)=27 (Q39). Attribution preserved.

S12 independently rederives R05's exact physical mod101
120-edge weighted-carry cocycle. Combined with the folded target,
this gives a sound 16-class (q mod4,k mod4) necessary guard.
Without the *actual physical carries* it provides no no-go.

**Reproduction:** calculation/new_structures/S12/mod101_even.py,
with genuine independent native-bigint and digit-vector
120-step controls at 20 q,k classes. Scope is the all-width
modular identities, NOT a positive 120-step physical seam return.

**Missing lemma:** exact physically rooted same-J,C 120-step
W9-preserving U3-growth cycle and all-phase nonpalindrome guard,
uniform for independently large q,k. UNDECIDED.