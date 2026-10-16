# Checked finite interval-count checkpoint

Status: **LEAN_CHECKED; independent review 和 integration pending**.

The full fresh build began at `2026-10-16T21:18:28.918201+00:00` 和 finished at `2026-10-16T21:20:20.072928+00:00`.

Compiler:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

All nine unchanged local dependencies, both new proof modules, 和 the final audit module compiled from source into an initially absent build directory. No `.olean` files were copied into the build. All compiler commands exited zero. The exact types of the generic, ordinary-decimal, 和 196 endpoints were printed.

All seven new theorem declarations have literal transitive axiom reports. The generic theorem family uses only `propext` 和 `Quot.sound`; the numeric corollaries additionally use `Classical.choice` through the existing arithmetic dependency. No other axiom appears in any of these reports.

| Source | SHA-256 |
|---|---|
| `Agent9WindowIntervalCounts.lean` | `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9` |
| `Agent9DigitSumIntervalCounts.lean` | `0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4` |
| `Agent9IntervalCountsAudit.lean` | `37b98536e7ae0ea520ce20df9ad47a42727625710c72e132180d14b818f011cd` |

The exact completed record is `development/full-001/summary.json`. Full stdout/stderr for every command 和 frozen copies of all new Lean sources accompany it. The earlier successful generic-only build is retained under `development/generic-001/`; its first execution attempt encountered an absent scratch cwd before any compiler was launched, recorded in `development/generic-000-launch-failure.json`.

The theorem counts actual times in `[s,s+N)` whose ordinary-decimal digit sum exceeds `B`, with denominator `sharpDigitSumEscapeBound B+1`. Every natural `B,s,N`, including zero, is retained. The only numeric input hypothesis is `0<n`.

The result is a finite count, not a proof of a real density limit, pointwise digit-sum divergence, palindrome avoidance, a fixed all-time safe seed, or the 196 conjecture. Iteration retains the original behavior through palindromes. Seven audited declarations are source-audit metadata, not seven independent major results or a measure of progress toward P196.

The delegated proof author has made no Git or remote writes. The parent is the publication writer 和 independent reviewer.
