# AA55 target: alternating two-W9-band seam

Status: PARTIAL / UNDECIDED. No candidate has been tested yet in this workspace; this is a target specification, not a result.

## Exact target
Find a physically rooted base-10 reverse-and-add template with two W9 bands of independently parameterized widths `(q_1,q_2)`, an inner U band, seam junction(s), and centre C, for which a 240-step genuine decimal orbit returns to the same template family while exchanging the two W9 widths (or following a proved finite cycle of width pairs). The same rooted clock and a non-palindrome guard must be preserved. Any proposed relation must hold for all sufficiently large widths, not just for finite samples.

## Required evidence
1. Explicit decimal integer construction for every tested width pair.
2. Independent big-integer reverse-and-add replay for 240 steps.
3. Structural equality with the claimed endpoint family, including both W9 bands, all seams, clock phase, U band and centre.
4. Replay at q=40,80,160 after any candidate survives two epochs.
5. An all-width argument for the return map before calling it a certificate.

## Current obstacle
The supplied census reports approximately 21-23 W9 columns lost per epoch for stationary one-band seams. Width exchange only helps if the exact two-epoch map reverses or transfers this drift, and that has not been established. The 22-column observation alone is not a proof of impossibility or existence.