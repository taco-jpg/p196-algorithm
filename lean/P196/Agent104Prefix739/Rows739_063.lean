import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0252 : leaf0252.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0253 : leaf0253.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0254 : leaf0254.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0255 : leaf0255.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0252 : checkRow ranks (fastLongPred 7) [3,2,13,13,0,11,14] 1 = true := by decide +kernel
theorem row_branch0253 : checkRow ranks (fastLongPred 7) [3,2,3,18,4,3,3] 1 = true := by decide +kernel
theorem row_branch0254 : checkRow ranks (fastLongPred 7) [1,16,0,5,5,16,6] 0 = true := by decide +kernel
theorem row_branch0255 : checkRow ranks (fastLongPred 7) [3,11,14,0,12,12,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
