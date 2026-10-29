# AC18 exact target

Rooted phase-9 p12/m9, B_9 and W_9 from `lat_p12m9.txt` (LSD-first coefficient words). For every J in {0,...,18}^3 union {0,...,18}^4 and every U among the 30 rotations of (9,a,18-a), a even 0..18, and **every** palindromic coefficient centre C in {0,...,18}^*, whose middle coefficient is even if odd-length: test the necessary equation

P(14,100;J,U,C) --[120 genuine base-10 reverse/add steps]--> P(14,105;J,U,C), where P=H+C+reverse(H), H=B_9 + W_9^q + J + U^k.

The immediate missing lemma to decide is that there is no such fixed-J 120-step endpoint at the reference width for |J|=3,4, without assuming W9 stays undamaged before the endpoint. An exhaustive no-go is not an all-time decimal Lychrel certificate, and gives no statement about moving J, other phases or seam widths, or wider q,k without a separately verified lift.