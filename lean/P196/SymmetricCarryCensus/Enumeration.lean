import P196.Agent104P620Witness.Agent124PrefixK
import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9FiniteProducts
import P196.SymmetricCarryCensus.Support

set_option autoImplicit false

/-!
# Exact membership and duplicate freedom of the original symmetric-word list

The original half-word enumerator is the existing finite list product over
the nineteen coefficients. Taking the initial half recovers every input to
the mirror map, so mirroring does not introduce duplicates. The original
filter imposes exactly the positive exterior and even-center conditions.

Completeness reuses `wordOf_mem_symWords`; no second full-word enumerator is
introduced. These are coefficient words, without weights for their possible
ordinary digit realizations.
-/

namespace SymmetricCarryCensus

open Agent124.PrefixK SevenColumn.ShortBoundary FoldedDecimal

/-- The original half-word enumerator is the existing finite list product. -/
theorem lists19_eq_wordChoices (r : Nat) :
    lists19 r = P196.Agent9.Ensemble.wordChoices (List.range 19) r := by
  induction r with
  | zero => rfl
  | succ r ih => simp only [lists19, P196.Agent9.Ensemble.wordChoices, ih]

/-- Exact length and coefficient semantics for the original half words. -/
theorem mem_lists19_iff (r : Nat) (h : List Nat) :
    h ∈ lists19 r ↔ h.length = r ∧ ∀ x ∈ h, x < 19 := by
  rw [lists19_eq_wordChoices, P196.Agent9.Ensemble.mem_wordChoices]
  simp only [List.mem_range]

/-- Reifying the complete finite function recovers its original list. -/
theorem wordOf_wordFun (w : List Nat) : wordOf (wordFun w) w.length = w := by
  apply List.ext_getElem
  · simp [wordOf]
  · intro i _ hi
    simp [wordOf, wordFun, hi]

/-- The original mirror retains the supplied canonical half as its prefix. -/
theorem mirror_take_half (L : Nat) (h : List Nat)
    (hh : h.length = (L + 1) / 2) :
    (mirror L h).take ((L + 1) / 2) = h := by
  unfold mirror
  rw [← List.map_take, List.take_range, Nat.min_eq_left (by omega : (L + 1) / 2 ≤ L)]
  calc
    (List.range ((L + 1) / 2)).map
        (fun i => h.getD (min i (L - 1 - i)) 0) =
      (List.range ((L + 1) / 2)).map (fun i => h.getD i 0) := by
        apply List.map_congr_left
        intro i hi
        have hi' := List.mem_range.mp hi
        rw [Nat.min_eq_left (by omega : i ≤ L - 1 - i)]
    _ = wordOf (wordFun h) h.length := by
      rw [hh]
      rfl
    _ = h := wordOf_wordFun h

/-- Reading a mirrored coefficient uses the nearer exterior half index. -/
theorem wordFun_mirror (L : Nat) (h : List Nat) (i : Nat) (hi : i < L) :
    wordFun (mirror L h) i = h.getD (min i (L - 1 - i)) 0 := by
  exact getD_range_map (fun j => h.getD (min j (L - 1 - j)) 0) L i hi

private theorem getD_lt19 (h : List Nat) (hb : ∀ x ∈ h, x < 19) (i : Nat) :
    h.getD i 0 < 19 := by
  cases he : h[i]? with
  | none => simp [he]
  | some x =>
    have hx := hb x (List.mem_of_getElem? he)
    simpa only [List.getD_eq_getElem?_getD, he, Option.getD_some] using hx

/-- The original full-word enumeration is exactly finite-word admissibility. -/
theorem mem_symWords_iff (L : Nat) (w : List Nat) :
    w ∈ Agent124.PrefixK.symWords L ↔
      w.length = L ∧ FoldedDecimal.Admissible L (SevenColumn.ShortBoundary.wordFun w) := by
  constructor
  · intro hw
    unfold symWords at hw
    obtain ⟨hmap, hok⟩ := List.mem_filter.mp hw
    obtain ⟨h, hh, rfl⟩ := List.mem_map.mp hmap
    have hb := ((mem_lists19_iff ((L + 1) / 2) h).mp hh).2
    have hL : 0 < L := by
      by_cases hz : L = 0
      · subst L
        simp [symOK, mirror] at hok
      · omega
    have htest : 0 < (mirror L h).getD 0 0 ∧
        (L % 2 = 0 ∨ ((mirror L h).getD (L / 2) 0) % 2 = 0) := by
      simpa only [symOK, Bool.and_eq_true, decide_eq_true_eq,
        Bool.or_eq_true, beq_iff_eq] using hok
    refine ⟨by simp [mirror], hL, ?_, ?_, ?_, ?_⟩
    · simpa only [wordFun, List.getD_eq_getElem?_getD] using htest.1
    · intro i hi
      rw [wordFun_mirror L h i hi]
      have hiBound := getD_lt19 h hb (min i (L - 1 - i))
      omega
    · intro i hi
      have hj : L - 1 - i < L := by omega
      have he : L - 1 - (L - 1 - i) = i := by omega
      rw [wordFun_mirror L h i hi, wordFun_mirror L h (L - 1 - i) hj,
        he, Nat.min_comm]
    · intro i hi hfix
      have hmid : i = L / 2 := by omega
      have hodd : L % 2 ≠ 0 := by omega
      have hc := htest.2.resolve_left hodd
      simpa only [wordFun, List.getD_eq_getElem?_getD, hmid] using hc
  · rintro ⟨hlen, ha⟩
    have hm := wordOf_mem_symWords (wordFun w) L ha
    have he : wordOf (wordFun w) L = w := by
      rw [← hlen]
      exact wordOf_wordFun w
    simpa only [he] using hm

/-- No admissible full word occurs twice in the original enumeration. -/
theorem symWords_nodup (L : Nat) : (symWords L).Nodup := by
  have hbase : (lists19 ((L + 1) / 2)).Nodup := by
    rw [lists19_eq_wordChoices]
    exact P196.Agent9.Ensemble.wordChoices_nodup _ List.nodup_range _
  have hmap : ((lists19 ((L + 1) / 2)).map (mirror L)).Nodup := by
    apply nodup_map_of_injOn _ _ hbase
    intro a ha b hb he
    have hla := ((mem_lists19_iff ((L + 1) / 2) a).mp ha).1
    have hlb := ((mem_lists19_iff ((L + 1) / 2) b).mp hb).1
    have ht := congrArg (fun w : List Nat => w.take ((L + 1) / 2)) he
    change (mirror L a).take ((L + 1) / 2) =
      (mirror L b).take ((L + 1) / 2) at ht
    rw [mirror_take_half L a hla, mirror_take_half L b hlb] at ht
    exact ht
  exact List.Pairwise.filter (symOK L) hmap

#print axioms mem_symWords_iff
#print axioms symWords_nodup

end SymmetricCarryCensus
