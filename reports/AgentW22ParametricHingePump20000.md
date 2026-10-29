# W22: exact antipodal 9-insertion pumping and a uniform 20k decimal family

## Scope and label

**PAPER PROOF**: universal one-step base-10 symmetric-neutral-9 insertion lemma below, all k >= 0. **COMPUTED**: 20,000 verified instances of its guard along the explicit W22 base trajectory; exact per-edge k=1 commutation checked on all 20,000 edges, separate k=37 spot controls and independent 20,000-step ordinary-decimal replays for k=1 and k=37. The resulting conclusion applies to every k>=0 for 20,000 steps only, NOT an infinite decimal Lychrel certificate or Lean proof.

## One-step insertion lemma

Let P be any legitimate symmetric base-10 pair coefficient word with length n and entries 0..18. Let T(P) be the normalized-digit pairword after one genuine reverse-and-add step, including the possible leading overflow gamma in {0,1}. Pick a site j strictly in the first half with P[j-1], P[j], P[j+1] all equal to 9, and the reflected three coefficients likewise 9. Let c_low be the incoming normalization carry before P[j], and c_up before P[n-j]. Assume c_low+c_up=1.

Define I_j^k(P) by inserting k copies of 9 immediately before P[j] and k copies before P[n-j], symmetrically. Then gamma(I_j^k(P))=gamma(P) and

T(I_j^k(P)) = I_j^k(T(P))    for every integer k>=0,

provided j is strictly interior enough for the high-side shifted partner on gamma=1 to remain in the 9-run (the three-neighbour guard above suffices). The insertion leaves leading digits and original centre parity unchanged.

### Proof

Carry recurrence at a coefficient 9 is c_next=floor((9+c)/10)=c for either c=0 or1. Inserting any number of 9s within the two reflected 9-runs therefore inserts normalized digits u=9(1-c_low) and v=9(1-c_up), does not alter ANY original normalized digit or the final carry, and has u+v=9. When gamma=0 the two newly inserted output digits pair directly and create one inserted pair coefficient 9 (per inserted pair), leaving every original paired coefficient unchanged. When gamma=1 the high partner is shifted by one position: each inserted digit meets the adjacent original digit of the same constant run rather than its directly inserted opposite. Both sums are again u+v=9; all pairs outside the insertion neighbourhood are identical, and the original pair coefficient at the boundary site j was already 9. Hence the same exact insertion of 9 in T(P) occurs. Repeat the one-cell argument k times; carry and the three-neighbour run guard are preserved. This proves the universal lemma.

No assumption that the finite outer bulk is periodic, or that a 9 run exists for all future time, is made by the lemma.

## Verified fixed-site corridor and induction

The baseline seed P0 = 8^14000 9^8000 10^16000 9^8000 8^14000 and its 20,001 exact integer states were first established in AgentW22AntiphaseNineHinge20000. The new checker independently generates the exact pairword orbit and at every t=0..19,999 scans the full carry recurrence and proves numerically:
- fixed first-half index j=21750 lies at least 201 cells inside the selected 9 run;
- c_low+c_up=1 at the two insertion sites, for all 20,000 checked edges;
- full-word T(I_j(P_t))=I_j(T(P_t)), with the same gamma, on every one of 20,000 edges;
- gamma cumulative 8296, and the max start / min end of the 9 runs across states t=0..20000 are 21549 / 22000. Thus the common fixed insertion interval is [21549,22000), and j lies safely in it.

At the seven times 0,1,2,5000,10000,15000,19999, k=37 commutation is checked independently by constructing and normalizing the entire +74-coefficient pairword.

Induct on t using the exact one-step lemma: for any k>=0, T^t(I_j^k(P0))=I_j^k(T^t(P0)) for all t<=20000. Because all base states retain a 9 and insertion adds only 9s, every extended actual integer is nonpalindromic. Because the overflow is unchanged at every edge, its decimal length is 60000+2k initially and 68296+2k after 20000 steps; the 8296-overflow clock is independent of k. Valid actual decimal seeds exist: split each paired coefficient p as low min(p,9), high p-min(p,9), except outermost p0=8 as low0/high8. This keeps the leading digit nonzero for all k.

## Independent positive and negative controls

A separate program hinge_fast.cpp performs complete schoolbook decimal reverse-add and full pairword equality at every step, with 20,000-step replays for k=1 and k=37. Observed final 9-run lengths respectively 1199 and 1235; both have final A half-run 654, B half-run 1344, length 68298 or 68370, and overflow count 8296. The same-phase (8/8) negative control correctly violates the pump identity: the 9 corridor becomes 18, rather than 9.

## What remains

This uniform theorem is only a finite-horizon result: for any fixed k, the outer A and central B finite reservoirs and the growing interface defects have not been proved to renew forever. Insertion produces more neutral resource but no source replenishing the two six-clock bulks. An infinite certificate needs a periodic emission mechanism or a genuine inductive renewable seam, not merely a larger k.
