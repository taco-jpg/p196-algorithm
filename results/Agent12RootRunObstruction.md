# Canonical-root obstruction for fixed overflow schedules
**PAPER PROOF.** In the `bauto3`/`bauto5` position automaton, a time-rooted overflow word beginning `11 0^r 1` with `r >= 1` has no outgoing edge from the canonical initial state for any base `b > 2^(r+1)`.
At the canonical root `L=0`, `H=g`, `Y=1` on overflow positions; its first-column sequence satisfies `floor((x_t+h_t)/b)=g_t`, `h_t in {0,1}`, `x_(t+1)=x_t%b+(1 if g_t else (x_t+h_t)%b)`, `1<=x_0<=2b-2`.
The first two ones allow only `(x_0,x_1,x_2)=(b-1,b,1)` or `(2b-2,b-1,b)`; the next zero forbids `x_2=b`. Starting at `x_2=1`, each of the `r` zeros gives `x_(t+1)=2x_t+h_t` and therefore `x_(r+2)<=2^(r+1)-1`. The following one would require `b<=x_(r+2)+h_(r+2)<=2^(r+1)`, a contradiction.
**Corollary:** for fixed, unrotated `g=1100011000` (`r=3`), no reachable exterior SCC exists for any base `b>=17`, without a state cap.
**Sharpness of root condition:** base 16 admits the closed first-column trajectory `(15,16,1,3,7,15,16,1,3,7)` (not necessarily a full lattice certificate).
**Reproduce:** `python3 calculation/decimal_frontier/lattice_formats/code/agent12_root_obstruction.py --max-base 100`; exhaustive time-closed root trajectories at `b=9`: 4, `b=16`: 4, `b>=17` through 100: 0; distinct base-13 `1010010000` control: 8.
**Separate full-SCC controls:** locally reconstructed exact `bauto3` yielded base 9: 956,310 states, 7 nontrivial SCCs, period-4 depth-61; base 13: 250,302 states, 5 SCCs, fixed-point depths 55 and 75. These reproduce existing controls, not a new census.
**Not claimed:** arbitrary phases or other schedules, existence of a new Lychrel certificate, a decimal result, or a Lean-verified theorem.
