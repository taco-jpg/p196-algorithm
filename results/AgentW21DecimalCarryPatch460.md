# AgentW21DecimalCarryPatch460
- **COMPUTED**, finite decimal pairword/exterior result, NOT a Lychrel certificate.
- A new 40-coefficient terminal patch Q improves the first rooted period-8 exterior mismatch of the equal-length N26 W++R patch from 88c+340 to 88c+460, at tested c=0,1,3,225: 120 extra steps with zero additional initial digits.
- At the first mismatch, column 38 is wrong because its reflected high digit receives carry 0 rather than the required 1 on the preceding step.
- c=225 gives a 9,158-digit genuine decimal integer: through step 20,000, all 20,001 states are nonpalindromic, full pairwords agree with an independent normalizer, and at least two exact 20-column exterior band copies persist. Final length 19,158 digits.
- Independent 20,000-step GMP integer reverse-and-add confirms no palindrome and matching checkpoint FNV64 hashes. First rooted exterior failure is t=20,260. Q++Q does not regenerate.
- Reproduction: calculation/new_structures/agent-W21/{replay.cpp,gmp.cpp,plateau_search.cpp,trace.txt}; detailed scope: reports/AgentW21DecimalCarryPatch460.md.
