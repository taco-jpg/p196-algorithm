import P196.Drafts.Agent119FourColumnPrefix.FourColumnAncestry
import P196.Agent104P620Witness.PalindromeBridge

/-!
# Exact last-step bridge for three-digit palindrome prefixes

Agent #119, task `agent119-four-column-prefix-kernel`.

For a palindrome `P` whose canonical decimal numeral begins with digits
`a,b,c`, the final reverse-and-add step into `P` cannot overflow unless
`(a,b,c)` is one of `110, 111, 121, 122` (`GrowthPrefix`).  This is derived
here from the existing exact overflow-palindrome criterion of
`LychrelDigitSums` together with the carry equations of the two leading
columns; leading digit one is therefore covered.  A non-overflowing final
step has no carries at all (Agent #104's `canonical_last_step` argument), so
the four-column projection of the final predecessor belongs to an explicit
finite root family `rootWords a b c`.

`ancestry_bound_of_checks` is the conditional endpoint: complete row checks,
the short-descent check and initial-rank checks of the roots, together with
the decidable premise that `a b c` is not one of the four growth prefixes,
imply the ordinary-integer ancestry bound.  It has no other premise.
-/

namespace FourColumnKernel

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge

/-- The canonical decimal numeral of `P` has at least three digits and its
leading digits, from the most significant end, are `a`, `b`, `c`. -/
def Starts3 (a b c P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 3 ≤ W ∧
    e (W - 1) = a ∧ e (W - 2) = b ∧ e (W - 3) = c

/-- The target family; palindromicity is explicit. -/
def PalindromeStarts3 (a b c P : Nat) : Prop :=
  Palindrome P ∧ Starts3 a b c P

/-- The only leading-digit patterns of a palindrome of width at least three
that is produced by an overflowing reverse-and-add step. -/
def GrowthPrefix (a b c : Nat) : Prop :=
  a = 1 ∧ ((b = 1 ∧ c ≤ 1) ∨ (b = 2 ∧ 1 ≤ c ∧ c ≤ 2))

instance (a b c : Nat) : Decidable (GrowthPrefix a b c) := by
  unfold GrowthPrefix
  infer_instance

/-- An overflowing step onto a palindrome of width at least three produces
one of the four growth prefixes.  Only the exact overflow criterion
(all pair sums 0 or 11) and the carry equations of the two leading columns
are used. -/
theorem overflow_palindrome_prefix
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P) (hW : 3 ≤ W)
    (hc : carry (columnSum d L) L = 1) :
    GrowthPrefix (e (W - 1)) (e (W - 2)) (e (W - 3)) := by
  have hnext : Canonical P (extended (columnSum d L) L) (L + 1) := by
    rw [← hstep]
    exact canonical_next_overflow n d L hsource hc
  obtain ⟨hwidth, hdigit⟩ := canonical_unique hnext htarget
  have hL : 2 ≤ L := by omega
  have hpal' : Palindrome (step (value d L)) := by
    rw [hsource.2.2.2, hstep]
    exact hpal
  obtain ⟨_, hvals⟩ := (step_palindrome_iff_overflow d L hsource.1 hsource.2.1
    hsource.2.2.1 hc).mp hpal'
  let q := columnSum d L
  have hq0 : q 0 = 11 := by
    have := (step_palindrome_iff_overflow d L hsource.1 hsource.2.1
      hsource.2.2.1 hc).mp hpal'
    exact this.1
  have hsym : q 0 = q (L - 1 - 0) := columnSum_symmetric d L 0 (by omega)
  have hqL1 : q (L - 1) = 11 := by
    simp only [Nat.sub_zero] at hsym
    omega
  have hqL2 : q (L - 2) = 0 ∨ q (L - 2) = 11 := hvals (L - 2) (by omega)
  have hb := carry_bounded q L (columnSum_bounded d L hsource.2.1)
  have hcL1 := hb (L - 1) (by omega)
  have hcL2 := hb (L - 2) (by omega)
  have eq1 := column_equation q (L - 1)
  have eq2 := column_equation q (L - 2)
  have hi1 : L - 1 + 1 = L := by omega
  have hi2 : L - 2 + 1 = L - 1 := by omega
  rw [hi1] at eq1
  rw [hi2] at eq2
  have hcq : carry q L = 1 := hc
  have hoL1 := output_bounded q (L - 1)
  have hoL2 := output_bounded q (L - 2)
  -- Identify the target's leading digits with the extended output.
  have e1 : e (W - 1) = 1 := by
    have h := hdigit L (by omega)
    have hw : W - 1 = L := by omega
    rw [hw, ← h]
    simp only [extended, Nat.lt_irrefl, if_false]
    exact hc
  have e2 : e (W - 2) = output q (L - 1) := by
    have h := hdigit (L - 1) (by omega)
    have hw : W - 2 = L - 1 := by omega
    rw [hw, ← h]
    simp only [extended, show L - 1 < L by omega, if_true]
    rfl
  have e3 : e (W - 3) = output q (L - 2) := by
    have h := hdigit (L - 2) (by omega)
    have hw : W - 3 = L - 2 := by omega
    rw [hw, ← h]
    simp only [extended, show L - 2 < L by omega, if_true]
    rfl
  unfold GrowthPrefix
  rw [e1, e2, e3]
  omega

/-- Outside the four growth prefixes, the final step into the palindrome
does not overflow. -/
theorem no_overflow_of_prefix
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P) (hW : 3 ≤ W)
    (hng : ¬ GrowthPrefix (e (W - 1)) (e (W - 2)) (e (W - 3))) :
    carry (columnSum d L) L = 0 := by
  rcases actual_overflow_cases d L hsource.2.1 with hc | hc
  · exact hc
  · exact absurd (overflow_palindrome_prefix hsource htarget hstep hpal hW hc) hng

/-- Exact final-step bridge: equal widths, no carries, pair sums equal the
target digits.  Same conclusion as Agent #104's `canonical_last_step`, with
the leading-digit hypothesis replaced by the non-growth prefix condition. -/
theorem canonical_last_step3
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P) (hW : 3 ≤ W)
    (hng : ¬ GrowthPrefix (e (W - 1)) (e (W - 2)) (e (W - 3))) :
    L = W ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      (∀ i, i < L → columnSum d L i = e i) ∧
      (∀ i, i < L → columnSum d L i ≤ 9) := by
  have hc := no_overflow_of_prefix hsource htarget hstep hpal hW hng
  have hnext : Canonical P (output (columnSum d L)) L := by
    rw [← hstep]
    exact canonical_next_no_overflow n d L hsource hc
  obtain ⟨hwidth, hdigit⟩ := canonical_unique hnext htarget
  have hp : Palindrome (value (output (columnSum d L)) L) := by
    rw [hnext.2.2.2]
    exact hpal
  have hs := (palindrome_value_iff (output (columnSum d L)) L
    hnext.2.1 (Or.inr hnext.2.2.1)).mp hp
  obtain ⟨hcarry, hpair⟩ := DecimalCarry.no_overflow_palindrome_has_no_carries
    L (columnSum d L) (carry (columnSum d L)) (output (columnSum d L))
    hsource.1 (columnSum_symmetric d L) hs
    (fun i _ => column_equation (columnSum d L) i) rfl hc
  refine ⟨hwidth, hcarry, ?_, ?_⟩
  · intro i hi
    exact (hpair i hi).trans (hdigit i hi)
  · intro i hi
    rw [hpair i hi]
    exact output_bounded _ i

/-- Exact finite superset of the four-column projections of every final
predecessor of a palindrome beginning `a b c`.  Width three contributes the
complete word `[a,b,a]` (only when `c = a` and the odd center `b` is even);
every larger width contributes `[a,b,c,d]` with a decimal digit `d`. -/
def rootWords (a b c : Nat) : List (List Nat) :=
  (if c = a ∧ b % 2 = 0 then [[a, b, a]] else []) ++
    (List.range 10).map (fun d => [a, b, c, d])

/-- The final predecessor of a palindrome beginning `a b c` (outside the
growth prefixes) projects into `rootWords a b c`. -/
theorem last_step_root
    {a b c n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P)
    (hP : PalindromeStarts3 a b c P) (hng : ¬ GrowthPrefix a b c) :
    project4 (columnSum d L) L ∈ rootWords a b c := by
  obtain ⟨hpal, e, W, htarget, hW, ha, hb, hc⟩ := hP
  have hng' : ¬ GrowthPrefix (e (W - 1)) (e (W - 2)) (e (W - 3)) := by
    rw [ha, hb, hc]
    exact hng
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step3 hsource htarget hstep hpal hW hng'
  subst hwidth
  have hp : Palindrome (value e L) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e L htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  have hadm : Admissible L (columnSum d L) := canonical_admissible n d L hsource
  have q0 : columnSum d L 0 = a := by
    rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using ha
  have q1 : columnSum d L 1 = b := by
    rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using hb
  have q2 : columnSum d L 2 = c := by
    rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using hc
  by_cases h3 : L = 3
  · subst h3
    have hca : c = a := by
      have hs2 : columnSum d 3 2 = columnSum d 3 0 :=
        columnSum_symmetric d 3 2 (by omega)
      omega
    have hbe : b % 2 = 0 := by
      have hcen := hadm.2.2.2.2 1 (by omega) (by omega)
      rw [q1] at hcen
      exact hcen
    have hproj : project4 (columnSum d 3) 3 = [a, b, a] := by
      rw [project4_short _ _ (by omega)]
      simp [wordOf, List.range_succ, q0, q1, q2, hca]
    rw [hproj]
    simp [rootWords, hca, hbe]
  · have hL4 : 4 ≤ L := by omega
    have h3s := hsmall 3 (by omega)
    have hproj : project4 (columnSum d L) L = [a, b, c, columnSum d L 3] := by
      rw [project4_long _ _ hL4]
      simp [wordPrefix, segment, q0, q1, q2]
    rw [hproj]
    simp only [rootWords, List.mem_append, List.mem_map, List.mem_range]
    exact Or.inr ⟨columnSum d L 3, by omega, rfl⟩

/-- Generic time bound: if the final predecessor of `orbit A (t + 1)`
always projects into a root family whose members have checked rank at most
`B`, then `t ≤ B`. -/
theorem time_bound_of_root
    {tree : RankTree} (rows : CheckedRows tree (longPred 4))
    (short : ShortDescent tree) {A t B : Nat} {roots : List (List Nat)}
    (hA : 0 < A)
    (hroot : ∀ n d L, Canonical n d L → step n = orbit A (t + 1) →
      project4 (columnSum d L) L ∈ roots)
    (initial : ∀ p ∈ roots, checkInitial tree B p = true) : t ≤ B := by
  obtain ⟨d, L, hcan⟩ := canonical_exists A hA
  let q := columnSum d L
  have ha : Admissible L q := canonical_admissible A d L hcan
  obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
  have hm := hroot (orbit A t) e _ he rfl
  have hproj := project4_congr (columnSum e (iterPairs q L t).1)
    (iterPairs q L t).2 (iterPairs q L t).1 hrep
  rw [hproj] at hm
  obtain ⟨r, hr, hb⟩ := checkInitial_sound (initial _ hm)
  have ht := actual_iterPairs_rank4 rows short q L ha t hr
  omega

/-- Conditional ordinary-integer endpoint: three explicit finite checks
(complete long rows, short descent, initial ranks of the root family) and the
non-growth premise `¬ GrowthPrefix a b c` imply the ancestry bound `B + 1`
for every palindrome beginning `a b c`. -/
theorem ancestry_bound_of_checks
    (tree : RankTree) (rows : CheckedRows tree (longPred 4))
    (short : ShortDescent tree) (a b c B : Nat) (hng : ¬ GrowthPrefix a b c)
    (initial : ∀ p ∈ rootWords a b c, checkInitial tree B p = true) :
    ∀ A P t, 0 < A → PalindromeStarts3 a b c P → orbit A t = P → t ≤ B + 1 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      have ht : t ≤ B := time_bound_of_root rows short hA
        (fun n d L hcan hstep => last_step_root hcan (hstep.trans hreach) hP hng) initial
      omega

/-- Corollary for the ordinary orbit of 196, using the existing
kernel-checked absence of palindromes through time 100. -/
theorem no_196_of_checks
    (tree : RankTree) (rows : CheckedRows tree (longPred 4))
    (short : ShortDescent tree) (a b c B : Nat) (hng : ¬ GrowthPrefix a b c)
    (hB : B + 1 ≤ 100)
    (initial : ∀ p ∈ rootWords a b c, checkInitial tree B p = true) :
    ∀ t, ¬ PalindromeStarts3 a b c (orbit 196 t) :=
  no_196_target_of_ancestry_bound (PalindromeStarts3 a b c) (B + 1) hB
    (fun _ h => h.1) (ancestry_bound_of_checks tree rows short a b c B hng initial)

#print axioms overflow_palindrome_prefix
#print axioms no_overflow_of_prefix
#print axioms canonical_last_step3
#print axioms last_step_root
#print axioms time_bound_of_root
#print axioms ancestry_bound_of_checks
#print axioms no_196_of_checks

end FourColumnKernel
