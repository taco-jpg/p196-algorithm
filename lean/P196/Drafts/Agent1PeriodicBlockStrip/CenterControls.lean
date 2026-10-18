import P196.Foundations.Agent1PeriodicCenterStrip

namespace Agent1.CenterStripAuthorControls
open Agent1.Periodic

theorem empty_period : stripPeriodCenter [] [1, 2, 3] = ([1, 2, 3], 0) := by decide

theorem empty_center : stripPeriodCenter [1, 2] [] = ([], 0) := by decide

theorem two_nonsymmetric_periods :
    stripPeriodCenter [1, 2] [1, 2, 1, 2, 9, 2, 1, 2, 1] = ([9], 2) := by decide

theorem overlapping_ends_are_not_removed :
    stripPeriodCenter [1, 1] [1, 1, 1] = ([1, 1, 1], 0) := by decide

theorem unreversed_suffix_is_not_removed :
    stripPeriodCenter [1, 2] [1, 2, 3, 1, 2] = ([1, 2, 3, 1, 2], 0) := by decide

theorem full_pair_leaves_empty_center :
    stripPeriodCenter [1, 2] [1, 2, 2, 1] = ([], 1) := by decide

end Agent1.CenterStripAuthorControls

#print axioms Agent1.CenterStripAuthorControls.empty_period
#print axioms Agent1.CenterStripAuthorControls.empty_center
#print axioms Agent1.CenterStripAuthorControls.two_nonsymmetric_periods
#print axioms Agent1.CenterStripAuthorControls.overlapping_ends_are_not_removed
#print axioms Agent1.CenterStripAuthorControls.unreversed_suffix_is_not_removed
#print axioms Agent1.CenterStripAuthorControls.full_pair_leaves_empty_center
