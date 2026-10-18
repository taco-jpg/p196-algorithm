import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0752 : leaf0752.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0753 : leaf0753.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0754 : leaf0754.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0755 : leaf0755.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0752 : checkRow ranks (fastLongPred 7) [11,7,14,13,13,16,12] 3 = true := by decide +kernel
theorem row_branch0753 : checkRow ranks (fastLongPred 7) [11,7,14,4,4,18,15] 3 = true := by decide +kernel
theorem row_branch0754 : checkRow ranks (fastLongPred 7) [11,16,5,11,11,5,13] 1 = true := by decide +kernel
theorem row_branch0755 : checkRow ranks (fastLongPred 7) [11,16,14,4,4,7,12] 1 = true := by decide +kernel
end SevenColumn.Certificate739
