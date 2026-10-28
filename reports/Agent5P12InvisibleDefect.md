# A decimal period-12 lattice has unbounded one-step apparent defect speed

**PAPER PROOF.** This is a counterexample to an *unconditional*, uniform
upper bound for the one-step advance of the first difference between an
actual pair word and the period-12, spatial-period-9 bulk lattice. It is
**not** a persistent-defect argument, a centre, a certificate, an all-width
exclusion, or a claim about 196. The period-8 K2 task is separate.

## Data and family

Use the repository's `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`:
base 10; temporal period `p=12`; exterior width 34; lattice period `m=9`;
`g=100010001000`. At phases 0 and 1 the bulk rows are

```
W0 = [5,18,4,8,1,15,4,0,5]
W1 = [10,14,13,12,9,7,10,4,5]
C0 = [0,0,1,0,0,0,1,0,0]  (incoming ascending carry)
```

For every `k>=0`, let `n=400+18k`, `h=n/2=200+9k` and form the palindromic
pair word `P` by reflecting the lower half `P[x]=B0[x]` for `x<34`,
`P[x]=W0[(x-34) mod 9]` for `34<=x<h`. Its entries lie in `0..18`,
its first and last coefficients are 10, and it is realized by a canonical
decimal integer: for every `x<h`, choose digit `d[x]=min(P[x],9)` and
`d[n-1-x]=P[x]-d[x]`, which makes the most significant digit 1.

Let `T(P)` mean carry-normalize `P` in base 10 to digits `O`, append a leading
carry if present, and take the reflected digit sums of `O`. Since the two
outermost pair coefficients are 10, `O` has length `n+1`: `g_0=1`.
Thus `T(P)[x]=O[x]+O[n-x]`.

## Exact next-lattice agreement for every k

The exterior values `T(P)[0..33]` equal published `B1[0..33]`. This finite
34-position check is included in the reproducer. For an interior position
`34<=x<h`, write `r=(x-34) mod 9`; the lattice row contains no coefficient
9, so incoming carries depend only on the preceding coefficient. The
successor coefficient is exactly

```
T(P)[x] = (W0[r]+C0[r]) mod 10
          + (W0[(r-1) mod 9] + (W0[r]>=10)) mod 10.
```

For residues `r=0..8` the right side is respectively
`10,14,13,12,9,7,10,4,5`, exactly `W1`. At the new odd centre `x=h`,
`T(P)[h]=2*(W0[3] mod 10)=16`, while `W1[(h-34) mod 9]=W1[4]=9`.
Therefore the **first** difference of `T(P)` from the time-1 exterior
is exactly `h`, irrespective of k. The new central difference is permitted;
no periodic-centre closure is claimed.

## Eight invisible local defects and their arithmetic

For `35<=j<=h-3`, put `r=(j-34) mod 9`. The following substitutions of both
`P[j]` and `P[n-1-j]` preserve **the entire** next pair word `T(P)`:

| r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| old | 5 | 18 | 4 | 8 | 1 | 15 | 4 | 0 | 5 |
| replacement | 14 | 9 | 13 | 17 | 10 | 6 | 13 | none | 14 |

For the eight applicable residues, the coefficient change is `+9` or `-9`
and flips the carry leaving both modified coefficients. The normalized
digit differences at `j,j+1,n-1-j,n-j` are, for `r=1,5`,
`(+1,-1,+1,-1)`; for the other six residues,
`(-1,+1,-1,+1)`. Since `g=1`, the reflected index of `j` is `n-j`;
changes at `j,n-j` cancel, as do those at `j+1,n-1-j`.
No further normalized digit changes occur because the next coefficients
are different from 9 and so reset the carry; hence the **whole** next
pair word is identical, not just a prefix.

Choose the fixed bulk site `j=35`, which has residue 1 and substitutes
`18 -> 9`. The modified pair word first differs from its lattice at
`j=35`, but its successor equals `T(P)` and first differs from the next
lattice at `h=200+9k`. Thus its apparent defect front advances by
`h-j=165+9k` positions in a single step. Given any constant c, choosing
`k>(c-165)/9` violates that bound. This is an exact all-k paper argument,
not an extrapolation from a finite number of runs.

## Independent controls and reproduction

`reproduce_wall_jump.py` reads the original lattice data and verifies all
nine interior residue equations, all applicable bulk sites at `n=400`,
finite exterior and centre comparisons, carry cancellations, and independent
schoolbook reverse-and-add digit arithmetic at lengths
`400,418,436,454,580,850,2200,18400`.

The existing published width-8 p12/m9 SAT horizons, last SAT `33,36,32`
and first UNSAT `34,37,33` for phase classes `0,1,2`, were independently
reproduced locally via QF_BV Z3 and a 36-case tiny-width enumerator control.
These are existing results, **not** re-committed as novel computations.

Run from the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/code/reproduce_wall_jump.py
```

No other bases, other temporal phases, persistent centre, or infinite
non-palindromic orbit is asserted.