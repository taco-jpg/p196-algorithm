# Agent S38: parity-complete mod-101 carry-source delta

**Label: PAPER PROOF.** This extends the all-width physical carry-source identity used by S12 to odd-length palindromic centres. It is a necessary checksum, not a return or certificate.

Let A = B ++ W^q ++ J, V = reverse(U), and
P_k = A ++ U^k ++ C ++ V^k ++ reverse(A), with |U|=|V|=3. Let c_i be the carry OUT of coefficient P_k[i-1] when normalizing P_k to decimal, and
K(P_k) = sum_{i=1}^{|P_k|} c_i (-10)^i (mod 101).
For a three-symbol block X, let a_X(b) be its local weighted carry sum
sum_{j=1}^3 e_j(-10)^j when the incoming carry is b; let
beta_X = F_X(0) = F_X(1) be its constant outgoing carry. These are defined
for every charge-zero U3 motif in T*, and for its reverse.

Put s = |A|+3k, t=s+|C|, z=t+3k, G_k=sum_{r=0}^{k-1}10^r (mod 101), and let b be the actual carry entering the first V block. Let K_C and K_Z denote the contributions to K(P_k) from the coefficient intervals [s,s+|C|) and [z,|P_k|), respectively. Then, for every q, every k>=1, and every finite coefficient centre C,

K(P_(k+5)) - K(P_k) = (-10)^s a_U(beta_U) + 9 K_C + (-10)^t [9 a_V(b) + (1 - 2 G_k) a_V(beta_V)] - 2 K_Z (mod 101).

**Proof.** Write x=-10 mod 101. Since x^4=1, x^3=10, x^15=10, and x^30=-1, the five new U blocks contribute x^s a_U(beta_U) because 1+10+10^2+10^3+10^4 = 1 (mod 101). The first U block's carry map is constant, so all carries in the unchanged prefix and first k U blocks are identical. Thus the carry trace entering C is unchanged; the entire C carry contribution shifts by 15, changing by (x^15-1)K_C = 9K_C. The carry entering the first V block is therefore the same b, and the V carry map is also constant. Its old weighted contribution is x^t[a_V(b)+(G_k-1)a_V(beta_V)]; its new contribution is x^(t+15)[a_V(b)+(G_(k+5)-1)a_V(beta_V)]. Using G_(k+5)=G_k+10^k and the period-four geometric identity reduces their difference to the displayed V term. The suffix carry trace is unchanged but shifts by 30, so its contribution changes by (x^30-1)K_Z=-2K_Z. All earlier contributions cancel. No step uses the parity of |C|. For a physical odd-length T* pairword, C must be palindromic with an even midpoint coefficient; that condition supplies its canonical integer realization but is not needed by the carry identity itself. Q.E.D.

## Independent controls

- calculation/new_structures/S38/odd_centre_delta.cpp: compiled with g++ -O3 -std=c++17 -Wall -Wextra -Werror; 69,120 cases passed, including every q,k residue class mod 4 over four width scales and all 30 U motifs, three fixed junctions, and three odd palindromic centres.
- calculation/new_structures/S38/verify_odd_centre_delta.py: independent Python arbitrary-precision decimal oracle; 8,370 cases passed, including all exact q,k combinations in {20,40,80,160} and a 4x4 off-diagonal phase grid.
- Each control realizes both P(q,k) and P(q,k+5) as actual canonical decimal integers and checks n+reverse(n) against both schoolbook digit addition and coefficient normalization. The computed tests are implementation controls only; universality follows from the symbolic carry-reset proof.

**Exact contribution to the all-time proof:** the physical mod-101 carry-source checksum is now available without excluding the odd-centre branch. It does not establish a self-reproducing seam, prove all intermediate phases safe, or prove decimal Lychrel existence.
