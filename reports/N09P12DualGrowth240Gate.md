# N09: p12/m9–U3 simultaneous-growth renewal clock (PAPER PROOF)

**Scope.** This is a necessary condition for an exact **all-counter, literal full-interface** positive-growth decimal template return. No decimal Lychrel number, all-step nonpalindromic orbit, physical returning seam, or sufficiency is claimed. Finite integer controls are just arithmetic regressions.

## Statement

Use the published **rooted** p12/m9 exterior coefficients (LSB-first)
\`B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]\`,
\`W=[5,18,4,8,1,15,4,0,5]\`, so |W|=9, sum(W)=60. Choose any charge-zero p12-compatible inner period-three word
\`U=[9,a,18-a]\` (even a in 0..18), so |U|=3, sum(U)=27.
Let J be an arbitrary **fixed literal** seam and C a fixed palindromic centre with physically realizable middle coefficient. Let
\`H(q,k)=B++W^q++J++U^k\` and \`P(q,k)=H(q,k)++C++reverse(H(q,k))\`.

Assume that for every pair of sufficiently large **independent** counters (q,k), a genuine ordinary decimal reverse-and-add trajectory starting from a canonical positive integer having pairword P(q,k) follows the physically rooted p12 overflow clock (30 leading overflows in every 120 steps), and after **T=120r** steps, r>=1, returns to the same literal B,W,J,U,C with counters (q+Δq,k+Δk) for **fixed integers** Δq,Δk independent of q,k. Then necessarily
\[
3\Delta q+\Delta k=5r,\quad \Delta q\equiv0\pmod3.
\]
Equivalently, for a unique integer s,
\[
(\Delta q,\Delta k)=(3s,5r-9s).
\]
If both counters must be nondepleting indefinitely, s>=0 and 5r-9s>=0. If BOTH must grow strictly, the **first arithmetically possible** 120-multiple is **T=240** and the unique two-positive vector at T=240 is \`(Δq,Δk)=(3,1)\`. At T=120, the sole nonnegative vector is (0,5), so any physical repair with both positive counters must use a genuinely different macro-clock.

The result is conditional on a **literal phase-0 full-interface return** and the actual p12 overflow clock; phase-twisted returns, changing J/C during a macro without ultimately returning them, or a different overflow clock require a separate analysis. This arithmetic theorem does not supply the missing physical carry-port or central repair.

## Proof (all widths, all times under stated return hypothesis)

The length of the symmetric source pairword is \`2(34+9q+|J|+3k)+|C|\`. A fixed-cap return therefore changes decimal length by \`2(9Δq+3Δk)\`. The assumed actual 120r p12 clock has 30r overflows, each increasing the canonical integer's length by one. Hence \`18Δq+6Δk=30r\`, giving \`3Δq+Δk=5r\`.

Let \`S(P)\` be the integer sum of all coefficient entries of P. For any canonical base-10 integer N with pairword P(N), \`S(P(N))≡N+reverse(N)≡2N(mod9)\`. Since reverse(N)≡N(mod9), reverse-and-add sends \`N→2N(mod9)\`. Thus over 120r genuine steps \`S(P_next)≡2^(120r)S(P_original)≡S(P_original)(mod9)\` because 2^6≡1(mod9). Under the literal full-interface return, the only change in S(P) is \`2·60·Δq+2·27·Δk\`, so \`120Δq+54Δk≡3Δq≡0(mod9)\`. Hence \`3|Δq\`; substitute Δq=3s to obtain Δk=5r−9s. For r=1, nonnegative integer s permits only s=0; r=2 permits s=0 or1 and the sole both-positive case is s=1. Every assertion holds for arbitrary counter widths: no finite replay appears in the proof.

## Concrete physically canonical controls (not a return)

A separately implemented Python program constructs a **canonical positive decimal integer** with the complete symmetric pairword P, checks its actual pairword by ordinary decimal digit reversal, then performs 240 independent true-integer reverse-add steps. It uses J=(2,2), U=(9,8,10), C=(0), eight independent widths q=20/40/80/160, k=80/240; source mod11 is zero, the actual overflow count is 60, and returned word and hypothesized positive-growth target have identical length and mod9 coefficient mass. But each comparison still has **461** incorrect coefficients, first at index \`9q−8\`, before the W/U junction. Thus no candidate return is claimed.

Reproduce from repository root:
\`python3 calculation/new_structures/agent-N09/p12_joint240_gate.py\`.

## Research consequence and single missing lemma

For the rooted p12/m9 plus charge-zero U3 route, search for a **canonical full-interface 240-step return with W9 exponent gain +3 and U3 gain +1**, preserving the entire two-ended carry-port and every intermediate nonpalindrome guard for **all sufficiently large independent counters**. Alternatively, find a finite sequence of macro phases whose total drift satisfies the same equation with r>2 and is positive in both coordinates. Neither physical repair is established here.

Relation to prior art: Q01's \`docs/CERT_SPEC_Q01.md\` establishes the one-band temporal/length and mod9 gates; Q07 and Q39 establish the rooted 72-/120-edge inner-U3-only charge/phase targets. This report specializes the **two independent band counts** and gives their simultaneous-growth Diophantine clock, not an exterior census or another finite-horizon result.
