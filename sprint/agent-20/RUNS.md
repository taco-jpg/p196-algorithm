# Run notes (sprint agent 20), measured 2026-10-22

Machine: cloud sandbox, 2-core x86_64 Linux, 8 GB RAM, Python 3.13, cc -O3, Lean 4.19.0.
Repository at `main` c6902ac; batch branch `prefix-k45-certificates` a441ded checked out locally
(not committed here).

## Static audit — `extract_entries.py`

```
entries extracted: 2494  distinct prefixes: 2494  by length: {4: 2494}
  P196.Agent117P2641.A124117P2641K7Initial  k=7: 1
  P196.Agent124FourDigit.A124F4Entries  k=4: 1267
  P196.Agent124FourDigit.A124F5Entries  k=5: 463
  P196.PrefixK45.NewK4Final  k=4: 757
  P196.PrefixK45.NewK5Final  k=5: 6
leading-zero or digit>9 prefixes (vacuous): 0
noOverflowPre fails (entryOK would reject): 0
bound+1 > 100: 0
lists without a no_196 consumer in the same namespace: []
entries with no entryOK width found: 0
prefixes listed more than once: 0
bound histogram: {0: 314, 1: 360, 2: 547, 3: 344, 4: 120, 5: 170, 6: 98, 7: 122, 8: 115, 9: 73, 10: 28, 11: 97, 12: 8, 13: 27, 14: 7, 15: 10, 16: 4, 17: 4, 18: 2, 19: 4, 20: 4, 22: 2, 23: 2, 24: 6, 28: 12, 30: 2, 31: 2, 32: 6, 33: 1, 39: 1, 42: 1, 47: 1}
```

Coverage recount (RESULTS.md table + entry lists): 4,941 four-digit prefixes covered on `main`,
5,704 with the k45 branch; 396 three-digit prefixes fully covered with the k45 branch.
74 of the 1,731 `main` four-digit entries have an "x" parent; none of the 763 k45 entries does.

## Independent recomputation

```
[k=4] model validated on 120000 actual reverse-and-add steps
[k=4] 123462 long states, 207 short words, 110002 targets indexed in 0.9s
[k=4] 40 entries: equal 40 ...                       (first, sampled run on PrefixK45 only)
[k=4] 2024 entries: equal 2024, claimed>recomputed 0, recomputed>claimed 0, cycle 0
[k=5] model validated on 30000 actual reverse-and-add steps
[k=5] 2345778 long states, 549 short words, 2025749 targets indexed in 16.0s
[k=5] 469 entries: equal 469, claimed>recomputed 0, recomputed>claimed 0, cycle 0
      wall 17.0s maxrss 632 MB
[k=3] lazy inverse equals forward index on 6001 targets; no spurious predecessors on the other long states
[k=4] lazy inverse equals forward index on 110002 targets; no spurious predecessors on the other long states
2641 k=7 initial=1000 recomputed=5 claimed=5 states=25624 time=1.7s
```

Three-digit endpoints (`three_digit.py 5`, then `three_digit_k.py`):

```
620 claimed t<= 12 ranks k=3..5: [inf, 13, 11] best t<= 12 ok
119 8 | 213 23 | 216 10 | 257 16 | 348 16 | 384 7 | 426 24 | 429 24 | 474 7 | 674 5 | 737 12 |
755 12 | 778 25 | 783 14 | 784 14 | 787 25 | 788 14 | 789 38 | 858 36 | 859 36 | 905 11 |
906 11 | 923 7 | 935 10      -> rank+1 at k=5 equals the claimed bound (24 classes)
k=6: 276 31 | 277 31 | 278 31 | 377 8 | 385 8 | 785 40 | 786 27 | 856 38 | 857 25   -> all equal
k=6 (not yet equal): 217 28>23 | 218 36>34 | 777 27>25 | 739 inf
k=7: 217 rank=22 t<=23 | 218 rank=33 t<=34 | 777 rank=24 t<=25 | 739 rank=38 t<=39   -> all equal
```

## Forward scans — `fwdscan.c` + `compare_fwd.py`

```
./fwdscan 1 10000000 300          real 23m35.077s  user 18m58.079s   (7591 prefix lines)
./fwdscan -s 300 < rand_seeds.txt real  3m58.221s  user  3m51.893s   (2,000,000 seeds, Random(2020))

seeds < 10^7:   claimed 2545; observed 1742; VIOLATIONS 0; attained exactly 593;
                largest certified four-digit delay (12, '6241', '1709090')
random 2e6:     claimed 2545; observed 2348; VIOLATIONS 0; attained exactly 637;
                largest certified four-digit delay (20, '2973', '405784242604')
all combined:   claimed 2545; observed 2491; VIOLATIONS 0; attained exactly 968
histogram of (bound - max observed t), combined:
 {0: 968, 1: 559, 2: 435, 3: 183, 4: 90, 5: 39, 6: 66, 7: 34, 8: 21, 9: 15, 10: 12, 11: 14, 12: 6,
  13: 9, 14: 1, 15: 5, 16: 3, 17: 3, 18: 1, 19: 3, 21: 6, 22: 2, 23: 4, 24: 2, 25: 1, 27: 5, 30: 2,
  34: 1, 43: 1}
```

Delay > 100 (seed, steps): 1222 (4802083327646, 103) · 1332 (623031087358, 102) · 1354
(525853994724, 102) · 1365 (16364749691, 113) · 1443 (18788256210, 101) · 1469 (80523117705, 107) ·
1485 (2495407672183, 109) · 1573 (894868733627, 103) · 1599 (7087743853354, 109) · 2212
(3453984598754, 116) · 2344 (340023930894, 108) · 3599 (21217819763, 101) · 3674 (998117314580, 102)
· 3878 (2960671726311, 102) · 4456 (1186060307891929990, 261) · 4479 (284829704, 116) · 4618
(114560080449, 121) · 4862 (125224832174, 103) · 5554 (1702190, 101) · 5831 (1469644083, 105) · 6633
(1026588326, 109) · 6634 (13968441660506503386020, 289) · 6842 (65687233278, 105) · 8938
(588518634474, 106). The three-digit parents use the same witnesses (663 uses the 289-step one).

## Lean

```
PrefixFidelity    wall 4.0s   maxrss 520 MB    (lake env lean, deps prebuilt)
Controls          wall 9.1s   maxrss 1117 MB
DelayWitnesses    wall 23.8s  maxrss 2904 MB
TextbookPrefixes  wall 5.8s   maxrss 742 MB
lake build of the four modules (LEAN_NUM_THREADS=1): wall 37.9s, maxrss 2906 MB, "Build completed successfully."
```

lean4checker v4.19.0 (`lake env lean4checker <module>`, one module at a time) over the import closure
of `Agent124PrefixL`, `Agent124CodeCert`, `PrefixK45.NewK4Final`, `PrefixK45.NewK5Final`,
`A124F4Final`, `A124F5Final`, `A124117P2641K7Final`, `CertificateToLychrel.AdmissibleHeads` and the
four sprint modules (231 modules, including `Foundations.LychrelDigitSums` with the 100-step check):

```
lean4checker: 141 modules OK, 0 failed     real 18m12.002s
lean4checker: 90 modules OK, 0 failed      real  9m31.464s
```

Reproducer: `lake env lean ../sprint/agent-20/repro/SkipKernelTC.lean` prints
`'RedTeam.boom' does not depend on any axioms`; lean4checker on its compiled .olean:
`lean4checker found a problem in RedTeamRepro.SkipKernelTC` / `(kernel) declaration type mismatch,
'RedTeam.bad' has type True but it is expected to have type False` (exit 1).
