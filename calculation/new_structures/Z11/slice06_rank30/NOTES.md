# Z11 rank-30 audit notes

- Audited the latest Z10 slice-6 DONE against the shared lexicographic 30-U ordering; ranks 6 and 18 were listed, but rank 30=(18,9,0) was absent.
- Claimed this omitted subcell in issue #475 comment 6496054201.
- Exhausted all 2,476,099 J words with the AVX2 centre-independent endpoint cone. All have the exact clock and a W9 mismatch; no unknown or short prefixes.
- Ten genuine decimal controls pass across q=14,20,40,80,160 with even/odd legal centres; integer, digit-array, and pairword engines agree.
- This corrects coverage of the slice-6 census; it does not prove or disprove decimal Lychrel existence.
