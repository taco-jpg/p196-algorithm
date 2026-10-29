# Agent14P8FixedCarryRigidity
**PAPER PROOF.** For each of three known reachable decimal period-8 non-self-mirror bulk lattices (rec0/rec1 m=20, rec2 m=48, overflow 10101010), **base 10 is the unique integer base b>=2** supporting an 8-phase cyclic bulk with the lattice's complete unchanged ascending/descending carry itinerary.
The homogeneous return map is 16(I+S)^4 and invertible after subtraction from I; fractional first-coordinate slopes exclude b<10, and a tight carry-zero inequality with slope >1 excludes b>10.
**Scope:** unchanged full carry itinerary and prescribed temporal/spatial periods only. Different carries, other bases' cycles, rooted exteriors, centres, base-10 Lychrel certificates and 196 are not decided. No Lean claim.
Proof: reports/Agent14P8FixedCarryRigidity.md.
Inputs/certificate: calculation/decimal_frontier/lattice_formats/agent14_p8_rows.json and agent14_p8_slopes.json, checked against existing p8_scc.txt.
Primary and independent code: calculation/decimal_frontier/lattice_formats/code/agent14_fixed_carry_lift.py and agent14_fixed_carry_independent.py.
Run both from repository root using python3 (standard library only). Replays all 704 coefficient edges and exact slope recurrence; additional 10-step base-9 |B|61 and base-13 |B|75,55 positive controls.
