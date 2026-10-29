# Agent W08: Universal unknown-centre 88-step triple renewal

Label: **PAPER PROOF** of the general two-ended carry-cone rule, with a finite **COMPUTED** certificate trace. This is a finite-time base-10 result, NOT a Lychrel certificate.

## Claim and exact witness
Coefficient words are least-significant first. Set
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
and W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13].
Take U of length 144 with all entries 1 except U[13]=7,U[20]=7,U[30]=6 and put A=[8,0,0]++U (length 147).
For ANY palindromic coefficient word Z with entries 0..18, and an even midpoint if |Z| is odd, let
P0=B++W++A++Z++reverse(A)++reverse(W)++reverse(B).
There is a positive decimal integer whose digit-pair word is P0 (pick the low digit min(9,p) and the high digit p-min(9,p), midpoint p/2). The leading digit is 8.
Let N_(t+1)=N_t+reverse10(N_t), and Pt be the palindromic digit-pair word of Nt.

For EVERY such Z, t=0..264 has nonpalindromic Nt and digit-length overflow gamma_t=1 for even t and 0 for odd t (t<264). At t=88j for j=0,1,2,3, Pt=B++W++Cj++reverse(W)++reverse(B), where Cj is palindromic and |Cj|=294+|Z|+44j.
Thus the *same* two-scale period-20 band is regenerated at THREE 88-step checkpoints for all unknown centres. This does not claim Cj is constant, that renewal occurs at j=4, or that any integer has an infinite palindrome-free orbit.

## Sound two-ended carry-cone rule (paper proof)
Suppose an n-coefficient palindromic pairword P over 0..18 has known low prefix p of length L and therefore known high suffix reverse(p), with 2L<=n. Every possible middle contributes a carry c in {0,1} upon entering that high suffix. Normalize the known low prefix from carry 0 to obtain low[i]; normalize reverse(p) with carry c=0 and c=1 to obtain high_c[j] and overflow gamma_c. If gamma_0=gamma_1=g, the next pairword has fixed length n+g and its low coefficient at i<L is
low[i] + (1 if g=1 and i=0 else high_c[L-i-(0 if g else 1)]).
This coefficient is independent of all middle entries whenever both choices of c give the same value. Keep the maximal consecutive prefix of such certified coefficients. Every possible next pairword is palindromic and has the returned known prefix. The rule is sound by ordinary column-wise carry arithmetic. In particular, no unknown middle value is replaced by a guessed digit; only the two legitimate incoming carries are considered. Repeat inductively; validity of the length premise follows from the returned lengths in the finite trace.

The portable script affine_cone.py implements this exact rule and requires at EACH of the 265 states: (a) at least 39 known low coefficients; (b) repetition of the eight initial 39-coefficient temporal rows; (c) an odd coefficient among those 39; (d) g_t matching 10101010; (e) B++W known at t=88,176,264. A palindrome necessarily has all digit-pair coefficients even, so (c) excludes every palindrome. The fixed B++W prefix at checkpoints and pairword reflection give the full claimed template with central length n_t-118. No finite bound is imposed on |Z|; it appears only in n_0=412+|Z|, and the same proof uses only 2L<=n_t, true for all |Z|>=0. Hence one finite trace establishes the universal claim, not just its 45 examples.

## Exact output and controls
At times 0,88,176,264, the numbers of certified prefix coefficients are [206,162,114,67]; overflow count=132 and the first known odd-coefficient witness positions for phases 0..7 are [0,1,0,4,0,7,0,2].
Command from repo root:
python3 calculation/new_structures/agent-W08/affine_cone.py
Expected compact JSON is in calculation/new_structures/agent-W08/expectation.json.
An independent ordinary Python big-integer engine (decimal text reverse and addition, not the pair-coefficient recurrence) constructs 45 integer seeds, with nine independently randomized palindromic central lengths 0,1,2,3,7,17,47,180,600, and checks every one of the 265 states, the 8-phase root, three band-return checkpoints, growth and nonpalindromicity. It also mutates U[13] to 6 and observes a failure of the 176-step band return.
Run: (cd calculation/new_structures/agent-W08 && python3 ordinary_integer_check.py)
Python 3 standard library only. No Lean compilation performed.

## Why this is a two-scale result and what fails
The exterior has spatial period 20; the three successful macro renewals are separated by 88 time steps, and at each such renewal the arbitrary inner centre has grown by 44 pair coefficients. Unlike a numeric identity N_(t+88)=10^m*N_t, this renormalization is an exact **affine word template return with a growing central register**.
For the Z=[] control, direct decimal replay to step 352 gives only the first 2 of the 20 W coefficients at the attempted fourth return (P352[39:59]=[17,3,2,0,6,18,1,7,12,11,1,18,10,8,5,16,5,9,17,8]); a fourth renewal is not established. This failure redirects further construction toward an additional, independently programmable inner guard rather than extrapolating the 88-step rule.

A Lean translation would define an inductive prefix specification, prove the two-carry step lemma using norm_append, and check the 264 explicit prefix rows with decide or a verified Boolean checker. This report does NOT claim LEAN-VERIFIED status.
