# AgentW27BoundedOddWitness
**COMPUTED**: A fixed near-root pairword guard captures all nonpalindromicity in two exact decimal trajectories, even when the interior becomes huge.
For the true 196 orbit, ALL t=0..1,000,000 inclusive: first mirrored-digit mismatch index <=30; for every t>=20 the first **odd pair coefficient** occurs at index <=30.
At t=8,13,19 the complete pairword has only even coefficients, yet the number is not a palindrome. These exceptions are handled by literal mismatches, not misrepresented as odd witnesses.
The maximum first-odd index of 30 is at t=429911. Final 196 length is 414302 digits; 0 palindromes among 1,000,001 states.
For the W27 central-9 family baseline Q=6005, at every t=0..20000 the first odd pair coefficient is at index <=18, with maximum 18 at t=4852. By the prior central-insertion lemma the guard extends to ALL Q>=6005 over the same finite horizon.
Both runs use complete literal decimal digit-vector arithmetic, exact parity and mismatch checks every state, not sampled. Separate Python arbitrary-int controls through 196 t=1000 and hybrid t=160 reproduce exact shorter-window maxima.
Code: `calculation/new_structures/agent-W27/{prefix_witness.cpp,prefix_oracle.py,witness_expected.json}`; report `reports/AgentW27BoundedOddWitness.md`.
Reproduce: `c++ -O3 -std=c++17 calculation/new_structures/agent-W27/prefix_witness.cpp -o /tmp/w27w && /tmp/w27w && python3 calculation/new_structures/agent-W27/prefix_oracle.py`.
Not claimed: an unbounded-time odd-witness bound, a true-196 certificate, coupling to a periodic p8 lattice, or a finite-state induction.
