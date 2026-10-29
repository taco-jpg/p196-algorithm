# X30: complete two-bit carry-free paired-block eraser
- **PAPER PROOF:** For EVERY Q>=2, independently choose from a 7744-symbol alphabet for EACH of floor(Q/2) mirrored pairs of blocks in X0=("5346")^Q. All 7744^floor(Q/2) resulting distinct decimal seeds are nonpalindromes at t=0,1 and are EXACTLY X2 after two ordinary reverse-add steps.
- Each symbol is an integer pair (U,V), 1000<=U<=9999, 0<=V<=9999, with x,y independently in {0,1} satisfying U+rev4(V)=11781+90x+900y, V+rev4(U)=11781+900x+90y, leading(U)!=last(V). The one-step difference is (90x+900y)*10^(4b)+(900x+90y)*10^(4a), for mirrored a,b=Q-1-a, and the second reverse-add cancels its anti-mirror legal digit edits.
- **COMPUTED complete alphabet:** counts (x,y)=(0,0):4096, (1,0):1536, (0,1):1536, (1,1):576; total 7744=88^2, all options independently validated by exact Q=2 digit arithmetic.
- Compared with X30's preceding 5632-symbol theorem, this adds the second independent two-step switch and its interaction, including 2112 new symbols. It also gives a four-class exact local interface catalogue.
- At Q=8000, **7744^4000**, about 2^51675.45, seeds inherit W10's known palindrome-free t=0..20000 orbit; no claim after t=20000.
- **COMPUTED:** a deterministic mixed-colour Q8000 member passes 20001 full-state independent schoolbook/radix-1e9 checks, 32000→40323 digits, 8323 overflows, zero palindromes, final FNV64 MSB ASCII 33f8ce7f29c9f033.
- Reproduce: python3 calculation/new_structures/agent-X30/two_bit_counts.py; g++ -O3 -std=c++17 calculation/new_structures/agent-X30/two_bit_dipoles.cpp -o /tmp/x30b && /tmp/x30b 8000 2 20000. Proof in reports/AgentX30TwoBitCarryFreeFibre.md.
- **NOT** a base-10 Lychrel number/certificate, Lean proof or infinite result.
