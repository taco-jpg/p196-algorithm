# Decimal dyadic spacetime substitution: 36 states, 16 time rows and 18 all-height safe steps

**PAPER PROOF** with strictly bounded time: all dyadic heights h>=2 have exactly checked decimal reverse-and-add steps 0..18 and explicit nonpalindrome digit witnesses; every h>=7 supports an exact binary spatial substitution with **36 types of 16-row spacetime macrotiles** in its stated interior. The finite machine is new: each type stores the entire time-dependent coefficient vector t3..t18, not just a time-15 colour. No Lean certification or infinite decimal Lychrel number is claimed.

## 1. Concrete decimal family and two-ended carry mechanics

Let `sigma(14)=(14,16)` and `sigma(16)=(16,14)`, `w_h=sigma^h(14)`, and `P_0(h)=([4]++w_h)++reverse([4]++w_h)`. These are *pair coefficients* of an actual positive decimal integer N_0(h): the least-significant digit is 0, the most-significant is 4, and all other opposing digits sum to the 14/16 coefficient (lower digit 5/7, upper digit 9). Hence N_0 is not palindromic. Earlier results prove the exact all-h initial three-step formula `P_3(h)=G_h++reverse(G_h)` with a 3-letter sliding-block coding of w_h in the bulk and fixed/finite-parity boundary corrections.

For a pairword P with coefficients in 0..18, decimal carry through a coefficient 9 transmits its incoming bit, while any coefficient !=9 fixes its outgoing bit to `[P_i>=10]`. If **no run of three consecutive 9s** occurs, carry entering a bulk cell depends only on the nearest non-9 among the preceding 1,2,3 cells. The corresponding mirror digit has an analogous carry from the other direction. Denote these carry bits `C_left(i)`, `C_right(i)` and `C_shift(i)` (the last starts at i itself). Given output-length growth bit gamma=0 or1, the exact next bulk coefficient is, respectively,

```
 gamma=0: Q_i=((P_i+C_left(i))%10)+((P_i+C_right(i))%10)
 gamma=1: Q_i=((P_i+C_left(i))%10)+((P_(i-1)+C_shift(i))%10).
```

This identity is just addition of ordinary decimal digits, including the reflected partner's one-position shift under a final carry. The centre and two exteriors are handled separately by the ordinary normalisation operation. Discarding four input coefficients from each end is sufficient for a **sound interior local transducer** with neutral-run upper bound2. This is a new reusable finite-state carry contract for an aperiodic, changing-period band.

## 2. Proving 18 decimal transitions simultaneously for all h

The genuine decimal overflow bits for t0..t17 are

```
011000010101001001
```

The coefficient words P_t(h) have neutral-9 run lengths at most2 at every *input time* t3..t17. We prove these statements for all heights, not by extrapolating a finite simulation:

- A coefficient at t3+s, 0<=s<=15, in the interior depends on a 3-letter source coding of w_h followed by s applications of the carry transducer, each needing at most four additional symbols on each side. A length-125 window of w_h suffices for all fifteen updates: source G length123, and `123-2*4*15=3` output coefficients remain at t18.
- Since 125<=128=2^7, every length-125 factor of w_h for h>=7 occurs in a concatenation of two sigma^7 single-letter blocks. It is therefore among the factors of `sigma^7(UV)` for U,V in {14,16}, exactly **376 distinct factors**. Exhaustive checking of these 376 windows tests all temporal interior carry preconditions, the full resulting labels, and every no-three-9 condition at t3..t17. This is a universal finite-language argument.
- The initial G coding requires at most three original w letters. An exterior margin 64 plus fifteen radius-four updates plus the three-letter coding is **127 original letters**, smaller than a 128-letter sigma^7 block. For h>=10, the first 128 letters of w_h always equal sigma^7(14); its last128 depend only on h parity because sigma toggles the last letter. Thus all exceptional exterior and mirrored-centre windows belong to exactly **two** classes, represented by h10 and h11. Heights h2..9 are each checked completely. The checker additionally compares two later parity controls h12,h13, without using them in the universal proof.

These obligations yield all decimal step identities and nonpalindrome witnesses by ordinary induction on t, for each arbitrary h>=2. The first opposing unequal digit pair of N_t is always within the first six positions for 1<=t<=18; `spacetime36_quotient.json` records every witness (with the two small h2 exceptions) and the entire gamma schedule. The source `spacetime36.py` implements every finite universal factor and parity-boundary check.

## 3. The exact 36-state 16-row spacetime substitution

Fix the set F of all 376 length-125 substitution factors. For any factor `f in F`, form the length123 initial third-time G segment by the explicit 3-letter coding

```
d(x,y)=2*(x+y-27)
H(x,y,z)=d(x,y)+d(y,z)-9*([d(x,y)>=10]+[d(y,z)>=10]).
```

Applying the gamma-specific radius-three carry rule with a *safe four-cell trim* for each temporal transition t3,...,t17 produces a sequence of length123,115,...,3. At each t=3+s record the coefficient at current segment index `61-4s` (zero-based). This is the **16-entry temporal vector** `Phi(f)=(Phi_3(f),...,Phi_18(f))`. It is sound for every possible real hierarchy height, since all neutral-run and boundary assumptions above were independently checked.

Define the two binary **spatial children** of a length125 factor by substituting its 125 letters and taking windows

```
S_0(f)=sigma(f)[62:187],    S_1(f)=sigma(f)[63:188].
```

The checker verifies closure: both children of every one of the 376 states lie in F. A factor of w_h centred at position c maps after applying sigma to child factors centred at positions 2c and 2c+1. Because G is shifted from w by exactly two positions and the trim is symmetric, for every h>=7 and `62<=c<=2^h-63` we have the exact 16-row identity

```
(P_t(h)[c+2] for t=3..18) = Phi(w_h[c-62:c+63]).            (1)
```

Consequently for every t in the **entire 16-time slab**, with i=c+2 and 64<=i<=2^h-61,

```
(P_t(h+1)[2i-2], P_t(h+1)[2i-1])
   = ( Phi_t(S_0(f_i)), Phi_t(S_1(f_i)) ),
f_i=w_h[i-64:i+61].                                     (2)
```

This is a genuine exact period-doubling **spacetime strip**, not an assertion that different times happen to look alike. A temporal macro-tile that can be stacked to cover *all* future times is NOT provided; the 16-row strip remains finite in the time direction.

The finite output-vector algebra has **36 distinct 16-time vectors** across all 376 factors. Crucially, these 36 vector classes are already closed under both children: all members of one class have the same output vector, left-child class and right-child class. Hence the partition refinement is **36 -> 36** and the resulting 36-state Moore quotient is minimal on the admissible factor domain. The exact full machine is in `spacetime36_quotient.json`, including each class's 16 coefficients, both children and multiplicity; `spacetime36_states.tsv` assigns each actual factor and both original children to a class.

The time3..17 sub-vectors require only **32** distinguishable states, and the new time18 component refines this to **36**. This locates an exact temporal state-split and supplies the 36-state successor alphabet for any continuation. The state split is a *positive finite refinement* in a temporal hierarchy, not an exclusion claim or an infinite-period conjecture.

## 4. Independent genuine-integer verification and reproduction

The separate `spacetime36_independent.cpp` implements plain digit-vector decimal `N+reverse(N)` arithmetic, without importing the symbolic pairword carry engine, for h=2..14 and **18 steps**. It recomputes every pairword from opposing actual digits and checks the entire real overflow word, no-palindromicity, and neutral-run bounds. At h7..14 the concrete integer pairwords are checked against the 376-state temporal labels at **506,368** site-time cells. At h7..12 it also checks **234,240** concrete next-height child labels across every time3..18, beyond mere finite substitution closure. All 376 admissible factor states actually appear in tested genuine h>=9 words; changing any source-state output label at t15 is detected against its observed integer coefficient (376 independent mutation witnesses). Original child-factor transitions and quotient consistency are independently checked in C++.

To regenerate and verify all code, tables, classes and controls from repo root:

```
sh calculation/new_structures/agent-N15/run_spacetime36.sh
```

The script checks both the all-height factor lemma and the exact committed 36-class tables bit-for-bit, compiles the independent integer implementation and asserts the actual 506,368 pairword entries. All files are under `calculation/new_structures/agent-N15/`, with no external data or packages.

## 5. Missing temporal return, without disguising a finite strip as a proof of infinity

An infinite base-10 Lychrel certificate still needs a **phase-aware temporal gluing law** on these space-time tile types, with correct length-growth, exterior carry and centre seam, and a nonpalindromic witness for every concatenated macrotime block. The present machine only gives exact closure under *spatial* doubling for 16 specific temporal rows. It does not imply the same states reproduce after another 16 rows, and it does not identify any indefinitely palindrome-free natural-number orbit. Its constructive value is an explicit, small, fully checked 36-state alphabet of nonperiodic spacetime structures in which to search for a true time-direction fixed point.
