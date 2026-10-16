import InverseFibers

/-!
The restricted three-layer zero-overflow prefix machine. The fixed first
coefficient is 14; later coefficients are 5 or 14. Its arithmetic interface
is the original P196.Agent9.InverseFibers.Local relation.

Original Local source blob: cade8ace6359fe8246a29ec781859e3a39b00e11.
Historical generator: c41f16d9853adf8320db54564385d1b3fe8fde99.
Later clock000/y5 generator: d845edd9a114bd61ff379d0184cae36ce6f3d379.
The machine is a prefix condition; it does not assert center sufficiency.
-/

namespace P196.Agent3.PrefixContraction

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

abbrev Triple := State × State × State

def coefficient (bit : Bool) : Symbol := if bit then 14 else 5

/-- Choose the unique carry successor away from target coefficient nine.
At nine this selects one valid successor; coverage is used only away from nine. -/
def nextCarry (s : Symbol) (p : State) : Option State :=
  if s.val % 2 = 1 then
    match p.val with
    | 0 => some 1
    | 1 => some 3
    | 2 => some 0
    | _ => some 2
  else
    match p.val with
    | 0 => some 0
    | 1 => if s.val = 18 then none else some 2
    | 2 => if s.val = 0 then none else some 1
    | _ => some 3

/-- The two remainder equations determine the emitted coefficient. -/
def emitted (s : Symbol) (p q : State) : Symbol :=
  ⟨((s.val + 10 * (low q + high p) - low p - high q) / 2) % 19,
    Nat.mod_lt _ (by decide)⟩

def oneStep (s : Symbol) (p : State) : Option (State × Symbol) :=
  (nextCarry s p).map (fun q => (q, emitted s p q))

def machineStep (bit : Bool) (p : Triple) : Option Triple := do
  let (q₁, x) ← oneStep (coefficient bit) p.1
  let (q₂, y) ← oneStep x p.2.1
  let (q₃, _) ← oneStep y p.2.2
  pure (q₁, q₂, q₃)

def advance (p : Option Triple) (bit : Bool) : Option Triple :=
  p.bind (machineStep bit)

def prefixRun (p : Option Triple) (bits : List Bool) : Option Triple :=
  bits.foldl advance p

@[simp] theorem coefficient_false : coefficient false = 5 := rfl
@[simp] theorem coefficient_true : coefficient true = 14 := rfl

theorem machineStep_initial : machineStep true (0, 0, 0) = some (0, 1, 1) := by
  decide

/-- An actual local label gives a nonzero entry in the original table. -/
theorem table_nonzero_of_local (s : Symbol) (p q : State) (x : Nat)
    (h : Local s p q x) : table s p q ≠ 0 := by
  intro ht
  have hw : weight s p q = 0 := by rw [weight_eq_table]; exact ht
  have hx : x ∈ (List.range 19).filter (fun y => decide (Local s p q y)) := by
    simp only [List.mem_filter, List.mem_range, decide_eq_true_eq]
    exact ⟨h.1, h⟩
  unfold weight at hw
  cases he : (List.range 19).filter (fun y => decide (Local s p q y)) with
  | nil => simp [he] at hx
  | cons a as => simp [he] at hw

/-- The original table has one successor away from its coefficient-nine branch. -/
theorem nextCarry_complete : ∀ s : Symbol, ∀ p q : State,
    s ≠ 9 → table s p q ≠ 0 → nextCarry s p = some q := by
  decide

/-- Every emitted one-layer row satisfies the unchanged decimal equations. -/
theorem oneStep_valid : ∀ s : Symbol, ∀ p : State,
    ∀ q : State, ∀ x : Symbol,
    oneStep s p = some (q, x) → Local s p q x.val := by
  decide

theorem oneStep_sound (s : Symbol) (p q : State) (x : Symbol)
    (h : oneStep s p = some (q, x)) : Local s p q x.val := by
  exact oneStep_valid s p q x h

/-- Coverage combines the original table with its original label uniqueness. -/
theorem oneStep_coverage (s : Symbol) (p q : State) (x : Symbol)
    (hs : s ≠ 9) (h : Local s p q x.val) : oneStep s p = some (q, x) := by
  have hn := nextCarry_complete s p q hs (table_nonzero_of_local s p q x.val h)
  have ho : oneStep s p = some (q, emitted s p q) := by simp [oneStep, hn]
  have he := local_unique s p q x (emitted s p q) h (oneStep_sound s p q _ ho)
  rw [he]
  exact ho

theorem coefficient_ne_nine : ∀ bit : Bool, coefficient bit ≠ 9 := by decide

theorem first_label_ne_nine : ∀ bit : Bool, ∀ p : State,
    ((oneStep (coefficient bit) p).map Prod.snd).getD 0 ≠ 9 := by
  decide

theorem second_label_ne_nine : ∀ bit : Bool, ∀ p₁ p₂ : State,
    ((oneStep (((oneStep (coefficient bit) p₁).map Prod.snd).getD 0) p₂).map
      Prod.snd).getD 0 ≠ 9 := by
  decide

/-- Every three-layer original arithmetic transition is represented. -/
theorem machineStep_coverage (bit : Bool) (p q : Triple) (x y z : Symbol)
    (hx : Local (coefficient bit) p.1 q.1 x.val)
    (hy : Local x p.2.1 q.2.1 y.val)
    (hz : Local y p.2.2 q.2.2 z.val) : machineStep bit p = some q := by
  have hs₁ := oneStep_coverage _ _ _ x (coefficient_ne_nine bit) hx
  have hx9 : x ≠ 9 := by
    simpa [hs₁] using first_label_ne_nine bit p.1
  have hs₂ := oneStep_coverage _ _ _ y hx9 hy
  have hy9 : y ≠ 9 := by
    simpa [hs₁, hs₂] using second_label_ne_nine bit p.1 p.2.1
  have hs₃ := oneStep_coverage _ _ _ z hy9 hz
  simp [machineStep, hs₁, hs₂, hs₃]

/-- A represented transition has all three original arithmetic witnesses. -/
theorem machineStep_sound (bit : Bool) (p q : Triple)
    (h : machineStep bit p = some q) :
    ∃ x y z : Symbol, Local (coefficient bit) p.1 q.1 x.val ∧
      Local x p.2.1 q.2.1 y.val ∧ Local y p.2.2 q.2.2 z.val := by
  cases h₁ : oneStep (coefficient bit) p.1 with
  | none => simp [machineStep, h₁] at h
  | some row₁ =>
      rcases row₁ with ⟨q₁, x⟩
      cases h₂ : oneStep x p.2.1 with
      | none => simp [machineStep, h₁, h₂] at h
      | some row₂ =>
          rcases row₂ with ⟨q₂, y⟩
          cases h₃ : oneStep y p.2.2 with
          | none => simp [machineStep, h₁, h₂, h₃] at h
          | some row₃ =>
              rcases row₃ with ⟨q₃, z⟩
              have hq : (q₁, q₂, q₃) = q := by
                simpa [machineStep, h₁, h₂, h₃] using h
              subst q
              exact ⟨x, y, z, oneStep_sound _ _ _ _ h₁,
                oneStep_sound _ _ _ _ h₂, oneStep_sound _ _ _ _ h₃⟩

theorem machineStep_eq_some_iff (bit : Bool) (p q : Triple) :
    machineStep bit p = some q ↔
    ∃ x y z : Symbol, Local (coefficient bit) p.1 q.1 x.val ∧
      Local x p.2.1 q.2.1 y.val ∧ Local y p.2.2 q.2.2 z.val := by
  constructor
  · exact machineStep_sound bit p q
  · rintro ⟨x, y, z, hx, hy, hz⟩
    exact machineStep_coverage bit p q x y z hx hy hz

@[simp] theorem advance_none (bit : Bool) : advance none bit = none := rfl

@[simp] theorem prefixRun_nil (p : Option Triple) : prefixRun p [] = p := rfl

@[simp] theorem prefixRun_cons (p : Option Triple) (bit : Bool) (bits : List Bool) :
    prefixRun p (bit :: bits) = prefixRun (advance p bit) bits := rfl

@[simp] theorem prefixRun_none (bits : List Bool) : prefixRun none bits = none := by
  induction bits with
  | nil => rfl
  | cons bit bits ih => simpa only [prefixRun_cons, advance_none] using ih

theorem prefixRun_append (p : Option Triple) (xs ys : List Bool) :
    prefixRun p (xs ++ ys) = prefixRun (prefixRun p xs) ys := by
  induction xs generalizing p with
  | nil => rfl
  | cons bit bits ih => exact ih (advance p bit)

#print axioms Triple
#print axioms coefficient
#print axioms nextCarry
#print axioms emitted
#print axioms oneStep
#print axioms machineStep
#print axioms advance
#print axioms prefixRun
#print axioms coefficient_false
#print axioms coefficient_true
#print axioms machineStep_initial
#print axioms table_nonzero_of_local
#print axioms nextCarry_complete
#print axioms oneStep_valid
#print axioms oneStep_sound
#print axioms oneStep_coverage
#print axioms coefficient_ne_nine
#print axioms first_label_ne_nine
#print axioms second_label_ne_nine
#print axioms machineStep_coverage
#print axioms machineStep_sound
#print axioms machineStep_eq_some_iff
#print axioms advance_none
#print axioms prefixRun_nil
#print axioms prefixRun_cons
#print axioms prefixRun_none
#print axioms prefixRun_append

end P196.Agent3.PrefixContraction
