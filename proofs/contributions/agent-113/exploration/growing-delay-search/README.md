# Exploration: spacer families with growing first-palindrome time (negative, finite scope)

Agent #113, 15 October 2026. **Exploratory computation only; no theorem.**

Motivation: the repository proves `FiniteDelayBound D → IsLychrel C_D`
(`DecimalDelayBridge`), and records that unbounded finite first-palindrome
delay is not proved. An explicit family of terminating seeds whose first
positive palindrome time grows without bound would refute every
`FiniteDelayBound D`. This search looked for the simplest candidate shape.

Search (`search.cpp`, digit-vector reverse-and-add, exact): seeds
`A · B^r · C` (decimal concatenation; `A` without leading zero, `B` one digit,
`C` any digit string), first positive palindrome time with a cap of 400 steps,
evaluated at `r = 4, 8, 12, 16, 20, 24, 32`. A family is reported if every
tested `r` terminates within the cap, the times strictly increase in `r`, and
the time at `r = 24` exceeds the time at `r = 4` by at least 8.

| run | `|A|`, `|C|` | patterns | reported |
|---|---|---:|---:|
| `./search 2 2 400` | ≤ 2, ≤ 2 | 108,900 | 0 |
| `./search 3 3 400` | ≤ 3, ≤ 3 | 11,088,900 | 0 |

Interpretation (heuristic, not proved): carries cross a spacer of equal digits
within a single step whenever the spacer pair sums are 9 (or stay inert when
they are 0), so these shapes give no column-by-column moving signal whose
travel time scales with `r`. Other shapes (two spacers, nested repetition,
growing cores) are untested. A missing result is not an exclusion.

Reproduce: `g++ -O2 -o search search.cpp && ./search 3 3 400 > grow33.out`
(about 10 minutes on one core).
