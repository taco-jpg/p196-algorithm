# AgentX23DistributedKinkCrystal18
- **COMPUTED**, finite-horizon only, base 10; NOT an infinite Lychrel certificate.
- Explicit 46,078-digit seed is realized from the symmetric coefficient word B ++ W^400 ++ (8,6,8)^5000 ++ reverse((8,6,8)^5000) ++ reverse(W^400) ++ reverse(B); B (39 coefficients), W (20 coefficients) are in the source.
- Every t=0..20,000: genuine GMP integer N_t matches independently evolved *full* pair coefficients, and N_t is not a palindrome; at t=20,000: 56,078 digits.
- All 20,000 overflow bits alternate 10; the 39-coefficient p8 exterior clock holds; period-20 outer lattice has a matching prefix >=3,457; inner spatial period-3 crystal has a matching centre suffix >=8,551 at every state.
- The nonuniform ring (8,6,8) reaches a minimal temporal 18-cycle at t=11 under the alternating clock, synchronized with the p8 exterior at t+72; explicit 18 rows are provided.
- The separating noncrystalline interface grows from width 0 to width 15,992 by t=20,000, so this does NOT close a finite certificate or imply survival past t=20,000.
- Reproduce: `cd calculation/new_structures/agent-X23 && g++ -O3 -std=c++17 crystal18.cpp -lgmpxx -lgmp -o crystal18 && ./crystal18 400 5000 20000`.
- Code/data: `calculation/new_structures/agent-X23/`; details: `reports/AgentX23DistributedKinkCrystal18.md`.
