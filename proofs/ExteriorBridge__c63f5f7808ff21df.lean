import ExteriorCore

namespace P196.Agent6

/-- Coefficient bounds for decimal mirrored-sum words. -/
def Coefficients (w : Word) : Prop := ∀ x ∈ w, x ≤ 18

def Nonneutral (c : Nat) : Prop := 0 < c ∧ c ≤ 17 ∧ c ≠ 9

def carryPhase (c : Nat) : Nat := if 10 ≤ c then 1 else 0

def digitPhase (c : Nat) : Nat := c - 9 * carryPhase c

theorem norm_length (w : Word) (e : Nat) : (norm w e).1.length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm,ih]

theorem norm_append (a b : Word) (e : Nat) :
    norm (a ++ b) e =
      ((norm a e).1 ++ (norm b (norm a e).2).1,
       (norm b (norm a e).2).2) := by
  induction a generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm,ih]

theorem norm_carry_bit (w : Word) (e : Nat) (hw : Coefficients w)
    (he : e ≤ 1) : (norm w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => exact he
  | cons x xs ih =>
      have hx : x ≤ 18 := hw x (by simp)
      have ht : Coefficients xs := by
        intro y hy
        exact hw y (by simp [hy])
      exact ih ((x+e)/10) ht (by omega)

theorem carryPhase_bit (c : Nat) : carryPhase c ≤ 1 := by
  unfold carryPhase
  split <;> omega

/-- A nonneutral coefficient resets either incoming carry bit in one column. -/
theorem nonneutral_reset (c e : Nat) (hc : Nonneutral c) (he : e ≤ 1) :
    (c+e)/10 = carryPhase c ∧
    (c+e)%10 = c+e-10*carryPhase c := by
  rcases hc with ⟨hp,hm,hn⟩
  unfold carryPhase
  split <;> omega

theorem phase_stable (c : Nat) (hc : Nonneutral c) :
    (c+carryPhase c)/10 = carryPhase c ∧
    (c+carryPhase c)%10 = digitPhase c := by
  rcases hc with ⟨hp,hm,hn⟩
  by_cases h : 10 ≤ c
  · simp only [digitPhase,carryPhase,if_pos h]
    omega
  · simp only [digitPhase,carryPhase,if_neg h]
    omega

theorem norm_replicate_stable (c m : Nat) (hc : Nonneutral c) :
    norm (List.replicate m c) (carryPhase c) =
      (List.replicate m (digitPhase c), carryPhase c) := by
  have hs := phase_stable c hc
  induction m with
  | zero => rfl
  | succ m ih => simp [List.replicate_succ,norm,hs.1,hs.2,ih]

/-- One entrance digit followed by arbitrarily many stable bulk digits. -/
theorem norm_band (c m e : Nat) (hc : Nonneutral c) (he : e ≤ 1) :
    norm (List.replicate (m+1) c) e =
      ((c+e-10*carryPhase c) :: List.replicate m (digitPhase c), carryPhase c) := by
  have hr := nonneutral_reset c e hc he
  simp [List.replicate_succ,norm,hr.1,hr.2,norm_replicate_stable c m hc]

/-- Outer bands around an arbitrary coefficient middle. -/
def surrounded (B : Word) (c g : Nat) (W : Word) : Word :=
  B ++ List.replicate (g+2) c ++ W ++ List.replicate (g+2) c ++ B.reverse

/-- Actual normalization, including the possible final carry as a digit. -/
def normalizedDigits (q : Word) : Word :=
  let out := norm q 0
  out.1 ++ if out.2 == 0 then [] else [out.2]

/-- Exact normalization of the surrounded word; no freely chosen carry. -/
theorem surrounded_normalization (B W : Word) (c g : Nat)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W) :
    norm (surrounded B c g W) 0 =
      ((norm B 0).1 ++
       [(c+(norm B 0).2-10*carryPhase c)] ++
       List.replicate (g+1) (digitPhase c) ++
       (norm W (carryPhase c)).1 ++
       [(c+(norm W (carryPhase c)).2-10*carryPhase c)] ++
       List.replicate (g+1) (digitPhase c) ++
       (norm B.reverse (carryPhase c)).1,
       (norm B.reverse (carryPhase c)).2) := by
  have hb := norm_carry_bit B 0 hB (by omega)
  have hw := norm_carry_bit W (carryPhase c) hW (carryPhase_bit c)
  simp only [surrounded, norm_append]
  rw [norm_band c (g+1) (norm B 0).2 hc hb]
  rw [norm_band c (g+1) (norm W (carryPhase c)).2 hc hw]
  simp [List.append_assoc]

#print axioms norm_length
#print axioms norm_append
#print axioms norm_carry_bit
#print axioms carryPhase_bit
#print axioms nonneutral_reset
#print axioms phase_stable
#print axioms norm_replicate_stable
#print axioms norm_band
#print axioms surrounded_normalization
end P196.Agent6
