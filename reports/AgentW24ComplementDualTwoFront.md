# W24: complementary carry kink and a two-front decimal period-20 orbit

Labels: PAPER PROOF for the exact one-step base-b complement kink; COMPUTED for the finite 20,000-step decimal observation and independent controls. No Lean theorem and no infinite decimal Lychrel certificate.

## Exact dual-carry theorem (PAPER PROOF)

Let b>=3 and n>=2. Let P=(p_0,...,p_(n-1)) be a palindromic pair-coefficient word with all coefficients in [0,2b-2], and let Q_i=2(b-1)-P_i. Assume P has at least one coefficient !=b-1; write k for the first such index. Assume the paired realizations are positive base-b integers with n digits (both are realizable if the outer p_0 is in [1,2b-3], and for odd n the centre coefficient must be even).

Normalize S=sum(P_i*b^i) and T=sum(Q_i*b^i), and pad both base-b digit strings to length n+1, least significant first: s_0..s_n and t_0..t_n. Then for every i:
- i<k: s_i+t_i=2(b-1);
- i=k: s_i+t_i=b-2;
- k<i<n: s_i+t_i=b-1;
- i=n: s_i+t_i=1.
Exactly ONE of S and T gains a leading digit on normalization. Their sum is exactly 2(b^n-1). This is an explicitly located single carry-kink, independent of the entire unspecified interior word.

Proof: before k, the two carries entering each position are (0,0), since the coefficient pair is (b-1,b-1). At k, exactly one outgoing carry becomes 1 and the other 0. Thereafter, if the incoming carries sum to 1, the outgoing carries also sum to 1 for every pair (p,2b-2-p) with p in [0,2b-2], including p=b-1. The sum of normalized output digits at position i is 2b-2 + (sum incoming carries) - b*(sum outgoing carries). The four displayed cases follow. Symmetry ensures the nonneutral position k precedes the top; hence the final carry sum remains 1. The all-(b-1) word is excluded since it immediately produces palindromes.

In decimal, with k=0, the two normalized outputs have digitwise sum [8,9,9,...,9,1] from low to high; their zero-padded *folded pairwords* therefore have coefficientwise sum [9,18,18,...,18,9]. IMPORTANT: this last relation uses a common padded length n+1; the canonical pairword of the shorter integer has a different mirror axis. Thus this is an **affine staggered-length symmetry**, not a false assertion that reverse-and-add commutes with reversal or digit complementation. Indeed F(rev N)=F(N), rather than F(rev N)=rev(F(N)).

This gives a certificate-design primitive with an exact neutral 9-sum bulk and a single two-track carry junction. To obtain an infinite certificate, a finite grammar or carry transducer must sustain/renew this junction across arbitrary future time and keep a fixed physical track nonpalindromic. Neither requirement is proved by this lemma.

## New concrete decimal two-front mechanism (COMPUTED)

Use the FIRST SCC of calculation/decimal_frontier/lattice_formats/p8_scc.txt: its time-0 rooted path B has length 39 and spatial-periodic W has length 20. Define H_q = (18-B) ++ (18-W)^q, where subtraction is entrywise, and P_q = H_q ++ reverse(H_q). Construct a physical decimal seed with digit at lower index i equal to max(0,P_q[i]-9) and its reflected digit equal to min(9,P_q[i]); it has 78+40q digits and leading digit 1. This is a genuinely different trajectory from the original N02 seed, which uses the uncomplemented pairword. Unlike the N02 periodic exterior rooted at column 39, this companion develops an additional OUTER advancing defect front.

For q=900, the independent C++ digit-array reverse-and-add engine and GNU GMP mpz_class base-10 integer engine produced **identical complete integers after every one of 20,000 additions**. Every state t=0..20000 was explicitly tested for digit palindrome and had none. At every state we computed the longest contiguous run of positions i in the lower half for which P_t[i]=P_t[i+20], with i+20 also in the lower half; its minimum size was 2732. These coefficients define a genuine period-20 word on a long open interval, not merely an aggregate count. No assumed theoretical recurrence is used to evolve either integer.

Selected checkpoints: t=0: digits=36078, run=[35,18019), length=17984; t=88: digits=36116, run=[92,18006), length=17914; t=1000: digits=36498, run=[640,17846), length=17206; t=5000: digits=38177, run=[3006,17144), length=14138; t=10000: digits=40229, run=[5930,16294), length=10364; t=15000: digits=42297, run=[8873,15410), length=6537; t=20000: digits=44400, run=[11844,14576), length=2732. Full checkpoint hashes and the precise initial recipe are in dual_observations.json and dual_front.cpp.

The two-front phenomenon differs from a centre-only eroding p8 exterior: the complementary starting pairword destroys rooted phase locking, yet the spatial-period-20 bulk survives in between two opposite invading fronts for at least 20,000 steps. Numerically the left run bound moves from 35 to 11844 while the right bound moves from 18019 to 14576. Those are endpoint measurements, NOT a proven constant wall velocity or an eventual recurrence. The band shrinks and is not self-replenishing. The search must therefore target a **complement-kink emitter** or an *anti-complementary two-track renewal* that creates more than the two invading fronts consume per macroperiod.

## Reproduction and exact scope

From the repository root:

    python3 calculation/new_structures/agent-W24/complement_carry.py
    g++ -O3 -std=c++17 -Wall -Wextra calculation/new_structures/agent-W24/dual_front.cpp -lgmpxx -lgmp -o /tmp/w24dual
    /tmp/w24dual 30 300
    /tmp/w24dual 900 20000 > /tmp/w24_dual_replay.json

The Python checker exhaustively checks all paired six-coefficient palindromic pairwords with nonzero-leading realizations in each base 3..21, plus 10,000 seeded random larger words in bases 3..97, against independent physical reverse-add integer arithmetic; 373,812 checks pass. The C++ program checks complete GMP-vs-digit-vector equality at EVERY time, not sampled times. The 20,000-step data are finite and do not prove a decimal Lychrel number. No claim is made for q other than those actually executed, for all time, or for the original 196 seed. GitHub clone / full repository verify.py --changed were unavailable locally; no Lean files are included.
