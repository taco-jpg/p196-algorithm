# Three-column saturation obstruction — Agent #4

**Established:** a closed walk in the exact three-column exterior relation with P steps and O overflows can satisfy 2O=P only if **8 divides P**. Combining this with the complementary-quotient charge and width laws excludes a returned full six-phase interface of period 36. Every nonempty full return in phases {2,4,8,16,14,10} therefore has **P >= 42**, regardless of interface size and without assuming the signed gap gains are nonnegative.

The finite relation, complete edge certificate, arbitrary-length telescoping argument, and final explicitly conditional period bound are compiled Lean theorems. The ordinary whole-word projection and its application to the complementary quotient are the written bridge below. The result is not yet one end-to-end Lean theorem about the ordinary 196 orbit. No persistent interface, finite Lychrel witness, global acyclicity result, external novelty, or independent human review is claimed. This is AI-assisted research.

## 1. Exact necessary three-column relation

Use least-significant-first canonical mirrored-sum words q. Their coefficients are in 0,...,18, q is symmetric, and its exterior coefficient is positive. Let (a,b,c) be its first three coefficients; assume its width is at least six. Let e be the actual carry into its reflected third column from the intervening word. Every carry is a bit because a column total is at most 18+1.

The low-side carries and digits are

    l1 = floor(a/10),             l2 = floor((b+l1)/10),
    d0 = a mod 10,                d1 = (b+l1) mod 10,
    d2 = (c+l2) mod 10.

The high-side carries and digits are

    r2 = floor((c+e)/10),         r1 = floor((b+r2)/10),
    gamma = floor((a+r1)/10),
    h0 = (a+r1) mod 10,           h1 = (b+r2) mod 10,
    h2 = (c+e) mod 10.

Without overflow, the first three coefficients of the next mirrored-sum word are (d0+h0,d1+h1,d2+h2). With overflow, the new leading digit is one and reflection shifts by one column, giving (d0+1,d1+h0,d2+h1). These are exactly `advance` in `PrefixModel.lean`.

There is no leading-zero ambiguity: without overflow, the high digit a+r1 is positive; with overflow, the appended one is positive. The output width increases by exactly gamma. This derives the relation from ordinary decimal normalization, not independent guesses for each column's carry.

The finite relation permits either e for every prefix. It is a necessary overapproximation of complete trajectories. Individual edges can be realized by ordinary integers, as the tests demonstrate; this does not make every sequence of abstract edges simultaneously realizable by one integer.

## 2. A strictness certificate, not a finite time cutoff

The domain has 18*19*19=6,498 prefixes and 12,996 controlled edges. The generator starts from the valid one-column potential

    a: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
    U: 0 0 0 1 0 1 1 1 2  1  1  1  2  1  2  2  2  3.

Every edge obeys 2*gamma+U(a_next)<=1+U(a). Give a tight edge cost one except for the following recurrent eight-cycle, whose edges have cost zero:

    (8,12,9) -> (17,5,0) -> (8,13,5) -> (17,6,11)
      -> (8,14,8) -> (17,8,17) -> (8,16,16) -> (17,13,14)
      -> (8,12,9).

Longest-path relaxation in this zero/one-cost graph supplies a nonnegative rank r bounded by 40. Define V=41U+r. The emitted finite tables satisfy, for every controlled edge,

    82*gamma + V(next) <= 41 + V(current).                 (1)

They also supply a clock C in 0,...,7 such that equality in (1) implies

    C(next) = C(current)+1 (mod 8).                        (2)

The clock is the displayed cycle index on its eight vertices and zero elsewhere. There are twelve tight controlled edges because four cycle transitions permit both carry controls. The generated V ranges from zero through 128.

The generator is an untrusted producer. It uses only exact integers, no floating-point optimizer or graph package. Eighteen `by decide +kernel` row theorems independently check the entire finite statement (1)--(2) inside Lean's kernel. The proof does not rely on trusting the search, rank relaxation, or strongly-connected-component interpretation.

## 3. Arbitrary closed walks and saturation

For any P-step valid prefix path, summing (1) gives

    82O + V(final) <= 41P + V(initial).

If the prefix returns, its potential cancels, yielding 2O<=P. If 2O=P, the sum of the nonnegative step slacks is zero, so each step is tight. Equation (2) then advances the clock by P; its return forces P=0 modulo eight. `tight_clock_telescope` proves this by induction for arbitrary P, and `saturated_closed_prefix_period` supplies the closed-path theorem.

The finite exterior inequality

    a+1 <= a_next+10*gamma

also telescopes, giving P<=10O on a returned prefix. Therefore a nonempty closed prefix path has O>0. This weak lower rate is used only for positivity; sharper lower growth bounds already exist elsewhere in the repository.

No fixed time horizon appears in these path theorems. The finite work establishes a local certificate, after which induction applies it to walks of every length. Conversely, this does not exclude arbitrary longer nonsaturated returns.

## 4. Application to every full complementary-quotient return

The source is `../../contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, initially inspected at main `a71d6e79b009da691e2d97057f83e108a3fcff4f`, blob `f48a0ec61e7ff0419bb9121a792e79505810db50`. Its template is

    B c^g A d^h C d^h rev(A) c^g rev(B), d=18-c.

For any finite returned quotient walk, choose both initial gaps large enough that every within-walk gap is at least three. Such a choice exists even for signed gains: there are only finitely many partial losses. The source's exact quotient identity realizes the whole finite walk. The first three coefficients depend only on the phase and B, because the outer constant band is long enough. Hence a returned phase/interface supplies a closed path in the three-column relation above. This does not assume an infinite repetition or nonnegative gains.

For c in {2,4,8,16,14,10}, a returned phase forces 6|P. Agent #2's exterior charge law, independently formalized by Agent #5, forces 9|O. Returning all interfaces makes the exact width gain equal 2*(Delta_g+Delta_h), so O is even. These credited results give 18|O and O>0. Therefore 2O<=P implies P>=36.

If P<42, divisibility by six now forces P=36. The overflow restrictions then force O=18, so 2O=P. The saturation theorem would require 8|36, a contradiction. Therefore **P>=42**.

The relevant Lean endpoint is `unit_phase_full_cycle_period_at_least_forty_two`. Its phase, even-overflow, and modulo-nine premises remain explicit. They must not be attributed to arbitrary prefix paths: they come from the full quotient return as just explained. A returned integer itself is not being claimed; only the finite interfaces return while the two gap coordinates may change.

For a saturated full six-phase return, the same reasoning also gives 72|P: 8|P and 18|O with P=2O imply this by elementary arithmetic. This extra observation is written here, not a separately declared endpoint in the current formal file.

## 5. Compilation, exact bytes, and tests

Published generator: `c208c5cb85d0e923d410c20091e50c7d8f4ceded`.
Published path theorem: `c3cdc2c653e8be52ccdf1df5871d9ec1b12e9ee7`.
Byte-exact generated certificate and audit commit: **`e681826088c49e8a3c3421be54c395c145c61db4`**.

Fresh GitHub Actions run **38686134384** passed using official Lean **4.19.0**, release commit **6caaee842e94**. It verified source hashes, regenerated the certificate, compiled all three modules, audited every theorem, and safely rebased its own generated files before publishing. The same generated source bytes had already passed a separate local native build. The exact CI research snapshot was subsequently downloaded and its hashes checked.

The 18 finite row declarations have no axiom dependencies. The ten path/support declarations use only `propext`, `Classical.choice`, and `Quot.sound`, with the finite `exterior_progress` declaration using no axioms. There are no admitted proofs, custom axioms, or native-evaluation shortcuts in the accepted sources. The audits do not establish literature originality or a bridge absent from the theorem statements.

Source SHA-256 values:

    PrefixModel.lean:
      8ea1199dbd413869efd8e48955119361cb44c6d7cc69722d276cb1c825da37b0
    SaturationCertificate.lean:
      7ce611b42425dcad50527788d95b9bfa648883ed11561df3ebbb6438a1728791
    SaturationTheorem.lean:
      9a7f65a82d611bf24f2661de0715d0a70f69da0b5a51d3ad00725cde37f5b2eb
    Complete edge stream:
      63832c9046703be3fdfba4fec90465810bb9b46bbd7f026a9099e9a4fde732ee

Reproduce from this directory:

    python generate_certificate.py
    python verify_lean.py --lean /path/to/lean-4.19.0-linux/bin/lean \
      PrefixModel.lean SaturationCertificate.lean SaturationTheorem.lean
    python test_prefix_projection.py

The build uses one Lean worker to keep memory bounded. `test_prefix_projection.py` separately realizes every one of the 12,996 prefix/carry controls with an ordinary seven-digit integer and checks 10,000 seeded ordinary integers of widths six through 100. The one-step prefix and width formulas agree with literal decimal reversal and integer addition. These controls passed locally; the all-length conclusion comes from the stated proof, not from these samples.

## 6. Collaboration and remaining gap

Agent #2's charge/gain result is commit `12563cbc1604dd226dd50cec97e2bf175d190998`. Agent #5's formal exterior clock is `db65db3646694d95fe6a8e7a0f836d66d8e6a4c8`. Agent #8's mass and path formalization is `8902b2b8d5cf495d7ee407e905817e1737aae770`. Agent #9's exact erasure source is `9a8c30c0e097f3ef0cfc5c614be957f153e4b827`. Their contributions are not attributed to Agent #4.

The same CI run freshly compiled and dependency-audited the pinned Agent #5, #8, and #9 modules, totaling 82 supporting declarations. Agent #4 then independently rebuilt their exact downloaded bytes locally and repeated those audits successfully. A reciprocal-review record is published separately; compilation alone is not a claim that their whole-word semantic bridges are already integrated.

No cycle meeting the persistent two-gap criterion is supplied. Longer nonsaturated returns, full end-to-end Lean integration of the ordinary word projection and charge premises, and a proof of infinite palindrome avoidance for the particular 196 orbit remain unresolved.
