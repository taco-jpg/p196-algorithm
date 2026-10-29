# Exact zero-partner reset and sharp exponential no-carry barrier

**PAPER PROOF (all integer bases `b>=2`, every overflow word, any time period, and every `q>=0`).** The exact position automaton has a current cut `(L,H,Y)` and temporal coefficient `x_t ∈ {0,...,2b−2}` with guessed outgoing carry bit `c_t ∈ {0,1}`. Every transition satisfies

`floor((x_t+c_t)/b)=H_t`,
`x_(t+1)=((x_t+L_t) mod b)+(g_t ? Y_t : ((x_t+c_t) mod b))`.

Indices in this theorem are consecutive indices in the periodic temporal clock. Suppose:

1. `g_t=1`, `Y_t=0`, `L_t=0` (a zero-partner overflow time),
2. `g_(t+1)=0`, `H_(t+1)=L_(t+1)=1` (a one-carry zero-overflow time),
3. `g_(t+2),...,g_(t+q+1)=0` (q more zero-overflow times, empty for q=0).

**Forced reset.** At t the outgoing coefficient is `x_(t+1)=x_t mod b ∈ [0,b−1]`. At t+1 the imposed carry `H_(t+1)=1` requires `x_(t+1)+c_(t+1)>=b`, hence necessarily `x_(t+1)=b−1`, `c_(t+1)=1`. With `L_(t+1)=1`, the zero-overflow rule gives `x_(t+2)=0+0=0` exactly. No assumption of cyclic closure or positivity at t is used.

**Growth bound.** For a zero-overflow time, the modulo terms satisfy `(x+L) mod b <= x+1` and `(x+c) mod b <= x+1`. Therefore `x_(v+1)<=2*x_v+2`. Starting from the reset value 0, induction over the subsequent q zero-overflow times gives `x_(t+2+q)<=2^(q+1)-2`. If the required carry at that time is `H_(t+2+q)=1`, necessarily `b <= x_(t+2+q)+c_(t+2+q) <=2^(q+1)-1`. This contradicts `b>=2^(q+1)` and proves the theorem for all q. For q=0 this says the newly reset coefficient can never immediately produce required carry 1 in any valid base.

**Sharpness for every q>=1.** Set `b=2^(q+1)-1` and take `x_t=b−1`, `L_t=Y_t=0`, `c_t=0`, then `x_(t+1)=b−1`. At the next time choose `H=L=c=1`, obtaining `x_(t+2)=0`. At each of the q intervening zero-overflow times choose `L=c=1`, yielding the exact coefficients `x_(t+2+j)=2^(j+1)-2` for `j=0,...,q`. For the q steps themselves all demanded `H=0` are valid because `x+c<b`; at the final time `x_(t+2+q)=b−1` and `c=1` gives `H=1`. Thus the threshold cannot be weakened from `b>=2^(q+1)` to `b>=2^(q+1)-1`. The q=1, b=3 witness is a minimal positive example; the q=0 exclusion is universal b>=2.

**Application and precise limitation.** The case q=0 rules out any local successor cut with `Y_t=0,L_t=0,g_t=1` immediately followed by `g_(t+1)=0,H_(t+1)=L_(t+1)=1,H_(t+2)=1`. This exact 3-time pattern occurs in eight individually enumerated terminal states in the diagonal family `g=1 0^r 11 0^(r+1)`, `b=2^(r+1)`, in the finite checked range r=5..19 (time origin t=r+2). For the r=4 boundary, the same eight have H_(t+2)=0 and H_(t+3)=1; choose q=1, b=32>=4, and obtain the contradiction. This application is only to states with that explicit local signature; the theorem does not assert that the empirical templates exhaust root-reachable states at arbitrary r, nor that all 32 observed terminal states are covered. Therefore the all-r acyclicity claim remains **UNDECIDED**.

**Independent reproduction and positive controls.** From repository root run:

`bash calculation/decimal_frontier/lattice_formats/code/agent16_reset_run.sh /tmp/a16-reset`

It runs a primary explicit trajectory/carry enumerator over bases 2..200 and q=0..7 where the base-bound applies, plus sharp witnesses for q=1..12. The independent checker composes exact integer-valued transition relations instead of enumerating carry words, for bases 2..300 and q=0..7. These tests are finite controls, **not** the proof of the unbounded theorem. For positive controls, a standalone copy of the exact C++ position-automaton graph checker runs b=9, `g=1100011000` (956310 vertices, two depth-61 SCCs of size four) and b=13, `g=1010010000` (250302 vertices, depth-55 and depth-75 singleton cyclic SCCs). All source files, checker, commands, and exact expected output assertions are included in this commit. No Lean changes or decimal Lychrel number are claimed.
