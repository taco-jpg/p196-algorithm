# Agent S38: odd-centre folded endpoint moment and epoch target

**Label: PAPER PROOF.** This supplies the endpoint residue formula needed to apply the physical mod-101 carry cocycle when the T* coefficient centre has odd length. It does not prove a seam return.

Let C = D ++ [c] ++ reverse(D), let A = B ++ W^q ++ J, and set
Y_k = A ++ U^k ++ D, m = |Y_k|. Then the symmetric pairword is
P_k = Y_k ++ [c] ++ reverse(Y_k), with odd length 2m+1. Define
E(Y) = sum_r (-1)^r Y_(2r) and O(Y) = sum_r (-1)^r Y_(2r+1), modulo 101. Directly folding the mirrored coefficient positions gives

- m = 0 mod 4: V_10(P_k) = 2 E(Y_k) + c;
- m = 1 mod 4: V_10(P_k) = 20 O(Y_k) + 10 c;
- m = 2 mod 4: V_10(P_k) = 2 E(Y_k) - c;
- m = 3 mod 4: V_10(P_k) = 20 O(Y_k) - 10 c.

**Proof.** Since 10^2 = -1 mod 101 and 10^(-1) = -10, the coefficient at index i in Y contributes the folded weight 10^i + 10^(2m-i). If m is even, the odd-index weights vanish and each even-index weight is 2(-1)^r; if m is odd, the even-index weights vanish and each odd-index weight is 20(-1)^r. The central coefficient contributes c 10^m, which is +c, -c, +10c, or -10c according as m is 0, 2, 1, or 3 mod 4. This proves the four cases. Physical realization of odd P_k additionally requires c even.

Under k -> k+5, Y gains five U blocks immediately before D and D shifts 15 positions. Let R(E,O)=(-O,E), s=|A|+3k, and M(X)=(E(X),O(X)). Then the exact moment transition is

M(Y_(k+5)) = M(Y_k) + R^s M(U^5) + R^(s+15) M(D) - R^s M(D).

This follows by additivity of E/O moments and the one-position shift law R. Since m increases by 15, the folded endpoint switches between the even-m and odd-m channels; the four old/new cases are determined by m mod 4. No finite-width assumption is used.

Finally, the physical one-step carry cocycle remains valid for odd L as well. Let y be the normalized decimal output digits and let x=-10 mod 101. Schoolbook normalization gives y_i=p_i+c_i-10c_(i+1), with the terminal carry gamma appended at position L when gamma=1; hence V_x(y)=V_x(P)+2K(P). Symmetry p_i=p_(L-1-i) gives V_x(P)=(-10)^(L-1) V_10(P). Pairing output digits gives S_next=S+10^(L+gamma-1)V_x(y), which simplifies to

V_10(P_next) = (1 - 10^(gamma-2)) V_10(P) + 2*10^(L+gamma-1) K(P) (mod 101).

No parity assumption on L is used. Composing this identity over the rooted 120-step overflow clock gives the existing S12 epoch identity
S_(k+5) = 84 S_k + 57*10^L W_120 (mod 101), where
W_120 = sum_(r=0)^29 7^r (8K_(4r)+4K_(4r+1)+2K_(4r+2)+K_(4r+3))
is the packet-weighted sum of the 120 physical carry sources. Thus the odd-centre endpoint formula determines the unique necessary value

W_120 = (S_(k+5)-84 S_k) * inverse(57*10^L) (mod 101).

This is a parity-complete necessary checksum for the 120-step seam search. It is not sufficient for the actual edge return or for all-phase nonpalindrome safety.

## Independent controls

Run python3 calculation/new_structures/S38/verify_odd_centre_endpoint.py. The verifier passed 8,370 controls. It checks the folded formula and the k -> k+5 moment update against direct coefficient evaluation; on the full q,k grid in {20,40,80,160}, it additionally checks the physical one-step cocycle against Python arbitrary-precision n + reverse(n), a fresh-buffer schoolbook digit adder, and coefficient normalization. The off-diagonal q=20..23, k=40..43 grid checks all 16 q/k mod-4 phase classes across every U motif, junction, and odd centre.

**Exact contribution to the all-time proof:** the mod-101 epoch cocycle now has an exact folded endpoint target for odd-centre T* states, so the odd branch cannot be silently omitted from seam constraints. No self-reproducing seam or decimal Lychrel number is claimed.
