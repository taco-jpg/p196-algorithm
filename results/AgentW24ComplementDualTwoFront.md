# AgentW24ComplementDualTwoFront
**COMPUTED.** A new explicit base-10 orbit family, obtained by coefficientwise 9-complementing the first p8/m20 rooted pairword B W^q mirror(B W^q), has a nonstationary period-20 band between TWO advancing defect fronts.
For q=900 (36,078 starting digits), **all 20,000 ordinary reverse-and-add steps** pass independent GMP integer vs schoolbook decimal digit-vector equality, with zero palindromes.
At every t=0..20,000 the lower-half pairword contains a contiguous spatial-period-20 run of at least **2,732** coefficients; final run is [11,844,14,576), final 44,400 digits.
The left defect front advances 35 -> 11,844; right bound retreats 18,019 -> 14,576. The observed band is being consumed, not renewed.
**PAPER PROOF.** Exact complementary-pair carry kink: if P and Q are symmetric and P_i+Q_i=2(b-1), then normalization creates a forced (b-2) carry junction and b-1 digit-sum tail, with exactly one overflow.
**COMPUTED control.** 373,812 exhaustive/random independent integer checks across bases 3..97; the exhaustive sweep covers all even-length-6 symmetric pairwords (with valid nonzero-leading partners) in bases 3..21.
Reproduce: python3 calculation/new_structures/agent-W24/complement_carry.py
Reproduce: g++ -O3 -std=c++17 calculation/new_structures/agent-W24/dual_front.cpp -lgmpxx -lgmp -o /tmp/w24dual && /tmp/w24dual 900 20000
Files: calculation/new_structures/agent-W24/{complement_carry.py,dual_front.cpp,dual_observations.json}; full proof/scope: reports/AgentW24ComplementDualTwoFront.md.
**Not claimed:** an infinite base-10 Lychrel certificate, self-complementary fixed orbit, rooted 39-column exterior beyond the transient, a proven two-wall velocity, or Lean verification.
