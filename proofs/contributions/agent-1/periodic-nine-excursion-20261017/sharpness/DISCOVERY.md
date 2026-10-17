# Local seven-column drop: bounded discovery

Agent #1 specialist `/root/suffix_receipt_resume` executed `discovery.py` under accepted initial nine-excursion claim `4a96b34d8991f7cb13484e6dc25548ea7870f271`. Baseline: `fa8cf9024c8aaa8c97a6426b004a7869c12ed887`. Source pins, exact command, exit, timestamps, and output are retained in `discovery-001.json`, `discovery-001-command.json`, and `discovery-001.console.log`. This is ordinary exact-integer computational evidence; no Lean proof or universal impossibility is claimed.

The fixed family contains 2,774 distinct symmetric centers and nine outer words, for **24,966 cases**. Centers are `9^p ++ core ++ 9^p`, `p=0..4`, with core `[a,a]`, `[a,b,b,a]`, or `[a,c,a]`, `a,b=0..18` and even `c=0..18`. Outer words are `[1]`, `[9]`, `[10]`, `[18]`, `[10,0]`, `[18,0]`, `[10,8]`, `[18,8]`, `[9,0]`. The maximum center length is 12 and outer length is 2. Hard budgets were 30,000 cases and 30 seconds, plus a 35-second wrapper timeout. All planned cases completed; recorded script time was `0.3004340109982877` seconds, wrapper time `0.3319198099998175` seconds, exit 0.

Each case uses the preserved algorithm's actual `full`, `image`, and `valid` functions, loaded from the pinned source without running its search routine. The script computes the exact raw slices, maximal strips, actual carry scans, and one further actual raw period. It separately checks the known mixed-nine center formula. Source validity is asserted, including coefficient bounds, symmetry, odd-center parity, and positive outside coefficient. No clock or carry bit is chosen independently.

No case satisfied all requested predicates. Of 7,665 cases with initial literal center normalization, actual mixed entries, and actual clock one, **zero** had additional center stripping. There were 32 normalized mixed-entry cases with additional stripping when clock one was not required. These counts are bounded-family results, not general theorems.

Removing only the initial-normalization predicate produced 2,023 controls satisfying the other requirements. The first stored control is:

```
B = [10]
H = [9,9,9,9,0,9,9,9,9]
w = [9,9,9,9]
leftEntry = 1; rightEntry = 0; rawGamma = 1
centerPeriods = 2
quotientOuter = [1,0,9,9,9]
quotientCenter = [10,10]
next rawPeriod = [9,9,9,9]
```

Its center length drops from 9 to 2. Initial normalization is false. This remains a computational control, not a compiled Lean statement. No original-domain sharpness witness was found and no cycle was sought.

The exact proposed strengthening sent to root is:

```
hv    : ValidPeriodic B H [9,9,9,9]
hnorm : stripPeriodCenter [9,9,9,9] H = (H,0)
hmix  : leftEntry B + rightEntry B H [9,9,9,9] = 1
hg    : rawGamma B H [9,9,9,9] = 1
------------------------------------------------
centerPeriods B H [9,9,9,9] = 1
```

The proposed statement needs no future-nine or nonempty-output premise. It is **unproved at this discovery checkpoint**. The source-derived motivation is that the clock-one pad shifts the pairing by one position; a complete nine boundary in that paired residual may force four original nine coefficients at each end of the symmetric input center, contradicting literal initial normalization. Root authorized this narrow obstruction as a potential source task, pending publication of the precise claim refinement before substantive proof work.

The required actual issue check-in was accepted at [6228609594](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6228609594) and fetched back with an identical body. The exact initial claim API response and issue read are preserved. No other agent acknowledgment, proof, public theorem, or Git publication is inferred from that delivery.
