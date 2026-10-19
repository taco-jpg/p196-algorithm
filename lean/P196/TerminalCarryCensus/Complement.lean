import P196.TerminalCarryCensus.Scan
import P196.TerminalCarryCensus.Halves

/-!
Subtracting each independent coefficient from eighteen permutes the half
words, including the empty half. Mirroring preserves this pointwise
complement relation. The original mirror recovery identifies the neutral
full words with the all-nine halves, so the finite scan theorem applies
without choosing a first or last non-nine position.
-/

set_option autoImplicit false

namespace TerminalCarryCensus

open DecimalDigits SevenColumn.ShortBoundary Agent124.PrefixK
open SymmetricCarryCensus

/-- Complement every independent coefficient around eighteen. -/
def halfComplement (h : List Nat) : List Nat :=
  h.map (fun a => 18 - a)

private theorem getD_mem_of_lt (h : List Nat) (i : Nat)
    (hi : i < h.length) : h.getD i 0 ∈ h := by
  simpa only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi,
    Option.getD_some] using List.getElem_mem hi

private theorem halfComplement_get (h : List Nat) (i : Nat)
    (hi : i < h.length) :
    (halfComplement h).getD i 0 = 18 - h.getD i 0 := by
  simp [halfComplement, List.getD_eq_getElem?_getD,
    List.getElem?_map, hi]

/-- The complement preserves the exact bounded-half and center conditions. -/
theorem halfComplement_mem (L : Nat) (h : List Nat) (hh : h ∈ halves L) :
    halfComplement h ∈ halves L := by
  obtain ⟨hlen, hb, hc⟩ := (mem_halves_iff L h).mp hh
  apply (mem_halves_iff L (halfComplement h)).mpr
  refine ⟨by simpa only [halfComplement, List.length_map] using hlen, ?_, ?_⟩
  · intro a ha
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp ha
    have hxBound := hb x hx
    omega
  · by_cases he : L % 2 = 0
    · exact Or.inl he
    · right
      have hcenter := hc.resolve_left he
      have hi : L / 2 < h.length := by omega
      rw [halfComplement_get h (L / 2) hi]
      have hbound := hb _ (getD_mem_of_lt h (L / 2) hi)
      omega

/-- Complementing an enumerated half twice recovers the original half. -/
theorem halfComplement_involutive (L : Nat) (h : List Nat)
    (hh : h ∈ halves L) : halfComplement (halfComplement h) = h := by
  have hb := ((mem_halves_iff L h).mp hh).2.1
  change (h.map (fun a => 18 - a)).map (fun a => 18 - a) = h
  rw [List.map_map]
  calc
    h.map ((fun a => 18 - a) ∘ (fun a => 18 - a)) = h.map id := by
      apply List.map_congr_left
      intro a ha
      have haBound := hb a ha
      simp only [Function.comp_apply, id_eq]
      omega
    _ = h := List.map_id h

/-- Complementing all halves changes only their order in the enumeration. -/
theorem halfComplement_perm (L : Nat) :
    ((halves L).map halfComplement).Perm (halves L) := by
  refine perm_of_nodup_mem_iff _ _ ?_ (halves_nodup L) ?_
  · apply nodup_map_of_injOn _ _ (halves_nodup L)
    intro a ha b hb heq
    have h := congrArg halfComplement heq
    simpa only [halfComplement_involutive L a ha,
      halfComplement_involutive L b hb] using h
  · intro h
    constructor
    · intro hh
      obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hh
      exact halfComplement_mem L a ha
    · intro hh
      exact List.mem_map.mpr ⟨halfComplement h, halfComplement_mem L h hh,
        halfComplement_involutive L h hh⟩

/-- Every genuine mirrored column is complementary to its transformed column. -/
theorem mirror_complementary (L : Nat) (h : List Nat) (hh : h ∈ halves L) :
    ∀ i, i < L → wordFun (mirror L h) i +
      wordFun (mirror L (halfComplement h)) i = 18 := by
  obtain ⟨hlen, hb, _⟩ := (mem_halves_iff L h).mp hh
  intro i hi
  have hindex : min i (L - 1 - i) < h.length := by omega
  rw [wordFun_mirror L h i hi,
    wordFun_mirror L (halfComplement h) i hi,
    halfComplement_get h (min i (L - 1 - i)) hindex]
  have hbound := hb _ (getD_mem_of_lt h (min i (L - 1 - i)) hindex)
  omega

/-- The original mirror is all nine exactly when its recovered half is all nine. -/
theorem mirror_all_nines_iff (L : Nat) (h : List Nat) (hh : h ∈ halves L) :
    ((List.range L).all (fun i => wordFun (mirror L h) i == 9)) =
      h.all (fun a => a == 9) := by
  have hlen := ((mem_halves_iff L h).mp hh).1
  rw [Bool.eq_iff_iff]
  simp only [List.all_eq_true, List.mem_range, beq_iff_eq]
  constructor
  · intro hall a ha
    have htake : a ∈ (mirror L h).take ((L + 1) / 2) := by
      rw [mirror_take_half L h hlen]
      exact ha
    have hfull : a ∈ mirror L h := List.mem_of_mem_take htake
    obtain ⟨i, hi, heq⟩ := List.mem_map.mp hfull
    have hiL := List.mem_range.mp hi
    have hread := hall i hiL
    rw [wordFun_mirror L h i hiL] at hread
    exact heq.symm.trans hread
  · intro hall i hi
    rw [wordFun_mirror L h i hi]
    have hindex : min i (L - 1 - i) < h.length := by omega
    exact hall _ (getD_mem_of_lt h (min i (L - 1 - i)) hindex)

/-- The paired actual terminal carries sum to one except on an all-nine half. -/
theorem terminal_complement_sum (L : Nat) (h : List Nat) (hh : h ∈ halves L) :
    carry (wordFun (mirror L h)) L +
      carry (wordFun (mirror L (halfComplement h))) L =
        if h.all (fun a => a == 9) then 0 else 1 := by
  have hs := complementary_carry_sum (wordFun (mirror L h))
    (wordFun (mirror L (halfComplement h))) L (mirror_complementary L h hh)
  rw [mirror_all_nines_iff L h hh] at hs
  exact hs

#print axioms halfComplement_mem
#print axioms halfComplement_involutive
#print axioms halfComplement_perm
#print axioms mirror_complementary
#print axioms mirror_all_nines_iff
#print axioms terminal_complement_sum

end TerminalCarryCensus
