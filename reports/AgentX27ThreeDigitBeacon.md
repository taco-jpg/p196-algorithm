# X27: exhaustive small-seed decimal parity beacon and 100,000-step survivor

**Label: COMPUTED.** The finite arithmetic identities and exact `879` / `978` coalescence are also elementary PAPER PROOF ingredients. The result is not an infinite Lychrel certificate.

## Finite alphabet safety property

For any decimal integer `N` with `n` canonical digits `d_0,...,d_(n-1)` least-significant-first, define its pairword `P_i=d_i+d_(n-1-i)` and `F_32(N)` to mean `exists i<min(32,floor(n/2)) such that P_i is odd`. Every decimal palindrome has even `P_i` everywhere, so `F_32(N)` is a sufficient nonpalindrome witness. Unlike an odd **middle** coefficient for an odd-length number (impossible since `P_mid=2*d_mid`), this property is meaningful for both parities and for every length.

## Complete 2- and 3-digit census through 5,000 steps

Two algorithmically distinct implementations enumerate every seed from 10 to 999 inclusive, stopping at the first failure of `F_32` or after step 5,000:

1. `small_scan.cpp` stores each decimal integer as a vector of digit values, performing ordinary schoolbook addition against its literal reversal. `c++ -O3 -std=c++17 small_scan.cpp -o /tmp/x27scan && /tmp/x27scan 5000 32` returns exactly two survivors `879 978`.
2. `small_scan_independent.py` stores Python arbitrary-precision integers, computes the decimal representation afresh at every step, parses the reversed string as a new integer, and checks `F_32` by characters. `python3 small_scan_independent.py 5000` independently returns exactly `[879,978]`, with 988 failed seeds.

Both positive seeds have three-digit pairword `(17,14,17)`, since the outer digit sum is `8+9=17` and the centre contributes `7+7=14`. The exact arithmetic successors of both are the same `1857`, so their integer orbits coincide from step 1 onward. No assumption about their future dynamics is needed for this equality. This is an exact finite family, not merely a computational coincidence.

## Independent 20,000-state replay and longer 100,000-state check

The existing `verify.cpp` has a new optional explicit decimal seed argument (`./verify 0 20000 32 879`). It cross-compares GMP arbitrary-precision arithmetic with a separate literal decimal digit vector **at every** state `t=0..20000`. It also validates the exact full-column carry parity law for both overflow cases and the full resulting prefix against the two-sided incoming carry transducer, with the prefix shortened to `floor(n/2)` when `n<64`. All 20,001 states satisfy `F_32`. At `t=20000` the integer has 8,245 digits and residue 476991197 mod 1000000007; there are 8,242 overflow steps, 9,987 odd-length and 10,014 even-length states, and maximum earliest odd index **17**. FNV-like parity trace checksum: `38dd817f4a0c68c3`.

The separate `longrun.cpp` with `./longrun 0 100000 879` replays the literal-digit arithmetic to 100,000, recording the first odd pair index at each state and checking true palindrome digit symmetry only if no odd pair is found. It finds maximum earliest-odd index **22**, so `F_32` is always true. At step 100,000 the integer has 41,387 digits, and 41,384 overflow events have occurred. There are no all-even pairwords; 25 states have earliest odd index >=16 (the first at t=9,237), and zero have earliest odd index >=32. The 100k extension is NOT a second independent GMP replay; the independent GMP agreement covers 20k.

Since each starting seed 879 or 978 has `F_32` and both become 1857 after one step, the whole finite 100k claim applies to both without rerunning their common tail separately. The literal-digit runs do not imply a permanent parity invariant. In particular, the `F_32` census's rejection of 196 at `t=8` is **not** evidence of a palindrome; the assertion is only about loss of this sufficient parity witness. This directs the next format search to a *hybrid two-state obstruction*, using odd pair coefficients when present and a separate digit-inequality witness for the rare all-even-pair states, rather than exclusion of otherwise promising 196-type trajectories.

## Reproduction

Run `bash calculation/new_structures/agent-X27/small_reproduce.sh` from any working directory, with C++17, GMP and Python3 installed. The script compiles all C++ sources, runs both census engines, independently replays 879 through 20k, extends the literal-digit check to 100k, asserts the exact deterministic summaries, and verifies the two integer starters' first-step coalescence.

This is **COMPUTED FINITE HORIZON**, with exact 2- and 3-digit seed scope, not a proof of any base-10 Lychrel number, not a uniqueness statement among all larger seeds, and not a Lean result.
