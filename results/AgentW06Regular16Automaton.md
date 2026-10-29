# AgentW06Regular16Automaton
- **PAPER PROOF:** p8/m20 carry-erasure language extends from eight independent toggles per W block to sixteen candidate +/-9 toggles with a two-state nearest-neighbor compatibility automaton.
- Exact transfer-count matrix (previous/next j19 bit) is [[1864,1864],[1152,1152]]; all-length legal mask count A(M)=3728*3016^(M-1), M>=1.
- Every accepted mask word at fixed M and even C in 0..18 yields the identical entire first-step pairword and **identical full integer after the second reverse-add**. A precise four-impulse proof is in the report.
- **COMPUTED:** for M=320,C=18, all A(320) distinct 12,879-digit seeds avoid palindromes through 20,000 steps by the proved synchronization plus independent GMP/digit-array 20k baseline replay from AgentW06RegularCarryErase; final length 22,879, FNV64 3bba2a5955eee568.
- Controls: 37,280 exhaustive one-block/centre cases, 280 multiblock random cases up to M=1000, 35 independent Python BIGINT pairs, invalid adjacent-toggle control, exact transfer matrix.
- Code: calculation/new_structures/agent-W06/{regular16_automaton.py,regular16_observations.json}. Detailed proof and commands: reports/AgentW06Regular16Automaton.md.
- Not claimed: every erasing mask, infinite Lychrel orbit, regenerative junction, or Lean verification.
