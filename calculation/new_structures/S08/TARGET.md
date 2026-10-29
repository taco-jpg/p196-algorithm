# S08 target: R18 second-epoch carry obstruction

Exact scope: phase-4 rooted p12/m9 family with B=B4, W=W4, J=[17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2], U=[18,0,9], and odd palindromic C=[a,b,a] where 0<=a<=18, b is even in [0,18], and 2a-b=5 mod 11. This leaves exactly 17 centres.

The symbolic claim is restricted to independent q,k>=512. For each of those centres, the exact 120-step pairword image first differs from T(q,k+5) at index 9q+35 (actual 9, expected 5); after 240 steps the first difference from T(q,k+10) is at 9q+12 (actual 6, expected 5). The rooted outer prefix is restored at the first endpoint but not the second.

The local carry diagnosis is independently checked on all 16 integer pairs q,k in {20,40,80,160} x {20,40,80,160}: at state 135 / phase 7, the W-ending coefficient and its high mirror are 17; both carry-ins are 0. The next phase requires coefficient 15 but receives 14. This rules out centre-only repair for this fixed seam; it is not a global no-go for the decimal Lychrel problem.
