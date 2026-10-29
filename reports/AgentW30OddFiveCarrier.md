# Agent W30: a phase-40 odd five-site carrier in decimal pairword space

## Labels and exact scope

**PAPER PROOF** for the local carry-elimination identity below. **COMPUTED** for the five-cell wave and for an independent 20,000-step full integer replay. **UNDECIDED** whether any infinite decimal orbit realizes the carrier with a perpetually nonempty guarded region. This is not a proof that 196 (or another number) is a Lychrel number. No Lean theorem is claimed.

## A piecewise-affine bulk rule (valid for either overflow bit)

Let `P=[p_0,...,p_(n-1)]` be the palindromic decimal pairword `p_i=d_i+d_(n-1-i)`, with entries 0..18, ordered least significant first. Its normalization gives `a_i=(p_i+c_i) mod 10`, `c_(i+1)=floor((p_i+c_i)/10)`, `c_0=0`, and overflow `gamma=c_n` (zero or one). The new pairword is `P'_i=a_i+a_(n+gamma-1-i)` for a non-overflow digit index `i`. Put `h(x)=1` when `x>=10`, otherwise 0. When `x!=9`, `floor((x+c)/10)=h(x)` for *either* incoming carry `c in {0,1}`. Thus the relevant carries around a low-index site are functions only of three adjacent input coefficients.

For `1<=i<=floor(n/2)-2` with `p_(i-1),p_i,p_(i+1) != 9`, substitution yields exact equations:

```
gamma=0: P'_i = 2*p_i + h(p_(i-1)) + h(p_(i+1)) - 20*h(p_i)
gamma=1: P'_i = p_i + p_(i-1) - 9*(h(p_i)+h(p_(i-1)))
```

The second line uses the high-side partner at index `n-i`, not `n-1-i`. Both formulas are **exact identities** in the stated interior, not approximations, and define the two branches of a piecewise-affine cellular automaton on 9-free interior words. Unlike a general interval mask, each branch retains the exact correlation between neighbouring carry indicators and pairword entries. An interior periodic word with all 40 phases 9-free can therefore be checked with five symbols and a finite phase clock, independent of the surrounding centre.

## Positive 5-site phase wave

Set `V_0=(17,3,14,3,17)`. Apply the first branch when `t` is odd, the second when `t` is even, i.e. `gamma_t=1` for even `t` and 0 for odd `t`. Work cyclically on 5 sites. The eight rows before the first spatial translation are:

| t | row (low-index order) |
| --- | --- |
| 0 | 17,3,14,3,17 |
| 1 | 16,11,8,8,11 |
| 2 | 14,3,17,17,3 |
| 3 | 8,8,11,16,11 |
| 4 | 17,17,3,14,3 |
| 5 | 11,16,11,8,8 |
| 6 | 3,14,3,17,17 |
| 7 | 11,8,8,11,16 |

Every row has an odd coefficient, every row avoids the carry-exception coefficient 9, and for every `t`, `V_(t+8)[i] = V_t[(i-2) mod 5]`. Thus `V_40=V_0`. The row is **not a rooted period-five certificate**: establishing a matching canonical exterior/centre interface for all times remains necessary. This isolated bulk dynamics is not in conflict with the earlier reachable p8 exterior census (which found m20 and m48 rooted lattices).

## Concrete decimal integer and full checker

Use previously published `B0` (39 coefficients) and `W0` (20 coefficients) from `calculation/new_structures/agent-N10/phase.json` (also explicitly included in `replay.cpp`, so the program can run without a data loader). Set `q=300, k=4200`, `L=B0 ++ W0^q`, and:

```
P0 = L ++ V0^(2*k) ++ reverse(L).
```

`P0` is a palindromic coefficient word of length 54,078. To realize it as an actual decimal integer, for each mirror pair `(i,n-1-i)` with `i<n/2`, put digit `max(0,p_i-9)` at the low position and `p_i-max(0,p_i-9)` at the high position. The leading digit is 9 because `p_0=17`. This defines one canonical positive 54,078-digit seed, not a formal polynomial masquerading as a number.

For each `t=0,...,20000`, let `idx=39+20*q=6039`, `end=idx+10*k=48039`, and define the *conservative* guarded interval:

```
I_t = [idx+t+2, end-t-2)              (integer coefficient indices)
P_t[j] = V_(t mod 40)[(j-idx) mod 5]  for EVERY j in I_t.
```

The checker tests this entire interval, not a sampled coefficient, at all 20,001 time points. It independently checks the **entire actual pairword** `pairs(d_t)=P_t` for every `t`, separately advances the pairword via carry normalization, advances ordinary decimal digits via grade-school addition, and advances an arbitrary-precision integer with independent base-10^9 limb operations (including reversed-decimal conversion). At every time, the integer's canonical decimal representation must match the digit-array engine exactly; every overflow bit must match `101010...`; no digit word may be palindromic. The periodic island is therefore a *real integer* phenomenon rather than a formal-only spacetime row.

Reproduction: `sh calculation/new_structures/agent-W30/run.sh` (Python random whole-number checks, short run and 20,000-step main run). The run uses standard Python and C++17. A separately compiled `-DW30_GMP` flag additionally tests short integer traces against GMP; `W30_GMP=1 sh calculation/new_structures/agent-W30/run.sh` activates it. An earlier full-size GMP replay agreed through step 13,000 but was intentionally replaced by the faster independent limb implementation for the complete run.

Observed length increases from 54,078 to 64,078 with exactly 10,000 one-bit overflows; protected-interval length decreases from 41,996 to 1,996; the final protected odd-coefficient count is 1,596. Full-digit FNV64 checkpoints are in `checkpoints.json` and agree with the executable run (FNV hashes are identifiers, not formal proofs). The local affine equations also pass 319,820 independent eligible site checks across 20,000 seeded random canonical decimal integers; both overflow branches are covered. A modified local predicted coefficient fails the checker by construction.

## What has *not* closed

The 40-row carrier is **genuine and odd at every phase**, but its two boundary interfaces have not been shown to preserve or replenish an island indefinitely. The conservative one-cell-per-side light cone gives guard width `41996-2*t`; it becomes nonpositive at `t=20998`. This is a **loss of the certified witness interval**, not evidence of a palindrome at 20,998. An all-time certificate would require a finite boundary transducer or a renormalising duplication operation that replenishes the five-cell odd carrier at least as fast as each interface consumes it, while maintaining the exact alternating overflow schedule. That is the constructive search direction, not a no-go conclusion.

Lean roadmap: define a coefficient-window local step lemma from the existing normalized carry definitions, prove the gamma-0 and gamma-1 identities by substitution and `omega`/integer case splits, register a checked 40-row cyclic table with `decide`, then combine with a *new, separately proved* interface-replenishment invariant. No such interface theorem is asserted here.