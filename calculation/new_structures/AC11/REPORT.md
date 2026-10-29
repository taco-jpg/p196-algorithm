# AC11: phase-2 p12/m9 short-junction endpoint-only obstruction

**Label: COMPUTED** (exhaustive 4,115,400 J/U census with centre-independent two-carry prefix argument). **Not Lean-verified; not a decimal Lychrel certificate.**

## Exact predicate

For the rooted phase-2 lattice, B2=(2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11), W2=(1,10,8,5,9,16,0,9,11). Take a symmetric LSD-first coefficient pairword B2 ++ W2^14 ++ J ++ U^k ++ C ++ reverse(B2 ++ W2^14 ++ J ++ U^k), with J of length 3 or 4 over coefficients 0..18, U any of the 30 rotations of (9,a,18-a) for a=0,2,...,18, k>=48 and **any physically realizable palindromic centre C** of either parity. An endpoint with identical q=14 W9 prefix after 120 genuine decimal reverse-and-add steps is necessary for a stationary same-J T(q,k)->T(q,k+5) return.

**EXHAUSTED-NONE:** Each of 30*(19^3+19^4)=4,115,400 J/U choices has a proven centre-independent W9-prefix mismatch at zero-indexed pairword coefficient 135..149, strictly before the W9 cut 160. All 120 overflow events follow the phase-2 clock, sum=30, and every final certified prefix has length >=172. None is unresolved. J3/U=205,770; J4/U=3,909,630.

First-mismatch histogram: 135:84723, 136:668658, 137:1816359, 138:1174774, 139:226099, 140:124436, 141:9377, 142:9129, 144:1575, 145:107, 146:84, 147:70, 148:6, 149:3. Five disjoint base-19 junction code ranges [0,27436), [27436,54872), [54872,82308), [82308,109744), [109744,137180) yielded 823,080 tests apiece, invalid=unresolved=0 in every range.

## Centre-independent carry-prefix argument

Every actual digit vector d defines a symmetric coefficient pairword p[i]=d[i]+d[L-1-i] (0<=p[i]<=18). One genuine reverse-and-add step evolves p to pair(normalize_base10(p)). If the outermost n coefficients p[0:n] are known, the unknown incoming high-side carry from the interior is 0 or 1. Scan from index n-1 inward until the first p[r]!=9. At this index, floor((p[r]+c)/10) is independent of c in {0,1}. Therefore all high normalized digits for j<r and the final overflow gamma are *exact*, irrespective of the centre. The low normalized digits are exact from carry zero. The next symmetric coefficient pairword has a known prefix of length r when gamma=0 or length r+1 when gamma=1. This propagator is endpoint-only: it **never** requires W9 matching at intermediate times. Starting with B2 ++ W2^14 ++ J ++ U^48, it certifies at least 172 endpoint coefficients after 120 steps, enough to witness each mismatch before cut 160.

Thus the result applies for **q=14 and every k>=48, all physically realizable C**. A universal q>=14 extension would require separately validating the T12 protected-cut lift; it is not asserted.

## Reproduction and checks

Compile: \`g++ -O3 -std=c++17 calculation/new_structures/AC11/census.cpp -o /tmp/ac11\`. Run: \`/tmp/ac11 0 137180\` (or five disjoint ranges above). Independent control: \`python3 calculation/new_structures/AC11/independent_verify.py\`.

The C++ check includes no strict-phase pruning; each of 4,115,400 candidate junction/U combinations is tested. An independent Python two-seed implementation agreed with the optimized last-non-nine carry reset for 500 random examples x120=60,000 transitions. 168 physical Python big-integer controls passed 120 steps each, with independent schoolbook normalization and two palindromic-centre parities: 120 controls at q=14,k=100 plus 48 at (q,k)=(20,80),(40,160),(80,320),(160,640). These larger-width checks validate implementation but do not prove a symbolic all-q lift.

**Missing all-time lemma:** construction of a moving/growing seam or an exactly recurrent epoch junction with W9 replenishment. The result is only a no-go for the stationary J3/J4 phase-2 reference-width class. No decimal Lychrel number has been proved.