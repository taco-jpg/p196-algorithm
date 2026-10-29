# AgentW06RegularCarryErase
- **PAPER PROOF:** Exact all-length p8/m20 decimal carry-erasure language. Each 20-cell W band has eight independent +/-9 toggles. For every M>=1 and fixed even centre C, all 256^M distinct canonical seeds have the same entire first-step pairword and **identical second-step integers**.
- The proof identifies four disjoint one-digit carry impulses at each mirrored toggle, cancelling in the (n+1)-digit output's symmetric coefficient sums.
- **COMPUTED:** For M=320,C=18, all 2^2560 distinct 12,879-digit seeds avoid palindromes at states t=0..20,000 via the all-length synchronization proof plus independent 20k replay.
- GMP integer decimal-string reverse-add and independent digit-array arithmetic agree: final length 22,879 digits; complete MSD FNV64 3bba2a5955eee568; zero palindrome/clock failures; 295 rooted coefficients checked every step.
- Controls: 2,560 exhaustive one-block mask/centre cases, 500 random multiblock cases, 90 Python-bigint cases, and an intentionally failing adjacent-toggle mutant.
- Code: calculation/new_structures/agent-W06/{toggle_family.py,toggle_schoolbook.cpp,toggle_gmp.cpp,toggle_observations.json}.
- Reproduction and proof: reports/AgentW06RegularCarryErase.md.
- Not claimed: infinite decimal Lychrel number, regenerative junction cycle, or Lean verification.
