# Decimal growing packet precursor (agent-N05)
**COMPUTED**, exact scope: one explicit 6071-digit positive decimal seed and its first 1000 ordinary reverse-and-add steps. No decimal Lychrel number or infinite glider is claimed.

## Construction and local mechanism
Coordinates are LSB-first pair-word positions. Source p12 lattice has gamma=100010001000, m=9, and B_0 width 34. Form a palindromic coefficient word `P_0 = (B_0 ++ W_0[0:3000]) ++ [0,0] ++ reverse(B_0 ++ W_0[0:3000])`. Realize it as a positive integer with each paired coefficient p split into (p-min(p,9),min(p,9)); perform two ordinary reverse-and-add steps and modify symmetric pair coefficients at absolute indices x=1008..1011 to [8,8,4,16]. Realize the modified palindromic pair word as a new positive integer. Seed length = 6071 decimal digits.
For each phase, the exact bulk lower entering carry is the supplied nine-site `C_t`; descending carry is obtained by right-to-left normalization. Compute `u_j=(P_j+c_j)%10`, `v_j=(P_j+d_j)%10`, and the successor pair coefficient `P'_{j}=u_j+v_{j-gamma_t}`. This gives a finite perturbation operator with untouched bulk at the far ends. The reference code checks all 108 phase/spatial bulk positions.

The defect behaves as an initially coherent one-sided front: changed-site counts at k=0..19 are
`2,1,1,2,2,3,3,4,4,4,4,5,5,4,5,6,7,7,8,9`.
For k=0..17 the leftmost mismatch is x+1, while the rightmost grows to x+7. At k=18 the leftmost mismatch becomes x: repaired-wake persistence ends. At k=999 the support has 573 cells and spans x-183..x+430. Thus a propagating front occurs but fails to remain a finite-width glider.

## Independent replay and limitations
`phase_packet.py` does not generate its ordinary-integer next values from the carry-window method: it computes N+reverse10(N) using Python arbitrary-precision integers and decimal digit conversion. It separately recomputes pair coefficients of the full integer at EVERY step and compares them with the local bulk-plus-defect prediction on an expanding interior window. It independently checks all 1000 whole integers for palindromicity and all 1000 overflow bits. All pass. There are 250 length increases.
This validates an interior mechanism only, not a global symbolic template or eternity of the seed. The growth of the packet after step 15 specifically redirects the next search toward **moving-interface finite certificates with a glider that returns after a superperiod while both buffers grow**, rather than stationary width-k centres.

## Reproduce
```sh
python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 8,8,4,16 > /tmp/n05-packet.json
```
The compact output baseline `packet_samples.json` records (step, changed sites, left offset, right offset), including every 24th step and the endpoint. No external packages are required.
