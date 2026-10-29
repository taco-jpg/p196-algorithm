# AgentW27BoundedOddWitness
**COMPUTED**: A fixed near-root pairword guard captures all nonpalindromicity in two decimal trajectories, without inspecting their deep centres.
For the true 196 orbit, t=0..100000 inclusive, first digit-pair mismatch index <=28; for every t>=20 the first **odd pair coefficient** occurs at index <=28.
At t=8,13,19 the complete pairword has only even coefficients, yet the number is not a palindrome. These three exceptions are handled by literal mismatches, not misrepresented as odd witnesses.
For the W27 central-9 family baseline Q=6005, at every t=0..20000 the first odd pair coefficient is at index <=18, with maximum 18 at t=4852. By the already committed central-insertion lemma this guard extends to ALL Q>=6005 over the same finite horizon.
196 maximum first-odd index 28 at t=9777; 196 first digit-pair mismatch maximum 28. Final 196 length at 100000 is 41490; zero palindromes.
Both profiles come from full ordinary decimal carry replays, with per-state exact pair-coefficient and palindrome/mismatch checks. Independent Python arbitrary-int control through 196 t=1000 and hybrid t=160 reproduces exact local maxima.
Code: `calculation/new_structures/agent-W27/{prefix_witness.cpp,prefix_oracle.py,witness_expected.json}`; report `reports/AgentW27BoundedOddWitness.md`.
Reproduce: `c++ -O3 -std=c++17 calculation/new_structures/agent-W27/prefix_witness.cpp -o /tmp/w27w && /tmp/w27w && python3 calculation/new_structures/agent-W27/prefix_oracle.py`.
Not claimed: a global bound for all t, a true-196 certificate, a 196/exterior lattice coupling, or a periodic finite-state invariant.
