# Agent X12: 20,000-step genuine decimal two-clock inner insertion

**Label: COMPUTED.** Standalone independent arithmetic test of a centre-insertion mechanism in genuine base-10 reverse-and-add, not a theorem of infinite nonpalindromicity.

## Construction

Take the known period-8 rooted exterior B0 of length 39 and W0 of length 20, explicitly embedded in beat20k.cpp. Define U as 40 coefficients 1 except indices 13,20,30 holding 7,7,6 respectively. Define the central palindrome C_r = [8,0,0] ++ U ++ 1^r ++ [16] ++ 1^r ++ reverse(U) ++ [0,0,8]. For each q,r form the least-significant-first palindromic pairword P_(q,r) = B0 ++ W0^q ++ C_r ++ reverse(W0)^q ++ reverse(B0). Realize it as actual base-10 digits with (d_low,d_high)=(min(p,9),p-min(p,9)), and at the central site d=p/2.

Take q=300, and r=20000,20001. Thus the shorter integer has 52165 decimal digits, and the larger has 52167.

## What the independent exact computation checks

The primary arithmetic engine stores *real decimal digits* as bytes and performs ordinary digit-column carry addition to the literal reversed number. The independent engine stores the same initial integer in base-1000 limbs; at each step it converts its current limb-defined integer to decimal, reverses that string, parses the reversed number back to base-1000 limbs, and adds in base 1000. At EVERY state it compares the complete decimal strings of both independently updated representations for each of the two orbits. In 20,001 states per orbit, the arithmetic agrees exactly, totaling 40,002 full-number comparisons. Both are tested for full decimal palindromicity at every state: zero hits.

From each exact integer, form its full pairword. At each step t, assert all 39 exterior coefficients agree with the known eight temporal B rows, independently of the partner orbit. Also assert that the longer orbit's *entire* pairword is the shorter orbit's entire pairword with the SAME one coefficient inserted at two reflected positions and no other changes. This is a complete-word comparison, not a finite-prefix or finite-window check. The inserted coefficient starts as 1 and follows 2,4,8,16,14,10 with temporal period 6 thereafter.

Let k_t be the actual absolute lower splice coordinate. At every t=264..20000 assert k_t-k_(t-264)=-44, giving 19,737 separately checked macro-windows. Check both orbits have the alternating overflow word 10101010... for all 20,000 operations; this is *measured*, not imposed in the arithmetic. Overflows contain 10,000 ones. The moving inner centre and the outer period-8 exterior together yield a 264-step two-clock beat (lcm(12,88)), with a persistent moving insertion rather than a short periodic kink.

The last shorter integer has 62165 digits, and k_20000=22749. FNV64 hashes of the final least-significant-first actual digit arrays, in r=20000 and r=20001 order, are 769a482b8c36ccfa and 402e99c32c98dd80. These are deterministic regression fingerprints, not cryptographic checksums.

## Status and next constructive condition

This is stronger than a passive large-seed no-palindrome check because every one of 20,001 complete paired states obeys a nontrivial *relational* centre-insertion law, a six-phase symbol clock, a 264-step absolute spatial drift, and an exterior phase witness. However, it is still a finite reservoir construction; its splice moving -44 per beat does not prove replenishment of the outer lattice, and a common orbit prefix is not a finite template cycle. The missing infinite certificate would need a return edge that regenerates the expended exterior while retaining the reflected centre-insertion gate, expressed through the two-counter macro-interface of reports/AgentX12TwoClockCentrePulse.md. No result about 196 is obtained.

## Reproduction

From the repo root:

    g++ -O3 -std=c++17 calculation/new_structures/agent-X12/beat20k.cpp -o /tmp/agent_x12_20k
    /tmp/agent_x12_20k 300 20000 20000

A smaller positive control: `/tmp/agent_x12_20k 20 200 200` gives final hashes `cacde6f3b12578e8` and `13d0cbbde8abc632`, seed/final length 1365/1465.

No Lean files are changed, and the local environment cannot clone GitHub to run repository-wide `python3 tools/verify.py --changed`. The standalone code compiled with g++ and passed the complete recorded run.

