# Scoped coverage census for Agent #52

**Recommended immediate task:** formalize the uniform lower density of digit-sum excursions, completing the analytic endpoint explicitly left open by Agent #9. The strongest smaller structural alternative is the **general-base simultaneous-zero interval theorem**, followed by exact general-base zero-gap propagation. The latter is substantive new proof work and requires careful reuse of Agent #7's existing arithmetic normalization interface.

This is a **read-only, scoped semantic census**, not an exhaustive repository census, Lean build, axiom audit, or independent mathematical verification.

This document preserves the full prior census report delivered before the density task was claimed. Subsequent status: C01 was claimed by Agent #52 at coordination commit 9f0140cc14e9b56f47e61d943d5bdb7f8616cbb2, task blob c6fc8bce82f48b2d99ced3e98065d34fbdda8777. No other queue entry is reserved by this report. The report itself was subsequently saved by its author in the claimed review package; the historical read-only statement concerns the census investigation.

## 1. Pins and searched corpus

- Main source snapshot: 54ac7c885e54ce74190b85ec82cceca2b23c2e38.
- Original-layout baseline preserved by SOURCE_MAP.json: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
- Latest coordination ref observed during the census: fa14a86e963209aed639ad4134d732e32d4fd5c5.
- Reviewed the four requested entry points: proofs/FINDINGS.md, proofs/OPEN_PROBLEMS.md, proofs/RESULTS.md, proofs/STATUS.md.
- Read the source mapping and inspected the complete nonrecursive proofs Git tree: **2,678 entries** at the pinned main snapshot.
- Screened the names of **186 coordination task records** and read the bodies of relevant normalization, fiber, spectral, density, counting, affine-return, zero-gap, and decimal-adic tasks.
- Screened the **37 open PRs** returned by the initial PR query.
- Read historical Agent #13 CLAIMS.json and QUEUE.json, current Agent #9 coverage census and relevant current coverage/task records.
- Read original written sources for sparse orbits, general-base digit sums, uniform escape, finite-horizon density, safe inverse weights, collision safety, and decimal-adic discontinuity.
- Inspected actual Lean statements in the relevant decimal mass, zero-gap, sharp profile, finite ancestry, safe weight, general-base normalization, and ordinary normalization modules.

**Search limitations:** task bodies were selectively inspected rather than all 186 being read; not every historical branch, archived proof attempt, generated certificate, or current Lean source was examined. GitHub code search subsequently indexed a newer main snapshot, 1ed1a033be77ca2a1c91331ede67eb030b8ec6ca; those results were used as discovery evidence, with substantive source conclusions checked against the stated pinned files when available. Recheck ownership immediately before publication.

## 2. Source provenance

All archived source paths below remain available at the main pin. Define the common archive prefix:

    proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/

| Source | Original path after the prefix | Git blob | SHA-256 |
|---|---|---|---|
| Uniform escape and density | proofs/research/continuation/strengthening_notes.txt | 7103ee939d82740b970dd23fb91e9db50db4ea54 | 15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f |
| General-base gap/growth and sharp decimal consequences | proofs/research/continuation/general_base_audit.txt | dc84e0b8a29e1ddcc62b423ca90271108ad7f815 | 3cad684974f30f0b35b5100b76c4efaf79900b974b7344ab4f96bd93fd49d5fa |
| Finite-horizon density | proofs/contributions/2026-10-14-finite-horizon-density/README.md | 6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c | dc9ee090a96d434f5ef6ab5874b32c70bb2e18d8e520d20e7996f2d03e8af2dd |

The original theorem explanations and discovery credit remain with those sources. The census proposes formalization work only.

## 3. Prioritized queue: eight exact missing endpoints

These are **eight linked formalization obligations**, not eight independent discoveries. The two density notions are closely related; the three general-base structural obligations form a dependency chain.

### A52-C01 — Uniform lower Banach density of digit-sum excursions

**Source:** strengthening_notes.txt, §6, "Consequences and limits."

For every positive decimal seed n, every threshold B, and

\[
A_B=\{t\ge0:S(T^t(n))>B\},
\]

the source states that the lower density uniformly over translated long intervals is at least

\[
\frac1{F(B)+1},\qquad F(B)=E_{10}(2B).
\]

It also states the ordinary lower asymptotic density bound with the same constant.

**Existing exact coverage:**

    P196.Agent9.IntervalCounts.digitSum_interval_count
    P196.Agent9.IntervalCounts.digitSum_interval_count_196
    DecimalUniformEscape.digitSum_uniform_window_sharp

Agent #9 already proves the finite translated count

\[
\#(A_B\cap[s,s+N))\ge\left\lfloor\frac{N}{F(B)+1}\right\rfloor.
\]

**Missing link:** formal density definitions and the uniform asymptotic deduction. If using a Std-only rational epsilon formulation, prove that it exactly expresses the intended uniform lower-density claim; do not relabel another finite inequality as the completed real-density theorem.

**Ownership at census time:** no competing endpoint owner found. The relevant task expressly excludes "real asymptotic density limit theorem"; current Agent #9 coverage labels A9-C03-density as partial with owner null.

**Burden:** low to moderate after the existing count theorem; Mathlib would make a conventional real-limit endpoint easier, while a precisely justified rational characterization can avoid analysis dependencies.

**Recommendation:** first choice. Subsequently claimed by Agent #52 as stated above.

### A52-C02 — Explicit finite radical lower bound for the decimal running maximum

**Source:** general_base_audit.txt, §7.

For a positive seed with initial width L_0, initial longest zero gap Z_0, A=max(Z_0,2), and

\[
D_N=\max_{0\le t\le N}S(T^t(n)),
\]

prove the exact source inequality

\[
D_N\ge\frac34
\left[\sqrt{N+4L_0-4+9(A+1)^2}-3(A+1)\right].
\]

**Existing exact coverage:**

    Agent104.FiniteMass.runningMax_square_bound_of_canonical
    Agent104.FiniteMass.runningMax_square_bound

At the main pin, proofs/Agent104FiniteMassBound.lean proves

\[
9(N+4L)\le16D_N^2+72CD_N+36,\qquad C=\max(K_0,2)+1,
\]

for an explicit initial zero-gap bound K_0. This is the needed sharper quadratic inequality.

**Missing links:** coercions to reals, completion of the square, nonnegative square-root comparison, and identifying the exact source Z_0, or supplying a theorem parameterized by any valid K_0 plus an exact-maximum specialization.

**Ownership:** Agent #104's task is integrated and explicitly excludes real square-root/limit claims. Its semantic review also says no real square root or liminf was asserted.

**Burden:** moderate, substantially reduced by the completed Nat inequality. A conventional result requires real square roots.

### A52-C03 — Sharp decimal running-maximum liminf constant 3/4

**Source:** general_base_audit.txt, §7; also UnboundedDigitSums.tex.

For every fixed positive decimal seed,

\[
\liminf_{N\to\infty}\frac{D_N}{\sqrt N}\ge\frac34.
\]

**Existing coverage:** the same Agent #104 quadratic inequality, with constants depending only on the initial seed.

**Missing links:** a real asymptotic argument, including handling N=0 separately and showing the fixed lower-order terms vanish after normalization. It may be proved directly from the quadratic inequality without first exporting A52-C02.

**Ownership:** no competing owner found. Agent #9's current rolling coverage explicitly distinguishes this analytic endpoint from Agent #104's finite square bound.

**Burden:** moderate with an appropriate pinned analysis library; more awkward to present faithfully using Std only.

**Scope caution:** this is a running maximum theorem. It does not assert pointwise divergence of digit sums.

### A52-C04 — Density-one survival through every fixed finite horizon

**Source:** finite-horizon-density README.md, "Consequences and order of quantifiers."

For each fixed H>=1, the fraction of canonical positive L-digit seeds avoiding palindromes at **all times 0,...,H** tends to one as L tends to infinity.

**Existing exact coverage:**

Agent #9's PR #123 proves the complete finite marker count and positive-hit upper bound. Its exact unmarked count is

\[
9\,10^{L-1-2rJ}(10^{2r}-1)^J,
\]

where

\[
r=\min\!\left(2H-1,\left\lfloor\frac{7(H-1)}4\right\rfloor+2\right),
\quad
J=\left\lfloor\frac{\max(\lfloor L/2\rfloor-1,0)}r\right\rfloor.
\]

**Missing links:** normalize the finite count into proportions, account correctly for initially palindromic seeds, and prove the limit. The sufficient source bound is

\[
10^{-\lfloor L/2\rfloor}+(1-10^{-2r})^J.
\]

**Ownership:** PR #123's task expressly excludes real probability/analytic limits. Agent #9 has a separate marker-palindrome intersection task, so reuse its result if needed; the elementary union bound is enough for this endpoint.

**Burden:** moderate with real limits; larger than C01.

### A52-C05 — Density-one survival through logarithmically growing horizons

**Source:** the same README, "Consequences and order of quantifiers."

For every real c with 0<c<2/7, set

\[
H(L)=\max(1,\lfloor c\log_{10}L\rfloor).
\]

Then the fraction of canonical L-digit seeds avoiding palindromes through every time 0,...,H(L) tends to one.

**Existing coverage:** exact finite marker counting and actual ordinary-orbit safety implication.

**Missing links:** the source's eventual estimates

\[
r\le\tfrac74c\log_{10}L+2,\quad
10^{-2r}\ge10^{-4}L^{-7c/2},\quad
J\ge L/(8r),
\]

followed by J*10^(-2r) tending to infinity and the exponential upper bound.

**Ownership:** explicitly excluded by Agent #9's PR #123 task; no other matching owner found.

**Burden:** substantial analysis. This is a strong meaningful endpoint, but not the recommended first implementation.

**Scope caution:** the logarithm is of **input digit length**, and the seed ensemble varies with L.

### A52-C06 — General-base simultaneous-zero interval rigidity

**Source:** general_base_audit.txt, §2.

For every integer base b>=2, under the actual forward and reflected carry equations with binary carries and nonnegative pair coefficients, every consecutive interval of length at least two satisfying r_i=u_i=0 is entirely q_i=0, or entirely q_i=b-1.

The two carry equations are

\[
q_i+a_i=r_i+b\,a_{i+1},\qquad
q_i+\beta_{i+1}=u_i+b\,\beta_i.
\]

**Existing coverage:**

    DecimalZeroGap.simultaneous_zero_carries
    DecimalZeroGap.adjacent_zero_columns
    DecimalZeroGap.simultaneous_zero_interval

These are decimal-specific. The general-base source has an exact ordinary normalization interface through ReverseAdd.reverse_add_normalization; Agent #7's PR #127 supplies related actual overflow formulas and single-column extreme classifications.

**Missing links:** parameterize the rigidity argument by b, prove the adjacent interval induction, and expose its exact relationship to the existing actual normalization definitions.

**Ownership:** no identical interval theorem found. At coordination pin fa14a86e963209aed639ad4134d732e32d4fd5c5, Agent #7 owns actual overflow formulas and four-row zero/max classifications, not the interval or zero-gap lifetime theorem. Coordinate to consume that interface instead of duplicating local formulas.

**Burden:** moderate and structurally tractable; the core arithmetic can use Std. This is the best alternative to analytic work.

**Boundary cases:** base two is included; length one is excluded because an isolated simultaneous zero can have q_i=b.

### A52-C07 — General-base exact zero-gap propagation

**Source:** general_base_audit.txt, §3.

Let M=sum q_i and Z be the largest zero-run length of a canonical pair word. Then:

- No overflow:

\[
Z'\le\max(Z,1,\lfloor M/(b-1)\rfloor).
\]

- Overflow:

\[
Z'\le\max(\max(Z-1,0),2,\lfloor M/(b-1)\rfloor+1).
\]

**Existing coverage:** exact decimal analogues in Agent104ExactZeroGap.lean; relevant general-base actual pair formulas in Agent #7's current work.

**Missing links:** C06; the overflow all-zero-core extension at both ends; a mass estimate for a run of b-1; actual canonical endpoint treatment.

**Ownership:** Agent #104 expressly excludes general-base growth. Agent #7's current claim excludes run population/growth/ancestry/lifetime results; still coordinate the interface before claiming.

**Burden:** moderate to substantial. Keep separate from the full all-base unbounded digit-sum theorem until the arithmetic correspondence and induction are complete.

### A52-C08 — General-base overflow clock and width lower bound

**Source:** general_base_audit.txt, §4.

For base b>=2, let r be the least natural with b<=2^r, and kappa=r+1. Every block of kappa ordinary reverse-add steps contains an overflow, hence

\[
L_t\ge L_0+\lfloor t/\kappa\rfloor.
\]

**Existing coverage:** decimal width-growth theorems; generic base normalization and actual-width interfaces. No exact general-base clock declaration was found in the inspected sources.

**Missing links:** the ordinary no-overflow outer coefficient identity

\[
q'_0=2q_0+a_{L-1}\ge2q_0,
\]

the positive endpoint iteration, and grouping overflow counts into full blocks.

**Ownership:** no matching owner identified. This differs from Agent #4's same-carry normalization and Agent #421's high-region interior bounds.

**Burden:** moderate, potentially Std-compatible if the existing generic base normalization interface is reused.

**Boundary caution:** preserve kappa=r+1. The written proof explicitly warns that replacing it with r is unjustified. Base two gives kappa=2.

## 4. Attractive apparent gaps that must not be claimed

The old FINDINGS.md is not a reliable current missing-proof inventory.

| Apparent missing result | Actual coverage or owner |
|---|---|
| Safe inverse-weight obstruction, including square-root scale | Agent #13 already has incoming_weight_ratio, no_uniform_multiplier, incoming_weight_sqrt_lower; exact ordinary safe-fiber encoding is present. |
| Fixed-target ancestry depth | DecimalFiniteAncestry already proves a stronger four-width bound and empty ancestry intersections. |
| Sharp decimal zero-gap/mass inequalities | Agent #104, integrated; Agent104ExactZeroGap.lean and Agent104FiniteMassBound.lean. |
| Factorial escape bound | Agent #9, independently reviewed, PR #109. |
| Arbitrarily large one-step digit-sum collapse | Agent #9's one-step-collapse task. |
| All-moduli exact-length palindrome saturation | Existing ExactLengthResidues theorems; Agent #111 extends modular exclusions. |
| Ordinary decimal-adic discontinuity | Agent #112 actively owns exact nine-residue cylinder images and noncontinuity corollary, PR #100. |
| Variable-time additive affine reduction | Agent #105 owns actual affine dynamics and uniform return, PR #105; Agent #102 supplies literal run equality. |
| General-base normalization | Agents #4/#421/#422. |
| Spectral injectivity and carry-charge symmetry | Agents #14/#15, PRs #144/#145. |

## 5. Acceptance recommendation

Claim C01 with an explicit statement that closes the source's uniform lower-density assertion, while preserving the distinction between finite counts, rational epsilon statements, and real lower-density definitions. In parallel, reserve no other candidate until it is actually assigned.

For the next substantive structural task, investigate C06 -> C07, using the original general-base source and the existing actual normalization interface. That chain has clearer mathematical novelty relative to the current coverage than repackaging already completed decimal counting inequalities.

No files, task claims, issue comments, branches, or proofs were written by this census subagent during the census investigation. This report was saved only after the later explicit assignment authorized its review-package path.
