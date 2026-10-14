# Constructive return investigation

No finite decimal Lychrel witness or all-time closed construction was found.
This branch investigated mixed periodic interiors and, after those failed,
delayed wall repair through an interval allowed to leave residue balance.

## A genuine delayed repair, with no repeated renewal yet

Write G for the exact finite decimal pair-sum update and F for the
unconditional anti-complement wall update from the existing notes. For m>=1,
put C=6m+3 and

    V_m = 1 · 9^(2m-1) · (8,2) · 9^(2m-1)
          · (16,10) · 9^(2m-1) · 17,
    Q_m = V_m reverse(V_m) = Delta_C(V_m).

The previous ninth-step obstruction does not prevent every delayed return.
The following exact identity holds for every m>=2:

    G^10(Q_m) = Delta_C(F^10(V_m)).

Thus the ninth update loses balance, but the tenth update restores balance
at the old C. For m>=4 the returned wall is

    (5,5,6,3,16,17) · 18^(2m-7)
    · (17,16,15,6,1,12) · 9^(2m-4)
    · (6,17,12,3,2,1) · 0^(2m-7)
    · (1,2,15,12,13,13).

It has width C+3 and is anti-complementary. The separate finite cases m=2,3
also obey the return identity.

At time nine, the actual pair-sum word differs from the signed wall
difference only by

    0^C · (-1,20,-1) · 0^C.

The respective central triples are (3,14,3) and (4,-6,4). A zero carry
enters either triple (the preceding coefficient is 7), and both leave zero
carry. Their normalized digit triples are respectively (3,4,4) and
(4,4,3). These are reversals, so they have the same next mirrored sums,
namely (7,8,7). The identical surrounding digit columns are unaffected.
This explains the repair directly.

The symbolic checker uses affine run lengths with m=k+4, for every k>=0;
it checks all ten updates as exact identities rather than extrapolating
from samples. It also checks safety through step eleven. Cases m=2,3 are
separate exact integer calculations; 737 ordinary-integer transitions
provide independent implementation controls.

This does not give a recurrent growing family. Step eleven has length
2C+3 and coefficient sum 18(C+3), but central coefficient 16. The only
possible balanced parameter is D=C+3. The central residue is a singleton
modulo D, so balance would require 18 there. Hence balance is lost again.
The returned wall is not another V_m, and C has not increased.

The variable-time discovery scan allowed arbitrary unbalanced intermediate
states and ran through 24m+128 updates for m=1,...,64,96,128,192,256.
It found exactly the step-ten balanced return above for every m>=2 and no
other balanced returns within those bounds. Its 74,752 steps found no
palindrome, which is only bounded evidence. No equation of the required
form G^tau(m)(Q_m)=Q_f(m), with f(m)>m and a repeatable finite seed, was found.
No coupled defect/front construction regenerating increasing digit mass
has been established.

Reproduction:

    python main_existence_attempt/constructive/delayed_repair_identity.py
    python main_existence_attempt/constructive/delayed_scale_probe.py

## Exact scope of the mixed-block obstruction

For each specified macro clock, a candidate alphabet consists of distinct
three-symbol q blocks, each returning to itself when repeated periodically.
The proposed nonperiodic interior allows every finite concatenation of
alphabet blocks. A necessary condition is that cyclic words AB, AAB, ABB
map back to concatenations of blocks in the same alphabet.

For the eleven-step clock (1,1,0,0,0,1,0,0,0,0,1) repeated three times,
there are 15 eligible motifs. For the alternating 24-step clock there are
209, including the all-nine motif with every possible carry branch.
No alphabet of size >=2 satisfies those necessary conditions. A solver-free
closure certificate exhausts all 105 and 21,736 initial motif pairs,
respectively. Its forced additions number 2 and 1,995; no branching is
needed. A separate finite-set replay checks every implication and rejection.

These are exclusions of freely concatenable, individually recurrent
period-three alphabets under the two stated clocks. They do not exclude
correlated block languages, other clocks, growing return times, general
morphic families, or decimal Lychrel numbers. Additional two-block discovery
scans at periods 72 and 132 also found no code, but were not extended to an
arbitrary-alphabet certificate.

Reproduction:

    python main_existence_attempt/constructive/bulk_mixture.py
    python main_existence_attempt/constructive/mixed_alphabet_search.py
    python main_existence_attempt/constructive/alphabet_closure_certificate.py

The scripts use exact integer column arithmetic. Their concrete graph and
run certificates have not been instantiated as Lean theorems.
