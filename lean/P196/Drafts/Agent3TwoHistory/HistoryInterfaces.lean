import P196.Drafts.Agent3TwoHistory.ActualWords
import P196.Agent101ProtectedFamily.FiniteHorizonOverflow

/-!
Compatibility between Agent #9's existing complete inverse-path semantics
and Agent #8's original coefficient-word operations used by the protected
family. The local arithmetic and full mirrored-word path theorem are reused.
-/

namespace P196.Agent3.TwoHistory

open P196.Agent9.InverseFibers

/-- The retained carry in Agent #9's scan is the original terminal carry. -/
theorem scan_terminalCarry (w : List Nat) (e : Nat) :
    (scan w e).2 = Agent8.terminalCarry w e := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih =>
    exact ih ((x + e) / 10)

/-- An existing accepting folded inverse path is an actual full-word
transition with zero final carry, including the even-center closure. -/
theorem path_actual_transition (ss : List Symbol) (xs : List Nat)
    (hp : Path ss 0 xs) :
    Agent8.terminalCarry (mirror xs) 0 = 0 ∧
      Agent8.stepWord (mirror xs) = mirror (ss.map Fin.val) := by
  have ha := realizes_actual ss xs (path_realizes ss 0 xs hp)
  exact ⟨by rw [← scan_terminalCarry]; exact ha.2.2.1, ha.2.2.2⟩

/-- Even mirrored words with bounded coefficients and positive outer
coefficient are canonical coefficient words in the existing interface. -/
theorem mirror_canonical (xs : List Nat)
    (hb : ∀ x ∈ xs, x < 19) (hp : 0 < xs.headD 0) :
    Agent8.CanonicalPair (mirror xs) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro hn
    have hz := congrArg List.length hn
    simp only [mirror, List.length_append, List.length_reverse, List.length_nil] at hz
    have hx : xs = [] := List.length_eq_zero_iff.mp (by omega)
    simp [hx] at hp
  · simp [mirror, List.reverse_append]
  · intro x hx
    have hm : x ∈ xs := by simpa [mirror] using hx
    have h := hb x hm
    omega
  · cases xs with
    | nil => simp at hp
    | cons x xs => simpa [mirror] using hp

end P196.Agent3.TwoHistory
