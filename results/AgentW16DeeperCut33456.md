# AgentW16DeeperCut33456
- Label: **COMPUTED**; exact base-10 scope: every pair of integers `kw>=440,kv>=530` in the stated two-independent-pump family, at orbit times `t=0..33456`. Not an infinite result.
- Seed coefficient word, LSD first: `P0=H ++ [9] ++ reverse(H)`, where `H=B ++ W^kw ++ [9] ++ V^kv`; `B,W,V` are explicit in `skew_contract.cpp`, of periods `|W|=20`, `|V|=48`. The starting decimal integer is `D0=normalize(P0)`.
- The fixed paired-insertion cuts are `iW=839`, `iV=39+20*kw+1+48*427`; they support **independent arbitrary additions** to `kw` and `kv` at every certified transition (33,456 checked edges) through two-ended carry loops and the overflow-shifted high-side compatibility identity.
- Every state has an external mismatch anchor before `iW`, hence no palindrome. Decimal overflow alternates `1,0`; baseline `kw=440,kv=530` grows from 68,562 to 85,290 decimal digits.
- Baseline/shifted ordinary digit-array controls verify every pairword edge. Independent GMP ordinary-decimal-number replay and final LSD-first FNV64 given in `cut_observations.json`.
- The **next** paired-insertion edge fails at `t=33456` by `gamma cut phase slip` at the V cut. This is not an observed palindrome, not a statement about later ordinary orbit steps, and not a universal no-go.
- Moving the V proof cut from period-offset 400 (first failure 31,340) to 427 lengthens the certified two-parameter horizon without changing any seed number. Offset 428 fails earlier (33,238), demonstrating a shrinking viable cut corridor.
- Source: `calculation/new_structures/agent-W16/{skew_contract.cpp,cut_extended.cpp,independent_gmp.cpp,run_cut_extended.sh,cut_observations.json}`; full reasoning `reports/AgentW16DeeperCut33456.md`.
- Reproduce: `sh calculation/new_structures/agent-W16/run_cut_extended.sh`; no base-10 Lychrel certificate and no claim about 196.
