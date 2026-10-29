# Agent Y04: all-time no-go for nested append-only p8 centre renewals

**Label: COMPUTED** for exhaustive acyclicity, with a paper-proof modular reduction. This is a restricted impossibility result, not a decimal Lychrel certificate or general no-go theorem for growing centres.

## Exact theorem

Let `a_0,a_1,...` be the phase-zero labels of an infinite walk from the canonical root `(0,85,0x1111)` in the **full reachable** eight-phase, base-10 column graph with overflows `10101010` and temporal column recurrence `x_8=x_0`. For every `k>=0`, put `h_k=h_0+2k` and let `P_k` be the full symmetric pairword obtained from the first `h_k` coefficients. Fix either even length `2h_k`, or odd length `2h_k-1`, in the latter case requiring the central coefficient `a_(h_k-1)` even. Suppose these are normalized physical positive numbers and the *pairword* of eight genuine reverse/add steps from `P_k` is exactly `P_(k+1)` with four overflow digits, for every `k`. **No such infinite sequence exists.** The condition is deliberately about pairwords: different concrete digit splittings cannot evade it because the next reverse/add number depends only on pair sums.

For even parity, the physical number's residue modulo 9 is `Q_k=sum_(j<h_k) a_j (mod 9)`. Each eight-step return multiplies this by `2^8=4 (mod 9)`. The appended block `s_k=a_(h_k)+a_(h_k+1)` therefore satisfies `s_k=3Q_k (mod 9)`. Moreover `s_(k+1)=3Q_(k+1)=12Q_k=s_k (mod 9)`. Thus **every** consecutive two-edge block on the infinite walk has the *same* sum `c` modulo 9, where necessarily `c in {0,3,6}`.

For odd parity, the central coefficient denotes twice the single central digit; therefore `Q_k=sum_(j<h_k-1) a_j + a_(h_k-1)/2 (mod 9)`. The increment is `s_k=(a_(h_k-1)+2a_(h_k)+a_(h_k+1))/2`, an integer because both successive central coefficients are even. The identical congruence argument gives `s_k=s_(k+1)=c (mod 9)` for one fixed `c in {0,3,6}`. Equivalently each two-step macro edge from a state with preceding even label `p`, through labels `u,v`, must have `v` even and `(p+2u+v) mod 18 = 2c`.

The finite graph used is **exact**, not an exterior-width cutoff. For state `(L,H,Y)` and temporal column `x_t`, choose upper incoming carry `z_t` in `{0,1}`, demand `H_t=floor((x_t+z_t)/10)`, and set `L'_t=floor((x_t+L_t)/10)`, `H'_t=z_t`, `Y'_(t/2)=(x_t+z_t) mod 10` at even `t`. At even `t`, `x_(t+1)=(x_t+L_t) mod 10+Y_(t/2)`; at odd `t` replace the second term by `(x_t+z_t) mod 10`. Enforce `x_8=x_0`, allow `x_0 in 1..18` at the root and `0..18` elsewhere, and retain *all* distinct labelled edges. The result is 244,785 reachable states and 263,584 labelled edges, matching the published N03/X03 root graph. An infinite nested bridge would give an infinite path in one of the six constrained finite macro graphs, hence a directed cycle; none has one.

## Exhaustive terminal graph checks (no state cap)

| centre | macro residue c=0 | c=3 | c=6 | verdict |
|---|---:|---:|---:|---|
| even, 244,785 states | 33,256 edges | 31,208 | 31,348 | all DAG |
| odd, 121,508 state/previous-even-label pairs | 8,018 | 8,376 | 8,404 | all DAG |

`append_growth_no_go.cpp` enumerates the eight-phase graph by recursive column DFS and proves DAG by removing every vertex in a Kahn indegree peeling. `independent_acyclicity.cpp` constructs the complete graph again by a separate iterative phase dynamic program and checks cycles by explicit iterative depth-first grey/black coloring. Both independently produce the exact same state, edge and six constrained macro-edge counts and find no cycle. A dropped label is not permitted: deduplication is by **(target,label)**, not just target. The standalone ordinary Python integer test reconstructs an actual 274-digit N03 seed and independently computes actual decimal reverse/add for 16 steps: the complete time-zero folded pairword is exact at t=8 (length 278); the attempted t=16 append has its first wrong pair at index 138 (initial halfwidth 137), agreeing with the modular obstruction. The integer test is a regression control, not the proof of all-time acyclicity.

## Scope boundary and constructive redirection

This decides the **append-only, unmodified-older-columns, single nested period-eight oracle** version of the N03/X03 centre-growth lemma for all widths and both parities. It does not constrain a genuine nonlinear repair `F` that changes previously written centre columns, switches time phase, or moves through a non-period-eight carry history. Those are now the relevant targets: **a periodic centre repair must rewrite a bounded older suffix or genuinely alter the temporal carry state, rather than appending two columns of an unchanged oracle**. No finite-horizon survival result is used as an all-time claim, and no existence claim about any decimal Lychrel number is made.

Run all checks using the three commands in `results/AgentY04AppendOnlyP8NoGo.md`; only a standard C++17 compiler and Python 3 are needed. No Lean file was modified; repository-wide `tools/verify.py --changed` was unavailable without a Git checkout in this environment.
