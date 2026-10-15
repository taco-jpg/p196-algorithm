# How sharp are the certified bounds? (diagnostic, not proofs)

The seven-column certificates give upper bounds on `H(P)`, the largest `t` with `T^t(A) = P` for some
positive `A`, over all palindromes `P` of a prefix family. The abstraction over-approximates, so the
true supremum may be smaller. These scripts compute the **exact** depth for concrete palindromes.

Method (`exact_depth.py`): for a palindrome `P` with leading digit at least 2, every predecessor has
pair-sum word equal to the digit word of `P` (this is `PalindromeBridge.canonical_last_step`), and the
pair-sum word of `T(X)` depends only on that of `X`. So `H(P) = 1 + D(digits(P))`, where `D` is the depth
of the exact backward tree of pair-sum words under `F`, which is finite at each width (0 if the digit word
is not an admissible pair word). Exact preimages are enumerated by two outside-in carry transducers (same
width; one shorter with overflow), every candidate re-checked by the forward map. Both transducers agree
with brute force on 1,668 image words of widths up to 8 (`python3 exact_depth.py`).

Exhaustive results (`scan_prefix.py PREFIX WMAX [WMIN]`), all palindromes of each width:

| family | widths scanned | best exact depth found | at | certified bound |
|---|---|---:|---|---:|
| 218 | 3–18 | 15 | width 16, `2189992442999812` | 34 |
| 777 | 3–16 | 14 | width 13, `7779554559777` | 25 |
| 217 | 3–16 | 15 | width 15, `217459000954712` | 23 |

Per-width maxima are in `scan_*.jsonl`; they are not monotone in width (218: 15 at width 16, 7 at 17,
10 at 18). Explicit integer starts (`witness.py`) are kernel-checked in `../controls/Witnesses.lean`:
`orbit 10199522000 15 = 2189992442999812`, `orbit 183981000 14 = 7779554559777`,
`orbit 1020400000 15 = 217459000954712`, each a palindrome of its family.

So the true suprema lie in [15, 34], [14, 25] and [15, 23]. Wider palindromes were not scanned
exhaustively and may have deeper ancestry; no sharpness claim is made either way.
