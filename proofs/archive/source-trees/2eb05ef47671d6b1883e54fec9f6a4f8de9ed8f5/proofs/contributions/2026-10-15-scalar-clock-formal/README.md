# Actual scalar-clock transitions, rotations, and width growth

This contribution formalizes the elementary actual-orbit bridge for the
scalar clock

`(4,8,16,7,15,6,13)`.

It proves the overflow schedule, width growth at every phase rotation and
time offset, the width-one obstruction, and a conditional warmup transfer.
The numerical 94/98 hierarchy has **not** been instantiated in Lean here.
Its wide-word bound remains an explicit hypothesis in the transfer theorems.

## Exact actual transition

For an admissible symmetric decimal pair word `q` of width `L`, put
`a=q(0)` and let `c` be the actual carry entering column `L−1`. The proofs
establish `c∈{0,1}` and identify the Boolean transducer input with that exact
carry. Put

- `l=a mod 10`,
- `h=(a+c) mod 10`,
- `e=(a+c)/10`.

The next outside coefficient is `l+h` when `e=0`, and `l+1` when `e=1`.
The actual overflow is `e`. This formula includes width one; no separation
or independence of boundary windows is assumed.

## Proven consequences

The seven clock phases force overflows `(0,0,1,0,1,0,1)`. Every rotated block
of seven phases has three overflows. If the actual outside coefficient
follows `phase(s+i)` for `i=0,...,7R` starting at orbit time `a`, then

`width(a+7R) = width(a) + 3R`.

For canonical initial decimal digits, the same formula gives the actual
numeric iterate's decimal length. Width-one admissible words cannot
complete one period, for any starting phase.

For initial width `L≥2`, define `k=ceil(max(14−L,0)/3)` using natural-number
arithmetic. Then `k≤4`; if the clock persists for those `k` periods, its width
is at least fourteen. Given an independently supplied actual wide-word bound
`B`, the formal transfer yields `R≤B+k≤B+4`. The hypothesis named `hwide` is
present in the Lean theorem. No concrete value of `B` is asserted by this
package.

| File | Main content |
| --- | --- |
| `ScalarClock.lean` | Finite phase/overflow arithmetic and exact allowed incoming bits. |
| `ActualScalar.lean` | Exact connection to whole-word carries, next coefficient, and overflow. |
| `ScalarOrbit.lean` | Actual orbit composition; arbitrary phase/time rotations; width and decimal-length formulas; conditional warmup transfer. |
| `WidthOne.lean` | Actual width-one and width-two carry calculations excluding a complete period from width one. |

These results concern a prescribed outside-coefficient sequence. They do
not prove palindrome occurrence, non-occurrence, or the P196 conjecture.

## Verification

`check.py` rebuilds the exact `LychrelDigitSums.lean` prerequisite and all
four new modules in a fresh temporary directory, then audits the transitive
axiom dependencies of all 35 public theorems. It records source, object,
log, and direct dependency hashes, and checks that sources and dependencies
remain unchanged. It imports no preexisting project object files and does
not rebuild or import the large seven-step rank certificate.

Run with Lean 4.19.0:

```sh
python3 check.py --lean /path/to/lean-4.19.0/bin/lean
```

The supplied `verification.json` and `compile.log` record the successful
fresh build. Only Lean's standard `propext`, `Quot.sound`, and
`Classical.choice` are permitted by the axiom audit. No custom axiom,
`native_decide`, `sorry`, or `admit` occurs in these proof sources.

The current verification environment used the previously documented
readlink compatibility shim for the Lean executable's self-path lookup.
The shim does not alter the elaborator or kernel; ordinary installations
can run the command directly.
