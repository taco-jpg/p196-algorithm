# W29 Carry-Parikh finite quotient
- **PAPER PROOF:** For every base b>=2 and every pair-coefficient block w, the carry/digit-frequency XOR transducer F has F^3=F, and the carry/last-digit/unordered-edge XOR transducer U has U^4=U^2.
- An r-band template with independently positive repetition counts needs at most 2^r or 3^r representative checks for a universal nonpalindrome witness on its normalized successor.
- Every palindrome has at most one odd-frequency digit and zero parity mask of unordered adjacent distinct-digit pairs.
- **PAPER PROOF decimal control:** symmetric even-coefficient family P(k)=[4,18]++[10,12,12]^k++[0]++[12,12,10]^k++[18,4], k>=1, has successor histogram mask 830 and nonzero edge mask 576742227289321472 uniformly; its explicit canonical split is nonpalindromic.
- **COMPUTED:** full GMP-vs-independent-digit replay for 196 and 88(0^14000)75 over 20,001 states each, no palindromes, edge mask nonzero at every checked state.
- **COMPUTED:** 2,400-seed sweep, 981,786 nonpalindromic states, 974 seeds surviving 1,000 steps; every inspected state is certified by the union of histogram, odd pair-coefficient, or unordered-edge parity.
- Code: calculation/new_structures/agent-W29/certificate.py and replay.cpp; compact data: summary.json.
- Reproduce and precise limitations: reports/AgentW29CarryParikh.md.
- **NOT CLAIMED:** a base-10 infinite Lychrel number, a closed template cycle, a proof about 196 after step 20,000, or Lean verification.
