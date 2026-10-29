# R08 moving-interface target

**UNDECIDED** original goal: obtain a genuine 120-step all-time p12/m9 B34-W9-U3 return with fixed W9 count q, U3 exponent k -> k+5, full two-ended physical carry ports, and a non-palindrome witness at every step. A moving J(k) may carry state, but its width/position must obey the exact 30-overflow length law.

**PAPER PROOF subroute obstruction (precise scope):** let q be any of 20,40,80,160 and U any rotation of (9,a,18-a) with even a in [0,18]. Put B=B34 and W=W9 from lat_p12m9.txt. For every r>=200 and EVERY palindromic digit-pair core D (any width or contents, 0..18, with any odd midpoint even and a canonical realization), define P=B W^q U^r D rev(U)^r rev(W)^q rev(B). After 120 genuine decimal reverse-and-add steps, the output pairword does NOT begin with the literal B W^q. In particular, no moving-junction repair which permanently recedes beyond 200 U blocks can close the claimed 120-step return for these q.

**Finite kernel closing the universal quantifier r and D:** check 120 ordinary steps of B W^q U^200 [12] rev(U)^200 rev(W)^q rev(B), for all 120 (q,U) cases. At every time t<120, position zero is not 9; the last two positions of the protected prefix of length m-3t are not both 9; and at time 120 one of the last 30 W positions differs from literal W. The exact carry-shield lemma, proved in NOTES.md, transfers these facts to ALL r>=200 and arbitrary D.

Reproduce: python3 calculation/new_structures/R08/shield.py. This is a negative obstruction to **receding** interfaces only, not a decimal Lychrel existence proof or a no-go for interface-anchored active repair.
