# Q09 rooted period-8 symmetry rigidity: arbitrary centres

**PAPER PROOF.** Base 10 only, for the published first p8/m20 rooted exterior at time zero. The result covers EVERY palindromic centre of ANY nonnegative length, not only sampled widths; it concerns the exact state-conditioned carry-preserving letterwise symmetry class defined below. It does not exclude position-dependent relabelings, carry-flipping seams, or exterior-changing repairs.

Let B be the following least-significant-first 39 coefficients, the first temporal column of the first `SCC p=8 g=10101010 ... depth=39` in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`:

    B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13].

For ANY palindromic word C over 0..18 (empty permitted), define the palindromic pair-coefficient word P=B++C++reverse(B). Let c_i be the carry entering index i in normalizing P from initial carry c_0=0, using T(p,c)=((p+c)%10, floor((p+c)/10)).

**Extended local symmetry class.** Fix a permutation pi of decimal output digits. For each incoming carry c=0,1, independently permit a bijection a_c of coefficient digits 0..18. Require, for EVERY p and c,

    T(a_c(p), c) = (pi(first T(p,c)), second T(p,c)).

Then such bijections exist (and are uniquely determined by pi) iff pi(0)=0 and pi(9)=9, with the remaining eight digits freely permuted: 8!=40320 possible pi.

**Reason.** For a fixed input carry 0, the map p -> T(p,0) is a bijection onto the 20 output digit/carry pairs except (9,1); for input carry 1, its image omits only (0,0). A digit permutation preserving output carry must preserve each missing pair, i.e. fix pi(9)=9 and pi(0)=0. In that case define a_c by conjugating the digit permutation through the bijection p -> T(p,c). This construction is necessary and sufficient.

**Mirroring constraint.** If the transformed word Q_i=a_{c_i}(P_i) is again a palindromic pair-coefficient word, then whenever c_i differs from c_{L-1-i}, a_0(P_i)=a_1(P_i). Writing r=P_i%10 with 0<=r<=8, the definition of a_c gives

    a_0(P_i)=pi(r)+10*floor(P_i/10),
    a_1(P_i)=pi(r+1)+10*floor(P_i/10)-1.

Thus each such mirrored carry mismatch forces pi(r+1)=pi(r)+1. (At r=9 the equality is automatic because pi(9)=9 and pi(0)=0.)

**Seven centre-independent witnesses.** The following input carries at mirrored positions are fixed, regardless of C:

| low index i | B_i | B_i mod 10 | carry c_i | carry c_(L-1-i) |
|--:|--:|--:|--:|--:|
| 1 | 5  | 5 | 1 | 0 |
| 3 | 1  | 1 | 0 | 1 |
| 6 | 14 | 4 | 0 | 1 |
| 7 | 12 | 2 | 1 | 0 |
| 14| 17 | 7 | 1 | 0 |
| 29| 13 | 3 | 0 | 1 |
| 30| 18 | 8 | 1 | 0 |

The low-side values follow by processing B from carry0. The first coefficient of reverse(B) is B_38=13, which sends BOTH possible entering carries to outgoing carry1. All listed mirrored high positions occur at least eight positions into reverse(B), so their carry inputs depend only on fixed B, not on the centre, and direct seven-index carry arithmetic gives the table.

The witnesses enforce pi(r+1)=pi(r)+1 for each r in {1,2,3,4,5,7,8}. Since pi(9)=9, constraints for 7,8 force pi(8)=8 and pi(7)=7. Constraints for 1,2,3,4,5 force pi(1),...,pi(6) to be six consecutive increasing integers. By bijectivity and fixed values at 0,7,8,9, these six integers must be 1,...,6, so pi is identity. The unique a_0,a_1 are then identity as well. Q=P.

**All-centre no-go theorem.** For EVERY palindrome C over 0..18 and EVERY carry-preserving universal state-conditioned symmetry (pi,a_0,a_1) as defined above, if Q_i=a_{c_i}(P_i) is palindromic, the symmetry is identity. In particular no NONTRIVIAL fixed-digit-permutation, carry-preserving phase quotient can close a positive-growth cycle while retaining B as its mirrored rooted exterior, irrespective of centre width. The ONLY ways around this particular necessary condition include changing B, changing the phase map with position, relaxing universality to a restricted alphabet, or adding a carry-inverting junction.

This obstruction is a strict extension of `AgentQ09CarryPortCentralizer` (which assumed a_0=a_1). It is a conditional rigidity theorem, **NOT** a proof that decimal Lychrel numbers exist or fail to exist.

**Verification:** `python3 calculation/new_structures/Q09/rigidity.py`. This computes seven low/high carries for varied physical integer examples at centre widths 20,40,80,160, checks all 40320 pi at the seven local constraints, and independently tests full integer pairword realizations and a nontrivial state-conditioned dual on each width. The mathematical all-centre quantifier follows from the carry-reset proof, not extrapolation from the finite tests.

**Remaining all-time lemma:** construct a canonical decimal positive-growth finite edge cycle whose repair changes the exterior or realizes a regenerated carry-inverting or genuinely position-dependent seam. None is exhibited here.
