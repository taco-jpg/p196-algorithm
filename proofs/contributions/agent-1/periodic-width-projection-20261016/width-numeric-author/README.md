# Ordinary decimal-width residue wrappers

Frozen author source: `proofs/Agent1PeriodicWidthNumeric.lean`, SHA256
`31a0d8c78e64e8b1a0929fb808c5dbc40adfdf39db7248c58d0870d1eeee1706`,
Git blob `eef4bc74a2037d70b9244767fa2efbe93939a422`.
Author: Agent1 specialist `/root/research_status/numeric_bridge_review`.
Imports: the frozen `Agent1PeriodicWidth` and existing `Agent1PeriodicNumeric`.
Neither imported source was edited.

The two public wrappers in namespace `Agent1.Periodic` are:

* `periodic_decimalLength_mod_eight B H w k n d hlen hcan`:
  `decimalLength n % 8 = widthResidue B H`. Its only premises are
  `w.length = 4` and the original `DecimalDigits.Canonical n d`
  at `(periodicWord B H w k).length`. This allows `k = 0` whenever the
  premises hold. It requires neither coefficient bounds nor a column-sum
  representation because it identifies only the input digit count.
* `periodic_actual_step_decimalLength_mod_eight B H w k hk n d hB hH hw
  hcan hrep hlen`: the actual `Lychrel196.step n` has decimal length modulo
  eight equal to `widthResidue (quotientOuter B H w) (quotientCenter B H w)`.
  It retains exactly the existing positive-copy-count, coefficient-bound,
  canonical-digit, and complete in-range column-sum premises, and adds
  period length four. In particular, `hrep` quantifies over every input
  column; it is not a phase-only or finite-sample test.

The original `Canonical` predicate requires positive length, bounded decimal
digits, a nonzero leading digit, and equality of their value to the input.
It does not admit padding the input with leading zeros. The first proof
reuses `DecimalQuantitativeMass.decimalLength_of_canonical` and
`periodicWord_length_mod_eight`. The second reuses the existing
`periodic_actual_step_decimalLength` and `quotient_width_mod_eight`, with
the original definition of `rawGamma`. No new carry calculation is proved.
For small positive `k`, this is a width-residue identity only; it supplies
no whole-word quotient formula, canonical successor representation by that
quotient, or chosen ordinary integer orbit.

## Actual verification

Official Lean 4.19.0, commit `6caaee842e94`, binary SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every Lean invocation used `--trust=0 -j1 -DElab.async=false` and a
1500 MiB RSS stop threshold monitored every 10 ms, with a 600-second
timeout and no virtual-address cap.

`attempt-001` retained a preflight failure before Lean started: the supplied
older guard `FILES.json` omits compiled objects, so its missing object hash
prevented the initially intended reuse. The diagnostic and unchanged source
snapshot are retained. No proof failure occurred.

`attempt-002` passed all three actual invocations:

| Check | Seconds | Sampled peak RSS (KiB) |
| --- | ---: | ---: |
| Fresh unchanged existing Numeric module | 0.40 | 443320 |
| New WidthNumeric module | 0.31 | 444496 |
| Full new-module origin audit | 1.29 | 753548 |

The kernel-reported maximum child RSS was 753420 KiB. No watchdog fired.
This is an **author increment**, with fifteen reused pinned objects
(the fourteen-module Quotient closure and frozen Width), one existing
dependency compiled fresh, and the new wrapper compiled fresh. It is not
a fresh build of the complete dependency closure. The unchanged existing
Numeric source SHA256 is
`d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7`,
matching the Guard registry and earlier reviewed source build.

The full audit enumerates every declaration originating in WidthNumeric,
checks the literal types and axioms of both public exports, rejects custom
safe axioms, and follows transitive axiom dependencies of all theorem,
safe definition, and safe opaque constants. Result: **3 theorem constants,
0 safe definitions, 0 safe opaques**. The third theorem is an elaborator
proof helper. The axiom union is exactly `propext`, `Classical.choice`,
and `Quot.sound`. No unsafe implementation axioms, unsafe/partial
definitions, or unsafe opaques originate in this module.

Exact commands, logs, source/object pins, imported-source provenance,
literal public types, and audit inventory are under `attempt-002/`.
`run-attempt.py` reproduces this author increment in a new labelled folder.
Source and dependency pins were checked before and after verification.
The scoped width registry adds Numeric and WidthNumeric and a third root,
giving thirty modules and fifteen public theorem endpoints. Its outer
catalog and WidthLift gates remain explicitly provisional.

The parent owns independent combined verification and publication. This
helper made no Git writes and did not alter frozen Width or the global
accepted registry.
