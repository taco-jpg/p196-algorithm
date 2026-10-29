# Agent N19: bidirectional de-pumping and a shorter decimal two-band 20,000-step witness

**PAPER PROOF** finite counter de-pumping theorem, conditional only on the fully reproduced finite arithmetic/matrix checks. **COMPUTED** two independent complete 20,000-step arithmetic replays and literal shape controls. No infinite orbit or decimal Lychrel proof.

## Stronger constructive family

For **every integer k >= 13314**, let `N_k` be the decimal integer with digit string

    9 8^k 59 9^k 80 7^k 20 0^k 1.

For **each t from 0 through 20000**, its ordinary decimal reverse-and-add orbit is not a palindrome and its exact folded pairword is

    H_t(k) = L_t ++ x_t^(a_t + k - 13314) ++ J_t ++ y_t^(b_t + k - 13314) ++ R_t

with the two disjoint ordered bulk runs of length at least 100 at **every** state, the same six-phase clock `(x,y)=(8,16),(16,14),(14,10),(10,2),(2,4),(4,8)`, and the same exterior/junction words `L_t,J_t,R_t` independent of `k`. At time 20,000 the central `J_t` has 13,183 coefficients. This improves the earlier bound k>=15000 by 1,686 (6,744 fewer initial decimal digits) without giving up any checked steps or independent verifications.

The canonical k=13314 seed has **53,264 decimal digits**, final t=20000 number has **61,497 digits**. At step 20,000 the two surviving runs have lengths **134 and 100**. Both independent engines agree on **every 20,001-row full-pairword FNV64 hash and every block boundary/length statistic**, with complete trace CSV SHA256

`0992a0a6c9922c58ef7ce696b8496227974ac01eec066289ca41d8019c5a40fe`.

## New detail: bidirectional finite-monoid de-pumping

The exact 40-state carry transducer in `unary_allk.py` has, for all six phases and both possible overflows, idempotent transition matrices `M²=M` for each of the two synchronized paired coefficient columns. As noted in the previous N19 all-counter report, a true edge with a positive-length constant paired column can have **arbitrarily many copies inserted** without changing the accept/reject result or the exact arithmetic edge. More strongly, **any positive number of copies may also be deleted**: for any a,b>=1 and a',b'>=1, `M^a = M^a' = M`; this is an equality of the full two-ended carry relations, not a heuristic about isolated carries.

The k=15000 baseline trace has both aligned source/target bulk intersections of length at least 1820/1786. Deleting d=1686 paired columns from each run leaves aligned overlaps at least 134/100 at all 20,000 edges, so every single edge remains exact. At t=0 the physically canonical seed k=13314 is precisely the de-pumped source; by induction all t=0..20000 obey the shortened symbolic formula. Odd pair coefficients lie outside the even-valued bulk cells, minimum two at every t, and remain when bands shrink, so none of these iterates is palindromic. From that shorter reference, ordinary upward pumping gives the theorem for **all** k>=13314.

The length-100 condition is locally tight at this boundary: with k=13313 the direct digit-list engine first fails the defined two-macroscopic-band shape at t=19999 (its right longest-phase run is only 99); with k=13314 it has right run >=100 through t=20000. This **does not** assert that k=13313 reaches a palindrome, nor that no alternative seed or alternative template works. It is a positive witness optimization with one adjacent shape-threshold control, not an exclusion census.

## Reproduce and limits

    bash calculation/new_structures/agent-N19/run_optimized.sh

This compiles two independent engines (`bulk20k_digits.cpp`, `bulk20k_gmp.cpp`), uses GMP-only step-10000 checkpoint so no other engine bootstraps it, compares all 20,001 per-state records, verifies the SHA256 and compact data under `optimized_checkpoints.csv`, checks all 12 matrix identities and 20,000 aligned overlaps, replays both k=13314 and k=13315 and checks exact full folded-word de-pumping and odd witnesses, and confirms the adjacent k=13313 shape threshold. Requires GMP/g++, Python3, sha256sum. The finite pairword and counter claims are **not** an infinite-time certificate; bulk lengths remain erosive and a replenishing outer rewrite is still missing. No Lean claim.