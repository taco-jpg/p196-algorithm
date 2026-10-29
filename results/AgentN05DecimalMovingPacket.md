# AgentN05DecimalMovingPacket
**COMPUTED.** Decimal period-12 / spatial-period-9 lattice: a deliberately modified real 6071-digit reverse-and-add starting integer yields a thin, directed pair-word defect.
At phase 2, lower-half indices x=1008..1011 are set to [8,8,4,16]; only offsets +1,+2 initially differ from the bulk. By step 1 there is just one changed site; through step 15, the changed support stays in [x+1,x+6], with <=6 occupied cells, and its right edge propagates.
It *breaks* at step 16 (seven sites) and the lower wall first retreats to x at step 18; by step 999 the defect occupies 573 sites over offsets [-183,430]. This is a finite packet precursor, NOT a periodic glider.
Independent ordinary Python big integers verify every step's pair word on an expanding interior window, exact phase overflow (250 over 1000 steps), and zero palindromes through 1000 steps. This is NOT a Lychrel certificate, not a full-orbit claim, and not a 20,000-step candidate.
Code: `calculation/new_structures/agent-N05/phase_packet.py`. Data: `calculation/new_structures/agent-N05/packet_samples.json`. Details: `reports/AgentN05DecimalMovingPacket.md`.
Reproduce from repository root:
`python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 8,8,4,16 > /tmp/n05.json`
