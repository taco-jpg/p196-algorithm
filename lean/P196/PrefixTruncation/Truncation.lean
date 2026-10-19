import P196.Agent104P620Witness.PrefixInverse
import P196.Agent104P620Witness.PrefixCertificate

/-!
# Truncating the complete backward prefix relation

The exact local inverse equations remain valid after taking a common prefix.
Consequently every positive prefix cutoff maps a backward path to a backward
path of the same length.  A cutoff larger than the current word is harmless;
there is no upper-bound hypothesis on the cutoff.

These are statements about the finite coefficient abstraction.  They do not
assert realizability of an abstract path by an ordinary integer orbit.
-/

namespace PrefixTruncation

open SevenColumn SevenColumn.Certificate

/-- Truncation retains the current nonoverflow boundary equations. -/
theorem noOverflow_take {p s : List Nat} {x y : Nat}
    (h : NoOverflow p s x y) (k : Nat) :
    NoOverflow (p.take k) (s.take k) x y := by
  induction k generalizing p s x y with
  | zero => exact NoOverflow.nil x y
  | succ k ih =>
      cases h with
      | nil => exact NoOverflow.nil _ _
      | cons ha hz hy hv tail =>
          exact NoOverflow.cons ha hz hy hv (ih tail)

/-- At a new overflow boundary, the discarded equations supply the terminal
carry required by the truncated relation. -/
theorem overflowTail_take {p s : List Nat} {a x y : Nat}
    (h : OverflowTail p s a x y) (k : Nat) :
    OverflowTail (p.take k) (s.take k) a x y := by
  induction k generalizing p s a x y with
  | zero => exact OverflowTail.nil h.outer_carry
  | succ k ih =>
      cases h with
      | nil terminal => exact OverflowTail.nil terminal
      | cons ha hz hy hv tail =>
          exact OverflowTail.cons ha hz hy hv (ih tail)

/-- A positive cutoff preserves the exterior source coefficient. -/
theorem longCompatible_take {p s : List Nat}
    (h : LongCompatible p s) {k : Nat} (hk : 0 < k) :
    LongCompatible (p.take k) (s.take k) := by
  cases k with
  | zero => omega
  | succ k =>
      cases h with
      | noOverflow positive equations =>
          exact LongCompatible.noOverflow positive (noOverflow_take equations (k + 1))
      | overflow positive ha outer equations =>
          exact LongCompatible.overflow positive ha outer (overflowTail_take equations k)

/-- The complete executable backward relation projects to every positive
prefix width, including cutoffs that exceed the original word length. -/
theorem prefixPredecessors_take {p s : List Nat}
    (h : s ∈ prefixPredecessors p) {k : Nat} (hk : 0 < k) :
    s.take k ∈ prefixPredecessors (p.take k) :=
  mem_prefixPredecessors_iff.mpr
    (longCompatible_take (mem_prefixPredecessors_iff.mp h) hk)

/-- Projection preserves path length.  Repeated projected vertices are
retained, so a positive closed walk remains a positive closed walk. -/
theorem backPath_take {n : Nat} {p z : Word}
    (h : BackPath (fun p s => s ∈ prefixPredecessors p) n p z)
    {k : Nat} (hk : 0 < k) :
    BackPath (fun p s => s ∈ prefixPredecessors p) n (p.take k) (z.take k) := by
  induction h with
  | refl p => exact BackPath.refl _
  | step edge _ ih =>
      exact BackPath.step (prefixPredecessors_take edge hk) ih

#print axioms noOverflow_take
#print axioms overflowTail_take
#print axioms longCompatible_take
#print axioms prefixPredecessors_take
#print axioms backPath_take

end PrefixTruncation
