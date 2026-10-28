# Complete one-site response kernel of the decimal period-12 lattice

**PAPER PROOF.** This theorem classifies exactly when changing one symmetric
pair of coefficients in the periodic bulk leaves the *entire* next pair word
unchanged. Unlike `Agent5P12InvisibleDefect`, this treats all twelve temporal
phases, both input-length parities, and proves the **absence** of such a
nontrivial one-site kernel at all nine non-overflow phases. It is not a
bounded-width centre exclusion, a persistence theorem for general defects, a
Lychrel certificate, or a claim about the orbit of 196.

## Scope and data

Use the existing `lat_p12m9.txt`: temporal period 12, overflow word
`100010001000`, spatial period 9, fixed exterior width `nB=34`. For a
phase `t`, construct a palindromic decimal pair word by reflecting the lower
half `B_t ++ W_t W_t ...`, with total length n large enough to have a bulk.
For odd n replace its *central* coefficient with the nearest lower even
coefficient if needed; this preserves the required pair-word parity. The
first coefficient is 1, 2, 5 or 10 and so the pair word has a canonical
decimal realization. Write `h=ceil(n/2)` and choose a site

    nB+2m <= j <= h-(m+3),    m=9,

so that there are at least two full periods separating the site from the
exterior and more than a period separating it from the centre. Put
`j'=n-1-j`, `r=(j-nB) mod 9`, and replace BOTH symmetric coefficients
`P[j]=P[j']=q=W_t[r]` by the same `q'` in 0..18. We count nontrivial
replacements `q' != q` only. The claim is independent of n and of j
apart from its phase/residue and these safe bulk margins.

## Complete table

`-` means **no** nontrivial one-site substitution preserves the next pair
word. In the following three overflow phases the original bulk rows and
the unique invisible replacements (ordered by residue 0..8) are:

| phase | W_t | replacement by residue r=0..8 |
|---|---|---|
| 0 | 5,18,4,8,1,15,4,0,5 | 14,9,13,17,10,6,13,-,14 |
| 4 | 8,1,15,4,0,5,5,18,4 | 17,10,6,13,-,14,14,9,13 |
| 8 | 4,0,5,5,18,4,8,1,15 | 13,-,14,14,9,13,17,10,6 |

For t=1,2,3,5,6,7,9,10,11, **every** residue is `-`. These are exactly
the phases with overflow bit 0. All replacements above differ by +9 or -9.

## Carry-reset lemma (all lengths)

For coefficients in 0..18 and an incoming carry c in {0,1}, the outgoing
carry is `floor((q+c)/10)`. Whenever q != 9 this carry is independent of
c: it is 0 for q<=8, and 1 for q>=10. No temporal row W_t is identically
9; its maximum cyclic run of consecutive 9s is in fact 1 (check its nine
stored values). Therefore a changed carry entering the unmodified bulk
resets after at most two columns. With the margins above, the two modified
sites and their carry-response neighborhoods are disjoint. Their incoming
carries are the same before and after the substitution, independently of
centre and exterior boundary conditions. The terminal overflow is also
unchanged since the most significant exterior coefficient is unchanged.

Let delta=q'-q, and let A and B be the change in outgoing carry at the
lower site j and upper reflected site j' respectively (each in {-1,0,1}).
The changed normalized digit at j is `delta-10A`, at j' it is
`delta-10B`. At the next cells the changes are congruent to A and B
modulo 10. A/B are small enough that a zero next-digit change *forces*
A/B=0, regardless of whether the neighboring coefficient is 9.

### Case gamma=0: no nontrivial invisible single-site change

The next pair word pairs normalized positions by the old reflection
`i <-> n-1-i`. Equality of the next paired value at `j+1` forces the
normalized digit at `j+1` to be unchanged, because its partner `j'-1`
lies before the upper perturbation and is unaffected by the lower carry
(reset lemma). Hence A=0. Similarly, equality at `j-1` forces B=0.
Equality at `j` now requires `(delta-10A)+(delta-10B)=2delta=0`, so
q'=q. Thus all nine residues at all nine non-overflow phases are excluded
for *any* bulk width, without enumeration.

### Case gamma=1: two exact linear equations

The three overflow rows W_0, W_4, W_8 have NO coefficient 9. The digit
changes are supported *only* at `j,j+1,j',j'+1` and, in that order, equal
`delta-10A, A, delta-10B, B`. Since the new reflection is
`i <-> n-i`, the next pair-word differences at j and j+1 are

    delta - 10A + B,      A + delta - 10B.

All other paired coefficients agree automatically. Both expressions vanish
**if and only if** `A=B` and `delta=9A` (subtract the equations to get
11(B-A)=0). For each r the incoming lower carry is the recorded
`C_t[r]`, and the incoming upper carry is exactly
`1{W_t[(r+1) mod 9]>=10}` because its preceding coefficient is not 9.
Thus A and B are determined by a pair of integer divisions
`floor((q+c)/10)` and `floor((q'+c)/10)`. Evaluate q'=0..18; the 3x9
finite table above is the complete solution. In particular, the q=0 cell
in each overflow row has no solution, while the other eight have exactly
one (a change by +/-9).

## Reproduction and controls

The standalone Python checker `classify_all_phase.py` reads exactly the
existing lattice data. It first verifies the overflow schedule, carry
conditions, and all 3x9 local-equation solutions. It then independently
computes ordinary pair-word normalization for **every** interior site and
all 18 alternative coefficients, for each of the 12 phases, both input
parities and lengths 400/418 (even) and 401/419 (odd). It asserts
full-next-pair-word agreement **if and only if** the table predicts it.

    python3 calculation/decimal_frontier/lattice_kinks/code/classify_all_phase.py

The all-width conclusion follows from the carry-reset lemma, not an
extrapolation from those finite test lengths. No repeated census, centre
search or new base-10 infinite orbit is claimed.