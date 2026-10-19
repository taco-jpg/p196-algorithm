import P196.FoldedCollisionPrefixes.Terminals

/-!
# Finite halves of reflected collision traces

A prefix with k edges is stored as k+1 states, with no unused function
tail. Saturated access supplies a total Nat-indexed function for the
existing collision-path interface; every semantic access lies inside the
finite tuple. The two reflected traces differ at their midpoint.
-/

set_option autoImplicit false

namespace FoldedCollisionPrefixes

open CrossWidthCollisionStates CrossWidthCollisionPaths

/-- A finite tuple containing the initial state and k further states. -/
abbrev Prefix (k : Nat) := Fin (k + 1) → State

/-- Total access to the tuple, saturated at its last state. -/
def prefixAt {k : Nat} (p : Prefix k) (i : Nat) : State :=
  p ⟨min i k, Nat.lt_succ_of_le (Nat.min_le_right i k)⟩

/-- Extract the first k+1 states of a full trace, starting at index one. -/
def takePrefix (k : Nat) (f : Nat → State) : Prefix k :=
  fun i => f (i.val + 1)

/-- A finite graph walk starting at the forced collision boundary. -/
def Walk (k : Nat) (p : Prefix k) : Prop :=
  prefixAt p 0 = initial ∧
    ∀ i, i < k → Edge (prefixAt p i) (prefixAt p (i + 1))

/-- Acceptance for shorter width 2*k+2, with a reflected central edge. -/
def EvenAccepted (k : Nat) (p : Prefix k) : Prop :=
  Walk k p ∧ EvenTerminal (prefixAt p k)

/-- Acceptance for shorter width 2*k+3, with one central state. -/
def OddAccepted (k : Nat) (p : Prefix (k + 1)) : Prop :=
  Walk (k + 1) p ∧ OddTerminal (prefixAt p (k + 1))

/-- Reflect a prefix with a doubled midpoint, giving shorter width 2*k+2. -/
def evenTrace (k : Nat) (p : Prefix k) (i : Nat) : State :=
  if i ≤ k + 1 then prefixAt p (i - 1)
  else flip (prefixAt p (2 * k + 2 - i))

/-- Reflect a prefix with one midpoint, giving shorter width 2*k+3. -/
def oddTrace (k : Nat) (p : Prefix (k + 1)) (i : Nat) : State :=
  if i ≤ k + 2 then prefixAt p (i - 1)
  else flip (prefixAt p (2 * k + 3 - i))

/-- Saturated access agrees with every actual finite index. -/
theorem prefixAt_fin {k : Nat} (p : Prefix k) (i : Fin (k + 1)) :
    prefixAt p i.val = p i := by
  unfold prefixAt
  have hi : i.val ≤ k := by have := i.isLt; omega
  have he : (⟨min i.val k,
      Nat.lt_succ_of_le (Nat.min_le_right i.val k)⟩ : Fin (k + 1)) = i := by
    apply Fin.ext
    exact Nat.min_eq_left hi
  rw [he]

/-- Extracting a full trace preserves each retained state. -/
theorem prefixAt_take (k : Nat) (f : Nat → State) {i : Nat} (hi : i ≤ k) :
    prefixAt (takePrefix k f) i = f (i + 1) := by
  change f (min i k + 1) = f (i + 1)
  rw [Nat.min_eq_left hi]

/-- The even reflection preserves the complete retained half. -/
theorem evenTrace_prefix (k : Nat) (p : Prefix k) {i : Nat} (hi : i ≤ k) :
    evenTrace k p (i + 1) = prefixAt p i := by
  have h : i + 1 ≤ k + 1 := by omega
  simp only [evenTrace, if_pos h, Nat.add_sub_cancel]

/-- The odd reflection preserves the complete retained half. -/
theorem oddTrace_prefix (k : Nat) (p : Prefix (k + 1))
    {i : Nat} (hi : i ≤ k + 1) :
    oddTrace k p (i + 1) = prefixAt p i := by
  have h : i + 1 ≤ k + 2 := by omega
  simp only [oddTrace, if_pos h, Nat.add_sub_cancel]

/-- Extraction is a left inverse of the even reflection on finite tuples. -/
theorem takePrefix_evenTrace (k : Nat) (p : Prefix k) :
    takePrefix k (evenTrace k p) = p := by
  funext i
  change evenTrace k p (i.val + 1) = p i
  rw [evenTrace_prefix k p (by have := i.isLt; omega)]
  exact prefixAt_fin p i

/-- Extraction is a left inverse of the odd reflection on finite tuples. -/
theorem takePrefix_oddTrace (k : Nat) (p : Prefix (k + 1)) :
    takePrefix (k + 1) (oddTrace k p) = p := by
  funext i
  change oddTrace k p (i.val + 1) = p i
  rw [oddTrace_prefix k p (by have := i.isLt; omega)]
  exact prefixAt_fin p i

end FoldedCollisionPrefixes

#print axioms FoldedCollisionPrefixes.Prefix
#print axioms FoldedCollisionPrefixes.prefixAt
#print axioms FoldedCollisionPrefixes.takePrefix
#print axioms FoldedCollisionPrefixes.Walk
#print axioms FoldedCollisionPrefixes.EvenAccepted
#print axioms FoldedCollisionPrefixes.OddAccepted
#print axioms FoldedCollisionPrefixes.evenTrace
#print axioms FoldedCollisionPrefixes.oddTrace
#print axioms FoldedCollisionPrefixes.prefixAt_fin
#print axioms FoldedCollisionPrefixes.prefixAt_take
#print axioms FoldedCollisionPrefixes.evenTrace_prefix
#print axioms FoldedCollisionPrefixes.oddTrace_prefix
#print axioms FoldedCollisionPrefixes.takePrefix_evenTrace
#print axioms FoldedCollisionPrefixes.takePrefix_oddTrace
