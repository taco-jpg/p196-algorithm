# STUDIO_JOBS — W5 decimal exterior frontier on the 32-core Mac Studio

Limits obeyed by every command below: <= 16 parallel processes (`NSHARD=16`), `nice -n 19`, <= 8 GB per process.
macOS ignores `ulimit -v`, so the memory of a process is set by the engine cap `-cap` (visited cut states): table = 2^k entries, k = smallest with 0.6*2^k >= cap,
entry = 16 B (`bin/bx`, p<=32) or 24 B (`bin/bx3`, p<=59); +50% transient while the table doubles; frontier vectors add ~0.1-0.5 GB.

| cap (states) | bx (16 B) table | bx3 (24 B) table | use |
|---|---|---|---|
| 300 000 | 8 MB | 12 MB | first pass |
| 3 000 000 | 128 MB | 192 MB | standard |
| 12 000 000 | 512 MB | 768 MB | rung 1 for residue |
| 48 000 000 | 2.1 GB | 3.2 GB | rung 2 |
| 150 000 000 | 4.3 GB (6.4 GB peak while doubling) | 6.4 GB table (9.6 GB peak while doubling: too much, use cap <= 80M = 3.2 GB table) | rung 3 (bx); for bx3 stop at 80M |
| 300 000 000 | bx1 only (8 B keys): 4.3 GB (6.4 GB peak) | - | the (01)^8 word (p=16, key = 59 bits with mixed-radix Y) |

Everything is resumable: re-running a stage skips decisive words (EXHAUSTED/ACCEPT) and only retries capped words whose old cap is smaller than the new one.

## 0. What is shipped / state at hand-over
`out/db/b10_p{p}.jsonl` (one JSON record per survivor word: status, visited states, depth, secs, cap, wdone, accepted e), produced from `out/db_b10.jsonl` by `py/split_db.py`.
Survivor lists are NOT shipped (210 MB): regenerate them in seconds with `studio/make_lists.sh` (the enumerator output is deterministic; lists identical to the ones used here).
`out/fc_counts_b10.txt` holds the expected F1 survivor counts per (p,G) for p<=40; `make_lists.sh A B` writes the same numbers for p in [A,B] to out/fc_counts_regen.txt -> check with
`grep -E '^p=(1[7-9]|[23][0-9]|40) ' out/fc_counts_b10.txt | diff - out/fc_counts_regen.txt` (must be silent when A=17, B=40).
Copy to the Studio: `src/ py/ studio/ out/db/ out/fc_counts_b10.txt` (about 40 MB); nothing else is needed.

## 1. Setup and self-test (about 2 minutes)
```
cd w5_exterior
studio/build.sh                                  # bin/bx1 (key<=63 bits), bin/bx (p<=32), bin/bx3 (p<=59), bin/fc_enum   (clang++ and g++ both tested)
studio/make_lists.sh 17 40                       # lists/fc_b10_p{p}_G{G}.txt, 5.6 M words in total, seconds
python3 py/known_check.py                        # 15 known streams must print True
bin/bx 10 -g 00001110001                         # must print ACCEPT states=18061 depth=59 ... e=00111010011@29      (p11)
bin/bx 10 -g 000100010001                        # must print ACCEPT states=45571 depth=71 ... e=101101010010@53     (p12)
bin/bx 10 -g 001010101001010101                  # default cap 40M: must print EXHAUSTED states=3800689 depth=57 (the p18 'SQ1' word; ~6 s)
DBDIR=/tmp/selftest studio/run_stage.sh st "25" 3000000 40 bin/bx 16     # p=25: 3428 words, 3426 EXHAUSTED, 2 CAPPED (cap 3M); 22 s CPU single-shard here, ~2 s on 16 shards
```

## 2. Job A — finish p = 25..32 (the residue ladder)
State at hand-over (final, after a PARTIAL 40M pass that reached p=30: measured CAPPED at 40M = p25:0 p26:0 p27:2 p28:3 p29:2 p30:9; not yet run at 40M: p31:12 (12M residue), p32:22 (12M residue + 5 never re-run); total 50 capped for p=25..32 + 4 with p<=24 = 54): the 3428/5181/7865/11939/18130/27641/42052/64249 F1 survivors of p=25..32 are all decided except the capped words in the
table below (EXTERIOR.md §4 lists the words; `python3 py/summarize.py 10 --files out/db/b10_p*.jsonl` regenerates the list).  Rung 1 has been run here for p=25..31 and 36 of 41 words of p=32.
Commands (smallest G first inside each p; ~1 min per word per 40M states):
```
# rung 1: cap 12M          (about 0.5 GB per process)
studio/run_stage.sh r1 "25 26 27 28 29 30 31 32" 12000000 300 bin/bx 16
# rung 2: cap 48M          (2.1 GB per process)
studio/run_stage.sh r2 "25 26 27 28 29 30 31 32" 48000000 900 bin/bx 16
# rung 3: cap 150M         (4.3 GB per process, 6.4 GB peak)
studio/run_stage.sh r3 "25 26 27 28 29 30 31 32" 150000000 3000 bin/bx 12
# anything still CAPPED after rung 3 is a genuinely hard near-critical word (see below): list it with
python3 py/summarize.py 10 --files out/db/b10_p2[5-9].jsonl out/db/b10_p3[0-2].jsonl | sed -n '/CAPPED/,$p'
```

Residue counts.  Measured: cap 3M (all of p=25..32) and cap 12M (run here, pass 3b; the 12M rung decided 59% of the 3M residue for p=25..31).
The later rungs are PREDICTIONS from the measured heavy tail N(>x) ~ x^-0.6 of the number of visited states (p=32: 1740 / 937 / 382 / 186 / 82 / 41 words need more than
1e4 / 3e4 / 1e5 / 3e5 / 1e6 / 3e6 states; ratio per factor 3: 0.54, 0.41, 0.49, 0.44, 0.50; same slope for p=28..31; the 3M->12M step predicted 0.435 x 67 = 29 of the 67 words of p=25..30, measured 27):

| p | F1 survivors | capped at 3M (measured) | capped at 12M (measured) | at 48M (pred.) | at 150M (pred.) |
|--:|--:|--:|--:|--:|--:|
| 25 | 3,428 | 2 | 2 | 0 (measured at 40M) | 0-1 |
| 26 | 5,181 | 3 | 2 | 1 | 0-1 |
| 27 | 7,865 | 8 | 6 | 3 | 1 |
| 28 | 11,939 | 12 | 4 | 2 | 1 |
| 29 | 18,130 | 13 | 2 | 1 | 0 |
| 30 | 27,641 | 29 | 11 | 5 | 2 |
| 31 | 42,052 | 29 | 12 | 5 | 3 |
| 32 | 64,249 | 41 | <=22 (36 of the 41 re-run: 17 capped, 5 not yet re-run) | ~10 | ~5 |
| total | | 137 | ~61 | ~27 | ~13 |

Words that sit in structural families (long (01)^m runs, (0001)^m blocks: (01)^12, (0001)^6, (01)^16 ...) are expected to stay capped at every rung ("supercritical" frontier).
Cost per visited state (measured here, shared 2-core box): 1.0-1.2 us at 12M states (p25-31; 12-17 s per word), 1.8 us at p=32 (22-30 s per word), 1.4-1.9 us at 40M states (57-75 s per word, 1 GB table).
Rung 2 (48M, ~61 words x ~90 s) ~1.5 core-h, rung 3 (150M, ~27 words x ~300 s) ~2.3 core-h: a few minutes of wall time on 16 processes plus stragglers.


## 3. Job B — re-decide p <= 24 (open words), same ladder
```
studio/run_stage.sh b0 "16" 300000000 6000 bin/bx1 1                      # (01)^8 with the 8-byte-key build: cap 300M = 4.3 GB (6.4 GB peak); 1 process
studio/run_stage.sh b1 "21 24" 150000000 3000 bin/bx 4                    # p21 word, p24 (0001)^6 and (01)^12: <= 3 words, cap 150M = 4.3 GB each
```
State at hand-over (cap 40M here): the ONLY open words with p <= 24 are p16 (01)^8 (quotient m=8, 40.0M states, reached depth 70), p21 001001010101001010101 (40.0M states, depth 82),
p24 (0001)^6 (m=6, 40.0M quotient states, depth 47; it contains the p12 stream doubled, so a complete run must also list ALL accepted e) and p24 (01)^12 (m=12, depth 16 at 40M).
Everything else with p <= 24 is decided: all F1 survivors of p = 17..20, 22, 23 and all but those four words of p = 16, 21, 24 (EXTERIOR.md §4).
Cost per word at 40M states: 50-60 s here (nice 10, shared 2-core box); the Studio is >= 2x faster per core.

## 4. Job C — extension beyond the current frontier: p = 33..40 with `bin/bx3`
F1 survivors (exact): p33 97,997; p34 149,930; p35 229,202; p36 351,150; p37 537,852; p38 824,965; p39 1,265,801; p40 1,943,815.
Measured mean time per survivor at cap 300k (uniform random sample of 300 words, this box): p33 6.9 ms, p34 12.9, p35 13.0, p36 19.3, p38 33.1, p40 47.5 ms
(p37, p39 interpolated 25 and 40 ms); capped fraction at 300k: 0.3-0.7%.  CPU hours (first pass): 0.2, 0.5, 0.8, 1.9, 3.7, 7.6, 14, 26  -> 55 core-hours,
i.e. ~3.5-4.5 h wall on 16 processes.
```
# first pass: cap 300k, 20 s per word                                          (do p33..p36 first: ~3.4 core-hours ~ 15 min wall)
studio/run_stage.sh c1 "33 34 35 36" 300000 20 bin/bx3 16
studio/run_stage.sh c1 "37 38 39 40" 300000 20 bin/bx3 16                       # ~50 core-hours ~ 3.5 h wall
# residue: cap 3M (0.2 GB), then 12M, 48M exactly as in Job A (replace bin/bx by bin/bx3, rung 3 limited to cap 80M)
studio/run_stage.sh c2 "33 34 35 36 37 38 39 40" 3000000 60 bin/bx3 16
studio/run_stage.sh c3 "33 34 35 36 37 38 39 40" 12000000 300 bin/bx3 16
```
Expected residue after the 300k pass: ~0.5% of the words (p36: ~1.7k, p40: ~10k); after cap 3M about 25-40% of those remain (p30-32: 300k->3M cut 74->29, 116->29, 185->41), after 12M about 40% of THOSE (measured 3M->12M: 59% decided).
bx3 handles p<=59 and G*ydig+2p <= 191 bits; for p>=41 regenerate lists with `studio/make_lists.sh 41 44` (p44: ~1.6e7 words: only do G<=? by `-Gmin/-Gmax` if needed).

## 5. Protocol if a NEW stream appears
`run_stage.sh` prints `NEW` lines from `py/check_accepts.py` (any accepted (g,e) whose cyclic primitive root is not the p11 stream (g=00001110001,e=00111010011)
or the p12 stream (g=000100010001,e=101101010010)). Then, on that word only:
1. `python3 py/verify_ext.py 10 <g> <e>` — mirror `Bstep` replay + real-integer replay (needs the p196 `neutral_band_search.py`; edit its path at the top if the folder moved).
2. Save the witness JSON (`bin/bx 10 -g <g> -w` prints `WIT g=... B_t=...`), replay with the mirror `cycleOK` for >= 3 cycles with a large gap.
3. Immediately start the centre search (cauto_fast / cauto_fast64 for k=1,2; CP-SAT padded; widths 7..160) and STOP the other jobs; report at once.

## 6. Bookkeeping
* Per-stage logs: `logs/studio_<stage>_p<p>_s<i>.log` (non-exhausted words only); shard DBs `out/studio/<stage>_p<p>_s<i>.jsonl`; merged DB per p `out/db/b10_p<p>.jsonl`.
* Funnel table at any time: `python3 py/summarize.py 10 --g --files out/db/b10_p*.jsonl`.
* Keep `out/db/` (small for p<=32: ~25 MB; p=40 alone ~400 MB as JSON lines; gzip when done).
