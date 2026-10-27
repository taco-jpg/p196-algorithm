import P196.Agent119NeutralLengthAccounting.Main

/-!
# Finite-state extraction for the unchanged neutral-band checker

A checked cycle contains a checked cycle with distinct source interfaces.
Only original edges are retained, so arbitrary edge predicates survive.
Membership in any finite list of interfaces bounds the extracted length.
The initial interface and the ordered driver streams may change.
-/

namespace Agent104.NeutralJointWidth

open Agent120.Neutral
open Agent119.NeutralLengthAccounting

/-- The joint interface at which an edge starts. -/
def sourcePair (E : Edge) : List Nat × List Nat := (E.B, E.C)

private theorem chainOK_append_iff (b : Nat) (xs ys : List Edge) (B C : List Nat) :
    chainOK b (xs ++ ys) B C = true ↔
      chainOK b xs B C = true ∧
      chainOK b ys (endB xs B) (endC xs C) = true := by
  induction xs generalizing B C with
  | nil => simp [chainOK, endB, endC]
  | cons E xs ih =>
      simp only [List.cons_append, chainOK, Bool.and_eq_true, decide_eq_true_eq,
        endB, endC, ih, and_assoc]

/-- A repeated source inside a checked chain supplies a shorter checked cycle. -/
private theorem chain_nodup_or_shorter_cycle (b : Nat) (es : List Edge)
    (B C : List Nat) (hc : chainOK b es B C = true) :
    (es.map sourcePair).Nodup ∨
      ∃ ds D F, cycleOK b ds D F = true ∧ ds.length < es.length ∧
        ∀ E ∈ ds, E ∈ es := by
  induction es generalizing B C with
  | nil => exact Or.inl List.nodup_nil
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, ht⟩ := hc
      subst B
      subst C
      by_cases hdup : sourcePair E ∈ es.map sourcePair
      · obtain ⟨E', hm, hp⟩ := List.mem_map.mp hdup
        obtain ⟨xs, ys, hes⟩ := List.mem_iff_append.mp hm
        subst es
        have hwhole : chainOK b ((E :: xs) ++ E' :: ys) E.B E.C = true := by
          simpa only [List.cons_append, chainOK, Bool.and_eq_true,
            decide_eq_true_eq, true_and] using And.intro he ht
        obtain ⟨hpre, htail⟩ :=
          (chainOK_append_iff b (E :: xs) (E' :: ys) E.B E.C).mp hwhole
        simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at htail
        have hEB : E'.B = E.B := congrArg Prod.fst hp
        have hEC : E'.C = E.C := congrArg Prod.snd hp
        have hcloseB : endB (E :: xs) E.B = E.B := htail.1.1.1.symm.trans hEB
        have hcloseC : endC (E :: xs) E.C = E.C := htail.1.1.2.symm.trans hEC
        refine Or.inr ⟨E :: xs, E.B, E.C,
          (cycleOK_iff_closed_chain b (E :: xs) E.B E.C).mpr
            ⟨List.cons_ne_nil _ _, hpre, hcloseB, hcloseC⟩, ?_, ?_⟩
        · simp only [List.length_cons, List.length_append]
          omega
        · intro A hA
          rcases List.mem_cons.mp hA with hA | hA
          · exact List.mem_cons.mpr (Or.inl hA)
          · exact List.mem_cons_of_mem E (List.mem_append_left _ hA)
      · rcases ih E.B2 E.C2 ht with hn | ⟨ds, D, F, hd, hl, hs⟩
        · exact Or.inl (List.nodup_cons.mpr ⟨hdup, hn⟩)
        · refine Or.inr ⟨ds, D, F, hd, ?_, ?_⟩
          · simp only [List.length_cons]
            omega
          · exact fun A hA => List.mem_cons_of_mem E (hs A hA)

/-- No finiteness assumption is needed to remove repeated source interfaces. -/
theorem cycleOK_exists_simple {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) :
    ∃ ds D F, cycleOK b ds D F = true ∧
      (∀ E ∈ ds, E ∈ es) ∧ (ds.map sourcePair).Nodup := by
  have aux : ∀ n (xs : List Edge) (D F : List Nat), xs.length = n →
      cycleOK b xs D F = true →
      ∃ ds D' F', cycleOK b ds D' F' = true ∧
        (∀ E ∈ ds, E ∈ xs) ∧ (ds.map sourcePair).Nodup := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
        intro xs D F hlen hx
        have hchain := ((cycleOK_iff_closed_chain b xs D F).mp hx).2.1
        rcases chain_nodup_or_shorter_cycle b xs D F hchain with hn |
            ⟨ys, D', F', hy, hl, hs⟩
        · exact ⟨xs, D, F, hx, fun _ h => h, hn⟩
        · obtain ⟨ds, D'', F'', hd, hsub, hn⟩ :=
            ih ys.length (by omega) ys D' F' rfl hy
          exact ⟨ds, D'', F'', hd, fun E hE => hs E (hsub E hE), hn⟩
  exact aux es.length es B C rfl hc

private theorem nodup_length_le_of_mem {α : Type} {xs ys : List α}
    (hn : xs.Nodup) (hs : ∀ x ∈ xs, x ∈ ys) : xs.length ≤ ys.length := by
  induction xs generalizing ys with
  | nil => simp
  | cons x xs ih =>
      obtain ⟨hx, ht⟩ := List.nodup_cons.mp hn
      obtain ⟨pre, post, hys⟩ := List.mem_iff_append.mp (hs x List.mem_cons_self)
      subst ys
      have htail : ∀ y ∈ xs, y ∈ pre ++ post := by
        intro y hy
        have hym := hs y (List.mem_cons_of_mem x hy)
        rcases List.mem_append.mp hym with hm | hm
        · exact List.mem_append_left _ hm
        · rcases List.mem_cons.mp hm with heq | hm
          · subst y
            exact False.elim (hx hy)
          · exact List.mem_append_right _ hm
      have hh := ih ht htail
      simp only [List.length_cons, List.length_append] at hh ⊢
      omega

/-- An arbitrary finite source carrier bounds some accepted cycle. -/
theorem cycleOK_exists_bounded {b : Nat} {es : List Edge} {B C : List Nat}
    (P : Edge → Prop) (states : List (List Nat × List Nat))
    (hc : cycleOK b es B C = true) (hp : ∀ E ∈ es, P E)
    (hs : ∀ E ∈ es, (E.B, E.C) ∈ states) :
    ∃ ds D F, cycleOK b ds D F = true ∧
      (∀ E ∈ ds, P E) ∧ (∀ E ∈ ds, (E.B, E.C) ∈ states) ∧
      0 < ds.length ∧ ds.length ≤ states.length := by
  obtain ⟨ds, D, F, hd, hsub, hn⟩ := cycleOK_exists_simple hc
  have hstates : ∀ E ∈ ds, (E.B, E.C) ∈ states :=
    fun E hE => hs E (hsub E hE)
  have hmap : ∀ s ∈ ds.map sourcePair, s ∈ states := by
    intro s hsm
    obtain ⟨E, hE, heq⟩ := List.mem_map.mp hsm
    subst s
    exact hstates E hE
  have hlength := nodup_length_le_of_mem hn hmap
  have hne := ((cycleOK_iff_closed_chain b ds D F).mp hd).1
  refine ⟨ds, D, F, hd, fun E hE => hp E (hsub E hE), hstates, ?_, ?_⟩
  · exact List.length_pos_iff.mpr hne
  · simpa only [List.length_map] using hlength

end Agent104.NeutralJointWidth

#print axioms Agent104.NeutralJointWidth.cycleOK_exists_simple
#print axioms Agent104.NeutralJointWidth.cycleOK_exists_bounded
