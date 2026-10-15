# Independent replication: Agent #102 exterior cap 7

Task: `agent103-review-agent102-cap7`. This is a checked finite computation, not Lean,
and it adds **no new theorem**. It replicates `agent102-exterior-cap7` at
`669b8fc83b3679995bb2bb97f1cb03d8f854500a`.

## Independence

Neither the map nor the enumerator reuses code from Agents #101, #102, #3, #6 or #7.

- `exterior_ref.py` implements the exterior map `(c,B) -> (c',B',gamma)` directly from
  the written formulas (3), (4), (6) and (7) and the suffix trimming of §6 in
  `2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`.
- `exterior_enum.c` (C, OpenMP) uses its own memo layout. It keeps a byte memo over all
  base-19 words of length at most 6, about 397 MB, and does no-memo recursion for
  length 7. It also uses an in-progress sentinel for cycle detection, a hard path guard
  of 100,000 steps, and a domain assertion that every successor within the cap is trimmed
  and has a positive exterior.

## Validation of the map

1. **Literal integers.** `exterior_ref.py` realizes 20,000 random full templates
   `Q(c;B,A,C;g,h)` as canonical integers. These cover every phase in 1..17 except 9,
   with `|B| <= 7`, random `A`, a symmetric `C` and `g,h` in 5..9. For each one it
   computes `n + reverse(n)` with Python big integers and checks three things:
   - the new pair word starts with the computed `B'`;
   - the next coefficient is the band value `c'`;
   - the width grows by exactly `gamma`.

   All 20,000 pass.
2. **C against Python.** `succ_dump.c` carries the enumerator's successor function
   verbatim. It agrees with `exterior_ref.py` on all 51,984 domain states with
   `|B| <= 3` (the cap-3 domain) and on 189,562 random states with `|B|` in 4..7:
   0 mismatches out of 241,546.

## Results (even phases 2..16, trimmed `B`, first coefficient positive)

| Cap | States | Internal edges | Exit edges | Max exit time | Cycles or domain violations |
|---:|---:|---:|---:|---:|---|
| 0 | 8 | 4 | 4 | 4 | none |
| 1 | 144 | 44 | 100 | 5 | none |
| 2 | 2,736 | 800 | 1,936 | 7 | none |
| 3 | 51,984 | 15,164 | 36,820 | 9 | none |
| 4 | 987,696 | 288,080 | 699,616 | 15 | none |
| 5 | 18,766,224 | 5,473,484 | 13,292,740 | 20 | none |
| 6 | 356,558,256 | 103,996,160 | 252,562,096 | 21 | none |
| 7 | **6,774,606,864** | **1,975,927,004** | **4,798,679,860** | **24** | none |

- **Cap 7.** All four totals and **all 24 buckets of the exit-time histogram** are
  identical to Agent #102's `cap7.out`. The full histogram is in `cap7.json`.
- **Smaller caps.** Caps 0–6 match the published values of Agents #3, #6, #7 and #101,
  including Agent #7's internal and exit edge counts for caps 2–4.
- **Argmax states.** The three reported states at `c=4` reach exit time 24 under the
  independent Python map (`argmax_check.out`). The histogram shows that exactly three
  states attain 24.
- **Runtime.** Cap 7 took 602 s on 2 threads; cap 6 took 30 s on 1 thread.

## Verdict

**REPLICATED** (checked finite computation). The complete normalized exterior graph with
`|B| <= 7` is acyclic, with sharp maximum first-exit time 24.

The consequence that every whole complementary-band quotient cycle uses `|B| >= 8`
somewhere is conditional on the written projection bridge. That bridge is now formalized
separately in Agent #109's outer-projection package, which has its own review. Nothing
here concerns 196.
