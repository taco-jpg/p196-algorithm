# AgentN05BalancedGliderStrip
**PAPER PROOF.** A translating-glider strip certificate format: palindromic pair words with two independently pumpable periodic buffers and a finite moving defect. Finite carry-window tiles and insertion-commutation checks imply exact reverse-and-add closure for all sufficiently long buffers; a cyclic strip with nonnegative total buffer changes and an odd pair coefficient at every phase certifies nonpalindromicity forever.
A necessary design equation for a return of fixed finite blocks is `sum(gamma)=2m*(delta_left+delta_right)`. For a balanced one-period extension of BOTH buffers, the first schedule-compatible horizons are decimal p12/m9 T=144, p8/m20 T=160, and p8/m48 T=384.
This differs from a stationary centre: the moving defect advances one spatial period per balanced cycle, while the centre retreats by two. These are proposed search horizons, NOT found cycles.
No decimal instance, no Lean verification and no theorem about 196 are claimed. Formal soundness statement and Lean sketch: `reports/AgentN05BalancedGliderStrip.md`.
Code/data: `calculation/new_structures/agent-N05/balanced_glider_periods.py`, `balanced_horizons.json`.
Reproduce: `python3 calculation/new_structures/agent-N05/balanced_glider_periods.py`
