# AC45 joined adjacent-column 120-track ROBDD (2026-10-29)
**Label: UNDECIDED** for PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH. **COMPUTED** for the stated finite symbolic measurements and independent tests; the local transfer identity is **PAPER PROOF**.

**Missing-lemma contribution (exactly one sentence):** The joined-column engine enforces equality of the hidden high-carry and gamma-one digit-lag ports between adjacent folded columns, supplying a necessary physical coupling for the unbuilt pi185 120-layer product rather than multiplying independent one-column possibilities.

Let x_j be the folded pair coefficient at spatial column j, and (lo,hi,lag) the incoming low carry, outward high carry, and previous upper digit. Existential high-in h_j is legal iff floor((x_j+h_j)/10)=hi. Define a=(x_j+lo)%10, b=(x_j+h_j)%10, and y_j=a+(b if gamma=0 else (1 if j=0 else lag)). The next column receives (floor((x_j+lo)/10),h_j,b). This precisely identifies the two columns' shared carry and gamma-one high digit. By consecutive digit normalization, the relation is necessary and sufficient for every physical *local* 1-step scan, but the centre join must still be enforced separately.

Source: canonical rooted phase-0 B34=(10,4,6,6,...), W9=(5,18,4,8,1,15,4,0,5), fixed boundary phase clock (1000)^30 and source/target first n coefficients B[:n]. Exact 120-track ROBDD measurement:

| n adjacent columns | accepting high-in bitstrings | live ROBDD nodes | reachable temporal states |
|---|---:|---:|---:|
| 1 | 1,073,741,824 | 90 | 1,545 |
| 2 | 288,230,376,151,711,744 | 515 | 12,270 |
| 3 | 22,358,028,821,495,790,305,280 | 4,096 | 47,596 |
| 4 | 9,724,686,151,416,460,353,732,608 | 12,999 | 294,907 |

These counts are **conditional source-side spatial-collar assignments**, not reachable states in the free-J/C pi185 NFA and not distinct full physical orbits. Variables are interleaved by time and space and skipped bits are counted exactly. This is a true joined 120-layer product for the measured n=1..4 prefix, but it is neither an unbounded spatial product nor an endpoint-return decision.

Reproduce: \`python3 calculation/new_structures/AC45/joined_columns.py\`. The 1,440 deterministic short-clock BDD counts were checked against an independent explicit path-count dynamic program, including positive cases and a planted gamma-one carry choice. 30 genuinely rooted source numbers at q,k=(14,100),(20,120),(40,200),(80,400),(160,800), three U choices and two valid centre parities were replayed for 120 steps (3,600 physical edges). Every step agrees with a separate decimal big-integer reverse/add calculation and schoolbook digit addition, including the prescribed clock and local four-column transfer. None is asserted to return.

**Unsolved:** existential image across arbitrary finite SAME J, palindrome SAME C, whole W9 and U3 cuts, centre closure, same-marked spatial endpoints, all 30 U rotations, and language emptiness. Strict-phase W9 preservation and odd-centre mod-11 pruning were not used. No decimal all-time certificate, no EXHAUSTED-NONE census, no ALERT.
