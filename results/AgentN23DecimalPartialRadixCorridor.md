# AgentN23DecimalPartialRadixCorridor
**COMPUTED.** Exact 174-step nonpalindromic reverse-and-add corridor for EVERY member of a growing decimal family.
Source N0(q) is the real decimal integer with digit string 12 + (99)^(52+q) + 34, all q>=0.
At all 175 time slices the full base-100 grouping is U_t ++ [99]^q ++ W_t (literal boundaries vary with time).
The new *partial-high-block* rational-polynomial checker proves 174 ordinary DECIMAL arithmetic transitions for all q>=0, including odd decimal lengths, and proves nonpalindromicity of every time slice for all q>=0.
Independent ordinary Python big-integer replay checks every complete numeral at q=0,1,2,10,50,100,250.
At step 175 (qbase 50), the single-symbol insertion rule first fails: q=0 has local [88], q=1 has [98,89], an interacting carry front, not an exclusion of richer formats.
A reproducible frontier table for qbase=45..60 shows first collision steps 157..212 and the local substitution.
Code/data/reproduction: calculation/new_structures/agent-N23/ and bash calculation/new_structures/agent-N23/reproduce_corridor.sh.
Derivation and exact scope: reports/AgentN23DecimalPartialRadixCorridor.md.
No infinite decimal certificate, no proof about 196, no new Lychrel number, no Lean claim.
