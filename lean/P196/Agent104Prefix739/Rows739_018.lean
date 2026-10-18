import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0072 : leaf0072.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0073 : leaf0073.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0074 : leaf0074.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0075 : leaf0075.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0072 : checkRow ranks (fastLongPred 7) [1,15,16,9,14,16,1] 0 = true := by decide +kernel
theorem row_branch0073 : checkRow ranks (fastLongPred 7) [1,15,16,9,16,4,12] 0 = true := by decide +kernel
theorem row_branch0074 : checkRow ranks (fastLongPred 7) [1,15,16,10,0,1,7] 0 = true := by decide +kernel
theorem row_branch0075 : checkRow ranks (fastLongPred 7) [1,15,16,9,16,11,5] 0 = true := by decide +kernel
end SevenColumn.Certificate739
