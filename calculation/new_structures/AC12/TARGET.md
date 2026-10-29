# AC12 phase-3 fixed-seam target

Let H(q,k)=B3 ++ W3^q ++ J ++ U^k and P(q,k)=H(q,k) ++ C ++ reverse(H(q,k)), with published rooted p12/m9 phase-3 rows, 30 charge-zero U3 rotations and a realizable palindromic centre C.

**Target:** an exact physical 120-step reverse-and-add return P(q,k) -> P(q,k+5) with the identical J,C and q fixed for every q>=14,k>=100, including actual carry/overflow/length and nonpalindrome guards. The T12 cut-insertion theorem makes the reference-width (14,100) return necessary; the restoration of B3 W3^14 at t120 is an endpoint-only necessary condition.

AC12 exhaustively checks this necessary condition for all J words of length 3 and 4 at q14/k100, all 30 U rotations, odd C=[4,14,4] and even C=[4,4]. No strict-per-phase W9 pruning. The existing T12 two-port reset cone leaves 300-152-122=26 protected U coefficients and separates distant centre effects, subject to the phase-3 clock. An exclusion here does not exclude longer or changing seams, nor prove a decimal Lychrel number.