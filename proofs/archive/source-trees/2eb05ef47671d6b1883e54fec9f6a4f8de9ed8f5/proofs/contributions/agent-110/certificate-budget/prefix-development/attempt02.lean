import CertificateCarryBudget
import PrefixModel

namespace Agent110.CertificatePrefix

open Agent109 Agent109.Cert
open P196.Agent4.Saturation (Prefix advance)

/-- The first three exterior coefficients, continued by the constant band. -/
def padPrefix (B : Word) (c : Nat) : Prefix :=
  ⟨B.getD 0 c, B.getD 1 c, B.getD 2 c⟩

def statePrefix (s : State) : Prefix := padPrefix s.B s.c

theorem prefix_a (s : State) : (statePrefix s).a = CarryBudget.exterior s := by
  cases he : s.B <;> simp [statePrefix, padPrefix, CarryBudget.exterior, he]

theorem getD_bounded (B : Word) (c i : Nat) (hB : Bounded B) (hc : c ≤ 18) :
    B.getD i c ≤ 18 := by
  induction B generalizing i with
  | nil => simpa using hc
  | cons a as ih =>
    cases i with
    | zero => simpa using hB a (by simp)
    | succ i =>
      apply ih
      intro x hx; exact hB x (by simp [hx])

theorem prefix_bounds (s : State) (hc : Phase s.c) (hB : Bounded s.B) :
    (statePrefix s).a ≤ 18 ∧ (statePrefix s).b ≤ 18 ∧ (statePrefix s).c ≤ 18 := by
  have hc18 : s.c ≤ 18 := by have := hc.2.1; omega
  exact ⟨getD_bounded _ _ _ hB hc18, getD_bounded _ _ _ hB hc18,
    getD_bounded _ _ _ hB hc18⟩

theorem getD_replicate_default (c j i : Nat) : (List.replicate j c).getD i c = c := by
  induction j generalizing i with
  | zero => simp
  | succ j ih =>
    cases i with
    | zero => simp [List.replicate_succ]
    | succ i => simpa only [List.replicate_succ] using ih i

theorem getD_append_replicate (B : Word) (c j i : Nat) :
    (B ++ List.replicate j c).getD i c = B.getD i c := by
  induction B generalizing i with
  | nil => exact getD_replicate_default c j i
  | cons a as ih =>
    cases i with
    | zero => rfl
    | succ i => exact ih i

/-- Arbitrary suffix trimming leaves the band-padded prefix unchanged. -/
theorem padPrefix_trim (B : Word) (c j : Nat) :
    padPrefix (B ++ List.replicate j c) c = padPrefix B c := by
  unfold padPrefix
  rw [getD_append_replicate, getD_append_replicate, getD_append_replicate]

end Agent110.CertificatePrefix

#print axioms Agent110.CertificatePrefix.prefix_a
#print axioms Agent110.CertificatePrefix.getD_bounded
#print axioms Agent110.CertificatePrefix.prefix_bounds
#print axioms Agent110.CertificatePrefix.getD_replicate_default
#print axioms Agent110.CertificatePrefix.getD_append_replicate
#print axioms Agent110.CertificatePrefix.padPrefix_trim
