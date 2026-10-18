import P196.Agent2SaturatedProfile.WholeWordBridge

/-! Review illustrations only, not new main-theorem ownership.
The fresh closure and this module must both compile before these declarations
are reported as checked. No native evaluator is used. The associated Python
enumeration remains a bounded diagnostic even if these two instances compile.
-/
namespace P196.Agent104.Agent4Review
open DecimalDigits P196.Agent4.WholeWord

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

def decimalDigits (n i : Nat) : Nat := n / 10^i % 10

theorem decimalDigits_bounded (n i : Nat) : decimalDigits n i ≤ 9 := by
  have h := Nat.mod_lt (n / 10^i) (by decide : 0 < 10)
  unfold decimalDigits
  omega

theorem canonical_89870 : Canonical 89870 (decimalDigits 89870) 5 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i _
  exact decimalDigits_bounded _ _

theorem canonical_179745797 :
    Canonical 179745797 (decimalDigits 179745797) 9 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i _
  exact decimalDigits_bounded _ _

theorem canonical_770 : Canonical 770 (decimalDigits 770) 3 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i _
  exact decimalDigits_bounded _ _

theorem canonical_176176 : Canonical 176176 (decimalDigits 176176) 6 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i _
  exact decimalDigits_bounded _ _

theorem orbit_89870_eight : Lychrel196.orbit 89870 8 = 179745797 := by
  decide +kernel

theorem orbit_770_seven : Lychrel196.orbit 770 7 = 176176 := by
  decide +kernel

/-- Nonempty ordinary saturated prefix return: width 5 to 9 in eight steps. -/
theorem saturated_return_89870 :
    Lychrel196.orbit 89870 8 = 179745797 ∧
    Canonical 89870 (decimalDigits 89870) 5 ∧
    Canonical (Lychrel196.orbit 89870 8) (decimalDigits 179745797) 9 ∧
    prefix3 (columnSum (decimalDigits 89870) 5) = ⟨8,16,16⟩ ∧
    prefix3 (columnSum (decimalDigits 179745797) 9) = ⟨8,16,16⟩ ∧
    2*9 = 2*5+8 ∧ 8%8=0 := by
  refine ⟨orbit_89870_eight, canonical_89870, ?_, by decide +kernel,
    by decide +kernel, by decide, by decide⟩
  rw [orbit_89870_eight]
  exact canonical_179745797

/-- Dropping saturation is unsound: the canonical prefix returns at time seven. -/
theorem nonsaturated_return_770 :
    Lychrel196.orbit 770 7 = 176176 ∧
    Canonical 770 (decimalDigits 770) 3 ∧
    Canonical (Lychrel196.orbit 770 7) (decimalDigits 176176) 6 ∧
    prefix3 (columnSum (decimalDigits 770) 3) = ⟨7,14,7⟩ ∧
    prefix3 (columnSum (decimalDigits 176176) 6) = ⟨7,14,7⟩ ∧
    2*6 < 2*3+7 ∧ 7%8≠0 := by
  refine ⟨orbit_770_seven, canonical_770, ?_, by decide +kernel,
    by decide +kernel, by decide, by decide⟩
  rw [orbit_770_seven]
  exact canonical_176176

#print axioms decimalDigits_bounded
#print axioms canonical_89870
#print axioms canonical_179745797
#print axioms canonical_770
#print axioms canonical_176176
#print axioms orbit_89870_eight
#print axioms orbit_770_seven
#print axioms saturated_return_89870
#print axioms nonsaturated_return_770
end P196.Agent104.Agent4Review
