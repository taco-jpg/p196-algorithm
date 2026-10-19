import P196.TerminalCarryCensus.Balance

/-!
# Terminal-one counts in the original admissible enumeration

Mirroring the auxiliary half products creates no duplicates. Every original
admissible word has one such half. Conversely, a mirrored auxiliary word
with terminal carry one must have positive exterior, so it belongs to the
original symWords list. This identifies the two filtered lists without
introducing another complete admissible-word enumeration.
-/

set_option autoImplicit false

namespace TerminalCarryCensus

open DecimalDigits Agent124.PrefixK SevenColumn.ShortBoundary
open SymmetricCarryCensus

private theorem odd_center_value (L : Nat) (h : List Nat) (he : L % 2 ≠ 0) :
    wordFun (mirror L h) (L / 2) = h.getD (L / 2) 0 := by
  rw [wordFun_mirror L h (L / 2) (by omega), Nat.min_eq_left (by omega)]

private theorem mirror_mem_of_positive (L : Nat) (h : List Nat)
    (hh : h ∈ halves L) (hp : 0 < wordFun (mirror L h) 0) :
    mirror L h ∈ symWords L := by
  have hd := (mem_halves_iff L h).mp hh
  unfold symWords
  apply List.mem_filter.mpr
  refine ⟨List.mem_map.mpr ⟨h,
    (mem_lists19_iff ((L + 1) / 2) h).mpr ⟨hd.1, hd.2.1⟩, rfl⟩, ?_⟩
  simp only [symOK, Bool.and_eq_true, decide_eq_true_eq,
    Bool.or_eq_true, beq_iff_eq]
  refine ⟨?_, ?_⟩
  · simpa only [wordFun, List.getD_eq_getElem?_getD] using hp
  · by_cases he : L % 2 = 0
    · exact Or.inl he
    · apply Or.inr
      change wordFun (mirror L h) (L / 2) % 2 = 0
      rw [odd_center_value L h he]
      exact hd.2.2.resolve_left he

private theorem original_word_has_half (L : Nat) (w : List Nat)
    (hw : w ∈ symWords L) : ∃ h ∈ halves L, mirror L h = w := by
  unfold symWords at hw
  obtain ⟨hmap, hok⟩ := List.mem_filter.mp hw
  obtain ⟨h, hraw, rfl⟩ := List.mem_map.mp hmap
  have hd := (mem_lists19_iff ((L + 1) / 2) h).mp hraw
  refine ⟨h, (mem_halves_iff L h).mpr ⟨hd.1, hd.2, ?_⟩, rfl⟩
  by_cases he : L % 2 = 0
  · exact Or.inl he
  · apply Or.inr
    simp only [symOK, Bool.and_eq_true, decide_eq_true_eq,
      Bool.or_eq_true, beq_iff_eq] at hok
    have hc : wordFun (mirror L h) (L / 2) % 2 = 0 := by
      simpa only [wordFun, List.getD_eq_getElem?_getD] using
        hok.2.resolve_left he
    rw [odd_center_value L h he] at hc
    exact hc

private theorem terminal_one_positive (L : Nat) (h : List Nat)
    (hh : h ∈ halves L) (hc : carry (wordFun (mirror L h)) L = 1) :
    0 < wordFun (mirror L h) 0 := by
  have hL : 0 < L := by
    by_cases hz : L = 0
    · subst L
      simp [carry] at hc
    · omega
  have hb : ∀ i, i < L → wordFun (mirror L h) i ≤ 18 := by
    intro i hi
    have hsum := mirror_complementary L h hh i hi
    omega
  have hprev := carry_bounded (wordFun (mirror L h)) L hb (L - 1) (by omega)
  have hlast : wordFun (mirror L h) (L - 1) = wordFun (mirror L h) 0 := by
    rw [wordFun_mirror L h (L - 1) (by omega), wordFun_mirror L h 0 hL]
    simp
  have hrec : carry (wordFun (mirror L h)) L =
      (wordFun (mirror L h) (L - 1) +
        carry (wordFun (mirror L h)) (L - 1)) / 10 := by
    calc
      carry (wordFun (mirror L h)) L =
          carry (wordFun (mirror L h)) ((L - 1) + 1) :=
        congrArg (carry (wordFun (mirror L h))) (by omega)
      _ = _ := rfl
  rw [hlast] at hrec
  omega

private theorem terminal_count_transfer (L : Nat) :
    (symWords L).countP (fun w => carry (wordFun w) L == 1) = halfOnes L := by
  have hn : ((halves L).map (mirror L)).Nodup := by
    apply nodup_map_of_injOn _ _ (halves_nodup L)
    intro a ha b hb heq
    have hla := ((mem_halves_iff L a).mp ha).1
    have hlb := ((mem_halves_iff L b).mp hb).1
    calc
      a = (mirror L a).take ((L + 1) / 2) := (mirror_take_half L a hla).symm
      _ = (mirror L b).take ((L + 1) / 2) :=
        congrArg (fun w : List Nat => w.take ((L + 1) / 2)) heq
      _ = b := mirror_take_half L b hlb
  have hp :
      (((halves L).map (mirror L)).filter
        (fun w => carry (wordFun w) L == 1)).Perm
      ((symWords L).filter (fun w => carry (wordFun w) L == 1)) := by
    refine perm_of_nodup_mem_iff _ _
      (List.Pairwise.filter _ hn)
      (List.Pairwise.filter _ (symWords_nodup L)) ?_
    intro w
    simp only [List.mem_filter]
    constructor
    · rintro ⟨hmap, hc⟩
      obtain ⟨h, hh, rfl⟩ := List.mem_map.mp hmap
      have hone : carry (wordFun (mirror L h)) L = 1 := by
        simpa only [beq_iff_eq] using hc
      exact ⟨mirror_mem_of_positive L h hh (terminal_one_positive L h hh hone), hc⟩
    · rintro ⟨hw, hc⟩
      obtain ⟨h, hh, heq⟩ := original_word_has_half L w hw
      exact ⟨List.mem_map.mpr ⟨h, hh, heq⟩, hc⟩
  simpa only [halfOnes, List.countP_eq_length_filter, List.filter_map,
    List.length_map, Function.comp_def] using hp.length_eq.symm

/-- Exact terminal-one count at every even width, including width zero. -/
theorem terminal_ones_even (m : Nat) :
    (symWords (2 * m)).countP
      (fun w => carry (wordFun w) (2 * m) == 1) = (19 ^ m - 1) / 2 := by
  rw [terminal_count_transfer]
  exact half_ones_even m

/-- Exact terminal-one count at every odd width, including width one. -/
theorem terminal_ones_odd (m : Nat) :
    (symWords (2 * m + 1)).countP
      (fun w => carry (wordFun w) (2 * m + 1) == 1) = 5 * 19 ^ m := by
  rw [terminal_count_transfer]
  exact half_ones_odd m

#print axioms terminal_ones_even
#print axioms terminal_ones_odd

end TerminalCarryCensus
