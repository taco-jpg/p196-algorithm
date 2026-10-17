import P196.Agent102AffineParameterIntervals.Agent102ParameterIntervalAlgebra

/-!
Agent #102：在每次区间交之后删除空区间。
本模块保持原集合语义，不要求排序，也不声称输出最小。
-/

namespace Agent102.ParameterSets

def prune (R : Region) : Region :=
  R.filter (fun I => inhabited [I])

def fastInter (R S : Region) : Region :=
  prune (inter R S)

def fastComplement (R : Region) : Region :=
  (prune R).foldr (fun I acc => fastInter (prune I.complement) acc) univ

def fastInterAll (Rs : List Region) : Region :=
  Rs.foldr fastInter univ

theorem Interval.inhabited_singleton_of_contains {I : Interval} {k : Nat}
    (h : I.Contains k) : inhabited [I] = true := by
  apply (inhabited_eq_true_iff [I]).mpr
  exact ⟨k, I, by simp, h⟩

@[simp] theorem holds_prune (R : Region) (k : Nat) :
    holds (prune R) k ↔ holds R k := by
  constructor
  · rintro ⟨I, hI, h⟩
    exact ⟨I, (List.mem_filter.mp hI).1, h⟩
  · rintro ⟨I, hI, h⟩
    exact ⟨I, List.mem_filter.mpr
      ⟨hI, Interval.inhabited_singleton_of_contains h⟩, h⟩

@[simp] theorem holds_fastInter (R S : Region) (k : Nat) :
    holds (fastInter R S) k ↔ holds R k ∧ holds S k := by
  simp only [fastInter, holds_prune, holds_inter]

@[simp] theorem holds_fastComplement (R : Region) (k : Nat) :
    holds (fastComplement R) k ↔ ¬holds R k := by
  have hfold (T : Region) :
      holds (T.foldr (fun I acc => fastInter (prune I.complement) acc) univ) k ↔
        ¬holds T k := by
    induction T with
    | nil =>
      change holds univ k ↔ ¬holds empty k
      simp
    | cons I T ih =>
      simp only [List.foldr_cons, holds_fastInter, holds_prune,
        holds_interval_complement, ih, holds_cons, not_or]
  simpa only [fastComplement, holds_prune] using hfold (prune R)

@[simp] theorem holds_fastInterAll (Rs : List Region) (k : Nat) :
    holds (fastInterAll Rs) k ↔ ∀ R ∈ Rs, holds R k := by
  induction Rs with
  | nil => simp [fastInterAll]
  | cons R Rs ih =>
    change holds (fastInter R (fastInterAll Rs)) k ↔
      ∀ S ∈ R :: Rs, holds S k
    simp only [holds_fastInter, ih, List.mem_cons, forall_eq_or_imp]

end Agent102.ParameterSets
