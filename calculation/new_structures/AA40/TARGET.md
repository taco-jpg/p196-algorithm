# AA40 target statement

Try to prove or refute the following exact statement, not a finite-horizon proxy.

For the rooted decimal p12/m9 source data B (length 34), W (length 9), overflow clock g=(100010001000)^10, a charge-zero U3 word U, a finite seam J, and a palindromic pairword centre C, define
`H(q,k)=B ++ W^q ++ J ++ U^k`
and
`P(q,k)=H(q,k) ++ C ++ reverse(H(q,k))`.

Find a specified seam/centre state or a proved closed moving-seam family for which 120 genuine decimal reverse-and-add steps send `P(q,k)` to `P(q,k+5)` with q unchanged, for all independent q>=q0 and k>=k0, restoring the same rooted clock, W9 band, seam state, centre state, and all physical carry ports. Prove every intermediate state is non-palindromic. A different counter ledger is allowed only if the exact return family is restated and proved.

Current status: UNDECIDED. The Q999/Q111 carry-cocycle relation is a necessary condition only; it does not itself establish or refute this return.