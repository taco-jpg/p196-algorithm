# T02MovingQDecreaseObstruction

Label: PAPER PROOF (exact affine carry simulation, independently replayed by arbitrary-precision integer and digit-array arithmetic). Not Lean-verified.

Missing-lemma contribution: an all-width obstruction to every two-epoch q-decreasing endpoint from the rooted R18 phase-4 J24/C3 family, under the R36 charge relation and X45 seam/centre length invariant; this redirects the search away from that root.

Scope: all 30 rotations of (9,a,18-a) for even a in {0,2,...,18}; independent q,k>=512; target q'=q-a with 1<=a<=q-1, k'=k+10+3a, arbitrary finite J' and palindromic C' satisfying 2|J'|+|C'|=51.

Proof: the exact affine folded-pairword engine runs 240 steps and gives first mismatch against B4 W4^q at offset -24 or -22 from the cut 34+9q. For a=1,2 the defect lies inside the required target W band. For a>=3, the target U3 band starts at s=-9a+|J'|<=-2. If s<=-27, its first three cells are an undamaged W4 triple, none of which is an allowed U3 word. For -26<=s<=-2, the symbolic window scan over all source U words and offsets shows no allowed U3 word matches more than three consecutive cells, while the target U band has at least 3*(512+19) cells. Thus no endpoint exists in this class, regardless of J' contents.

Independent controls: moving_q_endpoint.cpp checked 30 source U words and all 30 target U' words at (q,k)=(20,80),(40,160),(80,320),(160,640), 240 genuine reverse-add steps each. The Boost cpp_int engine and separate schoolbook digit-array engine agreed on all 28,800 steps; zero clock errors, zero sampled palindromes, and zero endpoint hits for a=1..10 and |J'|<=25. These are controls, not the all-width proof.

Reproduce symbolic proof: python3 calculation/new_structures/T02/moving_q_symbolic.py

Reproduce integer controls: g++ -O3 -std=c++17 calculation/new_structures/T02/moving_q_endpoint.cpp -o /tmp/t02_moving_q && /tmp/t02_moving_q

Scope limit: this does not exclude other exterior phases, other source J/C families, targets outside the R36/X45 charge-length class, or prove the existence/nonexistence of a decimal Lychrel number.
