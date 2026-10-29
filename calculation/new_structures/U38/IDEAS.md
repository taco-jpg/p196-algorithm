# U38 ideas and exact route obstructions

## U38-1 — Odd-length palindrome residue saturation (PAPER PROOF; negative route result, no decimal Lychrel claim)

**Theorem.** Let M > 1 be odd with gcd(M, 10) = 1. Let d = ord_M(10) and n = ceil((M-1)/9). For every integer k >= d(n+1) and every residue r mod M, there is a canonical base-10 palindrome P of exact length 2k+1 such that P ≡ r (mod M).

**Proof.** Write the palindrome digits LSD-first as a_0,...,a_(2k), with a_i = a_(2k-i). Set the outer pair a_0 = a_(2k) = 1 and the centre a_k = 0. For m = 1,...,n, select the distinct interior pair positions i_m = k-dm; the bound on k gives 1 <= i_m <= k-1. Since 10^d ≡ 1 (mod M), each selected pair has the same residue weight:

10^(i_m) + 10^(2k-i_m) = 10^(k-dm)(1+10^(2dm)) ≡ 2·10^k = w (mod M).

The number w is a unit modulo M, because M is odd and coprime to 10. The fixed outer pair contributes w_0 = 1+10^(2k). Choose t in {0,...,M-1} with wt ≡ r-w_0 (mod M). Since 9n >= M-1, write t as a sum of n digits x_m with 0 <= x_m <= 9; put a_(i_m) = a_(2k-i_m) = x_m and all other non-outer digits equal to zero. Then P has exact length 2k+1, is palindromic, and its residue is w_0 + w Σx_m ≡ r (mod M). ∎

**Consequence for the assigned moduli.** For M_j = 10^j+1, the multiplicative order is exactly d = 2j: 10^j ≡ -1 (mod M_j), and no smaller positive exponent can give 1. For s < j, 0 < 10^s+1 < M_j; if j < d' < 2j, write d'=j+s and use 10^(d') ≡ -10^s (mod M_j), which cannot equal 1. Hence every residue modulo each 10^j+1, and every compatible residue tuple modulo any finite collection of these moduli, is represented by an odd-length palindrome of every sufficiently large exact odd length. For a finite collection, take its LCM M; it remains odd and coprime to 10 and the theorem applies.

**T* implication and scope.** The target clock has 30 genuine overflow transitions per 120-step macro. Each overflow increases canonical digit length by one, so every macro contains an odd-length state (if the start is even, the first overflow creates one; if already odd, it is already present). At every sufficiently large odd length, no residue class modulo a fixed finite product of 10^j+1 is palindrome-free. Thus **pure finite congruence residues, even with exact length or a finite length phase, cannot provide T*'s all-phase nonpalindrome guard**. This does not rule out invariants coupled to digit windows, physical carries, an infinite state, or a proof that the orbit eventually has only even lengths; it is not a decimal Lychrel certificate or a general no-go for T*.

| j | M = 10^j+1 | d = ord_M(10) | n = ceil((M-1)/9) | sufficient k | sufficient odd length 2k+1 |
|---:|---:|---:|---:|---:|---:|
| 1 | 11 | 2 | 2 | 6 | 13 |
| 2 | 101 | 4 | 12 | 52 | 105 |
| 3 | 1001 | 6 | 112 | 678 | 1357 |
| 4 | 10001 | 8 | 1112 | 8904 | 17809 |
| 5 | 100001 | 10 | 11112 | 111130 | 222261 |

**Independent controls (COMPUTED, supporting the paper proof rather than replacing it).** Run python3 calculation/new_structures/U38/verify_palindrome_residue_saturation.py. It constructs canonical palindromes and independently checks both int(P) % M and the LSD-first digit-array residue. The current run passed 1,232 checks: all residues for M=11, 101, 1001; 100 residues for M=10001; and 19 controls for the finite-family LCM M=101101 = lcm(11,101,1001).

**Redirect:** stop searching for a nonpalindrome guard based only on finitely many residues modulo 10^j+1; add physical digit/carry state or a genuinely orbit-specific restriction. This is narrower than T24's route, which already includes leading/trailing digit-carry constraints.


## U38-2 — Saturation persists under any fixed finite outer digit shell (PAPER PROOF; stronger route obstruction)

**Theorem.** Keep M, d, and n as in U38-1. Fix any finite LSD-first shell A=(a_0,...,a_(s-1)) with a_0 in {1,...,9} and all other a_i in {0,...,9}; this fixes the first s low digits and, by palindromicity, the first s high digits. For every k >= dn+s and every residue r mod M, there is a palindrome of exact length 2k+1 with that exact shell and residue r.

**Proof.** Fix the shell contribution c_k = Σ_(i=0)^(s-1) a_i(10^i+10^(2k-i)) mod M, set the centre digit to zero, and choose the same n positions i_m=k-dm as in U38-1. Since k >= dn+s, these positions lie in [s,k-1], so they do not overlap the fixed shell or its mirror. Their weights are all w=2·10^k mod M, a unit. Choose t in {0,...,M-1} with wt ≡ r-c_k mod M and express t as a sum of n digits in {0,...,9}. Assign those digits to the selected mirrored pairs and set every other unfixed digit to zero. The shell is unchanged, the resulting word remains a canonical palindrome of length 2k+1, and its residue is r. ∎

**Meaning.** Adding any fixed finite outer digit window to a finite family of congruence tests still cannot exclude palindromes at sufficiently large odd lengths. A viable guard must depend on more than a finite residue tuple and a fixed boundary digit shell; in particular, it must use genuinely propagated carry/digit state or another orbit-specific property. This still does not rule out T* or any carry-aware invariant.

**Controls.** Run python3 calculation/new_structures/U38/verify_fixed_shell_saturation.py. Current exact controls passed for every residue of M=11 with three shells, M=101 with a three-digit shell, and M=1001 with a four-digit shell, plus 20 sampled residues for M=101101 with a three-digit shell.
