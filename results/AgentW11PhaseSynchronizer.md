# W11: base-independent three-state synchronized-middle phase
- **PAPER PROOF:** In the formal b-ary four-corner reverse-add packet recurrence (any b>=2), synchronized middle packets with canonical bottom offset and guard theta in {-1,0,1}, theta=1 => units(M)!=0 remain synchronized and guard-preserving for **all symbolic steps**, with unbounded middle width.
- Exact middle transitions: theta=-1 -> b*M+rev(M); theta=0 -> M+rev(M); theta=1 -> M+b*rev(M). In every case theta'=gamma-c, gamma and c each in {0,1}.
- **COMPUTED:** decimal four-corner seed t=1..20000 has phase counts {-1:1849,0:12578,1:5573}; 471 middle trailing-zero states, none at theta=1; 19,999 transitions verified.
- Eight independent full-integer controls: bases 2,3,4,9,10,13,16,26 through 90 steps, all matching.
- Code/data: `calculation/new_structures/agent-W11/{phase_synchronizer.cpp,phase_base_controls.py,phase_transitions.txt}`.
- Scope, proof, exact commands and deliberate invalid-guard control: `reports/AgentW11PhaseSynchronizer.md`.
- **NOT CLAIMED:** that the physical packet gaps persist beyond a finite horizon, a decimal infinite Lychrel certificate, a Lean formalization, or anything about 196.
