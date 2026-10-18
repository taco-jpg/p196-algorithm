import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0692 : leaf0692.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0693 : leaf0693.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0694 : leaf0694.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0695 : leaf0695.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0692 : checkRow ranks (fastLongPred 7) [7,3,9,9,9,0,5] 2 = true := by decide +kernel
theorem row_branch0693 : checkRow ranks (fastLongPred 7) [7,3,9,9,8,4,8] 2 = true := by decide +kernel
theorem row_branch0694 : checkRow ranks (fastLongPred 7) [7,3,18,9,9,16,16] 2 = true := by decide +kernel
theorem row_branch0695 : checkRow ranks (fastLongPred 7) [7,4,2,5,0,1,4] 1 = true := by decide +kernel
end SevenColumn.Certificate739
