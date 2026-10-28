# Triple-ones root obstruction for all zero-run lengths and repetitions

**PAPER PROOF** for canonical-root first-coordinate time recurrence of the decimal exterior position automaton; **COMPUTED** independent finite checks. No complete decimal exterior, centre, or Lychrel number is claimed.

Let `g=(111 0^r)^k`, `r>=1`, `k>=1`, and let the temporal root coefficient take values `x_t in {0,...,18}` with guessed high carries `h_t in {0,1}`. The exact position-zero equation inherited from `bauto3.cpp` is

`floor((x_t+h_t)/10)=g_t`, `x_(t+1)=(x_t mod 10)+(g_t ? 1 : (x_t+h_t) mod 10)`.

The canonical initial spatial coefficient is positive: `1<=x_0<=18`. The first three overflow bits equal one. At the second bit we need `x_1+h_1>=10`; a case check of `x_0 in {9,...,18}` and `h_0 in {0,1}` shows only `x_0=18`, `x_1=9`, `h_1=1` can reach the third one. It follows `x_2=10`, `x_3=1`, and `h_0,h_2` remain free binary values.

For every subsequent zero, the condition `x_t+h_t<10` forces `x_(t+1)=2*x_t+h_t`. From `x_3=1`, after `j` zeros, the value lies in `[2^j,2^(j+1)-1]`. The first four zero positions can be legal, with after-one-block endpoint sets: `r=1`: `{2,3}`; `r=2`: `{4,5,6,7}`; `r=3`: `{8,...,15}`; `r=4`: `{16,17,18}`. A fifth zero is impossible because the input coefficient is at least 16, contradicting a required zero high carry.

In every new `111...` block, the first triple again forces the block-start coefficient to be 18. Therefore `r=1,2,3` cannot cross two blocks and cannot close after a single block either, and `r>=5` cannot finish one block. At `r=4`, the only legal block return is `18->18`, forcing the zero-step carries `h_3=0,h_4=0,h_5=1,h_6=0`. The other carries are `h_0=a in {0,1}`, `h_1=1`, `h_2=b in {0,1}`. Thus every one-block return has the exact coefficient itinerary `(18,9,10,1,2,4,9)` and one of four independently chosen carry words `(a,1,b,0,0,1,0)`. Concatenation of `k` time blocks is possible only by choosing one of those four loops in each block, so there are precisely `4^k` temporally closed histories. This is a true statement for all integers `r,k`, not an extrapolation from finite checks.

The Python script independently enumerates all one-block choices and verifies the resulting exact root transfer matrix; the separate C++ code directly evolves original time-step coefficient distributions for every tested `r,k` without using the Python block construction. Full base9/base13 controls use the existing exact spatial column recurrence, independently compiled in the supplied program. They are controls, not new SCC results.

**Run from the repository root:**

`python3 calculation/decimal_frontier/triple_ones_root/root_theorem.py --rmax 60 --kmax 12`

`g++ -std=c++17 -O2 calculation/decimal_frontier/triple_ones_root/independent_root.cpp -o /tmp/agent12_triple_independent && /tmp/agent12_triple_independent 100 12`

`g++ -std=c++17 -O3 calculation/decimal_frontier/triple_ones_root/full_scc_controls.cpp -o /tmp/agent12_triple_controls && /tmp/agent12_triple_controls`

**Limitation:** The surviving `r=4` root loops are necessary, not sufficient, for a complete exterior B-cycle or a centre. The higher-spatial-column existence problem for `(1110000)^k` is unresolved. Nothing here establishes a decimal Lychrel number or the status of 196.
