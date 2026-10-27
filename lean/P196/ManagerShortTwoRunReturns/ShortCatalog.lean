import P196.ManagerShortTwoRunReturns.CycleRefinement

/-!
Exact correlated catalogs, checked one column at a time. Each displayed row
list includes its repeated terminal phase. Full temporal rows are retained,
so existential boundary carries cannot be mixed across different phases.
The final empty catalogs use ordinary kernel reduction, not native_decide.
-/

namespace P196.ManagerShortTwoRun
set_option maxRecDepth 100000
set_option maxHeartbeats 5000000

/-- P=7, width gain2, 1 columns: 7 correlated traces. -/
def catalog7_1 : List Rows :=
  [[[1], [2], [5], [11], [2], [5], [10], [1]], [[2], [5], [10], [1], [2], [5], [11], [2]], [[2], [5], [11], [2], [5], [10], [1], [2]], [[5], [10], [1], [2], [5], [11], [2], [5]], [[5], [11], [2], [5], [10], [1], [2], [5]], [[10], [1], [2], [5], [11], [2], [5], [10]], [[11], [2], [5], [10], [1], [2], [5], [11]]]

theorem checked_catalog7_1 : candidates 7 2 1 = catalog7_1 := by
  decide +kernel

/-- P=7, width gain2, 2 columns: 0 correlated traces. -/
def catalog7_2 : List Rows :=
  []

theorem checked_catalog7_2 : candidates 7 2 2 = catalog7_2 := by
  rw [candidates, checked_catalog7_1]
  decide +kernel

/-- P=6, width gain2, 1 columns: 12 correlated traces. -/
def catalog6_1 : List Rows :=
  [[[1], [3], [7], [14], [5], [10], [1]], [[2], [5], [11], [2], [5], [11], [2]], [[3], [6], [12], [3], [6], [12], [3]], [[3], [7], [14], [5], [10], [1], [3]], [[5], [10], [1], [3], [7], [14], [5]], [[5], [11], [2], [5], [11], [2], [5]], [[6], [12], [3], [6], [12], [3], [6]], [[7], [14], [5], [10], [1], [3], [7]], [[10], [1], [3], [7], [14], [5], [10]], [[11], [2], [5], [11], [2], [5], [11]], [[12], [3], [6], [12], [3], [6], [12]], [[14], [5], [10], [1], [3], [7], [14]]]

theorem checked_catalog6_1 : candidates 6 2 1 = catalog6_1 := by
  decide +kernel

/-- P=6, width gain2, 2 columns: 3 correlated traces. -/
def catalog6_2 : List Rows :=
  [[[3, 2], [6, 4], [12, 9], [3, 2], [6, 4], [12, 9], [3, 2]], [[6, 4], [12, 9], [3, 2], [6, 4], [12, 9], [3, 2], [6, 4]], [[12, 9], [3, 2], [6, 4], [12, 9], [3, 2], [6, 4], [12, 9]]]

theorem checked_catalog6_2 : candidates 6 2 2 = catalog6_2 := by
  rw [candidates, checked_catalog6_1]
  decide +kernel

/-- P=6, width gain2, 3 columns: 0 correlated traces. -/
def catalog6_3 : List Rows :=
  []

theorem checked_catalog6_3 : candidates 6 2 3 = catalog6_3 := by
  rw [candidates, checked_catalog6_2]
  decide +kernel

/-- P=5, width gain2, 1 columns: 10 correlated traces. -/
def catalog5_1 : List Rows :=
  [[[1], [2], [4], [9], [10], [1]], [[2], [4], [9], [10], [1], [2]], [[3], [7], [15], [6], [12], [3]], [[4], [9], [10], [1], [2], [4]], [[6], [12], [3], [7], [15], [6]], [[7], [15], [6], [12], [3], [7]], [[9], [10], [1], [2], [4], [9]], [[10], [1], [2], [4], [9], [10]], [[12], [3], [7], [15], [6], [12]], [[15], [6], [12], [3], [7], [15]]]

theorem checked_catalog5_1 : candidates 5 2 1 = catalog5_1 := by
  decide +kernel

/-- P=5, width gain2, 2 columns: 5 correlated traces. -/
def catalog5_2 : List Rows :=
  [[[1, 4], [2, 8], [4, 16], [9, 13], [10, 3], [1, 4]], [[2, 8], [4, 16], [9, 13], [10, 3], [1, 4], [2, 8]], [[4, 16], [9, 13], [10, 3], [1, 4], [2, 8], [4, 16]], [[9, 13], [10, 3], [1, 4], [2, 8], [4, 16], [9, 13]], [[10, 3], [1, 4], [2, 8], [4, 16], [9, 13], [10, 3]]]

theorem checked_catalog5_2 : candidates 5 2 2 = catalog5_2 := by
  rw [candidates, checked_catalog5_1]
  decide +kernel

/-- P=5, width gain2, 3 columns: 5 correlated traces. -/
def catalog5_3 : List Rows :=
  [[[1, 4, 4], [2, 8, 8], [4, 16, 17], [9, 13, 15], [10, 3, 10], [1, 4, 4]], [[2, 8, 8], [4, 16, 17], [9, 13, 15], [10, 3, 10], [1, 4, 4], [2, 8, 8]], [[4, 16, 17], [9, 13, 15], [10, 3, 10], [1, 4, 4], [2, 8, 8], [4, 16, 17]], [[9, 13, 15], [10, 3, 10], [1, 4, 4], [2, 8, 8], [4, 16, 17], [9, 13, 15]], [[10, 3, 10], [1, 4, 4], [2, 8, 8], [4, 16, 17], [9, 13, 15], [10, 3, 10]]]

theorem checked_catalog5_3 : candidates 5 2 3 = catalog5_3 := by
  rw [candidates, checked_catalog5_2]
  decide +kernel

/-- P=5, width gain2, 4 columns: 20 correlated traces. -/
def catalog5_4 : List Rows :=
  [[[1, 4, 4, 5], [2, 8, 8, 11], [4, 16, 17, 3], [9, 13, 15, 7], [10, 3, 10, 13], [1, 4, 4, 5]], [[1, 4, 4, 6], [2, 8, 8, 12], [4, 16, 17, 4], [9, 13, 15, 9], [10, 3, 10, 5], [1, 4, 4, 6]], [[1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 8], [9, 13, 15, 18], [10, 3, 10, 15], [1, 4, 4, 7]], [[1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 9], [9, 13, 15, 9], [10, 3, 10, 6], [1, 4, 4, 7]], [[2, 8, 8, 11], [4, 16, 17, 3], [9, 13, 15, 7], [10, 3, 10, 13], [1, 4, 4, 5], [2, 8, 8, 11]], [[2, 8, 8, 12], [4, 16, 17, 4], [9, 13, 15, 9], [10, 3, 10, 5], [1, 4, 4, 6], [2, 8, 8, 12]], [[2, 8, 8, 14], [4, 16, 17, 8], [9, 13, 15, 18], [10, 3, 10, 15], [1, 4, 4, 7], [2, 8, 8, 14]], [[2, 8, 8, 14], [4, 16, 17, 9], [9, 13, 15, 9], [10, 3, 10, 6], [1, 4, 4, 7], [2, 8, 8, 14]], [[4, 16, 17, 3], [9, 13, 15, 7], [10, 3, 10, 13], [1, 4, 4, 5], [2, 8, 8, 11], [4, 16, 17, 3]], [[4, 16, 17, 4], [9, 13, 15, 9], [10, 3, 10, 5], [1, 4, 4, 6], [2, 8, 8, 12], [4, 16, 17, 4]], [[4, 16, 17, 8], [9, 13, 15, 18], [10, 3, 10, 15], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 8]], [[4, 16, 17, 9], [9, 13, 15, 9], [10, 3, 10, 6], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 9]], [[9, 13, 15, 7], [10, 3, 10, 13], [1, 4, 4, 5], [2, 8, 8, 11], [4, 16, 17, 3], [9, 13, 15, 7]], [[9, 13, 15, 9], [10, 3, 10, 5], [1, 4, 4, 6], [2, 8, 8, 12], [4, 16, 17, 4], [9, 13, 15, 9]], [[9, 13, 15, 9], [10, 3, 10, 6], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 9], [9, 13, 15, 9]], [[9, 13, 15, 18], [10, 3, 10, 15], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 8], [9, 13, 15, 18]], [[10, 3, 10, 5], [1, 4, 4, 6], [2, 8, 8, 12], [4, 16, 17, 4], [9, 13, 15, 9], [10, 3, 10, 5]], [[10, 3, 10, 6], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 9], [9, 13, 15, 9], [10, 3, 10, 6]], [[10, 3, 10, 13], [1, 4, 4, 5], [2, 8, 8, 11], [4, 16, 17, 3], [9, 13, 15, 7], [10, 3, 10, 13]], [[10, 3, 10, 15], [1, 4, 4, 7], [2, 8, 8, 14], [4, 16, 17, 8], [9, 13, 15, 18], [10, 3, 10, 15]]]

theorem checked_catalog5_4 : candidates 5 2 4 = catalog5_4 := by
  rw [candidates, checked_catalog5_3]
  decide +kernel

/-- P=5, width gain2, 5 columns: 0 correlated traces. -/
def catalog5_5 : List Rows :=
  []

theorem checked_catalog5_5 : candidates 5 2 5 = catalog5_5 := by
  rw [candidates, checked_catalog5_4]
  decide +kernel

theorem no_p7_g2_two_columns : candidates 7 2 2 = [] := checked_catalog7_2

theorem no_p6_g2_three_columns : candidates 6 2 3 = [] := checked_catalog6_3

theorem no_p5_g2_five_columns : candidates 5 2 5 = [] := checked_catalog5_5

#print axioms no_p7_g2_two_columns
#print axioms no_p6_g2_three_columns
#print axioms no_p5_g2_five_columns
end P196.ManagerShortTwoRun
