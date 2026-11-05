# r11d FINAL: decimal exteriors (9-wire streams) and uniform bands, periods 33–48

Studio directory: `~/p196_run/r11d/`. Local copy: `~/Desktop/p196_studio/r11d/`. The repository was read only and nothing was pushed.
Labels used: **COMPUTED** (exact program output, reproducible with the files here) and **UNDECIDED** (capped; nothing is claimed).

## 0. Result in one paragraph
No new decimal exterior stream (9-wire B-cycle) and no uniform band was found for any period T = 33…40. The same holds for the imprimitive clocks at T = 42, 44, 45, 46, 48 (COMPUTED). The check covered every F1 survivor at p = 33–40 (5,400,712 words) plus 5,637 imprimitive words at T = 42–48. Each word is either decided or listed as UNDECIDED:
- 9-wire: 112 words remain open. Two of them are already excluded by Theorem A, which leaves 110 UNDECIDED. Three of those 110 contain the known streams (p11³, p11⁴, N12⁴).
- band: 1,475 words remain UNDECIDED (capped at 12M/40M).

There were 0 accepted streams, so there were 0 NEW ones and no replay was needed. All band hits, including the sanity bands {0} and {18}, were 0.

## 1. Pipeline (in order)
1. **driver.sh** (previous agent, completed): `census.py` with `bin/bx3` over ALL F1 survivors (`lists/`, fc_enum), p = 33..40, 6 shards. Pass c1 used cap 300k states / 20 s. Pass c2 used 3M / 60 s on the capped words.
2. **bxb** (new, `src/bxb.cpp`): this is bx plus uniform-band acceptance (`-band "6,12;2,4,8,16,14,10;0;18"`).
   - A cut state (L,H,Y) is band-accepting when L_t = H_t = BC(u_{t+ph}) for all t and Y_t = BR(u_{t+ph}) at the overflow times, for every phase ph.
   - This is reach.cpp `accepts()` in BAND mode, via Lemma X (bx ≡ reach). The BFS is identical, so EXHAUSTED/ACCEPT keep their wire meaning.
   - Controls (`ctrl/bxb_controls.out`, all as expected):
     - base 13, 1010010000: band {8,16} phase 0 @55 and phase 1 @75, 250,302 states. This matches calib.sh (reach 250,301 + root).
     - base 4, 011001: band {2,4} phase 1 @13, 957 states. This matches Seal / calib.
     - base 10, (01)^4: no band, 244,785 states.
     - p11: e=00111010011@29.
     - p12: 3 streams @53, 136,653 states (nosym) and 45,571 (sym).
3. **driver2.sh**: bxb over ALL F1 survivors at p = 34, 36, 38, 40 (bands with q | T: {6,12} for all four, and the 6-cycle also at 36), with passes c1 and c2. It then ran bxb over ALL imprimitive F1 survivors at p = 42, 44, 45, 46, 48 (`lists_impr/`, `py/impr_list.py`).
4. **driver3.sh**: every word still capped was re-run with bxb at 12M / 60 s (c3).
5. **K-head period filter** (`kfam/khead_len.cpp`, `kfam/run_res_par.sh`): every word still open after c3 (2,314 words) was tested as pattern = g with L = p, Kmax 60, and a watchdog of 3 GB / 60 s.
   - "family dies at K=k" means G_k has no closed walk of length p. That rules out every 9-wire exterior with clock g, by Lemmas A1–A4 of `three_divides_r/PROOF.md`. The proof is unchanged; only the "12 ∤ period" test is replaced by "period | L".
   - `trans()` is byte-identical to khead4.cpp.
   - Controls:
     - The p11 word (L=11) and 0001 (L=12) survive.
     - 01 with L=36 dies at K=3 (the 8|p theorem).
     - 0001 with L=40 dies at K=21, consistent with Theorem A.
     - All 3 residue words that contain known streams (p11³, p11⁴, N12⁴) SURVIVE.
     - One cross-check: (00011)^8 dies at K=6 in kfam, and bx3 with a large cap gives EXHAUSTED at depth 6 (16.2M states).
   - The filter is used for the **9-wire only**. Bands are decided only by bxb.
6. **driver5.sh**: the 109 words that survived both (excluding the 3 known repetitions) were run with bxb at 40M / 300 s. None was decided; all stayed CAPPED.

## 2. Table (COMPUTED; out/final_table.md)
| p | words | wire: bx EXHAUSTED | ACCEPT | K-head DIES | wire UNDECIDED (known rep.) | band-checked | band EXHAUSTED | band hits | band UNDECIDED |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 33 | 97997 | 97964 | 0 | 22 | 11 (1) | – | – | – | odd T |
| 34 | 149930 | 149884 | 0 | 40 | 6 | 149930 | 149884 | 0 | 46 |
| 35 | 229202 | 229126 | 0 | 63 | 13 | – | – | – | odd T |
| 36 | 351150 | 351036 | 0 | 102 | 12 | 351150 | 351036 | 0 | 114 |
| 37 | 537852 | 537654 | 0 | 187 | 11 | – | – | – | odd T |
| 38 | 824965 | 824643 | 0 | 311 | 11 | 824965 | 824643 | 0 | 322 |
| 39 | 1265801 | 1265274 | 0 | 507 | 20 | – | – | – | odd T |
| 40 | 1943815 | 1942932 | 0 | 871 | 12 (incl. (0001)^10) | 1943815 | 1942932 | 0 | 883 |
| 42 imprim. | 707 | 693 | 0 | 10 | 4 | 707 | 693 | 0 | 14 |
| 44 imprim. | 1001 | 981 | 0 | 16 | 4 (1; incl. (0001)^11) | 1001 | 981 | 0 | 20 |
| 45 imprim. | 69 | 64 | 0 | 3 | 2 | – | – | – | odd T |
| 46 imprim. | 1503 | 1474 | 0 | 28 | 1 | 1503 | 1474 | 0 | 29 |
| 48 imprim. | 2357 | 2310 | 0 | 42 | 5 (1) | 2357 | 2310 | 0 | 47 |

- **COMPUTED: (0001)^10 at p40 and (0001)^11 at p44 are excluded.** Theorem A of three_divides_r requires 3 | r. The kfam control "0001, L=40, dies at K=21" is consistent with that.
- The remaining open words are listed in `out/final_open_wire.txt` and `out/final_open_band.txt`. Among them are (0001)^9 at p36 (3 | 9), (01)^20 at p40 (8 | 40), p11³ at p33, p11⁴ at p44 and N12⁴ at p48. Each of these is UNDECIDED; the last three are expected to be repetitions of known streams.
- Odd T: neither band period (q = 2 or 6) divides an odd T, so there is no uniform band whose combined period is odd.

## 3. Scope (what is NOT claimed)
- **The "T" of a band, as in r11g PROOF.md.** A band result at T covers only templates with lcm(left-end period, band period) = T.
  - For T = 34–40, the word lists contain every F1 clock of length T, imprimitive ones included (for example g = h² with |h| = 17). That covers left ends of period T/2 or T/3 under the {6,12} band and the 6-cycle. For example, T = 34 contains p17², and T = 36 under the 6-cycle contains the 9 | G words.
  - For T = 42–48, only the IMPRIMITIVE clocks were run. Primitive clocks of length 41–48 (tens of millions of F1 words) were **not run: UNDECIDED**. T = 41, 43, 47 are not covered at all.
- I did not use the 9 | G condition for the 6-cycle as a filter. Every word was checked, which is a superset.
- bx3 support: the key needs T ≤ 59. Odd p from 33 to 40 would need T = 2p ≥ 66 for a {6,12} band. Those combined periods lie outside 33–48 and are not claimed.
- Above the left end of a band template there are band cells, not padded 9s. So the K-head filter (Lemma A1) is not used for bands. The band UNDECIDED list is therefore longer than the wire list.

## 4. Files
- Sources:
  - `src/bxb.cpp` (wire + band), `src/bx.cpp` (repo copy)
  - `py/census_b.py`, `studio/run_stage_b.sh`
  - `driver2.sh` … `driver5.sh`
  - `kfam/khead_len.cpp`, `kfam/run_res_par.sh`, `kfam/run_kfam.sh`, `kfam/run_kfam_ctrl.sh`
  - `py/report_r11d.py`, `py/final_r11d.py`, `py/impr_list.py`
- Results:
  - `out/db/*.jsonl.gz` (bx3 wire DB), `out/dbB/*.jsonl.gz` (bxb wire + band DB)
  - `out/final_table.md`, `out/final_open_*.txt`
  - `kfam/res_kfam_w*.txt`, `kfam/kf_*.out`
  - `ctrl/bxb_controls.out`, `driver*.log`
- Deleted as regenerable: `lists/` (fc_enum), the shard files `out/studio*`, `lists_res/`.

## 5. Budget incident (recorded)
One unguarded test run of `khead_len 60` on a p39 word reached **230 GB RSS** for a short time before it finished. That run was over the 40 GB budget. Every later kfam run used a watchdog (3–8 GB). All other runs stayed at ≤ 6 compute threads and ≤ 35 GB.
