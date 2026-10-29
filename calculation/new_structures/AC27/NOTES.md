# AC27 running notes

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, phase-6 row of lat_p12m9.txt, T12/cut.py, Z11's exact cone, R30's independent verifier and #476 recent comments. Registered CLAIM before searching.
- No existing committed exhaustive phase-6 J5 cell; AB27 only reported PARTIAL 720/148,565,940 fixed-C triples.
- Implemented an independent AVX2 cone locally, checked against full coefficient recurrence for 36,000 transitions, then completed all 30 distinct U rotations × 19^5 J words. Eight output chunks summed independently. Global histogram checksum: 74,282,970; first mismatch minimum 133, maximum 156.
- The sole first-mismatch index 156 witness is U=(9,14,4), J=(14,5,14,16,4), code 1,864,151. Its genuine bigint replay across five widths and both centre parities retains W-cut-relative mismatch -4.
- Independently checked 310 real integer 120-step runs (37,200 steps) with schoolbook differential checks at reference width; no phase/length surprises. Shifted U bulk map F^120(U)=U checked for all 30 rotations.
- No claim about the time to a palindrome. The result is exclusion of a fixed-seam one-epoch return, NOT evidence of infinite nonpalindromic survival.
