import Agent101DigitPairs

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
    simp only [wrapDigits, List.mem_cons, List.mem_append, List.mem_singleton] at hd
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

end Agent101
