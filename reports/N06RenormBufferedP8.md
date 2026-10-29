# N06: A buffered decimal period-eight orbit and an 88:20 renormalisation front

**COMPUTED**, finite-time construction only. No decimal Lychrel number, infinite-time certificate, or theorem about 196 is claimed.

Define pairword P(N)[i]=d_i+d_(n-1-i), indexed from the least-significant digit, and T(N)=N+reverse(N). Take the first 39 phase-zero positions and the 20-site period from the original p8 SCC record calculation/decimal_frontier/lattice_formats/p8_scc.txt:
- entrance = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
- period = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13].

For k>=0 concatenate Q_k=entrance ++ period^k, length 39+20k. Set n=2|Q_k|; d_i=min(9,Q_k[i]), d_(n-1-i)=Q_k[i]-d_i for 0<=i<|Q_k|. This defines an explicit positive decimal N_k of length 78+40k with P(N_k)=Q_k++reverse(Q_k); leading digit 8. The centre is unconstrained and eventually invades the exterior.

The first eight pair coefficients as phases t=0,...,7 are rows (one row per position):
[17,8,17,8,17,8,17,8], [5,13,6,14,8,16,13,12], [0,5,11,8,17,16,14,9], [1,1,2,4,8,16,14,10], [13,5,10,3,6,14,10,6], [4,8,16,8,17,14,10,2], [14,9,18,16,13,12,6,7], [12,8,16,16,14,9,0,6]. Every temporal phase has an odd coefficient at index [0,1,0,4,0,7,0,2]. Any decimal palindrome has every pair coefficient even. Thus checking this prefix is a sound finite-step palindrome exclusion, regardless of the interior. Expected overflow bits repeat 10101010, starting with 1.

**Independent 20,000-step replay:** For k=225, N_225 has 9,078 decimal digits. Both buffered_prefix.cpp (independent ordinary digit-list reversal/addition, full palindrome test every step) and independent_gmp.cpp (GMP integer arithmetic, reverse the entire decimal expansion every step) independently checked all 20,001 states t=0..20,000: the first eight pair coefficients match every phase, no palindrome, and every overflow bit matches 10101010. Final number length 19,078; modulo 1,000,000,007 = 630236571; decimal-string FNV64 = 15053747816378579192. Seed SHA256 including newline: a43cd2f98f931b733c9a82dea8f7ae812963ab9ff5b5b0e0c740bbddc8a58b8f.

**Renormalisation observation (sample, NOT induction):** Let frontier F_k(t) be the number of initial pairword positions matching the original SCC eight-phase entrance followed by its repeating spatial-20 lattice. Full ordinary digit replay for k=225 gives F_225(t+88)=F_225(t)-20 at *each* of 18,901 integer times 100<=t<=19,000, with zero exceptions. Confirmed by frontier.cpp from all full pairwords, not inferred by comparing only first eight. F(0)=4539, F(1000)=4312, F(2000)=4084, F(10000)=2267, F(19000)=221, F(20000)=8. Apparent travelling defect-front speed 20/88=5/22 sites per step. This is not a proved all-time or all-k front law.

First prefix failure (k,t): (0,196), (1,316), (2,404), (3,492), (5,668), (10,1108), (20,1988), (50,4628), (100,9028), (224,19940), (225,20028), (226,20116). Every tested k>=1 satisfies t_failure=228+88k; for untested k this is a conjectural formula. At k225 the prefix breaks at t20028, which is NOT a palindrome claim. The construction supplies scale-dependent, long *finite* nonpalindromic orbits, not one infinite orbit.

Reproduce from the repository root: bash calculation/new_structures/agent-N06/run_checks.sh (requires C++17 and GMP headers/libraries). This runs two independent full-step engines, the sample-width controls, the source SCC frontier matcher, and exact assertions. All reference data and checksums are in observations.json. No Lean result or infinite-time soundness theorem has been claimed.

**Next direction:** Seek a finite 88-time-step macro-edge that shifts the active interface by 20 spatial positions, *and* a central restart mechanism that survives scale contraction. Simply extrapolating the observed slope would be invalid.