# Q04: exact two-width pumping lemma and rooted decimal rec2 carry gate

**PAPER PROOF.** No base-ten Lychrel orbit is proved. This is an all-symbolic-width, one-step NECESSARY CONDITION for a physical centre return, not a finite-horizon result.

## Schoolbook and two-ended carry setup

Let b>=2 and let P_m = B W^m C reverse(W)^m reverse(B) be a valid palindromic *pair-coefficient* word, with 0<=coeff<=2b-2, B nonempty and W nonempty. Pair sums specify N+reverse_b(N) uniquely, irrespective of digit realizations. Write H=B W^m. Let u in {0,1} be the true carry leaving the centre C and entering the high reflected copies. For positions i in H, ascending carries a_0=0, a_(i+1)=floor((H_i+a_i)/b). Descending carries d_|H|=u and d_i=floor((H_i+d_(i+1))/b). Let gamma=d_0 be the output overflow, l_i=(H_i+a_i) mod b, h_i=(H_i+d_(i+1)) mod b. Ordinary digit normalization gives the successor folded prefix F_m of length |H|:

If gamma=0: F_m[i]=l_i+h_i.
If gamma=1: F_m[0]=l_0+1 and F_m[i]=l_i+h_(i-1) for i>0.

No high bit is chosen freely for a real centre; its actual u is determined by normalizing the complete P_m. The conditional formula holds for either proposed u and can therefore filter physical centres.

## Universal exact finite-width reduction

For 0<=x<=2b-2, the bit-carry map f_x(c)=floor((x+c)/b) is the identity for x=b-1, constant zero for x<=b-2, or constant one for x>=b. Every full block W induces f_W in {identity,reset-0,reset-1}; therefore f_W^m=f_W for all m>=1. The reflected reverse(W) block has the same property.

Thus the low carry at the centre, after B W^m, is constant for m>=1, so for any fixed C its actual departing upper carry u is also independent of m>=1. For a fixed u, within the first ascending W copy the carry trace is fixed; all following ascending copies have the same trace. Descending from u, the final W copy has its own fixed trace; all preceding W copies have the same trace. The B cap's low/high traces and gamma are likewise independent of m. At gamma=1, the upper-digit partner is displaced by one cell, so it mixes only adjacent copies: the first, interior and last copy still have fixed output. In symbols there exist fixed A,X,Y,Z, lengths |B|, |W|, |W|, |W|, such that for ALL m>=2:

F_m = A concatenated X concatenated Y^(m-2) concatenated Z.

For m=2 the output determines A,X,Z; at m=3 it determines the middle Y. Therefore for any prescribed next exterior B' and spatial block W' of the same lengths,

(for all m>=2: F_m=B'(W')^m) iff (F_2=B'(W')^2 and F_3=B'(W')^3).

Check m=1 independently. This implication is exact for unbounded m, not extrapolation from numerical samples.

## Concrete decimal p8/m48 corollary

Use the physically rooted phase arrays in calculation/decimal_frontier/lattice_kinks/data/lat2.txt, with eight phases, outer B_t length 11, repeated W_t length 48, and expected overflow g=10101010. Compute F_m from the exact normalization above, for each phase and u=0,1, and test the next protected prefix B_(t+1) W_(t+1)^m at m=1,2,3. All cases have expected gamma; the truth values agree at these three widths. The theorem extends the calculation to ALL integers m>=1.

Phase 0: allowed upper u={0,1}.
Phase 1: allowed upper u={0}.
Phase 2: allowed upper u={0,1}.
Phase 3: allowed upper u={1}.
Phase 4: allowed upper u={0,1}.
Phase 5: allowed upper u={1}.
Phase 6: allowed upper u={0,1}.
Phase 7: allowed upper u={1}.

Therefore a genuinely renewable centre in this rooted decimal rec2 family MUST provide, at the odd phases 1,3,5,7, the upper carry signature (0,1,1,1) on EVERY recurrence. This has not been constructed, so no all-time decimal certificate follows. The previously published T02FullBandPortCriterion is for a different p8/m20 rooted exterior.

## Independent checks and caveats

Run: sh calculation/new_structures/Q04/reproduce.sh

The direct port code checks 24,000 randomized base/word/carry cases against twelve widths and verifies the eight rec2 phases at widths 1,2,3,4,5,20,40,80,160. The separate integer checker imports none of its port-code functions, reconstructs genuine numbers and carries from 640 different symmetric digit-pair words, and checks a genuine decimal N+reverse(N) step against predicted next prefixes; both real carry bits occur at each phase. It also independently replays the genuine Lean-certified base9 ten-step/+4 cycle and the existing base50 four-step/+1 cycle at multiple widths. The all-width conclusion rests on the proved carry-map identity, not on these sampled tests.

The auxiliary port_classes.py enumerates all independent-coordinate SPATIAL two-bit carry maps for period clocks p<=30: nine maps (I,0,1) squared, with closed-mask counts 15 for identity and eight for each nonidentity, and exact-return-mask counts 15,3,1 according to the number of identity rails. These are not a classification of the physical TEMPORAL centre transitions, which can couple coordinates. There is no infinite decimal seed, no all-time positive-growth centre cycle, no Lean kernel proof, no ALERT.
