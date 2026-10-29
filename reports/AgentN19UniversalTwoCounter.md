# Agent N19: all-width six-edge decimal counter transport via idempotent carry matrices

**PAPER PROOF** of the exact all-width decimal six-step symbolic pairword transport identity, by a finite Boolean transfer-matrix certificate; **COMPUTED** independent C++/Python controls below. The proof is conditional only on elementary base-10 carry arithmetic; it is not a decimal Lychrel certificate or a Lean proof.

## The statement

For every integer `k>=5`, define folded coefficient word (least-significant-first) `H_t(k) = L_t ++ [u_t]^(k-a_t) ++ J_t ++ [v_t]^(k-b_t) ++ R_t`, with the seven rows `(L,u,a,J,v,b,R)` specified in `reports/AgentN19CounterSynchronizedSixCycle.md`. Form its symmetric whole word `P_t(k)=H_t(k)++reverse(H_t(k))` at t=0,5,6 and `P_t(k)=H_t(k)++reverse(dropLast(H_t(k)))` at t=1,2,3,4. The central coefficient in the odd cases is even. Let `step` be the exact pairword digit-normalization/reversal map derived from `n+reverse(n)`. Then **for all k>=5 and all t=0..5, `step(P_t(k))=P_{t+1}(k)`**. The six overflows are `1,0,0,0,1,0` (initial length `4k+8`, final length `4k+10`). Every P_t contains an odd coefficient, so every one of the seven states is nonpalindromic for *any* physical realization of the pairwords. A canonical positive-leading seed is supplied by the earlier `counter_six.py`.

In particular the initial two synchronized block counters `(k,k)` become `(k-5,k-2)` after the six-step clock, with the **same** bulk symbols `(8,16)` at both ends of the clock. The difference of 3 proves a physical *counter-skew propagation* without postulating a periodic finite centre. This is an exact one-pass transport identity, **not a closed template cycle**: the finite outer/junction words also change.

## Why finitely many checks prove every k

The folded source/target edge is recognized by the exact two-ended carry NFA. At one paired position with coefficient x and next coefficient y, its state `(l,r,d)` comprises incoming low carry l, outgoing high carry r and the previous high output digit d. For guessed next high carry r' in {0,1}, require `l'=floor((x+l)/10)`, `r=floor((x+r')/10)`, and `y=low+high` for overflow 0 or `y=low+previousHigh` for overflow 1 (the very first output instead uses the overflow digit 1). Here `low=(x+l)%10`, `high=(x+r')%10`; the centre terminal checks the meeting carries and the odd/even length case. There are exactly `2*2*10=40` ordinary states, and the first letter has a separate fixed initialization. This relation is sound and complete for actual decimal arithmetic by direct digit carry equations, not by extrapolating from simulations.

For each edge t and every k>=20, write the **actual aligned folded input/target pair columns** as

`Z_t(k)=Z_t(20)[:11] ++ z1_t^(k-20) ++ Z_t(20)[11:31] ++ z2_t^(k-20) ++ Z_t(20)[31:]`.

This is an exact *word identity*, not a numerical observation: the cut at index 10 lies strictly inside both first bulk runs at k=20 and the cut at index 30 lies strictly inside both second bulk runs; all seven definitions have fixed literal boundaries and their two corresponding exponent lengths each increase by 1 when k increases. Hence insertion of one pair column at each cut produces Z(k+1). The six `(z1,z2)` pairs are `(8,16)/(16,14)`, `(16,14)/(14,10)`, `(14,10)/(10,2)`, `(10,2)/(2,4)`, `(2,4)/(4,8)`, `(4,8)/(8,16)`.

The 40x40 Boolean transition matrices of **each** of these twelve columns satisfy `M^2=M` (the checker builds their complete matrices and compares powers with no missing states). Therefore for k>=21 both inserted repetitions are represented by the same matrices as k=21, while k=20 is the zero-extra-letter case. The checker accepts **both k=20 and k=21** for every edge, establishing **every k>=20**. It separately checks **k=5..19** by the complete finite carry NFA, so all k>=5 are proved. All four relevant even/odd, overflow/no-overflow terminal rules are explicit in the imported `fold_check.py` and independently tested by 20,000 random digit-list examples. The code also checks uncompressed and compressed relational acceptance at 20,21,22,33,44,66; exact phase shapes and direct Python bigint replays for k=5..20 are already in `counter_six.py`.

## Reproduce from the repository

```
python3 calculation/new_structures/agent-N19/unary_allk.py
python3 calculation/new_structures/agent-N19/fold_check.py
python3 calculation/new_structures/agent-N19/counter_six.py
```

The universal proof checker prints six `EDGE` lines, each with `(mu,period)=(1,1)` for *both* matrices, followed by `ALL SIX EDGES TRUE FOR EVERY INTEGER k>=5`. It does **not** use a width cap to infer a universal claim: the cap 64 in `eventual()` is only a fail-closed resource guard, and the actual matrices repeat at power 2 in every case. The existing six-phase propagation still does not provide a replenishing outer boundary, nondecreasing counter update, or an infinite decimal certificate. The next constructive target is to glue a second emitter to turn the measured counter skew into an expanding 2-counter cycle while retaining the odd-coefficient safety guard.