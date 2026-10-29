# Agent16F2FixedBase4AllBase

**COMPUTED.** With canonical root and fixed period-six overflow word `101100`, in each of
its six time rotations, the complete uncapped reachable position automaton has:
base 4: 957 states, 1012 edges, four cyclic singleton SCCs (minimum root depths
9, 13, 14, 18); bases 5 and 6: five states, four edges, zero cyclic SCCs.
All 18 complete directed graphs match a separate brute-force carry-word checker.
**PAPER PROOF.** The existing all-base first-column classification
(`results/Agent16F2Base4RootClassification.md`) excludes root edges in
all bases other than 4, 5, 6, for all six rotations. Thus **base 4 alone**
has a reachable periodic exterior SCC for this fixed time necklace.

No other overflow schedule, disconnected bulk, centre, base-10 certificate,
or Lychrel number is claimed. Exact proof, code, independent checker, four
self-loop witnesses and positive base-9/base-13 controls: `reports/Agent16F2FixedBase4AllBase.md`.
