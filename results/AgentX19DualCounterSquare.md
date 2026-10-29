# AgentX19DualCounterSquare

- **COMPUTED**: a new two-parameter decimal four-orbit 99-insertion square persists through 20,000 genuine reverse-and-add steps, without a palindrome in any corner.
- Seeds: `N(Q,R) = 12(99)^Q34(99)^R56(99)^Q78`; four corners `(Q,R)`, `(Q+1,R)`, `(Q,R+1)`, `(Q+1,R+1)` with `Q=5500`, `R=6300`.
- At each `t=0..20000`, both outer-Q edges have exactly two removable `99` base-100 cells (LSD-first), both central-R edges exactly one; independently, the symmetric coefficient pairwords have exactly four and two removable `18` cells, respectively.
- Every corner's pairword contains at least 2 odd coefficients at every step, so none is palindromic; source digits checked directly as well.
- Independent MSB-first decimal-string arithmetic agrees with the LSD-first digit-vector implementation on the full base corner at **every** step; independent Python big integers check all four corners through 300 steps for `(100,100)` and additional small controls.
- Base corner grows from 34,608 to 42,903 decimal digits; 20,001-state FNV64 digest `3b6facc7d66a409d` (defined by `dual_replay.cpp`).
- First pairword insertion failures for `(Q,R)=(100,100)` occur at step 393 (outer Q) and 337 (central R), not at a palindrome; the two finite renewal clocks remain distinct.
- Data: `calculation/new_structures/agent-X19/first_break.csv` (36 independent Q,R choices), full runnable sources in the same directory.
- Reproduce: `bash calculation/new_structures/agent-X19/reproduce.sh` (C++17, Python 3); report `reports/AgentX19DualCounterSquare.md`.
- **Not claimed**: insertion-square closure at all Q,R or unlimited time, any finite infinite-time certificate, Lean verification, or anything about the orbit of 196.
