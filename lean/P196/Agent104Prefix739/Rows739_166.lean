import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0664 : leaf0664.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0665 : leaf0665.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0666 : leaf0666.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0667 : leaf0667.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0664 : checkRow ranks (fastLongPred 7) [7,3,9,8,3,0,5] 2 = true := by decide +kernel
theorem row_branch0665 : checkRow ranks (fastLongPred 7) [7,3,9,8,2,4,8] 2 = true := by decide +kernel
theorem row_branch0666 : checkRow ranks (fastLongPred 7) [7,3,9,8,1,3,4] 2 = true := by decide +kernel
theorem row_branch0667 : checkRow ranks (fastLongPred 7) [7,3,9,7,9,0,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
