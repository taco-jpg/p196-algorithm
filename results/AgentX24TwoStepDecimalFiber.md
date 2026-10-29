# AgentX24 two-step decimal inverse fibre
- **Label: COMPUTED** for a 20,000-step decimal replay and independent finite oracle tests; report provides an elementary all-k collision proof.
- Explicit rooted base-10 p8/m20 pairwords with central choice Cσ=[0,a1,...,ak,ak,...,a1,0], a_i in {1,10}.
- Exactly 2^k **distinct pairwords and first-step numerical values** coalesce to the *same numerical state at step two*, for every r>=1,k>=1.
- With r=234,k=200, all 2^200 seeds start at 9,840 decimal digits, and their common post-step-two orbit reaches step 20,000 without a palindrome; final length 19,840.
- Every one of the 20,001 checked pairwords has the correct rooted 39-column cap, at least six full spatial-period-20 band copies and reflected suffix.
- Independent implementations: GMP and decimal digit-vector addition checked each transition; Python bigint tests exhaustively check 2,550 small seeds and 60 large random cases.
- Reproduce from calculation/new_structures/agent-X24: g++ -O3 -std=c++17 packet_replay.cpp -lgmp -o packet_replay; ./packet_replay 234 20000 200; python3 fiber_check.py.
- Details: reports/AgentX24TwoStepDecimalFiber.md; data: calculation/new_structures/agent-X24/replay_k200_20k.log.
- Not an infinite decimal Lychrel certificate; no Lean proof or regenerative centre claimed.
