# AgentN05SATMovingFront
**COMPUTED.** Exact QF_LIA space-time carry constraints with independently fixed low/high bulk carries synthesize a nonzero decimal period-12/m9 defect packet from an unknown three-coefficient source.
The SAT witness at phase 2 is [6,3,7] at x=1008..1010. At steps 3..5 all mismatches are at x+1..x+3: the original position x is perfectly repaired, and a three-cell front has translated +1 within five steps. At step 6 it expands to four cells, so this is a transient moving glider primitive, **not a recurrent glider**.
The independent ordinary-integer replay validates 1000 reverse-and-add steps of a realized 6071-digit starting integer with no palindrome, exactly 250 overflows and exact local pairword agreement on expanding windows. No infinite decimal certificate or 20,000-step candidate is claimed.
Source: `calculation/new_structures/agent-N05/sat_glider.py` plus existing `phase_packet.py`. Data: `sat_h5_witness.json`. Report: `reports/AgentN05SATMovingFront.md`.
Reproduce (requires libz3): `python3 calculation/new_structures/agent-N05/sat_glider.py --H 5 --phase 2 --free --one-shot --drift 1 --wide 3 --margin 6 --M 48 --origin 990 --first 18 --timeout 4500`.
Independent integers: `python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 6,3,7`.
