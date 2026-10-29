# Decimal 88/20 travelling interface: explicit positive spatiotemporal mechanism

**Label: COMPUTED**, exact stated finite trajectories only. Existing phase exterior `B_t,W_t` comes from `calculation/decimal_frontier/lattice_formats/p8_scc.txt`; its discovery is not new. The new observation is a coherent moving defect profile, with a strict 88-step time/20-column spatial return for the **entire 120-column local window**, rather than merely the periodic bulk or a matching-prefix count.

## Measurement
For an actual decimal integer N_t, define its palindromic pair-coefficient word P_t by `P_t[i] = digit_i(N_t)+digit_(n_t-1-i)(N_t)`. The coefficient word is always palindromic even when N_t itself is not. Let `h_t` be the first coefficient position where P_t disagrees with `B_(t mod 8) ++ W_(t mod 8)^infinity` (take h_t=n_t/2 if there is no mismatch in the lower half). Define the 120-cell moving window `K_t = P_t[h_t-40:h_t+80]`, whose first mismatching position is at index40.

Construct four real decimal seeds from
`P_0=B_0 ++ W_0^300 ++ C ++ reverse(W_0^300) ++ reverse(B_0)`,
where `C=[]`, `[0,18,18,0]`, `[2,4,4,2]`, or `[9,6,6,9]`. The digit-pair realization uses `floor(p/2)` and `p-floor(p/2)`. Independently evolve all four by ordinary decimal digit-list reverse-and-add through 20,000 steps. For each core the following **exact finite property** holds:
```text
for every 1082 <= t <= 19912:
    h[t+88] == h[t]-20
    K[t+88] == K[t]     # literal equality of all 120 pair coefficients
```
This gives **18,831 window checks per core**, i.e. 2,259,720 directly compared pair coefficients each. A fifth run k=400,C=[] agrees with the k=300,C=[] moving window, but with h exactly 2000 greater.

The faster scalar metric `d_t=h_t-h_(t+1)` becomes strictly periodic with period22 after a small centre-dependent transient: `d_(t+22)=d_t` for t>=62 (19938 loss-period checks per run), with total loss **5 coefficients/22 steps**. It follows over the tested interval that `h_(t+88)=h_t-20`. Because 88 is divisible by the exterior's temporal period8 and 20 equals one complete spatial band, this is a true spatiotemporal return of the outward lattice phase, not just a coincidence of scalar speeds. The 120-cell windows add independent local shape information.

## Species and controls
At epoch t=1100 and t=1188, all four cores have identical per-core window FNV64 hashes, but not all cores have the same hash:
```text
core C=[]             h1100=5789 h1188=5769 hash=384f7ce9e19f7994
core C=[0,18,18,0]    h1100=5791 h1188=5771 hash=7942910fcc9b2eb6
core C=[2,4,4,2]      h1100=5791 h1188=5771 hash=7942910fcc9b2eb6
core C=[9,6,6,9]      h1100=5789 h1188=5769 hash=5dbafc1ca90c8790
```
The time-local loss words over t=1100..1121 are `0001000001000100020000` (cores 0,3) and `0002000000010000010001` (cores 1,2), each with sum5. Complete compact facts are in `glider_observations.json`, generated from full actual-integer replay. Some central cores ultimately enter the same measured local wave species, others remain different.

An entirely separate `glider_bigint.py` reconstructs the integers via Python `int`, reverses their decimal text `str(n)[::-1]`, computes `n+reverse(n)` with arbitrary-precision arithmetic, and checks the *literal full 120-cell moving window* for 231 distinct pairs t=1082..1312 (t+88<=1400) in cores 0 and 2. Both pass, and all integer iterates are checked for palindromicity. The C++ implementation checks 20,000 arithmetic steps and the exact window at every applicable step; neither derives the next number by a pairword shortcut.

## How it redirects construction
The existing bounded-centre/kink search looked for a stationary or temporally closing central defect. These positive orbits have a dynamically **advancing**, 88-periodic local interface while their unrestricted central region grows. The interface is a plausible elementary finite-state object: a 120-cell tape window, temporal phase8, integer digit-carry boundary states (0/1), and an 88-step/20-column translation contract. One can now search for a second, **replenishing** interface whose emitted 20-column band cancels this inward loss over 88 steps, or for a finite-state boundary class whose glider can be glued to a compatible new domain. No such self-replenishing domain is proven in this result.

This is not a certificate of a fixed decimal Lychrel number: the finite initial reservoir of W blocks continues to be consumed at speed5/22; a 120-cell window repeating for 18,831 compared times does not prove indefinite persistence after the shell is exhausted. Nor is the 88-step locality statement proven for arbitrary central words.

## Exact reproduction
```sh
sh calculation/new_structures/agent-N10/run_glider.sh
```
Uses C++17 compiler and Python standard library, no third-party dependencies. Replays five 20,000-step actual decimal orbits and two independent Python 1,400-step actual-bigint controls, verifying the 22-step scalar loss and 88-step full-window recurrence. Source `glider.cpp`, `glider_bigint.py`, `run_glider.sh`; compact observed wave metadata `glider_observations.json`. Repository-wide `tools/verify.py --changed` could not be run in the container without an accessible GitHub checkout; no Lean files are changed.
