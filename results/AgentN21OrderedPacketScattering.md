# AgentN21OrderedPacketScattering

**COMPUTED** in base 10 for the p=12/m=9 lattice and two 11-site packet symbols separated by 504 positions: packet order changes the first nonlinear collision time. Symbol A followed by B remains exactly additive through step 839 and first scatters at step **840** (two lower-half coefficients); B followed by A first scatters at step **801** (three coefficients). The 39-step asymmetry is a positive, direction-sensitive collision mechanism, not an exclusion or infinite decimal certificate.

A third packet symbol C gives nine ordered-pair controls with first interaction times: AA 820, AB 840, BA 801, BB 825, AC 832, CA 801, BC 817, CB 825, CC 817. All nine were checked through their first interaction using exact pairword radix normalization. Independent Python arbitrary-precision integer reverse-and-add checks seven canonical seeds (two arrangements and their singles/background) through step 900, with no palindrome or full pairword mismatch.

Reproduction: `sh calculation/new_structures/agent-N21/run_binary.sh` (or run the two Python files separately); source, fixture and checker in `calculation/new_structures/agent-N21/`. Interpretation, exact seeds and limitations: `reports/AgentN21OrderedPacketScattering.md`. No finite certificate cycle, Lean proof or conclusion about 196 is claimed.
