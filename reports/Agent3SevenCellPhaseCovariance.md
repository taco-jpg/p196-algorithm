# Complete seven-cell physical-carry covariance for decimal rec2

**PAPER PROOF.** Base 10, cyclic spatial period 48, temporal overflow 10101010, seven adjacent coefficient parities and two physical carry bits per cell. The universal eight-phase GF(2) covariance has exact rank **777728/16777216** and kernel **15999488**. This is an all-time classification of the stated local ansatz, not a centre no-go or decimal Lychrel certificate.

For physical pairword coefficients P_j in 0..18, ascending and descending carries obey a_(j+1)=floor((P_j+a_j)/10), d_(j-1)=floor((P_j+d_j)/10). The actual bulk images are
```
g0: Y_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1))
g1: Y_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)).
```
A 76-state physical carry automaton with 1444 edges induces exactly 124512 admissible 21-bit seven-cell masks. Their de Bruijn graph has 27296 six-cell vertices, one connected component and six self-loops. Over GF(2), 48-cycle histograms are circulations with even total edge count. The incidence gradients have rank 27295; the constant-one edge function is independent because a self-loop exists. Therefore the cyclic histogram rank is at most 124512-27295-1=**97216**. The per-phase 2^21-function kernel is at least 1972640 pointwise-inadmissible functions +27295 endpoint gradients +1 length parity = **1999936**.

The committed primary constructs three independent full-rank physical 48-cycle witness streams. Source mode embeds every admissible seven-state path using exact 0/18 boundary guards. For each image mode it constructs a 5776-state/109744-edge product transducer: one input carry edge plus both output carry bits, with exact input/output physical carry transition guards. The selected recurrent SCC has 3116 states for g0 (hub1563) and 5626 for g1 (hub0). For every one of the 124512 target output masks, a seven-node constrained path exists in that SCC. Its endpoints connect through the hub and its self-loop to form an exact 48-cycle. Every output is independently asserted to have the requested target mask. In each of source, g0 and g1, 97216 independent 48-cycle histogram rows saturate the upper bound in 97217 non-tree chord coordinates.

The three deterministic generated 4666368-byte witness streams have SHA256:
```
source a2d878e8247679cb7e0b70bb2cdd2171678e17c3b193f09fc35a31de1c32d143
g0     49e548146c864a8e9788cfdf988a8c28ed466a843c4cf804ce617ecc120432dd
g1     785922edd7c7d0fb54f42e6461d95cab51d8ce1a800e191358a0d443dbd7a9bd
```
The independent checker instead enumerates all physical masks via forward 76-state-set DP, chooses a different BFS spanning tree, uses opposite-pivot GF(2) elimination, and validates every witness through genuine 386-digit schoolbook reverse-and-add normalization (g1 yields a 387-digit result). Eight published 406-digit rec2 phase controls and wrong-overflow-shift negatives pass. The Boolean zeta transform between mask indicators and square-free monomials is invertible, so the ranks transfer to all 2^21 monomial features.

For phase coefficients c_t, universal covariance requires c_(t+1)·F(Y_g(P))=(2 if g0 else 11)c_t·F(P) modulo2 for every physical cyclic word P. At g0 phases, multiplier 2 vanishes, and the full g0-image rank forces the next coefficient into the 1999936-dimensional local cyclic-zero kernel. At the next g1 phase, the source coefficient is already local-zero, and the full g1-image rank forces the following coefficient into that same kernel. Conversely any independent choice of eight local-zero coefficients satisfies covariance. Thus rank=8×97216=**777728**, kernel=8×1999936=**15999488**. No phase-coupled universal seven-cell invariant exists beyond endpoint gradients, pointwise zeros and length parity.

**Exact scope:** cyclic 48-cell physical carry parity/carry ansatz, any temporal repetitions. Spatially varying, longer-window, boundary-sensitive, non-Boolean or nonlinear centre mechanisms remain UNDECIDED. No finite-centre exclusion, base-10 Lychrel number or 196 claim. Reproduce with `sh calculation/decimal_frontier/lattice_kinks/agent3_sevencell_covariance/run_checks.sh`; all standalone source, independent checker, small rec2 data and exact commands are in the same commit. Local controls passed (<600 MB per process). GitHub shell DNS prevented repository checkout and `python3 tools/verify.py --changed`; no Lean or global check is claimed.
