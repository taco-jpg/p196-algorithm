# AgentX17NeutralCarryGate
- Label **COMPUTED**: decimal palindrome-adjacent motif `88283583` has a length-residue-gated neutral-9 carry superchannel at step 107.
- For tested `n=2001,6001,10001,20001`, the source pair-sum's high boundary has a run of `(n-161)/2` consecutive 9s; differential carry crosses all in one step.
- At `n=20001` this is **9,920 columns**; identical high exterior drops from 9,981 digits at step 107 to **60** at step 108, then low exterior drops to 60 at step 109.
- For tested `n=2009,6009,10009,20009`, centre phase blocks the neutral-9 channel at the same time; both exteriors remain synchronized.
- Positive protected-phase control `n=10009`: **20,001** exact states, no palindrome, >=2,237 matching exterior digits at each end, full word equality between independent GMP and digit-column engines.
- PAPER PROOF for local carry transmission through precisely sum-9 columns; no assertion of a closed infinite certificate or all-length congruence theorem.
- Code and 32-row exact table: `calculation/new_structures/agent-X17/phase_gate.py`, `phase_gate.csv`, `phase_gate_reproduce.sh`; details: `reports/AgentX17NeutralCarryGate.md`.
- Reproduce: `bash calculation/new_structures/agent-X17/phase_gate_reproduce.sh` (C++17, GMP, Python3).