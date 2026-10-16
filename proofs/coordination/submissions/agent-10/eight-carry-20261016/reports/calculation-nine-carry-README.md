# Agent #10: finite carry searches and the eight-word witness

This directory preserves completed computational discovery evidence for the exact nine-word reconstruction result. The original source, input, output, control, command, and log files are copied byte for byte. Compiled executables, Python bytecode, and Lean objects are excluded. The shared `actual_simulator.inc` source is included beside both full-word enumerators.

## Scope and sizes

The K4 and K5 prefix searches enumerate coefficient pairs in `0..18`, with a common positive outer coefficient. At each observation they require every low carry at indices `1..K`, every reflected high carry at `L,L-1,...,L-K+1`, and one shared Boolean input carry at `L-K`. Here `L` is the current width. Terminal overflow determines the next prefix. The missing inner region is not required to evolve coherently, and the **K4/K5 necessary-projection inclusions are not formalized in Lean**.

| Preserved experiment | Initial difference or family | Complete size |
|---|---|---:|
| `four-prefix-check-002` | `(0,0,1,-3)`; `18×19×18×16` starts | 98,496 |
| `five-prefix-check-001` | `(0,0,0,1,-3)`; `18×19²×18×16` starts | 1,871,424 |
| `twice-padded-width15-001` | Width-15 symmetric, center-even completions of all 120 K4 survivors | 1,987,440 |
| `thrice-padded-width17-001` | Width-17 symmetric, center-even completions of all 1,326 K5 survivors | 21,961,212 |

The width-15 difference is `[0,0,1,-3,5,-6,6,-6,6,-6,5,-3,1,0,0]`. The width-17 difference is `[0,0,0,1,-3,5,-6,6,-6,6,-6,5,-3,1,0,0,0]`. Each retained prefix has `14×13×13×7 = 16,562` completions. Before filtering, these prescribed families contain **1,631,290,752** and **30,994,524,288** pairs, respectively. Swapping the two words covers the negative difference.

The full-word scans enumerate every filtered completion and compare actual complete carry words under continued reverse-and-add. **CSV sample bit strings never constrain actual trajectories.** A whole-family exclusion from a filtered scan additionally uses the computational projection and filter completeness.

## Exact survivor counts

Row zero gives the enumerated domain before any carry observation, after applying the prefix filter where relevant.

| Observations | K4 initial prefixes | K5 initial prefixes | Actual width-15 completions | Actual width-17 completions |
|---:|---:|---:|---:|---:|
| 0 | 98,496 | 1,871,424 | 1,987,440 | 21,961,212 |
| 1 | 73,530 | 1,397,070 | 172,200 | 1,864,832 |
| 2 | 43,919 | 835,407 | 62,784 | 696,818 |
| 3 | 23,096 | 436,263 | 49,776 | 515,311 |
| 4 | 13,059 | 246,682 | 27,370 | 282,685 |
| 5 | 6,001 | 110,986 | 15,024 | 156,113 |
| 6 | 2,621 | 48,146 | 4,910 | 41,090 |
| 7 | 739 | 12,549 | 126 | 1,094 |
| 8 | **120** | **1,326** | **0** | **32** |

The K4 compatible shared-bit path counts for lengths 1 through 8 are `[141246,143311,129588,98993,100588,83365,27871,2744]`; K5 counts are `[2683674,2726444,2438133,1877801,1864316,1554292,573798,33498]`. Both control modes reproduce the earlier K3 counts `[3870,2346,1246,692,334,134,37,0]`; K5 also reproduces K4 counts. Every one of the 32 full width-17 matches has overflow pattern `OOONNNON`.

## Positive eight-word witness

The first width-17 match is independently realized by ordinary integers

`n = 90000000560706169`, `m = 90000000806235169`.

Their complete carries match at times `0..7`. Initial pair coefficient three is `6` versus `5`, and their next integers are `186160707060706178` versus `186153261606235178`. The first carry separation is at time **8**, index **4**, with values **1 versus 0**. The exact arrays, digits, ordinary orbits, and carry traces are in `thrice-padded-width17-001/first_eight_integer_replay.json`.

The positive witness does **not** depend on prefix-filter soundness or search completeness. Its direct kernel certificate is [Agent10EightCarryCounterexample.lean](../../proofs/Agent10EightCarryCounterexample.lean); the exact uniform threshold is composed in [Agent10NineCarrySharp.lean](../../proofs/Agent10NineCarrySharp.lean).

Both witness inputs first reach palindromes at time **4**, namely `16999899899899899961` and `16989989999998998961`. These facts are also kernel checked. The domain is unrestricted continued iteration, including steps after a palindrome; this evidence asserts no palindrome avoidance and no resolution of the 196 problem.

## Preservation and replay

Historical receipts and runner scripts retain their original workspace paths and executable hashes. Excluded executables can be rebuilt from the included sources; preserved receipts are not rewritten to reflect this delivery. Run fresh outputs in a separate directory so retained evidence stays unchanged. For example, from the repository root:

```sh
AGENT10_REPLAY_DIR="$(mktemp -d)"
g++ -std=c++17 -O3 -Wall -Wextra -Werror \
  calculation/agent10-nine-carry-sharp-20261016/thrice-padded-width17-001/thrice_padded_witness_scan.cpp \
  -o "$AGENT10_REPLAY_DIR/scan"
"$AGENT10_REPLAY_DIR/scan" \
  calculation/agent10-nine-carry-sharp-20261016/thrice-padded-width17-001/survivors-5.csv \
  "$AGENT10_REPLAY_DIR/first.json" > "$AGENT10_REPLAY_DIR/result.json"
python3 calculation/agent10-nine-carry-sharp-20261016/thrice-padded-width17-001/replay_ordinary_integers.py \
  "$AGENT10_REPLAY_DIR/first.json" 8 > "$AGENT10_REPLAY_DIR/integer-replay.json"
```

`FILES.json` records repository-relative target paths, SHA-256 hashes, and sizes for this README and all 80 byte-preserved original files. It excludes itself to avoid self-reference; its own hash is supplied in the delivery handoff.
