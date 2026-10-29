# AgentV08CentralRunIndexAudit
**Label: PAPER PROOF** for the sharp all-length centre shielding lemma, plus **COMPUTED** genuine-integer counterexamples and controls; **not LEAN-VERIFIED**.
If a physical decimal pairword has centered full run x^k, k>=3, x in {2,4,8,10,14,16}, its successor has a centered run of the six-cycle successor symbol of length >=k−2+gamma, where gamma is actual overflow.
Sharp gamma=0 counterexample to the literal N19 full-run k−1 wording: 1984090 → 2888981, with pairwords [1,18,8,8,8,18,1] → [3,16,17,16,17,16,3]; k=3→1.
The original N19 test instead counts k in the folded halfword, where loss of one folded cell is consistent.
Proof: normalization through a constant x run stabilizes carry after first cell, leaving k−1 identical digits; non-overflow reflection matches k−2, overflow reflection matches k−1.
Independent ordinary-integer checks: 18 sharp members and 10,000 random cases; further N24/N25/N27/N29 controls.
Reproduce: python3 calculation/new_structures/agent-V08/audit.py.
Audit and exact scope: reports/audit_2026-10-28/AUDIT_N16-N30.md.
Not claimed: a decimal all-time cycle, an infinite Lychrel seed, or a full replay of all N16–N30 scripts.
