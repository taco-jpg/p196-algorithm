# Scoped census: missing Lean coverage 和 selected no-overflow horizon task

This document preserves the substance of the coverage specialist's report delivered to the parent before inspecting the newly authored counting module. It is a source census 和 semantic analysis, not a repository-wide mathematical acceptance record.

## Recommended task

The no-overflow finite-horizon Fibonacci family is the best immediate gap. It extends the existing Agent #9 package directly, matches a preserved written theorem, 和 is disjoint from Agent #2's general overflow bound 和 Agent #3's protected overflow finite-horizon family.

This was a read-only, scoped census, pinned to main `4b4edf976b2c7a9ba1dad80636c0e21c66350325`; the latest locally inspected coordination ref was `c0ef2640881a860150503d0485385542a0c16a68`. No repository files or remote state were changed by this specialist. No Lean execution or repository-wide coverage percentage is claimed.

For source paths below, the retained original tree is:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/`

Current flattened Lean sources are directly under `proofs/`. The inspected local repository was `/workspace/scratch/8dcaf4a67fa4/p196-agent9`.

## Inspected entry points 和 scope

Repository `AGENTS.md`; current `proofs/README.md`, `STATUS.md`, `OPEN_PROBLEMS.md`; relevant entries of `FINDINGS.md` 和 `REPORTS.md`; `PUBLICATION_SCOPE.md` 和 `PUBLICATION_POLICY.md`; task records on the inspected `origin/p196/coordination` ref; the historical Agent #9 five-module package; selected retained research arguments 和 current corresponding declaration interfaces.

The current flattened Lean source search checked the relevant declaration names 和 terms. This is not an exhaustive semantic review of every current, historical, generated, or remote-only Lean file. An apparent missing result is a candidate identified within this inspected scope, not proof of global absence.

## Prioritized candidate inventory

### 1. No-overflow fibers with any fixed future avoidance horizon — selected

Exact written statement: for `m,k >= 1`, let the target half-word be

```lean
11 :: (List.replicate m 9 ++ List.replicate k 18)
```

Its complete reflection has exactly `fib m` canonical no-overflow preimages under `Agent8.stepWord`; every canonical integer realizing that target pair-word avoids palindromes for the next `k` positive steps.

Source: `research/persist_inverse_fibers_proof.txt`, lines 163–187, especially "No-overflow family" at line 178.

Existing interfaces in coordination package `patches/agent9-nooverflow-fibonacci-20261016/`:

```lean
advance_formula
run_append
leading_eleven_exact
preimages_length
preimages_nodup
leading_eleven_positive
canonical_membership
fullPreimages_membership
fullPreimages_nodup
```

`DecimalSafeRuns__aaaac5a66315c5e2.lean` supplies:

```lean
DecimalSafeRuns.HasRun18
DecimalSafeRuns.hasRun18_iter
DecimalSafeRuns.iter_not_palindrome_of_run
```

Missing proof: show appended symbols `18` preserve `Counts.U`; transfer the exact count through canonical filtering 和 reflection; identify the central run of length `2*k`; transport list arithmetic to canonical numeric digits.

Overlap: historical Agent #9 proves the global even-width maximum 和 one-step avoidance only. Agent #3 explicitly reserves the overflow family with half-word `[14] ++ xs ++ 18^k`, not this family.

### 2. Exact finite seed counting for finite-horizon avoidance

Exact written statement: for the selected disjoint mirrored blocks,

\[
\#\{\text{canonical width-}L\text{ seeds with no marked all-nine block}\}
=9\,10^{L-1-2rJ}(10^{2r}-1)^J.
\]

This yields the early-hit upper bound `(1-10^(-2r))^J`, with the manuscript's explicit `r` 和 `J`.

Source: `contributions/2026-10-14-finite-horizon-density/README.md`, "Exact finite counting bound" at line 10; equations (1)–(5). The README explicitly says counting 和 asymptotics are written proofs, not Lean formalizations.

Existing interface in `FiniteHorizonBlocks__de01e0bf306b4eaa.lean`:

```lean
FiniteHorizonBlocks.blockLength
FiniteHorizonBlocks.MirroredNines
FiniteHorizonBlocks.mirroredNines_hasRun18
FiniteHorizonBlocks.mirroredNines_safe_prefix
```

Missing proof: a duplicate-free enumeration of canonical width-`L` digit vectors; disjointness of the selected `2*r*J` positions; product counting; soundness of the implication from an early palindrome hit to absence of every marker. Begin with the exact integer count before adding probability or limits.

Overlap: no matching task appeared in inspected coordination records. This counts an ensemble of seeds; Agent #3 counts preimages of one prescribed target.

### 3. Uniform temporal counting of digit-sum excursions

Exact written statement: for `F(B)=E_10(2B)`, every block of `F(B)+1` consecutive times contains a time with digit sum above `B`. Consequently every interval `[s,s+N)` contains at least

\[
\left\lfloor\frac{N}{F(B)+1}\right\rfloor
\]

such times; the stated lower asymptotic 和 lower Banach density is at least `1/(F(B)+1)`.

Source: `research/continuation/strengthening_notes.txt`, section 6, beginning line 233.

Existing exact interface in `SharpUniformDecimal__c7370132a3682d7b.lean`:

```lean
DecimalUniformEscape.digitSum_uniform_window_sharp
  (n : Nat) (hn : 0 < n) (B s : Nat) :
  ∃ t, s ≤ t ∧
    t ≤ s + sharpDigitSumEscapeBound B ∧
    B < digitSum (orbit n t)
```

Missing proof: partition a finite interval into disjoint blocks; select one witness per complete block; prove witnesses are distinct; count them. The finite count can use Lean/Std. Real density limits are a separate extension.

Overlap: no matching active temporal-density task found. Existing uniform escape already proves the window existence statement; re-proving that would duplicate coverage.

### 4. Closed factorial upper bound for the exact escape recurrence

Exact written statement:

\[
E_b(M)\le (4\kappa_b)^{M-1}M!\quad(M\ge1).
\]

For decimal, the existing recurrence has `kappa=5`, giving `E_10(M) <= 20^(M-1) * M!`.

Source: `research/continuation/strengthening_notes.txt`, equation (9), line 226.

Existing interfaces in `SharpUniformEscape__a2423abeea30044f.lean`:

```lean
DecimalProfile.sharpEscapeBound
DecimalProfile.sharpEscapeBound_one
DecimalProfile.sharpEscapeBound_recurrence
DecimalProfile.sharpEscapeBound_eq
DecimalProfile.sharpEscapeBound_ge
```

Missing proof: induction on the explicit recurrence, with a factorial function or suitable standard-library interface; a numeric uniform escape corollary follows.

Overlap: no matching task or current flattened Lean `factorial` occurrence found. Agent #4's general-base normalization concerns carry representatives, not this mass-escape recurrence. This is a small formalization task, not a major new mathematical result.

### 5. Arbitrarily large one-step digit-sum collapse

Exact written statement: for every even `k >= 2`, the canonical pair-word

\[
q=(10,\underbrace{9,\ldots,9}_{k},10)
\]

has a positive decimal realization `n` satisfying

\[
T(n)=11\cdot10^{k+1},\qquad
S(T(n))=2,\qquad
S(n)=(9k+20)/2.
\]

Thus no universal positive proportional lower bound for next digit sum in terms of current digit sum or width can hold.

Source: `research/continuation/strengthening_notes.txt`, line 285 onward.

Existing interfaces in `LychrelDigitSums__cee9857896191714.lean`:

```lean
FoldedDecimal.valid_word_realizable
DecimalDigits.value_output
FoldedDecimal.step_eq_word_value
DecimalMass.wordSum_columns
DecimalMass.digitSum_value
```

Agent #9's `normalize_scan` also supplies a convenient list normalization bridge.

Missing proof: exact normalization of the displayed family; symmetric canonical realization; digit-mass calculation; unboundedness of the initial mass while the output mass remains two.

Overlap: existing `ExteriorErasure.full_binary_collapse` concerns a different exterior map. No matching ordinary digit-sum collapse theorem or coordination task was located.

### 6. The sharp decimal running-maximum constant `3/4`

Exact written statement: for a fixed positive seed, with `D_N` its maximum digit sum through time `N`,

\[
\liminf_{N\to\infty}\frac{D_N}{\sqrt N}\ge\frac34.
\]

The source also supplies the explicit finite radical bound using initial zero-run parameter `A`.

Source: `research/continuation/general_base_audit.txt`, section 7, lines 179–206; `UnboundedDigitSums.tex`, equations for the finite bound 和 liminf.

Existing interfaces:

```lean
DecimalQuantitativeMass.runningMax
DecimalQuantitativeMass.digitSum_le_runningMax
DecimalQuantitativeMass.runningMax_attained
DecimalQuantitativeMass.runningMax_lower_bound
DecimalZeroGap.simultaneous_zero_interval
DecimalZeroGap.zero_core_extends
DecimalProfile.length_le_mass_zero_runs_sharp
```

Missing proof: the existing `runningMax_lower_bound` uses a coarser zero-gap bound. Recover the factor-nine mass estimate from the exact all-nine zero-run branch, obtain the sharper quadratic inequality, then prove the radical 和 asymptotic consequences.

Overlap: Agent #8 owns lower-width potentials, not this digit-mass inequality. The source explicitly says the constant `3/4` is a written consequence rather than part of the existing quantitative Lean file. Current flattened sources contained no `liminf` declaration.

### 7. Exact arithmetic obstruction to a continuous 10-adic extension

Exact written statement: if `n` has canonical width `ell`, `1<=c<=9`, 和 `j>=ell`, then

\[
\operatorname{reverse}_{10}(n+c10^j)
=c+10^{j-\ell+1}\operatorname{reverse}_{10}(n).
\]

This gives inputs approaching `n` 10-adically whose reverse-add outputs approach `n+c`, proving discontinuity of ordinary finite-integer reverse-add at every positive `n`.

Source: `research/astra_modular_fixed_modulus_theorem.md`, section 4, line 150 onward.

Existing interfaces: `DigitPerturbation__63c0c6ce55368669.lean` provides `digitSpike`, `value_digitSpike`, `reflected_digitSpike_value`, 和 `reverse10_twoDigits`; `DecimalDigits.reverse10_value` supplies general canonical reversal.

Missing proof: canonical digits of an arbitrary seed with a new distant leading digit; the general exact reversal identity; an elementary congruence-neighborhood discontinuity theorem. A topology library is optional if the endpoint uses explicit powers-of-ten congruences.

Overlap: modular-autonomy classification is already covered 和 must not be confused with this discontinuity theorem. No matching current declaration or task was found.

## Important coverage corrections

Several attractive apparent gaps in the old findings matrix are already covered:

- All-moduli exact-length palindrome saturation 和 fixed-modulus closed-set obstruction: `ExactLengthResidues.exact_length_palindrome_residues`, `exact_length_palindrome_residues_explicit`, `every_orbit_matches_palindrome`, 和 `fixed_modulus_closed_set_contains_palindrome` already exist. Agent #111's retained README records independent review 和 a fresh 13-module build.
- Reversal residue autonomy iff `M ∣ 99`: already in `ModularAutonomy__ce19bc4666cd4240.lean`.
- Even-width palindromic overflow implies divisibility by `121`: already in `astra_lean_modular__af14192db66453cd.lean`.
- General-base carry normalization, even-base sharpness, lower-width potentials, fourth-smoothing bounds, finite boundary transport, 和 fourth-column obstruction: reserved by current Agent #4/#421/#422, #8, #10, #14, 和 #15 records respectively.
- Historical Agent #9 Fibonacci package: exact mathematical scope appears complete at the advertised source level; its record still separates `LEAN-CHECKED` from pending independent semantic review 和 integration.

## Pre-implementation independent semantic review of the selected contract

The proposed no-overflow extension is mathematically consistent with the inspected interfaces.

1. Count preservation is exact. `advance_formula` specializes at `18` to
   ```lean
   advance 18 v = ⟨v.a, v.c, 0, v.d⟩
   ```
   so `Counts.U = a+d` is unchanged. `run_append` 和 `leading_eleven_exact` therefore give `fib m` after any appended run of eighteens.

2. Canonical filtering removes nothing. `leading_eleven_positive` accepts an arbitrary suffix, so every enumerated preimage has positive outer label. Its proof actually forces the outer input coefficient to be `5`.

3. The time offset needs explicit treatment. For any canonical integer `z` whose pair-word is the target `r`, the central run has length `2*k`. `iter_not_palindrome_of_run` proves
   ```lean
   ¬ Palindrome (orbit z (t + 1))
   ```
   for `t<k`, using `1+2*t <= 2*k`. If `z=step n` for a preimage integer `n`, these are times 2 through `k+1` of `n`. Time 1 of `n` requires its own argument: `r` has odd outer coefficient `11`, whereas a palindromic integer has even mirrored pair sums.

4. A pair-word is not its integer value. The bridge must quantify over `Canonical z d L` with `columnSum d L=r`, or prove that the actual output's canonical digits have that pair-word. Interpreting `value r L` as a realization silently changes the arithmetic.

5. This is not the maximum at the enlarged fixed width. The constructed width is `2*(m+k+1)` 和 the count is `fib m`; the unrestricted historical maximum at that width is `fib(m+k)`. The source claims preservation of the exponential rate with fixed `k`, not equality with the unrestricted maximum at each width. Any entropy or limit conclusion needs its own stated argument.

6. Parameter endpoints matter. The count formula may extend to `m=0`, but then the fiber is empty because `fib 0=0`. Nonemptiness requires `m>=1`. Positive-horizon safety requires `k>=1`.

A separate finite arithmetic control passed for all 24 parameter pairs `1<=m<=6`, `1<=k<=4`, enumerating 80 preimage words in total. It independently checked the local carry equations, duplicate freedom, exact Fibonacci counts, actual no-overflow normalization, exact common target, canonical digit realization, 和 the asserted numeric safety windows for selected realizations. The source, parameters, observed stdout, 和 replay provenance are preserved alongside this report. This is a finite semantic control, not a Lean proof.
