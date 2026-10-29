# W05: all-band-count three-renewal decimal interface and a new 20,000-step witness

**COMPUTED**: 264 all-band-count one-step symbolic checks, supported by the finite-residue saturation lemma below. **PAPER PROOF**: the lemma and its application to the precise symbolic segment algorithm. **COMPUTED**: independent GMP versus schoolbook 20,000-step orbit. **UNDECIDED**: infinitely many steps for any fixed decimal integer.

## Seed and the positive mechanism

All coefficients are base-19 symbols 0..9,A..I, interpreted as integers 0..18. The phase-0 rooted exterior and its spatially periodic band are

    B0 = H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D  (39 coefficients)
    W0 = H31DHBE3I12073ECF97D                     (20 coefficients)

Use the eight B/W phase rows as copied from N16's `rows.txt` in the self-contained symbolic verifier. Let `U` be forty `1` coefficients, changing `U[13]=7,U[20]=7,U[30]=6`. Define `C0=[8,0,0]++U++[16]++reverse(U)++[0,0,8]` (87 coefficients). For every integer `q>=1`, let

    P_q = B0 ++ W0^q ++ C0 ++ reverse(W0)^q ++ reverse(B0).

Construct a genuine decimal integer `N_q` of length `205+40(q-1)` by splitting each low-first pair coefficient `p` as `(min(p,9), p-min(p,9))` at opposite ends. Every `N_q` is positive with a nonzero leading digit. The 264-step conclusion is **for the actual integer orbits**: after each step `t=0..264`, the *entire* palindromic pairword has the form `B_{t mod 8} ++ W_{t mod 8}^q ++ C_t ++ reverse(W_{t mod 8})^q ++ reverse(B_{t mod 8})`, with `C_t` independent of q. The computed centre lengths are 87, 131, 175, 219 at times 0, 88, 176, 264. At each intermediate step, coefficient `B_t` has an odd entry, hence no palindromic decimal input can realize that pairword. The overflow bit is `1` at even t, `0` at odd t. This is a positive three-renewal all-q construction, stronger in quantifier scope than the original q=1..4 N18 control; it is not an infinite orbit.

## Exact all-q verifier and the saturation argument

For a palindromic pairword P, one-step reverse-and-add depends only on `P`: normalize coefficients from low to high with carry `c` (starting 0), producing digits `d_i=(P_i+c) mod 10` and next carry `floor((P_i+c)/10)`, appending carry as a new top digit if nonzero; next pairword is `d_i+d_{L-1-i}`. Every relevant 20-coefficient W and reversed W has **constant** carry-out independent of whether the incoming carry is 0 or 1 (checked against both inputs). Thus for every q>=1 the normalized digit list has an exact decomposition:

    D(q) = D_B ++ D_firstW ++ Y^(q-1) ++ D_C ++ D_firstReverseW ++ Z^(q-1) ++ D_reverseB ++ [overflow?1:empty].

All literal components and both repeating 20-blocks are computed by ordinary division/carry, without assuming an output formula. Next pairword is the pointwise sum `D(q)+reverse(D(q))`. The proposed output is `B_next ++ W_next^q ++ C_next ++ reverse(W_next)^q ++ reverse(B_next)`, where `C_next` is *deduced* from q=1 and must be palindromic, never supplied by a search.

**Finite-residue saturation lemma (PAPER PROOF).** Consider any identity between (a) the pointwise sum of two affine segmented words and (b) another affine segmented word, where every segment is either literal of fixed length or a repetition of a block of common length m, and all segment boundary slopes in parameter q are integer multiples of m. Build the finite set E of all affine `(slope,intercept)` segment endpoints across the three words, including reversed segments. Set

    Q = 2+m+max_{(a,b),(a',b') in E, a != a'} ceil(|b-b'|/|a-a'|).

If lengths agree, all q>=1 segment lengths are nonnegative and the identity holds for every integer 1<=q<=Q, then it holds for all q>=1. Proof: beyond all endpoint crossings, order of all boundaries cannot change. In any intersection of three segments, if a literal is involved, its finite overlap persists only at a fixed relative offset of all literal starts; since all slopes are multiples of m, the repeat phases also stay fixed modulo m. If all three segments repeat, their values depend only on i modulo m, and the intersection has either constant width with stable residues, or grows in increments of at least m and already contains all m residues by q=Q (the m extra units lie beyond every endpoint crossing). Every possible index-class identity has therefore already been checked by Q; no later failure can appear. This is an elementary finite reduction, not a bound on the original integer's lifetime. One can formalize its segment partition and residue argument in Lean separately; no Lean verification is claimed.

The attached `allq_renewal.py` independently derives segment endpoints and Q for every one of the 264 transitions. It tests all 1<=q<=Q with the actual symbolic normalized digits and recomputes `C_next` from q=1. The largest Q encountered is **36**, at t=263. Every one of the 264 tests passes. Because each step returns a q-independent centre and preserves q exactly, induction yields the stated all-q, 264-step property.

## Independent ordinary-integer replay

`replay.cpp` starts from the same explicit seed description, independently constructs a genuine decimal integer, and computes each step via both (a) GMP addition with independent literal decimal reversal and (b) an unrelated grade-school vector carry calculation, checking the entire integer at every iteration. It tests for any decimal palindrome and exact exterior prefix, and verifies every expected overflow. Reproduce with `sh calculation/new_structures/agent-W05/run.sh` in a checkout (requires Python3, g++, libgmpxx and libgmp). Controls:

| q | steps | seed digits | final digits | min exterior prefix | FNV64 |
|---:|---:|---:|---:|---:|---|
| 1 | 264 | 205 | 337 | 59 | dcbef01fd12242eb |
| 2 | 264 | 245 | 377 | 79 | a00b7f4c7470fd0f |
| 7 | 264 | 445 | 577 | 179 | f126cca93ccee4b4 |
| 47 | 264 | 2045 | 2177 | 979 | 64343d954a06847b |
| 230 | 20,000 | 9,365 | 19,365 | 156 | 54bb9dcae016dd03 |

The q=230 replay witnesses 20,000 decimal nonpalindromic steps with all corresponding phase prefixes containing **at least five complete 20-cell W bands** beyond the 39-cell B prefix. It does **not** exhibit a finite return of the centre and cannot be promoted to an infinite Lychrel certificate. A fourth 88-step full-band return is absent in the q=1 centre; the continuation project is to synthesize a closed centre return in this affine pumping representation rather than merely append unverified orbit time.

## Limits and scope

The all-q theorem is finite-time for exactly 264 steps and requires the specified centre and B/W data. It proves neither an all-time property of one N_q nor a fixed regular centre language. A finite q-independent macro-centre return with nonnegative band growth would be sufficient to close the gap, but no such return is asserted. All computational claims are supported by self-contained input fixtures and reproducible checks; repository-wide `tools/verify.py --changed` could not be executed in the tool container (GitHub DNS inaccessible), and no Lean source is added.
