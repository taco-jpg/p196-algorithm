# AgentN16DecimalProtectedExterior20k
**COMPUTED.** A base-10 integer with 12,078 decimal digits constructed from the rooted p8/m20 rec0 exterior and 300 repeated bulk blocks passes exactly 20,000 reverse-and-add steps without any palindrome.
Every one of its 20,001 pairwords starts with the correct 8-phase 39-coefficient rooted boundary, followed by at least 72 full 20-coefficient lattice blocks; the minimum exact matching prefix is 1,494 at t=19,994.
The overflow bits agree with `10101010` repeated 2,500 times; final digit length 22,078.
A direct GMP big-integer engine and independent schoolbook digit-vector engine agree on every step's exterior depth, length, and residues modulo 9,11,99,101,1001 (FNV64 checksum `56371448fdcc1993`).
A second q=301 seed also survives 20,000 steps; its checksum is `38532804c84fb2e8`.
Reproduce: `sh calculation/new_structures/agent-N16/run.sh`.
Source/data: `calculation/new_structures/agent-N16/{replay.cpp,independent.cpp,rows.txt}`.
Detailed construction, scope and modular derivations: `reports/AgentN16DecimalProtectedExterior20k.md`.
**Not claimed:** an infinite base-10 Lychrel number, a centre cycle, or all-q/all-time protection.
