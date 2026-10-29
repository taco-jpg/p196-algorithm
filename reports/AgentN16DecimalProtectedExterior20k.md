# Agent-N16: CRT-graded protected exterior, finite 20,000-step decimal orbit

## Construction (COMPUTED)
All coefficient words are LSB first; represent pair coefficients 0..18 by 0..9,A..I.
Read the eight rows B_t (length 39) and W_t (length 20) in `calculation/new_structures/agent-N16/rows.txt`.
The rows are transposed from the first rooted p8/m20 SCC of `calculation/decimal_frontier/lattice_formats/p8_scc.txt` and are not a newly discovered SCC.
For integer q>=1 define the *palindromic pair-coefficient* word
`P(q)=B_0 ++ W_0^q ++ reverse(W_0)^q ++ reverse(B_0)`.
Define digits of the decimal seed, LSB first, by `a_i=max(0,P_i-9)` for the lower half
and `a_{L-1-i}=min(9,P_i)` for every lower-half position i. Then the seed has 2(39+20q)
digits, and its folded pairword equals P(q) exactly. The q=300 seed has 12,078 digits.

**Measured at q=300, t=0..20,000 inclusive:** every integer N_t is nonpalindromic,
every pairword of N_t begins `B_(t mod 8) ++ W_(t mod 8)^72`, and the minimum number
of matching positions against the infinitely continued exterior is **1,494** at t=19,994
(39+72*20=1,479, so 72 entire bands are protected). Length is 22,078 at t=20,000.
Every increment in digit length is one iff t is even. A second q=301 seed has
minimum prefix 1,514 at t=19,994. This is a constructive **finite-horizon**, not an infinite, result.

## Direct reproducibility and independence
Run `sh calculation/new_structures/agent-N16/run.sh`. It compiles two separate implementations
without repository imports: `replay.cpp` uses GMP `mpz_add` on the actual decimal
number and independently reverses its digit string; `independent.cpp` uses raw
LSB-first digit arrays and computes every digit of N+reverse(N) by grade-school carrying.
Each engine constructs its seed independently, checks all 20,001 states for nonpalindromicity,
tests the *exact* pairword prefix phase at each step, enforces the 10101010 overflow word,
and hashes the matching-prefix length, digit length and residues modulo 9, 11, 99, 101,
1001 at every state. FNV64 checksums:
`q=100, H=2000: 39a381b57f874fdc`;
`q=300, H=20000: 56371448fdcc1993`;
`q=301, H=20000: 38532804c84fb2e8`.
The two implementations produce the same checksum for each independent replay.
The check is not a finite-cycle closure test, and the central defect is unrestricted.

## Nonpalindromic boundary witness (PAPER PROOF conditional only on the computed prefix)
If an ordinary decimal integer is a palindrome, every coefficient
`P_i=d_i+d_{L-1-i}=2d_i` is even. Inspection of each of the eight B_t rows
shows an odd coefficient. Therefore *any* integer having one of the displayed
exterior prefixes is nonpalindromic, whatever its central defect.
This explains why a freely growing centre is compatible with the finite-horizon guarantee.

## CRT modular filters (PAPER PROOF; not independent existence results)
Write `D(z)=sum_i d_i z^i` for digits LSB first and L for length.
Reversal satisfies `R(10)=10^(L-1)D(10^(-1))` modulo any modulus coprime to 10.
Modulo 9, T(N)=2N. Modulo 99, `10^2=1`, so
`T(N)=2N (mod 99)` if L is odd, and `T(N)=11N (mod 99)` if L is even.
Hence modulo 11, T(N)=0 for even L, and =2N for odd L.
For symmetric pairword P, the contribution of a mirrored pair i,L-1-i modulo M
is `P_i(10^i+10^(L-1-i))`, with a single central term if L is odd.
Modulo 101, since `10^2=-1`, one parity of mirrored pairs cancels when L is odd:
i odd for L=1 mod 4; i even for L=3 mod 4.
Modulo 1001, since `10^3=-1`, for even L the mirrored pairs with
`i=(L-4)/2 (mod 3)` cancel. The joint modular phase uses L mod 12.
These are necessary projectors that guide future multi-lane, drifting-centre searches;
none alone establishes an infinite orbit. Current source checks the unprojected
integer residues on every state, not a claimed extra CRT exclusion.

## Limitation and next direction (UNDECIDED)
The last surviving 72 periodic blocks at t=20,000 are a buffer, not a closed
centre. To advance from a finite-horizon result to a decimal Lychrel proof, seek
a renormalisation or glider that restores periodic-band width at the same rate
the centre consumes it, possibly with a 12-clock CRT phase for the mod 101/1001 lanes.
No all-q, infinite-t, or eventual-palindrome claim is made.
