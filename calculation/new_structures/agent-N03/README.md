# Agent N03: uniform-substitution decimal carry bands

Status: **PAPER PROOF (conditional infinite-band compositionality)** plus **COMPUTED (two finite, ordinary digit-list 20,000-step replays)**. This is **not** a base-10 Lychrel certificate: a finite centre closure is missing.

The `bauto3` spatial-cut automaton for decimal overflow schedule `g=10101010` has an exactly reachable 1,104-state strongly connected component with 1,168 internal edges (64 branching vertices). Our independent `automaton.cpp` enumerates 244,785 reachable states and 263,584 deduplicated edges with no cap and writes a 27-column root path to a recurrent state `q=(L=242,H=226,Y=22595)` and two distinct closed loops `A` (119 columns) and `B` (48 columns), encoded as temporal 8-digit coefficient columns (`A..I` encode 10..18). These data appear in `witness.txt`.

Form equal-size macrotiles `U=A||B` and `V=B||A`, each exactly 167 columns. The two macros are distinct: at the second column `U` begins `5B448GEC` but `V` begins `6C66DC5C`. Let `s` be an infinite Fibonacci word (`A->AB,B->A`) or Thue–Morse word (bit parity), and define a **spatially aperiodic eight-phase bulk** from the 27-column root path followed by `U` for `s_i=A` and `V` for `s_i=B`. Any concatenation remains a legal walk because both macrotile paths return to the exact same state `q`. The infinite row at each of eight temporal phases is **not ultimately periodic**: if it were periodic, sampling positions `27+167i+1` would yield an ultimately periodic Fibonacci/Thue–Morse symbol sequence, contradiction.

## Explicit spatial cut-state semantics and exact local rule

At position `k` and time phase `t`, `x[t,k]` denotes the palindrome-symmetric pair coefficient (0..18); `L[t,k]` is the incoming carry from the low side, and `H[t,k]` is the carry transmitted toward the low side from the high half. For the 4 times with `g[t]=1`, `Y[t,k]` stores the high-side output digit of the preceding spatial column. A labelled edge `q_k -> q_{k+1}` is admissible exactly when there exists `h[t,k]` (incoming carry from the high side) with

```
H[t,k] = floor((x[t,k]+h[t,k])/10)
L[t,k+1] = floor((x[t,k]+L[t,k])/10)
H[t,k+1] = h[t,k]
Y[t,k+1] = (x[t,k]+h[t,k]) mod 10    (for g[t]=1)
x[t+1,k] = ((x[t,k]+L[t,k]) mod 10)
             + (g[t] ? Y[t,k] : ((x[t,k]+h[t,k]) mod 10))
```

with time indices modulo 8; the outer root state is `L=0,H=bits(g),Y=1` (the digit created by top overflow). These are directly the schoolbook base-10 addition equations; concatenation of closed state paths preserves every interior equation. The correct high-end carry and reflection at the *centre* is a separate boundary condition. A finite cap/transducer closing this state would turn the combinatorial bulk into a genuine universal decimal certificate; it is currently **UNDECIDED**. Arbitrary full-integer seeds are not claimed to preserve the complete bulk indefinitely.

## Reproduce

From this directory:

```
g++ -O3 -std=c++17 -o automaton automaton.cpp
./automaton 3000000 > /tmp/n03_graph.txt
cmp <(grep -E '^(ROOTPATH|LOOPA|LOOPB) ' /tmp/n03_graph.txt) <(grep -E '^(ROOTPATH|LOOPA|LOOPB) ' witness.txt)
python3 check.py witness.txt
g++ -O3 -std=c++17 -o replay replay.cpp
./replay witness.txt 20000 200 2048 fibmacro
./replay witness.txt 20000 200 2048 thuemacro
```

The entirely separate `check.py` recomputes all eight carry-normalized pair-word rows for Fibonacci and Thue-Morse concatenations, checks the closed eight-phase bulk equations with a 64-column high-side guard, and runs genuine decimal integer replays (32 steps) with full pair-word checking on all interior columns. `replay.cpp` does **not** read the automaton state or upper/lower carry equations; it directly adds ordinary reversed decimal digits, checks palindromes every step, computes all matching outer pair columns every step, and rejects an unexpected overflow schedule. Neither program can claim an infinite certificate.

For both 200-macrotile seeds, the starting integer has 66,854 decimal digits and 33,427 lower-half pair columns; the 20,000th integer has 76,854 digits, and at every intermediate step at least 2,048 outer pair coefficients match the exactly predicted eight-phase morphic word. Actual matched prefixes at step 20,000 are **30,743** (Fibonacci) and **30,749** (Thue–Morse). The discrepancy *first* appears in the centre-near suffix and moves outward by about 0.134 pair columns/step over this run. It has therefore **not** closed into an indefinite invariant; a bounded-width centre absorber or counter-propagating growth must be found.

## Next construction

Search an absorbing, possibly morphic, centre **acceptance language** attached to the specific branching boundary state `q`, rather than to one fixed m20/m48 periodic lattice. The return-block lengths are incommensurate but the two equal-length `U,V` macrocells restore constant spatial phase. A candidate cap should accept both macro paths with the exact same carry state and the eight-phase parity/overflow centre conditions. This is a constructive new format, not another census of excluded centres.