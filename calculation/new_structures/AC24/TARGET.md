# AC24 exact target

**Predicate.** Fix rooted phase 3 of `lat_p12m9.txt`: the 34-symbol exterior `B_3`, 9-symbol band `W_3`, and `q=14`. Enumerate every junction `J in {0,...,18}^5` and each of the 30 words `U=rotate(9,a,18-a)` (`a=0,2,...,18`). For *every* `k>=40` and every finite palindromic central coefficient word `C` that is physically realizable (odd-length middle coefficient even), define LSD-first `H=B_3++W_3^14++J++U^k`, `P=H++C++reverse(H)`.

Determine whether **120 genuine decimal reverse-and-add operations** can produce the literal return `P'=H'++C++reverse(H')`, `H'=B_3++W_3^14++J++U^(k+5)`.

**Missing necessary lemma.** A 120-step returning decimal certificate with these fixed phase-3 interfaces must restore the entire W9 prefix. We seek a centre-independent *sound* rejection, allowing W9 to be damaged and healed at intermediate steps. By the published phase-rotated T12 insertion theorem (V16), ruling out the reference-width return also rules out the same fixed-interface cycle at all `q>=14,k>=100`. This is a restricted predicate, not a proof that a base-10 Lychrel number exists or cannot exist.
