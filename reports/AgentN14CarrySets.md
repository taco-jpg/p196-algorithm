# Agent N14: Set-valued decimal carry contracts and period-39 width-12 local strip

## New format: a temporal strip with a carry-set interface (PAPER PROOF)

For base ten let `x[t,j]` be the palindromic pair coefficient at spatial position `j` (least significant first), clock `t mod p`, `j=0..K-1`. Let `g[t]∈{0,1}` be the overflow of its normalized coefficient value. For a chosen entering high carry `u∈{0,1}` into the highest observed column, compute the descending high carries `h[K-1]=u`, `h[j-1]=floor((x[j]+h[j])/10)`. Compute ascending low carries `l[0]=0`, `l[j+1]=floor((x[j]+l[j])/10)`. Then the normalized digit pair at spatial column `j` has coefficient

```
xnext[j] = (x[j]+l[j]) % 10 + (g[t] ?
            (j==0 ? 1 : (x[j-1]+h[j-1])%10)
            : (x[j]+h[j])%10).
```

The overflow condition is `g[t]=floor((x[0]+h[0])/10)`. Thus define `A[t]` as *the set* of carry inputs `u` satisfying every equation and the specified `x[t+1,j]`. Crucially `A[t]` may be `{0,1}` even for one fixed visible strip.

## Extending spatially by one column (PAPER PROOF)

Let `L[t]=floor((x[t,K-1]+l[t,K-1])/10)`. A new column coefficient `z[t]∈{0,...,18}` and entering upper carry `v[t]∈{0,1}` must satisfy

```
u[t] = floor((z[t]+v[t])/10) ∈ A[t]
z[t+1] = (z[t]+L[t])%10 + (g[t] ?
              (x[t,K-1]+u[t])%10 : (z[t]+v[t])%10).
```

These equations are *necessary and sufficient* to extend a specified legitimate open-boundary K-column temporal strip to K+1 columns. Necessity follows digit-by-digit carry arithmetic. For sufficiency, the chosen `u[t]` matches the high carry required below, and the only newly exposed low/high digits give exactly the displayed `z[t+1]`. Nothing here supplies a coherent centre, so it is not a global orbit/certificate.

This is a finite nondeterministic automaton with `19p` phase/state pairs. Any infinite continuation has a repeated phase/state, and therefore a temporally periodic continuation (possibly requiring a multiple of the original clock); conversely any directed cycle gives one. Thus an all-boundary carry-set closure is a **sound finite test for open-boundary temporal extension** and a necessary ingredient of any finite-band decimal certificate. A graph cycle by itself says nothing about existence of a mirror seam.

## Explicit base-ten 39-clock width-12 positive structure (COMPUTED)

`calculation/new_structures/agent-N14/p39_k12.txt` is a 39x12 coefficient table with primitive clock `g=010100100101010101010101001010101010101`. The arithmetic checker chooses, *separately at each time*, a one-column palindromic cap 0 or 18; it converts the complete symmetric coefficient vector to an ordinary Python integer, normalizes by division, recomputes all pair coefficients, and confirms the *entire observed 12-column prefix* at the next phase, including the overflow and wrap t=38→0. All **39/39** phases have at least one legal cap. **14/39** phases have both options. Corrupting the first coefficient fails the check.

Exact set-valued 19-state propagation beyond this table has its first empty reachable set after **13 transitions** for any 13th-column start coefficient and arbitrary legal carry inputs. This is an obstruction ONLY to extending this one fixed width-12 table; it is not evidence against base-ten Lychrel existence. The 39-time table itself is not a single evolving integer, since caps are independently reselected, and no 20,000-step pairword-shape replay is asserted.

## Search method, replays and redirection

The companion deterministic C++ temporal beam generator with `mt19937_64(14)`, K=7, 7000 trials detects this primitive 39-clock rooted strip after 6309 attempts; it does **not** enumerate SCCs. From K=7, branch on every permitted hidden carry and use the 19-state time-cycle transfer, then perform two-column lookahead in a 361-state product when a one-column branch stalls. The archived K12 table is an explicit reproducible witness of one successful branching choice; its validity is independent of the randomness used to find it.

From the repository root:

```
python3 calculation/new_structures/agent-N14/carryset_verify.py
python3 calculation/new_structures/agent-N14/carryset_transfer.py
python3 calculation/new_structures/agent-N14/carryset_two.py
g++ -O3 -std=c++17 calculation/new_structures/agent-N14/carryset_discover.cpp -o /tmp/n14discover
(cd calculation/new_structures/agent-N14 && /tmp/n14discover 7 7000 300)
```

The first script checks all 39 arithmetic transitions independently; the second reports flexible thirteenth-column failure at transition 13; the third searches two columns from the K10 prefix. The generator reproduces the K7 overflow word. Compared with a *fixed sampled carry stream* used in the earlier N14 result, using the exact allowed carry sets avoids spurious negative extension conclusions. **Redirect:** combine multiple spatial columns under joint carry constraints, search period multiplication, and enforce one coherent central seam. No Lean result, no decimal Lychrel proof, no global 20,000-step template replay is claimed.
