# Results

Every result below is a Lean 4 theorem that builds from source in this repository and whose axioms are only `propext`, `Classical.choice` and `Quot.sound` (checked by `python3 tools/verify.py`). There are 301 results (6585 checked endpoints — the theorems and definitions a reader should rely on — in 5217 modules). The only exception is the last section, [Written research reports (not Lean-verified)](#written-research-reports-not-lean-verified): those are paper proofs and computations by research agents, not Lean theorems.

**None of them proves that 196 is a Lychrel number.** Each result has an explicit scope; the scope text is the author's own description and says what is *not* claimed.

Machine-readable version: [`lean/registry.json`](lean/registry.json) (modules, root modules, every endpoint).

## Contents

1. [The orbit of 196 and palindrome-prefix exclusions](#the-orbit-of-196-and-palindrome-prefix-exclusions) (20)
2. [A conditional route to a Lychrel number](#a-conditional-route-to-a-lychrel-number) (4)
3. [One reverse-and-add step: predecessors, fibers, palindromic outputs](#one-reverse-and-add-step-predecessors-fibers-palindromic-outputs) (33)
4. [Carries: what carry sequences reveal and how they evolve](#carries-what-carry-sequences-reveal-and-how-they-evolve) (51)
5. [Periodic (repeated-block) words and their quotient dynamics](#periodic-repeated-block-words-and-their-quotient-dynamics) (28)
6. [Affine run words](#affine-run-words) (10)
7. [Finite abstractions and transducers](#finite-abstractions-and-transducers) (7)
8. [Sprint agent results (PRs #261–#287)](#sprint-agent-results-prs-261287) (7)
9. [Written research reports (not Lean-verified)](#written-research-reports-not-lean-verified) (19)

## The orbit of 196 and palindrome-prefix exclusions

Results about the actual orbit of 196, and the prefix-exclusion method used for it. `Core` also bundles four reviewed results on other topics (listed as its claims).

- **AllTimePowerResidues:** Exact fixed-exponent root counts modulo 99 for the ordinary orbit of 196 at every natural time: the first three residues have an additional `gcd(e,10)` condition and multiplicity, while the later count is zero or `gcd(e,6)` (`P196.AllTimePowerResidues.Main`). Includes the complete initial-time phase formula, necessary restrictions on actual powers, fifth-power compatibility exactly from time three onward, and incompatibility of exponent zero. These are modular conditions; no actual power occurrence, palindrome avoidance, or Lychrel conclusion is claimed.

- **OrbitPowerObstruction:** For every decimal seed and time, its orbit residue modulo 99 matches some power with exponent at least two exactly when the seed is not congruent to 3 or 6 modulo 9; every compatible residue has the explicit seventh-power representative with base `r ^ 13 % 99` (`P196.OrbitPowerObstruction.Main`). Seeds divisible by 3 but not by 9 therefore have no nontrivial integer power anywhere in their orbits. The modular converse asserts no actual power occurrence, and no palindrome or Lychrel conclusion is claimed.

- **OrbitPowerResidues:** For every positive exponent `e` and time `6 + t`, the number of distinct residues modulo 99 whose `e`-th powers match the ordinary orbit of 196 is `gcd e 6` if `gcd e 6` divides `t + 4`, and zero otherwise (`P196.OrbitPowerResidues.Main`). Gives exact modular compatibility and necessary time restrictions for actual powers, including squares, cubes, and sixth powers; compatibility does not assert that a power occurs in the integer orbit, and no palindrome or Lychrel conclusion is claimed.

### Orbit196Basics

*Basic facts about the orbit of 196*

Two direct facts about the ordinary orbit of 196, proved in the shared foundation module: none of the iterates at times 0 to 100 is a palindrome (a finite check), and the digit sum along the orbit exceeds every bound infinitely often (for every B and every start time there is a later t with digit sum > B). Neither implies that 196 is a Lychrel number.

- Root module(s): `P196.Foundations.LychrelDigitSums`
- 1 modules, 2 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Lychrel196.no_palindrome_through_100 : ∀ (k : Nat), k ≤ 100 → ¬Lychrel196.Palindrome (Lychrel196.orbit 196 k)
DecimalUnboundedMass.digitSum_196_unbounded_after : ∀ (B start : Nat),
  ∃ t, start ≤ t ∧ B < DecimalMass.digitSum (Lychrel196.orbit 196 t)
```
</details>

### Agent315Orbit196Residues

*The orbit of 196 is never divisible by 3 or 9*

No iterate of 196 is divisible by 3 (hence not by 9) (`not_dvd3_orbit196`, `not_dvd9_orbit196`). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent315Orbit196Residues.Orbit196Mod3`, `P196.Agent315Orbit196Residues.Orbit196Mod9`
- 3 modules, 4 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
not_dvd3_orbit196 (k : Nat) : ¬ 3 ∣ orbit 196 k
not_dvd9_orbit196 (k : Nat) : ¬ 9 ∣ orbit 196 k
```
</details>

### Agent9DigitSumWindows

*Digit sums along the orbit of 196 grow within explicit windows*

Quantitative digit-sum escape for 196: for every bound B and start s there is a time t in [s, s + W(B)] with digit sum of the t-th iterate greater than B, for explicit window sizes W (including a factorial bound 20^(2B-1)·(2B)! and a sharper one), and a lower bound on how many times in any interval exceed B. Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent9DigitSumWindows.UniformDecimal`, `P196.Agent9DigitSumWindows.SharpUniformDecimal`, `P196.Agent9DigitSumWindows.Agent9DecimalFactorialEscape`, `P196.Agent9DigitSumWindows.Agent9DigitSumIntervalCounts`
- 13 modules, 12 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
digitSum_uniform_window_196 (B s : Nat) : ∃ t, s ≤ t ∧ t ≤ s + digitSumEscapeBound B ∧ B < digitSum (orbit 196 t)
digitSum_uniform_window_196_factorial (B s : Nat) : ∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧ B < DecimalMass.digitSum (Lychrel196.orbit 196 t)
digitSum_interval_count_196 (B s N : Nat) : N / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) ≤ ((List.range' s N).filter (fun t => decide (B < DecimalMass.digitSum (Lychrel196.orbit 196 t)))).length
```
</details>

### Core

*Explicit accepted module registry: consolidation-reviewed core*

Previously accepted thirteen-prefix closure together with four independently reviewed branch-only packages; disjoint abstract-model and actual-arithmetic conclusions remain distinct.

- Root module(s): `P196.Core.OuterOrbit`, `P196.Core.AlternatingScalarBoundary`, `P196.Core.HighBaseFirstHit`, `P196.Agent10EightCarry.DifferenceObservability`, `P196.Core.TwoDigitMain`
- 37 modules, 25 checked endpoints
- Claim `agent113-thirteen-prefix`: Thirteen restricted palindrome-prefix ancestry bounds and exact sharpness; no unrestricted Lychrel theorem.
- Claim `agent3-five-step-charge`: From step five on, the charge of the explicit outer list map is divisible by 11 (`charge ... % 11 = 0`); it is not shown to be zero, and no ordinary-integer correspondence is claimed.
- Claim `agent9-alternating-spatial-boundary`: No finite spatial cut path from the root trace to either specified constant trace; actual exterior bridge remains separate.
- Claim `agent11-high-base-first-hit`: Ordinary integer reverse-add in every integer base at least 3, under exact high-pair-sum and canonical-digit hypotheses; first positive hit 1 or 2.
- Claim `agent10-nine-carry-reconstruction`: Identical complete carry words at times 0..8 and equal initial width determine pair sums and the next integer, not the initial integer.

<details><summary>Main statements (Lean)</summary>

```lean
Agent113.TwoDigit.no_196_thirteen_arith : ∀ (t k : Nat),
  Lychrel196.Palindrome (Lychrel196.orbit 196 t) →
    ¬Lychrel196.orbit 196 t / 10 ^ k ∈ [10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83]
Agent113.TwoDigit.startsTwo_iff : ∀ (a b P : Nat),
  Agent113.TwoDigit.StartsTwo a b P ↔ 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9 ∧ ∃ k, P / 10 ^ k = 10 * a + b
```
</details>

### Agent118PrefixKernel

*Prefixes 217, 218 and 777 excluded from the orbit of 196*

Kernel-checked prefix certificates (Agent #118): every positive seed that reaches a palindrome beginning with 217, 218 or 777 does so within 23, 33 and 25 steps respectively; since the first 100 iterates of 196 contain no palindrome, no palindrome in the orbit of 196 begins with 217, 218 or 777 (`no_196_217_palindrome`, `no_196_218_palindrome`, `no_196_777_palindrome`). Controls show the 218 bound 33 is attained and the family is reached (10700 reaches 21812 in two steps). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent118PrefixKernel.Conclusion217`, `P196.Agent118PrefixKernel.Conclusion777`, `P196.Agent118PrefixKernel.Controls218`, `P196.Agent118PrefixKernel.Witnesses`, `P196.Agent118PrefixKernel.Conclusion218`
- 1551 modules, 28 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
no_196_217_palindrome : ∀ t, ¬ PalindromeStarts3 2 1 7 (orbit 196 t)
no_196_218_palindrome : ∀ t, ¬ PalindromeStarts3 2 1 8 (orbit 196 t)
no_196_777_palindrome : ∀ t, ¬ PalindromeStarts3 7 7 7 (orbit 196 t)
ancestry_bound23 : ∀ A P t, 0 < A → PalindromeStarts3 2 1 7 P → orbit A t = P → t ≤ 23
ancestry_bound25 : ∀ A P t, 0 < A → PalindromeStarts3 7 7 7 P → orbit A t = P → t ≤ 25
```
</details>

### Agent124Prefix620

*Prefix 620 excluded from the orbit of 196*

Every positive seed that reaches a palindrome beginning with 620 does so within 12 steps (sharp: see Agent104P620Witness), so no palindrome in the orbit of 196 begins with 620 (`no_196_620`). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent124Prefix620.A124Prefix620Final`
- 327 modules, 2 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
ancestry_620 : ∀ A P t, 0 < A → PalStarts3 6 2 0 P → orbit A t = P → t ≤ 12
no_196_620 : ∀ t, ¬ PalStarts3 6 2 0 (orbit 196 t)
```
</details>

### Agent104P620Witness

Exact positive ordinary seed 19014942070 reaches palindrome 62003033030026 at time 12; first hit includes time zero; any uniform bound for the unchanged PalStarts3 6 2 0 family is at least 12.

- Root module(s): `P196.Agent104P620Witness.Agent104620Witness`
- 11 modules, 7 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent104.Prefix620Witness.exact_trajectory : List.map (Lychrel196.orbit Agent104.Prefix620Witness.seed)
    (List.range 13) =
  [19014942070, 26039883161, 42178776223, 74446563347, 148783127794, 646504515635, 1183019921281, 3004319025092,
    5909528159095, 11819046418190, 21000510510001, 31002012010013, 62003033030026]
Agent104.Prefix620Witness.twelve_steps : Lychrel196.orbit Agent104.Prefix620Witness.seed 12 =
  Agent104.Prefix620Witness.target
Agent104.Prefix620Witness.target_canonical : DecimalDigits.Canonical Agent104.Prefix620Witness.target
  Agent104.Prefix620Witness.targetDigit 14
```
</details>

### Agent104Prefix739

*Prefix 739 excluded from the orbit of 196*

Seven-column prefix certificate: every positive seed that reaches a palindrome beginning with 739 does so within 39 steps, so no palindrome in the orbit of 196 begins with 739 (`no_196_739_palindrome`). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent104Prefix739.Conclusion739`
- 346 modules, 3 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
no_196_739_palindrome : ∀ t, ¬ PalindromeStarts739 (orbit 196 t)
ancestry_bound39 : ∀ A P t, 0 < A → PalindromeStarts739 P → orbit A t = P → t ≤ 39
```
</details>

### Agent124PrefixFiveSix

*33 three-digit prefix classes excluded from the orbit of 196*

For each of 33 three-digit prefix classes (a, b, c) there is an ancestry bound of at most 40 steps for every positive seed, so no palindrome in the orbit of 196 begins with any of these prefixes (`no_196_all`; the list is `classes` in the Lean source). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent124PrefixFiveSix.Agent124PrefixSummary`
- 358 modules, 3 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
classes_length : classes.length = 33
ancestry_all : ∀ e ∈ classes, ∀ A P t, 0 < A → PalStarts3 e.1 e.2.1 e.2.2.1 P → orbit A t = P → t ≤ e.2.2.2
no_196_all : ∀ t, ∀ e ∈ classes, ¬ PalStarts3 e.1 e.2.1 e.2.2.1 (orbit 196 t)
```
</details>

### Agent117P2641

Ordinary reverse-and-add ancestry bound t <= 6 for every positive A ending at a canonical palindrome with prefix 2641, and all-time exclusion of that family from orbit 196. No other palindrome-family or unrestricted 196 conclusion.

- Root module(s): `P196.Agent117P2641.A124117P2641K7Final`
- 103 modules, 2 checked endpoints
- Claim `A117-2641-ANCESTRY`: For all A P t, 0 < A and PalStartsL [2,6,4,1] P and orbit A t = P imply t <= 6.
- Claim `A117-2641-NO196`: For all t, not PalStartsL [2,6,4,1] (orbit 196 t). This excludes only the 2641-prefix palindrome family.

<details><summary>Main statements (Lean)</summary>

```lean
Agent124.Cert117P2641K7.ancestry_2641 : ∀ (A P t : Nat),
  0 < A → Agent124.PrefixL.PalStartsL [2, 6, 4, 1] P → Lychrel196.orbit A t = P → t ≤ 6
Agent124.Cert117P2641K7.no_196_2641 : ∀ (t : Nat), ¬Agent124.PrefixL.PalStartsL [2, 6, 4, 1] (Lychrel196.orbit 196 t)
```
</details>

### Agent124FourDigit

*Longer-prefix refinements excluded from the orbit of 196*

Refinements by longer digit prefixes (lists `entries00`, `entries01`, ... in the F4 and F5 certificates), each with an ancestry bound: no palindrome in the orbit of 196 begins with any listed prefix (`no_196_00` ... `no_196_06`). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent124FourDigit.A124F4Final`, `P196.Agent124FourDigit.A124F5Final`
- 100 modules, 24 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
ancestry_00 : ∀ e ∈ entries00, ∀ A P t, 0 < A → PalStartsL e.1 P → orbit A t = P → t ≤ e.2 + 1
no_196_00 : ∀ t, ∀ e ∈ entries00, ¬ PalStartsL e.1 (orbit 196 t)
```
</details>

### PrefixK45

*763 further digit prefixes excluded from the orbit of 196 (width-4 and width-5 certificates)*

Width-4 and width-5 backward prefix certificates in the same format as `Agent124FourDigit`, with their own rank trees (4222 and 1190 nodes) checked by the existing `Agent124.CodeCert` row and short-word checkers: 757 four-digit prefixes at width 4 (`entries00` ... `entries07` in `PrefixK45.NewK4`) and 6 at width 5 (`entries00` in `PrefixK45.NewK5`), each with an ancestry bound of at most 14 steps, so no palindrome in the orbit of 196 begins with any listed prefix (`no_196_..`). None of these prefixes was excluded by an earlier result; together with the earlier refinements they exclude all ten four-digit refinements of 75 more three-digit prefixes (cells `R` in the combined table). Compiled and axiom-audited, not independently reviewed.

- Root module(s): `P196.PrefixK45.NewK4Final`, `P196.PrefixK45.NewK5Final`
- 23 modules, 18 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
ancestry_00 : ∀ e ∈ entries00, ∀ A P t, 0 < A → PalStartsL e.1 P → orbit A t = P → t ≤ e.2 + 1
no_196_00 : ∀ t, ∀ e ∈ entries00, ¬ PalStartsL e.1 (orbit 196 t)
```
</details>

### PrefixBatch4K6

*101 further width-6 digit prefixes excluded from the orbit of 196*

Width-6 backward prefix certificates for 101 four-digit prefixes that were not yet excluded in the repository, built as one package with one shared rank tree (329,042 nodes), with ancestry bounds of at most 44 steps.

- Root module(s): `P196.PrefixBatch4K6.K6C000Final`
- 73 modules, 4 checked endpoints

### Agent124ForwardInvariant

*277 digit prefixes excluded from the orbit of 196 (forward invariant)*

An explicit list `excluded` of 277 digit prefixes: no iterate of 196, at any time, is a palindrome beginning with one of them (`no_196_excluded`). Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent124ForwardInvariant.A124W3Summary`
- 22 modules, 2 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
excluded_length : excluded.length = 277
no_196_excluded : ∀ T, ∀ w ∈ excluded, ¬ PalStartsL w (orbit 196 T)
```
</details>

### Agent119EightFamilies

*Eight palindrome families dd0…0dd never occur in the orbit of 196*

For d in {1,2,3,4,6,7,8,9} and every r, the palindrome dd 0^(2r) dd (= 11·d·(10^(2r+2)+1)) is never an iterate of 196 (`orbit196_ne_fam`; d = 5 is open). Also: the orbit of 196 is never divisible by 3 or by 99, is divisible by 11 from time 3 on, and its residues mod 99 from time 6 are 2^k·88 mod 99 — yet every such residue has a palindrome representative, so residues mod 99 alone cannot exclude palindromes. Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent119EightFamilies.EightFamilies`, `P196.Agent119EightFamilies.TemporalResidues`
- 6 modules, 85 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
orbit196_ne_fam (d r t : Nat) (hd : d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 ∨ d = 6 ∨ d = 7 ∨ d = 8 ∨ d = 9) : orbit 196 t ≠ fam d r
orbit196_never_dvd99 (k : Nat) : ¬ 99 ∣ orbit 196 k
orbit196_mod99_after_six (k : Nat) : orbit 196 (6 + k) % 99 = (2 ^ k * 88) % 99
phase_has_palindrome_representative (k : Nat) : ∃ p : Nat, 0 < p ∧ Palindrome p ∧ p % 99 = orbit 196 (6 + k) % 99
```
</details>

### Agent113FiveLayer

*Uniform five-layer obstruction*

If X has width at least five and its outer pair sums follow the stated pattern, no positive orbit reaches X at any time t >= 5; in particular no iterate of 196 has this full pattern (`no_196_full_pattern`, sharp via 10000 -> 80008 in four steps). Includes a generic four-column backward-layer certificate giving depth bounds. Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent113FiveLayer.FiveLayer`, `P196.Agent113FiveLayer.FourColumnChain`
- 101 modules, 28 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
five_layer (A X : Nat) (hA : 0 < A) (hX : FullPattern X) : ∀ t, 5 ≤ t → orbit A t ≠ X
no_196_full_pattern : ∀ t, ¬ FullPattern (orbit 196 t)
sharp_four : orbit 10000 4 = 80008 ∧ FullPattern 80008
Cert4.depth_bound (C : Cert4) (hC : C.Checked) : ∀ A t X, 0 < A → orbit A t = X → 4 ≤ width X → C.inLayer 0 (quad X) = true → t < C.h
```
</details>

### Agent117RemainingCycles

*Where the prefix-exclusion method stops: 14 cycle witnesses*

Method limits, not exclusions: for 14 three-digit prefixes (112, 138, 164, 198, 248, 275, 398, 626, 710, 716, 790, 911, 936, 952) the finite k-column backward abstraction contains a reachable cycle, so this finite-prefix method cannot give an ancestry bound for them; plus the projection lemma from k+1 to k columns. Unregistered before 2026-10-17; compiled and axiom-audited during consolidation, not independently reviewed.

- Root module(s): `P196.Agent117RemainingCycles.Projection`, `P196.Agent117RemainingCycles.Cycle112_k8`, `P196.Agent117RemainingCycles.Cycle138_k7`, `P196.Agent117RemainingCycles.Cycle164_k7`, `P196.Agent117RemainingCycles.Cycle198_k7`, `P196.Agent117RemainingCycles.Cycle248_k7`, `P196.Agent117RemainingCycles.Cycle275_k8`, `P196.Agent117RemainingCycles.Cycle398_k7`, `P196.Agent117RemainingCycles.Cycle626_k7`, `P196.Agent117RemainingCycles.Cycle710_k7`, `P196.Agent117RemainingCycles.Cycle716_k7`, `P196.Agent117RemainingCycles.Cycle790_k7`, `P196.Agent117RemainingCycles.Cycle911_k7`, `P196.Agent117RemainingCycles.Cycle936_k7`, `P196.Agent117RemainingCycles.Cycle952_k7`
- 20 modules, 106 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
forwardAdmitted_project {s p : List Nat} {x : Nat} (hx : x < 19) (h : ForwardAdmitted (s ++ [x]) p) : ForwardAdmitted s (p.take s.length)
cycle_ok : walkOK ((z, 0) :: cycle) = true
```
</details>

### ExactModulo99Periods

For every positive ordinary decimal seed and every absolute time t >= 6, the reverse-and-add orbit has the exact modulo-99 phase 11 * ((2^(t % 6) * 5 * n) % 9). Classifies point returns and all suffix periods by divisibility by the least positive period: one for n % 9 = 0, two for n % 9 != 0 and n % 3 = 0, and six otherwise. Equal-time eventual residues agree exactly when the positive seeds agree modulo nine. The seed 100 shows that the displayed phase formula cannot be extended uniformly to time five. This is a residue classification, not periodicity or merging of integer orbits, a per-seed first-entry classification, palindrome avoidance, or a conclusion settling whether 196 is a Lychrel number.

- Root module(s): `P196.ExactModulo99Periods.Main`
- 5 modules, 17 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
namespace Agent7.ResiduePeriods

open Lychrel196

theorem orbit_mod99_eq_phase99 (n t : Nat)
    (hn : 0 < n) (ht : 6 ≤ t) :
    orbit n t % 99 = phase99 n t

theorem orbit_mod99_shift_iff (n s P : Nat)
    (hn : 0 < n) (hs : 6 ≤ s) :
    (orbit n (s + P) % 99 = orbit n s % 99) ↔ residuePeriod n ∣ P

theorem orbit_mod99_seed_iff (n m t : Nat)
    (hn : 0 < n) (hm : 0 < m) (ht : 6 ≤ t) :
    (orbit n t % 99 = orbit m t % 99) ↔ n % 9 = m % 9

end Agent7.ResiduePeriods
```
</details>

## A conditional route to a Lychrel number

What a successful certificate would give. No certificate is known.

### CertificateToLychrel

*From a checked return certificate to a Lychrel number*

Conditional route: any Agent109 return certificate `cert` with `check cert = true` yields a natural number m whose entire ordinary decimal reverse-and-add orbit (time 0 included) contains no palindrome. Admissibility is derived automatically from the check. No such certificate is known; nothing here concerns 196 specifically.

- Root module(s): `P196.CertificateToLychrel.AdmissibleHeads`
- 4 modules, 3 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent112.Admissibility.certificate_existence_of_check : ∀ (cert : Agent109.Cert.Certificate),
  Agent109.Cert.check cert = true → ∃ m, ∀ (k : Nat), ¬Agent109.Palindrome (Agent109.orbit m k)
Agent112.Admissibility.automatic_admissibility : ∀ (cert : Agent109.Cert.Certificate),
  Agent109.Cert.check cert = true → ∃ H M, Agent109.Cert.Admissible0 cert H M
Agent112.Admissibility.no_bounded_width_orbit : ∀ (w : Agent109.Word),
  0 < Agent109.evalL w →
    ∀ (L : Nat),
      (∀ (k : Nat), Agent109.Bounded (Agent109.orbitWord w k)) →
        (∀ (k : Nat), List.length (Agent109.orbitWord w k) = L) → False
```
</details>

### Agent218CertificateAudit

*Exact threshold feasibility, template reframing, and a six-phase counterexample*

**LEAN-VERIFIED:** for fixed cyclic states and trimming counts, the original checker's lower-bound clauses are feasible exactly when each total band gain is nonnegative. Common-padding identities permit exact transitions that move band letters into finite blocks; a concrete local example cannot satisfy the old one-sided trim equation with the same representatives. A period-three local strip counterexample refutes direct extension of scalar predecessor erasure to six-phase bulk. **THEOREM (paper proof in `reports/REPORT_218.md`):** every accepted certificate in phase class `{6,12}` satisfies `2 * totalGam < P`; the common-cut argument excludes saturation for arbitrary finite block widths. The new combined obstruction endpoint is outside the compiled endpoint list. The report supplies complete carry bookkeeping, code and 1000-step checks. Global checker satisfiability remains unresolved; no accepted certificate or decimal Lychrel witness is supplied.

- Root modules: `P196.Agent218CertificateAudit.ThresholdFeasibility`, `P196.Agent218CertificateAudit.TemplateReframe`, `P196.Agent218CertificateAudit.SixPhaseCounterexample`
- 3 modules, 11 checked endpoints
- Report: [reports/REPORT_218.md](reports/REPORT_218.md)

### CertificateBounds208

*LEAN-VERIFIED: exact elimination of return-certificate lower-bound search*

For fixed original states and trimming counts, some reassignment of `lo` and `lo'` passes the unchanged Agent109 checker exactly when the structural phase/block equations hold and both total signed band gains are nonnegative. The construction computes a prefix-floor bound; the existing `Agent109.NoPal.not_stepPal` theorem supplies the redundant safety guard. Composing with the existing ordinary-integer bridge gives conditional decimal Lychrel existence directly from these reduced hypotheses. No structural cycle or accepted certificate instance is supplied.

- Root: `P196.CertificateBounds208.BoundSynthesis`
- New module count: 1; checked endpoints: 4.
- Endpoints: `Agent208.CertificateBounds.cyclic_bounds_iff`, `Agent208.CertificateBounds.synthesize_valid`, `Agent208.CertificateBounds.bounds_exist_iff`, `Agent208.CertificateBounds.structural_cycle_existence`.
- Report: [reports/REPORT_208.md](reports/REPORT_208.md).

### CertificateInterface208

*LEAN-VERIFIED: every accepted return certificate needs an interface of length at least 3*

The unchanged original checker rejects every certificate whose interface blocks remain of length at most 2. A decreasing finite rank covers all 3048 bounded short-interface states across the eight even phases, either terminal-carry bit, and every permitted trim. Exact LocalOK projection and cyclic rank descent remove every exterior-width, center-width, band-length, or period restriction. No exclusion of wider interfaces or accepted certificate instance is asserted.

- Root: `P196.CertificateInterface208.CertificateInterface`
- New module count: 3; checked endpoints: 5.
- Endpoints: `Agent208.Interface.rank_decreases`, `Agent208.Interface.local_rank_decreases`, `Agent208.Interface.valid_has_wide_interface`, `Agent208.Interface.checked_has_wide_interface`, `Agent208.Interface.short_interfaces_rejected`.
- Report: [reports/REPORT_208.md](reports/REPORT_208.md).

### Agent213KnownBaseMechanisms

*Known-base neutral certificates and selected center rigidity*

**LEAN-VERIFIED:** Explicit neutral-band certificates yield Lychrel template values for every gap at least four in bases 11, 17, 26, plus concrete seeds and existence theorems. Each cycle has two overflows and trimming gain three. Separate integer equations extracted from a specified four-phase center itinerary force base 26; their decimal specialization is contradictory. The complete carry reconstruction, exact itinerary hypotheses, source audit, Python checks, and base-20 source gap appear in [reports/REPORT_213.md](reports/REPORT_213.md). The itinerary-to-equations derivation is a paper proof; no decimal existence or universal decimal obstruction is asserted.

- Root modules: `P196.Agent213KnownBaseMechanisms.CenterRigidity`, `P196.Agent213KnownBaseMechanisms.KnownBases`.
- 2 new modules, 20 checked endpoints; imports the existing `A120Certificate` soundness theorem.
- Principal endpoints: `Agent213.center_rigidity`, `Agent213.center_base10_impossible`, `Agent213.KnownBases.lychrel11_template`, `Agent213.KnownBases.lychrel17_template`, `Agent213.KnownBases.lychrel26_template`, and the corresponding `exists_lychrel11`, `exists_lychrel17`, `exists_lychrel26`.

## One reverse-and-add step: predecessors, fibers, palindromic outputs

Exact structure of a single ordinary decimal step: who can map to a given number, how many, and when the output is a palindrome.

- **InverseFiberGrowth:** rational upper and lower exponential bounds for exact even folded coefficient-word fibers, including the explicit 144/89 and 233/144 rate sandwich (`P196.InverseFiberGrowth.FiberBounds`; 8 modules, 7 endpoints). These are coefficient-word counts, not ordinary-integer predecessor counts or infinite-orbit assertions.
- **FibonacciRateCriterion:** exact quadratic characterizations of the scaled Fibonacci bounds at every index; the upper criterion needs only indices `p*q` and `p*q+1`, and the lower criterion only the prefix through `p*q+1` (`P196.FibonacciRateCriterion.Upper`, `P196.FibonacciRateCriterion.Lower`; 4 modules, 4 endpoints). These are arithmetic rate criteria, with no additional integer-orbit or Lychrel claim.

**PalindromeRuns:** Exact criterion for a canonical positive seed to remain palindromic at times `0..k`: it is initially palindromic and every digit `d` satisfies `2^k * d <= 9`. Thus every positive orbit has at most four consecutive palindromes, every five-state window contains a nonpalindrome, and every interval of `N` states has at least `N / 5` nonpalindromes (integer division). The four-state bound is attained from `1` and after `10`; no asymptotically sharp density or infinite palindrome-avoidance claim is made. Root: `P196.PalindromeRuns.Windows`; 4 modules, 9 endpoints.

- `ResidualFivePredecessorCount` (`P196.ResidualFivePredecessorCount.Basic`): the executable duplicate-free `survivors r` lists exactly the members of the existing residual-five fiber having a positive ordinary predecessor of any width; `survivors 0 = [1661]` and `(survivors (r + 1)).length = P196.Agent9.InverseFibers.fib r`. Counts distinct target integers, not predecessor multiplicities; no exclusion from the orbit of 196, arbitrary inverse-depth bound, or infinite-time claim.
- `ResidualFivePredecessorMass` (`P196.ResidualFivePredecessorMass.Basic`): the duplicate-free `predecessors r` lists exactly the positive ordinary integers `m` with `step m` in the existing residual-five fiber, with no source-width restriction; its distinct-source count satisfies `A(0) = 7`, `A(1) = 0`, and `A(r + 2) = 10*A(r + 1) + 25*A(r)`. No completeness claim for that fiber among unrestricted predecessors of its associated middle integer, or claim about the orbit of 196, is made.
- `ResidualFivePredecessorDigitMass` (`P196.ResidualFivePredecessorDigitMass.Basic`): every member of the existing residual-five fiber has decimal digit sum `9*r + 14`; every positive ordinary predecessor has digit sum `9*r + 7` and exactly `r` outgoing carries in any canonical representation. General digit-split mass bridges and an exact complementary-middle scan invariant are included. No unrestricted-fiber identification, orbit-of-196, or arbitrary inverse-depth claim is made.

### Agent101AllWidthMaximum

Sharp maximum cardinality of complete positive ordinary-integer reverse-add predecessor fibers across all decimal input widths: 9 * 10 ^ (D / 2 - 1) for every target width D >= 2, and one for target width one; arbitrary duplicate-free predecessor-list upper bounds and explicit complete attaining fibers.

- Root module(s): `P196.Agent101AllWidthMaximum.Agent101AllWidthMaximum`
- 17 modules, 41 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent101.reverse_wrapDigits : ∀ (a b : Nat) (xs : List Nat),
  (Agent101.wrapDigits a b xs).reverse = Agent101.wrapDigits b a xs.reverse
Agent101.exists_coefficientWord_of_reverse : ∀ (q : List Nat), q.reverse = q → ∃ h c, q = Agent101.coefficientWord h c
Agent101.coefficientWord_half_length : ∀ (h : List Nat) (c : Option Nat),
  h.length = (Agent101.coefficientWord h c).length / 2
```
</details>

### Agent101DigitSplit

Complete canonical finite digit splitting and ordinary integer inverse fibers at a prescribed input width; exact multiplicity; complete all-width 887 example. No infinite-time claim.

- Root module(s): `P196.Agent101DigitSplit.Agent101NumericFibers`
- 5 modules, 11 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent101.mem_rawWords : ∀ (h : List Nat) (c : Option Nat) (ds : List Nat),
  ds ∈ Agent101.rawWords h c ↔
    ds.length = (Agent101.coefficientWord h c).length ∧
      Agent101.digitsBounded ds ∧ Agent101.digitPairSums ds = Agent101.coefficientWord h c
Agent101.mem_canonicalWords : ∀ (h : List Nat) (c : Option Nat) (ds : List Nat),
  ds ∈ Agent101.canonicalWords h c ↔
    Agent101.canonicalDigits ds ∧ Agent101.digitPairSums ds = Agent101.coefficientWord h c
Agent101.canonicalWords_nodup : ∀ (h : List Nat) (c : Option Nat), (Agent101.canonicalWords h c).Nodup
```
</details>

### Agent101NonpalindromicFibers

Complete initially palindromic and nonpalindromic sublists of every prescribed ordinary-integer profile fiber, including all invalid and zero boundaries. Initial time only.

- Root module(s): `P196.Agent101NonpalindromicFibers.Agent101NonpalindromicFibers`
- 7 modules, 28 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent101.palindrome_natValue_iff_reverse : ∀ (ds : List Nat),
  Agent101.canonicalDigits ds → (Lychrel196.Palindrome (Agent101.natValue ds) ↔ ds.reverse = ds)
Agent101.digitPairSums_of_reverse_eq : ∀ (ds : List Nat),
  ds.reverse = ds → Agent101.digitPairSums ds = List.map (fun d => d + d) ds
Agent101.even_digitPairSums_of_reverse_eq : ∀ (ds : List Nat),
  ds.reverse = ds → ∀ (s : Nat), s ∈ Agent101.digitPairSums ds → s % 2 = 0
```
</details>

### Agent101ProtectedFamily

Exact complete integer digit-split family for the specified Agent3 profiles:5*11^m members, exactly one initial palindrome,5*11^m-1 remaining positive fixed-width seeds, common explicit second ordinary iterate, and nonpalindromicity at every finite time0..k+1 for0<k. Does not exhaust every second preimage and does not assert an infinite orbit.

- Root module(s): `P196.Agent101ProtectedFamily.Agent101ProtectedFamily`
- 25 modules, 10 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent101.Protected.mem_protectedSeeds_numeric : ∀ (m k n : Nat),
  n ∈ Agent101.Protected.protectedSeeds m k ↔
    Agent101.decimalWidth n (2 * (m + k + 1)) ∧
      ∃ xs, xs.length = m ∧ Lychrel196.step n = Agent101.natValue (P196.Agent3.OverflowHorizon.inputWord xs k)
Agent101.Protected.protectedSeeds_nodup : ∀ (m k : Nat), (Agent101.Protected.protectedSeeds m k).Nodup
Agent101.Protected.length_protectedSeeds : ∀ (m k : Nat), (Agent101.Protected.protectedSeeds m k).length = 5 * 11 ^ m
```
</details>

### Agent105AllPredecessors

Executable complete duplicate-free list of all positive ordinary integer reverse-add predecessors of every Canonical target, with no source-width hypothesis. Includes computational half/center projection, exact decoded fixed-width fibers and two small kernel boundary controls. No finite backward-search instance or infinite-time result.

- Root module(s): `P196.Agent105AllPredecessors.Agent105Predecessors9df76b`, `P196.Agent105AllPredecessors.Agent105PredecessorControls9df76b`
- 15 modules, 18 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent105WordFiber9df76b.half : List Nat → List Nat
Agent105WordFiber9df76b.center : List Nat → Option Nat
Agent105WordFiber9df76b.wordFiber : List Nat → List Nat
```
</details>

### Agent105InverseBoundaries

One-step ordinary decimal reverse-add: different-width predecessor necessary conditions and at most two finite pair-sum profiles; exact positive palindrome-target image and width-at-least-two first-hit-one construction. No infinite-time result.

- Root module(s): `P196.Agent105InverseBoundaries.Agent105CrossWidth9df76b`, `P196.Agent105InverseBoundaries.Agent105CrossWidthWitness9df76b`, `P196.Agent105InverseBoundaries.Agent105PalindromeImage9df76b`
- 9 modules, 38 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
@Agent105WidthSupport9df76b.canonical_width_unique : ∀ {n L K : Nat} {d e : Nat → Nat},
  DecimalDigits.Canonical n d L → DecimalDigits.Canonical n e K → L = K
@Agent105WidthSupport9df76b.canonical_digits_unique : ∀ {n L : Nat} {d e : Nat → Nat},
  DecimalDigits.Canonical n d L → DecimalDigits.Canonical n e L → ∀ (i : Nat), i < L → d i = e i
@Agent105WidthSupport9df76b.canonical_width_and_digits_unique : ∀ {n L K : Nat} {d e : Nat → Nat},
  DecimalDigits.Canonical n d L → DecimalDigits.Canonical n e K → L = K ∧ ∀ (i : Nat), i < L → d i = e i
```
</details>

### Agent105NumericDecoder

Complete executable two-ended numerical target decoder at every prescribed source width, with full local/scan soundness and completeness, exact positive canonical ordinary-predecessor iff, and kernel boundary controls. No infinite-time result.

- Root module(s): `P196.Agent105NumericDecoder.Agent105NumericDecoder9df76b`, `P196.Agent105NumericDecoder.Agent105DecoderControls9df76b`
- 12 modules, 29 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
@Agent105DecoderLocal9df76b.validEdge_unique : ∀ {u v a b : Nat} {E F : Agent105DecoderLocal9df76b.Edge},
  Agent105DecoderLocal9df76b.ValidEdge u v a b E → Agent105DecoderLocal9df76b.ValidEdge u v a b F → E = F
@Agent105DecoderLocal9df76b.validCenter_unique : ∀ {u a b q r : Nat},
  Agent105DecoderLocal9df76b.ValidCenter u a b q → Agent105DecoderLocal9df76b.ValidCenter u a b r → q = r
@Agent105DecoderLocal9df76b.decodePair_sound : ∀ {u v a b : Nat} {E : Agent105DecoderLocal9df76b.Edge},
  Agent105DecoderLocal9df76b.decodePair u v a b = some E → Agent105DecoderLocal9df76b.ValidEdge u v a b E
```
</details>

### Agent2OverflowFibers

*Agent #2 exact canonical overflow-fiber maximum: scoped source closure*

For every input width L>=2, the complete canonical coefficient-word fiber of the literal Agent8.stepWord with actual final carry1 has size at most2^(L/2-1); the explicit 5/10 target attains the bound and its immediate normalization is nonpalindromic. Coefficient words only; no digit-splitting count or all-time claim.

- Root module(s): `P196.Agent2OverflowFibers.Agent2OverflowFibers`
- 7 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent2.OverflowFibers.actualOverflowPreimages_membership : ∀ (L : Nat) (target q : List Nat),
  q ∈ P196.Agent2.OverflowFibers.actualOverflowPreimages L target ↔
    P196.Agent2.OverflowFibers.ActualOverflowFiber L target q
P196.Agent2.OverflowFibers.actual_overflow_fiber_bound : ∀ (L : Nat) (target : List Nat) (qs : List (List Nat)),
  2 ≤ L →
    qs.Nodup →
      (∀ (q : List Nat), q ∈ qs → P196.Agent2.OverflowFibers.ActualOverflowFiber L target q) →
        qs.length ≤ 2 ^ (L / 2 - 1)
P196.Agent2.OverflowFibers.actualOverflowPreimages_sharp : ∀ (L : Nat),
  2 ≤ L →
    (P196.Agent2.OverflowFibers.actualOverflowPreimages L (P196.Agent2.OverflowFibers.sharpTarget (L - 2))).length =
      2 ^ (L / 2 - 1)
```
</details>

### Agent14CarryfreeSaturation

For every odd L>=5 all99classes and every even L>=2 all9classes, exact canonical nonpalindromic ordinary input, all actual carries zero, canonical palindromic next value at the same width, and literal finite Q(1)/2 mod9 and Q(-1)/2 mod11. Preserve L=5 central collision, negative Int half, and no even input divisibility claim. No overflow family, ideal, quotient classification, U/S or orbit theorem.

- Root module(s): `P196.Agent14CarryfreeSaturation.Agent14CarryfreeSaturation`
- 5 modules, 22 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent14.Carryfree.residue_parameters : ∀ (s r : Nat),
  s < 9 → r < 11 → ∃ u b, 1 ≤ u ∧ u ≤ 10 ∧ b ≤ 9 ∧ (u + b) % 9 = s ∧ (u + 10 * b) % 11 = r
Agent14.Carryfree.even_residue_parameters : ∀ (s : Nat), s < 9 → ∃ a, 1 ≤ a ∧ a ≤ 9 ∧ a % 9 = s
Agent14.Carryfree.odd_three_digit_mod99 : ∀ (L a b c : Nat),
  5 ≤ L → L % 2 = 1 → (a * 10 ^ (L - 1) + b * 10 ^ (L - 2) + c * 10 ^ (L - 3)) % 99 = (a + 10 * b + c) % 99
```
</details>

### Agent14SpectralInjectivity

Exact T/R recurrence domination and fixed-width injectivity on arbitrary symmetric Nat coefficient words bounded by 18; original canonical-decimal column-sum corollary. No real-root, input-integer injectivity, evolution, ideal, or 196-orbit claim.

- Root module(s): `P196.Agent14SpectralInjectivity.Agent14SpectralDecimal`
- 4 modules, 15 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent14.Spectral.T_recurrence_exact : ∀ (n : Nat),
  Agent14.Spectral.T (n + 2) + Agent14.Spectral.T n = 20 * Agent14.Spectral.T (n + 1)
Agent14.Spectral.R_recurrence_exact : ∀ (n : Nat),
  Agent14.Spectral.R (n + 2) + Agent14.Spectral.R n = 20 * Agent14.Spectral.R (n + 1)
Agent14.Spectral.oddWeight_dominates : ∀ (n : Nat),
  18 * Agent14.Spectral.prefixSum Agent14.Spectral.oddWeight n < Agent14.Spectral.oddWeight n
```
</details>

### Agent51OverflowSaturation

Exact source Theorem 3 overflow saturation, all L>=18 and all s<9, with actual positive canonical nonpalindromic integer input, carry=1, palindrome next step, exact widths, and literal Q(1)/2 mod9 and Q(-1)/2 mod11 coordinates.

- Root module(s): `P196.Agent51OverflowSaturation.Saturation`
- 5 modules, 52 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent51.witness_polynomialValue : ∀ (L k : Nat) (x : Int),
  2 * k ≤ L →
    P196.Agent51.polynomialValue (DecimalDigits.columnSum (P196.Agent51.inputDigit L k) L) L x =
      P196.Agent51.polynomialValue (P196.Agent51.pairWord L k) L x
P196.Agent51.witness_value_one : ∀ (L k : Nat),
  2 * k ≤ L → P196.Agent51.polynomialValue (DecimalDigits.columnSum (P196.Agent51.inputDigit L k) L) L 1 = 22 * ↑k
P196.Agent51.witness_value_neg_one : ∀ (L k : Nat),
  2 * k ≤ L →
    P196.Agent51.polynomialValue (DecimalDigits.columnSum (P196.Agent51.inputDigit L k) L) L (-1) =
      if L % 2 = 1 ∧ k % 2 = 1 then 22 else 0
```
</details>

### Agent51ReciprocalMoment

Exact reciprocal first moment and derivative redundancy modulo9, all fixed natural widths and arbitrary signed symmetric coefficients, with literal formal coefficient differentiation and unchanged natural polynomialValue bridge.

- Root module(s): `P196.Agent51ReciprocalMoment.ReciprocalMoment`
- 3 modules, 50 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent51.inputDigit : Nat → Nat → Nat → Nat
P196.Agent51.pairWord : Nat → Nat → Nat → Nat
P196.Agent51.inputDigit_bounded : ∀ (L k i : Nat), P196.Agent51.inputDigit L k i ≤ 9
```
</details>

### ZeroEndingPredecessorParity

For every positive canonical target Y ending in zero, the complete positive ordinary reverse-and-add predecessor fiber has odd cardinality exactly when Y / 2 is a palindrome. Decimal reversal pairs all nonfixed predecessors; the fixed-point sublist is exactly [Y / 2] or empty. All source widths are included. No infinite-orbit or 196-orbit conclusion.

- Root module(s): `P196.ZeroEndingPredecessorParity.Integration`
- 19 modules, 7 checked endpoints; main theorem: `ZeroEndingPredecessorParity.predecessor_count_parity`

### CompleteFiberParity

For every canonical decimal target Y, an explicit coefficient test computes the parity of its complete positive ordinary reverse-and-add predecessor count. Apply the existing numerical decoder at the only possible source widths W and W-1, then take the Boolean OR of the two profile tests. For arbitrary source widths L < K, a nonempty width-K fiber forces the complete width-L count to be divisible by eight, so both counts cannot be odd. The formula also holds for any duplicate-free list containing exactly the positive ordinary predecessors. No orbit, ancestry bound or Lychrel conclusion.

- Root module(s): `P196.CompleteFiberParity.Integration`
- 22 modules, 12 checked endpoints; main theorem: `CompleteFiberParity.complete_predecessor_parity`

<details><summary>Main statements (Lean)</summary>

```lean
CompleteFiberParity.complete_predecessor_parity (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : DecimalDigits.Canonical Y e W) :
    (Agent105Predecessors9df76b.predecessors e W).length % 2 =
      if CompleteFiberParity.oddDecoded e W W ||
        CompleteFiberParity.oddDecoded e W (W - 1) then 1 else 0

CompleteFiberParity.shorter_fiber_divisible_by_eight_of_longer_nonempty
    (Y : Nat) (e : Nat → Nat) (W L K : Nat)
    (htarget : DecimalDigits.Canonical Y e W) (hLK : L < K)
    (hlonger : Agent105DecodedFiber9df76b.decodedFiber e W K ≠ []) :
    8 ∣ (Agent105DecodedFiber9df76b.decodedFiber e W L).length
```
</details>

### MaximalDigitSplitFibers

*Exact maximum equality and sharp submaximum of fixed-width predecessor fibers*

The fixed-profile maximum is attained exactly by outer sum nine or ten, all inner sums nine, and a realizable center. **When there is at least one inner pair**, the sharp submaximum requires exactly one inner sum eight or ten instead. For every ordinary integer target and complete duplicate-free predecessor list at a prescribed source width L >= 4, any count below the maximum 9 * 10^(L/2-1) is at most 81 * 10^(L/2-2), with explicit complete fibers attaining this bound at every such width. With no inner pairs, the sharp profile submaximum is eight, also with complete numerical witnesses. Different source widths are not combined; no multi-step or infinite-orbit result is asserted.

- Root module(s): `P196.MaximalDigitSplitFibers.Main`
- 17 modules, 30 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
namespace Agent7.MaximalDigitSplitFibers

open Agent101 Lychrel196

theorem numericFiber_max_iff (s : Nat) (h : List Nat) (c : Option Nat) :
    (numericFiber (s :: h) c).length = 9 * 10 ^ h.length ↔
      (s = 9 ∨ s = 10) ∧ (∀ t ∈ h, t = 9) ∧ centerCount c = 1

theorem numericFiber_submax_iff (s : Nat) (h : List Nat) (c : Option Nat)
    (hlen : 0 < h.length) :
    (numericFiber (s :: h) c).length = 81 * 10 ^ (h.length - 1) ↔
      (s = 9 ∨ s = 10) ∧ singleInnerDefect h ∧ centerCount c = 1

theorem fixed_width_preimages_gap (Y L : Nat) (xs : List Nat)
    (hL : 4 ≤ L) (hxs : xs.Nodup)
    (hm : ∀ n, n ∈ xs ↔ decimalWidth n L ∧ step n = Y)
    (hne : xs.length ≠ 9 * 10 ^ (L / 2 - 1)) :
    xs.length ≤ 81 * 10 ^ (L / 2 - 2)

end Agent7.MaximalDigitSplitFibers
```
</details>

### EvenTargetPredecessorParity

For every positive canonical even decimal target Y, the complete positive ordinary reverse-and-add predecessor count is odd exactly when Y / 2 is a palindrome and Y has one digit or leading digit one. This closed form uses only the target's half, width and leading digit. The per-width theorem also retains membership of Y / 2 in the specified complete fiber, and the formula holds for every duplicate-free list containing exactly the positive ordinary predecessors. Supporting profile equivalences include invalid profiles; the source/target shape bridge does not require a palindromic source. No orbit, ancestry bound or Lychrel conclusion.

- Root module(s): `P196.EvenTargetPredecessorParity.Integration`
- 26 modules, 8 checked endpoints; main theorem: `EvenTargetPredecessorParity.even_target_predecessor_parity`

<details><summary>Main statements (Lean)</summary>

```lean
EvenTargetPredecessorParity.even_target_predecessor_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : DecimalDigits.Canonical Y e W) (heven : Y % 2 = 0) :
    (Agent105Predecessors9df76b.predecessors e W).length % 2 =
      if Lychrel196.Palindrome (Y / 2) ∧ (W = 1 ∨ e (W - 1) = 1)
      then 1 else 0

EvenTargetPredecessorParity.even_target_odd_decoded_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : DecimalDigits.Canonical Y e W) (heven : Y % 2 = 0) :
    CompleteFiberParity.oddDecoded e W L = true ↔
      (Y / 2 ∈ Agent105DecodedFiber9df76b.decodedFiber e W L) ∧
      Lychrel196.Palindrome (Y / 2) ∧ (W = 1 ∨ e (W - 1) = 1)
```
</details>

### OddTargetPredecessorParity

For every positive canonical odd decimal target Y of width W, choose source width L = W-1 exactly when Y begins with one and ends with nine, and choose L = W otherwise. Its complete positive ordinary reverse-and-add predecessor count is odd exactly when L is at least two and the shifted half (Y + 10^(L-1) + 1) / 2 is a palindrome. At any prescribed source width, the exact criterion requires width at least two and that palindrome to have that width and leading digit at most five; those numeric bounds follow automatically at the selected width. Both forms also apply to every duplicate-free list containing exactly the positive ordinary predecessors. The proof supplies an actual predecessor in the converse and covers widths zero and one. No orbit, ancestry bound or Lychrel conclusion.

- Root module(s): `P196.OddTargetPredecessorParity.Integration`
- 39 modules, 19 checked endpoints; main theorem: `OddTargetPredecessorParity.odd_target_predecessor_parity_simple`

<details><summary>Main statements (Lean)</summary>

```lean
OddTargetPredecessorParity.odd_target_predecessor_parity_simple
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : DecimalDigits.Canonical Y e W) (hodd : Y % 2 = 1) :
    (Agent105Predecessors9df76b.predecessors e W).length % 2 =
      if 2 ≤ OddTargetPredecessorParity.selectedWidth e W ∧
        Lychrel196.Palindrome (OddTargetPredecessorParity.shiftedHalf Y
          (OddTargetPredecessorParity.selectedWidth e W)) then 1 else 0

OddTargetPredecessorParity.odd_target_odd_decoded_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : DecimalDigits.Canonical Y e W) (hodd : Y % 2 = 1) :
    CompleteFiberParity.oddDecoded e W L = true ↔
      OddTargetPredecessorParity.candidateAccepts Y L
```
</details>

### OddPredecessorTargetCensus

An executable duplicate-free list contains exactly all positive decimal targets of width W with an odd complete ordinary reverse-and-add predecessor count. Every listed integer has the requested width. The counts are 0 at width zero, 4 at width one, 50 at width three, 10^(k+1) at every width 2*k+2, and 505*10^k at every width 2*k+5. The generator enumerates accepted symmetric coefficient profiles: from source width three onward their nonoverflow and overflow counts are respectively 45*10^((L-3)/2) and 55*10^((L-3)/2). Exact decoding and the existing cross-width divisibility result establish numerical uniqueness and complete ordinary semantics. No orbit, ancestry bound, asymptotic-density or Lychrel conclusion.

- Root module(s): `P196.OddPredecessorTargetCensus.Integration`
- 33 modules, 44 checked endpoints; main theorems: `OddPredecessorTargetCensus.mem_targets`, `OddPredecessorTargetCensus.length_targets_even`, `OddPredecessorTargetCensus.length_targets_odd`

<details><summary>Main statements (Lean)</summary>

```lean
OddPredecessorTargetCensus.targets_nodup (W : Nat) :
    (OddPredecessorTargetCensus.targets W).Nodup

OddPredecessorTargetCensus.mem_targets (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : DecimalDigits.Canonical Y e W) :
    Y ∈ OddPredecessorTargetCensus.targets W ↔
      (Agent105Predecessors9df76b.predecessors e W).length % 2 = 1

OddPredecessorTargetCensus.targets_have_width (W Y : Nat)
    (hY : Y ∈ OddPredecessorTargetCensus.targets W) :
    Agent101.decimalWidth Y W

OddPredecessorTargetCensus.length_targets_even (k : Nat) :
    (OddPredecessorTargetCensus.targets (2 * k + 2)).length = 10 ^ (k + 1)

OddPredecessorTargetCensus.length_targets_odd (k : Nat) :
    (OddPredecessorTargetCensus.targets (2 * k + 5)).length = 505 * 10 ^ k
```
</details>

### OddPredecessorTargetSparsity

Executable duplicate-free lists enumerate exactly the positive targets with odd complete ordinary reverse-and-add predecessor cardinality below every decimal power and every exclusive numerical cutoff. For the count S_W below 10^W, the exact cumulative identities are 9*S_(2*k+4)+29=1505*10^k and 9*S_(2*k+3)+29=605*10^k, with initial counts 0, 4, 14 and 64. The bound S_W^2 <= 5*10^W holds at all decimal powers, and integer constant four fails at width three. For the count A_N below an arbitrary cutoff N, A_N^2 <= 50*N and N >= 50*r^2 imply r*A_N <= N. A finite kernel certificate gives A_2000=124, ruling out constant five at arbitrary cutoffs. Constant fifty is not claimed optimal. No real-analysis limit API, orbit-frequency, ancestry or Lychrel conclusion.

- Root module(s): `P196.OddPredecessorTargetSparsity.Integration`
- 39 modules, 22 checked endpoints; main theorems: `OddPredecessorTargetSparsity.mem_below`, `OddPredecessorTargetSparsity.below_quadratic`, `OddPredecessorTargetSparsity.below_effectively_sparse`

<details><summary>Main statements (Lean)</summary>

```lean
OddPredecessorTargetSparsity.mem_below (Y : Nat) (e : Nat → Nat) (K N : Nat)
    (hY : DecimalDigits.Canonical Y e K) :
    Y ∈ OddPredecessorTargetSparsity.below N ↔
      Y < N ∧ (Agent105Predecessors9df76b.predecessors e K).length % 2 = 1

OddPredecessorTargetSparsity.belowPower_count_even (k : Nat) :
    9 * (OddPredecessorTargetSparsity.belowPower (2 * k + 4)).length + 29 = 1505 * 10 ^ k

OddPredecessorTargetSparsity.belowPower_count_odd (k : Nat) :
    9 * (OddPredecessorTargetSparsity.belowPower (2 * k + 3)).length + 29 = 605 * 10 ^ k

OddPredecessorTargetSparsity.belowPower_quadratic (W : Nat) :
    (OddPredecessorTargetSparsity.belowPower W).length ^ 2 ≤ 5 * 10 ^ W

OddPredecessorTargetSparsity.below_quadratic (N : Nat) :
    (OddPredecessorTargetSparsity.below N).length ^ 2 ≤ 50 * N

OddPredecessorTargetSparsity.below_effectively_sparse (r N : Nat)
    (hN : 50 * r ^ 2 ≤ N) :
    r * (OddPredecessorTargetSparsity.below N).length ≤ N

OddPredecessorTargetSparsity.below_two_thousand :
    (OddPredecessorTargetSparsity.below 2000).length = 124
```
</details>

### SharpOddTargetSparsity

Nine is the smallest natural-number constant in the uniform quadratic bound for the complete odd-predecessor target census. If A_N counts all positive ordinary reverse-and-add targets below the exclusive cutoff N whose complete predecessor cardinality is odd, then A_N^2 <= 9*N for every N. A kernel certificate gives A_200000=1269 and 1269^2>8*200000, proving that a natural-number constant c works at every cutoff exactly when c>=9. The explicit reciprocal-proportion threshold improves to N>=9*r^2. The proof uses the original coefficient families, their first one or two positional terms, finite leading-block inequalities at all ninety two-digit interval indices, and the existing exact cumulative counts. Sharpness is only among natural-number constants. No best real or rational constant, orbit-frequency, ancestry or Lychrel conclusion.

- Root module(s): `P196.SharpOddTargetSparsity.Integration`
- 45 modules, 21 checked endpoints; main theorems: `SharpOddTargetSparsity.below_quadratic_nine`, `SharpOddTargetSparsity.uniform_integer_constant_iff`, `SharpOddTargetSparsity.below_effectively_sparse_nine`

<details><summary>Main statements (Lean)</summary>

```lean
SharpOddTargetSparsity.below_quadratic_nine (N : Nat) :
    (OddPredecessorTargetSparsity.below N).length ^ 2 ≤ 9 * N

SharpOddTargetSparsity.below_two_hundred_thousand :
    (OddPredecessorTargetSparsity.below 200000).length = 1269

SharpOddTargetSparsity.below_quadratic_eight_fails :
    ¬ ∀ N : Nat, (OddPredecessorTargetSparsity.below N).length ^ 2 ≤ 8 * N

SharpOddTargetSparsity.uniform_integer_constant_iff (c : Nat) :
    (∀ N : Nat, (OddPredecessorTargetSparsity.below N).length ^ 2 ≤ c * N) ↔ 9 ≤ c

SharpOddTargetSparsity.below_effectively_sparse_nine (r N : Nat)
    (hN : 9 * r ^ 2 ≤ N) :
    r * (OddPredecessorTargetSparsity.below N).length ≤ N
```
</details>

### OrdinaryImageSparsity

An executable duplicate-free list contains exactly all ordinary reverse-and-add targets Y<N with a positive integer predecessor. If A_N is its length, then A_N^3 <= 900*N^2 for every natural cutoff N, and N>=900*r^3 implies r*A_N<=N. The proof evaluates the original shortWordsK coefficient words, removes numerical collisions, and uses their exact cumulative counts C_(2*k+1)+2=11*19^k and C_(2*k+2)+2=29*19^k. The intermediate bound is C_W^3<=9*10^(2*W). These statements cover the entire positive ordinary image. No optimal constant, exact distinct-target count formula, terminal-carry or overlap census, orbit-frequency estimate, ancestry bound, palindrome avoidance or Lychrel conclusion.

Requires the `SymmetricCarryCensus` result for the original profile census and the decimal cutoff bound in `OddPredecessorTargetSparsity`.

- Root module(s): `P196.OrdinaryImageSparsity.Integration`
- 51 modules, 17 checked endpoints; main theorems: `OrdinaryImageSparsity.mem_allBelow`, `OrdinaryImageSparsity.allBelow_cubic`, `OrdinaryImageSparsity.allBelow_effectively_sparse`

<details><summary>Main statements (Lean)</summary>

```lean
OrdinaryImageSparsity.allBelow_nodup (N : Nat) :
    (OrdinaryImageSparsity.allBelow N).Nodup

OrdinaryImageSparsity.mem_allBelow (Y N : Nat) :
    Y ∈ OrdinaryImageSparsity.allBelow N ↔
      Y < N ∧ ∃ n : Nat, 0 < n ∧ Lychrel196.step n = Y

OrdinaryImageSparsity.profileCount_odd (k : Nat) :
    OrdinaryImageSparsity.profileCount (2 * k + 1) + 2 = 11 * 19 ^ k

OrdinaryImageSparsity.profileCount_even (k : Nat) :
    OrdinaryImageSparsity.profileCount (2 * k + 2) + 2 = 29 * 19 ^ k

OrdinaryImageSparsity.profileCount_cubic (W : Nat) :
    OrdinaryImageSparsity.profileCount W ^ 3 ≤ 9 * 10 ^ (2 * W)

OrdinaryImageSparsity.allBelow_cubic (N : Nat) :
    (OrdinaryImageSparsity.allBelow N).length ^ 3 ≤ 900 * N ^ 2

OrdinaryImageSparsity.allBelow_effectively_sparse (r N : Nat)
    (hN : 900 * r ^ 3 ≤ N) :
    r * (OrdinaryImageSparsity.allBelow N).length ≤ N
```
</details>

### CrossWidthCollisionStates

For any two canonical positive sources of different widths with the same ordinary reverse-and-add target, the paired carry-difference trace is a closed walk from (11,2,2) in an explicit finite graph. Every state in the full index range 1<=i<=L lies in an eleven-element list, and six ordinary collision pairs with longer source width at most nine realize all eleven states. The second short/long coefficient pair is exactly one of (0,1), (9,0), (10,1), and (11,2), with global witnesses for each; consequently the common target ends in 01, 11, or 21. Existing adjacent-width, outer-coefficient and ordinary witness theorems are imported. No converse for arbitrary graph walks, exact overlap census, count recurrence, optimal witness-width bound, attainment of all states or coefficient pairs at each fixed width, orbit or Lychrel conclusion.

- Root module(s): `P196.CrossWidthCollisionStates.Classification`
- 12 modules, 22 checked endpoints; main theorems: `CrossWidthCollisionStates.cross_width_state_closed_walk`, `CrossWidthCollisionStates.state_realized_iff`, `CrossWidthCollisionStates.second_pair_realized_iff`, `CrossWidthCollisionStates.cross_width_output_mod100`

<details><summary>Main statements (Lean)</summary>

```lean
CrossWidthCollisionStates.productive_nodup :
    CrossWidthCollisionStates.productive.Nodup

CrossWidthCollisionStates.productive_length :
    CrossWidthCollisionStates.productive.length = 11

CrossWidthCollisionStates.cross_width_state_productive
    {n m L K i : Nat} {d e : Nat → Nat}
    (hn : DecimalDigits.Canonical n d L) (hm : DecimalDigits.Canonical m e K)
    (hLK : L < K) (hstep : Lychrel196.step n = Lychrel196.step m)
    (hi : 1 ≤ i) (hiL : i ≤ L) :
    CrossWidthCollisionStates.stateAt
      (DecimalDigits.columnSum d L) (DecimalDigits.columnSum e K) L i ∈
        CrossWidthCollisionStates.productive

CrossWidthCollisionStates.state_realized_iff (s : CrossWidthCollisionStates.State) :
    (∃ (n m L K i : Nat) (d e : Nat → Nat),
      DecimalDigits.Canonical n d L ∧ DecimalDigits.Canonical m e K ∧ L < K ∧
      Lychrel196.step n = Lychrel196.step m ∧ 1 ≤ i ∧ i ≤ L ∧
      CrossWidthCollisionStates.stateAt
        (DecimalDigits.columnSum d L) (DecimalDigits.columnSum e K) L i = s) ↔
    s ∈ CrossWidthCollisionStates.productive

CrossWidthCollisionStates.productive_realized_small
    (s : CrossWidthCollisionStates.State)
    (hs : s ∈ CrossWidthCollisionStates.productive) :
    ∃ (n m L K i : Nat) (d e : Nat → Nat),
      DecimalDigits.Canonical n d L ∧ DecimalDigits.Canonical m e K ∧ L < K ∧
      Lychrel196.step n = Lychrel196.step m ∧ 1 ≤ i ∧ i ≤ L ∧ K ≤ 9 ∧
      CrossWidthCollisionStates.stateAt
        (DecimalDigits.columnSum d L) (DecimalDigits.columnSum e K) L i = s

CrossWidthCollisionStates.second_pair_realized_iff (a b : Nat) :
    (∃ (n m L K : Nat) (d e : Nat → Nat),
      DecimalDigits.Canonical n d L ∧ DecimalDigits.Canonical m e K ∧ L < K ∧
      Lychrel196.step n = Lychrel196.step m ∧
      DecimalDigits.columnSum d L 1 = a ∧ DecimalDigits.columnSum e K 1 = b) ↔
    (a, b) ∈ CrossWidthCollisionStates.secondPairs

CrossWidthCollisionStates.cross_width_output_mod100
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : DecimalDigits.Canonical n d L) (hm : DecimalDigits.Canonical m e K)
    (hLK : L < K) (hstep : Lychrel196.step n = Lychrel196.step m) :
    Lychrel196.step n % 100 = 1 ∨
      Lychrel196.step n % 100 = 11 ∨ Lychrel196.step n % 100 = 21
```
</details>

### CrossWidthCollisionPaths

Reflected closed paths in the collision graph arise from canonical ordinary sources of widths L and L+1 exactly when both reconstructed coefficient words have even self-reflected centers. Closed paths already reconstruct bounded symmetric words with equal positional values and exactly the supplied carry states; the center conditions make them admissible decimal digit-pair words. Their pathValue is the actual common reverse-and-add output, and at a fixed L it determines the entire finite trace 1<=i<=L. Two explicit closed paths show that the shorter and longer center requirements cannot be omitted. No uniqueness of original source digit splits or off-window path values, unrestricted-walk realization, folded-path enumeration, exact overlap census, counting recurrence, orbit or Lychrel conclusion.

Requires the StateSpace and ActualTrace modules of `CrossWidthCollisionStates`.

- Root module(s): `P196.CrossWidthCollisionPaths.Obstructions`
- 14 modules, 21 checked endpoints; main theorems: `CrossWidthCollisionPaths.valid_iff_realized`, `CrossWidthCollisionPaths.pathValue_eq_step`, `CrossWidthCollisionPaths.pathValue_eq_iff`

<details><summary>Main statements (Lean)</summary>

```lean
CrossWidthCollisionPaths.valid_iff_realized
    (L : Nat) (f : Nat → CrossWidthCollisionStates.State) :
    CrossWidthCollisionPaths.Valid L f ↔
      ∃ (n m : Nat) (d e : Nat → Nat),
        DecimalDigits.Canonical n d L ∧ DecimalDigits.Canonical m e (L + 1) ∧
        Lychrel196.step n = Lychrel196.step m ∧
        ∀ i, 1 ≤ i → i ≤ L →
          CrossWidthCollisionStates.stateAt
            (DecimalDigits.columnSum d L) (DecimalDigits.columnSum e (L + 1)) L i = f i

CrossWidthCollisionPaths.closed_values_equal
    {L : Nat} {f : Nat → CrossWidthCollisionStates.State}
    (h : CrossWidthCollisionPaths.Closed L f) :
    DecimalDigits.value (CrossWidthCollisionPaths.shortWord f) L =
      DecimalDigits.value (CrossWidthCollisionPaths.longWord L f) (L + 1)

CrossWidthCollisionPaths.closed_trace_recovered
    {L : Nat} {f : Nat → CrossWidthCollisionStates.State}
    (h : CrossWidthCollisionPaths.Closed L f) :
    ∀ i, 1 ≤ i → i ≤ L →
      CrossWidthCollisionStates.stateAt
        (CrossWidthCollisionPaths.shortWord f)
        (CrossWidthCollisionPaths.longWord L f) L i = f i

CrossWidthCollisionPaths.pathValue_eq_iff
    {L : Nat} {f g : Nat → CrossWidthCollisionStates.State}
    (hf : CrossWidthCollisionPaths.Valid L f)
    (hg : CrossWidthCollisionPaths.Valid L g) :
    CrossWidthCollisionPaths.pathValue L f = CrossWidthCollisionPaths.pathValue L g ↔
      ∀ i, 1 ≤ i → i ≤ L → f i = g i

CrossWidthCollisionPaths.short_center_obstruction :
    CrossWidthCollisionPaths.Closed 3 CrossWidthCollisionPaths.shortCenterPath ∧
      ¬ CrossWidthCollisionPaths.Valid 3 CrossWidthCollisionPaths.shortCenterPath

CrossWidthCollisionPaths.long_center_obstruction :
    CrossWidthCollisionPaths.Closed 4 CrossWidthCollisionPaths.longCenterPath ∧
      ¬ CrossWidthCollisionPaths.Valid 4 CrossWidthCollisionPaths.longCenterPath
```
</details>

### FoldedCollisionPrefixes

Finite tuples containing the independent half of the collision trace uniquely parametrize ordinary common reverse-and-add targets at each specified pair of adjacent source widths. Shorter widths 2*k+2 use k+1 states and an even coefficient on the central reflected edge; shorter widths 2*k+3 use k+2 states with a reflection-fixed, even central state. These acceptance conditions are exactly full-trace validity. Extraction and reflection give exact finite-tuple and active-interval round trips, and the existing full-path realization and value-injectivity theorems give ordinary target surjectivity and tuple-value injectivity. Every edge reverses under reflection. Odd terminal successors are always unique; on the productive catalogue their existence is exactly the even terminal condition, with an explicit extension state. No target enumeration, cardinality formula, cross-width count equality, recurrence, source digit-split uniqueness, off-window function equality, orbit or Lychrel conclusion.

Requires the Realization closure of `CrossWidthCollisionPaths`.

- Root module(s): `P196.FoldedCollisionPrefixes.Targets`
- 18 modules, 38 checked endpoints; main theorems: `FoldedCollisionPrefixes.even_valid_iff`, `FoldedCollisionPrefixes.odd_valid_iff`, `FoldedCollisionPrefixes.even_targets_iff`, `FoldedCollisionPrefixes.odd_targets_iff`, `FoldedCollisionPrefixes.even_value_eq_iff`, `FoldedCollisionPrefixes.odd_value_eq_iff`

<details><summary>Main statements (Lean)</summary>

```lean
FoldedCollisionPrefixes.even_valid_iff
    (k : Nat) (p : FoldedCollisionPrefixes.Prefix k) :
    FoldedCollisionPrefixes.EvenAccepted k p ↔
      CrossWidthCollisionPaths.Valid (2 * k + 2)
        (FoldedCollisionPrefixes.evenTrace k p)

FoldedCollisionPrefixes.odd_valid_iff
    (k : Nat) (p : FoldedCollisionPrefixes.Prefix (k + 1)) :
    FoldedCollisionPrefixes.OddAccepted k p ↔
      CrossWidthCollisionPaths.Valid (2 * k + 3)
        (FoldedCollisionPrefixes.oddTrace k p)

FoldedCollisionPrefixes.even_targets_iff (k Y : Nat) :
    FoldedCollisionPrefixes.CommonTarget (2 * k + 2) Y ↔
      ∃ p : FoldedCollisionPrefixes.Prefix k,
        FoldedCollisionPrefixes.EvenAccepted k p ∧
        FoldedCollisionPrefixes.evenValue k p = Y

FoldedCollisionPrefixes.odd_targets_iff (k Y : Nat) :
    FoldedCollisionPrefixes.CommonTarget (2 * k + 3) Y ↔
      ∃ p : FoldedCollisionPrefixes.Prefix (k + 1),
        FoldedCollisionPrefixes.OddAccepted k p ∧
        FoldedCollisionPrefixes.oddValue k p = Y

FoldedCollisionPrefixes.even_value_eq_iff
    {k : Nat} {p q : FoldedCollisionPrefixes.Prefix k}
    (hp : FoldedCollisionPrefixes.EvenAccepted k p)
    (hq : FoldedCollisionPrefixes.EvenAccepted k q) :
    FoldedCollisionPrefixes.evenValue k p =
      FoldedCollisionPrefixes.evenValue k q ↔ p = q

FoldedCollisionPrefixes.odd_value_eq_iff
    {k : Nat} {p q : FoldedCollisionPrefixes.Prefix (k + 1)}
    (hp : FoldedCollisionPrefixes.OddAccepted k p)
    (hq : FoldedCollisionPrefixes.OddAccepted k q) :
    FoldedCollisionPrefixes.oddValue k p =
      FoldedCollisionPrefixes.oddValue k q ↔ p = q

FoldedCollisionPrefixes.productive_terminal_extension_iff
    {s t : CrossWidthCollisionStates.State}
    (hs : s ∈ CrossWidthCollisionStates.productive) :
    (CrossWidthCollisionStates.Edge s t ∧ FoldedCollisionPrefixes.OddTerminal t) ↔
      (FoldedCollisionPrefixes.EvenTerminal s ∧
        t = FoldedCollisionPrefixes.terminalExtension s)
```
</details>

### CrossWidthTargetCensus

An executable duplicate-free census lists exactly the ordinary reverse-and-add outputs shared by canonical sources of widths L and L+1, for every natural L. The lists are empty at shorter widths zero and one. Productive finite-walk enumeration and the existing terminal test give exactly the accepted even prefixes. Explicit terminal extension and truncation pair these prefixes bijectively with the accepted odd prefixes; the existing target-value injectivity then gives equally many distinct outputs at shorter widths 2*k+2 and 2*k+3. Kernel-checked counts for L = 0,...,7 are 0,0,1,1,2,2,7,7, with exact first nonempty lists [121] and [1111]. No recurrence, closed cardinality formula, asymptotic estimate, source digit-split uniqueness, orbit or Lychrel conclusion.

Requires `FoldedCollisionPrefixes.Targets` and the existing generic finite-product Nodup theorem from `Agent9FiniteProducts`.

- Root module(s): `P196.CrossWidthTargetCensus.Census`
- 24 modules, 46 checked endpoints; main theorems: `CrossWidthTargetCensus.mem_targets`, `CrossWidthTargetCensus.targets_nodup`, `CrossWidthTargetCensus.targets_paired_length`, `CrossWidthTargetCensus.small_target_counts`

<details><summary>Main statements (Lean)</summary>

```lean
CrossWidthTargetCensus.mem_targets (L Y : Nat) :
    Y ∈ CrossWidthTargetCensus.targets L ↔
      FoldedCollisionPrefixes.CommonTarget L Y

CrossWidthTargetCensus.targets_nodup (L : Nat) :
    (CrossWidthTargetCensus.targets L).Nodup

CrossWidthTargetCensus.targets_paired_length (k : Nat) :
    (CrossWidthTargetCensus.targets (2 * k + 2)).length =
      (CrossWidthTargetCensus.targets (2 * k + 3)).length

CrossWidthTargetCensus.small_target_counts :
    (List.range 8).map (fun L => (CrossWidthTargetCensus.targets L).length) =
      [0, 0, 1, 1, 2, 2, 7, 7]

CrossWidthTargetCensus.targets_two :
    CrossWidthTargetCensus.targets 2 = [121]

CrossWidthTargetCensus.targets_three :
    CrossWidthTargetCensus.targets 3 = [1111]

CrossWidthTargetCensus.extendEven_accepted
    {k : Nat} {p : FoldedCollisionPrefixes.Prefix k}
    (h : FoldedCollisionPrefixes.EvenAccepted k p) :
    FoldedCollisionPrefixes.OddAccepted k (CrossWidthTargetCensus.extendEven p)

CrossWidthTargetCensus.extendEven_truncate
    {k : Nat} {p : FoldedCollisionPrefixes.Prefix (k + 1)}
    (h : FoldedCollisionPrefixes.OddAccepted k p) :
    CrossWidthTargetCensus.extendEven (CrossWidthTargetCensus.truncatePrefix p) = p
```
</details>

### CrossWidthTargetRecurrence

For C_L equal to the number of distinct ordinary reverse-and-add outputs shared by canonical sources of widths L and L+1, the exact recurrence C_(L+6)=2*C_(L+4)+3*C_(L+2)+C_L holds for every natural L, including zero and one. A kernel-checked cubic identity on the existing productive collision states is transported through a weighted fold of the unchanged walk enumeration; the terminal indicator counts exactly the existing target list. The executable three-count window starts at (1,2,7) and updates (a,b,c) to (b,c,2*c+3*b+a). Every component matches its census count, and the all-width arithmetic evaluator agrees exactly with the duplicate-free target-list length. The first nine even-family counts are 1,2,7,21,65,200,616,1897,5842. No asymptotic growth, generating-function formalism, minimal recurrence order, optimal complexity, source digit-split uniqueness, orbit or Lychrel conclusion.

Requires the complete `CrossWidthTargetCensus.Census` closure and Lean Core list algebra.

- Root module(s): `P196.CrossWidthTargetRecurrence.Evaluator`
- 29 modules, 15 checked endpoints; main theorems: `CrossWidthTargetRecurrence.weightedWalks_succ`, `CrossWidthTargetRecurrence.transfer_cubic`, `CrossWidthTargetRecurrence.target_count_recurrence`, `CrossWidthTargetRecurrence.countWindow_eq_lengths`, `CrossWidthTargetRecurrence.targetCount_eq_length`

<details><summary>Main statements (Lean)</summary>

```lean
CrossWidthTargetRecurrence.target_count_recurrence (L : Nat) :
    (CrossWidthTargetCensus.targets (L + 6)).length =
      2 * (CrossWidthTargetCensus.targets (L + 4)).length +
      3 * (CrossWidthTargetCensus.targets (L + 2)).length +
      (CrossWidthTargetCensus.targets L).length

CrossWidthTargetRecurrence.countWindow_eq_lengths (k : Nat) :
    CrossWidthTargetRecurrence.countWindow k =
      ((CrossWidthTargetCensus.targets (2 * k + 2)).length,
       (CrossWidthTargetCensus.targets (2 * (k + 1) + 2)).length,
       (CrossWidthTargetCensus.targets (2 * (k + 2) + 2)).length)

CrossWidthTargetRecurrence.targetCount_eq_length (L : Nat) :
    CrossWidthTargetRecurrence.targetCount L =
      (CrossWidthTargetCensus.targets L).length

CrossWidthTargetRecurrence.small_countWindow :
    (List.range 9).map (fun k => (CrossWidthTargetRecurrence.countWindow k).1) =
      [1, 2, 7, 21, 65, 200, 616, 1897, 5842]
```
</details>

### OrdinaryImageCensus

An executable duplicate-free slice of the existing allBelow list contains exactly every ordinary reverse-and-add output of decimal width W with a positive predecessor. Write M_W for its length and J_L for the existing adjacent-source-width overlap count. The exact formulas are M_0=0, M_1=4, 2*M_(2*k+2)+2*J_(2*k+1)=27*19^k+1, and 2*M_(2*k+3)+2*J_(2*k+2)+1=189*19^k. The proof identifies the output-width census with the union of the original same-width carry-zero values and preceding-width carry-one values, with intersection exactly the unchanged common-target census. It reuses the original profile and terminal-carry counts. The arithmetic imageCount evaluator equals the complete numerical list length at every width; its first nine values are 0,4,14,93,256,1793,4872,34107,92590. No exact cumulative or arbitrary-cutoff formula, optimal density constant, asymptotic growth, optimal complexity, orbit or Lychrel conclusion.

Requires `SymmetricCarryCensus.Counts`, `TerminalCarryCensus.Terminal`, `OrdinaryImageSparsity.Enumeration`, `CrossWidthTargetRecurrence.Evaluator`, and the existing canonical width interfaces. The two original coefficient-count results retain their separate source ownership.

- Root module(s): `P196.OrdinaryImageCensus.Evaluator`
- 53 modules, 18 checked endpoints; main theorems: `OrdinaryImageCensus.mem_widthTargets`, `OrdinaryImageCensus.count_balance`, `OrdinaryImageCensus.count_even`, `OrdinaryImageCensus.count_odd`, `OrdinaryImageCensus.imageCount_eq_length`

<details><summary>Main statements (Lean)</summary>

```lean
OrdinaryImageCensus.mem_widthTargets (W Y : Nat) :
    Y ∈ OrdinaryImageCensus.widthTargets W ↔
      Agent101.decimalWidth Y W ∧
        ∃ n : Nat, 0 < n ∧ Lychrel196.step n = Y

OrdinaryImageCensus.count_even (k : Nat) :
    2 * (OrdinaryImageCensus.widthTargets (2 * k + 2)).length +
      2 * CrossWidthTargetRecurrence.targetCount (2 * k + 1) = 27 * 19 ^ k + 1

OrdinaryImageCensus.count_odd (k : Nat) :
    2 * (OrdinaryImageCensus.widthTargets (2 * k + 3)).length +
      2 * CrossWidthTargetRecurrence.targetCount (2 * k + 2) + 1 = 189 * 19 ^ k

OrdinaryImageCensus.imageCount_eq_length (W : Nat) :
    OrdinaryImageCensus.imageCount W = (OrdinaryImageCensus.widthTargets W).length

OrdinaryImageCensus.small_imageCount :
    (List.range 9).map OrdinaryImageCensus.imageCount =
      [0, 4, 14, 93, 256, 1793, 4872, 34107, 92590]
```
</details>

## Carries: what carry sequences reveal and how they evolve

Carry observability, carry accounting and exterior coordinates over finitely many steps.

- **SymmetricCarryCensus**: the original `symWords L` list contains every admissible symmetric coefficient word exactly once; its size is zero at width zero, nine at width one, and `18 * 19^(L/2-1)` times an odd-width factor ten otherwise. A whole-word complement involution proves that each actual carry bit occurs exactly `9 * 19^(L/2-1)` times that factor at every strictly internal position `0 < j < L`; the checked pair `[9,18,9]` and `[10,0,10]` shows terminal carries need not complement (`P196.SymmetricCarryCensus.Census`, 16 modules, 6 endpoints). Counts are unweighted coefficient words; no integer multiplicity, joint-path realization, fixed-seed reachability or palindrome avoidance is claimed.

- **TerminalCarryCensus**: the original `symWords` enumeration has exactly `(19^m - 1)/2` terminal-one words at width `2*m` and `5*19^m` at width `2*m+1`, including widths zero and one. A finite complementary-scan theorem isolates the all-nine exception; a complement involution on the existing half-word products gives the count, and terminal carry one forces the positive exterior needed to transfer it to the original enumeration (`P196.TerminalCarryCensus.Terminal`, 18 modules, 3 endpoints). Counts are unweighted coefficient words; no integer multiplicity, target-fiber count, trajectory frequency, joint-path realization or palindrome avoidance is claimed.

- **MirroredCarryCensus**: for `0 < j <= m`, the original `symWords` enumeration has exact joint counts at mirrored internal carry positions. At even width `2*m`, each equal-bit pair occurs `(A+E)/2` times and each unequal-bit pair `(A-E)/2` times, where `A=9*19^(m-1)` and `E=9*19^(j-1)`; at odd width `2*m+1`, each of the four pairs occurs `45*19^(m-1)` times. Complementing only the middle preserves the left carry and pairs the right carry except on an all-nine middle, whose count follows by insertion and deletion. The even boundary `j=m` is included (`P196.MirroredCarryCensus.Census`, 22 modules, 3 endpoints). Counts are unweighted coefficient words; no full carry-word independence, integer multiplicity, target-fiber count, trajectory frequency, joint-path realization or palindrome avoidance is claimed.

- **CommonOverflowRigidity:** At every shared width, symmetric coefficient words bounded by eighteen with common first overflow agree at every index below that width if their normalized digit differences are antisymmetric at both consecutive normalizations (`P196.CommonOverflowRigidity.Main`). The second terminal carries are derived to agree; positivity and center parity are unnecessary. Canonical initial numerals then have equal first reverse-and-add outputs. The original digit split need not agree, and no other defect-pattern or infinite-orbit exclusion, palindrome-avoidance result, or 196 conclusion is claimed.

- **LowDigitSumTermination:** Every positive integer with decimal digit sum at most 9 reaches a palindrome in 1–3 steps (`LowDigitSumTermination.palindrome_within_three_of_digitSum_le_nine`); 180 attains time 3, while digit-sum-10 input 190 first hits at time 7. Every iterate of a hypothetical Lychrel seed therefore has digit sum at least 10. No existence or 196 conclusion. Root: `P196.LowDigitSumTermination.Main`; 4 modules, 8 checked endpoints.

- **DigitSumTenTermination:** Every positive integer with decimal digit sum at most 10 reaches a palindrome in 1–4 steps except for 190, whose first hit at 7 makes the uniform seven-step bound sharp. Input 280 attains the four-step bound away from 190; digit-sum-11 input 20900 first hits at 12. Every iterate of a hypothetical Lychrel seed therefore has digit sum at least 11. No existence or 196 conclusion. Root: `P196.DigitSumTenTermination.Main`; 8 modules, 10 checked endpoints.

- **DigitSumElevenClassification:** Every positive integer with decimal digit sum at most 11 reaches a palindrome in 1–12 steps except `100090001` and `200090000`, exactly the two positive-time exceptions through time 12. Their positive orbits agree; the first is palindromic at time zero, and the second has no positive reverse-and-add predecessor. Every positive-time term of a hypothetical Lychrel orbit therefore has digit sum at least 12. The imported `20900` control makes twelve sharp outside the exceptions. No infinite avoidance, existence, or 196 conclusion. Root: `P196.DigitSumElevenClassification.Main`; 19 modules, 20 checked endpoints.

- **CommonOverflowGap:** At equal initial canonical width, common first-step terminal carry one and an antisymmetric normalized old-width digit difference imply `step (step n) + 9 * step n = step (step m) + 9 * step m`; hence strict order reversal and exact ninefold gap scaling, without requiring equal second-output widths (`P196.CommonOverflowGap.Numeric`). Includes a structural value identity and the existing canonical witness; no repeated-overflow, infinite-orbit or 196 conclusion.

- **CarryCountGrowth**: every positive ordinary decimal orbit has arbitrarily large outgoing carry counts after every starting time, with an explicit window from the current actual width; the count includes the terminal carry (`P196.CarryCountGrowth.CarryCountGrowth`, 3 modules, 12 endpoints). This includes the continued orbit of 196 and does not establish palindrome avoidance, carry density or convergence to infinity.

- **CarryCountDecoding**: the first `Nat.log2 L + 6` total outgoing carry counts recover the initial digit sum of every positive seed of decimal width at most `L`, via an exact powers-of-two weighted decoder; equal finite histories allow different initial widths, and complete carry-count histories are equivalent to complete digit-sum histories (`P196.CarryCountDecoding.CarryCountDecoding`, 4 modules, 9 endpoints). Ordinary iteration continues after palindromes; no initial-integer reconstruction, optimal horizon or palindrome avoidance is claimed.

- **UniformCarryWindows**: a width-independent weighted carry budget implies that twelve consecutive total outgoing carry counts at most `B` force initial digit sum at most `11*B`; every positive orbit has a count greater than `B` in each half-open window of length `H = sharpDigitSumEscapeBound (11*B) + 12`, and every interval of length `N` contains at least `N/H` such times (`P196.UniformCarryWindows.UniformEscape`, 16 modules, 9 endpoints). Terminal carries are included and ordinary iteration continues after palindromes; no optimal bound, density-limit existence, convergence of every carry count or palindrome avoidance is claimed.

- **AdaptiveCarryDecoding**: the maximum `B` of the first twelve total outgoing carry counts determines a sufficient total observation length `9 * (Nat.log2 (11*B) + 2)` without an initial-width bound; a chronological list decoder returns the exact initial digit sum for every positive actual seed once that many observations arrive, with an explicit finite termination theorem and a nine-step growth bound (`P196.AdaptiveCarryDecoding.Decoder`, 18 modules, 4 endpoints). Terminal carries are included and ordinary iteration continues after palindromes; no arbitrary-list realizability test, initial-integer reconstruction, optimal horizon or palindrome avoidance is claimed.

- **SparseProfileGrowth**: every positive coefficient after `t` actual nonsymmetric profile steps has a positive initial origin within distance `t`; a finite neighborhood mass bound and the exact integer bridge imply `digitSum (orbit n t) ≤ 18*(2*t+1)*digitSum n` for all seeds and times, including zero, independently of the initial width (`P196.SparseProfileGrowth.NumericGrowth`, 12 modules, 5 endpoints). Ordinary iteration continues after palindromes; no optimal bound, exact support equality, digit-sum monotonicity, positive lower growth rate or palindrome avoidance is claimed.

### Agent10CarryObservability

Scoped carry-observability results for unchanged ordinary decimal dynamics: at least three nonoverflows among seven actual transitions at every admissible width; eight complete carry words reconstruct all pair sums under a difference bound of five or initial nonoverflow and hence determine the next integer at shared canonical width; eight words always reconstruct the exterior pair sum; explicit canonical integers show that six words do not determine pair sums or the next integer. No arbitrary-width full eight-word reconstruction or P196 conclusion.

- Root module(s): `P196.Agent10CarryObservability.Agent10PrefixExclusion`, `P196.Agent10CarryObservability.Agent10SixCarryCounterexample`
- 11 modules, 49 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent10SmoothingBoundary.prefix_rigidity : ∀ (a0 a1 a2 a3 a4 a5 a6 : Int),
  -5 ≤ a1 ∧ a1 ≤ 5 →
    -5 ≤ a2 ∧ a2 ≤ 5 →
      -5 ≤ a3 ∧ a3 ≤ 5 →
        -5 ≤ a4 ∧ a4 ≤ 5 →
          -5 ≤ a5 ∧ a5 ≤ 5 →
            -5 ≤ a6 ∧ a6 ≤ 5 →
              -1 ≤ a0 ∧ a0 ≤ 1 →
                -1 ≤ a1 + 4 * a0 ∧ a1 + 4 * a0 ≤ 1 →
                  -1 ≤ a2 + 4 * a1 + 6 * a0 ∧ a2 + 4 * a1 + 6 * a0 ≤ 1 →
                    -1 ≤ a3 + 4 * a2 + 6 * a1 + 4 * a0 ∧ a3 + 4 * a2 + 6 * a1 + 4 * a0 ≤ 1 →
                      -1 ≤ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ∧ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ≤ 1 →
                        -1 ≤ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ∧ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ≤ 1 →
                          -1 ≤ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ∧ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ≤ 1 → a0 = 0
Agent10SmoothingBoundary.four_rigidity_at_five : ∀ (f : Agent10SmoothingBoundary.Series),
  (∀ (i : Nat), -5 ≤ f i ∧ f i ≤ 5) →
    (∀ (i : Nat), -1 ≤ Agent10SmoothingBoundary.four f i ∧ Agent10SmoothingBoundary.four f i ≤ 1) → ∀ (i : Nat), f i = 0
Agent10SmoothingBoundary.witness_zero_after : ∀ (i : Nat), 11 ≤ i → Agent10SmoothingBoundary.witness i = 0
```
</details>

### Agent10EightCarry

Every admissible width has at least three nonoverflows in seven actual transitions. Eight complete carry observations determine pair sums when the initial difference is bounded by five; initial nonoverflow implies this bound. Numeric consequence: equality of the next ordinary reverse-and-add integer at shared canonical initial width. Inherited sharp four-smoothing boundary is retained. No universal eight-word reconstruction, initial-integer injectivity, or palindrome-avoidance conclusion.

- Root module(s): `P196.Agent10EightCarry.Agent10EightCarry`
- 8 modules, 26 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent10SmoothingBoundary.prefix_rigidity : ∀ (a0 a1 a2 a3 a4 a5 a6 : Int),
  -5 ≤ a1 ∧ a1 ≤ 5 →
    -5 ≤ a2 ∧ a2 ≤ 5 →
      -5 ≤ a3 ∧ a3 ≤ 5 →
        -5 ≤ a4 ∧ a4 ≤ 5 →
          -5 ≤ a5 ∧ a5 ≤ 5 →
            -5 ≤ a6 ∧ a6 ≤ 5 →
              -1 ≤ a0 ∧ a0 ≤ 1 →
                -1 ≤ a1 + 4 * a0 ∧ a1 + 4 * a0 ≤ 1 →
                  -1 ≤ a2 + 4 * a1 + 6 * a0 ∧ a2 + 4 * a1 + 6 * a0 ≤ 1 →
                    -1 ≤ a3 + 4 * a2 + 6 * a1 + 4 * a0 ∧ a3 + 4 * a2 + 6 * a1 + 4 * a0 ≤ 1 →
                      -1 ≤ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ∧ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ≤ 1 →
                        -1 ≤ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ∧ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ≤ 1 →
                          -1 ≤ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ∧ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ≤ 1 → a0 = 0
Agent10SmoothingBoundary.four_rigidity_at_five : ∀ (f : Agent10SmoothingBoundary.Series),
  (∀ (i : Nat), -5 ≤ f i ∧ f i ≤ 5) →
    (∀ (i : Nat), -1 ≤ Agent10SmoothingBoundary.four f i ∧ Agent10SmoothingBoundary.four f i ≤ 1) → ∀ (i : Nat), f i = 0
Agent10SmoothingBoundary.witness_zero_after : ∀ (i : Nat), 11 ≤ i → Agent10SmoothingBoundary.witness i = 0
```
</details>

### Agent10NineCarrySharp

Exact uniform complete-carry observation threshold nine for all active initial pair coefficients of admissible words and for the next integer of canonical ordinary decimal inputs at a common initial width. Reuses the unchanged nine-word upper bound and a direct kernel-certified width17 eight-word collision. Includes all prior13 modules and the preserved seven-word example. Every terminal carry is observed; ordinary iteration continues after a palindrome. No initial-integer injectivity or palindrome-avoidance claim.

- Root module(s): `P196.Agent10TwoPairReconstruction.Agent10ThreeColumnCarry`, `P196.Agent10CarryObservability.Agent10SixCarryCounterexample`, `P196.Agent10NineCarrySharp.Agent10SevenCarryCounterexample`, `P196.Agent10NineCarrySharp.Agent10NineCarrySharp`
- 16 modules, 122 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent10SmoothingBoundary.prefix_rigidity : ∀ (a0 a1 a2 a3 a4 a5 a6 : Int),
  -5 ≤ a1 ∧ a1 ≤ 5 →
    -5 ≤ a2 ∧ a2 ≤ 5 →
      -5 ≤ a3 ∧ a3 ≤ 5 →
        -5 ≤ a4 ∧ a4 ≤ 5 →
          -5 ≤ a5 ∧ a5 ≤ 5 →
            -5 ≤ a6 ∧ a6 ≤ 5 →
              -1 ≤ a0 ∧ a0 ≤ 1 →
                -1 ≤ a1 + 4 * a0 ∧ a1 + 4 * a0 ≤ 1 →
                  -1 ≤ a2 + 4 * a1 + 6 * a0 ∧ a2 + 4 * a1 + 6 * a0 ≤ 1 →
                    -1 ≤ a3 + 4 * a2 + 6 * a1 + 4 * a0 ∧ a3 + 4 * a2 + 6 * a1 + 4 * a0 ≤ 1 →
                      -1 ≤ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ∧ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ≤ 1 →
                        -1 ≤ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ∧ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ≤ 1 →
                          -1 ≤ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ∧ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ≤ 1 → a0 = 0
Agent10SmoothingBoundary.four_rigidity_at_five : ∀ (f : Agent10SmoothingBoundary.Series),
  (∀ (i : Nat), -5 ≤ f i ∧ f i ≤ 5) →
    (∀ (i : Nat), -1 ≤ Agent10SmoothingBoundary.four f i ∧ Agent10SmoothingBoundary.four f i ≤ 1) → ∀ (i : Nat), f i = 0
Agent10SmoothingBoundary.witness_zero_after : ∀ (i : Nat), 11 ≤ i → Agent10SmoothingBoundary.witness i = 0
```
</details>

### Agent10TwoPairReconstruction

Complete earlier Agent10 carry-observability closure, plus universal reconstruction of both first pair coefficients at every active index from eight complete carry words, without initial nonoverflow. An exact encoded three-column graph excludes all 5,184 starts of difference(0,1,-3); actual carry and width transport includes overlapping widths3/4 and the active width-one/two boundary. No full arbitrary-width eight-word reconstruction or P196 theorem.

- Root module(s): `P196.Agent10TwoPairReconstruction.Agent10ThreeColumnCarry`, `P196.Agent10CarryObservability.Agent10SixCarryCounterexample`
- 13 modules, 83 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent10SmoothingBoundary.prefix_rigidity : ∀ (a0 a1 a2 a3 a4 a5 a6 : Int),
  -5 ≤ a1 ∧ a1 ≤ 5 →
    -5 ≤ a2 ∧ a2 ≤ 5 →
      -5 ≤ a3 ∧ a3 ≤ 5 →
        -5 ≤ a4 ∧ a4 ≤ 5 →
          -5 ≤ a5 ∧ a5 ≤ 5 →
            -5 ≤ a6 ∧ a6 ≤ 5 →
              -1 ≤ a0 ∧ a0 ≤ 1 →
                -1 ≤ a1 + 4 * a0 ∧ a1 + 4 * a0 ≤ 1 →
                  -1 ≤ a2 + 4 * a1 + 6 * a0 ∧ a2 + 4 * a1 + 6 * a0 ≤ 1 →
                    -1 ≤ a3 + 4 * a2 + 6 * a1 + 4 * a0 ∧ a3 + 4 * a2 + 6 * a1 + 4 * a0 ≤ 1 →
                      -1 ≤ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ∧ a4 + 4 * a3 + 6 * a2 + 4 * a1 + a0 ≤ 1 →
                        -1 ≤ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ∧ a5 + 4 * a4 + 6 * a3 + 4 * a2 + a1 ≤ 1 →
                          -1 ≤ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ∧ a6 + 4 * a5 + 6 * a4 + 4 * a3 + a2 ≤ 1 → a0 = 0
Agent10SmoothingBoundary.four_rigidity_at_five : ∀ (f : Agent10SmoothingBoundary.Series),
  (∀ (i : Nat), -5 ≤ f i ∧ f i ≤ 5) →
    (∀ (i : Nat), -1 ≤ Agent10SmoothingBoundary.four f i ∧ Agent10SmoothingBoundary.four f i ≤ 1) → ∀ (i : Nat), f i = 0
Agent10SmoothingBoundary.witness_zero_after : ∀ (i : Nat), 11 ≤ i → Agent10SmoothingBoundary.witness i = 0
```
</details>

### EightCarryWidthBound

Exactly eight complete carry observations are necessary and sufficient uniformly at shared initial decimal widths at most fourteen, both for all active initial pair coefficients of admissible words and for the next integer of canonical ordinary inputs. The upper bound adds rigidity of symmetric integer series that vanish outside an initial segment of length at most ten and whose fourth smoothing has every coefficient in [-1,1], without an input coefficient bound. A kernel-certified width-thirteen pair, 9000004163209 and 9000001716109, has seven identical complete carry words but different next integers. All terminal carries are observed, later widths are unrestricted, and ordinary iteration continues after a palindrome. No initial-integer injectivity, optimality of the width-fourteen bound, separate optimality at every individual width, arbitrary-width eight-word reconstruction, or palindrome-avoidance result is claimed.

- Root module(s): `P196.EightCarryWidthBound.Sharpness`
- 15 modules, 18 checked endpoints
- Main endpoints: `EightCarryWidthBound.eight_carry_words_determine_pair_sums_of_width_le_fourteen`, `EightCarryWidthBound.eight_carry_words_determine_next_integer_of_width_le_fourteen`, `EightCarryWidthBound.WidthThirteenWitness.seven_carry_counterexample`, `EightCarryWidthBound.eight_is_exact_threshold_through_fourteen`

### EightCarryMaximalWidth

Sixteen is the exact largest uniform common initial decimal width bound for reconstruction from eight complete carry observations, both for every active pair coefficient of admissible words and for the next integer of canonical ordinary inputs. Eight is also the exact smallest uniform observation count over widths at most sixteen. The proof adds exact symmetric core classifications at nominal widths eleven and twelve and a complete kernel-certified seven-column prefix exclusion with a proved bridge to actual carry histories. It imports the width-fourteen upper bound, the canonical width-thirteen seven-observation collision, and the canonical width-seventeen eight-observation collision. All terminal carries are included, later widths are unrestricted, and ordinary iteration continues after a palindrome. No initial-integer injectivity, separate optimality at each individual width, arbitrary-width eight-observation reconstruction, or palindrome-avoidance result is claimed.

- Root module(s): `P196.EightCarryMaximalWidth.Sharpness`
- 71 modules, 25 checked endpoints
- Main endpoints: `EightCarryMaximalWidth.eight_carry_words_determine_pair_sums_of_width_le_sixteen`, `EightCarryMaximalWidth.eight_carry_words_determine_next_integer_of_width_le_sixteen`, `EightCarryMaximalWidth.eight_pair_reconstruction_iff_width_le_sixteen`, `EightCarryMaximalWidth.eight_next_integer_reconstruction_iff_width_le_sixteen`, `EightCarryMaximalWidth.pair_reconstruction_up_to_sixteen_iff`, `EightCarryMaximalWidth.next_integer_reconstruction_up_to_sixteen_iff`

### EightCarryThreePairSharp

At every common admissible initial decimal width, eight complete carry observations determine the first three active initial pair coefficients. Three is the exact largest uniform recoverable prefix length: an imported canonical width-seventeen pair with eight equal complete carry words differs at index three. The proof adds a necessary prefix classification for integer inputs in [-9,9] with fourth smoothing in [-1,1] and a kernel-certified finite exclusion of the remaining seven-column pattern, importing the proved bridge from actual histories and the five-column candidate cover from EightCarryMaximalWidth. Terminal overflow carries are included, later widths are unrestricted, and ordinary iteration continues after palindromes. No optimal observation count for the first three pairs, full pair recovery at arbitrary width, individual initial-digit reconstruction, or palindrome-avoidance conclusion is claimed.

- Root module(s): `P196.EightCarryThreePairSharp.Sharpness`
- 82 modules, 7 checked endpoints
- Main endpoints: `EightCarryThreePairSharp.eight_carries_determine_first_three_active_pairs`, `EightCarryThreePairSharp.eight_carry_prefix_reconstruction_iff`

### CarryPrefixThresholds

The exact uniform complete-carry observation threshold is zero for an empty initial pair prefix, seven for one coefficient, eight for two or three coefficients, and nine for every longer prefix, at every common admissible initial width. The new seven-observation exterior theorem follows from a global fourth-smoothing bound in [-2,2] and a kernel-certified three-column exclusion; the eight- and nine-observation upper bounds and the six- and eight-observation counterexamples are imported. A new canonical width-nine pair, 490039199 and 480047399, shares seven complete carry words but differs at initial pair index one, with next integers 1481969293 and 1473787483; its eighth observation differs at incoming index two. Every recovered index is initially active, all terminal carries are observed, later widths are unrestricted, and ordinary iteration continues after palindromes. No complete arbitrary-width recovery from seven or eight observations, initial-integer injectivity, optimal initial-width bound, or palindrome-avoidance conclusion is claimed.

- Root module(s): `P196.CarryPrefixThresholds.Thresholds`
- 93 modules, 14 checked endpoints
- Main endpoints: `CarryPrefixThresholds.seven_carries_determine_exterior_pair`, `CarryPrefixThresholds.SevenCarryWitness.seven_carry_counterexample`, `CarryPrefixThresholds.prefix_reconstruction_iff`

### SevenCarryMaximalWidth

Seven complete carry observations determine every active initial pair coefficient and the next ordinary integer uniformly over common positive initial widths at most W exactly when W ≤ 8. After removing the already recovered exterior coefficient, the proof classifies symmetric residuals of width at most six under a fourth-smoothing bound in [-2,2]. Only two signed nonzero profiles at residual width five remain; kernel-certified finite coverage, center parity, and the reflected fifth coefficient exclude their actual width-seven realizations. The existing canonical width-nine witness supplies both lower bounds without another witness computation. The algebraic classifications are necessary conditions and the finite lists are one-sided covers. Terminal carries are observed, later widths are unrestricted, and ordinary iteration continues after palindromes. The observation count is fixed at seven; no minimum-observation-count, initial-integer-injectivity, or palindrome-avoidance claim is made.

- Root module(s): `P196.SevenCarryMaximalWidth.Sharpness`
- 92 modules, 15 checked endpoints
- Main endpoints: `SevenCarryMaximalWidth.seven_carry_words_determine_pair_sums_of_width_le_eight`, `SevenCarryMaximalWidth.seven_pair_reconstruction_iff_width_le_eight`, `SevenCarryMaximalWidth.seven_next_integer_reconstruction_iff_width_le_eight`

### CarryWidthThresholds

The minimum number of complete carry observations needed to reconstruct all active initial pair coefficients uniformly over common positive initial widths at most W is determined for every W and every observation count K. Exactly the same threshold reconstructs the next ordinary integer from shared-width canonical decimal inputs.

| Cumulative initial-width bound W | Required observation threshold |
|---|---:|
| 0 (empty width class) | 0 |
| 1 | 4 |
| 2 | 5 |
| 3 through 8 | 7 |
| 9 through 16 | 8 |
| 17 and above | 9 |

The proof adds width-one and width-two upper bounds and canonical witness pairs (3,4), (16,17), and (809,719), which share respectively three, four, and six complete carry observations while differing at active pair index zero and in their next integers. Their actual pair orbits represent ordinary integer iteration at every time. The remaining bounds import the existing seven-, eight-, and nine-observation results. Terminal carries are observed, later widths are unrestricted, and ordinary iteration continues after palindromes. These are optimal thresholds for cumulative width classes; no optimality at each exact individual width, initial-integer or initial-digit injectivity, or palindrome-avoidance claim is made.

- Root module(s): `P196.CarryWidthThresholds.Thresholds`
- 95 modules, 10 checked endpoints
- Main endpoints: `CarryWidthThresholds.pair_reconstruction_iff`, `CarryWidthThresholds.next_integer_reconstruction_iff`

### BoundedCarryPrefixThresholds

For every initial-width bound W, requested active-prefix length J, and observation count K, uniform pair-prefix reconstruction holds exactly when min(widthThreshold W, prefixThreshold J) ≤ K. The imported width threshold is 0, 4, 5, 7, 8, or 9 for W equal to zero, one, two, three through eight, nine through sixteen, or at least seventeen. The imported prefix threshold is 0 for J zero, 7 for J one, 8 for J two or three, and 9 thereafter. Equivalently, the joint property holds exactly when either full bounded-width reconstruction or arbitrary-width prefix reconstruction holds. Replacing J by min(J,W) preserves the property. All positive reconstruction results and the five lower witnesses at widths one, two, three, nine, and seventeen are imported unchanged. Both the requested-prefix and initially active-index guards are retained; terminal carries are observed and later widths are unrestricted. These are thresholds for cumulative width classes and active pair coefficients, with no claim about exact individual-width minima, original digit splitting, or palindrome avoidance.

- Root module(s): `P196.BoundedCarryPrefixThresholds.Thresholds`
- 113 modules, 3 checked endpoints
- Main endpoints: `BoundedCarryPrefixThresholds.reconstruction_iff`, `BoundedCarryPrefixThresholds.reconstruction_iff_either`, `BoundedCarryPrefixThresholds.prefix_cutoff_reduction`

### ExactSmallWidthCarryThresholds

For each fixed positive initial width L from one through eight and every observation count K, reconstruction of all initially active pair coefficients holds exactly when K reaches the corresponding threshold below. The same thresholds characterize recovery of the next ordinary integer from canonical inputs sharing that exact initial width. The pair property ranges over all admissible profiles at that width.

| Exact initial width L | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Minimum complete carry observations | 4 | 5 | 7 | 6 | 7 | 6 | 7 | 7 |

The new upper bounds at widths four and six follow from a global fourth-smoothing bound [-4,4], symmetric rigidity at width four, and a necessary two-core factorization at width six. Seven kernel certificates give one-sided prefix covers; the actual width-six reflection excludes both nonzero cores in both orientations. Earlier upper bounds at the other widths and the lower witnesses at widths one through three are imported unchanged. Five new canonical pairs at widths four through eight share one fewer observation, differ in an active initial pair coefficient, and have unequal next integers; their pair recursion represents ordinary numeric iteration at every time. Terminal carries are included, later widths are unrestricted, and iteration continues after palindromes. No exact-width minimum is asserted outside one through eight, and no original digit splitting or palindrome avoidance is claimed.

- Root module(s): `P196.ExactSmallWidthCarryThresholds.Thresholds`
- 98 modules, 21 checked endpoints
- Main endpoints: `ExactSmallWidthCarryThresholds.pair_reconstruction_iff`, `ExactSmallWidthCarryThresholds.next_integer_reconstruction_iff`, `ExactSmallWidthCarryThresholds.exact_width_counterexample`, `ExactSmallWidthCarryThresholds.six_carry_words_determine_pair_sums_of_width_four`, `ExactSmallWidthCarryThresholds.six_carry_words_determine_pair_sums_of_width_six`

### ExactWidthCarryThresholds

For each fixed positive initial width L from one through seventeen and every observation count K, the following exact minimum characterizes both reconstruction of all initially active pair coefficients and recovery of the next ordinary integer. The pair property ranges over all admissible profiles at that exact width; the integer property ranges over canonical inputs sharing that width. The fixed-width predicates and the entire classification through width eight are imported unchanged.

| Exact initial width L | Minimum complete carry observations |
|---|---|
| 1 | 4 |
| 2 | 5 |
| 4, 6 | 6 |
| 3, 5, 7, 8, 10 | 7 |
| 9, 11, 12, 13, 14, 15, 16 | 8 |
| 17 | 9 |

The new positive case is seven-observation reconstruction at width ten. Removing the already determined exterior pair leaves a symmetric width-eight integer series with fourth smoothing in [-2,2]; it must be zero or one of the two signs of [1,-2,2,-1,-1,2,-2,1]. Three new kernel certificates supply 893 one-sided finite obligations, reusing the existing first-three and even-fourth coefficient covers, and exact width-ten reflection excludes both nonzero orientations. Five new canonical pairs at widths ten, eleven, twelve, fourteen and sixteen share one fewer complete observation, differ in an active initial pair coefficient, and have unequal next integers. Their pair recursion represents ordinary numeric iteration at every time. The other lower witnesses and the eight- and nine-observation upper bounds are imported unchanged. Terminal carries are included, later widths are unrestricted, and iteration continues after palindromes. No minimum is asserted at width zero or above seventeen, and no original digit splitting, initial-integer injectivity, or palindrome avoidance is claimed.

- Root module(s): `P196.ExactWidthCarryThresholds.Thresholds`
- 120 modules, 13 checked endpoints
- Main endpoints: `ExactWidthCarryThresholds.pair_reconstruction_iff`, `ExactWidthCarryThresholds.next_integer_reconstruction_iff`, `ExactWidthCarryThresholds.exact_width_counterexample`, `ExactWidthCarryThresholds.seven_carry_words_determine_pair_sums_of_width_ten`, `ExactWidthCarryThresholds.smooth_four_box_two_width_eight_classification`

### Agent6CertificateCoordinateAudit

Original full checker acceptance implies normalized-row signed-beta cancellation and both signs. An executable necessary filter preserves the original Boolean checker when used as a precheck. Exact rejected controls demonstrate insufficiency. Weighted normalized-row balance is separate from legacy totalGam. No accepted certificate instance, integer realization, new global cycle exclusion, or 196 conclusion.

- Root module(s): `P196.Agent6CertificateCoordinateAudit.CertificateControls`
- 20 modules, 29 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent6.CertificateCoordinates.rowOuter_orbit : ∀ (cert : Agent109.Cert.Certificate),
  Agent109.Cert.Valid cert →
    ∀ (n : Nat),
      Agent6.ExteriorCoordinates.outerIter n (Agent6.CertificateCoordinates.rowOuter cert 0) =
        Agent6.CertificateCoordinates.rowOuter cert (n % cert.P)
Agent6.CertificateCoordinates.rowOuter_orbit_of_lt : ∀ (cert : Agent109.Cert.Certificate),
  Agent109.Cert.Valid cert →
    ∀ (i : Nat),
      i < cert.P →
        Agent6.ExteriorCoordinates.outerIter i (Agent6.CertificateCoordinates.rowOuter cert 0) =
          Agent6.CertificateCoordinates.rowOuter cert i
Agent6.CertificateCoordinates.rowOuter_closed : ∀ (cert : Agent109.Cert.Certificate),
  Agent109.Cert.Valid cert →
    Agent6.ExteriorCoordinates.outerIter cert.P (Agent6.CertificateCoordinates.rowOuter cert 0) =
      Agent6.CertificateCoordinates.rowOuter cert 0
```
</details>

### Agent6CoordinateDynamics

Exact finite exterior overflow/rho quotient; signed beta update; nonzero and sign controls; finite telescoping, closed-orbit zero sum, both-sign witnesses and weighted balance. No ordinary integer-orbit correspondence, cycle existence, or global acyclicity claim.

- Root module(s): `P196.Agent6CoordinateDynamics.CoordinateCycle`
- 9 modules, 58 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent6.ExteriorCoordinates.phaseCarry_le_one : ∀ (c : Nat), Agent6.ExteriorCoordinates.phaseCarry c ≤ 1
Agent6.ExteriorCoordinates.phaseCarry_eq_div_nine : ∀ (c : Nat),
  c ≤ 17 → c ≠ 9 → Agent6.ExteriorCoordinates.phaseCarry c = c / 9
Agent6.ExteriorCoordinates.phaseDigit_identity : ∀ (c : Nat),
  9 * Agent6.ExteriorCoordinates.phaseCarry c + Agent6.ExteriorCoordinates.phaseDigit c = c
```
</details>

### Agent6CoordinateThreshold

Exact finite exterior overflow/rho quotient, sharp phase domain, and bounded zero/one threshold. No all-time orbit claim.

- Root module(s): `P196.Agent6CoordinateThreshold.CoordinateThreshold`
- 4 modules, 16 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent6.ExteriorCoordinates.phaseCarry_le_one : ∀ (c : Nat), Agent6.ExteriorCoordinates.phaseCarry c ≤ 1
Agent6.ExteriorCoordinates.phaseCarry_eq_div_nine : ∀ (c : Nat),
  c ≤ 17 → c ≠ 9 → Agent6.ExteriorCoordinates.phaseCarry c = c / 9
Agent6.ExteriorCoordinates.phaseDigit_identity : ∀ (c : Nat),
  9 * Agent6.ExteriorCoordinates.phaseCarry c + Agent6.ExteriorCoordinates.phaseDigit c = c
```
</details>

### Agent6NormalizedCarryAccounting

Numeric carry survives suffix stripping under c<=18 or bounded raw B. Under bounded raw B only, the original normalized stateOuter overflowBit equals gam. Listed-row indicator sums equal original totalGam. Original check=true supplies the weighted balance with 9*totalGam or18*(totalG+totalH), consuming existing coordinate and gain identities. Exact kernel controls delimit missing hypotheses. No accepted certificate, new recurrence, overflow necessity, ordinary realizability or 196 conclusion.

- Root module(s): `P196.Agent6NormalizedCarryAccounting.CarryControls`
- 21 modules, 16 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent6.NormalizedCarry.gam_eq_overflow : ∀ (s : Agent109.Cert.State),
  Agent109.Cert.gam s = Agent6.ExteriorCoordinates.overflow s.c s.B
Agent6.NormalizedCarry.overflow_stripSuffix_of_le18 : ∀ (c : Nat) (B : List Nat),
  c ≤ 18 →
    Agent6.ExteriorCoordinates.overflow c (P196.Agent7.Finite.stripSuffix c B) = Agent6.ExteriorCoordinates.overflow c B
Agent6.NormalizedCarry.overflow_stripSuffix_of_bounded : ∀ (c : Nat) (B : List Nat),
  Agent109.Bounded B →
    Agent6.ExteriorCoordinates.overflow c (P196.Agent7.Finite.stripSuffix c B) = Agent6.ExteriorCoordinates.overflow c B
```
</details>

### Agent8CommonOverflowDefect

*Common-overflow defect transport scoped source registry*

Exact common-carry antisymmetric normalized-digit transport, ordinary-decimal two-step consequences, and finite actual witness.

- Root module(s): `P196.Agent8CommonOverflowDefect.Agent8DefectWitness`
- 8 modules, 7 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent8.CommonOverflowDefect.common_carry_transport : ∀ (q s : Nat → Nat) (L h : Nat),
  h = 0 ∨ h = 1 →
    DecimalDigits.carry q L = h →
      DecimalDigits.carry s L = h →
        P196.Agent8.CommonOverflowDefect.AntisymmetricDefect q s L →
          ∀ (i : Nat),
            i < L + h →
              ↑(FoldedDecimal.nextColumns q L i) - ↑(FoldedDecimal.nextColumns s L i) =
                P196.Agent8.CommonOverflowDefect.oldDigitDefect q s L i -
                  P196.Agent8.CommonOverflowDefect.shift (P196.Agent8.CommonOverflowDefect.oldDigitDefect q s L) h i
P196.Agent8.CommonOverflowDefect.overflow_noncancellation : ∀ (q s : Nat → Nat) (L : Nat),
  DecimalDigits.carry q L = 1 →
    DecimalDigits.carry s L = 1 →
      P196.Agent8.CommonOverflowDefect.AntisymmetricDefect q s L →
        (∃ i, i < L ∧ DecimalDigits.output q i ≠ DecimalDigits.output s i) →
          ∃ i, i < L + 1 ∧ FoldedDecimal.nextColumns q L i ≠ FoldedDecimal.nextColumns s L i
P196.Agent8.CommonOverflowDefect.numeric_common_carry_transport : ∀ (n m : Nat) (d f q s : Nat → Nat) (L h : Nat),
  DecimalDigits.Canonical n d L →
    DecimalDigits.Canonical m f L →
      (∀ (i : Nat), i < L → DecimalDigits.columnSum d L i = q i) →
        (∀ (i : Nat), i < L → DecimalDigits.columnSum f L i = s i) →
          h = 0 ∨ h = 1 →
            DecimalDigits.carry q L = h →
              DecimalDigits.carry s L = h →
                P196.Agent8.CommonOverflowDefect.AntisymmetricDefect q s L →
                  ∃ a b,
                    DecimalDigits.Canonical (Lychrel196.step n) a (L + h) ∧
                      DecimalDigits.Canonical (Lychrel196.step m) b (L + h) ∧
                        ∀ (i : Nat),
                          i < L + h →
                            ↑(DecimalDigits.columnSum a (L + h) i) - ↑(DecimalDigits.columnSum b (L + h) i) =
                              P196.Agent8.CommonOverflowDefect.oldDigitDefect q s L i -
                                P196.Agent8.CommonOverflowDefect.shift
                                  (P196.Agent8.CommonOverflowDefect.oldDigitDefect q s L) h i
```
</details>

### Agent5ExactDigitStreams

Exact executable low10-adic and high fractional decimal streams, coherent digit prefixes and bounds, and unchanged outerNext reconstructed at every cutoff>=B.length+1 using only phase/length/zValue/rhoNum. Includes empty, zerohead and untrimmed bounded words. Reuses Agent6 published exact overflow thresholds.

- Root module(s): `P196.Agent5ExactDigitStreams.CoordinateOnlyStreams`
- 9 modules, 30 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent5.ExactDigitStreams.adicNumeratorDigits_length : ∀ (n : Nat) (a : Int),
  (Agent5.ExactDigitStreams.adicNumeratorDigits n a).length = n
Agent5.ExactDigitStreams.fractionDigits_length : ∀ (n r D : Nat),
  (Agent5.ExactDigitStreams.fractionDigits n r D).length = n
Agent5.ExactDigitStreams.adicNumeratorDigits_bounded : ∀ (n : Nat) (a : Int) (d : Nat),
  d ∈ Agent5.ExactDigitStreams.adicNumeratorDigits n a → d ≤ 9
```
</details>

### Agent5OrdinaryStreamPrefix

The exact first B.length+1 paired coefficients after one actual reverseAddDigits step, expressed as literal coordinate streams with actual-carry, threshold and quotient selectors; the ordinary numeral wrapper retains original DecimalDigits, PositiveLast and surrounded-shape hypotheses.

- Root module(s): `P196.Agent5OrdinaryStreamPrefix.OrdinaryStreamStep`
- 15 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent5.OrdinaryStreamPrefix.normalize7_eq_norm6 : ∀ (w : List Nat) (e : Nat),
  P196.Agent7.Finite.normalize w e = P196.Agent6.norm w e
Agent5.OrdinaryStreamPrefix.nonneutralPhase_nonneutral6 : ∀ (c : Nat),
  Agent115.ExteriorFactorization.nonneutralPhase c → P196.Agent6.Nonneutral c
Agent5.OrdinaryStreamPrefix.ordinary_raw_prefix_from_normalized_streams : ∀ (D B W : List Nat) (c gap : Nat),
  Agent115.ExteriorFactorization.nonneutralPhase c →
    P196.Agent6.Coefficients B →
      P196.Agent6.Coefficients W →
        P196.Agent6.paired D = P196.Agent6.surrounded B c gap W →
          List.take (B.length + 1) (P196.Agent6.paired (P196.Agent6.reverseAddDigits D)) =
            List.zipWith Nat.add
              (Agent5.ExactDigitStreams.adicNumeratorDigits (B.length + 1)
                (Agent115.ExteriorFactorization.zValue c B - ↑c))
              (Agent5.ExactDigitStreams.fractionDigits (B.length + 1) (Agent115.ExteriorFactorization.rhoNum c B)
                (9 * 10 ^ B.length * 10 ^ (P196.Agent7.Finite.normalize B.reverse (if 10 ≤ c then 1 else 0)).snd))
```
</details>

### Agent5StreamAgreementWindow

Exact finite one-step literal-stream agreement through q <= gap + outgoing carry, with canonical all-gap witnesses proving uniform sharpness in both carry branches. Original surrounded shape, eight phases, coefficient bounds18 and canonical numeral hypotheses remain explicit.

- Root module(s): `P196.Agent5StreamAgreementWindow.StreamAgreementWindow`, `P196.Agent5StreamAgreementWindow.StreamWindowSharpness`
- 17 modules, 26 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent5.OrdinaryStreamWindow.take_prefix_replicate : ∀ (L M : List Nat) (t m q : Nat),
  q ≤ m → List.take (L.length + q) (L ++ List.replicate m t ++ M) = L ++ List.replicate q t
Agent5.OrdinaryStreamWindow.paired_bands_window : ∀ (L M R : List Nat) (t e gap q : Nat),
  e ≤ 1 →
    L.length = R.length + 1 →
      q ≤ gap + e →
        List.take (R.length + 1 + q)
            (P196.Agent6.paired
              (L ++ List.replicate (gap + 1) t ++ M ++ List.replicate (gap + 1) t ++ R ++ P196.Agent6.carryEnd e)) =
          List.zipWith Nat.add (L ++ List.replicate q t)
            ((if (e == 0) = true then R.reverse ++ [t] else 1 :: R.reverse) ++ List.replicate q t)
Agent5.OrdinaryStreamWindow.surrounded_raw_exterior_window : ∀ (B W : List Nat) (c gap q : Nat),
  P196.Agent6.Nonneutral c →
    P196.Agent6.Coefficients B →
      P196.Agent6.Coefficients W →
        q ≤ gap + (P196.Agent6.norm B.reverse (P196.Agent6.carryPhase c)).snd →
          List.take (B.length + 1 + q)
              (P196.Agent6.paired (P196.Agent6.normalizedDigits (P196.Agent6.surrounded B c gap W))) =
            List.zipWith Nat.add (P196.Agent6.lowEnd B c ++ List.replicate q (P196.Agent6.digitPhase c))
              ((if ((P196.Agent6.norm B.reverse (P196.Agent6.carryPhase c)).snd == 0) = true then
                  List.reverse (P196.Agent6.norm B.reverse (P196.Agent6.carryPhase c)).fst ++ [P196.Agent6.digitPhase c]
                else 1 :: List.reverse (P196.Agent6.norm B.reverse (P196.Agent6.carryPhase c)).fst) ++
                List.replicate q (P196.Agent6.digitPhase c))
```
</details>

### StreamObservationInjectivity

*Finite reconstruction from separate exterior digit streams*

At a fixed nonneutral phase and common width n, the first n+1 digits of the separate original low and high coordinate streams determine every coefficient of a word bounded by 18, with the actual outgoing carry decoded from stream residues rather than supplied separately. Includes empty, zero-head, and untrimmed words. Phase-two witnesses show that n digits can fail at every positive width, even for validOuter words, so the uniform n+1 cutoff is sharp. No ordinary integer-orbit, reverse-and-add injectivity, or 196 conclusion is claimed.

- Root module(s): `P196.StreamObservationInjectivity.Injectivity`, `P196.StreamObservationInjectivity.Sharpness`
- 11 modules, 5 checked endpoints
- Endpoints: `Agent5.StreamObservationInjectivity.no_overflow_iff_stream_residues`, `Agent5.StreamObservationInjectivity.decodeCarry_correct`, `Agent5.StreamObservationInjectivity.exterior_eq_of_stream_prefixes`, `Agent5.StreamObservationInjectivity.exterior_eq_of_streams_at_cutoff`, `Agent5.StreamObservationInjectivity.observation_cutoff_sharp`

### TrimmedStreamObservation

*Sharp asymmetric observation of trimmed exterior words*

At a fixed nonneutral phase and shared width n, coefficient words bounded by 18 and terminally trimmed are determined by n low digits and n+1 high digits of the separate original coordinate streams, without supplied equality of normalization carries. Includes empty and zero-head words, validOuter specializations, and larger independent cutoffs. The residue classification isolates phases eight and ten; outside those phases the same shared-width recovery requires no trimming, while positive-head collisions at both exceptional phases show that trimming cannot be dropped uniformly. Terminally trimmed words of potentially different widths are recovered from both streams at a common cutoff at least max(lengths)+1; a valid phase-ten unequal-width collision shows that reducing its low cutoff to max(lengths) can fail even with every high cutoff known. Phase-four valid witnesses make n-1 low digits insufficient at every positive width even with every high cutoff known. Phase-two valid witnesses make n high digits insufficient at every width n>=2 even with every low cutoff known. These sharpness claims are uniform over nonneutral phases, not assertions of optimality at each phase separately. No ordinary integer-orbit, reverse-and-add injectivity, palindrome-avoidance, or 196 conclusion is claimed.

- Root module(s): `P196.TrimmedStreamObservation.Injectivity`, `P196.TrimmedStreamObservation.RegularPhases`, `P196.TrimmedStreamObservation.WidthRecovery`, `P196.TrimmedStreamObservation.Controls`, `P196.TrimmedStreamObservation.Sharpness`, `P196.TrimmedStreamObservation.LowSharpness`
- 19 modules, 13 checked endpoints
- Endpoints: `Agent5.TrimmedStreamObservation.cross_highValue_phase_carries`, `Agent5.TrimmedStreamObservation.low_carry_eq_of_trimmed_high`, `Agent5.TrimmedStreamObservation.exterior_eq_of_mixed_prefixes`, `Agent5.TrimmedStreamObservation.valid_exterior_eq_of_mixed_prefixes`, `Agent5.TrimmedStreamObservation.exterior_eq_of_mixed_cutoffs`, `Agent5.TrimmedStreamObservation.exterior_eq_of_mixed_prefixes_of_regular_phase`, `Agent5.TrimmedStreamObservation.exterior_eq_of_common_prefixes`, `Agent5.TrimmedStreamObservation.valid_exterior_eq_of_common_prefixes`, `Agent5.TrimmedStreamObservation.untrimmed_phase_eight_collision`, `Agent5.TrimmedStreamObservation.untrimmed_phase_ten_collision`, `Agent5.TrimmedStreamObservation.unequal_width_mixed_collision`, `Agent5.TrimmedStreamObservation.high_cutoff_sharp_with_complete_low`, `Agent5.TrimmedStreamObservation.low_cutoff_sharp_with_complete_high`

### PhaseStreamRecovery

*Recovering exterior phase and word from sharp finite observations*

For coefficient words bounded by 18, explicit total decoders receiving only the width and the first n+1 original low and high digits recover the nonneutral phase and the actual high normalization carry. The same observations jointly identify the phase and every coefficient at a shared width n, without trimming, positive-head, or supplied carry equality assumptions; empty words and zero heads are included. Each stream uses its own phase and its own calculated high denominator. Terminally trimmed words of potentially different widths and phases are identified at any common cutoff at least max(lengths)+1, including validOuter states. At nonneutral phases, for arbitrary untrimmed bounded words, equality of both complete streams is equivalent to equal phases and equal canonical stripSuffix cores. This equivalence already holds at any finite cutoff at least max(core lengths)+1, independently of the numbers of appended phase letters. Removing the maximal phase suffix preserves every low prefix for all natural phases and every high prefix at nonneutral phases, without coefficient bounds. Each n+1 observation budget is separately sharp at every width, including zero, when the opposite cutoff stays at n+1: the same valid word at phases ten and twelve defeats low cutoff n, while phases two and twelve defeat high cutoff n. These sharpness witnesses give finite prefix collisions, not equality of complete infinite streams. No ordinary integer-orbit, reverse-and-add injectivity, palindrome-avoidance, or 196 conclusion is claimed.

- Root module(s): `P196.PhaseStreamRecovery.CanonicalFibers`, `P196.PhaseStreamRecovery.Sharpness`
- 23 modules, 13 checked endpoints
- Endpoints: `Agent5.PhaseStreamRecovery.decodePhase_correct`, `Agent5.PhaseStreamRecovery.decodeHighCarry_correct`, `Agent5.PhaseStreamRecovery.phase_eq_of_stream_prefixes`, `Agent5.PhaseStreamRecovery.state_eq_of_stream_prefixes`, `Agent5.PhaseStreamRecovery.state_eq_of_streams_at_cutoff`, `Agent5.PhaseStreamRecovery.state_eq_of_common_prefixes`, `Agent5.PhaseStreamRecovery.valid_state_eq_of_common_prefixes`, `Agent5.PhaseStreamRecovery.phase_low_cutoff_sharp`, `Agent5.PhaseStreamRecovery.phase_high_cutoff_sharp`, `Agent5.PhaseStreamRecovery.stripSuffix_low_stream`, `Agent5.PhaseStreamRecovery.stripSuffix_high_stream`, `Agent5.PhaseStreamRecovery.state_streams_eq_iff`, `Agent5.PhaseStreamRecovery.all_streams_eq_iff`

### BidirectionalWordDecoder

*Sharp constructive decoding of exterior observations*

An explicit total recursive decoder reconstructs a natural coefficient word from its width and its two original decimal positional values when all coefficients are at most 90, using one reconstruction step per position and no enumeration or noncomputable choice. A parameterized bound for coefficients at most 9k supports the proof. The positional pair is injective at every coefficient bound in widths zero through two, exactly through bound 100 in width three, and exactly through bound 90 at each width at least four. Explicit collisions at 101 and 91 prove necessity, with positive-head witnesses at every width at least four; the exact uniform threshold over all widths is 90. The recursive decoder correctness itself is asserted through 90, independently of the stronger width-three injectivity bound. Composing the original phase/carry and positional-value identities gives executable recovery of the whole exterior state from n+1 original low and high digits. That stream theorem retains nonneutral phases and the coefficient bound of 18, including empty, zero-head, and untrimmed words. Under the same nonneutral-phase and bound-18 assumptions, a canonical decoder receives only a cutoff parameter N and the two N+1 prefixes; it returns the phase and original stripSuffix core whenever the core length is at most N, even when phase padding makes the original width arbitrarily larger. No ordinary integer-orbit injectivity, palindrome-avoidance, or 196 conclusion is claimed.

- Root module(s): `P196.BidirectionalWordDecoder.CanonicalDecoder`, `P196.BidirectionalWordDecoder.Sharpness`
- 24 modules, 10 checked endpoints
- Endpoints: `Agent5.BidirectionalWordDecoder.highValue_bound`, `Agent5.BidirectionalWordDecoder.decodeValues_length`, `Agent5.BidirectionalWordDecoder.decodeValues_correct`, `Agent5.BidirectionalWordDecoder.width_three_collision`, `Agent5.BidirectionalWordDecoder.width_ge_four_collision`, `Agent5.BidirectionalWordDecoder.values_injective_at_iff`, `Agent5.BidirectionalWordDecoder.values_injective_bound_iff`, `Agent5.BidirectionalWordDecoder.observedValues_correct`, `Agent5.BidirectionalWordDecoder.decodeState_correct`, `Agent5.BidirectionalWordDecoder.decodeCanonicalState_correct`

### StreamNonisolation

*No finite coordinate observation isolates a canonical exterior state*

At every nonneutral phase, every valid exterior word and every finite cutoff admit a strictly longer valid canonical word, beyond any supplied lower width, with the same calculated high carry and the same two original coordinate-stream prefixes. The explicit witness appends sufficiently many copies of the phase and then the phase plus one. Its terminal coefficient prevents maximal phase-suffix removal, so this is a different canonical state rather than a padded representation of the original. Generic append lemmas preserve low observations through the old width for arbitrary natural coefficients and phases; high preservation uses nonneutral phases, coefficients at most 18, and a carry-preserving final coefficient. All high expressions retain the actual word widths and calculated normalization carries in their original denominators. The main valid-word theorem includes empty words and cutoff zero; its bounded-word intermediate also permits zero heads and untrimmed inputs. Consequently no decoder of a fixed finite pair of prefixes recovers all valid states, even when chosen with knowledge of the phase and cutoff. At each individual valid state, the observations cannot certify any finite upper bound on canonical core width, even when the actual high carry is supplied. The alternative word depends on the finite cutoff; equality of complete infinite streams is not asserted. No ordinary integer-orbit reachability, palindrome-avoidance, or 196 conclusion is claimed.

- Root module(s): `P196.StreamNonisolation.Obstruction`
- 15 modules, 10 checked endpoints
- Endpoints: `Agent5.StreamNonisolation.append_low_prefix`, `Agent5.StreamNonisolation.append_high_carry`, `Agent5.StreamNonisolation.append_high_prefix`, `Agent5.StreamNonisolation.extendWord_length`, `Agent5.StreamNonisolation.extendWord_canonical`, `Agent5.StreamNonisolation.extendWord_valid`, `Agent5.StreamNonisolation.extendWord_same_prefixes`, `Agent5.StreamNonisolation.arbitrarily_wide_valid_same_prefixes`, `Agent5.StreamNonisolation.no_finite_stream_decoder`, `Agent5.StreamNonisolation.no_finite_core_width_certificate`

### UniversalPhasePrefixes

*One canonical word realizes every nonneutral phase at a finite observation*

For every valid exterior target at a nonneutral phase, every finite cutoff, and every lower width, one strictly longer word is simultaneously valid and maximally trimmed at all eight nonneutral phases, with the same calculated high carry and both original observed prefixes as the target. The witness appends phase padding and the odd coefficient 1 or 11; it is chosen before the alternative phase and is independent of that phase. The terminal coefficient transfers either incoming phase carry to the incoming carry of the target phase, while its position lies beyond the observed window. Generic low-prefix phase independence holds through the word width for arbitrary natural phases and coefficients. Generic high carry transfer also needs no bounds; the normalized high-prefix and high relay identities retain nonneutral phases and coefficient bound 18. Each original high denominator retains its own word width and calculated carry. Bounded intermediate statements include zero heads and untrimmed words; the main theorem uses original validity and includes the empty word and cutoff zero. At every individual valid target, finite prefixes and even the supplied actual high carry cannot certify its phase among unrestricted widths. No decoder selected for a fixed cutoff recovers every valid state phase from those three observations. The common alternative depends on the finite cutoff; equality of complete streams or agreement of future dynamical observations is not asserted. No ordinary integer-orbit reachability, palindrome-avoidance, or 196 conclusion is claimed.

- Root module(s): `P196.UniversalPhasePrefixes.Obstruction`
- 16 modules, 11 checked endpoints
- Endpoints: `Agent5.UniversalPhasePrefixes.low_prefix_phase_independent`, `Agent5.UniversalPhasePrefixes.relay_high_carry`, `Agent5.UniversalPhasePrefixes.high_prefix_normalized`, `Agent5.UniversalPhasePrefixes.relay_high_prefix`, `Agent5.UniversalPhasePrefixes.universalWord_length`, `Agent5.UniversalPhasePrefixes.universalWord_canonical`, `Agent5.UniversalPhasePrefixes.universalWord_valid`, `Agent5.UniversalPhasePrefixes.universalWord_same_prefixes`, `Agent5.UniversalPhasePrefixes.arbitrarily_wide_all_phase_same_prefixes`, `Agent5.UniversalPhasePrefixes.no_finite_phase_certificate`, `Agent5.UniversalPhasePrefixes.no_finite_phase_decoder`

### FiniteExteriorHistories

*Finite exterior histories cannot determine phase or bound canonical width*

For every nonneutral phase c and coefficient word B bounded by 18, the existing universalWord c B m reproduces the target's actual high normalization carry and both original coordinate-stream prefixes of length cut at every time t at most T under the original outerIter, at every alternative initial nonneutral phase d, provided 2*T is at most m and cut+T is at most B.length+m. The generic theorem allows empty, zero-head, and untrimmed words. Consequently every valid target, finite cutoff, finite time horizon, and lower width W admit one word longer than both the target and W that is initially valid and maximally trimmed at all eight phases simultaneously and matches the entire finite observation history. This same initial word is chosen before the alternative phase and time; the explicit sufficient padding is max(cut,W)+2*T. Each observation uses its own current phase, word width, numerator, denominator, and calculated carry. The proof exposes an every-cutoff identity equating the phase-extended successor coefficient prefix to the sum of the two original digit prefixes. A shared coefficient window through one target-phase position beyond the target word forces the actual high carry and both one-shorter prefixes. Step and iterate phase/coefficient bounds require only nonneutral phase and bound 18; width growth by at most one per step requires neither. A general propagation theorem retains radius N-t when the initial window is N and the target initial width plus 2*t is at most N. A literal finite list records carry, low prefix, and high prefix at times zero through T. At every valid target, that history cannot certify its initial phase or any finite upper bound on canonical core width; the latter obstruction holds even when the initial phase is known. No decoder selected for fixed cut and T recovers every valid initial phase from that finite list alone. The alternative depends on the finite horizon and cutoff. No optimality of the buffer, single alternative matching all times or cutoffs, equality of complete streams, ordinary integer-orbit realization, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.FiniteExteriorHistories.Obstruction`
- 25 modules, 18 checked endpoints
- Endpoints: `Agent5.FiniteExteriorHistories.coefficientPrefix_stripSuffix`, `Agent5.FiniteExteriorHistories.sameObservation_take`, `Agent5.FiniteExteriorHistories.coefficientPrefix_outerNext`, `Agent5.FiniteExteriorHistories.outerNext_nonneutral`, `Agent5.FiniteExteriorHistories.outerNext_bounded`, `Agent5.FiniteExteriorHistories.outerNext_length_le`, `Agent5.FiniteExteriorHistories.outerIter_nonneutral`, `Agent5.FiniteExteriorHistories.outerIter_bounded`, `Agent5.FiniteExteriorHistories.outerIter_length_le`, `Agent5.FiniteExteriorHistories.sameObservation_of_coefficientPrefix`, `Agent5.FiniteExteriorHistories.sameObservation_step`, `Agent5.FiniteExteriorHistories.sameObservation_outerIter`, `Agent5.FiniteExteriorHistories.universalWord_same_history`, `Agent5.FiniteExteriorHistories.arbitrarily_wide_all_phase_same_history`, `Agent5.FiniteExteriorHistories.observationHistory_eq_iff`, `Agent5.FiniteExteriorHistories.no_finite_history_phase_certificate`, `Agent5.FiniteExteriorHistories.no_finite_history_core_width_certificate`, `Agent5.FiniteExteriorHistories.no_finite_history_phase_decoder`

### OrdinaryExteriorHistories

*Eight distinct ordinary seeds of equal width realize every finite exterior history*

An ordinary observation consists of the full terminal carry of the mirrored-pair-word normalization at time t and the separate low and high prefixes of the canonical decimal digits of the accepted Lychrel196 integer orbit at time t+1. If an ordinary integer realizes an existing complementary template at a nonneutral phase, all three finite blocks have coefficients bounded by 18, and both initial bands have length at least 2*T+cut+2, these observations agree with the original exterior observation of outerIter through every t at most T. The actual carry, separate ends, original stream numerators, current exterior widths, and carry-dependent high denominators are retained. The adapter reuses the existing whole-template normalization and actual_outer_orbit; no supplied interior path, initial trimming, or extra positivity hypothesis is needed. For every nonneutral valid exterior target, finite cut and T, and lower width W, the existing all-phase exterior history construction yields one word A longer than both the target and W, initially valid and maximally trimmed at all eight phases. With g=2*T+cut+2, each phase d has a positive ordinary seed whose exact pair word is template d A [] [] g g, whose initial decimal width is 2*A.length+4*g, and whose observations through T equal the target exterior history. The same A is chosen before d. An explicit injective family indexed by Fin 8 realizes phases 2,4,6,8,10,12,14,16; all eight seeds have equal full decimal widths at every time through T+1. Reusable adapters identify the canonical digits of every ordinary successor with the full pair-word normalization and its width increment with the actual terminal carry, including zero. Equal finite ordinary histories and equal initial widths therefore preserve equal widths through the successor of the last observed transition. Literal template length gives positive realizations of the stated common width; the first positive-length phase band separates template phases and hence ordinary seeds, without assuming pairWord injective. The seeds depend on the finite cutoff and horizon. No single integer realizing an infinite exterior history, replacement of an arbitrary separately supplied integer history, optimal band length, total carry count, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.OrdinaryExteriorHistories.Family`
- 38 modules, 12 checked endpoints
- Endpoints: `Agent5.OrdinaryExteriorHistories.digits_step_eq_normalize`, `Agent5.OrdinaryExteriorHistories.phase_of_nonneutral`, `Agent5.OrdinaryExteriorHistories.ordinary_step_observation_of_template`, `Agent5.OrdinaryExteriorHistories.ordinary_history_of_template`, `Agent5.OrdinaryExteriorHistories.digits_step_length`, `Agent5.OrdinaryExteriorHistories.digits_length_of_template`, `Agent5.OrdinaryExteriorHistories.positive_template_realized`, `Agent5.OrdinaryExteriorHistories.template_phase_injective`, `Agent5.OrdinaryExteriorHistories.distinct_phase_seeds`, `Agent5.OrdinaryExteriorHistories.digit_widths_of_same_history`, `Agent5.OrdinaryExteriorHistories.arbitrarily_wide_all_phase_ordinary_history`, `Agent5.OrdinaryExteriorHistories.eight_phase_ordinary_family`

### PhaseEighteenIsolation

*Finite original observations isolate the upper exterior boundary*

A coefficient-bounded phase-18 exterior target B is finitely isolated among all coefficient-bounded competitors A at arbitrary natural phases d at most 18, without an upper bound on the competing width. Equality of the actual outgoing normalization carries, the original low prefixes of length L=B.length+1, and the original high prefixes of length L plus the target actual carry implies d=18 and equality of the maximally phase-stripped words. Each high observation keeps its own original word width and calculated carry in its denominator. Consequently equality of the carry and both original prefixes at the common cutoff B.length+2 recovers the phase and canonical core. The generic theorem assumes only coefficient bound 18 and d<=18, allowing empty, zero-head, and untrimmed words, and competing phases 0,9 and odd values. For original validOuter states it recovers the entire competing word A=B. The proof pads the target by one 18 and the competitor by its own phase, compares equal-width positional values modulo nine, and forces the exact maximal tail quotient. Reusable interfaces identify positive literal fractional-prefix values with scaled integer quotients without requiring proper fractions or digits below ten; identify low block prefixes with positional residues; and separate the high block value from its remaining-tail quotient. For bounded coefficients and d<=18 that quotient is at most two and equals two exactly when d=18 and every tail coefficient is 18. It is distinct from the actual normalization carry. Phase padding preserves the original carry and both streams for every natural phase at most 18, without coefficient bounds; the carry proof reuses the existing suffix-removal invariance. Original validity is exposed as a suffix-retraction interface. The exact valid control (18,[8]) has actual carry zero and first literal high output 10, demonstrating why the high-prefix arithmetic cannot assume ordinary decimal digits at this boundary. The original observations, normalizer and exterior state definitions are unchanged. No optimal cutoff, removal of the supplied carry, complete phase-zero classification, extension to competing phases above 18, ordinary integer realization, infinite orbit, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.PhaseEighteenIsolation.Isolation`
- 36 modules, 14 checked endpoints
- Endpoints: `Agent5.PhaseEighteenIsolation.fractionDigits_value`, `Agent5.PhaseEighteenIsolation.low_prefix_append_value`, `Agent5.PhaseEighteenIsolation.high_prefix_append_value`, `Agent5.PhaseEighteenIsolation.rho_quotient_le_two`, `Agent5.PhaseEighteenIsolation.rho_quotient_eq_two_iff`, `Agent5.PhaseEighteenIsolation.boundary_values_rigidity`, `Agent5.PhaseEighteenIsolation.phase_padding_carry_of_le_eighteen`, `Agent5.PhaseEighteenIsolation.phase_padding_high_of_le_eighteen`, `Agent5.PhaseEighteenIsolation.sameObservation_phase_padding`, `Agent5.PhaseEighteenIsolation.stripSuffix_eq_of_valid`, `Agent5.PhaseEighteenIsolation.phase18_canonical_fiber_of_prefixes`, `Agent5.PhaseEighteenIsolation.phase18_canonical_fiber_of_observation`, `Agent5.PhaseEighteenIsolation.phase18_valid_state_isolated`, `Agent5.PhaseEighteenIsolation.phase18_high_coefficient_ten`

### FiniteObservationIsolation

*Finite original observation isolation in all ten even exterior phases*

Among original valid exterior states at the ten even phases from zero through eighteen, finite original observations isolate exactly all phase-eighteen states and the empty phase-zero state. The isolation predicate chooses one cutoff depending on the target before quantifying over every valid competitor in those ten phases, without any competing word-width bound. Observations contain the actual outgoing high normalization carry and both original literal prefixes, each with its own word width and calculated carry in the high denominator. The proof imports the existing nonisolation theorem for the eight interior phases and the phase-eighteen isolation theorem. The new lower-boundary classification proves that, for any natural phase without an upper phase bound, a valid state has first literal high output zero exactly when its phase is zero and its word is empty; this control alone isolates that state. For every nonempty valid zero-phase target and every cutoff and lower width, one arbitrarily wide canonical word works simultaneously at all ten even alternative phases, preserving the actual carry and both finite observations. The word is the existing universalWord at phase zero: append max(cutoff, lower width) zeros and then one. Nonemptiness preserves its positive first coefficient. Its validity interface allows every natural alternative phase different from one. Carry preservation allows arbitrary natural phases and unbounded coefficient words; low-prefix preservation has the same scope through the padded word width. High-prefix and joint preservation allow unbounded coefficient words at phases at most eighteen when the zero padding length is at least the cutoff. Reusable fractional prefix interfaces recover an equal-length literal output list from its highValue at positive denominators, even for improper initial fractions, and prove exact stability after replacing r/D by (scale*r+tail)/(scale*D) when D and scale are positive and 10^cutoff*tail<scale. No new normalizer, stream, or state dynamics is introduced. No optimal cutoff, isolation classification for odd target phases or phases above eighteen, equality of infinite streams, one fixed word matching all finite temporal histories, ordinary integer realization, infinite orbit, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.FiniteObservationIsolation.Classification`
- 42 modules, 11 checked endpoints
- Endpoints: `Agent5.FiniteObservationIsolation.fractionDigits_eq_of_highValue_eq`, `Agent5.FiniteObservationIsolation.fractionDigits_add_small_tail`, `Agent5.FiniteObservationIsolation.first_high_zero_iff`, `Agent5.FiniteObservationIsolation.zero_empty_state_isolated`, `Agent5.FiniteObservationIsolation.zero_extension_carry`, `Agent5.FiniteObservationIsolation.zero_extension_low`, `Agent5.FiniteObservationIsolation.zero_extension_high`, `Agent5.FiniteObservationIsolation.zero_extension_sameObservation`, `Agent5.FiniteObservationIsolation.zero_extension_valid`, `Agent5.FiniteObservationIsolation.arbitrarily_wide_zero_all_phase_same_observation`, `Agent5.FiniteObservationIsolation.finitely_isolated_iff`

### CompleteExteriorFibers

*Complete exterior stream fibers have at most two valid states*

Among original valid exterior states in the ten even phases from zero through eighteen, a pair of complete original low and high streams has at most two state representatives. The complete-stream predicate means equality of both literal prefixes at every cutoff, without supplying equality of the actual high carries; each high stream keeps its own numerator, word width and calculated carry in its denominator. A valid interior-phase target is the unique valid representative even when competitors may use either boundary phase, reusing the existing interior classification. The upper bound two is attained in both boundary phases zero and eighteen at every common word width m+3. Explicit valid words have first coefficients one and eleven, calculated high carries zero and one, equal low values and a high numerator and denominator that both scale by ten. Thus their two original streams agree at every cutoff. No decoder chosen with knowledge of the boundary phase and exact width at least three recovers every valid word from the two complete streams alone. A reusable fixed-phase recovery theorem allows every natural phase at most eighteen, including odd phases and nine: for words with coefficients at most eighteen, equality of the actual carry and original prefixes at a cutoff at least max of the two word lengths plus two determines the maximally phase-stripped words; original validity gives full word equality. Empty, untrimmed and zero-head words are included in the core theorem. The proof pads to one positive width, derives a low positional residue and an exact high positional value, and imports the published boundary rigidity instead of repeating its modulo-nine proof. This gives at most two valid representatives at each fixed natural phase at most eighteen. Extending only the missing boundary low-tail cases and importing the interior formula shows that, for words with coefficients at most eighteen, a low prefix at the same max-length-plus-two cutoff identifies the phase among the ten even phases; this yields the global two-state bound without an a priori width bound on complete-stream competitors. The explicit boundary carry interface permits any natural phase, while its value and stream collision interfaces retain the two boundary phases. No new normalizer or dynamics is introduced. No claim that every boundary state has a second representative, optimal finite cutoff, minimal collision width, phase recovery over odd or unrestricted phases, ordinary integer realization, equality of orbits, infinite dynamical conclusion, palindrome avoidance, or conclusion about 196 is made.

- Root module(s): `P196.CompleteExteriorFibers.Obstruction`
- 53 modules, 16 checked endpoints
- Endpoints: `Agent5.CompleteExteriorFibers.eq_of_low_residue_highValue`, `Agent5.CompleteExteriorFibers.same_phase_core_eq_of_observation`, `Agent5.CompleteExteriorFibers.same_phase_valid_eq_of_observation`, `Agent5.CompleteExteriorFibers.same_phase_eq_of_streams_and_carry`, `Agent5.CompleteExteriorFibers.adicNumeratorDigits_even_phase`, `Agent5.CompleteExteriorFibers.low_prefix_even_phase`, `Agent5.CompleteExteriorFibers.phase_eq_of_low_prefix`, `Agent5.CompleteExteriorFibers.phase_eq_of_complete_streams`, `Agent5.CompleteExteriorFibers.same_phase_complete_fiber_at_most_two`, `Agent5.CompleteExteriorFibers.complete_fiber_at_most_two`, `Agent5.CompleteExteriorFibers.interior_complete_fiber_singleton`, `Agent5.CompleteExteriorFibers.boundary_values`, `Agent5.CompleteExteriorFibers.boundary_carries`, `Agent5.CompleteExteriorFibers.boundary_sameStreams`, `Agent5.CompleteExteriorFibers.boundary_double_fiber`, `Agent5.CompleteExteriorFibers.no_boundary_complete_decoder`

### BoundedStreamCandidates

*Exact two-candidate decoding of bounded original stream prefixes*

An explicit total executable decoder takes arbitrary low and high input lists and a natural word-width bound N. Its output contains exactly the original valid exterior states in the ten even phases from zero through eighteen whose word length is at most N and whose two original prefixes of length N+2 equal the entire supplied lists. No phase or actual carry is supplied to the list decoder. Each high prefix retains its own numerator, original word width and calculated carry in its denominator, including improper first high terms. The output always has length at most two and has no repeated states, without any input consistency, length or digit assumptions. The decoder recovers the phase from the last low term, then tests actual-carry guesses zero and one. For each guess it works at the positive width N+1, computes candidate positional values from prefixes, chooses between the two low lifts by a modulo-nine test, applies the published recursive positional decoder and removes the phase suffix. A decidable filter checks original validity, phase membership, width, both complete finite input lists and the actual calculated carry of the candidate. This uses two positional reconstructions, without exhaustive search over words. Correctness for the actual carry guess permits every known natural phase at most eighteen, including odd phases and nine, and valid words of width at most N. The standalone low-phase recovery requires only coefficients at most eighteen and the width bound, allowing empty, untrimmed and zero-head words. The scalar lift theorem covers every natural padded width, including zero. Existing boundary collision families show that, for either phase zero or eighteen and every N at least three, some valid word of exactly width N produces an output of length exactly two. The old positional decoder, padding, quotient identities, low-tail formula and boundary collisions are imported without changing them. The result characterizes finite-prefix compatibility within the supplied width bound. No equivalence with complete-stream fibers beyond that statement, optimal cutoff, minimum collision width, runtime or bit-complexity bound, recovery without a width bound, odd or unrestricted unknown-phase recovery, ordinary integer realization, equality of orbits, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.BoundedStreamCandidates.Sharpness`
- 52 modules, 7 checked endpoints
- Endpoints: `Agent5.BoundedStreamCandidates.phaseFromLow_correct`, `Agent5.BoundedStreamCandidates.restoreLow_correct`, `Agent5.BoundedStreamCandidates.candidateAtCarry_correct`, `Agent5.BoundedStreamCandidates.mem_decodeCandidates`, `Agent5.BoundedStreamCandidates.decodeCandidates_length`, `Agent5.BoundedStreamCandidates.decodeCandidates_nodup`, `Agent5.BoundedStreamCandidates.boundary_candidates_length_two`

### CompleteStreamDecoder

*Exact decoding of complete original stream fibers from a bounded source*

An explicit total executable decoder enumerates the entire complete-stream fiber of an original valid exterior source in the ten even phases from zero through eighteen, given a natural bound N on the source word length and its two original prefixes of length N+3. Membership is equivalent to the candidate being valid, having one of those phases and sharing both complete original streams with the source. No candidate width bound is supplied, and neither phase nor actual carry is provided to the decoder. Each high stream retains its own numerator, original word width and separately calculated carry in the denominator, including improper first high terms. The function reuses the published bounded candidate decoder with width bound N+1. On arbitrary input lists it always returns at most two states and has no repetitions. A new intrinsic width theorem proves that a valid complete-stream competitor is at most one coefficient longer than its source; symmetry therefore bounds their width difference by one. It imports the existing interior singleton result and proves the two boundary cases from the centered low coordinate and the terminal trimming condition. A finite-to-complete equivalence at cutoff at least the maximum of both word lengths plus two requires only coefficient bounds of eighteen: it covers every fixed natural phase at most eighteen, including odd phases and nine, and also unknown phases among the ten even phases. It assumes neither validity, positive heads, trimmed suffixes nor equality of actual carries. A separate low-only theorem recovers the exact centered low coordinate at a fixed phase under the same coefficient and cutoff bounds. Empty words are included throughout. Explicit valid pairs prove that the extra position is necessary in both boundary phases: [11] and [1,1] in phase zero, and [11,9,7] and [1,0,18,17] in phase eighteen, with actual carries one and zero. Existing padding, positional bounds, prefix quotients, phase recovery and rational digit scaling are imported. The decoder membership theorem presupposes observations from a valid source with the supplied width bound. No isolation against unbounded finite-prefix imitators, optimal cutoff, complexity bound, decoding without a source-width bound, unrestricted unknown-phase classification, ordinary integer realization, equality of orbits, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.CompleteStreamDecoder.Decoder`
- 62 modules, 8 checked endpoints
- Endpoints: `Agent5.CompleteStreamDecoder.zValue_eq_of_low_prefix`, `Agent5.CompleteStreamDecoder.same_phase_streams_iff_prefixes`, `Agent5.CompleteStreamDecoder.same_streams_iff_prefixes`, `Agent5.CompleteStreamDecoder.complete_competitor_length_le`, `Agent5.CompleteStreamDecoder.mem_completeCandidates`, `Agent5.CompleteStreamDecoder.completeCandidates_length`, `Agent5.CompleteStreamDecoder.completeCandidates_nodup`, `Agent5.CompleteStreamDecoder.boundary_width_slack_sharp`

### OriginalStreamSuccessor

*Exact exterior successor decoding and future coalescence from original streams*

An explicit total executable function of a cutoff and two finite lists reconstructs the exact original exterior successor whenever the inputs are the original low and high prefixes of a coefficient word bounded by eighteen, its phase is one of the ten even phases from zero through eighteen, and the cutoff is at least its word length plus two. The function recovers the phase from the last low term and does not receive the actual carry. At phase eighteen it subtracts one from the high value of the complete finite high prefix and reconstructs the same number of decimal places before summing the two windows and stripping the new phase suffix. This corrects the distinction between the original terminating rational expansion and the native scan with trailing nines, including improper first high terms. A new boundary reconstruction theorem proves literal equality with the native high scan followed by its constant tail at both phases zero and eighteen; all interior assembly is imported. The fixed-phase assembly only requires cutoff at least word length plus one. Consequently two bounded-coefficient states in the ten even phases with equal original prefixes at cutoff at least the maximum of their word lengths plus two have exactly equal original successors. Equality of both complete original streams therefore implies equal successors and equal exact exterior iterates at every positive time. No validity, positive head, trimmed suffix, nonempty word, competing carry equality, or assumptions on future states are supplied to these reconstruction and coalescence theorems. Each original high stream keeps its own word width and calculated carry in the denominator. The valid phase-eighteen source [8] explicitly refutes the uncorrected stream-sum formula. Imported boundary families give, in each of phases zero and eighteen and every shared width m+3, distinct valid initial states with opposite calculated carries, identical original low and high stream histories at every time, and identical exact states at every positive time. Their initial carries differ, so this is not equality of observations that additionally record that initial carry. The function is total on arbitrary lists, but semantic correctness requires the stated source and cutoff conditions. No recognition of those conditions from arbitrary inputs, equality for unbounded finite-prefix imitators, successor injectivity, recovery of the initial carry, odd or unrestricted phase classification, optimal cutoff, complexity bound, ordinary integer realization, equality of ordinary integer orbits, palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.OriginalStreamSuccessor.Controls`
- 54 modules, 8 checked endpoints
- Endpoints: `Agent5.OriginalStreamSuccessor.boundary_high_reconstruction`, `Agent5.OriginalStreamSuccessor.outerNext_from_corrected_prefixes`, `Agent5.OriginalStreamSuccessor.successorFromPrefixes_correct`, `Agent5.OriginalStreamSuccessor.outerNext_eq_of_prefixes`, `Agent5.OriginalStreamSuccessor.outerNext_eq_of_complete_streams`, `Agent5.OriginalStreamSuccessor.outerIter_positive_eq_of_complete_streams`, `Agent5.OriginalStreamSuccessor.uncorrected_phase_eighteen_failure`, `Agent5.OriginalStreamSuccessor.boundary_full_history_ambiguity`

### BoundaryOrdinaryStreams

*Ordinary boundary digit windows and finite protected exterior histories*

At each boundary phase zero or eighteen, a valid original exterior word B other than the empty zero-phase state has a positive ordinary reverse-and-add realization for every requested cutoff and finite horizon T. Its initial pair word is exactly the original surrounded shape with empty center and gap parameter 2*T+cutoff, hence physical band length 2*T+cutoff+2 on each side and exact decimal width 2*B.length+2*(2*T+cutoff+2). At every time t through T inclusively, the terminal normalization carry of the actual ordinary transition and the separate low and high prefixes of the canonical digits at time t+1 equal the stated exterior observation of the original outerIter t. The low prefix and actual high carry retain their original definitions. The high readout applies the published phase-eighteen correction to a complete window of length B.length+1+cutoff before taking the requested cutoff. It is proved coherent under further prefix cuts, of exact requested length, and independent of which complete corrected window containing that cutoff is used. For any actual surrounded pair word with bounded exterior and middle, the complete one-step window has length B.length+1+q whenever q is at most the gap parameter plus the actual terminal carry. The original high denominator keeps the original word width and separately computed carry. Two general band normalizations isolate both decimal ends; the phase-free pairing theorem and suffix transport then prove that an actual ordinary step follows the original exterior successor, with bounded new exterior and middle and loss of at most two units of gap parameter. These conditional window and propagation theorems assume bounded coefficients and the actual ordinary pair-word representation, without extra validity or positivity premises. The positive realization theorem imports the generic mirrored-word realization and supplies its canonicality explicitly. No ordinary integer, including zero, has either protected zero bands around an empty exterior or the coherent one-digit observation of that state. Kernel controls show that directly correcting a short high prefix can fail, and that equal short original prefixes with equal actual carry can correspond to different ordinary high digits; the latter is realized by two explicit positive seeds. No single seed for all horizons, optimal cutoff or band reserve, arbitrary-phase classification, reconstruction of ordinary digits from ambiguous short input, equality or injectivity of ordinary integers, infinite palindrome avoidance, or conclusion about 196 is claimed.

- Root module(s): `P196.BoundaryOrdinaryStreams.Family`
- 70 modules, 16 checked endpoints
- Endpoints: `Agent5.BoundaryOrdinaryStreams.complete_high_window_take`, `Agent5.BoundaryOrdinaryStreams.coherentHigh_prefix`, `Agent5.BoundaryOrdinaryStreams.coherentHigh_length`, `Agent5.BoundaryOrdinaryStreams.boundary_surrounded_normalization`, `Agent5.BoundaryOrdinaryStreams.boundary_pairWord_propagation`, `Agent5.BoundaryOrdinaryStreams.ordinary_boundary_window`, `Agent5.BoundaryOrdinaryStreams.ordinary_boundary_observation`, `Agent5.BoundaryOrdinaryStreams.boundary_surrounded_orbit`, `Agent5.BoundaryOrdinaryStreams.boundary_history_of_surrounded`, `Agent5.BoundaryOrdinaryStreams.positive_boundary_surrounded_realized`, `Agent5.BoundaryOrdinaryStreams.zero_empty_surrounded_not_realizable`, `Agent5.BoundaryOrdinaryStreams.zero_empty_observation_not_realizable`, `Agent5.BoundaryOrdinaryStreams.short_high_correction_failure`, `Agent5.BoundaryOrdinaryStreams.short_original_prefix_ambiguity`, `Agent5.BoundaryOrdinaryStreams.ordinary_short_prefix_ambiguity`, `Agent5.BoundaryOrdinaryStreams.boundary_history_realized`

### Agent5EvenBaseAbsorption

Initial-validity propagation for odd m>=1, positive-head overflow within a power bound and every such window, eventual moment absorption modulo 2*(m+2), decimal sharpness and essential-assumption counterexamples; no ordinary-integer orbit bridge or all-time palindrome claim.

- Root module(s): `P196.Agent5EvenBaseAbsorption.FiniteOverflow`
- 5 modules, 47 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent5.General.InitialValidity.band_digit_bounds : ∀ (m c : Int),
  P196.Agent5.General.InitialValidity.Phase m c →
    1 ≤ c - m * P196.Agent5.General.bulkCarry m c ∧ c - m * P196.Agent5.General.bulkCarry m c < m
P196.Agent5.General.InitialValidity.phase_step : ∀ (m c : Int),
  (∃ r, m = 2 * r + 1) →
    P196.Agent5.General.InitialValidity.Phase m c →
      P196.Agent5.General.InitialValidity.Phase m (P196.Agent5.General.nextPhase m c)
P196.Agent5.General.InitialValidity.boundary_digit_bounds : ∀ (m c e : Int),
  P196.Agent5.General.InitialValidity.Phase m c →
    0 ≤ e ∧ e ≤ 1 →
      0 ≤ c + e - (m + 1) * P196.Agent5.General.bulkCarry m c ∧ c + e - (m + 1) * P196.Agent5.General.bulkCarry m c ≤ m
```
</details>

### Agent104ExactMass

Exact mass/9 zero-gap transport, finite actual-orbit digit-sum ceilings, explicit escape horizon, and Nat quadratic running-maximum bound. No palindrome, Lychrel-existence, real-limit, or optimality claim.

- Root module(s): `P196.Agent104ExactMass.Agent104FiniteMassBound`
- 6 modules, 11 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent104.ExactZeroGap.interval_nine_mass : ∀ (q : Nat → Nat) (L a k : Nat),
  a + k ≤ L → (∀ (i : Nat), a ≤ i → i < a + k → q i = 9) → 9 * k ≤ DecimalMass.wordSum q L
Agent104.ExactZeroGap.zeroBound_next_nooverflow_exact : ∀ (q : Nat → Nat) (L M K : Nat),
  FoldedDecimal.Admissible L q →
    DecimalMass.wordSum q L ≤ M →
      DecimalZeroGap.ZeroBound q L K →
        DecimalDigits.carry q L = 0 →
          DecimalZeroGap.ZeroBound (FoldedDecimal.nextColumns q L) (FoldedDecimal.nextWidth q L) (max K (max 1 (M / 9)))
Agent104.ExactZeroGap.zeroBound_next_overflow_exact : ∀ (q : Nat → Nat) (L M K : Nat),
  FoldedDecimal.Admissible L q →
    DecimalMass.wordSum q L ≤ M →
      DecimalZeroGap.ZeroBound q L K →
        DecimalDigits.carry q L = 1 →
          DecimalZeroGap.ZeroBound (FoldedDecimal.nextColumns q L) (FoldedDecimal.nextWidth q L)
            (max (K - 1) (max 2 (M / 9 + 1)))
```
</details>

## Periodic (repeated-block) words and their quotient dynamics

Numbers built from repeated digit blocks: guards, quotient paths, returns and catalogs.

### Agent1GroupIII

Seven-core GroupIII actual two-step delayed repair for all r>=1 and all canonical realizations; genuine first departure, both positive outputs safe, exact second pair word and positive witness.

- Root module(s): `P196.Agent1GroupIII.Agent1GroupIIINumeric`
- 8 modules, 5 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent1.GroupIII.component_two_step_return : ∀ (r p u v : Nat),
  P196.Agent1.GroupIII.Domain r p u v →
    (OverflowCarryNormalization.iterPairs (DelayedOverlapGate.component r p u v) (2 * r + 6) 2).fst = 2 * r + 6 ∧
      ∀ (i : Nat),
        i < 2 * r + 6 →
          (OverflowCarryNormalization.iterPairs (DelayedOverlapGate.component r p u v) (2 * r + 6) 2).snd i =
            P196.Agent1.GroupIII.returnedComponent r p u v i
P196.Agent1.GroupIII.whole_two_step_return : ∀ (r p u v : Nat),
  P196.Agent1.GroupIII.Domain r p u v →
    (OverflowCarryNormalization.iterPairs (DelayedOverlapGate.initial r p u v) (2 * r + 7) 2).fst = 2 * r + 7 ∧
      ∀ (i : Nat),
        i < 2 * r + 7 →
          (OverflowCarryNormalization.iterPairs (DelayedOverlapGate.initial r p u v) (2 * r + 7) 2).snd i =
            DelayedOverlapGate.shiftOne (P196.Agent1.GroupIII.returnedComponent r p u v) i
P196.Agent1.GroupIII.actual_intermediate_overlap_fails : ∀ (r p u v : Nat),
  P196.Agent1.GroupIII.Domain r p u v →
    ¬∀ (i : Nat),
        i < 2 * r + 7 →
          FoldedDecimal.nextColumns (DelayedOverlapGate.initial r p u v) (2 * r + 7) i =
            DelayedOverlapGate.shiftOne
              (fun j =>
                if j < 2 * r + 6 then FoldedDecimal.nextColumns (DelayedOverlapGate.component r p u v) (2 * r + 6) j
                else 0)
              i
```
</details>

### Agent1GroupIIIHandoff

Fixed original GroupIII(1,10,6): sharp second repair iff r>=2, genuine first/third departures, ordinary outputs1..4 safe for every canonical realization and nonvacuous positive witness. No time6/recurrence claim.

- Root module(s): `P196.Agent1GroupIIIHandoff.Agent1GroupIIIHandoffNumeric`
- 10 modules, 7 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
P196.Agent1.GroupIIIHandoff.time_four_overlap_iff : ∀ (r : Nat),
  1 ≤ r → (P196.Agent1.GroupIIIHandoff.OverlapAt r 4 ↔ 2 ≤ r)
P196.Agent1.GroupIIIHandoff.two_genuine_repairs : ∀ (r : Nat),
  2 ≤ r →
    ¬P196.Agent1.GroupIIIHandoff.OverlapAt r 1 ∧
      P196.Agent1.GroupIIIHandoff.OverlapAt r 2 ∧
        ¬P196.Agent1.GroupIIIHandoff.OverlapAt r 3 ∧ P196.Agent1.GroupIIIHandoff.OverlapAt r 4
P196.Agent1.GroupIIIHandoff.r1_time4_signed_defect : ∀ (i : Nat),
  i < 9 →
    ↑((OverflowCarryNormalization.iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).snd i) -
        ↑(DelayedOverlapGate.shiftOne
            (fun j =>
              if j < 8 then (OverflowCarryNormalization.iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).snd j
              else 0)
            i) =
      [1, -20, 1, 0, 0, 0, 1, -20, 1][i]!
```
</details>

### Agent1PeriodicCycleAdapter

Conditional realization of repeated copies of one supplied positive-length exact period-four full quotient cycle from original-valid initial data. Literal natural copy guards retain a fixed initial exponent and one ordinary seed for all times. Explicit safePeriodic=true at every finite cycle state supplies all-time nonpalindromicity of the successor seed through existing numeric safety. This formalizes the original METHOD section4 positive-cycle criterion. No qualifying cycle is constructed; no unconditional decimal existence, 196 result, arbitrary graph-cycle realization, safety-preservation theorem, or finite-witness quantifier swap is asserted.

- Root module(s): `P196.Agent1PeriodicCycleAdapter.Agent1PeriodicCycleNumeric`
- 30 modules, 12 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.repeatWordState : (Nat → Agent8.Word) → Nat → Nat → Agent8.Word
Agent1.Periodic.repeatWordState_zero : ∀ (x : Nat → Agent8.Word) (N : Nat), Agent1.Periodic.repeatWordState x N 0 = x 0
Agent1.Periodic.repeatWordState_succ : ∀ (x : Nat → Agent8.Word) (N : Nat),
  0 < N → x N = x 0 → ∀ (t : Nat), Agent1.Periodic.repeatWordState x N (t + 1) = x (t % N + 1)
```
</details>

### Agent1PeriodicEighteenReturn

An exact positive-length period-four quotient path from original-valid initial data with initial period [18,18,18,18] cannot return the complete tuple B,H,w. The specialized periodic-band geometry and one selected maximal-run tracking reuse unchanged RunAncestry.descendant_step, original arithmetic representation, the actual carry/clock bridge, and the positive full-return gain. There is no safety premise. No generic maximal-interval enumeration, run population renewal, whole-population extinction, nonconstant-period exclusion, safe-cycle construction, or conclusion about 196 is asserted.

- Root module(s): `P196.Agent1PeriodicEighteenReturn.Agent1PeriodicEighteenReturn`
- 31 modules, 8 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.periodic_eighteen_band_run : ∀ (B H : Agent8.Word) (k : Nat),
  0 < k →
    ∃ a b,
      RunAncestry.MaximalRun (fun j => (Agent1.Periodic.periodicWord B H [18, 18, 18, 18] k)[j]?.getD 0)
          (List.length (Agent1.Periodic.periodicWord B H [18, 18, 18, 18] k)) 18 a b ∧
        a ≤ List.length B ∧ List.length B + 4 * k ≤ b
Agent1.Periodic.periodic_eighteen_band_left_eq : ∀ (B H H' : Agent8.Word) (k k' i a b a' b' : Nat),
  RunAncestry.MaximalRun (fun j => (Agent1.Periodic.periodicWord B H [18, 18, 18, 18] k)[j]?.getD 0)
      (List.length (Agent1.Periodic.periodicWord B H [18, 18, 18, 18] k)) 18 a b →
    RunAncestry.MaximalRun (fun j => (Agent1.Periodic.periodicWord B H' [18, 18, 18, 18] k')[j]?.getD 0)
        (List.length (Agent1.Periodic.periodicWord B H' [18, 18, 18, 18] k')) 18 a' b' →
      List.length B ≤ i →
        i < List.length B + 4 * k → i < List.length B + 4 * k' → a ≤ i → i < b → a' ≤ i → i < b' → a = a'
Agent1.Periodic.quotientEighteenTrack : (Nat → Agent8.Word) →
  (Nat → Agent8.Word) → (Nat → Agent8.Word) → (Nat → Nat) → Nat → Nat → Nat → Nat × Nat
```
</details>

### Agent1PeriodicGuard

Exact all-exponent raw period-four guard extraction from literal k=3 output slices, actual digit decomposition and canonical successor-width corollary. No stripping, cycle or infinite-orbit assertion.

- Root module(s): `P196.Foundations.Agent1PeriodicGuardFacts`, `P196.Agent1PeriodicGuard.Agent1PeriodicNumeric`
- 12 modules, 10 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.normalize_periodicWord : ∀ (B H w : Agent8.Word) (k : Nat),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent8.Bounded w 18 →
        Agent8.normalize (Agent1.Periodic.periodicWord B H w (k + 3)) 0 =
          Agent1.Periodic.leftGuardDigits B w ++
                  Agent1.RepeatedBlock.pow (Agent1.Periodic.leftPeriodDigits B w) (k + 2) ++
                Agent1.Periodic.centerGuardDigits B H w ++
              Agent1.RepeatedBlock.pow (Agent1.Periodic.rightPeriodDigits B H w) (k + 2) ++
            Agent1.Periodic.rightGuardDigits B H w
Agent1.Periodic.scan_block_lengths : ∀ (B H w : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent8.Bounded w 18 →
        List.length (Agent1.Periodic.leftGuardDigits B w) = List.length B + List.length w ∧
          List.length (Agent1.Periodic.leftPeriodDigits B w) = List.length w ∧
            List.length (Agent1.Periodic.centerGuardDigits B H w) = List.length H + List.length w ∧
              List.length (Agent1.Periodic.rightPeriodDigits B H w) = List.length w ∧
                List.length (Agent1.Periodic.rightGuardDigits B H w) =
                  List.length B + Agent8.terminalCarry (Agent1.Periodic.periodicWord B H w 3) 0
Agent1.Periodic.periodic_actual_step_canonical_width : ∀ (B H w : Agent8.Word) (k : Nat),
  0 < k →
    ∀ (n : Nat) (d : Nat → Nat),
      Agent8.Bounded B 18 →
        Agent8.Bounded H 18 →
          Agent8.Bounded w 18 →
            DecimalDigits.Canonical n d (List.length (Agent1.Periodic.periodicWord B H w k)) →
              (∀ (i : Nat),
                  i < List.length (Agent1.Periodic.periodicWord B H w k) →
                    DecimalDigits.columnSum d (List.length (Agent1.Periodic.periodicWord B H w k)) i =
                      (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0) →
                ∃ d',
                  DecimalDigits.Canonical (Lychrel196.step n) d'
                    (2 * List.length B + 2 * (k * List.length w) + List.length H +
                      Agent8.terminalCarry (Agent1.Periodic.periodicWord B H w 3) 0)
```
</details>

### Agent1PeriodicGuardedPath

A supplied exact finite period-four quotient path with a natural copy schedule, literal exponent recurrence, and source guards k_i>=3 lifts an initial Canonical/full-column realization to the same ordinary seed through every endpoint. For any supplied initially original-valid finite path of length N, the literal recursive schedule starting at 2*N+3 supplies the guards and one positive canonical seed realizes all N steps. This formalizes the existing METHOD section4 finite-copy guard principle and reuses the original generic numeric representation theorem. The seed can depend on the path and N; no uniform infinite seed, safety, return existence, arbitrary abstract graph realization, affirmative interface search, or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicGuardedPath.Agent1PeriodicGuardedPath`
- 22 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.quotientPathWord : (Nat → Agent8.Word) →
  (Nat → Agent8.Word) → (Nat → Agent8.Word) → (Nat → Nat) → Nat → Agent8.Word
Agent1.Periodic.quotientPathExponent : (Nat → Agent8.Word) → (Nat → Agent8.Word) → (Nat → Agent8.Word) → Nat → Nat → Nat
Agent1.Periodic.quotient_path_guarded_step : ∀ (B H w : Nat → Agent8.Word) (k : Nat → Nat) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    (∀ (i : Nat), i < N → 3 ≤ k i) →
      (∀ (i : Nat),
          i < N →
            k (i + 1) =
              k i - 2 + Agent1.Periodic.outerPeriods (B i) (H i) (w i) +
                Agent1.Periodic.centerPeriods (B i) (H i) (w i)) →
        ∀ (i : Nat),
          i < N →
            Agent8.stepWord (Agent1.Periodic.quotientPathWord B H w k i) =
              Agent1.Periodic.quotientPathWord B H w k (i + 1)
```
</details>

### Agent1PeriodicNineCenter

For any nonempty period w and arbitrary center K, the original maximal center-strip function removes an added w/K/reverse-w wrapper, retains the same residual as stripping K, and increases the count by one. For bounded B,H and the actual mixed nine entry condition, the raw center is a nine wrapper around pair(fixedDigits H (leftEntry B) appended with rawGamma copies of 9*leftEntry B). The quotient center is that residual stripped center and its period count is the residual strip count plus one. Computed entries, clock and original executable fuel semantics are retained. No center descent, no-return obstruction, free carry assignment, qualifying cycle construction, unconditional decimal existence, or conclusion about196 is asserted.

- Root module(s): `P196.Agent1PeriodicNineCenter.Agent1PeriodicNinesCenter`
- 17 modules, 4 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.stripPeriodCenter_wrap : ∀ (w K : Agent8.Word),
  w ≠ [] →
    Agent1.Periodic.stripPeriodCenter w (w ++ K ++ List.reverse w) =
      ((Agent1.Periodic.stripPeriodCenter w K).fst, (Agent1.Periodic.stripPeriodCenter w K).snd + 1)
Agent1.Periodic.rawCenter_nines_mixed : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H [9, 9, 9, 9] = 1 →
        Agent1.Periodic.rawCenter B H [9, 9, 9, 9] =
          [9, 9, 9, 9] ++
              Agent8.pair
                (Agent8.fixedDigits H (Agent1.Periodic.leftEntry B) ++
                  List.replicate (Agent1.Periodic.rawGamma B H [9, 9, 9, 9]) (9 * Agent1.Periodic.leftEntry B)) ++
            [9, 9, 9, 9]
Agent1.Periodic.quotientCenter_nines_mixed : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H [9, 9, 9, 9] = 1 →
        Agent1.Periodic.quotientCenter B H [9, 9, 9, 9] =
          (Agent1.Periodic.stripPeriodCenter [9, 9, 9, 9]
              (Agent8.pair
                (Agent8.fixedDigits H (Agent1.Periodic.leftEntry B) ++
                  List.replicate (Agent1.Periodic.rawGamma B H [9, 9, 9, 9]) (9 * Agent1.Periodic.leftEntry B)))).fst
```
</details>

### Agent1PeriodicNineClockStrip

The original maximal center-strip algorithm retracts every center with no whole mirrored period wrapper. On a positive original QuotientPath with returned center and period, every center through the endpoint is literally normalized, without initial normalization, original validity or exterior-return assumptions. For original ValidPeriodic nine input with literal initial center normalization, actual mixed entries and actual rawGamma=1, centerPeriods=1; ClockStrip retains its prior-claim authorship and evidence. Combined with the existing exact ledger, a supplied positive original-valid full B/H/w nine return has nonempty centers and a used transition dropping center length by at least eight, excluding a source-center cap of eight. No free carry/clock model, hidden initial-normalization premise on the full-return theorem, actual cycle construction, unrestricted nonreturn, infinite ordinary orbit or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicNineClockStrip.Agent1PeriodicNinesSharpExcursion`
- 32 modules, 5 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.stripPeriodCenter_of_maximal : ∀ (w H : Agent8.Word),
  (¬∃ K, H = w ++ K ++ List.reverse w) → Agent1.Periodic.stripPeriodCenter w H = (H, 0)
Agent1.Periodic.quotient_path_return_centers_normal : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    0 < N → H N = H 0 → w N = w 0 → ∀ (i : Nat), i ≤ N → Agent1.Periodic.stripPeriodCenter (w i) (H i) = (H i, 0)
Agent1.Periodic.centerPeriods_nines_clock_one : ∀ (B H : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H [9, 9, 9, 9] →
    Agent1.Periodic.stripPeriodCenter [9, 9, 9, 9] H = (H, 0) →
      Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H [9, 9, 9, 9] = 1 →
        Agent1.Periodic.rawGamma B H [9, 9, 9, 9] = 1 → Agent1.Periodic.centerPeriods B H [9, 9, 9, 9] = 1
```
</details>

### Agent1PeriodicNineControl

One explicit finite control B=[1], H=[9,9,9,14,18,18,14,9,9,9], w=[9,9,9,9]: original ValidPeriodic; initial literal strip=(H,0); actual entry sum1; actual raw period unchanged; exactly two mirrored period pairs stripped; residual [18,18]; quotient outer [3]; next actual raw period also nine. Refutes only a blanket one-step centerPeriods<=1 bound on this original-valid initially normalized input domain with nonempty residual. No safe successor, cycle, infinite continuation, temporal descent or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicNineControl.Agent1PeriodicNinesExtraStrip`
- 15 modules, 1 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.nines_extra_strip_control : let B := [1];
let H := [9, 9, 9, 14, 18, 18, 14, 9, 9, 9];
let w := [9, 9, 9, 9];
Agent1.Periodic.ValidPeriodic B H w ∧
  Agent1.Periodic.stripPeriodCenter w H = (H, 0) ∧
    Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H w = 1 ∧
      Agent1.Periodic.rawPeriod B H w = w ∧
        Agent1.Periodic.centerPeriods B H w = 2 ∧
          Agent1.Periodic.quotientCenter B H w = [18, 18] ∧
            Agent1.Periodic.quotientOuter B H w = [3] ∧
              Agent1.Periodic.rawPeriod (Agent1.Periodic.quotientOuter B H w) (Agent1.Periodic.quotientCenter B H w)
                  (Agent1.Periodic.rawPeriod B H w) =
                w
```
</details>

### Agent1PeriodicNineCycle

An exact finite quotient path whose initial and final periods both equal [9,9,9,9] retains that period at every intermediate state, including the zero-length case. For an original-valid positive-length full-tuple return starting with that period, finite per-state safety follows without a supplied safety premise; the existing fixed-cycle soundness adapter then supplies one positive ordinary Lychrel seed conditionally on that return. The local canonical nine-band nonpalindrome statement requires positive exponent and full finite column representation. No concrete cycle is constructed, no unconditional Lychrel seed or 196 conclusion is asserted, and no constant-nine no-return theorem or generic run ancestry is claimed.

- Root module(s): `P196.Agent1PeriodicNineCycle.Agent1PeriodicNinesCycle`
- 34 modules, 5 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.quotient_path_nines_phase : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    w 0 = [9, 9, 9, 9] → w N = [9, 9, 9, 9] → ∀ (i : Nat), i ≤ N → w i = [9, 9, 9, 9]
Agent1.Periodic.quotient_path_nines_entry_sum : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    w 0 = [9, 9, 9, 9] →
      w N = [9, 9, 9, 9] →
        ∀ (i : Nat), i < N → Agent1.Periodic.leftEntry (B i) + Agent1.Periodic.rightEntry (B i) (H i) [9, 9, 9, 9] = 1
Agent1.Periodic.periodic_nines_input_nonpalindrome : ∀ (B H : Agent8.Word) (k n : Nat) (d : Nat → Nat),
  0 < k →
    DecimalDigits.Canonical n d (List.length (Agent1.Periodic.periodicWord B H [9, 9, 9, 9] k)) →
      (∀ (i : Nat),
          i < List.length (Agent1.Periodic.periodicWord B H [9, 9, 9, 9] k) →
            DecimalDigits.columnSum d (List.length (Agent1.Periodic.periodicWord B H [9, 9, 9, 9] k)) i =
              (Agent1.Periodic.periodicWord B H [9, 9, 9, 9] k)[i]?.getD 0) →
        ¬Lychrel196.Palindrome n
```
</details>

### Agent1PeriodicNineExcursion

Exact actual additional-strip/clock ledger for the all-nine four-entry phase, retaining original carry scans, whole-word clock and maximal center stripping. For a supplied positive-length original QuotientPath with original initial ValidPeriodic, initial all-nine period and exact B/H/w endpoint return, all centers through the endpoint are nonempty and some used transition decreases center length by at least seven; hence the maximum center length is at least eight and an everywhere-at-most-seven center cap excludes such a return. No initial maximal center-normalization premise, free carry/clock model, cycle construction, unrestricted nonreturn theorem, infinite ordinary orbit or 196 conclusion. Optional separate local sharpness controls are not included unless imported by the actual root.

- Root module(s): `P196.Agent1PeriodicNineExcursion.Agent1PeriodicNinesExcursion`
- 29 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.ninesExtraStrips : Agent8.Word → Agent8.Word → Nat
Agent1.Periodic.ninesExtraSum : (Nat → Agent8.Word) → (Nat → Agent8.Word) → Nat → Nat
Agent1.Periodic.quotientCenter_nines_length_balance : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H [9, 9, 9, 9] = 1 →
        List.length (Agent1.Periodic.quotientCenter B H [9, 9, 9, 9]) + 8 * Agent1.Periodic.ninesExtraStrips B H =
          List.length H + Agent1.Periodic.rawGamma B H [9, 9, 9, 9]
```
</details>

### Agent1PeriodicOuterCatalog

Actual original-valid period-four maximal quotient transitions project into the retained 878-state/1458-labelled-edge physical-outside/phase product, preserving the actual clock, exceptional all-nine labels, original validity and catalog membership. Complete outer-image deduplication is retained. One-way coverage only; no arbitrary abstract path realizability, all-vertex reachability, interface return, safety closure or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicOuterCatalog.Agent1PeriodicOuterCatalog`
- 25 modules, 18 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.outside_bounds : ∀ (B H w : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H w → 0 < Agent1.Periodic.outside B w ∧ Agent1.Periodic.outside B w ≤ 18
Agent1.Periodic.quotient_outside_step : ∀ (B H w : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H w →
    let e := Agent8.lastInput (Agent1.Periodic.periodicWord B H w 3);
    e ≤ 1 ∧
      Agent1.Periodic.rawGamma B H w = Agent8.overflow (Agent1.Periodic.outside B w) e ∧
        Agent1.Periodic.outside (Agent1.Periodic.quotientOuter B H w) (Agent1.Periodic.rawPeriod B H w) =
          Agent8.nextExterior (Agent1.Periodic.outside B w) e
Agent1.Periodic.mem_outerImages_of_actual : ∀ (q e : Nat),
  e ≤ 1 → Agent8.nextExterior q e ∈ Agent1.Periodic.outerImages q (Agent8.overflow q e)
```
</details>

### Agent1PeriodicPhaseCatalog

Actual bounded period-four raw transitions project into the exact retained59-phase124-labelled-edge catalog, retaining actual clock and exceptional all-nine boundary carries; original quotient validity and catalog membership are preserved. One-way coverage only; no arbitrary abstract path realizability, all-vertex reachability, safety closure or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicPhaseCatalog.Agent1PeriodicPhaseCatalog`
- 20 modules, 9 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.rawPeriod_eq_phaseImage : ∀ (B H w : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent8.Bounded w 18 →
        List.length w = 4 →
          w ≠ [9, 9, 9, 9] →
            Agent1.Periodic.rawPeriod B H w = Agent1.Periodic.phaseImage w (Agent1.Periodic.rawGamma B H w)
Agent1.Periodic.rawPeriod_nines : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent1.Periodic.rawPeriod B H [9, 9, 9, 9] =
        List.replicate 4 (18 - 9 * (Agent1.Periodic.leftEntry B + Agent1.Periodic.rightEntry B H [9, 9, 9, 9]))
Agent1.Periodic.phaseEdges_spec : Agent1.Periodic.phaseEdges =
  List.flatMap Agent1.Periodic.phaseOutputs Agent1.Periodic.phaseCatalog
```
</details>

### Agent1PeriodicPrefixSaturation

Necessary actual three-column projection of the original maximal period-four quotient, followed by reuse of the existing checked saturated eight-state prefix profile. For positive complete-tuple returns from period [14,14,4,4], derive strict unsaturation and positive gain G with clock=8G, signed shift=G, and 16G<N<=32G, hence N>=17. No generic saturation/profile reproof, odd-control balance, arbitrary graph realization, safety closure, saved outside-17/8 witness rejection, cycle existence or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicPrefixSaturation.Agent1PeriodicInitialUnsaturated`
- 58 modules, 9 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.firstThree_periodicWord : ∀ (B H w : Agent8.Word) (k : Nat),
  List.length w = 4 → 1 ≤ k → Agent8.firstThree (Agent1.Periodic.periodicWord B H w k) = Agent8.firstThree (B ++ w)
Agent1.Periodic.physicalPrefix_a : ∀ (B w : Agent8.Word),
  List.length w = 4 → (Agent1.Periodic.physicalPrefix B w).a = Agent1.Periodic.outside B w
Agent1.Periodic.physicalPrefix_valid : ∀ (B H w : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H w → P196.Agent4.Saturation.Valid (Agent1.Periodic.physicalPrefix B w)
```
</details>

### Agent1PeriodicQuotient

Exact executable maximal whole-period stripping, original rawguard composition for every exponent k>=3, and signed width balance; no safety/domain preservation or cycle claim.

- Root module(s): `P196.Foundations.Agent1PeriodicQuotient`
- 14 modules, 9 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.stripPeriodSuffix_spec : ∀ (w B : Agent8.Word),
  w ≠ [] →
    B =
      (Agent1.Periodic.stripPeriodSuffix w B).fst ++
        Agent1.RepeatedBlock.pow w (Agent1.Periodic.stripPeriodSuffix w B).snd
Agent1.Periodic.stripPeriodSuffix_maximal : ∀ (w B : Agent8.Word),
  w ≠ [] → ¬∃ D, (Agent1.Periodic.stripPeriodSuffix w B).fst = D ++ w
Agent1.Periodic.stripPeriodCenter_decomposition : ∀ (w H : Agent8.Word),
  H =
    Agent1.RepeatedBlock.pow w (Agent1.Periodic.stripPeriodCenter w H).snd ++
        (Agent1.Periodic.stripPeriodCenter w H).fst ++
      Agent1.RepeatedBlock.pow (List.reverse w) (Agent1.Periodic.stripPeriodCenter w H).snd
```
</details>

### Agent1PeriodicReducedCore

An exact positive-length full quotient return from original-valid initial data with explicit initial outerCatalog membership has one constant outerComponent label in [8,129], at every state through the endpoint. Existing quotient_return_core supplies catalog membership and component constancy. The structural label-130 converse and unchanged constant-eighteen no-return theorem remove that label. No concrete return or safe cycle is constructed; neither remaining component is excluded; catalog membership is not inferred for an arbitrary original-valid input; no 196 conclusion is asserted.

- Root module(s): `P196.Agent1PeriodicReducedCore.Agent1PeriodicReturnReducedCore`
- 48 modules, 2 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.outerComponent_eighteen_phase : ∀ (s : Agent1.Periodic.OuterNode),
  Agent1.Periodic.outerComponent s = 130 → s.fst = [18, 18, 18, 18]
Agent1.Periodic.quotient_return_reduced_core : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      (w 0, Agent1.Periodic.outside (B 0) (w 0)) ∈ Agent1.Periodic.outerCatalog →
        0 < N →
          B N = B 0 ∧ H N = H 0 ∧ w N = w 0 →
            ∃ c,
              c ∈ [8, 129] ∧
                ∀ (i : Nat),
                  i ≤ N →
                    (w i, Agent1.Periodic.outside (B i) (w i)) ∈ Agent1.Periodic.returnCore ∧
                      Agent1.Periodic.outerComponent (w i, Agent1.Periodic.outside (B i) (w i)) = c
```
</details>

### Agent1PeriodicReturnClock

Necessary clock and signed exponent-gain bounds for finite exact period-four quotient paths, using the original ValidPeriodic predicate and actual outside coefficient/carry. Reuse Agent8 exterior potential bounds and the existing exact width identity. No catalog premise, cycle existence, arbitrary graph realization, safety preservation, unguarded natural exponent trajectory, temporal-period divisibility, or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicReturnClock.Agent1PeriodicReturnClock`
- 21 modules, 4 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.quotient_path_valid : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      ∀ (i : Nat), i ≤ N → Agent1.Periodic.ValidPeriodic (B i) (H i) (w i)
Agent1.Periodic.quotient_path_closed_outside_clock_bounds : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      Agent1.Periodic.outside (B N) (w N) = Agent1.Periodic.outside (B 0) (w 0) →
        2 * Agent1.Periodic.quotientClockSum B H w N ≤ N ∧ N ≤ 4 * Agent1.Periodic.quotientClockSum B H w N
Agent1.Periodic.quotient_return_clock_gain : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      0 < N →
        B N = B 0 ∧ H N = H 0 ∧ w N = w 0 →
          ∃ G,
            0 < G ∧
              Agent1.Periodic.quotientClockSum B H w N = 8 * G ∧
                Agent1.Periodic.quotientDeltaSum B H w N = ↑G ∧ 16 * G ≤ N ∧ N ≤ 32 * G
```
</details>

### Agent1PeriodicReturnCore

Positive complete tuple returns of exact finite original-valid catalog-supported period-four quotient paths remain in one of the retained nonzero component classes 8,129,130. Initial phase [14,14,4,4] therefore requires physical outside 9 or 10. The certificate checks local rank and internal-edge restrictions, not SCC maximality or reachability. Zero-period paths are identified with the existing zeroStateOrbit and its no-return theorem. No cycle existence, arbitrary graph realization, safety, all-time ordinary orbit, constant-eighteen acyclicity or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicReturnCore.Agent1PeriodicReturnCore`
- 38 modules, 14 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.componentRank_pos : ∀ (c : Nat), 0 < Agent1.Periodic.componentRank c
Agent1.Periodic.outerEdge_rank_le : ∀ (e : Agent1.Periodic.OuterEdge),
  e ∈ Agent1.Periodic.outerEdges →
    Agent1.Periodic.componentRank (Agent1.Periodic.outerComponent e.target) ≤
      Agent1.Periodic.componentRank (Agent1.Periodic.outerComponent e.source)
Agent1.Periodic.outerEdge_rank_drop : ∀ (e : Agent1.Periodic.OuterEdge),
  e ∈ Agent1.Periodic.outerEdges →
    Agent1.Periodic.outerComponent e.source ≠ Agent1.Periodic.outerComponent e.target →
      1 + Agent1.Periodic.componentRank (Agent1.Periodic.outerComponent e.target) ≤
        Agent1.Periodic.componentRank (Agent1.Periodic.outerComponent e.source)
```
</details>

### Agent1PeriodicReturnUpperGap

Unchanged phase-catalog incoming initial-phase clock1, transported to the last literal quotient step; existing initial outside9/10 and original scalar lower-potential slack give N+2<=4C for positive complete initial-phase returns. The open actual quotient potential adapter reuses original local exterior bounds. No generic lower3/equality classifier, arbitrary-walk realization, safety, return existence or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicReturnUpperGap.Agent1PeriodicReturnUpper`
- 41 modules, 5 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.phaseEdge_initial_clock : ∀ (e : Agent1.Periodic.PhaseEdge),
  e ∈ Agent1.Periodic.phaseEdges → e.target = [14, 14, 4, 4] → e.clock = 1
Agent1.Periodic.quotient_return_initial_last_clock : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      w 0 = [14, 14, 4, 4] →
        0 < N → B N = B 0 ∧ H N = H 0 ∧ w N = w 0 → Agent1.Periodic.rawGamma (B (N - 1)) (H (N - 1)) (w (N - 1)) = 1
Agent1.Periodic.quotient_path_lower_potential : ∀ (B H w : Nat → Agent8.Word) (N : Nat),
  Agent1.Periodic.QuotientPath B H w N →
    Agent1.Periodic.ValidPeriodic (B 0) (H 0) (w 0) →
      ↑N ≤
        4 * ↑(Agent1.Periodic.quotientClockSum B H w N) + Agent8.lowerPotential (Agent1.Periodic.outside (B 0) (w 0)) -
          Agent8.lowerPotential (Agent1.Periodic.outside (B N) (w N))
```
</details>

### Agent1PeriodicSafety

Exact original periodic safe Boolean vs BadWord and every canonical next output for k>0; maximalstrip invariance and concrete valid safe-input/unsafe-successor plus k0 counterexamples. No forward safe closure/infiniteorbit.

- Root module(s): `P196.Agent1PeriodicSafety.Agent1PeriodicSafetyNumeric`, `P196.Agent1PeriodicSafety.Agent1PeriodicSafetyBoundary`
- 21 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.safePeriodic_iff_not_bad : ∀ (B H w : Agent8.Word) (k : Nat),
  0 < k →
    w ≠ [] →
      (Agent1.Periodic.safePeriodic B H w = true ↔
        ¬FoldedDecimal.BadWord (List.length (Agent1.Periodic.periodicWord B H w k)) fun i =>
            (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0)
Agent1.Periodic.safePeriodic_strip : ∀ (B H w : Agent8.Word),
  w ≠ [] →
    Agent1.Periodic.safePeriodic (Agent1.Periodic.stripPeriodSuffix w B).fst (Agent1.Periodic.stripPeriodCenter w H).fst
        w =
      Agent1.Periodic.safePeriodic B H w
Agent1.Periodic.safePeriodic_quotient_eq_raw : ∀ (B H w : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H w →
    Agent1.Periodic.safePeriodic (Agent1.Periodic.quotientOuter B H w) (Agent1.Periodic.quotientCenter B H w)
        (Agent1.Periodic.rawPeriod B H w) =
      Agent1.Periodic.safePeriodic (Agent1.Periodic.rawOuter B H w) (Agent1.Periodic.rawCenter B H w)
        (Agent1.Periodic.rawPeriod B H w)
```
</details>

### Agent1PeriodicValidity

Exact original ValidPeriodic preservation of raw and maximal quotient state, all inputvalidfields and both carrycases retained. One exact step yields valid successor and positive exponent; no safety/futurethreshold/iteration claim.

- Root module(s): `P196.Foundations.Agent1PeriodicValidity`
- 17 modules, 10 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.pair_middle_even : ∀ (D : Agent8.Word),
  List.length D % 2 = 1 → (Agent8.pair D)[List.length D / 2]?.getD 0 % 2 = 0
Agent1.Periodic.stripPeriodCenter_even : ∀ (w H : Agent8.Word),
  (List.length H % 2 = 1 → H[List.length H / 2]?.getD 0 % 2 = 0) →
    List.length (Agent1.Periodic.stripPeriodCenter w H).fst % 2 = 1 →
      (Agent1.Periodic.stripPeriodCenter w H).fst[List.length (Agent1.Periodic.stripPeriodCenter w H).fst / 2]?.getD 0 %
          2 =
        0
Agent1.Periodic.raw_center_even : ∀ (B H w : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent8.Bounded w 18 →
        List.length w = 4 →
          List.length (Agent1.Periodic.rawCenter B H w) % 2 = 1 →
            (Agent1.Periodic.rawCenter B H w)[List.length (Agent1.Periodic.rawCenter B H w) / 2]?.getD 0 % 2 = 0
```
</details>

### Agent1PeriodicWidthProjection

The compositional eight-residue lift of the original 878-node/1458-labelled-edge outside/phase catalog has 7024 distinct nodes and 11664 labelled edge-list entries. Every actual valid catalog-supported maximal period-four quotient projects to an edge preserving actual terminal carry and exceptional all-nine labels, with width residue advanced by that carry. Separately, finite literal quotient paths telescope signed interface width; equal endpoint interface widths force overflow count divisible by eight and total signed increment equal to overflow count divided by eight. No temporal-period divisibility, positive clock count, saved traversal order, reachability/SCC equality, arbitrary abstract path realization, guarded all-time exponent trajectory, safety closure, finite-interface return existence or 196 conclusion. Original Canonical input digits identify decimal-length residue for every copy count; with positive copy count and the complete original column-sum realization, the actual ordinary successor decimal-length residue equals that of the quotient interface. This does not assert the small-copy-count whole-word quotient formula.

- Root module(s): `P196.Agent1PeriodicWidthProjection.Agent1PeriodicWidthLift`, `P196.Foundations.Agent1PeriodicWidthPath`, `P196.Agent1PeriodicWidthProjection.Agent1PeriodicWidthNumeric`
- 30 modules, 16 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.widthResidue_lt : ∀ (B H : Agent8.Word), Agent1.Periodic.widthResidue B H < 8
Agent1.Periodic.periodicWord_length_mod_eight : ∀ (B H w : Agent8.Word) (k : Nat),
  List.length w = 4 → List.length (Agent1.Periodic.periodicWord B H w k) % 8 = (2 * List.length B + List.length H) % 8
Agent1.Periodic.quotient_width_mod_eight : ∀ (B H w : Agent8.Word),
  Agent8.Bounded B 18 →
    Agent8.Bounded H 18 →
      Agent8.Bounded w 18 →
        List.length w = 4 →
          (2 * List.length (Agent1.Periodic.quotientOuter B H w) + List.length (Agent1.Periodic.quotientCenter B H w)) %
              8 =
            (2 * List.length B + List.length H + Agent1.Periodic.rawGamma B H w) % 8
```
</details>

### Agent1PeriodicZeroCycle

Exact literal maximal zero-period quotient has no positive return from any original ValidPeriodic state, without a safety premise. Every positive-exponent valid periodic word is ordinarily realizable. Does not prove palindrome termination, nonzero-period acyclicity, or the 196 conjecture.

- Root module(s): `P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroCycle`
- 24 modules, 7 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.periodicWord_admissible : ∀ (B H w : Agent8.Word) (k : Nat),
  Agent1.Periodic.ValidPeriodic B H w →
    0 < k →
      FoldedDecimal.Admissible (List.length (Agent1.Periodic.periodicWord B H w k)) fun i =>
        (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0
Agent1.Periodic.periodicWord_realizable : ∀ (B H w : Agent8.Word) (k : Nat),
  Agent1.Periodic.ValidPeriodic B H w →
    0 < k →
      ∃ n d,
        0 < n ∧
          DecimalDigits.Canonical n d (List.length (Agent1.Periodic.periodicWord B H w k)) ∧
            ∀ (i : Nat),
              i < List.length (Agent1.Periodic.periodicWord B H w k) →
                DecimalDigits.columnSum d (List.length (Agent1.Periodic.periodicWord B H w k)) i =
                  (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0
Agent1.Periodic.rawPeriod_zero : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 → Agent8.Bounded H 18 → Agent1.Periodic.rawPeriod B H [0, 0, 0, 0] = [0, 0, 0, 0]
```
</details>

### Agent1PeriodicZeroEscape

For every original valid zero-period exact quotient state and every natural cap M, some interface width exceeds M by the original explicit escapeBound(initial width at exponent M+3,9*M). No safety, initial-cap, or positive-cap hypothesis. No palindrome or 196 conclusion.

- Root module(s): `P196.Agent1PeriodicZeroEscape.Agent1PeriodicZeroEscape`
- 26 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.zeroExponent_guarded_prefix : ∀ (s : Agent1.Periodic.ZeroState),
  Agent1.Periodic.ValidPeriodic s.fst s.snd [0, 0, 0, 0] →
    ∀ (M N : Nat),
      (∀ (t : Nat),
          t ≤ N →
            2 * List.length (Agent1.Periodic.zeroStateOrbit s t).fst +
                List.length (Agent1.Periodic.zeroStateOrbit s t).snd ≤
              M) →
        ∀ (t : Nat),
          t ≤ N →
            3 ≤ Agent1.Periodic.zeroExponent s (M + 3) t ∧
              M + 24 ≤
                2 * List.length (Agent1.Periodic.zeroStateOrbit s t).fst +
                    List.length (Agent1.Periodic.zeroStateOrbit s t).snd +
                  8 * Agent1.Periodic.zeroExponent s (M + 3) t
Agent1.Periodic.zeroLiftWord_step_prefix : ∀ (s : Agent1.Periodic.ZeroState),
  Agent1.Periodic.ValidPeriodic s.fst s.snd [0, 0, 0, 0] →
    ∀ (M N : Nat),
      (∀ (t : Nat),
          t ≤ N →
            2 * List.length (Agent1.Periodic.zeroStateOrbit s t).fst +
                List.length (Agent1.Periodic.zeroStateOrbit s t).snd ≤
              M) →
        ∀ (t : Nat),
          t < N →
            Agent8.stepWord (Agent1.Periodic.zeroLiftWord s (M + 3) t) = Agent1.Periodic.zeroLiftWord s (M + 3) (t + 1)
Agent1.Periodic.zero_interface_mass_le : ∀ (B H : Agent8.Word),
  Agent1.Periodic.ValidPeriodic B H [0, 0, 0, 0] →
    2 * List.sum B + List.sum H ≤ 18 * (2 * List.length B + List.length H)
```
</details>

### Agent1PeriodicZeroFoundation

Checked pointwise ordinary realizability of ValidPeriodic and exact zero-period stability. Full zero-quotient acyclicity remains WIP outside the current roots.

- Root module(s): `P196.Foundations.Agent1PeriodicRealizability`, `P196.Foundations.Agent1PeriodicZeroPeriod`
- 19 modules, 4 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.periodicWord_admissible : ∀ (B H w : Agent8.Word) (k : Nat),
  Agent1.Periodic.ValidPeriodic B H w →
    0 < k →
      FoldedDecimal.Admissible (List.length (Agent1.Periodic.periodicWord B H w k)) fun i =>
        (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0
Agent1.Periodic.periodicWord_realizable : ∀ (B H w : Agent8.Word) (k : Nat),
  Agent1.Periodic.ValidPeriodic B H w →
    0 < k →
      ∃ n d,
        0 < n ∧
          DecimalDigits.Canonical n d (List.length (Agent1.Periodic.periodicWord B H w k)) ∧
            ∀ (i : Nat),
              i < List.length (Agent1.Periodic.periodicWord B H w k) →
                DecimalDigits.columnSum d (List.length (Agent1.Periodic.periodicWord B H w k)) i =
                  (Agent1.Periodic.periodicWord B H w k)[i]?.getD 0
Agent1.Periodic.rawPeriod_zero : ∀ (B H : Agent8.Word),
  Agent8.Bounded B 18 → Agent8.Bounded H 18 → Agent1.Periodic.rawPeriod B H [0, 0, 0, 0] = [0, 0, 0, 0]
```
</details>

### Agent1PeriodicZeroWidthLoop

An explicit sixteen-edge labelled closed walk with eight clocks in the necessary width projection starts at the projection of an original-valid canonically realizable zero-period template. Every positive exact full quotient path from that initial tuple fails to return. No claim that an actual orbit follows the selected abstract walk, no nonpalindromicity or all-time safety, and no196 conclusion.

- Root module(s): `P196.Agent1PeriodicZeroWidthLoop.Agent1PeriodicZeroWidthLoop`
- 37 modules, 11 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.Periodic.zeroWidthEdge_mem : ∀ (t : Nat), Agent1.Periodic.zeroWidthEdge t ∈ Agent1.Periodic.widthEdges
Agent1.Periodic.zeroWidthEdge_labels : ∀ (t : Nat),
  t < 16 →
    (Agent1.Periodic.zeroWidthEdge t).source = Agent1.Periodic.zeroWidthNode t ∧
      (Agent1.Periodic.zeroWidthEdge t).target = Agent1.Periodic.zeroWidthNode (t + 1) ∧
        (Agent1.Periodic.zeroWidthEdge t).clock = t % 2 ∧ (Agent1.Periodic.zeroWidthEdge t).carries = none
Agent1.Periodic.zeroWidthNode_mem : ∀ (t : Nat), Agent1.Periodic.zeroWidthNode t ∈ Agent1.Periodic.widthCatalog
```
</details>

### Agent1Pr104Repair

Original Agent114 six short-r firsteleven theorems with isolated timezero proofrepair, no statementchange.

- Root module(s): `P196.Agent1Pr104Repair.Agent114ShortRFirst11`
- 7 modules, 6 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent114.ShortR.common_first_step : ∀ (r n : Nat) (d : Nat → Nat),
  DecimalDigits.Canonical n d (2 * r + 7) →
    (∀ (i : Nat), i < 2 * r + 7 → DecimalDigits.columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r 1 1 6 i) →
      Lychrel196.step n = DecimalDigits.value (DelayedOverlapGate.initial r 1 1 6) (2 * r + 7)
Agent114.ShortR.r1_to_r4_initial_not_palindrome : ∀ (r n : Nat) (d : Nat → Nat),
  1 ≤ r ∧ r ≤ 4 →
    DecimalDigits.Canonical n d (2 * r + 7) →
      (∀ (i : Nat), i < 2 * r + 7 → DecimalDigits.columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r 1 1 6 i) →
        ¬Lychrel196.Palindrome n
Agent114.ShortR.r1_first_eleven : ∀ (n : Nat) (d : Nat → Nat),
  DecimalDigits.Canonical n d 9 →
    (∀ (i : Nat), i < 9 → DecimalDigits.columnSum d 9 i = DelayedOverlapGate.initial 1 1 1 6 i) →
      ∀ (t : Nat), 1 ≤ t → t ≤ 11 → ¬Lychrel196.Palindrome (Lychrel196.orbit n t)
```
</details>

### Agent1RepeatedBlock

Exact repeated-block normalization, fixed contexts, independent two-band carry invariance and symmetric normalized-list length. No canonical integer-width, quotient-cycle or all-time orbit claim.

- Root module(s): `P196.Agent1RepeatedBlock.Agent1RepeatedBlockBoundary`
- 8 modules, 14 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent1.RepeatedBlock.normalize_pow_succ : ∀ (w : Agent8.Word) (e k : Nat),
  Agent8.Bounded w 18 →
    e ≤ 1 →
      Agent8.normalize (Agent1.RepeatedBlock.pow w (k + 1)) e =
        Agent8.fixedDigits w e ++ Agent1.RepeatedBlock.pow (Agent8.fixedDigits w (Agent8.terminalCarry w e)) k ++
          if Agent8.terminalCarry w e = 0 then [] else [Agent8.terminalCarry w e]
Agent1.RepeatedBlock.normalize_context : ∀ (B w H : Agent8.Word) (e k : Nat),
  Agent8.Bounded B 18 →
    Agent8.Bounded w 18 →
      e ≤ 1 →
        Agent8.normalize (B ++ Agent1.RepeatedBlock.pow w (k + 1) ++ H) e =
          Agent8.fixedDigits B e ++ Agent8.fixedDigits w (Agent8.terminalCarry B e) ++
              Agent1.RepeatedBlock.pow (Agent8.fixedDigits w (Agent8.terminalCarry w (Agent8.terminalCarry B e))) k ++
            Agent8.normalize H (Agent8.terminalCarry w (Agent8.terminalCarry B e))
Agent1.RepeatedBlock.terminalCarry_symmetric_bands : ∀ (B w H : Agent8.Word) (e k : Nat),
  Agent8.Bounded B 18 →
    Agent8.Bounded w 18 →
      Agent8.Bounded H 18 →
        e ≤ 1 →
          Agent8.terminalCarry
              (B ++ Agent1.RepeatedBlock.pow w (k + 1) ++ H ++ Agent1.RepeatedBlock.pow (List.reverse w) (k + 1) ++
                List.reverse B)
              e =
            Agent8.terminalCarry (B ++ w ++ H ++ List.reverse w ++ List.reverse B) e
```
</details>

## Affine run words

Digit words made of runs whose lengths are affine in a parameter: equality/palindrome decisions and uniform returns.

### Agent102AffineBoundary

Explicit affine run-word boundary examples, including failure of a template-independent uniform cutoff.

- Root module(s): `P196.Agent102AffineBoundary.Agent102AffineBoundary`
- 4 modules, 12 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent102.AffineBoundary.wordAt_moving : ∀ (k : Nat),
  Agent102.wordAt Agent102.AffineBoundary.moving k = List.replicate k 1
Agent102.AffineBoundary.wordAt_fixed : ∀ (N k : Nat),
  Agent102.wordAt (Agent102.AffineBoundary.fixed N) k = List.replicate N 1
Agent102.AffineBoundary.moving_fixed_eq_iff : ∀ (k N : Nat),
  Agent102.wordAt Agent102.AffineBoundary.moving k = Agent102.wordAt (Agent102.AffineBoundary.fixed N) k ↔ k = N
```
</details>

### Agent102AffineParameterIntervals

Exact finite interval unions for equality and palindrome parameters of actual Int.toNat-clipped affine run words; no cutoff prefix enumeration; complete quantified decisions and extensional interval certificates.

- Root module(s): `P196.Agent102AffineParameterIntervals.Agent102ParameterSetControls`
- 13 modules, 138 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent102.Affine.eval_zero : ∀ (k : Nat), Agent102.Affine.zero.eval k = 0
Agent102.Affine.eval_add : ∀ (f g : Agent102.Affine) (k : Nat), (f.add g).eval k = f.eval k + g.eval k
Agent102.Affine.intercept_bounds_of_cutoff : ∀ (f : Agent102.Affine) (k : Nat),
  f.cutoff ≤ k → -↑k < f.intercept ∧ f.intercept < ↑k
```
</details>

### Agent102AffineRuns

Literal affine run words: exact coverage, clipped-length endpoints, computable eventual equality and palindrome dichotomies.

- Root module(s): `P196.Agent102AffineBoundary.Agent102AffineBoundary`, `P196.Agent102AffineRuns.Agent102AffineDecision`
- 7 modules, 96 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent102.Affine.eval_zero : ∀ (k : Nat), Agent102.Affine.zero.eval k = 0
Agent102.Affine.eval_add : ∀ (f g : Agent102.Affine) (k : Nat), (f.add g).eval k = f.eval k + g.eval k
Agent102.Affine.intercept_bounds_of_cutoff : ∀ (f : Agent102.Affine) (k : Nat),
  f.cutoff ≤ k → -↑k < f.intercept ∧ f.intercept < ↑k
```
</details>

### Agent102AffineScalar

Explicit eventual positive-part identity and lexicographic comparison stability for arbitrary integer-affine functions on Nat parameters. This checkpoint alone proves no run-word equality stabilization or decimal 196 orbit claim.

- Root module(s): `P196.Agent102AffineScalar.Agent102AffineArithmetic`
- 2 modules, 17 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent102.Affine.eval_zero : ∀ (k : Nat), Agent102.Affine.zero.eval k = 0
Agent102.Affine.eval_add : ∀ (f g : Agent102.Affine) (k : Nat), (f.add g).eval k = f.eval k + g.eval k
Agent102.Affine.intercept_bounds_of_cutoff : ∀ (f : Agent102.Affine) (k : Nat),
  f.cutoff ≤ k → -↑k < f.intercept ∧ f.intercept < ↑k
```
</details>

### Agent102AllParameterDecisions

Exact compressed literal-run equality at arbitrary parameters; sound and complete universal/existential equality and palindrome decisions from finite prefix and proven tail; concrete kernel controls.

- Root module(s): `P196.Agent102AllParameterDecisions.Agent102AllParameterControls`
- 10 modules, 144 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent102.Affine.eval_zero : ∀ (k : Nat), Agent102.Affine.zero.eval k = 0
Agent102.Affine.eval_add : ∀ (f g : Agent102.Affine) (k : Nat), (f.add g).eval k = f.eval k + g.eval k
Agent102.Affine.intercept_bounds_of_cutoff : ∀ (f : Agent102.Affine) (k : Nat),
  f.cutoff ≤ k → -↑k < f.intercept ∧ f.intercept < ↑k
```
</details>

### Agent105AffineComponents

*Supporting interfaces for actual affine-run dynamics*

Supporting interfaces only: actual expanded affine-run word operations, finite-tail predicate selection, and explicit-hypothesis return-time/width bounds for the original Agent8 list orbit. This scoped build does not assert the complete actual uniform-return theorem or ordinary-integer realization.

- Root module(s): `P196.Agent105AffineComponents.Agent105AffineBasics`, `P196.Agent105AffineComponents.Agent105TailSelection`, `P196.Agent105AffineComponents.Agent105ReturnTimeBound`
- 6 modules, 40 checked endpoints
- Claim `agent105-8f1107db019a-affinebasics`: Actual expanded run-word append/reverse/bounded-symbol interfaces using unchanged Agent102.RunSpec and wordAt.
- Claim `agent105-8f1107db019a-tailselection`: Finite positive-time selection from explicit eventual cover and eventual stability predicates, including conjunction, negation, bounded safety, and list-indexed universal quantification.
- Claim `agent105-8f1107db019a-returntimebound`: Original Agent8 list-orbit potential and width inequalities, with explicit canonicality, return, equal-head, endpoint-width and positive-time hypotheses; includes the conditional 4*A*s bound.

<details><summary>Main statements (Lean)</summary>

```lean
Agent105.AffineDynamics.wordAt_nil : ∀ (k : Nat), Agent102.wordAt [] k = []
Agent105.AffineDynamics.wordAt_cons : ∀ (r : Agent102.RunSpec) (rs : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (r :: rs) k = List.replicate (r.length.eval k).toNat r.digit ++ Agent102.wordAt rs k
Agent105.AffineDynamics.wordAt_append : ∀ (rs ss : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (rs ++ ss) k = Agent102.wordAt rs k ++ Agent102.wordAt ss k
```
</details>

### Agent105NormalizeReview

*Independent actual affine-normalization closure review*

Actual Agent8 normalization of arbitrary signed-affine finite run lists with symbols at most 18 and incoming carry at most 1; eventual expanded affine-run output with symbols at most 9 and a fixed bit terminal carry. Scalar dichotomy is discharged using unchanged Agent102 arithmetic; repeated-block identities are unchanged Agent1 results. No stepWord iteration or uniform-safe-return conclusion is registered.

- Root module(s): `P196.Agent105NormalizeReview.Agent105AffineNormalize`
- 10 modules, 16 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent105.AffineNormalize.singleton_pow : ∀ (x k : Nat), Agent1.RepeatedBlock.pow [x] k = List.replicate k x
Agent105.AffineNormalize.terminalCarry_replicate_succ : ∀ (x e k : Nat),
  x ≤ 18 → e ≤ 1 → Agent8.terminalCarry (List.replicate (k + 1) x) e = (x + e) / 10
Agent105.AffineNormalize.fixedDigits_replicate_succ : ∀ (x e k : Nat),
  x ≤ 18 →
    e ≤ 1 →
      Agent8.fixedDigits (List.replicate (k + 1) x) e = [(x + e) % 10] ++ List.replicate k ((x + (x + e) / 10) % 10)
```
</details>

### Agent105UniformIntegerReturn

*Actual affine-run uniform plain and safe returns with ordinary-integer interpretation*

Plain and safe uniform positive pair-word returns for original Agent8 affine-run dynamics, plus the exact original Lychrel196 ordinary-natural-number interpretation. Positive slope, positive shift and actual variable-return/realizability assumptions remain explicit; one common t is bounded by 4*widthSlope*s. Positive realizers are retained and the final assertion ranges over every integer with the same pair word. No equality of arbitrary integer representatives or unconditional result about 196 is asserted.

- Root module(s): `P196.Agent105UniformIntegerReturn.Agent105UniformIntegerReturn`
- 26 modules, 115 checked endpoints
- Claim `agent105-8f1107db019a-affinebasics`: Literal expanded run-word interfaces using unchanged Agent102 data definitions.
- Claim `agent105-8f1107db019a-affinenormalize`: Unconditional actual decimal normalization closure on bounded-symbol signed-affine run families, preserving terminal carry and zero columns.
- Claim `agent105-8f1107db019a-tailselection`: Finite positive-time tail selection from explicit stable predicates and an eventual finite cover.
- Claim `agent105-8f1107db019a-returntimebound`: Actual Agent8 list-return potential and width inequalities; explicit canonicality, equal-head, return, width-gain and positive-time hypotheses.
- Claim `agent105-8f1107db019a-affinezip`: Unconditional actual truncating zipAdd closure, with scalar difference and ordering interfaces discharged by original Agent102 arithmetic.
- Claim `agent105-8f1107db019a-affineorbit`: Actual pair, stepWord and each fixed-time orbit closure, plus exact parameter shift and reversal interfaces.
- Claim `agent105-8f1107db019a-affineshape`: Eventual actual head and exact width data, retaining signed affine intercepts and including a common width-increment cutoff for all nonnegative shifts.
- Claim `agent105-8f1107db019a-affinestability`: Transfer of original Agent102 actual-word equality/palindrome stability to eventually represented actual word families.
- Claim `agent105-8f1107db019a-uniformreturn`: One positive safe-return time for an entire parameter tail, derived from eventual canonicality and unbounded positive safe-return existence for each sufficiently large parameter, with bound 4*widthSlope*s.
- Claim `agent105-8f1107db019a-uniformreturnplain`: The plain variable-positive-return theorem without a safety premise, with the same actual time bound.
- Claim `agent105-8f1107db019a-integersafety`: Exact equivalence between original Lychrel196 positive-time palindrome outputs and normalized Agent8 orbit words, with explicit representation and positive-time conditions.
- Claim `agent105-8f1107db019a-uniformintegerreturn`: Uniform plain and safe pair-word returns for every ordinary integer realizing a sufficiently large family member; positive-realizer existence is retained. Pair-word return is not claimed to be equality of arbitrary chosen integer representatives.

<details><summary>Main statements (Lean)</summary>

```lean
Agent105.AffineDynamics.wordAt_nil : ∀ (k : Nat), Agent102.wordAt [] k = []
Agent105.AffineDynamics.wordAt_cons : ∀ (r : Agent102.RunSpec) (rs : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (r :: rs) k = List.replicate (r.length.eval k).toNat r.digit ++ Agent102.wordAt rs k
Agent105.AffineDynamics.wordAt_append : ∀ (rs ss : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (rs ++ ss) k = Agent102.wordAt rs k ++ Agent102.wordAt ss k
```
</details>

### Agent105UniformSafeReturn

*Uniform positive safe returns for actual affine-run list dynamics*

Actual Agent8 list dynamics: eventual positive safe-return existence on a fixed finite signed-affine run family of symbols at most 18, with positive width slope and positive parameter shift and eventual original CanonicalPair, implies one common positive safe-return time at most 4*widthSlope*s on an entire parameter tail. Actual affine closure, equality/safety stability, eventual head/width and the finite time bound are proved. The registry does not assert return existence for a particular integer or ordinary-integer realization of every CanonicalPair.

- Root module(s): `P196.Agent105UniformSafeReturn.Agent105UniformReturn`
- 20 modules, 106 checked endpoints
- Claim `agent105-8f1107db019a-affinebasics`: Literal expanded run-word interfaces using unchanged Agent102 data definitions.
- Claim `agent105-8f1107db019a-affinenormalize`: Unconditional actual decimal normalization closure on bounded-symbol signed-affine run families, preserving terminal carry and zero columns.
- Claim `agent105-8f1107db019a-tailselection`: Finite positive-time tail selection from explicit stable predicates and an eventual finite cover.
- Claim `agent105-8f1107db019a-returntimebound`: Actual Agent8 list-return potential and width inequalities; explicit canonicality, equal-head, return, width-gain and positive-time hypotheses.
- Claim `agent105-8f1107db019a-affinezip`: Unconditional actual truncating zipAdd closure, with scalar difference and ordering interfaces discharged by original Agent102 arithmetic.
- Claim `agent105-8f1107db019a-affineorbit`: Actual pair, stepWord and each fixed-time orbit closure, plus exact parameter shift and reversal interfaces.
- Claim `agent105-8f1107db019a-affineshape`: Eventual actual head and exact width data, retaining signed affine intercepts and including a common width-increment cutoff for all nonnegative shifts.
- Claim `agent105-8f1107db019a-affinestability`: Transfer of original Agent102 actual-word equality/palindrome stability to eventually represented actual word families.
- Claim `agent105-8f1107db019a-uniformreturn`: One positive safe-return time for an entire parameter tail, derived from eventual canonicality and unbounded positive safe-return existence for each sufficiently large parameter, with bound 4*widthSlope*s.

<details><summary>Main statements (Lean)</summary>

```lean
Agent105.AffineDynamics.wordAt_nil : ∀ (k : Nat), Agent102.wordAt [] k = []
Agent105.AffineDynamics.wordAt_cons : ∀ (r : Agent102.RunSpec) (rs : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (r :: rs) k = List.replicate (r.length.eval k).toNat r.digit ++ Agent102.wordAt rs k
Agent105.AffineDynamics.wordAt_append : ∀ (rs ss : List Agent102.RunSpec) (k : Nat),
  Agent102.wordAt (rs ++ ss) k = Agent102.wordAt rs k ++ Agent102.wordAt ss k
```
</details>

### Agent205InterfaceGrowth

**LEAN-VERIFIED — exact cyclic run-length guards.** For a positive finite cycle of signed increments with arbitrary phase thresholds, cyclic lower bounds exist exactly when the total increment is nonnegative. The maximum prefix deficit gives the least initial reserve and protects every phase of every later traversal. The result includes natural lower bounds and independent pairs of coordinates. This is generic arithmetic; an exact decimal state cycle and its nonpalindrome tests remain separate obligations. Root: `P196.Agent205InterfaceGrowth.CyclicGuards`; 1 module, 7 checked endpoints. [reports/REPORT_205.md](reports/REPORT_205.md) supplies the written multi-band charge obstruction, complement-reflection obstruction, proofs, and reproducible identity checks; those additional results are labeled THEOREM rather than LEAN-VERIFIED.

## Finite abstractions and transducers

Finite models whose limits are stated explicitly.

**PrefixCycleLift:** Zero-based rows `31, 30, 29, 28` of the existing seven-column `Cycle398_k7` witness, read in forward time, have no eighth-column extension: the possible added coefficients shrink from `0..18` to `7..17`, then `14..18`, then the empty set. A sound checker and canonical integer bridge exclude this four-row trace from any ordinary orbit whose state at the trace start has width at least eight, including subsequent overflow and width increases. This does not exclude palindrome prefix `398` or invalidate the existing seven-column cycle. Root: `P196.PrefixCycleLift.Cycle398`; 15 modules, 15 endpoints.

- **PrefixTruncation**: every positive truncation preserves complete backward prefix edges and exact path lengths, transporting reachable positive-cycle rank obstructions to smaller widths; a nine-edge `[1]` cycle and a checked rank-zero refinement `[1, 9, 6]` show the converse fails (`P196.PrefixTruncation.Controls`, 9 modules, 12 endpoints). This concerns coefficient words and does not establish ordinary-orbit realizability or a 196 exclusion.

- **PrefixEdgeRealization**: every valid coefficient prefix of length `k` with either high inner carry bit has an actual positive integer witness at canonical source width `2*k+1`; the complete executable inverse is exactly one-step prefix realizability and is equivalent to the two existing forward carry-bit checks (`P196.PrefixEdgeRealization.Realization`, 12 modules, 5 endpoints). Witnesses may differ between edges; no joint path or cycle realization, fixed-seed reachability or palindrome avoidance is claimed.

- **PrefixWidthRealization**: explicit overlap symmetry, center parity and boundary-carry tests characterize actual positive integer one-step realizability at every source width at least the nonempty prefix length; full, double and odd boundary widths are specialized, and the constant prefix of twos proves the sharp universal threshold `L > 2*k` for both prescribed bits (`P196.PrefixWidthRealization.Controls`, 14 modules, 6 endpoints). Source and successor representations are canonical; no joint path or cycle realization, fixed-seed reachability or palindrome avoidance is claimed.

### Agent107FoldedTransducer

原 46 状态 folded transducer 的精确 872 边/251 终止行、完整有限路径、四分支输出和普通正整数一步实现；不提供安全闭合语言或无限不回文结论。

- Root module(s): `P196.Agent107FoldedTransducer.Agent107TransducerGraph`, `P196.Agent107FoldedTransducer.Agent107TransducerBoundary`
- 12 modules, 49 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent107.FoldedTransducer.actual_accepts : ∀ (L : Nat) (q : Nat → Nat),
  FoldedDecimal.Admissible L q → Agent107.FoldedTransducer.Accepts L q (Agent107.FoldedTransducer.actualState L q)
Agent107.FoldedTransducer.accepting_state_eq_actual : ∀ (L : Nat) (q : Nat → Nat)
  (p : Nat → Agent107.FoldedTransducer.State),
  FoldedDecimal.Admissible L q →
    Agent107.FoldedTransducer.Accepts L q p → ∀ (i : Nat), i ≤ L / 2 → p i = Agent107.FoldedTransducer.actualState L q i
Agent107.FoldedTransducer.accepting_finitePath_unique : ∀ (L : Nat) (q : Nat → Nat)
  (p r : Nat → Agent107.FoldedTransducer.State),
  FoldedDecimal.Admissible L q →
    Agent107.FoldedTransducer.Accepts L q p →
      Agent107.FoldedTransducer.Accepts L q r →
        Agent107.FoldedTransducer.finitePath L p = Agent107.FoldedTransducer.finitePath L r
```
</details>

### Agent113TripleMaximality

All 32 complementary descending prefixes have first-edge-no-overflow abstract three-column predecessor paths of arbitrarily large exact depths. This is an incompleteness result for the finite abstraction, not ordinary integer orbit realizability or a 196 result.

- Root module(s): `P196.Agent113TripleMaximality.Agent113TripleRepeat`
- 4 modules, 42 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent113.TripleMaximality.cycle01 : Agent113.TwoDigit.nextTriple 10 4 6 0 = (1, 5, 10)
Agent113.TripleMaximality.cycle12 : Agent113.TwoDigit.nextTriple 5 2 3 0 = (10, 4, 6)
Agent113.TripleMaximality.cycle23 : Agent113.TwoDigit.nextTriple 2 11 1 0 = (5, 2, 3)
```
</details>

### Agent2SaturatedProfile

Exact conditional saturated eight-cycle targets from Agent #215, actual whole-word specialization, numeric canonical-prefix corollary, derived local tightness and overflow profile. No existence or all-time persistence claim.

- Root module(s): `P196.Agent2SaturatedProfile.Agent2SaturatedProfile`
- 17 modules, 5 checked endpoints

<details><summary>Main statements (Lean)</summary>

```lean
Agent2.SaturatedProfile.saturatedEightCycleTarget : Agent215.Saturated8.SaturatedEightCycleTarget
Agent2.SaturatedProfile.actualSaturatedEightCycleTarget : Agent215.Saturated8.ActualSaturatedEightCycleTarget
Agent2.SaturatedProfile.numeric_saturated_prefix_profile : ∀ (seed : Nat) (d : Nat → Nat) (L P : Nat),
  DecimalDigits.Canonical seed d L →
    3 ≤ L →
      ∃ final W,
        DecimalDigits.Canonical (Lychrel196.orbit seed P) final W ∧
          (P196.Agent4.WholeWord.prefix3 (DecimalDigits.columnSum final W) =
              P196.Agent4.WholeWord.prefix3 (DecimalDigits.columnSum d L) →
            2 * W = 2 * L + P →
              ∃ r,
                ∀ (i : Nat),
                  i < P →
                    ∃ digits width,
                      DecimalDigits.Canonical (Lychrel196.orbit seed i) digits width ∧
                        P196.Agent4.WholeWord.prefix3 (DecimalDigits.columnSum digits width) =
                          Agent215.Saturated8.cycleState (↑r + i))
```
</details>

## Excluded palindrome prefixes — all results combined

One table instead of several overlapping lists. A cell is the three-digit prefix (row = first two digits, column = third digit). If the orbit of 196 ever reaches a palindrome, that palindrome cannot begin with any marked prefix. Several results overlap; each cell shows one source, the others are counted below.

`C` two-digit prefix (Core) · `K` single-prefix kernel (217, 218, 620, 739, 777) · `S` the 33 three-digit classes · `F` the forward-invariant list (277 prefixes) · `R` all ten four-digit refinements excluded (Agent124FourDigit together with PrefixK45) · `x` this method provably cannot decide it (Agent117RemainingCycles) · `.` open

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **10** | C | C | C | C | C | C | C | C | C | C |
| **11** | . | . | x | . | . | . | . | . | . | S |
| **12** | . | . | . | . | . | . | . | . | . | . |
| **13** | F | . | . | . | . | . | . | . | x | . |
| **14** | F | F | . | . | . | . | . | . | . | . |
| **15** | F | F | F | . | . | . | . | . | . | . |
| **16** | F | F | F | F | x | . | . | . | . | . |
| **17** | F | F | F | F | F | . | . | . | . | . |
| **18** | F | F | F | F | F | F | . | . | . | . |
| **19** | F | F | F | F | F | F | F | R | x | . |
| **20** | C | C | C | C | C | C | C | C | C | C |
| **21** | . | . | . | S | R | R | S | K | K | . |
| **22** | . | . | . | . | . | . | . | . | . | . |
| **23** | . | . | . | . | . | . | . | . | . | . |
| **24** | R | R | . | . | . | . | . | . | x | . |
| **25** | R | . | . | . | . | . | R | S | . | . |
| **26** | F | F | R | . | . | . | . | . | . | . |
| **27** | . | . | R | R | . | x | S | S | S | . |
| **28** | F | F | F | F | R | . | . | . | . | . |
| **29** | . | . | . | . | . | . | . | . | . | . |
| **30** | F | F | F | F | F | F | F | F | F | . |
| **31** | R | . | . | . | . | . | . | . | . | . |
| **32** | C | C | C | C | C | C | C | C | C | C |
| **33** | F | F | F | F | F | F | F | F | F | F |
| **34** | F | F | F | F | F | F | F | F | S | . |
| **35** | F | . | . | . | . | . | . | . | . | . |
| **36** | F | F | . | . | . | . | . | . | . | . |
| **37** | F | F | F | . | . | . | R | S | . | . |
| **38** | F | F | F | F | S | S | . | . | . | . |
| **39** | . | . | . | . | . | . | . | . | x | . |
| **40** | C | C | C | C | C | C | C | C | C | C |
| **41** | C | C | C | C | C | C | C | C | C | C |
| **42** | . | . | . | R | R | . | S | R | R | S |
| **43** | . | . | . | . | . | . | . | . | . | . |
| **44** | . | . | . | . | . | . | . | . | . | . |
| **45** | . | . | . | . | . | . | . | . | . | . |
| **46** | . | . | . | . | . | . | . | . | . | . |
| **47** | . | . | . | . | S | . | . | . | R | . |
| **48** | R | R | R | . | . | . | . | . | . | . |
| **49** | . | . | . | . | . | . | . | . | . | . |
| **50** | F | F | F | F | F | F | F | F | F | . |
| **51** | . | . | . | . | . | . | . | . | . | . |
| **52** | F | R | . | . | . | R | . | . | . | . |
| **53** | . | F | F | F | F | F | F | F | F | F |
| **54** | F | F | F | F | F | F | F | F | F | . |
| **55** | . | . | . | . | . | . | . | . | . | . |
| **56** | R | R | . | . | . | . | . | . | . | . |
| **57** | . | . | . | . | . | . | . | . | . | . |
| **58** | F | F | F | . | . | . | . | . | . | R |
| **59** | . | R | R | . | . | . | . | . | . | . |
| **60** | C | C | C | C | C | C | C | C | C | C |
| **61** | F | F | F | F | F | F | F | F | F | . |
| **62** | K | R | . | . | . | R | x | . | . | R |
| **63** | . | . | . | . | . | . | . | . | . | . |
| **64** | C | C | C | C | C | C | C | C | C | C |
| **65** | C | C | C | C | C | C | C | C | C | C |
| **66** | . | . | . | . | . | . | . | . | . | . |
| **67** | . | . | . | . | S | . | R | . | . | . |
| **68** | F | . | . | . | . | . | . | . | . | . |
| **69** | R | R | . | . | . | . | . | . | R | . |
| **70** | F | F | F | F | F | F | F | F | F | . |
| **71** | x | . | . | . | . | . | x | . | . | . |
| **72** | F | F | F | F | F | F | F | F | F | . |
| **73** | . | R | . | . | . | . | . | S | . | K |
| **74** | F | F | F | F | F | F | F | F | F | . |
| **75** | R | . | . | . | R | S | . | . | . | . |
| **76** | C | C | C | C | C | C | C | C | C | C |
| **77** | . | R | R | R | R | R | R | K | S | F |
| **78** | R | R | R | S | S | S | S | S | S | S |
| **79** | x | . | . | . | . | . | . | . | . | . |
| **80** | C | C | C | C | C | C | C | C | C | C |
| **81** | C | C | C | C | C | C | C | C | C | C |
| **82** | C | C | C | C | C | C | C | C | C | C |
| **83** | C | C | C | C | C | C | C | C | C | C |
| **84** | . | . | . | . | . | R | R | R | R | . |
| **85** | R | R | R | R | R | R | S | S | S | S |
| **86** | . | . | . | . | . | . | . | R | R | . |
| **87** | . | . | . | . | . | . | . | . | . | . |
| **88** | . | . | . | . | . | . | . | . | . | . |
| **89** | . | . | . | . | . | . | . | . | . | . |
| **90** | F | R | R | R | R | S | S | . | . | . |
| **91** | . | x | . | . | . | . | . | . | . | . |
| **92** | F | R | R | S | . | R | . | . | . | . |
| **93** | . | . | . | . | . | S | x | . | . | R |
| **94** | F | F | F | F | F | F | F | F | F | . |
| **95** | . | . | x | . | . | . | . | . | . | . |
| **96** | F | R | . | . | . | . | . | . | R | . |
| **97** | . | . | . | . | R | R | R | . | . | . |
| **98** | F | R | R | R | . | . | . | . | . | . |
| **99** | . | . | . | . | . | . | . | . | . | . |

396 of the 900 three-digit prefixes are excluded (321 by a three-digit or two-digit result, 124 of them by more than one, and 75 marked `R` because all ten of their four-digit refinements are excluded), 14 are provably out of reach of this method, and 490 are open.

Four-digit refinements: 2494 four-digit prefixes outside the C/K/S/F cells are excluded: 1731 from the lists `entries..` in `Agent124FourDigit` plus the single prefix 2641 in `Agent117P2641`, and 763 from `PrefixK45` (750 of them fill the `R` cells). Counting every result, 5704 of the 9000 four-digit prefixes (63.4%) are excluded.

Per-prefix status for all 9000 four-digit prefixes is in [calculation/prefix4_status.csv](calculation/prefix4_status.csv) (columns prefix, status, width, bound, where, note). `lean_main` (5808): excluded by a Lean result on main, either listed in a registered entries list (Agent124FourDigit 1730, PrefixK45 763, PrefixBatch4K6 101, Sprint Agent02 3, Agent117P2641 1) or through the cells C, K, S or F above. `lean_offline` (42): Lean-verified only in [calculation/math_v7.zip](calculation/math_v7.zip) (30 width-7 and 12 width-8 prefixes), not on main. `search_only` (13): certified by the backward search at widths 9 and 10, with no Lean proof (the Lean check of the width-9 package hit a heartbeat limit). `cycle` (1030): the backward search has a cycle at width 10. `nodecap` (2089): undecided, the search hit the 30M node cap at width 10. `leadone` (18): method not applicable (leading digit 1, all digits at most 2). Total 9000. Only `lean_main` is Lean-verified on main; `lean_offline` is Lean-verified but not on main; `search_only`, `cycle` and `nodecap` are not Lean proofs.

## Additional draft results (not reviewed)

139 groups of draft files from the old branches. They compile, pass the axiom audit, and each file proves at least one theorem statement that appears nowhere else in the repository; nobody has reviewed them. Earlier versions and copies whose statements are already covered were left out (they remain in the archive tags).

| Group | Files | New theorem statements | Source |
| --- | ---: | ---: | --- |
| `Drafts.Agent100GroupIIOverflowSharpness` | 7 | 36 | `proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/development/bridge/attempt02/Agent100GroupIIOverflowBridge.lean` … |
| `Drafts.Agent100GroupIIOverlap` | 1 | 5 | `proofs/contributions/agent-100/groupII-overlap-20261016/development/dynamics/attempt02.lean` |
| `Drafts.Agent100GroupIIRebase` | 10 | 22 | `proofs/contributions/agent-100/groupII-rebase-20261016/development/algebra/attempt02/Agent100GroupIIRebaseAlgebra.lean` … |
| `Drafts.Agent100ThirdGateBoundary` | 6 | 28 | `proofs/contributions/agent-100/third-gate-boundary-20261016/development/boundary/attempt02.lean` … |
| `Drafts.Agent102AffineParameterIntervals` | 3 | 12 | `proofs/contributions/agent-102/affine-parameter-intervals-20261016/development/compact-author/controls-001/CompactControls.lean` … |
| `Drafts.Agent102AffineRuns` | 3 | 23 | `proofs/contributions/agent-102/affine-runs-20261016/independent-lean/decision/source/LargeCoefficientExamples.lean` … |
| `Drafts.Agent103BroaderReturnFormal` | 30 | 22 | `proofs/contributions/agent-103/broader-return-formal/BroaderClock.lean` … |
| `Drafts.Agent103ResidualFive` | 1 | 17 | `proofs/contributions/agent-103/residual-five-20261016/evidence/independent-shape/ResidualFiveShape.lean` |
| `Drafts.Agent103ResidualFiveFibers` | 6 | 53 | `proofs/contributions/agent-103/residual-five-fibers-20261016/ResidualFiveCountArithmetic.lean` … |
| `Drafts.Agent103ResidualFiveFirsthitTwo` | 3 | 6 | `proofs/contributions/agent-103/residual-five-firsthit-two-20261016/ResidualFiveInitialPalindromes.lean` |
| `Drafts.Agent104Prefix620Kernel` | 170 | 3 | `proofs/contributions/agent-104/prefix620-kernel-20261016/development/coverage/attempt-002/Agent104Prefix620DataCoverage.lean` … |
| `Drafts.Agent104ReviewAgent13RealWeights` | 4 | 34 | `proofs/contributions/agent-104/review-agent13-real-weights/execution/hosted-38700059129-1/independent-audit/original-sources/proofs/contributions/agent-13/safe-predecessor-family/Counting.lean` … |
| `Drafts.Agent104ReviewAgent4TemporalStrip` | 3 | 27 | `proofs/contributions/agent-104/review-agent4-temporal-strip/semantic/ExactTypesApplied.lean` … |
| `Drafts.Agent104ReviewAgent4WholeWord` | 1 | 9 | `proofs/contributions/agent-104/review-agent4-whole-word/semantic/ReviewScopeWitnesses.lean` |
| `Drafts.Agent104SevenColumnKernel` | 3 | 7 | `proofs/contributions/agent-104/seven-column-kernel/certificate/Pilot739.lean` … |
| `Drafts.Agent105ActualHighReturn` | 7 | 22 | `proofs/contributions/agent-105/actual-high-return/dev_logs/composition/attempt_002.lean` … |
| `Drafts.Agent105HighReturnCriterion` | 10 | 14 | `proofs/contributions/agent-105/high-return-criterion/dev_logs/criterion/attempt_004.lean` … |
| `Drafts.Agent105ResidueTrap` | 8 | 8 | `proofs/contributions/agent-105/residue-trap/dev_logs/palindromes/attempt_003.lean` … |
| `Drafts.Agent106CongruenceCarryBudget` | 5 | 36 | `proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/development/budget/attempt-001/Agent106CarryBudget.lean` … |
| `Drafts.Agent106RunBirths` | 9 | 123 | `proofs/contributions/agent-106/run-births/OverflowBirths.lean` … |
| `Drafts.Agent107DfaHornClosure` | 4 | 23 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-001/Agent107DFAArithmetic.lean` … |
| `Drafts.Agent107PartitionSeamResponse` | 6 | 47 | `proofs/contributions/agent-107/partition-seam-response/development/pair-closure/attempt_002.lean` … |
| `Drafts.Agent107ReviewAgent109Outer` | 1 | 1 | `proofs/contributions/agent-107/review-agent109-outer/execution/agent107-outer109-clean-syq1jnqb/source-commit-OuterCompat.stdout.log` |
| `Drafts.Agent108ModularAutonomy` | 7 | 38 | `proofs/contributions/agent-108/modular-autonomy/AutonomyBasic.lean` … |
| `Drafts.Agent108WindowWeightsB31b8818` | 7 | 46 | `proofs/contributions/agent-108/window-weights-b31b8818/review/final-package-fresh17-001/sources/Indexing.lean` … |
| `Drafts.Agent109BoundaryKernelRecheck` | 239 | 280 | `proofs/contributions/agent-109/boundary-kernel-recheck/BoundaryCertificateK.lean` … |
| `Drafts.Agent109TemplateReturnCertificate` | 1 | 2 | `proofs/contributions/agent-109/template-return-certificate/CertCompat.lean` |
| `Drafts.Agent109TemplateStepSafety` | 1 | 7 | `proofs/contributions/agent-109/template-step-safety/NoPalStep.lean` |
| `Drafts.Agent110ReviewRadix` | 3 | 22 | `proofs/contributions/agent-110/review-radix/source_snapshots/ExteriorCapTwo.lean` … |
| `Drafts.Agent110Runtime` | 1 | 2 | `proofs/contributions/agent-110/runtime/Smoke.lean` |
| `Drafts.Agent110TwoStepReturn` | 4 | 10 | `proofs/contributions/agent-110/two-step-return-20261016/BoundaryArithmetic.lean` … |
| `Drafts.Agent111ExactLengthResidues` | 1 | 6 | `proofs/contributions/agent-111/exact-length-residues/development/outer/OuterBlock.attempt03.lean` |
| `Drafts.Agent112CertificateAdmissibility` | 2 | 3 | `proofs/contributions/agent-112/certificate-admissibility/AdmissibleCompat.lean` |
| `Drafts.Agent112EventualRealizability` | 4 | 16 | `proofs/contributions/agent-112/eventual-realizability/EventualCompat.lean` … |
| `Drafts.Agent112SmallPeriodObstruction` | 3 | 16 | `proofs/contributions/agent-112/small-period-obstruction/ProjectionControls.lean` … |
| `Drafts.Agent112TenadicCylinderImage` | 4 | 6 | `proofs/contributions/agent-112/tenadic-cylinder-image-20261016/CylinderImage.lean` … |
| `Drafts.Agent112TwoPhaseObstruction` | 5 | 19 | `proofs/contributions/agent-112/two-phase-obstruction/ActualInfiniteStrip.lean` … |
| `Drafts.Agent114Cap4KernelActualExit` | 2 | 10 | `proofs/contributions/agent-114/cap4-kernel-actual-exit/lean/ActualExit.lean` … |
| `Drafts.Agent114ReviewTemplateBridge` | 2 | 8 | `proofs/contributions/agent-114/review-template-bridge-20261015/ScopeRegression.lean` |
| `Drafts.Agent116Cap3Kernel` | 121 | 19 | `proofs/contributions/agent-116/cap3-kernel/Cap3AllBase.lean` … |
| `Drafts.Agent116CertificateExterior` | 123 | 6 | `proofs/contributions/agent-116/certificate-exterior/development/certificate/cap3-attempt-001.lean` … |
| `Drafts.Agent116Integration` | 126 | 9 | `proofs/contributions/agent-116/integration/endpoints/EndpointAudit.lean` |
| `Drafts.Agent116Review` | 1 | 3 | `proofs/contributions/agent-116/review/CanonicalityCounterexample.lean` |
| `Drafts.Agent119FourColumnPrefix` | 2 | 12 | `proofs/contributions/agent-119/four-column-prefix/FourColumnAncestry.lean` … |
| `Drafts.Agent120NeutralBandCalibration` | 4 | 72 | `proofs/contributions/agent-120/neutral-band-calibration/lean/A120Base.lean` … |
| `Drafts.Agent121MergedTemplateSafetyReview` | 3 | 10 | `proofs/contributions/agent-121/merged-template-safety-review/Agent121ScopeRegression.lean` |
| `Drafts.Agent121ReviewAgent116Checkpoint01` | 1 | 3 | `proofs/contributions/agent-121/review-agent116-checkpoint01/evidence/accepted-clean-rebuild/inputs/Agent121CertificateContracts.lean` |
| `Drafts.Agent123SeamMaskRealizability` | 4 | 20 | `proofs/contributions/agent-123/seam-mask-realizability/SeamMaskMass.lean` … |
| `Drafts.Agent123TemplateCertificateReplication` | 4 | 6 | `proofs/contributions/agent-123/template-certificate-replication/ContractProbes.lean` |
| `Drafts.Agent12ElevenCarries` | 1 | 3 | `proofs/contributions/agent-12/ElevenCarries.lean` |
| `Drafts.Agent12FirstHitFour` | 1 | 7 | `proofs/contributions/agent-12/FirstHitFour.lean` |
| `Drafts.Agent12FixedTarget` | 2 | 14 | `proofs/contributions/agent-12/FixedTarget.lean` |
| `Drafts.Agent13BufferedBinaryFamily` | 5 | 6 | `proofs/contributions/agent-13/buffered-binary-family/CarryPath.lean` |
| `Drafts.Agent13M99A03GapGainAudit` | 1 | 1 | `proofs/contributions/agent-13/m99-a03-gap-gain-audit/Audit.lean` |
| `Drafts.Agent14OrdinaryExteriorSixTwelveBridge` | 1 | 2 | `proofs/contributions/agent-14/ordinary-exterior-six-twelve-bridge/BridgeContract.lean` |
| `Drafts.Agent15SpectralCarryCharge` | 7 | 56 | `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/evidence/independent/runtime/environment-history/RuntimeSmoke.lean` … |
| `Drafts.Agent15SpectralCarrySupport` | 5 | 20 | `proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean` |
| `Drafts.Agent19Session22f4Agent19Session22f4` | 9 | 23 | `proofs/coordination/patches/agent19-session22f4/pr116/candidate-20261017/author/evidence/BoundaryBridge-attempt003.lean` … |
| `Drafts.Agent19Session8ff2acAgent19Session8ff2ac` | 1 | 7 | `proofs/coordination/patches/agent19-session8ff2ac/pr165-repair-20261017/source/ResidualFivePredecessorFilter.lean` |
| `Drafts.Agent1Agent104MonitorVerification` | 4 | 31 | `proofs/contributions/agent-1/agent104-monitor-verification-20261017/fresh-001/source/Agent107DFA.lean` … |
| `Drafts.Agent1CeilhalfVerification` | 10 | 78 | `proofs/contributions/agent-1/ceilhalf-verification-20261017/corrected-9ab3/fresh-002/compiled-sources/ArithmeticCRT.lean` … |
| `Drafts.Agent1PeriodicBlockStrip` | 1 | 6 | `proofs/contributions/agent-1/periodic-block-strip-20261016/center-author/clean-001/CenterControls.lean` |
| `Drafts.Agent1PeriodicOuterCatalog` | 1 | 2 | `proofs/contributions/agent-1/periodic-outer-catalog-20261016/choices-author/audit-001/ChoicesControls.lean` |
| `Drafts.Agent1PeriodicWidthProjection` | 1 | 1 | `proofs/contributions/agent-1/periodic-width-projection-20261016/width-lift-author/support-001/Support.lean` |
| `Drafts.Agent213GapgainSub72` | 2 | 2 | `proofs/contributions/agent-213/gapgain-sub72/GapGainSub72.lean` |
| `Drafts.Agent216Agent216GeneralNatExteriorCorrespondence` | 4 | 2 | `proofs/contributions/agent-216/agent216-general-nat-exterior-correspondence/ConcreteEdge.lean` |
| `Drafts.Agent216Agent216Mod22AbsorptionAudit` | 1 | 2 | `proofs/contributions/agent-216/agent216-mod22-absorption-audit/Mod22AbsorptionAudit.lean` |
| `Drafts.Agent216Agent216ResidueFilterDownstreamAudit` | 4 | 2 | `proofs/contributions/agent-216/agent216-residue-filter-downstream-audit/CanonicalCounterexample.lean` |
| `Drafts.Agent21M99A01RealizabilityInterface` | 7 | 2 | `proofs/contributions/agent-21/m99-a01-realizability-interface/M99A01RealizabilityInterface.lean` |
| `Drafts.Agent222M99B222GuardCounterexample` | 6 | 9 | `proofs/contributions/agent-222/M99-B222-guard-counterexample/GuardPreservationCounterexample.lean` … |
| `Drafts.Agent23M99A03GainIntegerBridge` | 3 | 2 | `proofs/contributions/agent-23/m99-a03-gain-integer-bridge/CertificateToInteger.lean` |
| `Drafts.Agent312M99C312BlockGuard` | 4 | 2 | `proofs/contributions/agent-312/M99-C312-block-guard/BlockGuard.lean` |
| `Drafts.Agent315TemporalColumn1199` | 1 | 2 | `proofs/contributions/agent-315/temporal-column-11-99/Divisor99Absorption.lean` |
| `Drafts.Agent317M99C317Uniformity` | 1 | 4 | `proofs/contributions/agent-317/m99-c317-uniformity/UniformityBridge.lean` |
| `Drafts.Agent34Sessionc91cAgent34Sessionc91c` | 2 | 5 | `proofs/coordination/evidence/agent34-sessionc91c/pr107/repair-20261016/repaired/RhoCycleLemmas.lean` |
| `Drafts.Agent3FiniteHorizonOverflow` | 1 | 2 | `proofs/contributions/agent-3/finite-horizon-overflow-20261016/review/cardinality/CardinalityIndependentReview.lean` |
| `Drafts.Agent3PrefixContraction` | 15 | 79 | `proofs/contributions/agent-3/prefix-contraction-20261016/NineColumnCertificate.lean` … |
| `Drafts.Agent3ThreeLayerPrefix` | 14 | 45 | `proofs/contributions/agent-3/three-layer-prefix-20261016/development/actual-depth/attempt-002.lean.txt` … |
| `Drafts.Agent3TwoHistory` | 11 | 113 | `proofs/contributions/agent-3/two-history-20261016/dependencies/agent9/ActualWords.lean` … |
| `Drafts.Agent412Agent412` | 5 | 22 | `proofs/coordination/submissions/agent412/PeriodTwelve.lean` … |
| `Drafts.Agent414Agent414` | 7 | 7 | `proofs/coordination/submissions/agent-414/boundary-kernel/Agent414BoundaryGraph0Bridge.lean` … |
| `Drafts.Agent418Agent418` | 5 | 34 | `proofs/coordination/submissions/agent-418/saturated-input-audit/Agent418AllPatternsRealizable.lean` … |
| `Drafts.Agent421Agent421` | 9 | 55 | `proofs/coordination/submissions/agent-421/general-base-nooverflow/Agent421NoOverflowConsequences.lean` … |
| `Drafts.Agent422Agent422` | 3 | 36 | `proofs/coordination/submissions/agent-422/checkpoint001/Agent422BaseDigits.lean` … |
| `Drafts.Agent4ComplementaryBulk` | 1 | 9 | `proofs/agent4/complementary_bulk/CycleConstraints.lean` |
| `Drafts.Agent4GeneralBaseNormalization` | 8 | 79 | `proofs/contributions/agent-4/general-base-normalization-20261016/ArithmeticBridge.lean` … |
| `Drafts.Agent4PrefixGrowth` | 1 | 2 | `proofs/agent4/prefix_growth/ModelSharpness.lean` |
| `Drafts.Agent4SaturationLift` | 5 | 30 | `proofs/agent4/saturation_lift/ActualWordStrip.lean` … |
| `Drafts.Agent5` | 2 | 19 | `proofs/agent5/GeneralOuterBudget.lean` … |
| `Drafts.Agent53BoundaryTableTranscription` | 5 | 1 | `proofs/contributions/agent-53/boundary-table-transcription-20261016/development/attempt-001/Agent53RootRanks.lean` |
| `Drafts.Agent6ComplementaryBulkExteriorAbsorbedObstruction` | 3 | 9 | `proofs/contributions/agent6-complementary-bulk/ExteriorAbsorbedObstruction.lean` |
| `Drafts.Agent6ComplementaryBulkExteriorOrdinaryWitnesses` | 4 | 3 | `proofs/contributions/agent6-complementary-bulk/ExteriorOrdinaryWitnesses.lean` |
| `Drafts.Agent6ComplementaryBulkExteriorPotentialObstruction` | 3 | 8 | `proofs/contributions/agent6-complementary-bulk/ExteriorPotentialObstruction.lean` |
| `Drafts.Agent6ComplementaryBulkExteriorSharp` | 3 | 1 | `proofs/contributions/agent6-complementary-bulk/ExteriorSharp.lean` |
| `Drafts.Agent7` | 1 | 5 | `proofs/agent7/OuterRank.lean` |
| `Drafts.Agent7AllbaseOverflowBirths` | 4 | 38 | `proofs/contributions/agent-7/allbase-overflow-births-20261016/arithmetic-dev/attempt-001/source/AdjacentBirths.lean` … |
| `Drafts.Agent7OddNooverflowFibers` | 20 | 156 | `proofs/contributions/agent-7/odd-nooverflow-fibers-20261016/actual-dev/attempt-003/source/OddActual.lean` … |
| `Drafts.Agent7RunPopulationRenewal` | 5 | 38 | `proofs/contributions/agent-7/run-population-renewal-20261016/dependencies/AncestryExtinction.lean` … |
| `Drafts.Agent8Agent8` | 1 | 5 | `proofs/coordination/patches/agent-8/lower-growth-20261016/Agent8LowerGrowth.lean` |
| `Drafts.Agent9FiniteEnsembleMarkerCount` | 7 | 78 | `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9FiniteHorizonCount.lean` … |
| `Drafts.Agent9NooverflowHorizon` | 10 | 35 | `proofs/contributions/agent-9/nooverflow-horizon-20261016/Agent9HorizonCounts.lean` … |
| `Drafts.Agent9OneStepDigitSumCollapse` | 3 | 10 | `proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/Agent9OneStepDigitSumCollapse.lean` |
| `Drafts.D20261014CollisionFormalCarryTransferNormalForm` | 1 | 5 | `proofs/contributions/2026-10-14-collision-formal/CarryTransferNormalForm.lean` |
| `Drafts.D20261014CollisionMassCarryResponseMass` | 1 | 17 | `proofs/contributions/2026-10-14-collision-mass/CarryResponseMass.lean` |
| `Drafts.D20261014ComponentHierarchyFormalComponentHierarchy` | 1 | 4 | `proofs/contributions/2026-10-14-component-hierarchy-formal/ComponentHierarchy.lean` |
| `Drafts.D20261014FiniteHorizonDensityFiniteHorizonBlocks` | 2 | 4 | `proofs/contributions/2026-10-14-finite-horizon-density/FiniteHorizonBlocks.lean` |
| `Drafts.D20261014LiftHierarchyFormalLiftHierarchy` | 1 | 3 | `proofs/contributions/2026-10-14-lift-hierarchy-formal/LiftHierarchy.lean` |
| `Drafts.D20261014OverflowMismatchFormalOverflowMismatch` | 1 | 14 | `proofs/contributions/2026-10-14-overflow-mismatch-formal/OverflowMismatch.lean` |
| `Drafts.D20261014PrefixExtensionFormalPrefixExtension` | 1 | 8 | `proofs/contributions/2026-10-14-prefix-extension-formal/PrefixExtension.lean` |
| `Drafts.D20261014SafePrefixOverflowSafeRuns` | 1 | 20 | `proofs/contributions/2026-10-14-safe-prefix/OverflowSafeRuns.lean` |
| `Drafts.D20261014SevenStepExtensionFormalActualRank` | 6 | 4 | `proofs/contributions/2026-10-14-seven-step-extension-formal/ActualRank.lean` |
| `Drafts.D20261014SevenStepExtensionFormalClockPaths` | 4 | 6 | `proofs/contributions/2026-10-14-seven-step-extension-formal/ClockPaths.lean` |
| `Drafts.D20261014SevenStepExtensionFormalNoFourReturns` | 17 | 11 | `proofs/contributions/2026-10-14-seven-step-extension-formal/NoFourReturns.lean` |
| `Drafts.D20261014SevenStepExtensionFormalRankCertificate` | 12 | 2 | `proofs/contributions/2026-10-14-seven-step-extension-formal/RankCertificate.lean` |
| `Drafts.D20261014SevenStepExtensionFormalSixPrefix` | 2 | 7 | `proofs/contributions/2026-10-14-seven-step-extension-formal/SixPrefix.lean` |
| `Drafts.D20261014SevenStepFormalActualBoundary` | 2 | 7 | `proofs/contributions/2026-10-14-seven-step-formal/ActualBoundary.lean` |
| `Drafts.D20261014SevenStepFormalBoundaryTransducer` | 1 | 7 | `proofs/contributions/2026-10-14-seven-step-formal/BoundaryTransducer.lean` |
| `Drafts.D20261014SevenStepFormalSevenStepOrbit` | 3 | 15 | `proofs/contributions/2026-10-14-seven-step-formal/SevenStepOrbit.lean` |
| `Drafts.D20261015ActualPrefixLiftReviewLabelNineCounterexample` | 7 | 3 | `proofs/contributions/2026-10-15-actual-prefix-lift-review/LabelNineCounterexample.lean` |
| `Drafts.D20261015Agent2ComplementarySearchAlternatingCharge` | 1 | 15 | `proofs/contributions/2026-10-15-agent2-complementary-search/AlternatingCharge.lean` |
| `Drafts.D20261015Agent3ComplementaryBulkBulkPhase` | 1 | 13 | `proofs/contributions/2026-10-15-agent3-complementary-bulk/BulkPhase.lean` |
| `Drafts.D20261015Agent3ComplementaryBulkOuterEscape` | 1 | 10 | `proofs/contributions/2026-10-15-agent3-complementary-bulk/OuterEscape.lean` |
| `Drafts.D20261015Agent8ComplementaryBulkAllPhaseRefinement` | 1 | 5 | `proofs/contributions/2026-10-15-agent8-complementary-bulk/AllPhaseRefinement.lean` |
| `Drafts.D20261015Agent9ComplementaryBulkExteriorErasure` | 1 | 25 | `proofs/contributions/2026-10-15-agent9-complementary-bulk/ExteriorErasure.lean` |
| `Drafts.D20261015BaseIntrinsicFormalIntrinsicCarry` | 1 | 10 | `proofs/contributions/2026-10-15-base-intrinsic-formal/IntrinsicCarry.lean` |
| `Drafts.D20261015BaseIntrinsicFormalIntrinsicPattern` | 2 | 15 | `proofs/contributions/2026-10-15-base-intrinsic-formal/IntrinsicPattern.lean` |
| `Drafts.D20261015BaseIntrinsicFormalIntrinsicReverseAdd` | 3 | 2 | `proofs/contributions/2026-10-15-base-intrinsic-formal/IntrinsicReverseAdd.lean` |
| `Drafts.D20261015ExternalIntrinsicReviewSources` | 2 | 31 | `proofs/contributions/2026-10-15-external-intrinsic-review/sources/IntrinsicSeam.lean` … |
| `Drafts.D20261015HighColumnFormalHighColumns` | 1 | 13 | `proofs/contributions/2026-10-15-high-column-formal/HighColumns.lean` |
| `Drafts.D20261015OverflowMismatchReductionFormalOverflowMismatchRedu` | 2 | 12 | `proofs/contributions/2026-10-15-overflow-mismatch-reduction-formal/OverflowMismatchReduction.lean` |
| `Drafts.D20261015SafeHighReturnSafeHighFamily` | 2 | 69 | `proofs/contributions/2026-10-15-safe-high-return/SafeHighFamily.lean` |
| `Drafts.D20261015SafeHighReturnSafeHighWitness` | 1 | 5 | `proofs/contributions/2026-10-15-safe-high-return/SafeHighWitness.lean` |
| `Drafts.D20261015ScalarClockFormalActualScalar` | 2 | 7 | `proofs/contributions/2026-10-15-scalar-clock-formal/ActualScalar.lean` |
| `Drafts.D20261015ScalarClockFormalScalarClock` | 1 | 6 | `proofs/contributions/2026-10-15-scalar-clock-formal/ScalarClock.lean` |
| `Drafts.D20261015ScalarFiniteCertificateFormalPilotArray` | 11 | 10 | `proofs/contributions/2026-10-15-scalar-finite-certificate-formal/pilot-array/PilotChecks.lean.txt` … |
| `Drafts.D20261015ScalarHierarchyReviewSourceSnapshots` | 16 | 56 | `proofs/contributions/2026-10-15-scalar-hierarchy-review/source_snapshots/ActualJobFamily.lean` … |
| `Drafts.Misc` | 527 | 217 | `proofs/Agent100DoubleGate.lean` … |
| `Drafts.Research` | 6 | 24 | `proofs/research/persist_arithmetic_width_rank.lean` … |
| `Drafts.ResearchMainExistenceAttempt` | 10 | 91 | `proofs/research/main_existence_attempt/ancestry_direct_pass/lean/FiniteAncestry.lean` … |

## Sprint agent results (PRs #261–#287)

Results of the Claude sprint agents, registered when their pull requests were merged. The scope text is the agent's own; each report under `sprint/` explains what is and is not claimed.

### Sprint01ForwardWalk

*Forward walks: 3,145 four-digit prefixes the width-8 forward invariant from time 100 cannot exclude*

Obstruction for the Agent124.Forward method, not a statement about palindromes of 196. For each of the 3,145 four-digit prefixes in `obstructed8` (3,134 with noOverflowPre plus 11 lead-one prefixes), an explicit list of inner carries walks the width-8 projection of orbit 196 100 to a full-width digit word beginning with that prefix (`forward_obstruction8`), so every code set that is closed under both forwardPrefix carry choices (fwdOK at width 8) and contains that projection contains an element of initialWordsL 8 pre. Generic lemma `forward_cannot_exclude`. Not claimed: anything at other widths or start times, anything about whether such palindromes occur, or about the backward (rank-certificate) method.

- Root modules: `P196.Sprint.Agent01.W8Final`
- 35 modules, 5 checked endpoints
- Report: [sprint/agent-01/REPORT.md](sprint/agent-01/REPORT.md)

### SprintAgent03

*Unguarded enrichment of the forward prefix abstraction gains nothing; 196's prefix state lies on a cycle (k = 3..7)*

Two statements about the k-column forward prefix abstraction (forwardPrefix with inner carry 0 or 1). (1) For any extra state X and any update δ : X → List Nat → Nat → X that never blocks a carry, the words of the least enriched invariant are exactly Reach w0 (proj_iff), and any enriched forward-closed set containing the start covers every Reach-word (enriched_invariant_covers, no_new_exclusion); this covers residues mod 99, width mod m, time mod 6 and the previous carry. (2) A word on a forward cycle, and every word forward-reachable from it, has no rank under any RowsClosed k rank function (rank_none_of_cycle, no_rank_of_cycleOK); the width-k projection of orbit 196 100 lies on such a cycle for k = 3..7 (kernel-checked carry witnesses), so no width-k batch entry for a k-digit prefix in its forward closure can pass entryOK (entryOK_false_3 .. entryOK_false_7). Not claimed: anything about palindromes of 196, that the forward closure equals the infinite-rank region (that was only computed), or anything at k ≥ 8.

- Root modules: `P196.Sprint.Agent03.EnrichedNoGain`, `P196.Sprint.Agent03.CycleRank`
- 19 modules, 17 checked endpoints
- Report: [sprint/agent-03/REPORT.md](sprint/agent-03/REPORT.md)

### SprintAgent04

*Width-7 cycle obstructions through one shared cycle; cycles realized by actual orbits*

Method limits, not exclusions. For the RowsClosed rank interface consumed by Agent124.PrefixL.entryOK: a word that reaches a backward closed walk has no rank, so entryOK fails for every bound for any prefix having such an initial word. Instances at width 7, all through one explicit length-7 cycle: 13 three-digit prefixes (138, 164, 198, 248, 275, 398, 626, 710, 716, 790, 911, 936, 952), 20 four-digit prefixes (1337, 1475, 2288, 6820, 8834, 8935, 8846, 4668, 1386, 3657, 4965, 8835, 1114, 4345, 3654, 6787, 1299, 4439, 1452, 8802) and 4456. Also: the canonical width-7 column words of orbit 10097 at times 220..228 form a closed walk with the actual carries; every width-7 column word of orbit 10151 at times 5..80 has no rank in any RowsClosed 7 function, and orbit 10151 81 is a palindrome beginning 1337. NOT claimed: minimality of the length-7 cycle, any statement about higher widths, any exclusion of palindromes from the orbit of 196, or that any orbit repeats forever.

- Root modules: `P196.Sprint.Agent04.PrefixesK7`, `P196.Sprint.Agent04.Realized`
- 3 modules, 58 checked endpoints
- Report: [sprint/agent-04/REPORT.md](sprint/agent-04/REPORT.md)

### Sprint.Agent05

*Delay witnesses: lower bounds for every prefix certificate*

A positive seed A with orbit A t a palindrome beginning with pre forces every Agent124 certificate entry (pre, b) accepted by entryOK (any width k, any rank function with RowsClosed/ShortClosed) to satisfy t <= b + 1, and keeps pre out of every entry list passing the two premises of no_196_of_entries with base check N < t. Instances: seed 1186060307891929990 reaches its first palindrome (119 digits, prefix 4456) at t = 261, so 4456, 445 and 44 can never pass the t <= 100 route; 449 four-digit prefixes (and their three- and two-digit parents) with kernel-checked witnesses t > 100 (Over100); 1514 certified four-digit entries whose bound b + 1 is attained by a real seed (Sharp). Not claimed: anything about whether 196 is a Lychrel number; witnesses are lower bounds only, absence of a large witness does not make a prefix certifiable.

- Root modules: `P196.Sprint.Agent05.Witness4456`, `P196.Sprint.Agent05.Over100`, `P196.Sprint.Agent05.Sharp`
- 33 modules, 32 checked endpoints
- Report: [sprint/agent-05/REPORT.md](sprint/agent-05/REPORT.md)

### SprintAgent02

Sprint agent 02 result; see sprint/agent-02/REPORT.md for what is and is NOT claimed. Registered by the owner when merging PR without editing the statements; nothing here proves that 196 is a Lychrel number.

- Root modules: `P196.Sprint.Agent02.P2342`, `P196.Sprint.Agent02.P9149P6676`, `P196.Sprint.Agent02.W3Final`
- 216 modules, 13 checked endpoints
- Report: [sprint/agent-02/REPORT.md](sprint/agent-02/REPORT.md)

### SprintAgent19

Sprint agent 19 result; see sprint/agent-19/REPORT.md for what is and is NOT claimed. Registered by the owner when merging PR without editing the statements; nothing here proves that 196 is a Lychrel number.

- Root modules: `P196.Sprint.Agent19.Arith118`, `P196.Sprint.Agent19.Arith620`, `P196.Sprint.Agent19.Arith739`, `P196.Sprint.Agent19.ArithClasses`, `P196.Sprint.Agent19.ArithFourDigit`, `P196.Sprint.Agent19.ArithLight`, `P196.Sprint.Agent19.AuditHeavy`, `P196.Sprint.Agent19.AuditLight`, `P196.Sprint.Agent19.CycleFormats`
- 11 modules, 96 checked endpoints
- Report: [sprint/agent-19/REPORT.md](sprint/agent-19/REPORT.md)

### SprintAgent20

Sprint agent 20 result; see sprint/agent-20/REPORT.md for what is and is NOT claimed. Registered by the owner when merging PR without editing the statements; nothing here proves that 196 is a Lychrel number.

- Root modules: `P196.Sprint.Agent20.Controls`, `P196.Sprint.Agent20.DelayWitnesses`, `P196.Sprint.Agent20.TextbookPrefixes`
- 4 modules, 41 checked endpoints
- Report: [sprint/agent-20/REPORT.md](sprint/agent-20/REPORT.md)

## Written research reports (not Lean-verified)

Paper proofs and computations by research agents (PRs #266–#286). **None of these is a Lean theorem**; their claims were spot-checked by independent computation on 2026-10-22, but they are not machine-verified. All are obstructions or tools; none gives a decimal Lychrel number.

- [reports/REPORT_214.md](reports/REPORT_214.md) (PR #268): Agent 214: periodic-band obstruction and restricted cycle classifications
- [reports/REPORT_205.md](reports/REPORT_205.md) (PR #269): Agent 205: interface growth obstructions and exact cyclic guards
- [reports/REPORT_215.md](reports/REPORT_215.md) (PR #270): Agent 215: global interface residues and affine run growth obstructions
- [reports/REPORT_202.md](reports/REPORT_202.md) (PR #271): Agent #202: sharp complementary-profile obstruction and base arithmetic
- [reports/REPORT_211.md](reports/REPORT_211.md) (PR #272): Agent 211: finite graph for separated templates and short-interface obstruction
- [reports/REPORT_204.md](reports/REPORT_204.md) (PR #273): Agent 204: periodic band obstructions and short-period bulk cycles
- [reports/REPORT_208.md](reports/REPORT_208.md) (PR #274): Agent 208: exact certificate-bound synthesis and interface obstruction
- [reports/REPORT_213.md](reports/REPORT_213.md) (PR #275): Agent 213: known-base certificates and restricted center rigidity
- [reports/REPORT_201.md](reports/REPORT_201.md) (PR #276): Agent 201: bounded template decidability and exact cap obstruction
- [reports/REPORT_219.md](reports/REPORT_219.md) (PR #277): Agent 219: endpoint-limit carry obstruction and constant-center return bounds
- [reports/REPORT_207.md](reports/REPORT_207.md) (PR #278): Agent 207: three-run and parity obstructions
- [reports/REPORT_209.md](reports/REPORT_209.md) (PR #279): Agent 209: binary embedding obstructions and finite block-code test
- [reports/REPORT_218.md](reports/REPORT_218.md) (PR #280): Agent 218: certificate feasibility audit and saturated phase obstruction
- [reports/REPORT_220.md](reports/REPORT_220.md) (PR #281): Agent 220: exact band algebra and scoped obstructions
- [reports/REPORT_206.md](reports/REPORT_206.md) (PR #282): Agent 206: recurring low centers exclude permanent central high witnesses
- [reports/REPORT_210.md](reports/REPORT_210.md) (PR #283): Agent 210: exact band algebra and improved finite-horizon bounds
- [reports/REPORT_212.md](reports/REPORT_212.md) (PR #284): Agent #212: exclude uniform returns of the decimal dyadic family
- [reports/REPORT_203.md](reports/REPORT_203.md) (PR #285): Agent 203: Seal constructions and critical-band obstruction
- [reports/REPORT_216.md](reports/REPORT_216.md) (PR #286): Agent 216: exact center obstruction and run renewal
