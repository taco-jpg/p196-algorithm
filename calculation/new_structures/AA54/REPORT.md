# AA54 base-transfer report

**Status: PARTIAL.** The transfer mechanisms are distinguished, and one exact obstruction to a direct base-9 transfer is proved. No decimal seam closure, all-time certificate, or global no-go is claimed.

## Mechanisms

The power-of-two certificates use a phase-indexed neutral-band cycle: the repeated coefficient is b-1, and the finite exterior/core cycle restores its carry/overflow interface while the band grows. The base-9 LatticeBand certificate instead uses an absorbing periodic lattice: the carry-out of a period block is independent of its incoming carry, and the periodic bulk has a reflection axis compatible with the total overflow shift.

For the decimal target, every candidate U3 motif is a rotation of U_a=(9,a,18-a), where a is even. Its three entries are pairwise distinct: 9 is odd while a and 18-a are even, and a=18-a would imply a=9. A reflection of a 3-cycle fixes one position and exchanges the other two, so a length-three word with a reflection axis must have two equal entries. Therefore no U3 rotation has a reflection axis. The base-9 self-mirror-lattice closure mechanism cannot transfer directly to a single U3 band.

A small independent checker enumerates all 30 distinct rotations and checks this criterion, plus the local carry-absorption property on the reachable carry states 0,1,2. Carry absorption alone does not establish a periodic row-map cycle or a mirrored seam return.

## Exact missing lemma

A coupled decimal W9|J|U3 seam/cocycle transition must restore the physical boundary state and mirror compatibility while preserving the W9 exponent and advancing k by 5 per 120 steps (or give a sound closed phase-indexed family). This report does not supply that lemma.

## Scope and redirect

The negative statement applies only to transferring the base-9 reflection-axis mechanism to a lone U3 periodic band. It does not exclude a coupled W9|J|U3 construction, a moving seam, a multi-band format, or a different periodic bulk.
