# W19: a universal context-independent two-step decimal packet eraser

**PAPER PROOF:** the exact base-10 collision theorem below for arbitrary coefficient-word contexts and all packet multiplicities. **COMPUTED:** complete finite local carry tables, 240 randomized full-coefficient contexts and 150 independent ordinary-integer contexts. No infinite decimal Lychrel number, no closed certificate and no Lean verification.

## Statement

All coefficient words are LSD-first; T(P)=pairs(norm10(P,0)) is the exact pairword successor. Let E be any nonempty coefficient word with first coefficient e0 in 10..17 and all remaining coefficients in 0..18. Let Q be any word with coefficients in 0..18, let an optional central coefficient c be 0..18, let m>=1 and choose independently a_i in {6,7,8} and epsilon_i in {0,1}. Define

    C0 = (14,9,9,0); C1 = (0,14,9,0)
    H = E ++ (a1,13) ++ C_epsilon1 ++ ... ++ (am,13) ++ C_epsilonm ++ Q
    P = H ++ ([c] if present else []) ++ reverse(H).

Then T²(P) is independent of EVERY epsilon_i, while P and T(P) are different for every mask. The packets are non-gauge: C0 and C1 have different coefficientwise residues modulo 9. This is an exact all-m, all-context statement, not a sampled replay claim.

For a genuine positive decimal integer N with pairword P, choose the digit pair at each mirrored site to be min(P_i,9) and P_i-min(P_i,9). When c is present, restrict c to EVEN values and use central digit c/2. Such N has canonical positive leading digit because e0 is 10..17. The 2^m resulting ordinary integers are distinct at stages 0,1,2 and become IDENTICAL at stage 3 of reverse-and-add. Every stage 0,1,2 is nonpalindromic: P, T(P), T²(P) each contain an odd coefficient at a packet site. No assertion is made about stages 3 onward.

## Proof by an exact carry-window table

Since the most significant source pair coefficient e0 is between 10 and 17, the first normalization has overflow gamma0=1. The first coefficient of T(P) is e0-9 in 1..8, so the second normalization cannot overflow (gamma1=0). All carries are bits.

Consider one packet preceded by (a,13), with a in {6,7,8}. Let l and r be arbitrary incoming low and reflected-high normalization carries; these are the only context-dependent values, both in {0,1}. Normalization of the low guard (a,13) gives (a+l,3) and outgoing carry 1. C0 then produces digits (5,0,0,1) and exits carry 0; C1 gives (1,4,0,1) and also exits carry 0. The unknown Q cannot change this exit.

On the reflected high side, reverse(C0)=(0,9,9,14) produces digits (r,9,9,4), exiting carry 1, while reverse(C1)=(0,9,14,0) produces (r,9,4,1), exiting carry 0. The following reflected guard (13,a) produces digits (4,a+1) versus (3,a+1), both exiting carry 0. Thus ALL normalized digits outside the packet and the immediately adjacent reflected guard agree for both packet choices, regardless of l,r and either centre parity. Every later packet starts with a fresh reset carry, so toggles compose independently.

The gamma0=1 reflected-pairing shift gives the low three-coefficient first-image window precisely (9,4,9) for C0 and (4,5,4) for C1. Their preceding coefficient is a+4, at least 10, and their following coefficient is 10. The high window is the reflection of the same triple, because T(P) is palindromic. These formulae are independent of l and r. The table checked by universal_guard.cpp exhausts a=6,7,8; l=0,1; r=0,1; bit=0,1, exactly 24 cases.

When T(P) is normalized again, its immediately preceding coefficient a+4 forces carry 1 into the low triple; the following coefficient 10 forces carry 1 into the mirrored high triple. With incoming carry 1, (9,4,9) normalizes to (0,5,9) and (4,5,4) to (5,5,4), both exiting carry 0. Reflected pairing of these digit triples yields (9,10,9) in both cases: 0+9=5+4=9 and 5+5=10. The two alternatives have identical T²(P) outside and inside every window. Packet starts are separated by six coefficient sites, so the three-wide windows and their one-site carry guards never overlap. Toggle mask bits one at a time: T²(P) is exactly constant for all 2^m masks.

The P0 words are distinct. T(P) is distinct because its windows (9,4,9) and (4,5,4) differ at a unique first site. Their integer values are also distinct: for any two masks, at the lowest differing packet start s the coefficient difference in P is 14 (nonzero modulo 10), and in T(P) it is 5 (nonzero modulo 10); contributions from later sites cannot cancel the least-significant nonzero decimal place. Therefore the true ordinary seed integers are distinct at times t=0,1,2, despite merging at t=3. Odd pair coefficients 9 (in P and T²(P)) and 9 or 5 (in T(P)) prove the first three states nonpalindromic.

## Exact controls, reproduction and scope

From repository root: bash calculation/new_structures/agent-W19/universal_guard_run.sh. The C++17 checker universal_guard.cpp verifies the 24 complete local carry configurations, then exhausts 25,886 packet masks across 240 seeded arbitrary E,Q, parity and guard choices, including 1..9 packets. Independent universal_guard_int.py constructs REAL decimal integer seeds, iterates Python int(n)+int(reverse(str(n))) and checks 150 unrelated arbitrary contexts containing 5,506 masks and 16,668 integer states, with exact stage counts (2^m,2^m,2^m,1). Physical odd centres are restricted to even coefficients. See universal_guard_expected.json.

This strictly strengthens the previous AgentW19TwoStepPacketErasure result: it needs no p8/m20 lattice, no periodic E or Q, no fixed centre, and only two guard coefficients per packet. It is an absorbing rewrite rule, NOT a regenerating packet emitter and NOT a complete infinite-orbit certificate. A plausible next construction would connect an independent bounded packet emitter to this universal absorber, with a complete finite macro-return proof. No Lean modules are changed. Runtime Git DNS prevented a repo checkout and tools/verify.py --changed, so no repository-wide or kernel verification is claimed.
