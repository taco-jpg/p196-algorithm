# Z03 target: phase-0 rooted p12/m9, five-coefficient junction

**Target status:** decided for this slice by `REPORT.md`; no positive return is claimed.

The family is the canonical rooted decimal pairword

`P(q,k;J,U,C) = B ++ W^q ++ J ++ U^k ++ C ++ reverse(U)^k ++ reverse(J) ++ reverse(W)^q ++ reverse(B)`,

with LSD-first coefficients, the phase-0 `B34/W9` rows and clock `g=(100010001000)^10` from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, `|J|=5`, and an arbitrary finite admissible palindromic pairword centre `C`. For odd-length `C`, its midpoint coefficient must be even so the source is physically realizable. The exact reference width is `(q,k)=(14,100)`.

The 30 distinct charge-zero U3 rotations are ordered lexicographically as integer triples. The assigned slice is 1-based ranks `3,15,27`, namely:

- rank 3: `U=(2,9,16)`
- rank 15: `U=(9,8,10)`
- rank 27: `U=(16,2,9)`

Every `J` word in `{0,...,18}^5` is represented once by its base-19 code, least-significant coefficient first. Thus the raw domain is exactly `3 * 19^5 = 7,428,297` `(U,J)` pairs. The endpoint-W9 check is independent of `C` by the T12 reset-cone bound; no centre values are enumerated.

**Exact question:** does any member of this assigned `(U,J)` domain restore the complete rooted `B W^14` prefix at step 120? Such restoration is necessary for the requested T* return. See `REPORT.md` for the exhaustive decision and its precise limits.
