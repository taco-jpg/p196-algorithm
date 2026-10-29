# Agent N02: a decimal travelling-defect growing centre, 20,000 actual reverse-and-add steps

**Label: COMPUTED.** The reported finite computations are exact; this is **not** a base-10 Lychrel certificate and does not prove any seed avoids palindromes forever. It is a positive constructive, length-growing *centre mechanism*, not another exclusion search. Previous foundational formats: `reports/AgentN02RegularCentreFormat.md` and `reports/AgentN02RegularPreimageRefinement.md`.

## Explicit family (base 10, arbitrary q >= 1)

All pair coefficients are **least significant first**. From the tracked first `SCC p=8 g=10101010` in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`, let `B_t` be its 39-row `path` at temporal phase t, and let `W_t` be its first 20-row `cyc`. In particular `|B_0|=39`, `|W_0|=20`, and all coefficients lie in `[0,18]`. Define the halfword `A_q = B_0 ++ W_0^q` and symmetric **even-length** pairword `P_q = A_q ++ reverse(A_q)`. Construct a canonical positive integer `N_q` with `2|A_q|=78+40q` decimal digits by setting, for each `0 <= i < |A_q|`, `d_i=min(A_q[i],9)`, `d_{n-1-i}=A_q[i]-d_i`. Here `d_i` are the actual decimal digits of the starting integer (least significant first), not pairword coefficients. This construction has `d_{n-1}=8`, so it is positive. It realizes `P_q[i]=d_i+d_{n-1-i}` exactly.

The evolving pairword at time t is checked against `B_(t mod 8) ++ (W_(t mod 8))^* ++ C_t ++ mirror(...)`, where `C_t` is the arbitrary growing defect tail. Formally the *front* `J_q(t)` is the first lower-half coefficient whose value differs from the phase-t infinite reference `B_t ++ W_t W_t ...`; if every lower-half coefficient agrees, `J_q(t)` equals the halfword length. The exterior stays valid as long as `J_q(t) >= 39`; this is a strictly stronger test than checking 39 prefix positions alone. All digits in the actual number are checked for palindrome equality at every step independently of this shape check.

## Measured moving-centre mechanism

For each `q=1..19` a separate Python arbitrary-precision decimal-integer reverse-and-add orbit was replayed until it first left the 39-column exterior. Every seed failed **exactly at time `88q+4`, at coefficient index 38**. The additional independent seed `q=30` retained the exterior and avoided palindromes for 1,500 steps. All these checks use Python integers, convert their values to decimal each step, reverse the decimal representation, add, and recompute pairs from the resulting actual digits. They read the external source lattice from the repository, not the embedded C++ copy.

For `q=228`, after a short initial transient, the **computed first-mismatch front** satisfies `J_228(t+88)=J_228(t)-20` for every tested `10 <= t <= 19979` where both times are within the checked run and the exterior has not failed. The same relation was checked on all admissible 88-apart pairs in the `q=1..19` and `q=30` independent Python runs. The overflow schedule is exactly `10101010`, so over each 88-step temporal block the integer length grows by 44 and its halfword length grows by 22. Consequently the centre-side defect length `h_t-J(t)` increases by `22+20=42` pairword coefficients per 88-step block. This is the new ***growing centre*** mechanism: its tip moves at rational velocity 20/88 in lower-half coordinates, while its tail expands. These equalities are **computed on the finite test sets**, not claimed for all q or all t.

The bulk is therefore a finite-time reservoir for a travelling centre defect, not an eternal neutral/absorbing band and not a periodic short kink. The front eventually reaches the rooted exterior, which explains why growing the initial reservoir can delay a failure without proving an infinite orbit.

## Independent 20,000-step ordinary integer replay

`glider_replay.cpp` contains a separate exact schoolbook digit-list engine **and** an independently updated GNU GMP (`mpz_class`) arbitrary-precision integer. Every step starts with equal decimal values; the full successor from GMP `N+reverse_decimal(N)` must equal the schoolbook decimal digit-list sum. It rejects every palindrome; it checks each first-mismatch front against the phase-specific 39+20 lattice, checks every overflow, and checks the 88-step front translation. No pairword/template recurrence is used to *compute* either successor. The starting seed `N_228` has **9,198 decimal digits**. The checks at steps 5,000 / 10,000 / 15,000 / 20,000 give integer lengths 11,698 / 14,198 / 16,698 / **19,198**, and front positions from the last pre-step respectively **3,463 / 2,327 / 1,191 / 54**. All 20,000 additions matched between the two arithmetic engines, every prior integer was nonpalindromic, and every checked phase had the prescribed exterior. The 64-bit FNV trace checksum through step 20,000 is `6266191277757808867` (this is a compact regression marker, not a cryptographic proof).

Continuing the **same** seed beyond 20,000 steps, the **first exterior failure occurs at step 20,068, position 38**. This does **not** mean the integer becomes a palindrome at 20,068; only the claimed exterior structure stops applying there. There is no claim about the subsequent fate of `N_228`, about 196, or about an infinite decimal orbit.

## Reproduce using tracked repository data

```sh
sh calculation/new_structures/agent-N02/glider_run.sh
```

This compiles `glider_replay.cpp` with `g++ -O3 -std=c++17 -lgmpxx -lgmp` (GNU GMP development libraries required), runs the independently coded pure-Python integer tests for all `q=1..19` plus `q=30`, and runs the full GMP + schoolbook digit check through the 20,068th exterior failure for `q=228`, verifying the 20,000-step checkpoints. The script ends `N02_GMP_20000_STEPS_AND_20068_FRONT_BREAK_PASS`. Compact regression expectations are in `glider_data.json`. The C++ code is fully self-contained; the independent Python script reads the original tracked `p8_scc.txt` at runtime. The long run was executed locally in both 20,000-step and 20,090-step modes, and the complete integrated reproduction script passed in a synthetic checkout with byte-equivalent first-SCC input. No Lean modules are added. The full project `tools/verify.py --changed` was unavailable because no checked-out repository/toolchain exists locally; this does not imply the full verifier passed.

## Specific next construction

A finite certificate requires the same centre-defect glider to **replenish its consumed lattice** rather than exhaust a finite initial reservoir. Search for a finite-state *glider gun* or two-front interface with a phase-periodic source that adds at least 20 new matching exterior coefficients per 88-step block. The measured exact rational drift and the stabilized leading 7+ glider coefficients at 88-spaced times provide a concrete target for a block-substitution/carry-tile renormalization checker. An infinite seed is **UNDECIDED**.
