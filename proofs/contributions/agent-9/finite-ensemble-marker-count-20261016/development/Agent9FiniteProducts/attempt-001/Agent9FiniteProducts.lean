import Std

/-!
Finite list products for the exact marker-complement count in
`2026-10-14-finite-horizon-density/README.md`, equation (3).
These generic lemmas enumerate every allowed finite word once.
-/

namespace P196.Agent9.Ensemble

def wordChoices {α : Type} (alphabet : List α) : Nat → List (List α)
  | 0 => [[]]
  | n + 1 => alphabet.flatMap fun a => (wordChoices alphabet n).map (a :: ·)

theorem mem_wordChoices {α : Type} (alphabet : List α) (n : Nat) (xs : List α) :
    xs ∈ wordChoices alphabet n ↔ xs.length = n ∧ ∀ a ∈ xs, a ∈ alphabet := by
  induction n generalizing xs with
  | zero => simp [wordChoices]
  | succ n ih =>
    constructor
    · intro hx
      obtain ⟨a, ha, ys, hy, rfl⟩ := List.mem_flatMap.mp hx
        |>.imp (fun a h => ⟨h.1, List.mem_map.mp h.2⟩)
      obtain ⟨hlen, hm⟩ := (ih ys).mp hy
      exact ⟨by simp [hlen], by simpa using And.intro ha hm⟩
    · rintro ⟨hlen, hm⟩
      cases xs with
      | nil => simp at hlen
      | cons a xs =>
        apply List.mem_flatMap.mpr
        refine ⟨a, hm a (by simp), List.mem_map.mpr ⟨xs, ?_, rfl⟩⟩
        exact (ih xs).mpr ⟨by simpa using hlen, fun b hb => hm b (by simp [hb])⟩

theorem length_flatMap_map {α β γ : Type} (as : List α) (bs : List β)
    (f : α → β → γ) :
    (as.flatMap fun a => bs.map (f a)).length = as.length * bs.length := by
  induction as with
  | nil => simp
  | cons a as ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map, ih,
      List.length_cons]
    simp [Nat.add_mul, Nat.add_comm]

theorem nodup_flatMap_map {α β γ : Type} (as : List α) (bs : List β)
    (f : α → β → γ) (ha : as.Nodup) (hb : bs.Nodup)
    (hf : ∀ a ∈ as, ∀ a' ∈ as, ∀ b ∈ bs, ∀ b' ∈ bs,
      f a b = f a' b' → a = a' ∧ b = b') :
    (as.flatMap fun a => bs.map (f a)).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro a ham
    rw [List.pairwise_map]
    apply List.Pairwise.imp_of_mem (p := hb)
    intro b b' hbm hb'm hne heq
    exact hne (hf a ham a ham b hbm b' hb'm heq).2
  · apply List.Pairwise.imp_of_mem (p := ha)
    intro a a' ham ha'm hne x hx y hy hxy
    obtain ⟨b, hbm, rfl⟩ := List.mem_map.mp hx
    obtain ⟨b', hb'm, rfl⟩ := List.mem_map.mp hy
    exact hne (hf a ham a' ha'm b hbm b' hb'm hxy).1

theorem wordChoices_nodup {α : Type} (alphabet : List α)
    (ha : alphabet.Nodup) (n : Nat) : (wordChoices alphabet n).Nodup := by
  induction n with
  | zero => simp [wordChoices]
  | succ n ih =>
    exact nodup_flatMap_map _ _ _ ha ih
      (fun _ _ _ _ _ _ _ _ h => List.cons.inj h)

theorem length_wordChoices {α : Type} (alphabet : List α) (n : Nat) :
    (wordChoices alphabet n).length = alphabet.length ^ n := by
  induction n with
  | zero => simp [wordChoices]
  | succ n ih =>
    rw [wordChoices, length_flatMap_map, ih, Nat.pow_succ]
    exact Nat.mul_comm _ _

def appendProduct {α : Type} (as bs : List (List α)) : List (List α) :=
  as.flatMap fun a => bs.map (a ++ ·)

theorem mem_appendProduct {α : Type} (as bs : List (List α)) (xs : List α) :
    xs ∈ appendProduct as bs ↔ ∃ a ∈ as, ∃ b ∈ bs, a ++ b = xs := by
  simp [appendProduct, List.mem_flatMap, List.mem_map]

theorem length_appendProduct {α : Type} (as bs : List (List α)) :
    (appendProduct as bs).length = as.length * bs.length :=
  length_flatMap_map as bs (· ++ ·)

theorem appendProduct_nodup {α : Type} (as bs : List (List α)) (r : Nat)
    (ha : as.Nodup) (hb : bs.Nodup) (hlen : ∀ a ∈ as, a.length = r) :
    (appendProduct as bs).Nodup := by
  apply nodup_flatMap_map as bs (· ++ ·) ha hb
  intro a ham a' ha'm b _ b' _ heq
  have hl : a.length = a'.length := (hlen a ham).trans (hlen a' ha'm).symm
  exact ⟨List.append_inj_left heq hl, List.append_inj_right heq hl⟩

/-- Concatenate exactly `J` allowed blocks, followed by an allowed suffix. -/
def blockChoices {α : Type} (blocks suffixes : List (List α)) : Nat → List (List α)
  | 0 => suffixes
  | J + 1 => appendProduct blocks (blockChoices blocks suffixes J)

theorem length_blockChoices {α : Type} (blocks suffixes : List (List α)) (J : Nat) :
    (blockChoices blocks suffixes J).length = blocks.length ^ J * suffixes.length := by
  induction J with
  | zero => simp [blockChoices]
  | succ J ih =>
    rw [blockChoices, length_appendProduct, ih, Nat.pow_succ]
    simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

theorem blockChoices_nodup {α : Type} (blocks suffixes : List (List α)) (r J : Nat)
    (hb : blocks.Nodup) (hs : suffixes.Nodup)
    (hl : ∀ b ∈ blocks, b.length = r) :
    (blockChoices blocks suffixes J).Nodup := by
  induction J with
  | zero => exact hs
  | succ J ih => exact appendProduct_nodup _ _ r hb ih hl

theorem blockChoices_word_length {α : Type} (blocks suffixes : List (List α))
    (r q J : Nat) (hb : ∀ b ∈ blocks, b.length = r)
    (hs : ∀ s ∈ suffixes, s.length = q) (xs : List α)
    (hx : xs ∈ blockChoices blocks suffixes J) : xs.length = J * r + q := by
  induction J generalizing xs with
  | zero => simpa [blockChoices] using hs xs hx
  | succ J ih =>
    obtain ⟨b, hbm, s, hsm, rfl⟩ := (mem_appendProduct _ _ xs).mp hx
    rw [List.length_append, hb b hbm, ih s hsm, Nat.succ_mul]
    omega

/-- Complete positional semantics, including a zero number of selected blocks. -/
theorem mem_blockChoices {α : Type} (blocks suffixes : List (List α))
    (r q J : Nat) (hb : ∀ b ∈ blocks, b.length = r)
    (hs : ∀ s ∈ suffixes, s.length = q) (xs : List α) :
    xs ∈ blockChoices blocks suffixes J ↔
      xs.length = J * r + q ∧ xs.drop (J * r) ∈ suffixes ∧
      ∀ j, j < J → (xs.drop (j * r)).take r ∈ blocks := by
  induction J generalizing xs with
  | zero =>
    simp only [blockChoices, Nat.zero_mul, Nat.zero_add, List.drop_zero,
      Nat.not_lt_zero, false_implies, forall_const, and_true]
    exact ⟨fun h => ⟨hs xs h, h⟩, And.right⟩
  | succ J ih =>
    constructor
    · intro hx
      obtain ⟨b, hbm, s, hsm, rfl⟩ := (mem_appendProduct _ _ xs).mp hx
      have hbl := hb b hbm
      obtain ⟨hsl, hsd, hblocks⟩ := (ih s).mp hsm
      have hdrop (j : Nat) : (b ++ s).drop ((j + 1) * r) = s.drop (j * r) := by
        rw [Nat.succ_mul, Nat.add_comm, ← hbl, List.drop_append]
      refine ⟨?_, ?_, ?_⟩
      · rw [List.length_append, hbl, hsl, Nat.succ_mul]
        omega
      · simpa only [hdrop] using hsd
      · intro j hj
        cases j with
        | zero => simpa [← hbl] using hbm
        | succ j => simpa only [hdrop] using hblocks j (by omega)
    · rintro ⟨hlen, hsuf, hblocks⟩
      apply (mem_appendProduct _ _ xs).mpr
      refine ⟨xs.take r, ?_, xs.drop r, ?_, List.take_append_drop r xs⟩
      · simpa using hblocks 0 (by omega)
      · apply (ih (xs.drop r)).mpr
        have hdrop (j : Nat) : (xs.drop r).drop (j * r) = xs.drop ((j + 1) * r) := by
          rw [List.drop_drop, Nat.succ_mul, Nat.add_comm]
        refine ⟨?_, ?_, ?_⟩
        · rw [List.length_drop, hlen, Nat.succ_mul]
          omega
        · simpa only [hdrop] using hsuf
        · intro j hj
          simpa only [hdrop] using hblocks (j + 1) (by omega)

end P196.Agent9.Ensemble
