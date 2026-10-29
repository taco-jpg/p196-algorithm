# Agent N13: bipolar decimal lattice pulse, collision with centre-origin wall

**Label: COMPUTED.** Scope: three concrete ordinary decimal reverse-and-add orbits, steps 0..6000, with independently replayed steps 0..800. No infinite decimal Lychrel theorem, universal pulse law, or Lean proof.

## Construction

Use the first reachable decimal period-8, spatial-period-20 lattice from `calculation/decimal_frontier/lattice_formats/p8_scc.txt`. The self-contained test code hardcodes its root path of 39 pair coefficients and its period-20 bulk. Every lower-half pair coefficient q lifts to valid actual decimal digits `(min(q,9),q-min(q,9))` on reflected least-significant/most-significant sides; thus the underlying decimal integers are fully defined and reproducible without the external SCC file.

- `A`: unmodified initial halfwidth H=5200, length 10400 decimal digits.
- `B`: same H, but change the lower-half pair coefficients at j=2000..2099 to `(7*j+11)%19`, with matching reflected coefficients. Exterior and centre initially remain identical to A; only a finite **interior pulse** differs.
- `C`: independent unmodified clean-control seed with halfwidth H=12000, length 24000 digits. It carries the same root periodic exterior but pushes its centre much farther away, allowing the centre-origin disturbance of A to be located without assuming an infinite ideal lattice.

Evolve A, B and C via the literal integer operation `T(N)=N+reverse(N)` in base 10 (independent full C++ digit arrays; Python standard arbitrary-precision integers for independent control). For a time t let `L(t)` and `R(t)` be respectively the least and greatest lower-half paired-coefficient indices where A and B disagree; let `Cfront(t)` be the first paired-coefficient index at which A differs from the far-centre control C, or -1 if there is no such difference in the compared overlap. Each timestep also counts the total differing paired indices and verifies the two shorter orbits retain equal lengths.

## Three independently observed ballistic interfaces

At all indicated integer start times, direct 22-step comparisons of the exact **actual** decimal orbits give:

| Front | Translation and direction | Exact start-time range | Comparisons |
| --- | --- | --- | ---: |
| `L` (pulse outer edge) | `L(t+22)=L(t)-5`, outward | t=18..5978 | 5961 |
| `R` (pulse inner edge) | `R(t+22)=R(t)+15`, inward | t=10..3405 | 3396 |
| `Cfront` (centre-origin outer wall) | `Cfront(t+22)=Cfront(t)-5`, outward | t=52..5978 | 5927 |

The two pulse edges initially enclose about 100 paired positions. Before interaction, their measured relative separation grows by **20 cells per 22 steps**. This is not the same as the central patch experiment `AgentN13DecimalShearedFront22`: here an actual finite pulse has two tracked boundary interfaces, one moving inward faster than the nominal growth of the digit-string centre, the other outward. The clean reference C locates a **third** front that comes from the original finite seed's central mirror-gluing defect, despite initially sharing A's same rooted exterior.

At step t=3400 the pulse inner edge `R=4416`, centre wall `Cfront=4439`, gap 23. By t=3425, `R=4433`, `Cfront=4434`, gap 1. At step **3426**, `R=4434` and `Cfront=4433`: their order crosses, the first such recorded crossing. From a 22-phase inner-edge extrapolation anchored at t=3300, **the first actual deviation occurs at t=3428** (observed R=4437 vs predicted R=4435). The discrepancy begins exactly as the two fronts have collided. This gives a concrete mechanism for why one separately stable moving local wall cannot be blindly extended across the nonperiodic centre wave.

The experiment is constructive data for a three-interface format: an outward pulse front, an inward pulse front, and a centre-sourced disturbance. It indicates that a prospective infinite certificate must manage **interface interactions** and not merely preserve one glider's isolated velocity. It does not prove that all possible interactions are destructive; a recombination/replenishing junction remains a plausible new construction target.

## Replay and independent checks

`pulse_collision.cpp` generates all three decimal seeds independently, evolves them through t=6000 by a straightforward decimal digit-array carry loop, and writes a full dense table (`time, min, max, count, center_front, length`). It checks equal length of A and B at every step. `pulse_check.py` verifies every step of all three exact 22-step laws on their specified intervals, determines the first crossing at t=3426 and first post-collision divergence at t=3428, checks no missing front, and validates 18 committed keyframes (`pulse_keyframes.csv`). `pulse_independent.py` does **not** call either C++ function: it reconstructs A/B/C as native Python integers and applies `n += int(str(n)[::-1])`. It compares all six table fields at **every step 0..800** against the C++ data: 801 complete independent three-orbit controls, no mismatches.

One command from any repository root:

```sh
bash calculation/new_structures/agent-N13/pulse_run.sh
```

On success this prints `AGENT_N13_BIPOLAR_PULSE_COLLISION_PASS`. The source, independent checker, full data generator and exact keyframes are all committed in the same result; no internet access or precomputed hidden files are necessary. The uncommitted full dense table is regenerated, not assumed. Python 3.11+ and a C++17 compiler are required.

## Limitations and next constructive direction

This is finite dynamics: the observed speeds are not global all-time laws. The right-front 15/22 pattern is disrupted by its encounter with the centre-origin outward wall; the left front continues its own 5/22 pattern for the tested horizon. Neither this result nor the previous carry tile gives a regenerative, repeating collision rule. A next positive construction would search for junction pairwords whose interacting fronts **re-emit the same external carry-gate word**, producing a phase-locked, self-sustaining source rather than a travelling pulse that inevitably hits the centre. No exclusion result is inferred.
