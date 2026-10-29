# Agent X16: nonperiodic all-width forced-carry reset with two neutral ports

**PAPER PROOF (identities for all k>=0), COMPUTED (3001 width regressions).** This is a new local mechanism, **not** a decimal infinite certificate. Its significance is that an arbitrarily wide Thue-Morse centre collapses to a carry-forced alphabet with just **two neutral coefficient-9 ports** after three genuine reverse-and-add steps. Builds on `AgentX16AutomaticCarryRibbon` without claiming a closed cycle.

Let `u(i)=popcount(i) mod 2`, `n=2k+8`, `h=n/2` and start with palindromic base-10 pair coefficients `P0_i=17-3*u(min(i,n-1-i))` for 0<=i<n. Every such pairword has a positive integer realization. Normalization from these coefficients computes the exact next number, independent of which realization is chosen. Write `P_t` for the next pairword and `c_t(i)` for its carry entering digit column i.

**Time 0:** Every P0 coefficient is 14 or 17; `c0(0)=0`, and `c0(i)=1` for `1<=i<=n`, so `gamma0=1`. The first output digits are `7`, followed by `P0_i-9` for 1<=i<n, then an overflow 1.

**Time 1:** Length n+1. `P1_0=P1_n=8`; for 1<=i<h, `P1_i=16-3*(u(i)+u(i-1))` (10,13,16); at i=h the centre is `16-6*u(h-1)` and the rest is mirrored. In particular P1_1=13. Therefore `c1=(0,0,1,1,...,1,0)` with n-1 middle ones, and `gamma1=0`. Normalization yields digit endpoints `(8,3,...,9)`.

**Time 2:** Length n+1. `P2_0=P2_n=17`, `P2_1=P2_(n-1)=7`, and for 2<=i<=n-2, `P2_i=2*(P1_i-9)` lies in the **neutral-free** alphabet {2,8,14}. The carry is entirely forced: `c2(0)=0`, `c2(1)=1`, `c2(2)=0`, `c2(i+1)=1 iff P2_i=14` for 2<=i<=n-2, `c2(n)=0`, `c2(n+1)=1`. This is an explicit 2-automatic *carry ribbon* from adjacent Thue-Morse bits (its bits in the lower half are `u(i)=u(i-1)=0`), without scanning any unbounded carry-9 runs. `gamma2=1`.

**Time 3:** Length n+2. The output pairword starts `P3_0=8`, `P3_1=15`, `P3_2=9` and is mirrored. For 3<=i<=n-2 let `A=P2_i`, `B=P2_(i-1)`, and `f(x)=1 if x=14 else 0`; the symmetric two-sided carry formula gives `P3_i=A+B-9*(f(A)+f(B))`. Since `x-9*f(x)` lies in {2,8,5}, every such interior coefficient lies in {4,7,10,13,16}. Therefore the **only** neutral coefficients P3_i=9 are at the two symmetric ports i=2 and i=n-1, for *every k*. The four states t=0,1,2,3 are nonpalindromic by odd-pair witnesses (17,13,17,15 respectively), and the exact first overflow schedule is 1,0,1.

This is a constructive two-port carry-reset gadget for arbitrary, nonperiodic centre width, not a loop. **What breaks:** those two 9-ports can transmit carries in the following step, and the next P4 phase has not been shown to regenerate the same two-port template. Redirect the search to an automatic return operator that feeds the two ports and restores the forced {2,8,14} interior after a longer macrocycle.

**Computed regression:** `python3 calculation/new_structures/agent-X16/forced_reset.py` checks all formulas against two independent ordinary-digit paths for k=0..3000 (source number lengths 8..6008) without any failure, including exactly two coefficient-9 sites at t=3. The universal statement is from the displayed algebra, not the finite tests. Same repository already contains the separate 20,000-step k=63 finite-survivor control, and base-9 B61/W4 check in `carry_ribbon.py`.

No Lean changes; the general `tools/verify.py --changed` cannot run in this isolated sandbox, which lacks the full Git checkout and pinned Lean toolchain.