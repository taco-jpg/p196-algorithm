# AC24 attempts / boundary of method

- A generic 120-step prefix from B3 W3^14 alone contracts from 160 to 70 coefficients. It **cannot** reject the junction: actual first endpoint mismatches lie around indices 134..149. Rejecting at index 7 (as an earlier phase-3 J6 report did) is incompatible with this exact prefix.
- Adding a fixed U^40 to the retained prefix, after the arbitrary J, gives enough information for a centre-independent no-return test. The high-side carry at the unknown cut is universally 0 or 1; carry convergence after the first non-nine coefficient makes the retained prefix sound even when W9 is temporarily damaged.
- The cost is an exhaustive `30*19^5` endpoint search, not a short SAT certificate. A failure at q=14 does **not** exclude q-changing, growing-junction, mixed-U, or higher-phase repair mechanisms; no global all-time Lychrel result follows.
