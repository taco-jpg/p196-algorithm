import BaseBirths
import ResetNormalization

/-!
Coupled adjacent arithmetic for an overflowing ordinary carry chain.
The outgoing carries of the two old neighboring coefficients are computed
from the incoming exterior carry bits.  The actual word-index bridge is a
separate module.  Every statement here includes base two.
-/
namespace P196.Agent7.AllBaseOverflow

/-- The coupled adjacent pair with both intermediate carries computed. -/
def adjacentPair (b a z l h : Int) : Int :=
  (z + (a + l) / b) % b + (a + (z + h) / b) % b

/-- The existing same-coefficient classifier, specialized to equal carries. -/
theorem residue_zero_iff (b x c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2 * b - 2) (hc : 0 ≤ c ∧ c ≤ 1) :
    (x + c) % b = 0 ↔
      (x = 0 ∧ c = 0) ∨ (x = b ∧ c = 0) ∨ (x = b - 1 ∧ c = 1) := by
  have he := BaseBirths.localPair_eq_zero_iff b x c c hb hx hc hc
  unfold BaseBirths.localPair at he
  omega

/-- The existing maximal-pair classifier determines one maximal digit. -/
theorem residue_max_iff (b x c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2 * b - 2) (hc : 0 ≤ c ∧ c ≤ 1) :
    (x + c) % b = b - 1 ↔
      (x = b - 1 ∧ c = 0) ∨ (x = b - 2 ∧ c = 1) ∨
        (x = 2 * b - 2 ∧ c = 1) := by
  have he := BaseBirths.localPair_eq_max_iff b x c c hb hx hc hc
  unfold BaseBirths.localPair at he
  omega

/-- Complete zero classification for the two coupled adjacent columns.
The intermediate carries u and v must satisfy their actual division equations. -/
theorem adjacent_residues_zero_iff (b a z l u v h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1)
    (hu : u = (a + l) / b) (hv : v = (z + h) / b) :
    (z + u) % b + (a + v) % b = 0 ↔
      (a = 0 ∧ z = 0) ∨
      (a = b - 1 ∧ z = b - 1 ∧ u = 1 ∧ v = 1) ∨
      (a = b - 1 ∧ z = b ∧ u = 0) ∨
      (a = b ∧ z = b - 1 ∧ v = 0) := by
  have hub : u = 0 ∨ u = 1 := by
    rw [hu]
    exact ResetNormalization.carry_bit b a l hb ha hl
  have hvb : v = 0 ∨ v = 1 := by
    rw [hv]
    exact ResetNormalization.carry_bit b z h hb hz hh
  have hu01 : 0 ≤ u ∧ u ≤ 1 := by omega
  have hv01 : 0 ≤ v ∧ v ≤ 1 := by omega
  have hzp := Int.emod_nonneg (z + u) (show b ≠ 0 by omega)
  have hap := Int.emod_nonneg (a + v) (show b ≠ 0 by omega)
  have hzero : (z + u) % b + (a + v) % b = 0 ↔
      (z + u) % b = 0 ∧ (a + v) % b = 0 := by omega
  rw [hzero, residue_zero_iff b z u hb hz hu01, residue_zero_iff b a v hb ha hv01]
  have hue := Int.emod_add_ediv (a + l) b
  have hve := Int.emod_add_ediv (z + h) b
  rw [← hu] at hue
  rw [← hv] at hve
  have hun := Int.emod_nonneg (a + l) (show b ≠ 0 by omega)
  have hvn := Int.emod_nonneg (z + h) (show b ≠ 0 by omega)
  have hult := Int.emod_lt_of_pos (a + l) (show 0 < b by omega)
  have hvlt := Int.emod_lt_of_pos (z + h) (show 0 < b by omega)
  rcases hub with rfl | rfl <;> rcases hvb with rfl | rfl <;>
    simp only [Int.mul_zero, Int.mul_one, Int.add_zero] at hue hve <;> omega

/-- Complete maximal classification for coupled adjacent columns, including b=2. -/
theorem adjacent_residues_max_iff (b a z l u v h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1)
    (hu : u = (a + l) / b) (hv : v = (z + h) / b) :
    (z + u) % b + (a + v) % b = 2 * b - 2 ↔
      (a = 2 * b - 2 ∧ z = 2 * b - 2) ∨
      (a = b - 1 ∧ z = b - 1 ∧ u = 0 ∧ v = 0) ∨
      (a = b - 1 ∧ z = b - 2 ∧ u = 1) ∨
      (a = b - 2 ∧ z = b - 1 ∧ v = 1) := by
  have hub : u = 0 ∨ u = 1 := by
    rw [hu]
    exact ResetNormalization.carry_bit b a l hb ha hl
  have hvb : v = 0 ∨ v = 1 := by
    rw [hv]
    exact ResetNormalization.carry_bit b z h hb hz hh
  have hu01 : 0 ≤ u ∧ u ≤ 1 := by omega
  have hv01 : 0 ≤ v ∧ v ≤ 1 := by omega
  have hzp := Int.emod_nonneg (z + u) (show b ≠ 0 by omega)
  have hap := Int.emod_nonneg (a + v) (show b ≠ 0 by omega)
  have hzlt := Int.emod_lt_of_pos (z + u) (show 0 < b by omega)
  have halt := Int.emod_lt_of_pos (a + v) (show 0 < b by omega)
  have hmax : (z + u) % b + (a + v) % b = 2 * b - 2 ↔
      (z + u) % b = b - 1 ∧ (a + v) % b = b - 1 := by omega
  rw [hmax, residue_max_iff b z u hb hz hu01, residue_max_iff b a v hb ha hv01]
  have hue := Int.emod_add_ediv (a + l) b
  have hve := Int.emod_add_ediv (z + h) b
  rw [← hu] at hue
  rw [← hv] at hve
  have hun := Int.emod_nonneg (a + l) (show b ≠ 0 by omega)
  have hvn := Int.emod_nonneg (z + h) (show b ≠ 0 by omega)
  have hult := Int.emod_lt_of_pos (a + l) (show 0 < b by omega)
  have hvlt := Int.emod_lt_of_pos (z + h) (show 0 < b by omega)
  rcases hub with rfl | rfl <;> rcases hvb with rfl | rfl <;>
    simp only [Int.mul_zero, Int.mul_one, Int.add_zero] at hue hve <;> omega

/-- The zero classifier with no named intermediate carries. -/
theorem adjacentPair_zero_iff (b a z l h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1) :
    adjacentPair b a z l h = 0 ↔
      (a = 0 ∧ z = 0) ∨
      (a = b - 1 ∧ z = b - 1 ∧ (a + l) / b = 1 ∧ (z + h) / b = 1) ∨
      (a = b - 1 ∧ z = b ∧ (a + l) / b = 0) ∨
      (a = b ∧ z = b - 1 ∧ (z + h) / b = 0) :=
  adjacent_residues_zero_iff b a z l _ _ h hb ha hz hl hh rfl rfl

/-- The maximal classifier with no named intermediate carries. -/
theorem adjacentPair_max_iff (b a z l h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1) :
    adjacentPair b a z l h = 2 * b - 2 ↔
      (a = 2 * b - 2 ∧ z = 2 * b - 2) ∨
      (a = b - 1 ∧ z = b - 1 ∧ (a + l) / b = 0 ∧ (z + h) / b = 0) ∨
      (a = b - 1 ∧ z = b - 2 ∧ (a + l) / b = 1) ∨
      (a = b - 2 ∧ z = b - 1 ∧ (z + h) / b = 1) :=
  adjacent_residues_max_iff b a z l _ _ h hb ha hz hl hh rfl rfl

/-- A new interior extreme must use an old neutral coefficient b-1. -/
theorem adjacent_new_extreme_neutral (b a z l u v h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1)
    (hu : u = (a + l) / b) (hv : v = (z + h) / b)
    (hnew : ((z + u) % b + (a + v) % b = 0 ∧ ¬ (a = 0 ∧ z = 0)) ∨
      ((z + u) % b + (a + v) % b = 2 * b - 2 ∧
        ¬ (a = 2 * b - 2 ∧ z = 2 * b - 2))) :
    a = b - 1 ∨ z = b - 1 := by
  rw [adjacent_residues_zero_iff b a z l u v h hb ha hz hl hh hu hv,
    adjacent_residues_max_iff b a z l u v h hb ha hz hl hh hu hv] at hnew
  omega

/-- Without a neutral neighbor an extreme is exactly inherited from two extremes. -/
theorem adjacent_without_neutral (b a z l u v h : Int) (hb : 2 ≤ b)
    (ha : 0 ≤ a ∧ a ≤ 2 * b - 2) (hz : 0 ≤ z ∧ z ≤ 2 * b - 2)
    (hl : 0 ≤ l ∧ l ≤ 1) (hh : 0 ≤ h ∧ h ≤ 1)
    (hu : u = (a + l) / b) (hv : v = (z + h) / b)
    (han : a ≠ b - 1) (hzn : z ≠ b - 1) :
    ((z + u) % b + (a + v) % b = 0 ↔ a = 0 ∧ z = 0) ∧
      ((z + u) % b + (a + v) % b = 2 * b - 2 ↔
        a = 2 * b - 2 ∧ z = 2 * b - 2) := by
  rw [adjacent_residues_zero_iff b a z l u v h hb ha hz hl hh hu hv,
    adjacent_residues_max_iff b a z l u v h hb ha hz hl hh hu hv]
  omega

#print axioms residue_zero_iff
#print axioms residue_max_iff
#print axioms adjacent_residues_zero_iff
#print axioms adjacent_residues_max_iff
#print axioms adjacentPair_zero_iff
#print axioms adjacentPair_max_iff
#print axioms adjacent_new_extreme_neutral
#print axioms adjacent_without_neutral

end P196.Agent7.AllBaseOverflow
