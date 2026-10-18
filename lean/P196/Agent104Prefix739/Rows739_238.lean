import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0952 : leaf0952.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0953 : leaf0953.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0954 : leaf0954.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0955 : leaf0955.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0952 : checkRow ranks (fastLongPred 7) [12,17,6,12,1,11,9] 9 = true := by decide +kernel
theorem row_branch0953 : checkRow ranks (fastLongPred 7) [12,17,6,3,10,9,13] 3 = true := by decide +kernel
theorem row_branch0954 : checkRow ranks (fastLongPred 7) [12,10,14,16,18,14,5] 3 = true := by decide +kernel
theorem row_branch0955 : checkRow ranks (fastLongPred 7) [12,10,14,7,16,0,18] 0 = true := by decide +kernel
end SevenColumn.Certificate739
