# Agent N16: measured 22-step inward defect-front clock
**COMPUTED** for the explicitly replayed times and q values, not a decimal Lychrel proof.

Let the initial symmetric pair-coefficient word be `B0 ++ W0^q ++ reverse(W0)^q ++ reverse(B0)`, with the canonical decimal seed decomposition and eight phase rows in `rows.txt`. The data are copied independently from the first rooted rec0 p8/m20 lattice in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`. For actual integer N_t define the folded pairword `P_t[i]=digit_i(N_t)+digit_(L-1-i)(N_t)`. Let M_q(t) be its longest prefix matching `B_(t mod8) W_(t mod8)^infinity`, and set `D_q(t)=39+20q-M_q(t)`.

**Exact empirical formula:** for all t=22..20,000 at both q=300 and q=301, `D_q(t)=5*(t//22)+F[t%22]`, where F is the 22-entry table `[0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3,3,5,5,5,5]`. The 19,979 cases per q all pass. Separate q=100 through t=2,000 and q=5 through t=300 also pass all t>=22. The q=300 minimum matched prefix is 1,494 and the q=301 minimum is 1,514. At each step, a GMP integer evolves via true N+decimal_reverse(N), while an independent LSB-first schoolbook digit-vector engine evolves via its own carry loop; the program compares the **entire integers** before checking the front law. All initial and updated numbers are genuine base-10 integers, not only abstract pair words.

**Exact finite bulk identity:** with phase t in Z/8 and spatial index j in Z/20,
`W_(t+22)[j-5]=18-W_t[j]`. Verify 160 identities with `check_twist.py`; the equivalent +2/+5 symmetry gives 160 more. This complement-twisted spatial symmetry is compatible with the observed glider displacement, but it does NOT say the entire growing centre has a 22-step repeating or complemented profile.

**CRT-compatible macroclock:** lcm(22,8,12)=264. The measured front moves 12*5=60 lattice positions in 264 steps; 60 is divisible by spatial period 20 and the CRT position-lane period 12 (mod99 order2, mod101 order4, mod1001 order6). So a *future* 264-step interface certificate could simultaneously restore spatial, temporal and modular positions. It must **produce** 60 cells of fresh exterior per macrocycle to offset this inward motion. This experiment does not produce them.

**Reproduce:** `sh calculation/new_structures/agent-N16/front_clock/run.sh`; requires C++17, GMP headers/library, Python3. Data, generator, full-integer independent replay and table checker are all committed under `calculation/new_structures/agent-N16/front_clock/`. q controls: 5/300,100/2000,300/20000,301/20000. The shorter q=5 case shows the law before the exterior vanishes, not indefinite survival.

**UNDECIDED:** the front law for all q or unlimited time; existence of a self-renewing interface, an actual decimal Lychrel number, or any 264-step centre cycle.
