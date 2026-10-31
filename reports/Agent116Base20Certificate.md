# Agent 116 — T7: explicit base-20 neutral certificate

## Result and scope

**LEAN-VERIFIED:** An independently reconstructed eight-edge cycle is accepted by the unchanged
`Agent120.Neutral.cycleOK 20`. Its checked soundness theorem gives a base-20
Lychrel number, with an explicit 216-digit seed, and every neutral-template gap
at least four. The new Lean module compiled, passed kernel replay, and passed
the actual repository gate with all six endpoints audited.

This supplies an explicit base-20 control for the neutral-band route.
[REPORT_203](REPORT_203.md) and [REPORT_213](REPORT_213.md) document the earlier
source gap: Seal's announced base-20 digits were omitted. This reconstruction
does **not** identify the present seed with his historical seed or claim novelty
of base-20 existence. It establishes no base-10 certificate, no decimal Lychrel
number, and no impossibility of the general decimal route.

The additional transfer result is **PAPER PROOF** for the displayed boundary
carry itinerary, corroborated by independent arithmetic. Its full-center
strengthening is **COMPUTED exact rational elimination**, not a Lean theorem.

## Complete certificate and explicit seed

All coefficients are least significant first. Complete data are supplied twice:

- `calculation/agent-116/cert20.json`: all `(B,C,B2,C2,u,v)` edges.
- `lean/P196/Agent116Base20Certificate/Certificate.lean`: eight named exterior
  words, eight named centers, the literal edge list, and six theorem endpoints.

The stored certificate uses this phase order:

| Phase | B width | C width | e | g | u | v |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 91 | 26 | 0 | 0 | 1 | 0 |
| 1 | 90 | 26 | 1 | 0 | 0 | 0 |
| 2 | 90 | 26 | 0 | 0 | 0 | 0 |
| 3 | 90 | 26 | 0 | 1 | 0 | 0 |
| 4 | 91 | 27 | 1 | 0 | 1 | 0 |
| 5 | 90 | 27 | 0 | 0 | 0 | 0 |
| 6 | 90 | 27 | 1 | 0 | 0 | 1 |
| 7 | 90 | 25 | 1 | 1 | 0 | 0 |

Thus `e=01001011`, `g=00010001`, `u=10001000`, `v=00000010`;
`sumGam=2`, `sumGain=3`, `sum(u)=2`, `sum(v)=1`.
After eight ordinary reverse-add steps the same coefficient blocks return,
with each neutral gap increased by one. The generic soundness condition is
`gap >= 2 + sumGam`, hence every initial gap at least four works.

The seed is `val 20 (tmpl 20 exterior20_0 center20_0 4)`.
In ordinary most-significant-first base-20 notation (`A=10` through `J=19`):

```text
300DA5G78ECGEDCDB57C57C0GBHAH7GH3C881DCFF7F4H0A4GA41036BC8H97CHI438F12A3620DGBHHBD3C8FE22BA00009769E2DICGGD44DGGBHE2DA778JJJJ9B22EF8D4DAGICFD1263A21F833HHC79I9CB63014AG3A0G4G8FFCD078D3GH7GAHBH0B75C75BDCDEGCF96G59E0J2
```

The infinite statement follows from `lychrel_of_cycle`, not from the finite
orbit replay. This is base-20 digit reversal throughout.

## Reconstructing the witness

From repository root, with Python 3 and a C++17 compiler:

```bash
python3 calculation/agent-116/base20_search.py --reconstruct --output /tmp/agent116-cert20-reconstructed.json
```

Output:

```text
{"status":"MIRROR_ACCEPTED","base":20,"period":8,"overflow":2,"exterior_trim":2,"center_trim":1,"max_B":91,"max_C":27}
```

The script compiles the existing exact `bauto.cpp` and `cauto_fast.cpp` in a
temporary directory. It uses these constructive source queries:

```bash
bauto 20 8 8 -g 10001000 -w -cap 1000000
cauto_fast 20 10100101 10001000 27 27 -v 00100000 -w -cap 3000000
```

The source exterior stream is `e=10100101`, `g=10001000`.
The script supplies the recovered B/C pair to the exact Python mirror,
extracts its canonical closed cycle, and rechecks `cycleOK`. This explains
the different rotation in the stored certificate. The reconstructed JSON
matches the checked-in fixture exactly.

Discovery detail: the all-length mode returned `NOPERIOD` for this source
stream, whereas the direct range `1 180` found its first witness at center
width 27 and 154 feasible initial widths through 180. `NOPERIOD` is therefore
an undecided periodicity computation, even on this positive driver.
The short reproducer queries only the known successful width.

The supporting search wrapper distinguishes actual empty-frontier exhaustion
from depth/state/time limits. It preserves feasibility without extracted arrays
as `FEASIBLE_NO_WITNESS`. No completed base-20 period census or shortest-seed
claim is made here. Agent107's separate completion audit retains its scope.

## Independent arithmetic replay — COMPUTED

```bash
python3 calculation/agent-116/base20_replay.py --selftest --certificate calculation/agent-116/cert20.json --orbit-steps 1000
```

This verifier evaluates entire coefficient words as integers, obtains digits
and carries by division by powers of the base, reconstructs successors, checks
literal trims and closure, then separately calls the mirror. It also checks
ordinary reverse-add against the predicted template at every phase.

| Check | Exact result |
|---|---|
| Eight existing source-certificate controls | 56 edges, 168 independent integer-step checks |
| New certificate | 8 edges, 24 integer-step checks at gaps 2, 3, 5 |
| Mirror acceptance | `True` |
| Ordinary reverse-add iterations | 1,000 |
| Exact phase/template matches | 1,001 |
| Palindromes in that finite orbit | 0 |
| Initial/final gap | 4 / 129 |
| Initial/final base-20 digit count | 216 / 466 |

The separate `base20_projection.py` contains an independent necessary head
projection and uncompressed tuple-state exterior transfer search. Its projection
is only necessary; accepted projected loops need not lift. Exhausted transfer
graphs concern B alone. Caps remain `UNDECIDED`; no center conclusion follows.

## A precise decimal-transfer obstruction — PAPER PROOF

Freeze the first seven boundary carry cases and trim positions of this center,
allowing both the base b and its coefficients to vary. Write x_t for the first
center coefficient before phase t. The witnessed boundary laws are

```text
x1 = 2*x0 - 2*b + 1
x2 = 2*x1 + 1
x3 = 2*x2 - 2*b + 1
x4 = x3 - b
x5 = 2*x4 + 2
x6 = 2*x5 - 2*b + 1
2*x6 + 1 = b - 1
```

Here phase 3 overflows; phase 6 trims a neutral pair; the other displayed
phases do not trim. These equations follow directly from normalization:
if k_j are center carries, entering e=k_0 and outgoing k_m=1-e, the raw head is
`2*x-b*(k1+km)+e+k_(m-1)` without overflow, and `x+b*(e-k1)` with overflow.

Successive substitution gives `x6=32*x0-46*b+33`, so

```text
64*x0 + 68 = 93*b.
```

As `93^(-1) = 53 (mod 64)`, this forces **b = 20 (mod 64)**.
In particular b=10 is impossible for these boundary cases.
Even the final two equations suffice for the decimal contradiction:
x6 is odd, and b=2*x6+2 is divisible by four.
At b=20 the actual heads are `28,17,35,31,11,24,9`, followed by raw head 19.

This is a restriction on that explicit itinerary. Different carry cases,
different centers, different periods, and decimal certificates in general are
outside its scope.

```bash
python3 calculation/agent-116/base20_transfer.py --full-system
python3 calculation/agent-116/base20_transfer.py --emit-equations
```

The standard-library script independently extracts the actual carries and
checks all seven laws. With the complete center carry words, phase widths,
and trims frozen, symbolic propagation gives 14 integer linear equations in
the 13 independent initial center entries and b. Exact `Fraction` elimination
has rank 14 and forces b=20. A separate exact row reduction corroborated that
unique solution. `--emit-equations` prints the full matrix for direct review.
This stronger computation has the same explicit frozen-itinerary limitation.

## Lean verification

The only imported result is the existing
`P196.Drafts.Agent120NeutralBandCalibration.A120Certificate`.
Registered endpoints under `Agent116.Base20` are:

```text
cert20_ok             cert20_overflows       cert20_gain
lychrel20_template    lychrel20_seed           exists_lychrel20
```

The three finite statements use `by decide` and have no axioms.
The three derived theorems use only `propext`, `Classical.choice`, `Quot.sound`.
Lean is 4.19.0, one thread, with an 8 GiB address-space ceiling and a
1,200-second timeout. The actual build including three A120 dependencies
took 11.641 seconds, peak RSS 639,884 KiB; the new module's official
`lean4checker` replay took 1.676 seconds, peak RSS 529,280 KiB.

The literal `python3 tools/verify.py --changed` completed with exit 0:

```text
[rules] 5218 Lean files, 302 projects, OK
[changed] against origin/main: 1 new/changed Lean file(s); building 1 module(s); auditing 1 project(s)
[build] OK
[kernel replay] 1 module(s) re-checked by lean4checker
[axioms] 6 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The complete changed gate took 49.158 seconds, peak RSS 476,644 KiB.
Its comparison base is main `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

The campaign instruction in issue #289 requires a review PR and forbids
README/RESULTS edits; those explicit instructions govern this contribution.
All new source stays in Agent116 paths except the required registry entry.

## Coordination and credit

- Task claim: issue #289, comment 6432821654.
- Constructive progress: issue #289, comment 6432893018.
- Existing A120 checker/soundness, B/C search sources, prior known-base
  certificates, and Agent7 normalization supply the foundations.
- REPORT_203 / REPORT_213 retain the prior historical-source audit.
- This result adds explicit base-20 data, independent replay, registered
  Lean instantiation, and the scoped transfer obstruction.
