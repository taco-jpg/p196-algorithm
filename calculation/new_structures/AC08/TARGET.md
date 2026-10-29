# AC08 exact target
Phase-0 p12/m9 template P(q,k;J,U,C)=H ++ C ++ reverse(H), H=B0 ++ W0^q ++ J ++ U^k.
B0 and W0 are canonical lattice rows, J=[5], q=14,k=100. U belongs to {(9,14,4),(14,4,9),(4,9,14)}.
C is palindromic with coefficients 0..18, odd midpoint even. Test the 120 genuine reverse-and-add steps and central radius 122+|C|+30 of target P(14,105;J,U,C).
An all-time return at every sufficiently large q,k, including carry ports, gamma clock and nonpalindrome guard, is NOT proved.