import P196.Agent117P2641.Agent124FastPred
import P196.Agent117P2641.Agent124PrefixR

/-!
# Code-keyed rank certificates with a fused predecessor check (Agent #124)

A `CodeTree` stores only numeric keys and ranks.  The key of a word is
Agent #104's `wordCode` (base 19 with a leading marker 1); `decode` inverts it
on words with entries below 19 (`decode_wordCode`), so a stored key determines
its word.  The rank function of a tree is `R t w = lookupC t (wordCode w)`.

The row check `rowOK` decodes a key and walks the exact four-guess inverse of
`Agent124.FastPred.pred2` column by column, accumulating the code of each
candidate predecessor and looking it up as soon as the word is complete.  No
predecessor list is built.  Its soundness (`rowsClosed_of_all`) is proved
against the complete inverse, so the certificate data, ordering and ranks
remain untrusted.  Short descent and initial bounds are checked the same way.
-/

namespace Agent124.CodeCert

open SevenColumn SevenColumn.Certificate SevenColumn.ShortBoundary
open Agent124.FastPred Agent124.PrefixK Agent124.PrefixR

/-! ## Code-keyed trees -/

theorem blt_true {a b : Nat} : Nat.blt a b = true ↔ a < b := by simp [Nat.blt_eq]

theorem blt_false {a b : Nat} : Nat.blt a b = false ↔ ¬ a < b := by
  constructor
  · intro h h'
    have := blt_true.mpr h'
    rw [h] at this
    contradiction
  · intro h
    cases hh : Nat.blt a b
    · rfl
    · exact absurd (blt_true.mp hh) h

inductive CodeTree where
  | empty
  | node (key rank : Nat) (left right : CodeTree)
  deriving Inhabited

def lookupC : CodeTree → Nat → Option Nat
  | .empty, _ => none
  | .node k r l rt, c =>
      cond (Nat.blt c k) (lookupC l c) (cond (Nat.blt k c) (lookupC rt c) (some r))

def CodeTree.All (P : Nat → Nat → Prop) : CodeTree → Prop
  | .empty => True
  | .node k r l rt => l.All P ∧ P k r ∧ rt.All P

theorem lookupC_all {P : Nat → Nat → Prop} :
    ∀ {t : CodeTree}, t.All P → ∀ {c r : Nat}, lookupC t c = some r → P c r
  | .empty, _, _, _, hr => by simp [lookupC] at hr
  | .node k r0 l rt, h, c, r, hr => by
      simp only [CodeTree.All] at h
      simp only [lookupC] at hr
      cases hlt : Nat.blt c k
      · rw [hlt, cond_false] at hr
        cases hgt : Nat.blt k c
        · rw [hgt, cond_false] at hr
          cases hr
          have h1 : ¬ c < k := blt_false.mp hlt
          have h2 : ¬ k < c := blt_false.mp hgt
          have hck : c = k := by omega
          subst hck
          exact h.2.1
        · rw [hgt, cond_true] at hr
          exact lookupC_all h.2.2 hr
      · rw [hlt, cond_true] at hr
        exact lookupC_all h.1 hr

/-- Rank function of a code tree. -/
def R (t : CodeTree) (w : List Nat) : Option Nat := lookupC t (wordCode w)

/-! ## Decoding -/

def decodeF : Nat → Nat → List Nat → List Nat
  | 0, _, acc => acc
  | f + 1, c, acc => cond (Nat.blt c 19) acc (decodeF f (c / 19) (c % 19 :: acc))

def decode (c : Nat) : List Nat := decodeF 32 c []

def codeStep (a d : Nat) : Nat := 19 * a + d

theorem wordCode_eq (w : List Nat) : wordCode w = w.foldl codeStep 1 := rfl

theorem foldl_codeStep_pos (c : Nat) (hc : 1 ≤ c) :
    ∀ u : List Nat, 1 ≤ u.foldl codeStep c
  | [] => hc
  | d :: u => by
      simp only [List.foldl_cons]
      apply foldl_codeStep_pos
      unfold codeStep
      omega

theorem wordCode_concat (u : List Nat) (d : Nat) :
    wordCode (u ++ [d]) = 19 * wordCode u + d := by
  simp [wordCode_eq, List.foldl_append, codeStep]

theorem decodeF_wordCode : ∀ (n : Nat) (u : List Nat), u.length = n →
    (∀ x ∈ u, x < 19) → ∀ f, n ≤ f → ∀ acc, decodeF f (wordCode u) acc = u ++ acc
  | 0, u, hl, _, f, _, acc => by
      have : u = [] := List.eq_nil_of_length_eq_zero hl
      subst u
      cases f with
      | zero => rfl
      | succ f => rfl
  | n + 1, u, hl, hb, f, hf, acc => by
      rcases List.eq_nil_or_concat u with h | ⟨v, d, hu⟩
      · subst h
        simp at hl
      · rw [List.concat_eq_append] at hu
        subst hu
        have hvl : v.length = n := by simpa using hl
        have hd : d < 19 := hb d (by simp)
        have hvb : ∀ x ∈ v, x < 19 := fun x hx => hb x (by simp [hx])
        obtain ⟨f', rfl⟩ : ∃ f', f = f' + 1 := ⟨f - 1, by omega⟩
        have hpos : 1 ≤ wordCode v := foldl_codeStep_pos 1 (by decide) v
        have hge : ¬ (wordCode (v ++ [d]) < 19) := by
          rw [wordCode_concat]
          omega
        have hblt : Nat.blt (wordCode (v ++ [d])) 19 = false := blt_false.mpr hge
        have hdiv : wordCode (v ++ [d]) / 19 = wordCode v := by
          rw [wordCode_concat]
          omega
        have hmod : wordCode (v ++ [d]) % 19 = d := by
          rw [wordCode_concat]
          omega
        simp only [decodeF, hblt, cond_false, hdiv, hmod]
        rw [decodeF_wordCode n v hvl hvb f' (by omega) (d :: acc)]
        simp

theorem decode_wordCode (w : List Nat) (hb : ∀ x ∈ w, x < 19) (hl : w.length ≤ 32) :
    decode (wordCode w) = w := by
  unfold decode
  rw [decodeF_wordCode w.length w rfl hb 32 hl []]
  simp

/-! ## Fused row check -/

def belowC (t : CodeTree) (r code : Nat) : Bool :=
  match lookupC t code with
  | some s => Nat.blt s r
  | none => false

theorem belowC_sound {t : CodeTree} {r code : Nat} (h : belowC t r code = true) :
    ∃ s, lookupC t code = some s ∧ s < r := by
  unfold belowC at h
  split at h
  · rename_i s hs
    exact ⟨s, hs, blt_true.mp h⟩
  · contradiction

def chkNo (t : CodeTree) (r : Nat) : List Nat → Nat → Nat → Nat → Bool
  | [], _, _, code => belowC t r code
  | v :: p, x, y, code =>
      (!(noOK v x y (noCandidate v x y 0 0) 0 0) ||
        chkNo t r p 0 0 (codeStep code (noCandidate v x y 0 0))) &&
      (!(noOK v x y (noCandidate v x y 0 1) 0 1) ||
        chkNo t r p 0 1 (codeStep code (noCandidate v x y 0 1))) &&
      (!(noOK v x y (noCandidate v x y 1 0) 1 0) ||
        chkNo t r p 1 0 (codeStep code (noCandidate v x y 1 0))) &&
      (!(noOK v x y (noCandidate v x y 1 1) 1 1) ||
        chkNo t r p 1 1 (codeStep code (noCandidate v x y 1 1)))

/-- First column: also require a positive outer source sum. -/
def chkNoTop (t : CodeTree) (r : Nat) : List Nat → Bool
  | [] => true
  | v :: p =>
      (!(Nat.blt 0 (noCandidate v 0 0 0 0) && noOK v 0 0 (noCandidate v 0 0 0 0) 0 0) ||
        chkNo t r p 0 0 (codeStep 1 (noCandidate v 0 0 0 0))) &&
      (!(Nat.blt 0 (noCandidate v 0 0 0 1) && noOK v 0 0 (noCandidate v 0 0 0 1) 0 1) ||
        chkNo t r p 0 1 (codeStep 1 (noCandidate v 0 0 0 1))) &&
      (!(Nat.blt 0 (noCandidate v 0 0 1 0) && noOK v 0 0 (noCandidate v 0 0 1 0) 1 0) ||
        chkNo t r p 1 0 (codeStep 1 (noCandidate v 0 0 1 0))) &&
      (!(Nat.blt 0 (noCandidate v 0 0 1 1) && noOK v 0 0 (noCandidate v 0 0 1 1) 1 1) ||
        chkNo t r p 1 1 (codeStep 1 (noCandidate v 0 0 1 1)))

def chkOvTail (t : CodeTree) (r : Nat) : List Nat → Nat → Nat → Nat → Nat → Bool
  | [], a, _, y, code =>
      !(Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y) || belowC t r code
  | v :: p, prev, x, y, code =>
      (!(ovOK v prev x y (overflowCandidate v prev x y 0 0) 0 0) ||
        chkOvTail t r p (overflowCandidate v prev x y 0 0) 0 0
          (codeStep code (overflowCandidate v prev x y 0 0))) &&
      (!(ovOK v prev x y (overflowCandidate v prev x y 0 1) 0 1) ||
        chkOvTail t r p (overflowCandidate v prev x y 0 1) 0 1
          (codeStep code (overflowCandidate v prev x y 0 1))) &&
      (!(ovOK v prev x y (overflowCandidate v prev x y 1 0) 1 0) ||
        chkOvTail t r p (overflowCandidate v prev x y 1 0) 1 0
          (codeStep code (overflowCandidate v prev x y 1 0))) &&
      (!(ovOK v prev x y (overflowCandidate v prev x y 1 1) 1 1) ||
        chkOvTail t r p (overflowCandidate v prev x y 1 1) 1 1
          (codeStep code (overflowCandidate v prev x y 1 1)))

def chkOv (t : CodeTree) (r : Nat) : List Nat → Bool
  | [] => true
  | v :: p => !(Nat.blt 0 v && Nat.ble v 10) ||
      chkOvTail t r p (overflowFirst v) ((overflowFirst v + 0) / 10) 1
        (codeStep 1 (overflowFirst v))

def rowOK (t : CodeTree) (k c r : Nat) : Bool :=
  !(Nat.beq (decode c).length k) || (chkNoTop t r (decode c) && chkOv t r (decode c))

/-- Helper: one guarded branch of a four-way conjunction. -/
theorem branch_of {c rest : Bool} (h : (!c || rest) = true) (hc : c = true) :
    rest = true := by
  subst hc
  simpa using h

theorem mem_cond_map_inv {c : Bool} {l : List (List Nat)} {a : Nat} {s : List Nat}
    (h : s ∈ cond c (l.map (a :: ·)) []) : c = true ∧ ∃ s', s' ∈ l ∧ s = a :: s' := by
  cases c
  · simp at h
  · simp only [cond_true, List.mem_map] at h
    obtain ⟨s', hs', rfl⟩ := h
    exact ⟨rfl, s', hs', rfl⟩

theorem chkNo_sound {t : CodeTree} {r : Nat} :
    ∀ (p : List Nat) (x y code : Nat), chkNo t r p x y code = true →
      ∀ s ∈ noPred2 p x y, belowC t r (s.foldl codeStep code) = true
  | [], x, y, code, h, s, hs => by
      simp only [noPred2, List.mem_singleton] at hs
      subst hs
      simpa [chkNo] using h
  | v :: p, x, y, code, h, s, hs => by
      simp only [chkNo, Bool.and_eq_true] at h
      obtain ⟨⟨⟨h00, h01⟩, h10⟩, h11⟩ := h
      simp only [noPred2, List.mem_append] at hs
      rcases hs with ((hs | hs) | hs) | hs
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkNo_sound p 0 0 _ (branch_of h00 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkNo_sound p 0 1 _ (branch_of h01 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkNo_sound p 1 0 _ (branch_of h10 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkNo_sound p 1 1 _ (branch_of h11 hc) s' hs'

theorem chkNoTop_sound {t : CodeTree} {r : Nat} (p : List Nat)
    (h : chkNoTop t r p = true) :
    ∀ s ∈ (noPred2 p 0 0).filter headPos, belowC t r (wordCode s) = true := by
  intro s hs
  rw [List.mem_filter] at hs
  obtain ⟨hs, hpos⟩ := hs
  cases p with
  | nil =>
      simp only [noPred2, List.mem_singleton] at hs
      subst hs
      simp [headPos] at hpos
  | cons v p =>
      simp only [chkNoTop, Bool.and_eq_true] at h
      obtain ⟨⟨⟨h00, h01⟩, h10⟩, h11⟩ := h
      simp only [noPred2, List.mem_append] at hs
      rw [wordCode_eq]
      rcases hs with ((hs | hs) | hs) | hs
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        have hp : Nat.blt 0 (noCandidate v 0 0 0 0) = true := by simpa [headPos] using hpos
        exact chkNo_sound p 0 0 _ (branch_of h00 (by rw [hp, hc]; rfl)) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        have hp : Nat.blt 0 (noCandidate v 0 0 0 1) = true := by simpa [headPos] using hpos
        exact chkNo_sound p 0 1 _ (branch_of h01 (by rw [hp, hc]; rfl)) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        have hp : Nat.blt 0 (noCandidate v 0 0 1 0) = true := by simpa [headPos] using hpos
        exact chkNo_sound p 1 0 _ (branch_of h10 (by rw [hp, hc]; rfl)) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        have hp : Nat.blt 0 (noCandidate v 0 0 1 1) = true := by simpa [headPos] using hpos
        exact chkNo_sound p 1 1 _ (branch_of h11 (by rw [hp, hc]; rfl)) s' hs'

theorem chkOvTail_sound {t : CodeTree} {r : Nat} :
    ∀ (p : List Nat) (a x y code : Nat), chkOvTail t r p a x y code = true →
      ∀ s ∈ ovTailPred2 p a x y, belowC t r (s.foldl codeStep code) = true
  | [], a, x, y, code, h, s, hs => by
      simp only [ovTailPred2] at hs
      obtain ⟨hc, rfl⟩ : (Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y) = true ∧ s = [] := by
        cases hcc : (Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y)
        · rw [hcc] at hs
          simp at hs
        · rw [hcc] at hs
          simp only [cond_true, List.mem_singleton] at hs
          exact ⟨rfl, hs⟩
      simp only [chkOvTail] at h
      simpa using branch_of h hc
  | v :: p, prev, x, y, code, h, s, hs => by
      simp only [chkOvTail, Bool.and_eq_true] at h
      obtain ⟨⟨⟨h00, h01⟩, h10⟩, h11⟩ := h
      simp only [ovTailPred2, List.mem_append] at hs
      rcases hs with ((hs | hs) | hs) | hs
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkOvTail_sound p _ 0 0 _ (branch_of h00 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkOvTail_sound p _ 0 1 _ (branch_of h01 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkOvTail_sound p _ 1 0 _ (branch_of h10 hc) s' hs'
      · obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
        exact chkOvTail_sound p _ 1 1 _ (branch_of h11 hc) s' hs'

theorem chkOv_sound {t : CodeTree} {r : Nat} (p : List Nat) (h : chkOv t r p = true) :
    ∀ s ∈ ovPred2 p, belowC t r (wordCode s) = true := by
  intro s hs
  cases p with
  | nil => simp [ovPred2] at hs
  | cons v p =>
      simp only [ovPred2] at hs
      obtain ⟨hc, s', hs', rfl⟩ := mem_cond_map_inv hs
      simp only [chkOv] at h
      rw [wordCode_eq]
      exact chkOvTail_sound p _ _ 1 _ (branch_of h hc) s' hs'

theorem rowOK_sound {t : CodeTree} {k r : Nat} {w : List Nat}
    (hb : ∀ x ∈ w, x < 19) (hl : w.length ≤ 32)
    (h : rowOK t k (wordCode w) r = true) :
    ∀ q ∈ longPred2 k w, belowC t r (wordCode q) = true := by
  intro q hq
  unfold rowOK at h
  rw [decode_wordCode w hb hl] at h
  unfold longPred2 at hq
  cases hlen : Nat.beq w.length k
  · rw [hlen] at hq
    simp at hq
  · rw [hlen, cond_true] at hq
    have h2 := branch_of h hlen
    simp only [Bool.and_eq_true] at h2
    unfold pred2 at hq
    rcases List.mem_append.mp hq with hq | hq
    · exact chkNoTop_sound w h2.1 q hq
    · exact chkOv_sound w h2.2 q hq

/-- Boolean check of every node of a subtree. -/
def allRowsC (t : CodeTree) (k : Nat) : CodeTree → Bool
  | .empty => true
  | .node c r l rt => allRowsC t k l && rowOK t k c r && allRowsC t k rt

theorem allRowsC_sound {t : CodeTree} {k : Nat} :
    ∀ {sub : CodeTree}, allRowsC t k sub = true → sub.All (fun c r => rowOK t k c r = true)
  | .empty, _ => trivial
  | .node c r l rt, h => by
      simp only [allRowsC, Bool.and_eq_true] at h
      exact ⟨allRowsC_sound h.1.1, h.1.2, allRowsC_sound h.2⟩

/-- Checked rows of every stored key give semantic row closure of `R t`
for words of width at most 32 (all certificate widths used here are ≤ 8). -/
theorem rowsClosed_of_all {t : CodeTree} {k : Nat} (hk : k ≤ 32)
    (h : t.All (fun c r => rowOK t k c r = true)) : RowsClosed k (R t) := by
  intro w r hb hr q hq
  have hq2 := longPred_mem_longPred2 hq
  have hlen : w.length = k := by
    unfold longPred at hq
    split at hq
    · assumption
    · contradiction
  have hrow := lookupC_all h hr
  exact belowC_sound (rowOK_sound hb (by omega) hrow q hq2)

/-! ## Short descent and initial bounds -/

def shortOKC (t : CodeTree) (s : List Nat) : Bool :=
  match lookupC t (wordCode (nextWord s)) with
  | none => true
  | some r => belowC t r (wordCode s)

theorem shortClosed_of_widths {t : CodeTree} {k : Nat}
    (h : ∀ n, n < k → (symWords n).all (shortOKC t) = true) : ShortClosed k (R t) := by
  intro s hs r hr
  unfold shortWordsK at hs
  rw [List.mem_flatMap] at hs
  obtain ⟨n, hn, hs⟩ := hs
  have hc := List.all_eq_true.mp (h n (List.mem_range.mp hn)) s hs
  unfold shortOKC at hc
  unfold R at hr
  rw [hr] at hc
  exact belowC_sound hc

def initOKC (t : CodeTree) (bound : Nat) (w : List Nat) : Bool :=
  match lookupC t (wordCode w) with
  | some r => Nat.ble r bound
  | none => false

theorem initialBounded_of_all {t : CodeTree} {k a b c bound : Nat}
    (h : (initialWordsK k a b c).all (initOKC t bound) = true) :
    InitialBounded k a b c bound (R t) := by
  intro w hw
  have hc := List.all_eq_true.mp h w hw
  unfold initOKC at hc
  unfold R
  split at hc
  · rename_i r hr
    exact ⟨r, hr, by simpa [Nat.ble_eq] using hc⟩
  · contradiction

end Agent124.CodeCert

#print axioms Agent124.CodeCert.lookupC_all
#print axioms Agent124.CodeCert.decode_wordCode
#print axioms Agent124.CodeCert.chkNo_sound
#print axioms Agent124.CodeCert.rowOK_sound
#print axioms Agent124.CodeCert.rowsClosed_of_all
#print axioms Agent124.CodeCert.shortClosed_of_widths
#print axioms Agent124.CodeCert.initialBounded_of_all
