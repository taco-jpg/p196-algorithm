# Y41 target: primitive rooted-family survey (variant 1/6)

## Question
For the first-index representative in rooted decimal families with temporal overflow periods p in {8,12,16,20,24}, decide whether a symmetric periodic-band template can have a physically rooted epoch return with a seam independent of band exponent q. The p31/G10 route belongs to agent-407.

A positive result must close both physical carries, overflow phase, band phase, centre parity, canonical leading digit, and the non-palindrome guard. A negative result must be an all-width obstruction or a completeness-certified finite-state emptiness result. Finite-horizon survival is not a certificate.

## Exact current scope

| Family | Exact screen | Broad seam status |
|---|---|---|
| p8/m20, g=10101010, G=4 | Band phase advances by 4 mod 20; at least 5 clock laps (40 steps) for phase closure. | UNDECIDED: phase closure is not seam/carry closure. |
| p12/m9, g=(1000)^3, G=3 | Band phase advances by 3 mod 9; at least 3 clock laps (36 steps) for phase closure. | UNDECIDED: this one-band gate does not decide the distinct two-band T* target. |
| p16/m4, g=(01)^8, G=8 | Phase gate passes in one lap. The selected primitive reflection-symmetric three-cycle has row-state period 48; the existing U32 mod-9 charge excludes 48 and 96 steps, but not 144. | PARTIAL only for that three-cycle subfamily. |
| p20 | Existing exterior census exhausts p=20 candidates in its neutral-band format. | UNDECIDED for arbitrary non-neutral W-band templates. |
| p24 | The exterior census marks g=(0001)^6 and g=(01)^12 as capped/undecided; other uniform-lattice searches have narrower scope. | UNDECIDED. |

This is a scope map, not a claim that any seam exists.

## Missing lemma
A completeness-sound finite physical seam-map theorem deciding recurrence for one unowned family while tracking both carries, overflow, band phase, canonicalization, centre parity, and the phasewise non-palindrome guard.
