import P196.Foundations.PeriodObstructions

/-!
Agent #2: index-level bridge to the repository's actual decimal normalizer.
`carryAt` records an actual prefix carry; it is not an extra interpreter premise.
The imported Agent8 transition remains the sole coefficient-word transition.
-/
namespace P196.Agent2.OverflowFibers

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

/-- Carry entering position `i`, starting with carry `e`. -/
def carryAt : List Nat → Nat → Nat → Nat
  | _, e, 0 => e
  | [], e, _ + 1 => e
  | x :: xs, e, i + 1 => carryAt xs ((x + e) / 10) i

@[simp] theorem carryAt_zero (q : List Nat) (e : Nat) : carryAt q e 0 = e := by
  cases q <;> rfl

theorem getElemBang_eq (q : List Nat) (i : Nat) (h : i < q.length) :
    q[i]! = q[i] := by
  rw [List.getElem!_eq_getElem?_getD, List.getElem?_eq_getElem h]
  rfl

theorem carryAt_succ (q : List Nat) (e i : Nat) (hi : i < q.length) :
    carryAt q e (i + 1) = (q[i]! + carryAt q e i) / 10 := by
  induction q generalizing e i with
  | nil => simp at hi
  | cons x xs ih =>
    cases i with
    | zero => simp [carryAt]
    | succ i =>
      simpa only [carryAt, List.getElem!_cons_succ] using
        ih ((x + e) / 10) i (by simpa using hi)

theorem carryAt_bound (q : List Nat) (e i : Nat) (he : e ≤ 1)
    (hq : ∀ x ∈ q, x ≤ 18) : carryAt q e i ≤ 1 := by
  induction q generalizing e i with
  | nil => cases i <;> exact he
  | cons x xs ih =>
    cases i with
    | zero => exact he
    | succ i =>
      apply ih ((x + e) / 10) i
      · have hx := hq x (by simp); omega
      · intro y hy; exact hq y (by simp [hy])

theorem normalize_length (q : List Nat) (e : Nat) :
    (Agent8.normalize q e).length =
      q.length + if carryAt q e q.length = 0 then 0 else 1 := by
  induction q generalizing e with
  | nil => simp only [Agent8.normalize, List.length_nil, carryAt]; split <;> simp
  | cons x xs ih =>
    simp only [Agent8.normalize, List.length_cons, ih, carryAt]
    omega

theorem normalize_getElemBang (q : List Nat) (e i : Nat) (hi : i < q.length) :
    (Agent8.normalize q e)[i]! = (q[i]! + carryAt q e i) % 10 := by
  induction q generalizing e i with
  | nil => simp at hi
  | cons x xs ih =>
    cases i with
    | zero => rfl
    | succ i =>
      simpa only [Agent8.normalize, carryAt, List.getElem!_cons_succ] using
        ih ((x + e) / 10) i (by simpa using hi)

theorem normalize_final_getElemBang (q : List Nat) (e : Nat) :
    (Agent8.normalize q e)[q.length]! = carryAt q e q.length := by
  induction q generalizing e with
  | nil =>
    simp only [Agent8.normalize, List.length_nil, carryAt]
    split <;> simp_all
    rfl
  | cons x xs ih =>
    simpa only [Agent8.normalize, List.length_cons, List.getElem!_cons_succ,
      carryAt] using ih ((x + e) / 10)

theorem reverse_getElemBang (q : List Nat) (i : Nat) (hi : i < q.length) :
    q.reverse[i]! = q[q.length - 1 - i]! := by
  simp only [List.getElem!_eq_getElem?_getD, List.getElem?_reverse hi]

theorem symmetric_getElemBang (q : List Nat) (hq : q.reverse = q)
    (i : Nat) (hi : i < q.length) : q[q.length - 1 - i]! = q[i]! := by
  rw [← reverse_getElemBang q i hi, hq]

theorem zipAdd_getElemBang (q r : List Nat) (i : Nat)
    (hi : i < q.length) (hj : i < r.length) :
    (Agent8.zipAdd q r)[i]! = q[i]! + r[i]! := by
  induction q generalizing r i with
  | nil => simp at hi
  | cons x xs ih =>
    cases r with
    | nil => simp at hj
    | cons y ys =>
      cases i with
      | zero => rfl
      | succ i =>
        simpa only [Agent8.zipAdd, List.getElem!_cons_succ] using
          ih ys i (by simpa using hi) (by simpa using hj)

theorem pair_getElemBang (q : List Nat) (i : Nat) (hi : i < q.length) :
    (Agent8.pair q)[i]! = q[i]! + q[q.length - 1 - i]! := by
  rw [Agent8.pair, zipAdd_getElemBang q q.reverse i hi (by simpa using hi),
    reverse_getElemBang q i hi]

/-- Canonical input conditions; an odd center is an even pair-sum coefficient. -/
def Canonical (q : List Nat) : Prop :=
  q.reverse = q ∧ (∀ x ∈ q, x ≤ 18) ∧ 0 < q.headD 0 ∧
    (q.length % 2 = 1 → q[q.length / 2]! % 2 = 0)

/-- The literal Agent8 fiber, restricted by its actual final carry. -/
def ActualOverflowFiber (L : Nat) (target q : List Nat) : Prop :=
  q.length = L ∧ Canonical q ∧ carryAt q 0 q.length = 1 ∧
    Agent8.stepWord q = target

theorem overflow_step_outer (q : List Nat) (hq : 0 < q.length)
    (hc : carryAt q 0 q.length = 1) :
    (Agent8.stepWord q)[0]! = q[0]! % 10 + 1 := by
  have hn : (Agent8.normalize q 0).length = q.length + 1 := by
    simp [normalize_length, hc]
  unfold Agent8.stepWord
  rw [pair_getElemBang _ 0 (by omega), hn]
  simp only [Nat.sub_zero, Nat.add_sub_cancel]
  rw [normalize_getElemBang q 0 0 hq, normalize_final_getElemBang, hc]
  simp

theorem overflow_step_inner (q : List Nat) (i : Nat)
    (h0 : 0 < i) (hi : i < q.length)
    (hc : carryAt q 0 q.length = 1) :
    (Agent8.stepWord q)[i]! =
      (q[i]! + carryAt q 0 i) % 10 +
      (q[q.length - i]! + carryAt q 0 (q.length - i)) % 10 := by
  have hn : (Agent8.normalize q 0).length = q.length + 1 := by
    simp [normalize_length, hc]
  unfold Agent8.stepWord
  rw [pair_getElemBang _ i (by omega), hn]
  simp only [Nat.add_sub_cancel]
  rw [normalize_getElemBang q 0 i hi,
    normalize_getElemBang q 0 (q.length - i) (by omega)]

#print axioms carryAt_zero
#print axioms getElemBang_eq
#print axioms carryAt_succ
#print axioms carryAt_bound
#print axioms normalize_length
#print axioms normalize_getElemBang
#print axioms normalize_final_getElemBang
#print axioms reverse_getElemBang
#print axioms symmetric_getElemBang
#print axioms zipAdd_getElemBang
#print axioms pair_getElemBang
#print axioms overflow_step_outer
#print axioms overflow_step_inner

end P196.Agent2.OverflowFibers
