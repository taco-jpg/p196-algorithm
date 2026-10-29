# AgentX01OverflowLockedNineBand
**COMPUTED:** For every integer Q>=4149 the decimal seed N0(Q)=49(99)^Q59 has nonpalindromic states t=0..20000, with a symmetric central 9-digit band of length >=3 (central pair coefficient 18).
Every one of the 20,000 exact symbolic transitions satisfies a new per-edge phase lock: paired trims r_t=1-gamma_t (gamma is actual leading overflow). Hence L_(t+1)=L_t-gamma_t; every non-overflow edge consumes ZERO centre fuel.
At Q=4149: gamma1=8295, gamma0=11705, trims=11705, no lock failures; initial 8302 digits, final 16597 digits, final central run L=3, exterior width 8297.
Independent ordinary Python bigint decimal reverse-add checks EVERY actual integer, central-run length, per-step lock, and palindrome test; all 15 reported checkpoints agree with the independent C++ transducer, final checksum mod 1000000007 = 13994719, pathhash = 289024506.
This reduces the 20k horizon padding from N23's Q=6016 for 12(99)^Q34, but is NOT an infinite decimal Lychrel certificate. Q=4148 violates the L>=2 safety condition by t=20000; no palindrome conclusion follows.
Reproduce: sh calculation/new_structures/agent-X01/reproduce.sh.
Code/data: calculation/new_structures/agent-X01/{x01_pump.cpp,x01_oracle.py,trace_20k.json}; proof scope: reports/AgentX01OverflowLockedNineBand.md.
No Lean files; local standalone arithmetic controls passed; repository-wide verify.py --changed unavailable without GitHub shell checkout.
