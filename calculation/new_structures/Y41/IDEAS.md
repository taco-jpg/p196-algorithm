# Y41 ideas and redirects

## Exact phase gate (proved, necessary only)
For a periodic band of spatial width m and an overflow clock with period p and G overflows per period, the band endpoint advances by G cells per p-step lap. Its phase lies in Z/mZ and is translated by G. A same-phase return after j laps requires jG=0 mod m, so the minimum is m/gcd(m,G). This is the multi-lap version of the one-lap condition m|G. It does not check the seam or centre.

## Scoped redirects
- Do not present p20 neutral-band exhaustion as a no-go for all W-band templates.
- Do not present p24's capped exterior candidates or a uniform-lattice search as a general seam exclusion.
- Do not repeat U32's p16/m4 charge proof. It excludes the stated 48/96-step three-cycle cases, not 144-step returns or every fixed-row longer-period case.
- Exact compatibility ranking, not survival ranking: p12/m9 needs 3 clock laps for band-phase closure; p8/m20 needs 5; p16/m4's selected three-cycle needs 3 laps for row-state closure but the existing charge excludes those first two row-cycle multiples, leaving 9 clock laps as the first multiple not excluded by that charge.

## Next useful step
Build a complete phase-indexed physical seam transition graph for one unowned family, then prove either a recurrent SCC with nonnegative resource drift and a non-palindrome guard, or a completeness-scoped empty graph. The phase gate alone is not that graph.
