# Agent N14: clock-lifted carry strips for decimal long overflow words

## Exact local structure (PAPER PROOF)
All pair coefficients are least-significant first, x[t,k] in 0..2b-2.
Let g[t] be the high overflow bit in normalizing a palindromic pairword, l[t,0]=0 the low carry, and h[t,k] the carry entering the mirror of column k from the middle. The high overflow equals h[t,-1]=g[t]. For a column sufficiently far from the centre:
\`\`\`
l[t,k+1] = floor((x[t,k]+l[t,k])/b)
h[t,k-1] = floor((x[t,k]+h[t,k])/b)
x[t+1,k] = (x[t,k]+l[t,k]) mod b
           + (g[t] ? (k==0 ? 1 : (x[t,k-1]+h[t,k-1]) mod b)
                   : (x[t,k]+h[t,k]) mod b).
\`\`\`
Proof: the two summands are exactly the low and reflected high digits of the normalized pairword; if g=1 the reflected partner shifts by one. The centre is excluded from this local theorem. This also gives an independent ordinary-integer test for any finite-width strip: append a single symmetric coefficient 0 or 2b-2 to force the desired h[t,K-1] for that one transition. **These caps may differ between steps; this does not produce an orbit.**

## Clock-lifted transfer (PAPER PROOF)
Suppose g, the entering low-carry stream L, the required high-carry stream H and (when g=1) the shifted partner stream Y have time period p. At a new spatial column the pair coefficient z_t belongs to 0..2b-2 and the unknown incoming carry u_t to {0,1}. Require floor((z_t+u_t)/b)=H_t, and update z_(t+1)=(z_t+L_t) mod b + (g_t?Y_t:(z_t+u_t) mod b). Compute the Boolean one-period relation R subset {0..2b-2}² by composing these finite transition rules p times. An infinite temporal extension exists, with the upper carry freely supplied, **if and only if** the directed graph R has a cycle. A shortest cycle of length r yields a sound extension of temporal period rp, with 1<=r<=2b-1. Proof: concatenate witnessing p-step paths around the R-cycle; conversely a never-dead path in the finite (t mod p,z) graph repeats a state and yields a directed cycle. This is a time-clock-lifting representation, NOT a complete pairword certificate; a legitimate centre must supply every chosen u_t coherently and its mirror must be checked.

Concrete positive control (base 10): g=01, L=(1,0), H=(1,1), Y=(-1,8) has NO length-one R-loop but has a length-two R-cycle. The resulting 4-step coefficient stream is (17,16,14,9). The boundary is not known to be reachable from a root. This shows why searching only for an extension with unchanged temporal period is incomplete.

## Base-10 rooted observation (COMPUTED, exact scope)
\`decimal_p72_w5.txt\` contains a p=72 primitive g stream, all five lower spatial pair-column values at 72 times, and a deliberately free upper carry stream. The rooted lower carry is 0, the overflow condition is enforced at the first column, and each column follows the local equations. \`independent_check.py\` independently constructs a symmetric finite pairword for EACH t, forces its carry using a one-column cap, calculates the complete ordinary Python integer, and tests all 72 normalizations; 72/72 pass. Flipping top carry bit 0 is rejected. This is a precise *boundary-driven, time-periodic strip*, not an indefinitely evolving decimal number.

For this same input, \`transfer.py\` propagates ALL 19 possible sixth-column coefficients and both upper carry choices. Reachable-set sizes for time transitions 0..9 are 18,10,11,10,3,3,2,2,2,0. Thus the sixth column cannot sustain even 10 transitions, regardless of its initial coefficient or upper carry. This is the exact failure, not an exclusion theorem for all possible decimal strips.

A genuine initial integer **110102959969697** has the stored strip as its first five pair-coefficient columns at times t=0..9, but at t=10 its pair prefix is (16,17,2,6,6), instead of target (16,17,2,6,7). This ordinary integer is nonpalindromic for steps 0..20000 (separate independent C++ digit-vector replay, 8279 final digits). **It does not preserve the claimed pairword shape for 20000 steps, and there is no Lychrel certificate.**

## Reproduction and next construction
Run from repo root:
\`\`\`
python3 calculation/new_structures/agent-N14/generate.py > /tmp/n14-witness.txt
diff -u calculation/new_structures/agent-N14/decimal_p72_w5.txt /tmp/n14-witness.txt
python3 calculation/new_structures/agent-N14/independent_check.py
python3 calculation/new_structures/agent-N14/transfer.py
g++ -O3 -std=c++17 calculation/new_structures/agent-N14/replay20k.cpp -o /tmp/n14-replay
/tmp/n14-replay 110102959969697 20000
\`\`\`
Expected: diff empty; independent PASS; transfer PASS (clock lift 2 and sixth-column horizon 10); \`first_pal=-1 nonpal_checked=20001 last_digits=8279\`.
**Redirect:** Do not make more fixed-p temporal strip censuses. Instead, co-synthesize the next column and its carry within the temporal beam, and admit period multiplication whenever R requires it. A full base-10 proof still needs a finite spatial pump, a coherent mirror seam, and a globally nonpalindromic step cycle. A Lean proof could first formalize the local equations and the finite R-cycle concatenation; no Lean verification is claimed.
