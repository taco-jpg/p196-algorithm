import SmallPeriodObstruction

/-! Author adversarial controls for the small-period approach.
The eight-cycle is the existing Agent4 saturation cycle, not a new discovery.
The auxiliary phase and charge streams below are deliberately independent
coordinates. They do not claim realization by a full exterior, certificate,
or ordinary integer. These controls locate a limitation of the relaxation. -/
namespace Agent112.SmallPeriod.Controls
open P196.Agent4.Saturation

/-- Only the projected path, scalar phase/charge laws and aggregate budgets.
Crucially, no full word identifies the auxiliary charge or inner carry. -/
def Relaxation (p : Nat) (s : Nat → Prefix) (e c : Nat → Nat)
    (q : Nat → Int) : Prop :=
  0 < p ∧
  (∀ i : Fin p, Valid (s i.val) ∧ e i.val ≤ 1 ∧
    (advance (s i.val) (e i.val)).1 = s (i.val + 1) ∧
    (c i.val = 6 ∨ c i.val = 12) ∧
    c (i.val+1) = Agent2Exterior.phase (c i.val) ∧
    q (i.val+1) % 9 =
      (2*q i.val - ((advance (s i.val) (e i.val)).2 : Int) * (c i.val : Int)) % 9) ∧
  s p = s 0 ∧ c p = c 0 ∧ q p = q 0 ∧
  0 < total (fun i => (advance (s i) (e i)).2) p ∧
  total (fun i => (advance (s i) (e i)).2) p % 2 = 0 ∧
  2*total (fun i => (advance (s i) (e i)).2) p ≤ p ∧
  p ≤ 4*total (fun i => (advance (s i) (e i)).2) p ∧
  (2*total (fun i => (advance (s i) (e i)).2) p = p → p % 8 = 0)

def phaseAt (i : Nat) : Nat := if i % 2 = 0 then 6 else 12

def eightData : List (Prefix × Nat) := [
  (⟨8,12,9⟩,1), (⟨17,5,0⟩,0), (⟨8,13,5⟩,0), (⟨17,6,11⟩,0),
  (⟨8,14,8⟩,0), (⟨17,8,17⟩,0), (⟨8,16,16⟩,1), (⟨17,13,14⟩,0)]
def eightEntry (i : Nat) : Prefix × Nat := eightData.getD (i%8) (⟨1,0,0⟩,0)
def eightState (i : Nat) : Prefix := (eightEntry i).1
def eightInput (i : Nat) : Nat := (eightEntry i).2
def eightCharge (i : Nat) : Int := if i%2=0 then 1 else 2

/-- A kernel-checked countermodel to deriving period>=12 from the relaxation.
It does not assert Agent109.Cert.check=true for any certificate. -/
theorem eight_relaxation : Relaxation 8 eightState eightInput phaseAt eightCharge := by
  simp only [Relaxation, Valid]
  decide +kernel

def tenData : List (Prefix × Nat) := [
  (⟨1,4,4⟩,0), (⟨2,8,8⟩,1), (⟨4,16,17⟩,0), (⟨9,13,15⟩,0),
  (⟨10,3,10⟩,0)]
def tenEntry (i : Nat) : Prefix × Nat := tenData.getD (i%5) (⟨1,0,0⟩,0)
def tenState (i : Nat) : Prefix := (tenEntry i).1
def tenInput (i : Nat) : Nat := (tenEntry i).2
def tenCharge (i : Nat) : Int :=
  ([2,4,8,7,2,7,5,1,2,7] : List Int).getD (i%10) 0

/-- The ten-step countermodel is a repeated five-step projected path, with
a ten-step phase/charge stream. No least-period assertion is made. -/
theorem ten_relaxation : Relaxation 10 tenState tenInput phaseAt tenCharge := by
  simp only [Relaxation, Valid]
  decide +kernel

theorem no_relaxation_period_twelve :
    ¬ (∀ (p : Nat) (s : Nat → Prefix) (e c : Nat → Nat) (q : Nat → Int),
      Relaxation p s e c q → 12 ≤ p) := by
  intro h
  have hh := h 8 eightState eightInput phaseAt eightCharge eight_relaxation
  omega

#print axioms eight_relaxation
#print axioms ten_relaxation
#print axioms no_relaxation_period_twelve
end Agent112.SmallPeriod.Controls
