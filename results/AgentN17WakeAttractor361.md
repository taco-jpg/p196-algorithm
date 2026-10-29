# Agent N17: a 361-seed basin for the decimal 44-step wake particle
- **Label: COMPUTED**, exhaustive over all 19^2 values of two central pair coefficients, at half-width h=500 through step 1500.
- Each of 361 explicit 1000-digit seeds has rooted period-8 / spatial-period-20 exterior and arbitrary last two lower-half coefficients (a,b) in 0..18; symmetric partners are set identically.
- **All 361** avoid a palindrome for 1500 iterations; min first-defect position 157; overflows alternate 1010.
- Every case has a travelling head with \`f_t=f_(t-44)-10\` and identical 60-cell comoving window [-20,+40) for **each** step t=716..1500; total 283,385 checks.
- The latest failure of this 44-step test in the entire ensemble is t=715, so 716 is sharp for this recorded class and horizon.
- At step 800, 27 distinct head windows occur; the 361 seeds are not all the same head state.
- Two independent exhaustive engines (literal digit vectors and GMP big integers) agree on counts, earliest-sharp onset, no-palindrome and overflow controls.
- Reproduce: \`bash calculation/new_structures/agent-N17/run_universe.sh\`; code \`universe.cpp\`, \`universe_gmp.cpp\` in the same directory; details in \`reports/AgentN17WakeAttractor361.md\`.
- **Not claimed:** any all-time glider, an infinite base-10 Lychrel number, an all-width basin, a bound beyond step 1500, or Lean verification.
