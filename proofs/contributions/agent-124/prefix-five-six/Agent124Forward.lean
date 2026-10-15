import Agent124PrefixL
import Agent124CodeCert

/-!
# A forward invariant of the 196 orbit in the prefix abstraction (Agent #124)

Agent #104's `actual_forwardPrefix` shows that the first `k` pair sums of the
next state are `forwardPrefix w c`, where `w` is the current `k`-column
projection and `c ∈ {0,1}` is one actual inner carry.  A finite set of words
that contains the projection of the 196 orbit at time 100 and is closed under
both carry choices therefore contains every later projection.  Since the last
predecessor of a non-overflow palindrome has projection equal to the
palindrome's leading digits, no palindrome in the 196 orbit can begin with a
`k`-digit word outside the set.

Everything here is conditional on two explicit finite checks (closure and the
initial membership); a concrete code-keyed set discharges them by kernel
reduction in a separate module.  This is not a Lychrel proof: such sets
contain digit words.
-/

namespace Agent124.Forward

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate Agent124.PrefixK Agent124.PrefixR Agent124.LeadOne Agent124.PrefixL Agent124.CodeCert

/-- Membership of a word in a code-keyed set. -/
def Mem (t : CodeTree) (w : List Nat) : Prop := (lookupC t (wordCode w)).isSome = true

/-- Forward-closure check of one stored key. Keys of other lengths are ignored. -/
def fwdOK (t : CodeTree) (k c : Nat) : Bool :=
  !(Nat.beq (decode c).length k) ||
    ((lookupC t (wordCode (forwardPrefix (decode c) 0))).isSome &&
      (lookupC t (wordCode (forwardPrefix (decode c) 1))).isSome)

/-- Boolean check of every key of a subtree. -/
def allFwd (t : CodeTree) (k : Nat) : CodeTree → Bool
  | .empty => true
  | .node c _ l rt => allFwd t k l && fwdOK t k c && allFwd t k rt

theorem allFwd_sound {t : CodeTree} {k : Nat} :
    ∀ {sub : CodeTree}, allFwd t k sub = true → sub.All (fun c _ => fwdOK t k c = true)
  | .empty, _ => trivial
  | .node c r l rt, h => by
      simp only [allFwd, Bool.and_eq_true] at h
      exact ⟨allFwd_sound h.1.1, h.1.2, allFwd_sound h.2⟩

theorem mem_forward {t : CodeTree} {k : Nat} (hk : k ≤ 32)
    (closed : t.All (fun c _ => fwdOK t k c = true))
    {w : List Nat} (hb : ∀ x ∈ w, x < 19) (hl : w.length = k) (hw : Mem t w)
    {e : Nat} (he : e ≤ 1) : Mem t (forwardPrefix w e) := by
  unfold Mem at hw
  obtain ⟨r, hr⟩ := Option.isSome_iff_exists.mp hw
  have hok := lookupC_all closed hr
  unfold fwdOK at hok
  rw [decode_wordCode w hb (by omega)] at hok
  have hlen : Nat.beq w.length k = true := by simp only [Nat.beq_eq]; exact hl
  rw [hlen] at hok
  simp only [Bool.not_true, Bool.false_or, Bool.and_eq_true] at hok
  have : e = 0 ∨ e = 1 := by omega
  rcases this with rfl | rfl
  · exact hok.1
  · exact hok.2

theorem iterPairs_width_ge (q : Nat → Nat) (L : Nat) :
    ∀ s, L ≤ (iterPairs q L s).1
  | 0 => Nat.le_refl L
  | s + 1 => by
      have ih := iterPairs_width_ge q L s
      change L ≤ nextWidth (iterPairs q L s).2 (iterPairs q L s).1
      have := width_le_nextWidth (iterPairs q L s).2 (iterPairs q L s).1
      omega

/-- Every later `k`-column projection of an actual trajectory stays in a
forward-closed set containing the initial projection. -/
theorem invariant {t : CodeTree} {k : Nat} (hk0 : 0 < k) (hk : k ≤ 32)
    (closed : t.All (fun c _ => fwdOK t k c = true))
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (hkL : k ≤ L)
    (h0 : Mem t (wordPrefix q k)) :
    ∀ s, Mem t (wordPrefix (iterPairs q L s).2 k)
  | 0 => h0
  | s + 1 => by
      have ih := invariant hk0 hk closed q L ha hkL h0 s
      let v := iterPairs q L s
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L s ha
      have hkv : k ≤ v.1 := Nat.le_trans hkL (iterPairs_width_ge q L s)
      change Mem t (wordPrefix (nextColumns v.2 v.1) k)
      rw [← actual_forwardPrefix v.2 v.1 k hv hkv]
      have hc := DecimalDigits.carry_bounded v.2 v.1 hv.2.2.1 (v.1 - k) (by omega)
      exact mem_forward hk closed (wordPrefix_lt19 v.2 v.1 k hv hkv)
        (prefix_length v.2 k) ih hc

/-- With a prefix of full certificate width, the initial family is that prefix. -/
theorem eq_of_mem_initialWordsL {k : Nat} {pre w : List Nat} (hlen : pre.length = k)
    (h : w ∈ initialWordsL k pre) : w = pre := by
  unfold initialWordsL at h
  rw [List.mem_filter] at h
  obtain ⟨h, _⟩ := h
  rw [List.mem_flatMap] at h
  obtain ⟨j, hj, h⟩ := h
  have hj0 : j = 0 := by
    have := List.mem_range.mp hj
    omega
  subst hj0
  simp [digitLists] at h
  exact h

theorem digitLists_length : ∀ {m : Nat} {w : List Nat}, w ∈ digitLists m → w.length = m
  | 0, w, h => by
      simp only [digitLists, List.mem_singleton] at h
      subst h
      rfl
  | m + 1, w, h => by
      simp only [digitLists, List.mem_flatMap, List.mem_range, List.mem_map] at h
      obtain ⟨a, _, t, ht, rfl⟩ := h
      simp [digitLists_length ht]

/-- Membership in an explicit list of excluded words with a fixed leading
digit gives the three premises of `no_196_outside`. -/
theorem mem_excluded_props {k a : Nat} {f : CodeTree} {w : List Nat} (hk : 1 ≤ k)
    (hw : w ∈ ((digitLists (k - 1)).map ([a] ++ ·)).filter
      (fun w => noOverflowPre w && (lookupC f (wordCode w)).isNone)) :
    w.length = k ∧ noOverflowPre w = true ∧ lookupC f (wordCode w) = none := by
  rw [List.mem_filter, List.mem_map] at hw
  obtain ⟨⟨t, ht, rfl⟩, h⟩ := hw
  simp only [Bool.and_eq_true, Option.isNone_iff_eq_none] at h
  refine ⟨?_, h.1, h.2⟩
  simp only [List.length_append, List.length_singleton, digitLists_length ht]
  omega

/-! ## The concrete 196 state at time 100 -/

/-- `Lychrel196.orbit 196 100`, a 47-digit number. -/
def N100 : Nat := 44757771534490515617290699271561508443627774644

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem orbit196_100 : orbit 196 100 = N100 := by decide

def d100 (i : Nat) : Nat := (N100 / 10 ^ i) % 10

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem value100 : value d100 47 = N100 := by decide

theorem canonical100 : Canonical N100 d100 47 := by
  refine ⟨by decide, fun i _ => ?_, by decide, value100⟩
  unfold d100
  omega

/-- The pair word of the 196 orbit at time 100. -/
def q100 : Nat → Nat := columnSum d100 47

/-- All-time exclusion: if a code-keyed set is forward closed and contains the
`k`-column projection of the 196 orbit at time 100, then no state of the 196
orbit, at any time, is a palindrome beginning with a `k`-digit word that is
missing from the set (when a final overflow into that word is impossible). -/
theorem no_196_outside {t : CodeTree} {k : Nat} (hk1 : 1 ≤ k) (hk : k ≤ 32)
    (hk47 : k ≤ 47)
    (closed : t.All (fun c _ => fwdOK t k c = true))
    (init : Mem t (wordPrefix q100 k)) :
    ∀ T pre, pre.length = k → noOverflowPre pre = true →
      lookupC t (wordCode pre) = none → ¬ PalStartsL pre (orbit 196 T) := by
  intro T pre hlen hno hnone hP
  by_cases hT : T ≤ 100
  · exact no_palindrome_through_100 T hT hP.1
  · obtain ⟨s, rfl⟩ : ∃ s, T = 100 + (s + 1) := ⟨T - 101, by omega⟩
    have horb : orbit 196 (100 + (s + 1)) = step (orbit N100 s) := by
      rw [LychrelCertificates.orbit_add, orbit196_100]
      rfl
    rw [horb] at hP
    have hadm : Admissible 47 q100 := canonical_admissible N100 d100 47 canonical100
    obtain ⟨e, he, hrep⟩ :=
      iterPairs_representation N100 d100 q100 47 s canonical100 (fun _ _ => rfl)
    have hm := canonical_last_step_initialL k pre (by omega) (by omega) hno he rfl hP
    have hproj := projectK_congr k (columnSum e (iterPairs q100 47 s).1)
      (iterPairs q100 47 s).2 (iterPairs q100 47 s).1 hrep
    rw [hproj] at hm
    have hW : k ≤ (iterPairs q100 47 s).1 :=
      Nat.le_trans hk47 (iterPairs_width_ge q100 47 s)
    rw [projectK_long _ _ _ hW] at hm
    have heq := eq_of_mem_initialWordsL hlen hm
    have hinv := invariant (by omega) hk closed q100 47 hadm hk47 init s
    rw [heq] at hinv
    unfold Mem at hinv
    rw [hnone] at hinv
    exact Bool.false_ne_true hinv

end Agent124.Forward

#print axioms Agent124.Forward.mem_forward
#print axioms Agent124.Forward.invariant
#print axioms Agent124.Forward.orbit196_100
#print axioms Agent124.Forward.canonical100
#print axioms Agent124.Forward.no_196_outside
#print axioms Agent124.Forward.digitLists_length
#print axioms Agent124.Forward.mem_excluded_props
