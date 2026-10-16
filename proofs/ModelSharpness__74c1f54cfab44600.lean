import SaturationTheorem

/-! Sharpness of the period-42 bound for its stated prefix/count premises.
This is an abstract prefix walk, NOT a full complementary quotient cycle,
NOT a coherent all-column carry history, and NOT a Lychrel witness.
-/
namespace P196.Agent4.Saturation

def sharpData : List (Prefix × Nat) := [
  (⟨8,12,9⟩,0),
  (⟨17,4,9⟩,0),
  (⟨8,12,13⟩,0),
  (⟨17,5,7⟩,0),
  (⟨8,13,12⟩,0),
  (⟨17,7,5⟩,0),
  (⟨8,15,12⟩,0),
  (⟨17,11,5⟩,0),
  (⟨8,10,7⟩,0),
  (⟨17,0,15⟩,0),
  (⟨8,8,6⟩,0),
  (⟨16,16,12⟩,0),
  (⟨7,14,10⟩,0),
  (⟨15,9,1⟩,0),
  (⟨6,5,11⟩,0),
  (⟨12,11,2⟩,0),
  (⟨3,5,4⟩,0),
  (⟨6,10,8⟩,1),
  (⟨13,0,18⟩,0),
  (⟨4,4,9⟩,1),
  (⟨8,9,9⟩,1),
  (⟨17,9,9⟩,1),
  (⟨8,8,0⟩,1),
  (⟨16,16,1⟩,0),
  (⟨7,14,8⟩,1),
  (⟨15,8,18⟩,0),
  (⟨6,14,17⟩,0),
  (⟨13,9,15⟩,0),
  (⟨4,4,6⟩,0),
  (⟨8,8,12⟩,1),
  (⟨16,17,5⟩,0),
  (⟨7,15,13⟩,0),
  (⟨15,11,7⟩,0),
  (⟨6,8,9⟩,1),
  (⟨12,17,9⟩,1),
  (⟨3,11,8⟩,0),
  (⟨7,2,17⟩,0),
  (⟨14,5,14⟩,0),
  (⟨5,10,10⟩,0),
  (⟨11,1,1⟩,0),
  (⟨2,3,2⟩,0),
  (⟨4,6,4⟩,1)
]

def sharpEntry (i : Nat) : Prefix × Nat :=
  (sharpData[i%42]?).getD (⟨1,0,0⟩,0)

def sharpState (i : Nat) : Prefix := (sharpEntry i).1
def sharpControl (i : Nat) : Nat := (sharpEntry i).2

/-- Every transition and the overflow count are checked by kernel reduction. -/
theorem period42_model_witness :
    (∀ i : Fin 42, Valid (sharpState i.val) ∧ sharpControl i.val ≤ 1 ∧
      (advance (sharpState i.val) (sharpControl i.val)).1 = sharpState (i.val+1)) ∧
    sharpState 42 = sharpState 0 ∧
    total (fun i => (advance (sharpState i) (sharpControl i)).2) 42 = 18 := by
  unfold Valid
  decide +kernel

/-- The literal model witness meets every hypothesis of the period lower bound. -/
theorem period42_model_meets_lower_bound_premises :
    (∀ i < 42, Valid (sharpState i)) ∧
    (∀ i < 42, sharpControl i ≤ 1) ∧
    (∀ i < 42, (advance (sharpState i) (sharpControl i)).1 = sharpState (i+1)) ∧
    sharpState 42 = sharpState 0 ∧ 0 < (42 : Nat) ∧ 42%6 = 0 ∧
    total (fun i => (advance (sharpState i) (sharpControl i)).2) 42 % 2 = 0 ∧
    total (fun i => (advance (sharpState i) (sharpControl i)).2) 42 % 9 = 0 := by
  have h := period42_model_witness
  refine ⟨?_,?_,?_,h.2.1,by decide,by decide,?_,?_⟩
  · intro i hi; exact (h.1 ⟨i,hi⟩).1
  · intro i hi; exact (h.1 ⟨i,hi⟩).2.1
  · intro i hi; exact (h.1 ⟨i,hi⟩).2.2
  · rw [h.2.2]
  · rw [h.2.2]

#print axioms period42_model_witness
#print axioms period42_model_meets_lower_bound_premises
end P196.Agent4.Saturation
