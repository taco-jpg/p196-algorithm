import OuterBounds

/-! Cap-three extension of the unchanged Agent 7 outer projection.
Finite computation below is checked by Lean's kernel. -/
namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Inclusive test at times 0 through n, parameterized by the cap. -/
def staysWithin (cap : Nat) : Nat → Outer → Bool
  | 0, s => decide (s.B.length ≤ cap)
  | n + 1, s => decide (s.B.length ≤ cap) && staysWithin cap n (outerNext s)

/-- Base-19 enumeration, separated by word length. -/
def decodeWord3 (k : Nat) : List Nat :=
  if k == 0 then []
  else if k ≤ 19 then [k - 1]
  else if k ≤ 380 then [(k - 20) / 19, (k - 20) % 19]
  else [(k - 381) / 361, ((k - 381) / 19) % 19, (k - 381) % 19]

def encodedAt (p : Fin 8) (k : Nat) : Outer :=
  { c := 2 * (p.val + 1), B := decodeWord3 k }

def encoded3 (p : Fin 8) (k : Fin 7240) : Outer := encodedAt p k.val

def ExitCheck (p : Fin 8) (k : Nat) : Prop :=
  validOuter (encodedAt p k) = true → staysWithin 3 9 (encodedAt p k) = false

def BatchCheck (start count : Nat) : Prop :=
  ∀ (p : Fin 8) (j : Fin count), ExitCheck p (start + j.val)

instance (p : Fin 8) (k : Nat) : Decidable (ExitCheck p k) := by
  unfold ExitCheck
  infer_instance

instance (start count : Nat) : Decidable (BatchCheck start count) := by
  unfold BatchCheck
  infer_instance

theorem of_batch {start count k : Nat} (h : BatchCheck start count)
    (p : Fin 8) (hlo : start ≤ k) (hhi : k < start + count) :
    ExitCheck p k := by
  have heq : start + (k - start) = k := by omega
  simpa only [heq] using h p ⟨k - start, by omega⟩

theorem exit_witness_of_false (cap n : Nat) (s : Outer)
    (h : staysWithin cap n s = false) :
    ∃ i, i ≤ n ∧ cap < (outerIterate i s).B.length := by
  induction n generalizing s with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    simp [staysWithin] at h
    simpa [outerIterate] using h
  | succ n ih =>
    by_cases hs : s.B.length ≤ cap
    · have hn : staysWithin cap n (outerNext s) = false := by
        simpa [staysWithin, hs] using h
      obtain ⟨i, hi, he⟩ := ih (outerNext s) hn
      exact ⟨i + 1, by omega, by simpa [outerIterate] using he⟩
    · exact ⟨0, by omega, by simpa [outerIterate] using (show cap < s.B.length by omega)⟩

#print axioms of_batch
#print axioms exit_witness_of_false
end P196.Agent116.Cap3
