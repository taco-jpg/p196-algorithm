import Agent9HorizonCounts
import Agent9HorizonSafety
import Compat

/-!
Agent #9: supplementary finite-integer interpretation of the complete
no-overflow coefficient-word fiber. This module reuses the published exact
Agent109.Compat.pairWord_step theorem; it does not prove a new normalizer.
The private lemmas only identify canonical functions with finite digit lists.

Pinned original compatibility modules:
TemplateStep: Git blob 75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d.
Compat: Git blob 0279661cd41c62e8b1e8f7fe53d005a80f79dd71.
Both are read unchanged from repository snapshot
4b4edf976b2c7a9ba1dad80636c0e21c66350325.
-/

namespace P196.Agent9.NoOverflowHorizon

open InverseFibers Lychrel196 DecimalDigits FoldedDecimal

private theorem evalL_ofFn (d : Nat → Nat) (L : Nat) :
    Agent109.evalL (List.ofFn (fun i : Fin L => d i.val)) = value d L := by
  induction L generalizing d with
  | zero => rfl
  | succ L ih =>
    rw [List.ofFn_succ, Agent109.evalL]
    change d 0 + 10 * Agent109.evalL
      (List.ofFn (fun i : Fin L => d (i.val + 1))) = value d (L + 1)
    rw [ih (fun i => d (i + 1))]
    exact (value_shift d L).symm

private theorem canon_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    Agent109.Canon (List.ofFn (fun i : Fin L => d i.val)) := by
  apply (Agent109.canon_iff _).mpr
  constructor
  · intro x hx
    obtain ⟨i, hi⟩ := List.mem_ofFn.mp hx
    have hb := hc.2.1 i.val i.isLt
    omega
  · intro x hx
    have hne : List.ofFn (fun i : Fin L => d i.val) ≠ [] := by
      intro hn
      have hl := congrArg List.length hn
      simp only [List.length_ofFn, List.length_nil] at hl
      have := hc.1
      omega
    have he : (List.ofFn (fun i : Fin L => d i.val)).getLast? =
        some (d (L - 1)) := by
      rw [List.getLast?_eq_getLast hne, List.getLast_ofFn]
    rw [he] at hx
    have heq := Option.some.inj hx
    have hp := hc.2.2.1
    omega

private theorem digits_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    Agent109.digits n = List.ofFn (fun i : Fin L => d i.val) := by
  have h := Agent109.digits_evalL (List.ofFn (fun i : Fin L => d i.val))
    (canon_of_canonical n d L hc)
  simpa only [evalL_ofFn, hc.2.2.2] using h

private theorem pairWord_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    Agent109.pairWord n =
      List.ofFn (fun i : Fin L => columnSum d L i.val) := by
  rw [Agent109.pairWord, digits_of_canonical n d L hc,
    Agent109.pair, Agent109.zipAdd_eq_zipWith]
  apply List.ext_getElem
  · simp
  · intro i hi hi'
    simp only [List.getElem_zipWith, List.getElem_ofFn,
      List.getElem_reverse, List.length_ofFn]
    rfl

private theorem pairWord_eq_of_columns (n : Nat) (d : Nat → Nat) (q : List Nat)
    (hc : Canonical n d q.length)
    (hr : ∀ i, i < q.length → columnSum d q.length i = q.getD i 0) :
    Agent109.pairWord n = q := by
  rw [pairWord_of_canonical n d q.length hc]
  apply List.ext_getElem
  · simp
  · intro i hi hj
    simpa only [List.getElem_ofFn, List.getD_eq_getElem?_getD,
      List.getElem?_eq_getElem hj, Option.getD_some] using hr i hj

private theorem columns_of_pairWord_eq (n : Nat) (d : Nat → Nat)
    (L : Nat) (q : List Nat) (hc : Canonical n d L)
    (hp : Agent109.pairWord n = q) :
    L = q.length ∧ ∀ i, i < L → columnSum d L i = q.getD i 0 := by
  have he : List.ofFn (fun i : Fin L => columnSum d L i.val) = q :=
    (pairWord_of_canonical n d L hc).symm.trans hp
  constructor
  · have hl := congrArg List.length he
    simpa only [List.length_ofFn] using hl
  · intro i hi
    have hv := congrArg (fun w : List Nat => w.getD i 0) he
    simpa only [List.getD_eq_getElem?_getD, List.getElem?_ofFn, hi,
      dif_pos, Option.getD_some] using hv

/-- Every complete fiber element satisfies the original finite-word
realizability conditions, including even center parity and positive exterior. -/
theorem protected_input_admissible (m k : Nat) (q : List Nat)
    (hq : FullActualFiber m k q) :
    Admissible q.length (fun i => q.getD i 0) := by
  obtain ⟨hlen, hsym, hb, hp, _, _⟩ := hq
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · cases q with
    | nil => simp at hp
    | cons x xs => simpa using hp
  · intro i hi
    have hx := hb q[i] (List.getElem_mem hi)
    simpa only [List.getD_eq_getElem?_getD,
      List.getElem?_eq_getElem hi, Option.getD_some] using Nat.le_of_lt_succ hx
  · intro i hi
    have he := List.getElem?_reverse (l := q) hi
    rw [hsym] at he
    exact congrArg (fun x : Option Nat => x.getD 0) he
  · intro i hi he
    rw [hlen] at hi he
    omega

/-- Every enumerated coefficient word has a positive canonical finite
integer realization. Its equality to the established actual pair-word
function is proved, rather than assumed. -/
theorem protected_input_realizable (m k : Nat) (q : List Nat)
    (hq : FullActualFiber m k q) :
    ∃ n d, 0 < n ∧ Canonical n d q.length ∧
      (∀ i, i < q.length → columnSum d q.length i = q.getD i 0) ∧
      Agent109.pairWord n = q := by
  have ha := protected_input_admissible m k q hq
  obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable (fun i => q.getD i 0)
    q.length ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  exact ⟨n, d, hn, hc, hr, pairWord_eq_of_columns n d q hc hr⟩

/-- The published list/integer compatibility theorem transfers every
canonical realization of a fiber element to the protected target at its
actual next width. -/
theorem protected_input_step_realization (m k n : Nat) (q : List Nat)
    (d : Nat → Nat) (hq : FullActualFiber m k q)
    (hc : Canonical n d q.length)
    (hr : ∀ i, i < q.length → columnSum d q.length i = q.getD i 0) :
    ∃ e, Canonical (step n) e (targetWord m k).length ∧
      ∀ i, i < (targetWord m k).length →
        columnSum e (targetWord m k).length i = targetColumns m k i := by
  have hp := pairWord_eq_of_columns n d q hc hr
  have htarget : Agent109.pairWord (step n) = targetWord m k := by
    rw [Agent109.Compat.pairWord_step, hp]
    exact hq.2.2.2.2.2
  have hn : 0 < n := by
    have h := value_positive d q.length hc.1 hc.2.2.1
    simpa only [hc.2.2.2] using h
  have hnext : 0 < step n := by
    unfold step
    omega
  obtain ⟨e, L, he⟩ := canonical_exists (step n) hnext
  obtain ⟨hlen, hrep⟩ := columns_of_pairWord_eq (step n) e L
    (targetWord m k) he htarget
  refine ⟨e, ?_, ?_⟩
  · simpa only [hlen] using he
  · intro i hi
    simpa only [hlen, targetColumns] using hrep i (by omega)

/-- The predecessor is one numeric operation earlier than the target.
Hence target times zero through `k` are predecessor times one through `k+1`. -/
theorem protected_predecessor_safe (m k n : Nat) (q : List Nat)
    (d : Nat → Nat) (hq : FullActualFiber m k q)
    (hc : Canonical n d q.length)
    (hr : ∀ i, i < q.length → columnSum d q.length i = q.getD i 0)
    (j : Nat) (hj : 1 ≤ j) (hjk : j ≤ k + 1) :
    ¬ Palindrome (orbit n j) := by
  obtain ⟨e, he, hrep⟩ := protected_input_step_realization m k n q d hq hc hr
  have hs : ∀ t, t ≤ k → ¬ Palindrome (orbit (step n) t) := by
    intro t ht
    cases t with
    | zero => exact protected_target_not_palindrome m k (step n) e he hrep
    | succ t =>
        exact protected_target_safe m k (step n) e he hrep (t + 1) (by omega) ht
  have h := hs (j - 1) (by omega)
  simpa only [orbit_from_step, show j - 1 + 1 = j by omega] using h

/-- A positive actual predecessor integer exists for every complete fiber
element, and its next `k+1` positive orbit values are nonpalindromic. -/
theorem protected_predecessor_realizable (m k : Nat) (q : List Nat)
    (hq : FullActualFiber m k q) :
    ∃ n d, 0 < n ∧ Canonical n d q.length ∧
      (∀ i, i < q.length → columnSum d q.length i = q.getD i 0) ∧
      Agent109.pairWord n = q ∧
      Agent109.pairWord (step n) = targetWord m k ∧
      ∀ j, 1 ≤ j → j ≤ k + 1 → ¬ Palindrome (orbit n j) := by
  obtain ⟨n, d, hn, hc, hr, hp⟩ := protected_input_realizable m k q hq
  refine ⟨n, d, hn, hc, hr, hp, ?_, ?_⟩
  · rw [Agent109.Compat.pairWord_step, hp]
    exact hq.2.2.2.2.2
  · intro j hj hjk
    exact protected_predecessor_safe m k n q d hq hc hr j hj hjk

#print axioms evalL_ofFn
#print axioms canon_of_canonical
#print axioms digits_of_canonical
#print axioms pairWord_of_canonical
#print axioms pairWord_eq_of_columns
#print axioms columns_of_pairWord_eq
#print axioms protected_input_admissible
#print axioms protected_input_realizable
#print axioms protected_input_step_realization
#print axioms protected_predecessor_safe
#print axioms protected_predecessor_realizable

end P196.Agent9.NoOverflowHorizon
