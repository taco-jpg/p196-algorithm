# AgentN18EightyEightRenormalization
**COMPUTED**: base-10 88-step lattice insertion covariance, exhaustive 79,640 symmetric coefficient cores of length 0..7, comparing q=1 and q=2.
Define `G(P)=pairs(normalize10(P))` on low-first pair coefficients, `T_q(C)=B ++ W^q ++ C ++ reverse(W^q) ++ reverse(B)`; B is width 39 and W spatial period 20 from `calculation/new_structures/agent-N18/lattice.txt`.
C ranges over palindromic coefficients in 0..18 with even midpoint for odd length (so decimal seed digits exist).
For every covered C, `G^88(T_1(C))=T_0(R(C))` and `G^88(T_2(C))=T_1(R(C))`, with `|R(C)|=|C|+84`; all 88 intermediate exterior rows match the temporal period-8 B and overflow 10101010, giving an odd pair coefficient/nonpalindrome witness.
Core counts at lengths 0..7: `1,10,19,190,361,3610,6859,68590`; no search cap.
**Positive renewal**: 24 cores of length 7 satisfy `R(C)=W ++ D ++ reverse(W)`, so one 88-step macrocycle replenishes one consumed band. Explicit C=`[8,0,0,16,0,0,8]` gives `|R|=91`, `|D|=51`.
In this exhaustive bounded-core set, none of those 24 replenishes a second time; this redirects the construction to backward preimages of the *two-renewal* condition with larger, structured centres rather than further short-centre exclusions.
Independent Python true-integer control: 248 selected cores, q=1,2,3, 88 updates each; validates centre covariance and the explicit one-renewal witness.
Reproduce inside `calculation/new_structures/agent-N18`: `g++ -std=c++17 -O3 renewal_hunt.cpp -o renewal_hunt && ./renewal_hunt 7`; `python3 check_renewal_bigint.py`.
**Not claimed**: covariance for all q or all core lengths, repeated renewal, an infinite decimal orbit, or Lean verification.
