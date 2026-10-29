# All-base, all-superperiod root-column theorem for 101100

## Precise statement

**PAPER PROOF.** Let `b>=2` and `k>=1` be integers, and let `g` be any
cyclic rotation of `(101100)^k`. For the exact `bauto3.cpp` canonical
root `L_t=0`, `H_t=g_t`, `Y_t=1` at overflow times, with first pair
coefficient `x_0>=1`, the number of distinct time-closed first-spatial-
column histories `(x_t,c_t)` of length `6k` is **4^k if b=4,5,6 and
zero otherwise**. For each admissible history, the pair-coefficient word
`x` is six-periodic; no genuinely new temporal coefficient orbit appears
at a higher multiplier. This concerns ONLY the first spatial transition,
not an exterior SCC, centre, or nonpalindromic integer orbit.

## Proof

Take the time-rooted six-letter block `g6=(1,0,1,1,0,0)` with input
coefficient `u=x_0`. In the canonical-root cut, the exact carry conditions
and transition are

`floor((x_t+c_t)/b)=g_t`, `c_t∈{0,1}`,

`x_(t+1)=(x_t mod b)+(g_t ? 1 : (x_t+c_t) mod b)`.

All pair coefficients are in `[0,2b-2]` and the initial one is positive.
The two consecutive overflows at t=2,3 followed by zero overflow at t=4
force `x_2=b-1`, `x_3=b`, `c_2=1`, `x_4=1`: since `x_3=(x_2 mod b)+1<=b`
with an overflow at t=3, `x_3` is b or b-1. In the latter case
`c_3=1` would yield `x_4=b`, which violates `g_4=0`; hence `x_3=b`.
The first overflow at t=0 followed by zero at t=1 similarly gives
`x_0>=b` and `x_1=x_0-b+1` (otherwise `x_1=b` violates `g_1=0`).
At t=1, `x_2=2*x_1+c_1=b-1`. Its parity forces
`c_1=1` for even b and `c_1=0` for odd b. Therefore **every** legal
six-step block, whether or not it closes on its own, must start at

`A(b) = b-1+floor((b-1)/2)`.

The last two zero-overflow steps give `x_5=2+c_4` and
`x_6=4+2*c_4+c_5∈{4,5,6,7}`. In a **closed 6k-step history**, the
input of each of its k six-blocks must again be `A(b)` (the root
conditions repeat). Hence `A(b)∈{4,5,6,7}`. Directly:
`A(2)=1` is impossible since the first overflow followed by zero
requires `x_0>=b`, `A(3)=3` is too small, and `A(b)>=9` for b>=7.
The only possibilities are b=4,5,6, with `A=(4,6,7)` respectively.
For these bases, `x_6=A(b)` forces **unique** `(c_4,c_5)`:
`(0,0)`, `(1,0)`, `(1,1)`, respectively. The complete coefficient
six-blocks and the other forced carries are:

| b | six coefficients x | `(c1,c2,c4,c5)` | free bits |
|---|---|---|---|
| 4 | `(4,1,3,4,1,2)` | `(1,1,0,0)` | c0,c3 |
| 5 | `(6,2,4,5,1,3)` | `(0,1,1,0)` | c0,c3 |
| 6 | `(7,2,5,6,1,3)` | `(1,1,1,1)` | c0,c3 |

Substitution verifies all six equations. The two free carry bits at
t=0 and t=3 do not affect the coefficient recurrence because those
steps are overflows; both values satisfy the carry inequality at the
coefficient of those times. Choices in different six-blocks are
independent, giving exactly `(2*2)^k = 4^k` histories. All six
coefficients are strictly positive, so cyclic rotation of time is a
bijection of admissible histories, preserving the initial positivity
condition. This proves all bases, all k and all six phases, with no
search cap and without assuming the coefficient period equals six.

## Reproduction and controls

The same commit includes:

- `calculation/decimal_frontier/lattice_formats/code/repeat101100.py`:
  independent exhaustive six-step transfer digraph with weighted edges
  and exact trace counts of its kth adjacency power, for all rotations.
- `calculation/decimal_frontier/lattice_formats/code/repeat101100_construct.py`:
  separate explicit coefficient/carry construction and digit-level
  recurrence checks, all six phase rotations.
- `calculation/decimal_frontier/lattice_formats/code/agent16_repeat_run.sh`:
  executes both algorithms and the mandatory complete SCC controls.

From repository root:

```bash
bash calculation/decimal_frontier/lattice_formats/code/agent16_repeat_run.sh /tmp/agent16-repeat
```

The transfer engine exhaustively checked every b=2..100, every six-phase
rotation and every k=1..8, obtaining exactly `4^k` or 0. The separate
explicit construction replayed all three bases for k up to 1000 with
16 independent carry-bit sequences and every phase. The runner also
uses the existing exact `agent16_root_graph.cpp` (already on `main`, not
duplicated here) for full graph control runs: b9 g=1100011000 gives
956310 states and two depth-61 size-4 SCCs; b13 g=1010010000 gives
250302 states and self-loops at depths 55 and 75. Tests complete within
8 GB/process; the larger controls use `nice -n 15`.

No statement about other overflow words, other formats, true base-10
infinite orbits, or the specific integer 196 is implied.
