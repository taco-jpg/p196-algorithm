# Eight-step fixed-width moving decimal packet (agent-N05)

**COMPUTED.** Constructive local glider lasting 8 steps in base 10 and independently verified 1000-step integer orbit segment, but NOT a self-sustained/recurrent glider, Lychrel number, or statement about 196.

## Finite-width transport
Lattice: p12 temporal gamma 100010001000, spatial period m9, phase t=2. Consider real palindromic pair coefficients P_x=d_x+d_(n-1-x), x least significant first. Start from the p12 bulk seed with exterior B0 width 34 and two buffer halves 3000 long, advance two steps, then change the four symmetric pair coefficients at x=1008..1011 to [6,1,17,18]; their unmodified values are [8,5,9,16]. Realize the altered pair word as a positive decimal integer using per-pair digit splitting.

At times k=0..8, the support of differences from the *time-aligned lattice* is:
```
k=0: four cells at offsets 0..3
k=1: four cells at offsets 0..3
k=2: four cells at offsets 0..3
k=3: four cells at offsets 1..4 (old trailing site now exact lattice)
k=4: four cells at offsets 1..4
k=5: four cells at offsets 1..4
k=6: four cells at offsets 1..4
k=7: four cells at offsets 1..4
k=8: four cells at offsets 1..4; coefficients [10,1,9,2]
k=9: five cells at offsets 0..4, so strictly finite-width transport fails.
```
This is a genuine moving repaired-wake front for eight iterations, but the *coefficient vector* is not shape-periodic: the transported packet changes internally and then spreads.

## Exact SMT construction and independent checks
The prior `sat_glider.py` defines the QF_LIA space-time constraints for 48 spatial cells from absolute 990, with the carry-in and descending carry set by the periodic lattice, and the exact equation `P'_(x)=u_x+v_(x-gamma_t)` (interior only). The new `sat_h8_partial.py` requires only p[0,18]=6, permits all three other source coefficients to range over [0,18], confines intermediate discrepancies to an eight-cell margin around the moving corridor, forces a true nonzero endpoint at time8, and asks Z3 for an eight-step one-site displacement. The SAT solution is [6,1,17,18], found with the pinned first coefficient. Every model source/target value is checked independently by `phase_packet.local_step`, not by SMT's own equations.

The separate `phase_packet.py` realizes the symmetric pairword as a positive **6071-digit decimal integer** and uses ordinary Python arbitrary-precision arithmetic for **1000 actual reverse-and-add iterations**. At every step the full integer's pair coefficients are compared against an independent local defect evolution over an expanding interior interval; all comparisons pass. Zero palindromes in these 1000 numbers; 250 digit increases match the p12 gamma schedule. At step999 the packet spreads to 575 changed cells over offsets [-185,434]. So there is no infinite orbit inference.

## Reproduction
```sh
python3 calculation/new_structures/agent-N05/sat_h8_partial.py
python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 6,1,17,18 > /tmp/n05-h8-int.json
```
The SMT script requires libz3.so.4. The integer script has no third-party dependencies. The structured expected trajectories are in `calculation/new_structures/agent-N05/sat_h8_witness.json`.

**Next constructive idea:** instead of a single localized packet, couple two such eight-step moving packets a spatial period apart; use an exact two-front return constraint to absorb the widening into a defect that repeats after a 144-step temporal/spatial period. No such coupled packet is claimed here.
