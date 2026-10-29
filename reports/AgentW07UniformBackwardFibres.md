# W07 all-q backward-fibre pumping: finite-but-uniform decimal survival

## Statement and labels
**PAPER PROOF**, relative to (i) the established universal one-step p8 lattice insertion lemma of AgentN10UniversalPumpLemma and (ii) the exact 20,000-step base-q=300 trace checked in AgentW07ReverseFibre20k: for every integer q>=300, the seed family defined below has no palindrome for t=0..20000, with full period-8 rooted caps B_t and at least q-228 full W_t lattice bands throughout. This is NOT a theorem of infinite survival at fixed finite q.

**COMPUTED** independent controls: whole pairwords of q=300 and 301 compared at each 20,001 time slice, direct integer-digit evolution for 20,000 steps each; independent GMP 20,000-step q=301 test plus q=300 from previous result; q=320 direct digit-array test and a deliberately corrupted band negative control.

## Construction
Fix the B and W from AgentN10UniversalPumpLemma, with |B|=39, |W|=20 and two positions in W equal to coefficient 1. For any q>=300 define H_q=B++W^q and P_q=H_q++reverse(H_q). At each of the 2q positions in W^q with pair coefficient 1, choose its low/high digit pair to be independently (0,1) or (1,0). At every other symmetric position s choose low=min(s,9), high=s-low. This gives exactly 2^(2q) distinct positive decimal integers, all length 2*(39+20q)=78+40q. High leading digit is 8 since B[0]=17. Each initial pairword is P_q and has odd coefficient 17, so no source is a palindrome. Integer N+reverse(N) depends only on P_q, so all 2^(2q) seeds coalesce after one step and share one future. The total family is infinite as q ranges over integers >=300.

## Length-independent proof via one-step insertion
For a symmetric coefficient word P=B_t++W_t^r++C++reverse(W_t^r)++reverse(B_t), define I_t(P) by inserting one copy W_t immediately after its first 39 coefficients and the reversed W_t immediately before its final 39. The N10 universal insertion lemma proves for every arbitrary palindromic C and r>=1:
    T(I_t(P))=I_(t+1 mod 8)(T(P)),
where T is the exact base-10 pairword map after ordinary reverse-and-add, including the actual length overflow. This also implies identical overflow bits. The middle C is NOT assumed bounded or periodic.

The independent q=300 whole-integer calculation (20,000 transitions) shows at each t<=20000 that P_t(300) has the phase B_t followed by at least 72 complete phase-W_t copies; by symmetry the other side is reflected, and the intervening centre is palindromic. In particular the lemma's r>=1 guard holds at every t<20000. The initial identity P_0(q)=I_0^(q-300)(P_0(300)) is literal. Inductively applying the one-step lemma for each additional inserted copy (each intermediate word still has at least 72 bands) yields P_t(q)=I_(t mod8)^(q-300)(P_t(300)) for every t<=20000 and every integer q>=300. All caps remain B_t and the number of complete W_t bands is at least 72+q-300=q-228. At each of the eight phases B_t contains at least one odd coefficient, and therefore no corresponding integer can be a palindrome. This proves the quantified finite-horizon claim, without guessing from a few experimental q values.

## Independent controls and reproduction
Previous base q=300: independent true decimal digit-vector and GMP mpz_class 20,000-step replays; final 22,078 digits, 10,000 overflows, min72 bands, FNV64=10989435956851471335.
New base q=301: complete direct decimal digit-vector 20,000-step replay has final 22,118 digits, min73 bands, same 10,000 overflow bits, FNV64=2676930820902518277. Separate GMP code in gmp_check.cpp repeats ALL 20,000 steps and independently checks the identical result. Base q=320 actual digit-vector test also has 10,000 overflows and min92 bands, final 22,878 digits and FNV64=6916198416407145479.
The additional uniform_pairword.cpp independently computes two different ordinary integer sequences q=300 and q=301, forms their complete symmetric pairwords at every t=0..20000, and checks literal equality with the phase-correct inserted word. Every one of 20,001 comparisons passes, not just exterior windows or checksums. Changing one phase coefficient causes a failure at t=0 as a negative control.
Reproduce from repository root:
    sh calculation/new_structures/agent-W07/uniform_run.sh
The script compiles C++17 sources and GMP, executes the previous W07 base-q=300 inverse/fibre/long-orbit regressions, the new pairword identity and corruption control, and a full independent q=301 GMP replay. No Lean files have been changed, and no Lean verification is asserted.

## Remaining gap
The certified horizon 20,000 is independent of q, which is a *uniform finite horizon*, not a fixed-seed infinite guarantee. The inward front still consumes a finite portion of the lattice. A genuine decimal Lychrel certificate would require an inductive renewal condition that prevents such consumption forever. Backward search should enforce future centre compatibility across multiple steps, not merely inflate the number of digit-split ancestors merging at the first step.
