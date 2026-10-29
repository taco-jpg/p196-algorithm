# Ordered multi-kink scattering on the decimal period-12 lattice

**COMPUTED.** A second constructive mechanism on the p12/m9 bulk: two distinct packets do not collide at a time determined by separation alone. At the same sites, 300 and 804, their order changes the first nonlinear interaction by 39 reverse-and-add steps. This matters for a finite-state centre made from a word of kink symbols: order cannot be quotiented away. No infinite cycle, Lychrel number or theorem about 196 is claimed.

Start from the 5,000-coefficient symmetric pairword defined in AgentN21P12TransducedPacketTrain, at p12 lattice phase 2. At an anchor replace 11 lower-half coefficients, together with reflected mates, by exactly one symbol:

    A = (6,1,0,1,11,14,10,6,11,16,1)
    B = (16,0,9,11,1,10,8,5,14,18,0)
    C = (16,0,9,11,1,10,8,8,9,16,0)

For X,Y in {A,B,C}, let P_t^0 be the unmodified pairword, P_t^X the orbit with X at 300, P_t^Y the orbit with Y at 804 and P_t^{XY} the orbit with both replacements. All four are actual integer orbits, with initial canonical decimal digits independently constructed by the checker. Define first nonlinear time T(XY) as the least t where the coefficientwise equality P_t^{XY}=P_t^X+P_t^Y-P_t^0 fails. The code checks every lower-half coefficient and requires equal lengths. Computed first nonlinear times, first positions, and numbers of discrepant lower-half coefficients:

    AA 820 (648, 3)       AB 840 (661, 2)       BA 801 (650, 3)
    BB 825 (664, 2)       AC 832 (656, 2)       CA 801 (650, 3)
    BC 817 (659, 2)       CB 825 (664, 2)       CC 817 (659, 2)

These are first interactions, not later annihilations. The order-sensitive difference T(AB)-T(BA)=39 steps is a constructive scattering delay. It is NOT a local interaction rule proved valid for arbitrary separation or arbitrary packet types, and it does not imply any stable soliton. In additional exploratory pairword replay, AB's nonlinear support has 2 lower-half cells at t=840, 17 at 864, 65 at 936, and 115 at 1008, consistent with a growing nonlinear wake; these later counts are not relied on by the committed assertion.

Independent numerical control is plain Python arbitrary-precision decimal arithmetic using the canonical seed realization in check_bigint.py: seven 5,000-digit seeds, namely background, A@300, B@804, AB, B@300, A@804, BA. Every orbit is replayed with N+int(str(N)[::-1]) for 900 full steps, and its entire decimal digit pairword is independently recovered at every state. A separate coefficient-normalization engine supplies the expected word. None of the seven orbits reaches a palindrome in these 901 checked states. The first nonlinear events are checked independently: AB (840, first lower-half position 661, two cells), BA (801, first position 650, three cells).

Reproduce from repository root with Python 3 and no external dependencies:

    sh calculation/new_structures/agent-N21/run_binary.sh

The runner compares all nine rows with the exact binary_trace.jsonl fixture and executes the bigint checker. This is finite exact computation, not an exhaustive search beyond the nine ordered pairs and the 900-step validation horizon. A possible next constructive direction is to seek symbols whose collision OUTPUT returns to the same finite alphabet, with bounded packet widths and nondecreasing periodic gaps. The present A/B/C symbols do not demonstrate that property.
