import Agent102ParameterIntervalDefs

/-!
Agent #102：自然数参数区间的集合运算规格。
所有结论允许空区间、倒置的有限区间以及无穷上端点。
-/

namespace Agent102.ParameterSets

@[simp] theorem Interval.contains_empty (k : Nat) :
    Interval.empty.Contains k ↔ False := by
  simp [Interval.Contains, Interval.empty]

@[simp] theorem Interval.contains_univ (k : Nat) :
    Interval.univ.Contains k ↔ True := by
  simp [Interval.Contains, Interval.univ]

@[simp] theorem Interval.contains_inter (I J : Interval) (k : Nat) :
    (I.inter J).Contains k ↔ I.Contains k ∧ J.Contains k := by
  rcases I with ⟨a, u⟩
  rcases J with ⟨b, v⟩
  cases u <;> cases v <;>
    simp [Interval.inter, Interval.Contains, Nat.max_le, Nat.lt_min,
      and_assoc, and_left_comm, and_comm]

@[simp] theorem holds_empty (k : Nat) : holds empty k ↔ False := by
  simp [holds, empty]

@[simp] theorem holds_univ (k : Nat) : holds univ k ↔ True := by
  simp [holds, univ]

@[simp] theorem holds_cons (I : Interval) (R : Region) (k : Nat) :
    holds (I :: R) k ↔ I.Contains k ∨ holds R k := by
  simp [holds]

@[simp] theorem holds_union (R S : Region) (k : Nat) :
    holds (union R S) k ↔ holds R k ∨ holds S k := by
  simp [holds, union, or_and_right, exists_or]

@[simp] theorem holds_inter (R S : Region) (k : Nat) :
    holds (inter R S) k ↔ holds R k ∧ holds S k := by
  constructor
  · rintro ⟨K, hK, hk⟩
    obtain ⟨I, hI, hK⟩ := List.mem_flatMap.mp hK
    obtain ⟨J, hJ, rfl⟩ := List.mem_map.mp hK
    obtain ⟨hi, hj⟩ := (Interval.contains_inter I J k).mp hk
    exact ⟨⟨I, hI, hi⟩, ⟨J, hJ, hj⟩⟩
  · rintro ⟨⟨I, hI, hi⟩, ⟨J, hJ, hj⟩⟩
    exact ⟨I.inter J,
      List.mem_flatMap.mpr ⟨I, hI, List.mem_map.mpr ⟨J, hJ, rfl⟩⟩,
      (Interval.contains_inter I J k).mpr ⟨hi, hj⟩⟩

@[simp] theorem holds_interval_complement (I : Interval) (k : Nat) :
    holds I.complement k ↔ ¬I.Contains k := by
  rcases I with ⟨a, u⟩
  cases u <;> simp [holds, Interval.complement, Interval.Contains] <;> omega

@[simp] theorem holds_complement (R : Region) (k : Nat) :
    holds (complement R) k ↔ ¬holds R k := by
  induction R with
  | nil =>
    change holds univ k ↔ ¬holds empty k
    simp
  | cons I R ih =>
    change holds (inter I.complement (complement R)) k ↔ ¬holds (I :: R) k
    simp only [holds_inter, holds_interval_complement, ih, holds_cons, not_or]

@[simp] theorem holds_unionAll (Rs : List Region) (k : Nat) :
    holds (unionAll Rs) k ↔ ∃ R ∈ Rs, holds R k := by
  constructor
  · rintro ⟨I, hI, hk⟩
    obtain ⟨R, hR, hI⟩ := List.mem_flatten.mp hI
    exact ⟨R, hR, I, hI, hk⟩
  · rintro ⟨R, hR, I, hI, hk⟩
    exact ⟨I, List.mem_flatten.mpr ⟨R, hR, hI⟩, hk⟩

@[simp] theorem holds_interAll (Rs : List Region) (k : Nat) :
    holds (interAll Rs) k ↔ ∀ R ∈ Rs, holds R k := by
  induction Rs with
  | nil => simp [interAll]
  | cons R Rs ih =>
    change holds (inter R (interAll Rs)) k ↔ ∀ S ∈ R :: Rs, holds S k
    simp only [holds_inter, ih, List.mem_cons, forall_eq_or_imp]

theorem test_eq_true_iff (R : Region) (k : Nat) :
    test R k = true ↔ holds R k := by
  simp only [test, List.any_eq_true, decide_eq_true_eq, holds]

theorem inhabited_eq_true_iff (R : Region) :
    inhabited R = true ↔ ∃ k, holds R k := by
  rw [inhabited, List.any_eq_true]
  constructor
  · rintro ⟨I, hI, h⟩
    refine ⟨I.lo, I, hI, ?_⟩
    rcases I with ⟨a, u⟩
    cases u <;> simp_all [Interval.Contains]
  · rintro ⟨k, I, hI, h⟩
    refine ⟨I, hI, ?_⟩
    rcases I with ⟨a, u⟩
    cases u <;> simp_all [Interval.Contains] <;> omega

end Agent102.ParameterSets
