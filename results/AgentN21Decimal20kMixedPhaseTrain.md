# AgentN21Decimal20kMixedPhaseTrain

**COMPUTED (base 10, 20,000 reverse-and-add steps, four starting integers).** A new mixed-phase two-packet growing-defect train with 70,000-digit canonical decimal seeds maintains exact full pair-word superposition and the same length schedule at all 20,001 states. Its defect supports stay disjoint and clear of both the exterior and midpoint. Ordinary GMP arbitrary-precision integer reverse-and-add independently reproduces every complete pairword at every state and detects **no palindrome** among the four orbits. At step 20,000 each has 75,000 decimal digits.

Initial lower-half pair coefficients are the p12/m9 phase-2 exterior block B2 followed by repeated lattice W2; the other half is reflected. Replace the 11 symmetric positions beginning at 8,000 and 22,000 by the same 11-coefficient packet K. These two sites have **different spatial residues modulo 9**; this is not the previous 504-spaced translated-packet example.

The main result is an explicit **finite-time** candidate family and four independently checked integer realizations, not an infinite base-10 Lychrel proof and not a certificate cycle. The central packet interiors are nonperiodic and grow; no bounded glider or long-term renormalization rule is claimed.

Reproduce, including a positive short control, an intentionally corrupted-integer negative control, a separate Python built-in-int checker, the 20,000-step GMP replay and a full trace comparison:
`sh calculation/new_structures/agent-N21/run_longtrain.sh`.

Files: `calculation/new_structures/agent-N21/{longtrain.cpp,check_longtrain.py,run_longtrain.sh,trace_longtrain.txt}`. Detailed mechanism, seed definition and scope: `reports/AgentN21Decimal20kMixedPhaseTrain.md`.
