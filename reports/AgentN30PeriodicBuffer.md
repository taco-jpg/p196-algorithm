# Agent N30: a two-pair decimal pump with a six-state absorbing bulk

**COMPUTED, exact finite horizon.** This is not a decimal Lychrel proof and does not concern the seed 196.

For every nonempty decimal word M let
N0(M) = 1 (89)^2749 8 ++ M ++ (62)^2750.
Equivalently, the 5500 exterior coefficient pairs (LSB index first) have low digits 2,6,2,6,... and high digits 1,8,9,8,9,... . The outer pair coefficients are 3,14,11,14,11,14,..., and the interior is universally quantified. This compresses the previously random 11,600-digit exterior to a fixed period-2 recipe (plus a one-digit edge).

## General absorbing uniform-bulk lemma (paper proof)

Let P_i = d_i+d_{n-1-i} be the palindrome-symmetric pair coefficient word for any n-digit integer N, with low indices i>=0. Suppose P_i=x for every i in the coefficient interval [a,b], where 0<=a<b<floor(n/2), x belongs to [0,18], and x != 9. Define c=0 for x<9 and c=1 for x>9; then floor((x+z)/10)=c for both z=0 and z=1. In the ordinary addition N+rev(N), the low normalized digit at any i in [a+1,b-1] equals y=(x+c) mod 10 because the preceding coefficient belongs to the same uniform interval and forces carry c. Symmetrically the high normalized digit indexed i has carry c because the following mirrored coefficient is also x. With no length growth, the new pair coefficient at i is 2y. With one extra leading digit, the high side is shifted by one: the partner of the low i digit is the previous high digit at i-1. Since i>=a+1 and i<=b-1, its carry is also forced to c. Thus in both overflow cases the next coefficient is exactly F(x)=2*((x+c) mod 10) at every i in [a+1,b-1], independent of the central digits. This is one-step radius-1 erosion, not a recurring centre certificate.

In base 10, x=2,4,8,16,14,10 gives F(x)=4,8,16,14,10,2, respectively. Every member differs from 9 and is absorbing. Therefore any sufficiently long uniform region with these values contains a shrinking, phase-period-6 exact interior under repeated reverse-add. The early period-2 input in this result produces interior coefficients [11,14] at stage 0, [4,10] at stage 1, [10,0] at stage 2, [1] at stage 3, and the six-cycle starts at stage 4. This statement concerns the bulk away from both edges, not the actual integer's first pair.

## Independent computations

The fixed 5500-pair nondeterministic mask format (defined and proved sound in the prior AgentN30TaintEnvelope) yields a disjoint low/high digit-set witness for every t=0..20,000, with first witness index <=25. At t=20,000, 5,447 of the 5,500 pairs contain a nonsingleton digit mask, but the witness persists. The mask computation depends only on the exterior, hence proves the result for every nonempty M.

The C++ program separately performs actual reverse-and-add using custom base-10^9 bigint limbs, checks every represented digit against its mask at each stage, and checks the full palindrome predicate, for M=0, 3^37, and 9^123; all three pass 20,001 states. The final digit lengths are 19,204, 19,240, and 19,326. The independent Python test checks 543,600 digit memberships and 16,150 actual disjoint-mask witnesses across random short centres. The bulk lemma's separate 25,000 random integer tests check 393,976 internal positions, including 11,232 no-overflow and 13,768 overflow branches.

## Exact reproduction

python3 calculation/new_structures/agent-N30/test_periodic.py
python3 calculation/new_structures/agent-N30/test_uniform_bulk.py
c++ -O3 -std=c++17 calculation/new_structures/agent-N30/periodic_family.cpp -o /tmp/n30_periodic
/tmp/n30_periodic 5500 20000 1 0
/tmp/n30_periodic 5500 20000 37 3
/tmp/n30_periodic 5500 20000 123 9

At 20,174 steps for K=5500 the **abstract witness** first fails; that is not an actual palindrome. The constructive follow-up is to keep front/bulk carry correlation rather than expanding the search for forbidden short centres. The six-state cycle itself was already known in decimal position automata; this result claims the new explicit rooted period-2 family, universal-centre replay, and causal bulk mechanism, not discovery of the six-cycle.
