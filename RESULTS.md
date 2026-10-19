# Results

Every result below is a Lean 4 theorem that builds from source in this repository and whose axioms are only `propext`, `Classical.choice` and `Quot.sound` (checked by `python3 tools/verify.py`). There are 232 results (5506 checked endpoints — the theorems and definitions a reader should rely on — in 4492 modules).

**None of them proves that 196 is a Lychrel number.** Each result has an explicit scope; the scope text is the author's own description and says what is *not* claimed.

Machine-readable version: [`lean/registry.json`](lean/registry.json) (modules, root modules, every endpoint).

## Contents

1. [The orbit of 196 and palindrome-prefix exclusions](#the-orbit-of-196-and-palindrome-prefix-exclusions) (16)
2. [A conditional route to a Lychrel number](#a-conditional-route-to-a-lychrel-number) (1)
3. [One reverse-and-add step: predecessors, fibers, palindromic outputs](#one-reverse-and-add-step-predecessors-fibers-palindromic-outputs) (17)
4. [Carries: what carry sequences reveal and how they evolve](#carries-what-carry-sequences-reveal-and-how-they-evolve) (19)
5. [Periodic (repeated-block) words and their quotient dynamics](#periodic-repeated-block-words-and-their-quotient-dynamics) (28)
6. [Affine run words](#affine-run-words) (9)
7. [Finite abstractions and transducers](#finite-abstractions-and-transducers) (3)

## The orbit of 196 and palindrome-prefix exclusions

Results about the actual orbit of 196, and the prefix-exclusion method used for it. `Core` also bundles four reviewed results on other topics (listed as its claims).

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

## One reverse-and-add step: predecessors, fibers, palindromic outputs

Exact structure of a single ordinary decimal step: who can map to a given number, how many, and when the output is a palindrome.

- **InverseFiberGrowth:** rational upper and lower exponential bounds for exact even folded coefficient-word fibers, including the explicit 144/89 and 233/144 rate sandwich (`P196.InverseFiberGrowth.FiberBounds`; 8 modules, 7 endpoints). These are coefficient-word counts, not ordinary-integer predecessor counts or infinite-orbit assertions.

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

## Carries: what carry sequences reveal and how they evolve

Carry observability, carry accounting and exterior coordinates over finitely many steps.

- **LowDigitSumTermination:** Every positive integer with decimal digit sum at most 9 reaches a palindrome in 1–3 steps (`LowDigitSumTermination.palindrome_within_three_of_digitSum_le_nine`); 180 attains time 3, while digit-sum-10 input 190 first hits at time 7. Every iterate of a hypothetical Lychrel seed therefore has digit sum at least 10. No existence or 196 conclusion. Root: `P196.LowDigitSumTermination.Main`; 4 modules, 8 checked endpoints.

- **CommonOverflowGap:** At equal initial canonical width, common first-step terminal carry one and an antisymmetric normalized old-width digit difference imply `step (step n) + 9 * step n = step (step m) + 9 * step m`; hence strict order reversal and exact ninefold gap scaling, without requiring equal second-output widths (`P196.CommonOverflowGap.Numeric`). Includes a structural value identity and the existing canonical witness; no repeated-overflow, infinite-orbit or 196 conclusion.

- **CarryCountGrowth**: every positive ordinary decimal orbit has arbitrarily large outgoing carry counts after every starting time, with an explicit window from the current actual width; the count includes the terminal carry (`P196.CarryCountGrowth.CarryCountGrowth`, 3 modules, 12 endpoints). This includes the continued orbit of 196 and does not establish palindrome avoidance, carry density or convergence to infinity.

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

## Finite abstractions and transducers

Finite models whose limits are stated explicitly.

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

`C` two-digit prefix (Core) · `K` single-prefix kernel (217, 218, 620, 739, 777) · `S` the 33 three-digit classes · `F` the forward-invariant list (277 prefixes) · `x` this method provably cannot decide it (Agent117RemainingCycles) · `.` open

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
| **19** | F | F | F | F | F | F | F | . | x | . |
| **20** | C | C | C | C | C | C | C | C | C | C |
| **21** | . | . | . | S | . | . | S | K | K | . |
| **22** | . | . | . | . | . | . | . | . | . | . |
| **23** | . | . | . | . | . | . | . | . | . | . |
| **24** | . | . | . | . | . | . | . | . | x | . |
| **25** | . | . | . | . | . | . | . | S | . | . |
| **26** | F | F | . | . | . | . | . | . | . | . |
| **27** | . | . | . | . | . | x | S | S | S | . |
| **28** | F | F | F | F | . | . | . | . | . | . |
| **29** | . | . | . | . | . | . | . | . | . | . |
| **30** | F | F | F | F | F | F | F | F | F | . |
| **31** | . | . | . | . | . | . | . | . | . | . |
| **32** | C | C | C | C | C | C | C | C | C | C |
| **33** | F | F | F | F | F | F | F | F | F | F |
| **34** | F | F | F | F | F | F | F | F | S | . |
| **35** | F | . | . | . | . | . | . | . | . | . |
| **36** | F | F | . | . | . | . | . | . | . | . |
| **37** | F | F | F | . | . | . | . | S | . | . |
| **38** | F | F | F | F | S | S | . | . | . | . |
| **39** | . | . | . | . | . | . | . | . | x | . |
| **40** | C | C | C | C | C | C | C | C | C | C |
| **41** | C | C | C | C | C | C | C | C | C | C |
| **42** | . | . | . | . | . | . | S | . | . | S |
| **43** | . | . | . | . | . | . | . | . | . | . |
| **44** | . | . | . | . | . | . | . | . | . | . |
| **45** | . | . | . | . | . | . | . | . | . | . |
| **46** | . | . | . | . | . | . | . | . | . | . |
| **47** | . | . | . | . | S | . | . | . | . | . |
| **48** | . | . | . | . | . | . | . | . | . | . |
| **49** | . | . | . | . | . | . | . | . | . | . |
| **50** | F | F | F | F | F | F | F | F | F | . |
| **51** | . | . | . | . | . | . | . | . | . | . |
| **52** | F | . | . | . | . | . | . | . | . | . |
| **53** | . | F | F | F | F | F | F | F | F | F |
| **54** | F | F | F | F | F | F | F | F | F | . |
| **55** | . | . | . | . | . | . | . | . | . | . |
| **56** | . | . | . | . | . | . | . | . | . | . |
| **57** | . | . | . | . | . | . | . | . | . | . |
| **58** | F | F | F | . | . | . | . | . | . | . |
| **59** | . | . | . | . | . | . | . | . | . | . |
| **60** | C | C | C | C | C | C | C | C | C | C |
| **61** | F | F | F | F | F | F | F | F | F | . |
| **62** | K | . | . | . | . | . | x | . | . | . |
| **63** | . | . | . | . | . | . | . | . | . | . |
| **64** | C | C | C | C | C | C | C | C | C | C |
| **65** | C | C | C | C | C | C | C | C | C | C |
| **66** | . | . | . | . | . | . | . | . | . | . |
| **67** | . | . | . | . | S | . | . | . | . | . |
| **68** | F | . | . | . | . | . | . | . | . | . |
| **69** | . | . | . | . | . | . | . | . | . | . |
| **70** | F | F | F | F | F | F | F | F | F | . |
| **71** | x | . | . | . | . | . | x | . | . | . |
| **72** | F | F | F | F | F | F | F | F | F | . |
| **73** | . | . | . | . | . | . | . | S | . | K |
| **74** | F | F | F | F | F | F | F | F | F | . |
| **75** | . | . | . | . | . | S | . | . | . | . |
| **76** | C | C | C | C | C | C | C | C | C | C |
| **77** | . | . | . | . | . | . | . | K | S | F |
| **78** | . | . | . | S | S | S | S | S | S | S |
| **79** | x | . | . | . | . | . | . | . | . | . |
| **80** | C | C | C | C | C | C | C | C | C | C |
| **81** | C | C | C | C | C | C | C | C | C | C |
| **82** | C | C | C | C | C | C | C | C | C | C |
| **83** | C | C | C | C | C | C | C | C | C | C |
| **84** | . | . | . | . | . | . | . | . | . | . |
| **85** | . | . | . | . | . | . | S | S | S | S |
| **86** | . | . | . | . | . | . | . | . | . | . |
| **87** | . | . | . | . | . | . | . | . | . | . |
| **88** | . | . | . | . | . | . | . | . | . | . |
| **89** | . | . | . | . | . | . | . | . | . | . |
| **90** | F | . | . | . | . | S | S | . | . | . |
| **91** | . | x | . | . | . | . | . | . | . | . |
| **92** | F | . | . | S | . | . | . | . | . | . |
| **93** | . | . | . | . | . | S | x | . | . | . |
| **94** | F | F | F | F | F | F | F | F | F | . |
| **95** | . | . | x | . | . | . | . | . | . | . |
| **96** | F | . | . | . | . | . | . | . | . | . |
| **97** | . | . | . | . | . | . | . | . | . | . |
| **98** | F | . | . | . | . | . | . | . | . | . |
| **99** | . | . | . | . | . | . | . | . | . | . |

321 of the 900 three-digit prefixes are excluded (124 of them by more than one result), 14 are provably out of reach of this method, and 565 are open.

Four-digit refinements: 1731 four-digit prefixes whose three-digit parent is still open are excluded (lists `entries..` in `Agent124FourDigit`, plus 2641 in `Agent117P2641`).

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

