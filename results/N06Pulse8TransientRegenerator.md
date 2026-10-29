# N06Pulse8TransientRegenerator
- Label: COMPUTED, a positive finite-time base-10 central pulse. No infinite certificate.
- New core C=[18,9,8,14,2,11,13,16] after the original p8 entrance39 and period20^L.
- For each tested L=1,2,10,221,222, eight leading pair coefficients remain on the eight-phase p8 schedule exactly 248 more steps than the same seed without C: first failure 476+88L.
- Same-length L1 controls: zero8 fails at t310, period8 at t348, engineered pulse8 at t564.
- L222 seed has 8,974 digits; digit-vector and independent GNU GMP ordinary integer reverse/add replay through t20,000 (20,001 full states): no palindrome, exact first8 and overflow, final 18,974 digits.
- Final modulo1000000007=383594414, decimal FNV64=746813162037088509, first pattern failure at t20012 (position7: actual13 vs expected14).
- Reproduction: bash calculation/new_structures/agent-N06/pulse8/run_checks.sh.
- Source/data: calculation/new_structures/agent-N06/pulse8/; detailed report reports/N06Pulse8TransientRegenerator.md.
- Not claimed: an all-L proof, stable centre cycle, infinite Lychrel number, Lean verification, or anything about 196.
