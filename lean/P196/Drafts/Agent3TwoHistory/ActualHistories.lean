import P196.Drafts.Agent3TwoHistory.TwoLayerCertificate
import P196.Drafts.Agent3TwoHistory.HistoryInterfaces

/-!
Two actual nonoverflow incoming histories for each freely chosen protected
overflow word. The finite certificate supplies local carries; Agent #9's
original accepting-path theorem supplies the whole-word semantics.
-/

namespace P196.Agent3.TwoHistory

open P196.Agent9.InverseFibers
open P196.Agent3.OverflowHorizon

theorem runStates_append (j : Joint) (as bs : List Bool) :
    runStates j (as ++ bs) = runStates (runStates j as) bs := by
  induction as generalizing j with
  | nil => rfl
  | cons a as ih => exact ih (jointStep a j)

theorem firstLabels_length (j : Joint) (bs : List Bool) :
    (firstLabels j bs).length = bs.length := by
  induction bs generalizing j with
  | nil => rfl
  | cons b bs ih => simp only [firstLabels, List.length_cons, ih]

theorem secondLabels_length (j : Joint) (bs : List Bool) :
    (secondLabels j bs).length = bs.length := by
  induction bs generalizing j with
  | nil => rfl
  | cons b bs ih => simp only [secondLabels, List.length_cons, ih]

theorem path_eighteens (k : Nat) :
    Path (List.replicate k (18 : Symbol)) 3 (List.replicate k 18) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      exact ⟨3, local_eighteen, ih⟩

theorem path_first_prefix (bs : List Bool) (j : Joint)
    (ss : List Symbol) (xs : List Nat)
    (ht : Path ss (runStates j bs).1 xs) :
    Path (bs.map symbol ++ ss) j.1
      ((firstLabels j bs).map Fin.val ++ xs) := by
  induction bs generalizing j with
  | nil => exact ht
  | cons b bs ih =>
      exact ⟨(jointStep b j).1, local_emit1 b j, ih (jointStep b j) ht⟩

theorem path_second_prefix (bs : List Bool) (j : Joint)
    (ss : List Symbol) (xs : List Nat)
    (ht : Path ss (runStates j bs).2 xs) :
    Path (firstLabels j bs ++ ss) j.2
      ((secondLabels j bs).map Fin.val ++ xs) := by
  induction bs generalizing j with
  | nil => exact ht
  | cons b bs ih =>
      exact ⟨(jointStep b j).2, local_emit0 b j, ih (jointStep b j) ht⟩

def completedBits (xs : List Bool) : List Bool :=
  xs ++ correction (runStates (0, 1) xs)

def historyBits (xs : List Bool) : List Bool := true :: completedBits xs

def historyTarget (xs : List Bool) (k : Nat) : List Symbol :=
  (historyBits xs).map symbol ++ List.replicate k 18

def historyHalf1 (xs : List Bool) (k : Nat) : List Nat :=
  (firstLabels (0, 0) (historyBits xs)).map Fin.val ++ List.replicate k 18

def historyHalf0 (xs : List Bool) (k : Nat) : List Nat :=
  (secondLabels (0, 0) (historyBits xs)).map Fin.val ++ List.replicate k 18

def historyWord0 (xs : List Bool) (k : Nat) : Agent8.Word :=
  mirror (historyHalf0 xs k)

def historyWord1 (xs : List Bool) (k : Nat) : Agent8.Word :=
  mirror (historyHalf1 xs k)

def historyWord2 (xs : List Bool) (k : Nat) : Agent8.Word :=
  inputWord (completedBits xs) k

theorem completedBits_length (xs : List Bool) :
    (completedBits xs).length = xs.length + 6 := by
  simp only [completedBits, List.length_append, correction_length]

theorem historyBits_length (xs : List Bool) :
    (historyBits xs).length = xs.length + 7 := by
  simp only [historyBits, List.length_cons, completedBits_length]

theorem historyBits_closes (xs : List Bool) :
    runStates (0, 0) (historyBits xs) = (3, 3) := by
  rw [historyBits, runStates, initial_step, completedBits, runStates_append,
    correction_closes]

theorem symbol_val (b : Bool) : (symbol b).val = choice b := by
  cases b <;> rfl

theorem historyTarget_values (xs : List Bool) (k : Nat) :
    (historyTarget xs k).map Fin.val = inputHalf (completedBits xs) k := by
  have heq : Fin.val ∘ symbol = choice := funext symbol_val
  simp only [historyTarget, historyBits, List.map_append, List.map_cons,
    List.map_map, heq, List.map_replicate]
  rfl

theorem history_path1 (xs : List Bool) (k : Nat) :
    Path (historyTarget xs k) 0 (historyHalf1 xs k) := by
  have h : Path (List.replicate k (18 : Symbol))
      (runStates (0, 0) (historyBits xs)).1 (List.replicate k 18) := by
    simpa only [historyBits_closes] using path_eighteens k
  exact path_first_prefix (historyBits xs) (0, 0) _ _ h

theorem history_path0 (xs : List Bool) (k : Nat) :
    Path (firstLabels (0, 0) (historyBits xs) ++ List.replicate k 18) 0
      (historyHalf0 xs k) := by
  have h : Path (List.replicate k (18 : Symbol))
      (runStates (0, 0) (historyBits xs)).2 (List.replicate k 18) := by
    simpa only [historyBits_closes] using path_eighteens k
  exact path_second_prefix (historyBits xs) (0, 0) _ _ h

theorem historyWord0_final_carry (xs : List Bool) (k : Nat) :
    Agent8.terminalCarry (historyWord0 xs k) 0 = 0 :=
  (path_actual_transition _ _ (history_path0 xs k)).1

theorem historyWord1_final_carry (xs : List Bool) (k : Nat) :
    Agent8.terminalCarry (historyWord1 xs k) 0 = 0 :=
  (path_actual_transition _ _ (history_path1 xs k)).1

theorem historyWord0_step (xs : List Bool) (k : Nat) :
    Agent8.stepWord (historyWord0 xs k) = historyWord1 xs k := by
  have h := (path_actual_transition _ _ (history_path0 xs k)).2
  have h18 : (18 : Symbol).val = 18 := rfl
  simpa only [historyWord0, historyWord1, historyHalf1, List.map_append,
    List.map_replicate, h18] using h

theorem historyWord1_step (xs : List Bool) (k : Nat) :
    Agent8.stepWord (historyWord1 xs k) = historyWord2 xs k := by
  have h := (path_actual_transition _ _ (history_path1 xs k)).2
  simpa only [historyWord1, historyWord2, historyTarget_values, inputWord,
    mirror] using h

theorem historyWord2_final_carry (xs : List Bool) (k : Nat) :
    Agent8.terminalCarry (historyWord2 xs k) 0 = 1 :=
  inputWord_final_carry (completedBits xs) k

theorem historyWord2_step (xs : List Bool) (k : Nat) (hk : 0 < k) :
    Agent8.stepWord (historyWord2 xs k) = target (xs.length + 6) k := by
  simpa only [historyWord2, completedBits_length] using
    inputWord_step (completedBits xs) k hk

theorem symbol_values_bounded (ss : List Symbol) (k : Nat) :
    ∀ x ∈ ss.map Fin.val ++ List.replicate k 18, x < 19 := by
  intro x hx
  rcases List.mem_append.mp hx with hm | hr
  · obtain ⟨s, _, rfl⟩ := List.mem_map.mp hm
    exact s.isLt
  · have h := List.mem_replicate.mp hr
    omega

theorem historyHalf0_head (xs : List Bool) (k : Nat) :
    (historyHalf0 xs k).headD 0 = 3 := by
  simp only [historyHalf0, historyBits, secondLabels, List.map_cons,
    List.cons_append, List.headD_cons, initial_emit0]
  rfl

theorem historyHalf1_head (xs : List Bool) (k : Nat) :
    (historyHalf1 xs k).headD 0 = 7 := by
  simp only [historyHalf1, historyBits, firstLabels, List.map_cons,
    List.cons_append, List.headD_cons, initial_emit1]
  rfl

theorem historyWord0_head (xs : List Bool) (k : Nat) :
    (historyWord0 xs k).headD 0 = 3 := by
  simp only [historyWord0, mirror, historyHalf0, historyBits, secondLabels,
    List.map_cons, List.cons_append, List.headD_cons, initial_emit0]
  rfl

theorem historyWord1_head (xs : List Bool) (k : Nat) :
    (historyWord1 xs k).headD 0 = 7 := by
  simp only [historyWord1, mirror, historyHalf1, historyBits, firstLabels,
    List.map_cons, List.cons_append, List.headD_cons, initial_emit1]
  rfl

theorem historyWord0_canonical (xs : List Bool) (k : Nat) :
    Agent8.CanonicalPair (historyWord0 xs k) := by
  apply mirror_canonical
  · exact symbol_values_bounded _ k
  · rw [historyHalf0_head]
    decide

theorem historyWord1_canonical (xs : List Bool) (k : Nat) :
    Agent8.CanonicalPair (historyWord1 xs k) := by
  apply mirror_canonical
  · exact symbol_values_bounded _ k
  · rw [historyHalf1_head]
    decide

theorem historyWord2_canonical (xs : List Bool) (k : Nat) :
    Agent8.CanonicalPair (historyWord2 xs k) := inputWord_canonical _ _

theorem historyWord0_length (xs : List Bool) (k : Nat) :
    (historyWord0 xs k).length = 2 * (xs.length + k + 7) := by
  simp only [historyWord0, mirror, List.length_append, List.length_reverse,
    historyHalf0, List.length_map, secondLabels_length, List.length_replicate,
    historyBits_length]
  omega

theorem historyWord1_length (xs : List Bool) (k : Nat) :
    (historyWord1 xs k).length = 2 * (xs.length + k + 7) := by
  simp only [historyWord1, mirror, List.length_append, List.length_reverse,
    historyHalf1, List.length_map, firstLabels_length, List.length_replicate,
    historyBits_length]
  omega

theorem historyWord2_length (xs : List Bool) (k : Nat) :
    (historyWord2 xs k).length = 2 * (xs.length + k + 7) := by
  rw [historyWord2, inputWord_length, completedBits_length]
  omega

theorem historyWord0_even (xs : List Bool) (k : Nat) :
    (historyWord0 xs k).length % 2 = 0 := by
  rw [historyWord0_length]
  omega

theorem historyWord1_even (xs : List Bool) (k : Nat) :
    (historyWord1 xs k).length % 2 = 0 := by
  rw [historyWord1_length]
  omega

theorem historyWord2_even (xs : List Bool) (k : Nat) :
    (historyWord2 xs k).length % 2 = 0 := by
  rw [historyWord2_length]
  omega

theorem historyWord1_has_eighteen (xs : List Bool) (k : Nat) (hk : 0 < k) :
    18 ∈ historyWord1 xs k := by
  simp [historyWord1, mirror, historyHalf1, List.mem_replicate, Nat.ne_of_gt hk]

end P196.Agent3.TwoHistory
