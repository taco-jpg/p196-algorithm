# Z48 independent census audit

**Status: EXHAUSTED-NONE (COMPUTED at the reference width).** The exact 120-step reference-width census finds no W9-prefix restoration for U=(10,9,8), phase 0, J length 3 or 4, at (q,k)=(14,100), for either tested centre parity. This is a scoped cell obstruction, not a global no-Lychrel theorem and not a decimal certificate.

## Exact object and method

The canonical rooted p12/m9 words are B (34 coefficients), W (9 coefficients), U=(10,9,8), with coefficients listed least-significant first and overflow clock g=100010001000 repeated ten times. For each raw junction J, form P=H ++ C ++ reverse(H), H=B ++ W^14 ++ J ++ U^100. The census implements normalization with a fresh carry and then forms the next pairword from mirrored digit sums. It enumerates all 19^3=6,859 length-3 junctions and all 19^4=130,321 length-4 junctions. No modular gate, parity prefilter, or MDD filter is used.

Both centre representatives were run over the full 137,180-J domain: odd C=[0,0,0] and even C=[8,8]. Their counts and mismatch histograms are identical. The stronger assertion for every finite palindromic C is inherited from the T12 reset-cone theorem, not inferred from testing two centres alone.

## Exhaustive counts

| Centre representative | J length | Raw J words | Wrong clocks | B-prefix mismatches | W9-prefix restorations | First mismatch absolute index | W9 offset |
|---|---:|---:|---:|---:|---:|---:|---:|
| C=[0,0,0] | 3 | 6,859 | 0 | 0 | 0 | 135–148 | 101–114 |
| C=[0,0,0] | 4 | 130,321 | 0 | 0 | 0 | 135–146 | 101–112 |
| C=[8,8] | 3 | 6,859 | 0 | 0 | 0 | 135–148 | 101–114 |
| C=[8,8] | 4 | 130,321 | 0 | 0 | 0 | 135–146 | 101–112 |

The W9 band has 126 coefficients at q=14, and its right cut is absolute index 160. Thus offsets 101–114 are 25–12 coefficients before the W9|J cut. Every case restores B and has the exact 30-overflow clock; the first mismatch is strictly inside W9.

### First-mismatch histogram

Offsets are measured from the beginning of W9. Counts are identical for C=[0,0,0] and C=[8,8].

| W9 offset | J length 3 | J length 4 | Total |
|---:|---:|---:|---:|
| 101 | 87 | 1,465 | 1,552 |
| 102 | 143 | 3,203 | 3,346 |
| 103 | 3,140 | 61,043 | 64,183 |
| 104 | 2,781 | 51,493 | 54,274 |
| 105 | 303 | 5,985 | 6,288 |
| 106 | 328 | 6,107 | 6,435 |
| 107 | 47 | 472 | 519 |
| 108 | 19 | 482 | 501 |
| 109 | 0 | 0 | 0 |
| 110 | 2 | 21 | 23 |
| 111 | 8 | 30 | 38 |
| 112 | 0 | 20 | 20 |
| 113 | 0 | 0 | 0 |
| 114 | 1 | 0 | 1 |
| **Total** | **6,859** | **130,321** | **137,180** |

The mismatch-index-array SHA-256 digests (little-endian int32) are 65dc2de3cd89e23d4b1d6d1106e0bdc6e2f98380b0a64698d1c4f3280094f245 for J length 3 and 85a3567012b3f4a616690f4792060edf2520a2a775f5eebf8fb4ee18d620dd2b for J length 4. They are reproducibility checks, not proofs.

## Independent genuine-decimal controls

Eighty controls (8 J representatives × 2 centre parities × q in {14,20,40,80,160}) were checked for 120 steps each. k=100 at q=14 and k=5q at q=20,40,80,160. Every state from the pairword recurrence exactly matched the pairword reconstructed from the ordinary arbitrary-precision integer update n <- n + int(str(n)[::-1]); every physical length increase matched the pairword overflow bit; all clocks were g^10 with 30 overflows.

Across the sampled seams, first W9 offsets were 103–104 at q=14, 157–158 at q=20, 337–338 at q=40, 697–698 at q=80, and 1417–1418 at q=160. The latter four ranges are 22–23 coefficients before the corresponding W9 cut. The exhaustive histogram is the q=14,k=100 result; the larger widths are independent replay controls, not an extrapolation proof.

## Cross-check against neighbouring cells

- **W17:** its committed cell is U=(8,9,10), J length 3–4, even centres. It independently reports 137,180 raw J words and zero W9 restorations, with absolute mismatch ranges 135–144 (length 3) and 135–147 (length 4). Counts and broad seam-local failure agree; exact histograms differ because U differs.
- **W42:** its committed cell is U=(10,8,9), odd centres only, and it applies the sound odd-centre A(J)=0 mod 11 gate, leaving 12,482 J words. Its offsets from the W9|J cut are -25,-24,-23,-22,-21,-20,-19,-18,-16,-15. This is a different U and a gated subset, so its histogram is not supposed to equal this raw 137,180-J census.
- **W43:** no calculation/new_structures/W43 artifact or committed histogram was present on main at audit time, so no exact W43 histogram can honestly be quoted. This audit supplies an independent exact histogram for the requested U=(10,9,8) cell and agrees with the owner update (m): all raw J words miss W9 by 12–25 coefficients at t=120.

## All-width scope and limits

The computed part is the exact reference-width census above. The extension to every q>=14,k>=100 for fixed J and arbitrary finite palindromic C relies on the existing T12 protected-cut insertion theorem and reset-cone centre-independence result: the reference-width W9 mismatch is before the centre, and insertion at the protected W cut shifts the mismatch and cut together. This report does not independently prove those lemmas. With those existing lemmas, the scoped phase-0 J-length-3–4 cell is excluded from a 120-step full-template return. Longer junctions, other phases/U words, moving or growing seams, and the global Lychrel problem remain open.

Reproduce the census and all controls with:
python3 calculation/new_structures/Z48/independent_census.py

Requires Python 3, NumPy, and Numba. The script emits the full machine-readable run as JSON. No results/<Name>.md is added because this is a scoped negative audit, not a missing-lemma theorem or decimal certificate.
