# Agent N17: a decimal travelling particle with a wake

**Status: COMPUTED** for the 20,000-step candidate and 44-step empirical comoving relation; **PAPER PROOF** for the stated local carry rule and finite-speed shielding lemma. No infinite decimal Lychrel number or Lean theorem is claimed.

## Explicit seed and replay

All coefficient words are least-significant-first. Let \(A_0(i)\) have a 39-column rooted prefix

\`17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13\`

followed by the spatial period-20 word

\`17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13\`.

For each \(h\ge39\), set \(P_0=A_0[0:h]++\operatorname{reverse}(A_0[0:h])\). At each mirrored digit pair \(i,2h-1-i\), choose \(d_i=\max(0,P_i-9)\), \(d_{2h-1-i}=P_i-d_i\). Then \(N_h\) is a positive \(2h\)-digit decimal integer. No giant literal seed is required; both programs construct it.

For \(h=8000\), independent literal digit-vector and GMP \`mpz\` big-integer reverse-and-add programs replayed 20,000 steps and checked every state for palindromes. They agree: overflow repeats 10101010, length goes from 16,000 to 26,000, no palindrome, rooted temporal 8-phase prefix persists to at least position 3,467, and the first odd coefficient of each 8-phase exterior sits at index 0,1,0,4,0,7,0,2. The outer word is spatially periodic of period 20 after column 39; the *centre is not fixed-width or spatially periodic*.

Define \(f_t\) as the first index where the lower-half pairword differs from the phase-\(t\bmod8\) exterior. After transient, for all recorded \(644\le t\le20000\), \(f_t=f_{t-44}-10\), and \(P_t[f_t-20:f_t+40]=P_{t-44}[f_{t-44}-20:f_{t-44}+40]\). This was checked on **every** step (19,357 comparisons), not sampled. The 60-cell head is a spacetime particle moving outward at exactly 10 cells per 44 steps on this finite horizon, while a much longer, nonrepeating wake remains behind. Deeper than about 40 cells behind the head, the comoving words are not generally equal. This is *not* an all-time 44-step periodic global template.

The breakdown mechanism is concrete: the head moves toward the low-index root, eventually eroding the finite protected band. For \(h=250,500,1000,2000\), the first root-prefix (<39 cells) departure occurs at steps 940,2084,4284,8684. These are not palindrome hits. This suggests looking for a defect whose velocity has the opposite sign, or for a wake-emitting boundary that continually replenishes protected cells.

## Exact semi-infinite folded carry rule

For a palindromic pairword \(P_i=d_i+d_{n-1-i}\), let \(\ell_0=0,\ \ell_{i+1}=\lfloor(P_i+\ell_i)/10\rfloor\), and let \(r_i=c_{n-i}\) be the carry from the mirrored high side, so \(r_i=\lfloor(P_i+r_{i+1})/10\rfloor\). The top overflow is \(\gamma=r_0\). If \(\gamma=0\), then
\[
P'_i=2P_i+\ell_i+r_{i+1}-10(\ell_{i+1}+r_i).
\]
If \(\gamma=1\), then \(P'_0=P_0-10\ell_1+1\) and for \(i\ge1\),
\[
P'_i=P_i+P_{i-1}+\ell_i+r_i-10(\ell_{i+1}+r_{i-1}).
\]
These identities follow by adding the two mirrored normalized digits and account for the changing palindrome axis. Since \(\lfloor(9+c)/10\rfloor=c\), while every other coefficient \(P_i\ne9\) resets the carry regardless of input, the right-side \(r_i\) is uniquely determined on this semi-infinite background. \`semica.py\` independently constructs its eight temporal rows from eight ordinary steps, verifies their spatial period after column 39, the 8-step closed folded recurrence on 700 columns, the alternating overflow, absence of adjacent 9s in the bulk, and the odd witnesses. Periodicity of the carries beyond column 41 reduces the infinite algebraic closure to finitely many column identities.

## Finite-speed shielding lemma (PAPER PROOF)

Suppose the first \(L\) mirrored coefficients of a finite decimal seed agree with the semi-infinite exterior \(A_t\), with \(L\ge41\) so that the final two protected coefficients \(A_t(L-2),A_t(L-1)\) lie in the period-20 bulk and are not both 9; also suppose \(2L\le n\). Both low-side digit carries up to index \(L\) are then fixed by the prefix. The high-side carry at each mirrored position \(i\le L-3\) is fixed by the shared non-9 coefficient at \(L-2\) or \(L-1\); this resets any unknown carry arriving from the centre. The high-side terms in both the \(\gamma=0\) and \(\gamma=1\) formulas are therefore determined. Consequently the overflow is fixed and the exact formulas imply that the next pairword agrees with \(A_{t+1}\) through at least \(L-2\) coefficients. Reflection and nonnegative length growth preserve disjointness. By induction, the first \(h-2t\) positions of \(N_h\)'s pairword agree with \(A_{t\bmod8}\), so its odd outer coefficient proves non-palindromicity whenever \(h-2t\ge39\). At each induction step before the last one, \(L\ge41\), so the trailing reset condition persists. Thus *for every prescribed finite horizon \(T\)*, choosing \(h\ge2T+39\) constructs a decimal integer nonpalindromic throughout steps \(0,\ldots,T\). This does **not** produce one fixed integer surviving all \(T\).

## Reproduction

Run \`bash calculation/new_structures/agent-N17/run.sh\` from repository root. Standalone:
\`python3 calculation/new_structures/agent-N17/semica.py\`,
\`g++ -O3 -std=c++17 calculation/new_structures/agent-N17/particle.cpp -o /tmp/n17p && /tmp/n17p 8000 20000\`,
\`g++ -O3 -std=c++17 calculation/new_structures/agent-N17/independent_gmp.cpp -lgmp -o /tmp/n17g && /tmp/n17g 8000 20000 /tmp/n17g.csv\`.
Controls: \`/tmp/n17p 500 1000\`; changing \(h\) to 250/500/1000/2000 and extending time reproduces the finite-band erosion onset. \`samples.csv\` records the independent big-integer milestones. No external input files or packages other than a C++ compiler, Python 3 and GMP are required.
