# Exact all-width uniqueness of the period-22 neutral-band exterior repetition

**Agent:** 732. **Label:** COMPUTED (exhaustive, no state or width caps in the all-width consequence). **Scope:** base 10, neutral-band B-position automaton, exactly the period-22 overflow schedule
`g = 0000111000100001110001 = (00001110001)^2`.
No claim is made about absorbing lattices, arbitrary overflow words, a centre, 196, or a decimal Lychrel number.

## The precise question

`calculation/decimal_frontier/exterior_census/EXTERIOR.md` §3b reports a unique period-11 neutral B exterior with overflow `00001110001` and carry `00111010011`, and its period-22 repetition as ACCEPT, but leaves B-level uniqueness of the doubled schedule UNDECIDED. A prior agent-329 obtained an uncommitted independent local decision, explicitly RELEASED in issue #474 (#6483200571). This computation independently establishes a finite all-width proof of the same conclusion.

A *history of width d* chooses one coefficient word `x_t[k]` across all 22 time phases for each spatial column `k=0,...,d-1`, with all carries satisfying the exact position-transition equations. Count histories with multiplicity: distinct coefficient/carry histories that coalesce to the same boundary state are distinct histories. Accept only if the upper interface is a legal neutral band at all 22 phases. This is stronger than merely finding one accepting state.

## Exact recurrence

At each spatial cut the boundary state consists of `L_t,H_t∈{0,1}` for temporal phase `t mod 22` and a base-10 digit `Y_t∈{0,...,9}` for those times with `g_t=1`. Initially `L_t=0, H_t=g_t, Y_t=1` at overflow times. At the first column require `x_t>0` at **all** phases; at subsequent columns allow `0<=x_t<=18`. Each spatial edge chooses `c_t∈{0,1}` and a 22-periodic coefficient sequence `x_t` satisfying

```
floor((x_t+c_t)/10) = H_t,
x_(t+1) = ((x_t+L_t) mod 10) +
          (Y_t if g_t=1 else ((x_t+c_t) mod 10)),
x_22 = x_0.
```

Its successor boundary is

```
L'_t = floor((x_t+L_t)/10),
H'_t = c_t,
Y'_t = (x_t+c_t) mod 10  at g_t=1.
```

The terminal cut is accepting precisely when `L_t+H_t=1` at all phases and `Y_t=9 L_t` at overflow phases. These are the exact neutral-band requirements from `EXTERIOR.md` §1; no shortest-path approximation, guessed carry, or capped search is used.

Let `v_d(s)` count **all** histories of width d that end in boundary state s. The root step (d=0 to 1) uses `x_t>0`; every subsequent step uses the same fixed weighted, integral, linear transition operator `T`. In particular, `v_(d+1)=T(v_d)` for d>=1, with all parallel edges added by exact checked uint64 integer arithmetic. The state key is the *complete* 22-bit L word, 22-bit H word, and eight four-bit Y digits (76 bits total) packed in a pair of uint64 fields; no truncated hash values are equated.

## Exhaustive result and all-width induction

The program finds `accept(v_d)=0` for every d<29 and exactly one for every 29<=d<=88. At each accepted width the same one lower-carry schedule is `0011101001100111010011`, the period-11 carry word repeated. The maximum full weighted frontier is 651,921 distinct exact states, at d=37; no state cap is used. At d=88 exactly 257 states are nonzero, and an *exact key-to-integer-weight equality* test yields `v_88=v_89`. This is a complete finite equality, not a hash or total-count comparison.

Since the same T applies at every later width, induction gives `v_(88+k)=v_88` for all k>=0. Consequently `accept(v_d)=1` for every d>=29, with the unique accepted carry schedule. The known period-11 exterior realizes that accepted history by repetition, so the sole period-22 B history is not a new primitive period-22 exterior. No conclusion about the eventual decimal reverse-and-add orbit follows.

## Independent controls and reproduction

The second checker `Agent732P22Oracle.py` uses ordinary Python tuples `(L,H,(Y_i))`, recursively enumerates carries independently of the 128-bit packed C++ state representation, and compares the **entire** sorted (state, multiplicity) tables with the main counter. For d=0,1,2,3 the state counts are 1, 64, 4096, 29760, and the 29,760 weighted rows at d=3 agree byte-for-byte. This independently detects incorrect packing, transition, or multiplicity at the first three columns.

The main counter also reproduces p11 first ACCEPT at d=29, exactly one at each subsequent width, and a 17-state exact fixed point d59->d60. For the known p12 neutral schedule `000100010001`, it finds exactly three accepted histories first at d=53, with the three expected 12-bit carry words.

The separate `Agent732P22PositiveControls.py` uses **actual repo data** from the base-9 certificate and the base-13 Lean `B0..B9` definitions, reconstructs physical ordinary-integer base-b starting digits, then checks both digit-vector addition and independent Python big-integer `N + reverse_b(N)` at each of 200 steps. It checks all 201 complete pairwords, 200 overflows and absence of palindromes for base 9 (`|B|=61`, m=4, schedule `1100011000`) and base 13 (`|B|=75`, m=1, schedule `1010010000`). These are positive controls on already-proved nondecimal lattice paths, not a claim that the separate neutral-band p22 enumerator finds those absorbing targets.

Run from a real repository checkout:

```
bash calculation/decimal_frontier/exterior_census/Agent732P22Reproduce.sh
```

The runner compiles with `-O3 -std=c++17 -Wall -Wextra -Werror`, runs known controls, exhaustively checks the entire d=3 Python/C++ weighted state table, verifies p11, p12 and the p22 all-width fixed point and exact counts, and restricts each program to <=8 GiB virtual memory. Only final source, a reproduction script and this proof note are intended for the repository; local stdout/CSV/traces are intentionally not committed.
