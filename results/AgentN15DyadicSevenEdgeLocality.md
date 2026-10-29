# AgentN15DyadicSevenEdgeLocality
**PAPER PROOF.** A new all-level dyadic finite-factor transfer format extends the earlier two-edge Thue–Morse decimal identity to **seven exact consecutive ordinary reverse-and-add pairword steps** for every height h>=2, not merely experimentally checked heights.
For each h, the new third pairword is an explicit 3-letter sliding-block coding of sigma^h(14), with fixed boundary coefficients; the next four steps are the *same* radius-one decimal carry cellular operator, fully sound because their input words avoid the neutral coefficient 9.
Universal finite-factor proof: sigma^4(AA), sigma^4(AB), sigma^4(BA), sigma^4(BB) cover all bulk windows of lengths 3/5/7/9; all values at time 3/4/5/6 are in sets avoiding 9. The two temporal-parity boundary classes (plus h2..7) are checked separately.
Fixed leading/trailing arithmetic witnesses prove the corresponding real decimal integers N_0,...,N_7 are all nonpalindromic for every h>=2.
Independent actual decimal integer digit-vector checker verifies the full predicted pairwords at h=2..15, steps3..7, with negative mutation controls; this finite replay is not the source of the universal claim.
Result and exact argument: `reports/AgentN15DyadicSevenEdgeLocality.md`; source: `calculation/new_structures/agent-N15/{ca_proof.py,ca_independent.cpp,run_ca.sh}`.
Reproduce: `sh calculation/new_structures/agent-N15/run_ca.sh`.
Scope: exactly the first seven transitions, not indefinite nonpalindrome avoidance, not a base-10 finite-cycle certificate, no claim about 196 or an asymptotic fixed point.
