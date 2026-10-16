# Independent adversarial review

Status: **PASS**. Mathematical/source review, finite controls, and the final
empty-object-directory Lean rebuild have completed. The accepted run is
`rebuild-bfdb7a5-final/manifest.json`; the first attempt remains separately
recorded as failed because of the reviewer audit-policy correction described
below. No blocking defect was found in the mathematical certificate budget.

The actual `certificate-budget/check.py` entrypoint was run, including `All`.
It rebuilt ten modules with Lean 4.19.0, audited 1,904 kernel-safe declarations
(including 1,501 exported, internal, and generated theorems), and separately
inventoried 1,088 unsafe compiler artifacts. Every mathematical declaration
has transitive axiom dependencies contained in the original three-item
whitelist. All ten source blobs match the fixed mathematical commit and all
source hashes remained unchanged throughout the accepted run. No author's
compiled object was used.

## Intended interpretation

`P` is `cert.states.length`, not the length of the links list. For index
`i < P`, the actual overflow is `Agent109.Cert.gam (cert.st i)`, the two signed
increments are `gam + j + j1 - 2` and `gam + j2 + k - 2`, and the successor is
indexed by `(i+1) % P`. These are the unmodified existing certificate semantics.

The advertised result is a necessary condition on accepted certificates. Neither
an accepted instance nor an integer in a nonpalindromic infinite orbit is
constructed by the budget result. Nothing here establishes that 196 enters a
certificate, or establishes the global exterior no-return target.

## Source-level checks

* `LocalOK` supplies exact raw-block trimming equalities. Its trim counts are
  arbitrary natural numbers, with no maximality requirement. Therefore a
  certified next exterior cannot simply be identified with the deterministic
  maximally trimmed `outerNext` exterior. The local arithmetic modules reviewed
  use the supplied equalities directly.
* The physical finite-block width is `2|B| + 2|A| + |C|`. The exact raw lengths
  are `|Br|=|B|+1`, `|Ar|+gam=|A|+2`, and `|Cr|+gam=|C|+2`. Hence the local
  width identity is derived from the actual source functions. Cyclic summation
  gives `H=2(Dg+Dh)` with no width identity as an extra hypothesis.
* Neither local increment is required to be nonnegative. The inequalities on
  successive `lo,lo'` values telescope around the cycle to give nonnegative
  total increments. Treating local gains as nonnegative would be incorrect.
* The actual exterior coefficient is `B.head?.getD c`. Empty `B` exposes the
  first outer-band coefficient `c`; it does not supply zero. The carry budget
  proves this case separately and derives the carry entering a nonempty
  exterior from the actual block normalization. It does not choose an
  arbitrary carry sequence as a theorem hypothesis.
* `Admissible0` gives positive exterior data only at index zero. The reviewed
  carry budget proves positivity at later indices from the actual local
  transition; no all-indices positivity hypothesis is silently introduced.
  Its bound `0<H` also uses the existing validity condition `0<P`.
* `check` does not require `links.length=P`. It uses `getD` at state indices.
  Extra links are irrelevant. A missing accessed link defaults to `lo=0`,
  conflicting with `2<=lo`, so a valid certificate has every needed link.
  New totals must continue to range over `P`, as the reviewed code does.
* Exterior charge is preserved by removing any number of trailing current
  phase letters, including zero. The six-phase carry clock thus applies to
  the certificate's nonmaximal trimming. Width parity and this clock yield
  divisibility of the overflow count by eighteen. The interface clock is
  derived from `Ar` and its two explicit trims; its cyclic residue condition
  is not postulated as a numerical premise.

## Independent finite controls

`independent_controls.py` imports no code under review. It reconstructs raw
blocks from the mathematical formulas and compares them with direct
normalization and literal Python-integer reverse-and-add. It enumerates all
16 nonneutral phases, every empty/single-coefficient `B,A`, and centers that
are empty, a single even coefficient, or a doubled coefficient. Every legal
trim of every resulting raw triple is tested.

The retained JSON records 192,000 source states, 596,608 arbitrary trims,
182,400 literal integer steps, 184,128 nonmaximal exterior trims, 28,576 empty
target exteriors, and 223,728 six-phase modular-clock controls. All controls
passed. These finite computations are not proofs of the all-length claims.

Besides width and scalar exterior identities, the control checks the independent
whole-block mass formula, for `F(s)=2 sum(B)+2 sum(A)+sum(C)`:

`F(s') + 2 c' (dg-dh) = 2 F(s) (mod 9)`.

For a six-phase state, division by the invertible phase gives a second clock;
cyclic summation therefore supports the advertised difference-of-gains residue.

The JSON preserves counterexamples to three incorrect proof shortcuts:
nonmaximal trimming can differ from `outerNext`; local gains can be negative;
and the scalar lower-budget inequality fails if positivity is dropped
(`p=e=0`). The last example is outside `Admissible0` and is not a counterexample
to the intended theorem.

## Independent compiler audit method

`independent_rebuild.py` creates a new object directory, copies the selected
source dependency closure into it, clears inherited Lean search paths, and
compiles every research dependency with the supplied Lean 4.19.0 wrapper.
It does not use the development cache, its build driver, or its declaration
scanner. Source hashes are checked after compilation.

For the transitive axiom audit it imports the new objects and enumerates every
compiled constant by its owning module in `Lean.Environment`. Every kernel-safe
declaration, including every exported and internal theorem, is transitively
checked with `Lean.collectAxioms`. Any dependency outside `propext`,
`Classical.choice`, and `Quot.sound` fails that check. Compiler-generated unsafe
artifacts are recorded separately; they cannot occur in kernel-safe proof
terms. A separate lexical scan excludes admitted proofs, custom axiom
declarations, native decision shortcuts, kernel-check skips, and source-level
`unsafe`/`partial` declarations.

The compiler audit mechanism was smoke-tested on an independent one-theorem
module. That smoke test is not the requested proof-module rebuild.

The first full attempt, `rebuild-bfdb7a5`, successfully recompiled all ten
modules, then correctly stopped at an overbroad audit policy: it initially
treated Lean compiler-stage unsafe artifacts as mathematical declarations.
The rejected `_cstage1` constant used `lcProof`. Lean 4.19.0's own
`Lean/Compiler/LCNF/ToLCNF.lean` explicitly documents this replacement of
nested proofs during compilation. The retained `StageProbe.lean` confirms the
constant has `unsafe=true`, `theorem=false`. The corrected audit uses the
kernel's `ConstantInfo.isUnsafe`, retains every such artifact in a separate
inventory, and does **not** add `lcProof` or any generated placeholder to the
mathematical axiom whitelist. The original failed manifest and logs remain.
The corrected mechanism was validated before starting a second full build
from another empty object directory. That second run passed, and it is the
accepted final checker run. The first failed run is not relabeled as passing.

The reviewed local source commit is
`bfdb7a5c8fc65bdceede0c397628b33598430704`, whose tree was independently read as
`10713ab15f1e3b31631df5c8429ca8e37321e7e7`. The publishing parent reports remote
commit `ec8f8e2a3580d061ba386cea918f49fa279385dd` with this same tree; this is the
remote reproducibility pin for the mathematical source.

The mathematical pin contains the earlier reviewer driver. Running the final
accepted checker also requires the corrected `independent_rebuild.py`; its
exact SHA-256 is recorded in the accepted manifest. The publisher should cite
the subsequent review commit for the runnable checker and retain the above
pin for the mathematical source.
