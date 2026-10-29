# AgentN25CarryFreeSplicing
Label: COMPUTED.
Claim: The explicit two-parameter decimal family `1789 0^u 3141 0^v 5926 0^u 5358` with `u,v>=40001` has no palindrome for times `t=0,...,20000`.
Scope: Finite horizon ONLY, not a decimal Lychrel proof. Three mirror-paired zero sectors persist throughout; joint dynamics decouple by an exact symmetric zero-splicing lemma (proof in report).
Base seed: 120019 digits; 20000 RAA steps; 8227 length overflows; final length 128246; each protected sector has >=8228 zeros at t=20000.
Two independent engines (decimal digits vs base-10^9 big integers) agree at every step; final SHA-256 `59464c5366b9800d8b557cd0434b3ad245d10e5b72d842b7f35aa463669e1fba`.
Reproduce: `python3 calculation/new_structures/agent-N25/run.py --steps 20000 --gap 40001`.
Splicing controls: `python3 calculation/new_structures/agent-N25/splice.py`.
Code/data: `calculation/new_structures/agent-N25/` (two C++ engines, Python runner, independent Python splice oracle, checkpoints).
Proof and limitations: `reports/AgentN25CarryFreeSplicing.md`.
