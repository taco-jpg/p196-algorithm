# Q01: T* phase-clock and centre-splice obstruction

**PAPER PROOF.** This extends the U3 complement-reflection lemma with an exact bulk transition formula and a phase-specific fixed-centre obstruction. It is not a no-go for asymmetric or phase-changing centre repairs.

## 1. Exact all-width bulk map

Let U=(u0,u1,u2) be any of the 30 charge-zero p12/m9 U3 rows. Let s0,s1,s2,s3 be its steady carry path, with s0=s3=tau_U and s_(i+1)=floor((u_i+s_i)/10). Extend s periodically with period 3. The one-step deep-bulk successor row F_gamma(U), for actual overflow gamma, is:

    F_0(U)_i = 2*u_i - 9 + 11*(s_i - s_(i+1))
    F_1(U)_i = u_i + u_(i-1) - 9 + 10*(s_(i-1) - s_(i+1))

All indices are modulo 3. These formulas are exact for every q and every k>=3, independently of finite J and C. For gamma=0, the paired output digit at the reflected position comes from the same coefficient u_i. For gamma=1, the extra leading overflow digit shifts the reflected partner by one coefficient, to u_(i-1); the second formula includes that lag. Substituting the complementary steady carries gives the displayed equations.

The published clock is gamma=(1,0,0,0,1,0,0,0,1,0,0,0), repeated ten times. Exhausting the exact 30-state map F_gamma gives:
- every one of the 30 U3 rows returns to its starting row after 120 steps;
- every 120-phase tau_U word has exactly 60 zeros and 60 ones;
- every phase transition stays within the 30-row U3 family.

This is a finite state enumeration with exact carry formulas, not a finite-horizon orbit claim. The map applies to all band widths because it was derived from the steady interior carries, not fitted to a sample width.

## 2. Exact centre-splice criterion

Let C be a legal palindromic coefficient centre, and let d0,...,dn be the decimal carry cuts when normalizing C from incoming carry e=d0. To extend the bulk complement-reflection law through the centre requires

    d_i + d_(n-i) = 1   for every i=0,...,n.

If n is even, the middle cut would have to satisfy 2*d_(n/2)=1, impossible for a carry bit. Thus an even-length centre cannot carry this symmetry through at all.

For odd n, the canonical central pair coefficient is even, hence is either low (<=8) or high (>=10), never 9. Delete all 9 coefficients from C and label each remaining coefficient L if it is <=8 and H if it is >=10; call this type word sigma(C). The carry symmetry holds **if and only if**:
1. sigma(C) alternates L,H,L,H,... or H,L,H,L,...; and
2. the incoming carry e is 1 when the first type is L, and 0 when it is H.

Reason: a low coefficient resets carry to 0 and can satisfy reflected complementarity only when entered with 1; a high coefficient resets to 1 and can satisfy it only when entered with 0; a 9 transmits carry unchanged. Thus non-9 types must alternate. Since C is palindromic, sigma(C) is palindromic; the odd central coefficient is non-9, so the centre type agrees with the first type. The stated input condition is therefore both necessary and sufficient.

Consequently, at a phase with tau_U=1 a centre preserving this symmetry must have a low central coefficient; at a phase with tau_U=0 it must have a high central coefficient. Section 1 proves that both tau values occur (60 times each) in every 120-phase U3 cycle. More sharply, across the 60 odd-length-centre phases, every U3 start and either initial length parity gives a tau split of 28/32 or 32/28, with 33 or 34 changes between consecutive odd phases. Thus any centre that preserves the law on all odd phases must switch its low/high central class at least 33 times per 120-step clock. **No single fixed centre C can extend the complementary-reflection carry invariant through the centre at every phase of the T* clock.**

## 3. Search consequence and scope

This closes the proposed *all-phase symmetric carry-walk* route for a phase-independent centre. A viable T* construction must deliberately break complement-reflection in a finite centre collar, use a phase-changing centre state, or establish a different invariant. It does **not** rule out a physically valid asymmetric carry trajectory, a phase-changing centre, or a complete decimal Lychrel certificate. It does not borrow the p16 neutral-exterior symmetry census.

## 4. Reproduction

Run from the repository root:

    python3 calculation/new_structures/Q01/tstar_phase_center_gate.py

Executed controls in an isolated local mirror:
- 1,440 actual canonical-integer phase/U checks across (q,k)=(20,20),(40,80),(80,40),(160,160), all matching the exact bulk map;
- all 30 U3 rows return after 120 formula-driven phase steps, each with 60 zero and 60 one carry states;
- over the 60 odd-centre phases, tau splits 28/32 or 32/28 and changes class 33 or 34 times for every U3 start and either initial length parity;
- 419,920 palindromic-centre/incoming-carry cases through centre length 8 agree with the exact centre-splice criterion.

These finite controls validate the formula implementation; the uniform-width statements follow from the exact carry derivation and finite 30-state enumeration. No full T* seam return or Lychrel number is claimed.
