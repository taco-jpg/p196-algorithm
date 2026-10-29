# SAT-synthesized repaired-wake moving front (agent-N05)

**COMPUTED**, scope: one SAT witness for five exact local pairword steps in base 10; 1000 independently checked whole-integer steps of a resulting realized seed. No recurring glider, no Lychrel certificate, no claim about 196.

## Exact space-time formulation
Use base-10 period-12 / spatial-period-9 bulk rows `W_t`, rooted at B-width 34, with gamma schedule 100010001000 and known lower carry `C_t`. For each time t and absolute spatial coordinate x inside a sufficiently buffered window, introduce an integer pair coefficient p[t,x] in [0,18], a lower carry l[t,x] and an upper mirrored carry h[t,x]. Force the coefficients outside the permitted defect corridor to W_t and fix the two boundary carry bits by propagation through 30 unchanged lattice cells. Assert for every source x:
```
l[t,x+1] = ite(p[t,x]+l[t,x]>=10,1,0)
h[t,x-1] = ite(p[t,x]+h[t,x]>=10,1,0)
u[t,x] = p[t,x]+l[t,x]-10*l[t,x+1]
v[t,x] = p[t,x]+h[t,x]-10*h[t,x-1]
p[t+1,x] = u[t,x]+v[t,x-gamma[t]].
```
The last equation is imposed on the interior x=2..M-3 only, not on the endpoints or centre. Source window M=48 starts at absolute x=990; phase=2. The unknown initial packet is in local cells [18,20] (absolute x=1008..1010). The time-5 packet must lie in [19,21], with a genuinely changed left endpoint both initially and at the target. Intermediate rows have six-cell margins. This is an exact QF_LIA SMT problem, not a heuristic cellular automaton.

Z3 returns SAT with initial coefficient triple [6,3,7]. The independent local transfer implementation, which never uses SMT constraints, produces the precise changed-site trajectory relative to absolute x=1008:
```
k=0: (0,6),(1,3),(2,7)
k=1: (0,13),(1,6),(2,15)
k=2: (0,6),(1,14),(2,11)
k=3: (1,11),(2,7),(3,7)
k=4: (1,2),(2,15),(3,15)
k=5: (1,6),(2,11),(3,11)
k=6: 4 changed cells in offsets [1,4] (loss of exact 3-cell form)
k=7: 3 changed cells in offsets [2,5], then spreading resumes.
```
Thus for k=3..5 the original leftmost site has returned to the unperturbed lattice and the packet has moved +1, a repaired wake on real decimal data. It is NOT a shape-periodic glider and cannot be used as an infinite certificate.

## Completely separate integer-arithmetic replay
The existing `phase_packet.py` constructs a real positive 6071-digit integer whose pairword at phase 2 has those symmetric modifications, then computes real N+reverse10(N) using Python arbitrary-precision integers. Each of the 1000 source numbers has no palindrome, every overflow bit agrees with the prescribed 12-phase schedule (250 overflows), and at every step an expanding interior interval of the FULL integer's pair coefficients agrees with the separately computed moving defect. By step 999 the defect occupies 561 sites, offsets [-188,415], so it has not returned to a finite width.

## Reproduction (from repository root)
```sh
python3 calculation/new_structures/agent-N05/sat_glider.py --H 5 --phase 2 --free --one-shot --drift 1 --wide 3 --margin 6 --M 48 --origin 990 --first 18 --timeout 4500 --output /tmp/n05-h5.smt2
python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 6,3,7 > /tmp/n05-h5-int.json
```
The first command uses libz3.so.4 via ctypes (no Python z3 package needed), or its emitted SMT-LIB assertions may be solved by an independent SMT-LIB solver. It always checks the decoded SAT model against the independent finite local carry evaluator before announcing success. The second is independent arbitrary-precision integer replay. Exact checks and data are in `sat_h5_witness.json`.

This positive finite-propagation mechanism motivates a **144-step diagonal-strip returning SAT search** as in `AgentN05BalancedGliderStrip`; no 144-step model has been obtained.
