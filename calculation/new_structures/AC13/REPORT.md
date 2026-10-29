# AC13 phase-4 short-junction physical endpoint lemma

**COMPUTED, not LEAN-VERIFIED.** Exhaustive finite J/U enumeration combined
with a centre-independent, k-uniform carry-prefix lemma. This is NOT a
base-10 Lychrel certificate, and does not decide the general problem.

**Exact result.** At rooted phase p=4, take B4 (length 34) and W4 (length
9) from decimal_frontier/lattice_kinks/data/lat_p12m9.txt. Write
H=B4 ++ W4^14 ++ J ++ U^k and P=H ++ C ++ reverse(H), with
|J|=3 or 4, every J coefficient 0..18, U one of all 30 cyclic rotations
of (9,a,18-a) for even a=0,2,...,18, k>=50, and C any physically
realizable palindromic coefficient centre (odd/even lengths included).
For every such P, the pairword after 120 genuine decimal n+reverse(n)
steps differs in the first 160 positions from B4 ++ W4^14. Thus the
same-J/C, q-fixed T* return P(14,k)->P(14,k+5) is impossible.

**Soundness lemma (PAPER proof of reduction).** If a symmetric pairword
P_i=d_i+d_{N-1-i} has known outer prefix p of length L with N>=2L,
its upper L coefficients are reverse(p). Normalizing P in base 10
exactly computes n+reverse(n). Each carry is 0 or 1 because coefficients
are 0..18. The lower L normalized digits follow from p with initial
carry 0. The upper L follow from reverse(p) with an *unknown* incoming
carry, exhaustively 0 or 1. For each carry choice compute the upper
digits, final length-overflow gamma, and correct shifted mirror pairing
if gamma=1. The longest common prefix of the two candidate next
pairwords is guaranteed to equal the actual next pairword's prefix.
Induct over 120 steps. This does NOT impose W9 at intermediate steps.
At k>=50 the initial known prefix
B4 ++ W4^14 ++ J ++ U^50 is independent of all further U copies
and of the centre C. The full pairword is long enough at each step to
keep upper and lower known segments disjoint. Hence a mismatch in the
certified final prefix is a rejection for *every* centre and every
k>=50, not an extrapolation from samples.

**Exact enumeration.** 30*(19^3+19^4)=4,115,400 cases;
4,115,400 conclusively rejected, 0 undecided, 0 ambiguous
step-overflow results; final certified prefix length 183..199,
first mismatch LSD-first index 134..151, always strictly before 160.
No strict-W9 phasewise MDD or odd-centre mod-11 pruning used.
The search has only one J/U instance per choice, and covers
infinitely many C/k by the independently justified prefix lemma.
Per-rotation exact result can be reproduced with index 0..29.

**Reproduction:**

    g++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/new_structures/AC13/exhaust.cpp -o /tmp/ac13_exhaust
    /tmp/ac13_exhaust 50
    python3 calculation/new_structures/AC13/independent_verify.py 30

The first command's full run returns
total=4115400 proved=4115400 unresolved=0 gamma_ambiguous=0
minretained=183 maxretained=199 mindiff=134 maxdiff=151.
Independent Python bigint verification uses a genuine decimal
source integer and 120 full n+reverse(n) iterations on each
30 U controls, each at (q,k)=(14,100),(20,100),(40,160),
(80,320),(160,640), with alternating even/odd centres.
The 150 big-int controls test the computation; the lemma, not
the controls, supplies centre/k universality. Additional 60
q=14 bigint controls covered both centre parities for all U.

**Exact missing-lemma contribution, in one sentence:** a sound
centre-independent physical-return obstruction decides every
phase-4 |J|=3/4, all-30-U fixed-seam T* candidate at q=14
uniformly for k>=50, without unsound strict-W9 pruning.

**Limitations:** q=14 only; the T12 lift to other q is NOT asserted.
Longer/moving J, q-changing edges and alternative phases remain open.
This negative cell is not a proof that any decimal Lychrel number exists.
