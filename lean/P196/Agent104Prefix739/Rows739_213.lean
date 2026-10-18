import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0852 : leaf0852.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0853 : leaf0853.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0854 : leaf0854.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0855 : leaf0855.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0852 : checkRow ranks (fastLongPred 7) [12,9,1,7,4,16,17] 3 = true := by decide +kernel
theorem row_branch0853 : checkRow ranks (fastLongPred 7) [12,9,1,7,4,8,11] 3 = true := by decide +kernel
theorem row_branch0854 : checkRow ranks (fastLongPred 7) [12,9,1,7,7,10,4] 2 = true := by decide +kernel
theorem row_branch0855 : checkRow ranks (fastLongPred 7) [12,9,1,7,13,17,4] 3 = true := by decide +kernel
end SevenColumn.Certificate739
