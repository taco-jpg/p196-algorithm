import P196.Agent101DigitSplit.Agent101MultiplicityBounds

/-!
Agent #101. Complete finite digit-split enumeration for a symmetric
coefficient word. This module counts original digit lists, not inverse
fibers of the autonomous pair-word map. No infinite-avoidance conclusion.
-/

namespace Agent101

def coefficientWord (h : List Nat) (c : Option Nat) : List Nat :=
  h ++ c.toList ++ h.reverse

def digitPairSums (ds : List Nat) : List Nat :=
  List.zipWith Nat.add ds ds.reverse

def digitsBounded (ds : List Nat) : Prop :=
  ∀ d ∈ ds, d ≤ 9

def canonicalDigits (ds : List Nat) : Prop :=
  digitsBounded ds ∧ 0 < ds.getLastD 0

def wrapDigits (a b : Nat) (ds : List Nat) : List Nat :=
  a :: (ds ++ [b])

def rawWords : List Nat → Option Nat → List (List Nat)
  | [], c => centerWords c
  | s :: h, c => (pairChoices false s).flatMap fun p =>
      (rawWords h c).map (wrapDigits p.1 p.2)

def canonicalWords : List Nat → Option Nat → List (List Nat)
  | [], none => []
  | [], some s => if 0 < s then centerWords (some s) else []
  | s :: h, c => (pairChoices true s).flatMap fun p =>
      (rawWords h c).map (wrapDigits p.1 p.2)

theorem coefficientWord_cons (s : Nat) (h : List Nat) (c : Option Nat) :
    coefficientWord (s :: h) c = wrapDigits s s (coefficientWord h c) := by
  simp [coefficientWord, wrapDigits, List.append_assoc]

theorem length_coefficientWord (h : List Nat) (c : Option Nat) :
    (coefficientWord h c).length = 2 * h.length + c.toList.length := by
  simp only [coefficientWord, List.length_append, List.length_reverse]
  omega

theorem length_digitPairSums (ds : List Nat) :
    (digitPairSums ds).length = ds.length := by
  simp [digitPairSums, List.length_zipWith]

theorem length_wrapDigits (a b : Nat) (ds : List Nat) :
    (wrapDigits a b ds).length = ds.length + 2 := by
  simp [wrapDigits, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

theorem getLastD_wrapDigits (a b d : Nat) (ds : List Nat) :
    (wrapDigits a b ds).getLastD d = b := by
  simp only [wrapDigits, List.getLastD_cons, List.getLastD_concat]

theorem digitsBounded_wrapDigits (a b : Nat) (ds : List Nat) :
    digitsBounded (wrapDigits a b ds) ↔ a ≤ 9 ∧ digitsBounded ds ∧ b ≤ 9 := by
  constructor
  · intro hb
    refine ⟨hb a (by simp [wrapDigits]), ?_, hb b (by simp [wrapDigits])⟩
    intro d hd
    exact hb d (by simp [wrapDigits, hd])
  · rintro ⟨ha, hm, hb⟩ d hd
    simp only [wrapDigits, List.mem_cons, List.mem_append, List.mem_singleton,
      List.not_mem_nil, or_false] at hd
    rcases hd with h | h | h
    · simpa [h] using ha
    · exact hm d h
    · simpa [h] using hb

theorem canonicalDigits_wrapDigits (a b : Nat) (ds : List Nat) :
    canonicalDigits (wrapDigits a b ds) ↔
      a ≤ 9 ∧ digitsBounded ds ∧ b ≤ 9 ∧ 0 < b := by
  simp only [canonicalDigits, digitsBounded_wrapDigits, getLastD_wrapDigits,
    and_assoc]

theorem digitPairSums_wrapDigits (a b : Nat) (ds : List Nat) :
    digitPairSums (wrapDigits a b ds) =
      wrapDigits (a + b) (a + b) (digitPairSums ds) := by
  unfold digitPairSums wrapDigits
  simp only [List.reverse_cons, List.reverse_append, List.reverse_nil,
    List.nil_append, List.cons_append, List.zipWith_cons_cons]
  rw [List.zipWith_append (show ds.length = ds.reverse.length by simp)]
  simp [Nat.add_comm]

theorem wrapDigits_injective (a b a' b' : Nat) (ds ds' : List Nat)
    (heq : wrapDigits a b ds = wrapDigits a' b' ds') :
    a = a' ∧ b = b' ∧ ds = ds' := by
  obtain ⟨ha, ht⟩ := List.cons.inj heq
  have hlen : ds.length = ds'.length := by
    have hh := congrArg List.length ht
    simp only [List.length_append, List.length_cons, List.length_nil] at hh
    omega
  have hb : b = b' := by
    have hh := List.append_inj_right ht hlen
    exact (List.cons.inj hh).1
  exact ⟨ha, hb, List.append_inj_left ht hlen⟩

theorem exists_init_last (ds : List Nat) (hne : ds ≠ []) :
    ∃ inner b, ds = inner ++ [b] := by
  induction ds with
  | nil => exact False.elim (hne rfl)
  | cons a ds ih =>
    cases ds with
    | nil => exact ⟨[], a, rfl⟩
    | cons a' ds' =>
      obtain ⟨inner, b, heq⟩ := ih (by simp)
      exact ⟨a :: inner, b, congrArg (List.cons a) heq⟩

theorem exists_wrapDigits (ds : List Nat) (hlen : 2 ≤ ds.length) :
    ∃ a b inner, ds = wrapDigits a b inner := by
  cases ds with
  | nil => simp at hlen
  | cons a ds =>
    have hne : ds ≠ [] := by intro he; simp [he] at hlen
    obtain ⟨inner, b, heq⟩ := exists_init_last ds hne
    exact ⟨a, b, inner, congrArg (List.cons a) heq⟩

theorem mem_centerWords_iff_pairSums (c : Option Nat) (ds : List Nat) :
    ds ∈ centerWords c ↔ ds.length = c.toList.length ∧
      digitsBounded ds ∧ digitPairSums ds = c.toList := by
  cases c with
  | none =>
    rw [mem_centerWords_none]
    constructor
    · intro heq; subst ds; simp [digitsBounded, digitPairSums]
    · rintro ⟨hlen, _, _⟩
      exact List.length_eq_zero_iff.mp hlen
  | some s =>
    rw [mem_centerWords_some]
    constructor
    · rintro ⟨hs, heven, rfl⟩
      have hd : s / 2 ≤ 9 := by omega
      have hsum : s / 2 + s / 2 = s := by omega
      simp [digitsBounded, digitPairSums, hd, hsum]
    · rintro ⟨hlen, hb, hp⟩
      cases ds with
      | nil => simp at hlen
      | cons a ds =>
        have htail : ds = [] := by
          apply List.length_eq_zero_iff.mp
          simp only [List.length_cons, Option.toList_some, List.length_nil] at hlen
          omega
        subst ds
        have ha : a ≤ 9 := hb a (by simp)
        have heq : a + a = s := by
          simpa [digitPairSums] using hp
        refine ⟨by omega, by omega, ?_⟩
        have hh : a = s / 2 := by omega
        simp [hh]

theorem mem_rawWords (h : List Nat) (c : Option Nat) (ds : List Nat) :
    ds ∈ rawWords h c ↔ ds.length = (coefficientWord h c).length ∧
      digitsBounded ds ∧ digitPairSums ds = coefficientWord h c := by
  induction h generalizing ds with
  | nil =>
    simpa [rawWords, coefficientWord] using mem_centerWords_iff_pairSums c ds
  | cons s h ih =>
    rw [rawWords]
    constructor
    · intro hm
      obtain ⟨p, hp, hm⟩ := List.mem_flatMap.mp hm
      obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hm
      obtain ⟨ha, hb, hs, _⟩ := (mem_pairChoices false s p.1 p.2).mp hp
      obtain ⟨hlen, hbd, hq⟩ := (ih inner).mp hi
      refine ⟨?_, (digitsBounded_wrapDigits _ _ _).mpr ⟨ha, hbd, hb⟩, ?_⟩
      · rw [coefficientWord_cons, length_wrapDigits, length_wrapDigits, hlen]
      · rw [digitPairSums_wrapDigits, coefficientWord_cons, hq, hs]
    · rintro ⟨hlen, hbd, hq⟩
      have htwo : 2 ≤ ds.length := by
        rw [coefficientWord_cons, length_wrapDigits] at hlen
        omega
      obtain ⟨a, b, inner, rfl⟩ := exists_wrapDigits ds htwo
      obtain ⟨ha, hiBound, hb⟩ := (digitsBounded_wrapDigits _ _ _).mp hbd
      rw [digitPairSums_wrapDigits, coefficientWord_cons] at hq
      obtain ⟨hs, _, hiSum⟩ := wrapDigits_injective _ _ _ _ _ _ hq
      have hiLen : inner.length = (coefficientWord h c).length := by
        rw [coefficientWord_cons, length_wrapDigits, length_wrapDigits] at hlen
        omega
      apply List.mem_flatMap.mpr
      refine ⟨(a, b), (mem_pairChoices false s a b).mpr ⟨ha, hb, hs, by simp⟩, ?_⟩
      exact List.mem_map.mpr ⟨inner, (ih inner).mpr ⟨hiLen, hiBound, hiSum⟩, rfl⟩

theorem mem_canonicalWords_iff_rawWords (h : List Nat) (c : Option Nat)
    (ds : List Nat) : ds ∈ canonicalWords h c ↔
      ds ∈ rawWords h c ∧ 0 < ds.getLastD 0 := by
  cases h with
  | nil =>
    cases c with
    | none =>
      simp only [canonicalWords, List.not_mem_nil, rawWords, mem_centerWords_none]
      constructor
      · intro h; exact False.elim h
      · rintro ⟨rfl, hp⟩
        exact (Nat.lt_irrefl 0) hp
    | some s =>
      by_cases hs : 0 < s
      · simp only [canonicalWords, rawWords, if_pos hs]
        constructor
        · intro hm
          refine ⟨hm, ?_⟩
          obtain ⟨_, heven, rfl⟩ := (mem_centerWords_some s ds).mp hm
          simp only [List.getLastD_cons, List.getLastD_nil]
          omega
        · exact And.left
      · simp only [canonicalWords, rawWords, if_neg hs, List.not_mem_nil]
        constructor
        · intro h; exact False.elim h
        · rintro ⟨hm, hp⟩
          obtain ⟨_, _, rfl⟩ := (mem_centerWords_some s ds).mp hm
          simp only [List.getLastD_cons, List.getLastD_nil] at hp
          omega
  | cons s h =>
    simp only [canonicalWords, rawWords]
    constructor
    · intro hm
      obtain ⟨p, hp, hm⟩ := List.mem_flatMap.mp hm
      obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hm
      obtain ⟨ha, hb, hs, hlead⟩ := (mem_pairChoices true s p.1 p.2).mp hp
      refine ⟨?_, ?_⟩
      · exact List.mem_flatMap.mpr ⟨p,
          (mem_pairChoices false s p.1 p.2).mpr ⟨ha, hb, hs, by simp⟩,
          List.mem_map.mpr ⟨inner, hi, rfl⟩⟩
      · rw [getLastD_wrapDigits]
        exact hlead rfl
    · rintro ⟨hm, hlead⟩
      obtain ⟨p, hp, hm⟩ := List.mem_flatMap.mp hm
      obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hm
      obtain ⟨ha, hb, hs, _⟩ := (mem_pairChoices false s p.1 p.2).mp hp
      rw [getLastD_wrapDigits] at hlead
      exact List.mem_flatMap.mpr ⟨p,
        (mem_pairChoices true s p.1 p.2).mpr ⟨ha, hb, hs, by intro _; exact hlead⟩,
        List.mem_map.mpr ⟨inner, hi, rfl⟩⟩

/-- Complete arithmetic digit-list semantics, not merely a recursive spec. -/
theorem mem_canonicalWords (h : List Nat) (c : Option Nat) (ds : List Nat) :
    ds ∈ canonicalWords h c ↔ canonicalDigits ds ∧
      digitPairSums ds = coefficientWord h c := by
  rw [mem_canonicalWords_iff_rawWords, mem_rawWords]
  constructor
  · rintro ⟨⟨_, hb, hq⟩, hlead⟩
    exact ⟨⟨hb, hlead⟩, hq⟩
  · rintro ⟨⟨hb, hlead⟩, hq⟩
    have hlen := congrArg List.length hq
    rw [length_digitPairSums] at hlen
    exact ⟨⟨hlen, hb, hq⟩, hlead⟩

theorem canonicalWords_length (h : List Nat) (c : Option Nat) (ds : List Nat)
    (hm : ds ∈ canonicalWords h c) : ds.length = (coefficientWord h c).length := by
  have hq := ((mem_canonicalWords h c ds).mp hm).2
  have hlen := congrArg List.length hq
  simpa only [length_digitPairSums] using hlen

theorem nodup_wrappedProduct (ps : List (Nat × Nat)) (ws : List (List Nat))
    (hp : ps.Nodup) (hw : ws.Nodup) :
    (ps.flatMap fun p => ws.map (wrapDigits p.1 p.2)).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro p _
    exact List.Pairwise.map _ (fun ds ds' hne heq =>
      hne (wrapDigits_injective _ _ _ _ _ _ heq).2.2) hw
  · apply List.Pairwise.imp (R := fun p q : Nat × Nat => p ≠ q) ?_ hp
    intro p q hne x hx y hy hxy
    obtain ⟨ds, _, rfl⟩ := List.mem_map.mp hx
    obtain ⟨ds', _, rfl⟩ := List.mem_map.mp hy
    have hh := wrapDigits_injective _ _ _ _ _ _ hxy
    exact hne (Prod.ext hh.1 hh.2.1)

theorem rawWords_nodup (h : List Nat) (c : Option Nat) : (rawWords h c).Nodup := by
  induction h with
  | nil => exact centerWords_nodup c
  | cons s h ih =>
    exact nodup_wrappedProduct _ _ (pairChoices_nodup false s) ih

theorem canonicalWords_nodup (h : List Nat) (c : Option Nat) :
    (canonicalWords h c).Nodup := by
  cases h with
  | nil =>
    cases c with
    | none => simp [canonicalWords]
    | some s =>
      simp only [canonicalWords]
      split
      · exact centerWords_nodup (some s)
      · simp
  | cons s h =>
    exact nodup_wrappedProduct _ _ (pairChoices_nodup true s) (rawWords_nodup h c)

theorem length_wrappedProduct (ps : List (Nat × Nat)) (ws : List (List Nat)) :
    (ps.flatMap fun p => ws.map (wrapDigits p.1 p.2)).length = ps.length * ws.length := by
  induction ps with
  | nil => simp
  | cons p ps ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map, ih, List.length_cons]
    simp [Nat.add_mul, Nat.one_mul, Nat.add_comm]

theorem length_rawWords (h : List Nat) (c : Option Nat) :
    (rawWords h c).length = centerCount c * natProduct (h.map (pairCount false)) := by
  induction h with
  | nil => simp [rawWords, length_centerWords, natProduct]
  | cons s h ih =>
    rw [rawWords, length_wrappedProduct, length_pairChoices, ih]
    simp only [List.map_cons, natProduct, Nat.mul_assoc, Nat.mul_left_comm]

theorem length_canonicalWords_cons (s : Nat) (h : List Nat) (c : Option Nat) :
    (canonicalWords (s :: h) c).length =
      pairCount true s * centerCount c * natProduct (h.map (pairCount false)) := by
  rw [canonicalWords, length_wrappedProduct, length_pairChoices, length_rawWords]
  simp only [Nat.mul_assoc]

theorem length_canonicalWords_nil (c : Option Nat) :
    (canonicalWords [] c).length = match c with
      | none => 0
      | some s => if 0 < s then centerCount (some s) else 0 := by
  cases c with
  | none => rfl
  | some s =>
    simp only [canonicalWords]
    split
    · exact length_centerWords (some s)
    · rfl

/-- The exact count includes all original digit splits and no duplicates. -/
theorem length_canonicalWords (h : List Nat) (c : Option Nat) :
    (canonicalWords h c).length = profileCount h c := by
  cases h with
  | nil => cases c <;> exact length_canonicalWords_nil _
  | cons s h => exact length_canonicalWords_cons s h c

end Agent101
