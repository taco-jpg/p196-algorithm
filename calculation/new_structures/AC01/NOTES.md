# AC01 running notes

- #476 registration precedes enumeration; revisited AB01's U=0,1,2 cell.
- Correct count across n=7..14 is 4,320,346,920 candidates; earlier 66,660,000 total denominator is incompatible with palindrome enumeration.
- Direct full 120-step decimal engine and window engine agree on checked cases. The window solver checks carry escape and guard coefficients every step, falling back to the direct engine on violation.
- U=0,1,2, n=7: 205,770/205,770, zero local matches, zero fallbacks (prior AB01 coverage independently corroborated).
- U=0,1,2, n=11..14: 60,000/4,308,412,260 sampled, zero local matches, zero fallbacks; no exhaustive claim.
- Five-width independent Python BigInt controls agree stepwise with schoolbook decimal arithmetic.
