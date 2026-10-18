import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0936 : leaf0936.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0937 : leaf0937.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0938 : leaf0938.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0939 : leaf0939.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0936 : checkRow ranks (fastLongPred 7) [12,10,14,16,16,13,7] 3 = true := by decide +kernel
theorem row_branch0937 : checkRow ranks (fastLongPred 7) [12,10,14,16,16,2,2] 3 = true := by decide +kernel
theorem row_branch0938 : checkRow ranks (fastLongPred 7) [12,10,14,14,13,15,17] 2 = true := by decide +kernel
theorem row_branch0939 : checkRow ranks (fastLongPred 7) [12,10,14,16,18,18,17] 3 = true := by decide +kernel
end SevenColumn.Certificate739
