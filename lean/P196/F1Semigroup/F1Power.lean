import P196.F1Semigroup.F1PowerChk1
import P196.F1Semigroup.F1PowerChk2
/-!
# Power closure: `Lang (w^k) ↔ Lang w` for all words `w` and all `k ≥ 1` (decimal F1 automaton)
-/
namespace F1

def pow (w : List Bool) : Nat → List Bool
  | 0 => []
  | k + 1 => w ++ pow w k

theorem pow_add (w : List Bool) (a b : Nat) : pow w (a + b) = pow w a ++ pow w b := by
  induction a with
  | zero => simp [pow]
  | succ a ih => rw [Nat.succ_add]; simp [pow, ih, List.append_assoc]

theorem pow_mul (w : List Bool) (k j : Nat) : pow (pow w k) j = pow w (k * j) := by
  induction j with
  | zero => simp [pow]
  | succ j ih =>
    show pow w k ++ pow (pow w k) j = _
    rw [ih, Nat.mul_succ, Nat.add_comm (k * j) k, pow_add]

theorem pow_nil (k : Nat) : pow [] k = [] := by
  induction k with
  | zero => rfl
  | succ k ih => simp [pow, ih]

theorem nilOK_all : ∀ i, i < nS → nilOK i = true := by
  intro i hi
  by_cases h : i < 217
  · exact nilOK_1 i h
  · exact nilOK_2 i (by unfold nS at hi; omega) (by omega)

theorem zeroRel_row (M : Rel) (h : zeroRel M = true) (x : Nat) : row M x = 0 := by
  unfold zeroRel at h
  rw [List.all_eq_true] at h
  unfold row
  by_cases hx : x < M.length
  · rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hx, Option.getD_some]
    have := h M[x] (List.getElem_mem hx)
    simpa using this
  · rw [List.getD_eq_getElem?_getD, List.getElem?_eq_none (by omega)]
    rfl

theorem pow5_eq (w : List Bool) : pow w 5 = w ++ ((w ++ w) ++ (w ++ w)) := by
  simp [pow, List.append_assoc]

/-- every nonempty word either has a closed walk or its fifth power has no walk at all -/
theorem dichotomy (w : List Bool) (hw : w ≠ []) : Lang w ∨ (∀ x z, ¬ Reach (pow w 5) x z) := by
  obtain ⟨i, hi, hrun⟩ := S_is_reachable_set.1 w
  have hok := nilOK_all i hi
  unfold nilOK at hok
  simp only [Bool.or_eq_true] at hok
  rcases hok with hacc | hz
  · left
    have h2 : accB i = true := by rw [← accQ_eq i hi]; exact hacc
    have h3 : LangB w = true := by
      unfold LangB; rw [hrun]; exact h2
    exact (LangB_iff w).1 h3
  · right
    have hM : ∀ x y, x < 18 → y < 18 → (MatRel (Sget i) x y ↔ Reach w (x + 1) (y + 1)) := by
      intro x y hx hy
      rw [← hrun]; exact MatRel_run w x y hx hy
    have hw2 : w ++ w ≠ [] := by simp [hw]
    have hM2 : ∀ x y, x < 18 → y < 18 → (MatRel (M2 (Sget i)) x y ↔ Reach (w ++ w) (x + 1) (y + 1)) :=
      fun x y hx hy => MatRel_append (Sget i) (Sget i) w w hw hM hM x y hx hy
    have hM4 : ∀ x y, x < 18 → y < 18 →
        (MatRel (M4 (Sget i)) x y ↔ Reach ((w ++ w) ++ (w ++ w)) (x + 1) (y + 1)) :=
      fun x y hx hy => MatRel_append (M2 (Sget i)) (M2 (Sget i)) (w ++ w) (w ++ w) hw2 hM2 hM2 x y hx hy
    have hM5 : ∀ x y, x < 18 → y < 18 →
        (MatRel (M5 (Sget i)) x y ↔ Reach (w ++ ((w ++ w) ++ (w ++ w))) (x + 1) (y + 1)) :=
      fun x y hx hy => MatRel_append (Sget i) (M4 (Sget i)) w ((w ++ w) ++ (w ++ w)) hw hM hM4 x y hx hy
    intro x z h
    have hne : pow w 5 ≠ [] := by rw [pow5_eq]; simp [hw]
    obtain ⟨hx1, hx2⟩ := Reach_start _ x z hne h
    obtain ⟨hz1, hz2⟩ := Reach_range _ x z hne h
    rw [pow5_eq] at h
    have ex : x - 1 + 1 = x := by omega
    have ez : z - 1 + 1 = z := by omega
    have := (hM5 (x - 1) (z - 1) (by omega) (by omega)).2 (by rw [ex, ez]; exact h)
    unfold MatRel at this
    rw [zeroRel_row _ hz] at this
    simp at this

theorem reach_pow_diag (v : List Bool) (x : Nat) (h : Reach v x x) : ∀ j, Reach (pow v j) x x := by
  intro j
  induction j with
  | zero => simp [pow, Reach]
  | succ j ih => simp only [pow]; rw [Reach_append]; exact ⟨x, h, ih⟩

theorem no_long (w : List Bool) (h5 : ∀ x z, ¬ Reach (pow w 5) x z) :
    ∀ n, 5 ≤ n → ∀ x z, ¬ Reach (pow w n) x z := by
  intro n hn x z h
  obtain ⟨m, rfl⟩ : ∃ m, n = 5 + m := ⟨n - 5, by omega⟩
  rw [pow_add, Reach_append] at h
  obtain ⟨y, hy, _⟩ := h
  exact h5 x y hy

/-- **Power closure**: for every word `w` and `k ≥ 1`, `w^k` has a closed walk iff `w` has one. -/
theorem power_closure (w : List Bool) (k : Nat) (hk : 1 ≤ k) : Lang (pow w k) ↔ Lang w := by
  by_cases hw : w = []
  · subst hw; rw [pow_nil]
  by_cases hl : Lang w
  · obtain ⟨x, hx1, hx2, hr⟩ := hl
    exact ⟨fun _ => ⟨x, hx1, hx2, hr⟩, fun _ => ⟨x, hx1, hx2, reach_pow_diag w x hr k⟩⟩
  · rcases dichotomy w hw with h | h5
    · exact absurd h hl
    · constructor
      · rintro ⟨x, hx1, hx2, hr⟩
        exfalso
        have := reach_pow_diag (pow w k) x hr 5
        rw [pow_mul] at this
        exact no_long w h5 (k * 5) (by omega) x x this
      · intro h; exact absurd h hl

end F1
