# Independent review of the saturation extension

Status: **PASS**. Source/statement review, new prefix controls, and the complete
15-module empty-object rebuild have passed. The accepted evidence is
`rebuild-abbf9ef/manifest.json`. No blocking defect was found.

The actual updated `check.py` entrypoint rebuilt all fifteen modules including
`All`, then audited **2,118 kernel-safe declarations**, including **1,637
theorems** (exported, private, and generated). Their transitive dependencies
contain only the original three allowed axioms. Another **1,189 unsafe
compiler artifacts** are separately inventoried. Every selected source blob
matches the fixed commit, every source hash remained unchanged, and no author
or previous reviewer compiled object was reused.

Mathematical local commit: `abbf9efe73146dcc091383023daddb07c98bc4ba`.
Its tree was independently checked as
`5be42ebc3e535b3fa22eeeb461900fc106bb7a88`. The publishing parent reports
remote commit `70b276c326989807310b9c8e61fa354411666e40` with that same tree.

## What the projection means

`padPrefix B c` is exactly the first three coefficients of `B` followed by
an indefinitely extended constant `c` band. It is a projection of the
symbolic certificate state. When `B=[]` and an actual outer band has length
two, this triple need not equal the first three physical coefficients of the
realized pair word. For example, `c=2, B=[], A=[5], C=[], g=h=2` has actual
prefix `(2,2,5)` and padded prefix `(2,2,2)`.

The new proof does not assume the false physical-prefix equality. It proves
the required recurrence directly from `Agent109.Br` and the normalization
definitions. This is enough to construct a path in Agent4's explicitly
defined finite relation, irrespective of a separate ordinary-integer lift
of an arbitrary path in that relation.

## Exactness of the local bridge

* For `|B|=0,1,2`, the input to the extended third column is `kOf c`. The
  nonneutral `Phase c` hypothesis is what makes the continued band reset its
  carry. The separate short-block lemmas account for the entrance column
  and the reflected alignment after overflow.
* For `B=a::b::d::bs`, the input bit is the actual
  `(norm bs.reverse (kOf c)).2`. Its bound follows from bounded coefficients.
  The proof does not impose an arbitrary fixed input bit, nor does it assume
  the bit is determined by the three coefficients alone.
* Removing any number of terminal `c'` letters leaves the `c'`-padded prefix
  unchanged. `padPrefix_trim` explicitly proves this for any index and trim
  count, including zero trim and an empty remaining exterior.
* `local_prefix_step` uses only the existing `LocalOK` conditions and produces
  an edge whose overflow is exactly `gam s`. There is no block-width cap,
  maximal-trimming assumption, or assumption on the actual band length
  beyond what is already encoded in the original certificate format.

## No assumed abstract path in the final endpoints

The generic helper `closed_prefix_path_of_projection` has explicit projection
hypotheses. The `_of_path` helpers likewise accept a `ClosedPrefixPath`.
These are not the direct results advertised for certificates.

`certificate_closed_prefix_path` supplies those hypotheses using the actual
`statePrefix`, `prefix_bounds`, `prefix_a`, and `local_prefix_step`. Initial
positive exterior data are propagated using the already reviewed actual
exterior transition. The path closes by indexing states modulo `cert.P`.
Each input bit is selected from the local proven existence statement; outside
the finite period its arbitrary fallback value is unused. The overflow sum is
identified with `totalGam cert` through the exact second component of every
transition, not by a newly assumed scalar equality.

The direct endpoints `period_at_least_forty_two` and
`checked_period_at_least_forty_two` do not accept a path, numerical congruence,
or potential inequality. They derive these facts from the original certificate
validity/check, initial positive exterior/admissibility, and initial SixPhase.

The direct saturation endpoints add precisely the requested saturation
condition `2*totalGam cert = cert.P`. They derive `P % 72 = 0` and `72 <= P`;
they do not assume the eight-step clock or any stronger path property.

Mathematically, the existing necessary conditions give `H % 18 = 0` and
`P % 6 = 0`. The new exact projection imports the checked finite clock:
if `P=2H`, then `P % 8 = 0`. Thus `P=36` is excluded, giving `P>=42` among
multiples of six. In the saturated case, `36 | P` and `8 | P` give `72 | P`;
the positive period then gives `P>=72`.

## New independent finite controls

`prefix_controls.py` imports no implementation under review and does not
rerun the old budget controls. It computes raw exteriors and three-column
updates independently using ordinary column normalization. It checks every
phase, all exteriors through length three, and all three-coefficient prefixes
with six selected tails through total length six. These tails include both
actual carry outcomes and propagation through runs of nines.

The retained JSON records **774,304 source exteriors** and **994,329 legal
suffix trims**, including **220,025 nonmaximal trims**, **32 empty targets**,
and both incoming carry bits. All new controls passed. They are finite
controls, not a proof of the all-width bridge.

It also retains exact counterexamples to three invalid shortcuts:

1. Padded coefficients need not be physical first-three coefficients at gap 2.
2. `B=(1,9,9,0)` and `B=(1,9,9,10)` at phase 2 have the same padded prefix,
   but actual incoming bits 0 and 1 produce different prefix outputs.
3. At excluded neutral phase 9, `B=[10]` violates the short-block recurrence
   with the phase bit. The nonneutral phase hypothesis is essential.

None is a counterexample to the reviewed theorem as stated.

## Rebuild and driver review

The accepted checker entrypoint was the updated `certificate-budget/check.py`,
which includes both new modules and `All`. Its full closure comprised the
previous ten modules plus `PrefixModel`, `SaturationCertificate`,
`SaturationTheorem`, `CertificatePrefix`, and `CertificateSaturation`.

The parent-owned driver changes were independently inspected: they add exactly
the three Agent4 dependency paths and exempt the exact standard-library import
`Lean.Elab.Tactic.Omega` from research-source mapping. The axiom policy was not
modified. No source under the older published review directory was edited by
this reviewer for the extension.

The new build uses a new, initially nonexistent directory
`reviewer-build/saturation-abbf9ef`; no author object or previous reviewer
object is reused. The established driver separately inventories unsafe compiler
artifacts and strictly audits every kernel-safe declaration and every theorem
against `propext`, `Classical.choice`, and `Quot.sound`.

Scope remains necessary conditions on accepted certificates only. There is
no accepted certificate instance, general exterior no-return theorem, or
conclusion about the orbit of 196.
