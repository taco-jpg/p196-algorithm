# AgentN15DyadicCoreShielding
**COMPUTED** positive mechanism: in decimal reverse-and-add *pairword dynamics*, a growing Thue–Morse absorbing dyadic shell delays the propagation of a central change from pair coefficient 0 to 18 into a fixed exterior window by roughly a number of steps proportional to shell width (finite levels h=6..12 only).
For shell width 2^h and exterior-prefix 16, the EXACT first differing step is h6:280, h7:587, h8:1355, h9:3160, h10:5796, h11:11546, h12:23223. A complete 7x5 table for prefix widths 4,8,16,32,64 is in `shield_data.json`.
Two independent engines reproduce every crossing: ordinary decimal digit-list reverse-and-add on both *actual integers*, and pairword carry normalisation. A third Python bigint checker verifies prefix-16 crossings h4..10.
Initial pairwords have the explicit nested form `(4 ++ sigma^h(14)) ++ [c] ++ reverse(4 ++ sigma^h(14))`, `c=0 or 18`, `sigma(14)=14,16`, `sigma(16)=16,14`.
This is a *transient shielding mechanism*, not a periodic glider, not a proof of all-h linear-time shielding, and not a base-10 Lychrel certificate.
Reproduce: `sh calculation/new_structures/agent-N15/run_shield.sh`. Detailed scope/proof obligations: `reports/AgentN15DyadicCoreShielding.md`.
