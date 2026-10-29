# AC42: exact phase-9 odd-centre two-epoch gate

**PAPER PROOF.** Necessary condition on genuinely repeated 120-step decimal returns, not a Lychrel certificate. The full physical endpoint-only phase-9 J6 cell is **UNDECIDED**, as are all even-centre, moving-seam and arbitrary one-epoch returns.

## Theorem (all q,k, with physical-return premise)

Let P(q,k)=H ++ C ++ reverse(H), H=B9 ++ W9^q ++ J ++ U^k, where B9 and W9 are the phase-9 rows of calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt; |J|=6 with coefficients 0..18; U is one of the 30 charge-zero 3-letter rotations; C=(4,14,4). Suppose a canonical decimal source with pairword P(q,k) returns by 120 genuine reverse-and-add steps to **exactly** P(q,k+5) and by another 120 steps to **exactly** P(q,k+10), with identical B9,W9,J,U,C and no implicit change of phase. Then

A(U) ≡ 5 (mod 11), and A(J) ≡ 9 (mod 11),

where A(X) is its least-significant-first alternating coefficient sum. This is a necessary condition for a fixed-J/C/U all-time pumping cycle. It uses neither strict-phase W9 preservation nor any assumption about intermediate junction geometry.

## Proof

An integer of even decimal length has reverse(n) ≡ -n (mod 11). Therefore, once an orbit encounters even digit length, its next integer is zero mod 11, and every later integer remains zero mod 11. The initial P has odd length 2(34+9q+6+3k)+3. An exact 120-step P(q,k)→P(q,k+5) gains 30 digits, requiring 30 actual overflows. Hence an even-digit state occurs strictly before the first 120-step endpoint. Both the 120-step and 240-step pairwords represent their respective **next** integers, so their alternating coefficient sums are zero mod 11.

For any odd palindromic C and even-length B,J with odd-length W,U, direct mirror expansion gives the exact identity

A(P(q,k)) = 2A(B) + 2(q mod 2)A(W) + 2(-1)^q A(J) + 2(-1)^q(k mod 2)A(U) + (-1)^(q+k) A(C).

Substitute k+5 and k+10 and subtract the two zero-residue conditions. Their different k parities imply A(U)=A(C) mod 11. The remaining even-k equation gives

2A(B)+2(q mod 2)A(W)+(-1)^q[2A(J)+A(C)] ≡ 0 (mod 11).

For the published phase-9 rooted rows, A(B9)=-6, A(W9)=12=-2A(B9), and A(C)=-6. Both q parities therefore yield 2A(J)+A(C)=-2A(B9)=12 (mod 11), so A(J)=9 and A(U)=A(C)=5 (mod 11). Checking all 30 U rotations leaves exactly 1-based ranks 1=(9,0,18) and 29=(18,0,9). QED.

## Exact computation and controls

An 11-residue dynamic-programming convolution counts all 19^6 J words without sampling, independently of decimal replay.

- At J[0]=0: 225,117 of 19^5=2,476,099 J words pass A(J)=9; with the two permitted U words only 450,234 of 74,282,970 odd-C J/U tuples pass the two-epoch necessary condition. Exactly 73,832,736 are excluded as **two consecutive restored 120-step endpoints**, not as single-epoch returns.
- Across all J: 4,276,922 of 47,045,881 words pass the J gate; with U, only 8,553,844 of 1,411,376,430 odd-C tuples survive the necessary gate.
- Independent direct enumeration of all 19^5 fixed-J[0] words confirms the DP count 225,117. A separate 1,000-case random exact alternating-sum test checks the mirror identity and even-centre parity.
- Independent ordinary Python-bigint decimal n+reverse(n) and a **non-in-place schoolbook digit-array engine** agree at every step of 20 controls (4 J/U/C settings times q/k = 14/100, 20/80, 40/160, 80/320, 160/640), 240 steps each, 4,800 checked transitions. Every control has the genuine phase-9 overflow sequence (0001)^60, total 60. These finite replays only audit the arithmetic, not an infinite return.

Run from repo root:

    python3 calculation/new_structures/AC42/phase9_gate.py --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt
    python3 calculation/new_structures/AC42/test_phase9_gate.py

## What remains missing

Even palindromic centres (e.g. C=(4,4)) have A(P)=0 identically, so **no** odd-centre congruence may prune them. The two surviving U rotations and admissible J residues are not returning seams. The exact two-ended physical 120+120 endpoint condition, a uniform insertion proof and an intermediate nonpalindrome guard remain unsolved. This is a finite-feasibility gate bearing on the missing periodic repair lemma, not the repair itself.
