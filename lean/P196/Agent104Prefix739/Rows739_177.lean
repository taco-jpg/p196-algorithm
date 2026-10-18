import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0708 : leaf0708.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0709 : leaf0709.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0710 : leaf0710.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0711 : leaf0711.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0708 : checkRow ranks (fastLongPred 7) [7,4,8,11,18,8,13] 1 = true := by decide +kernel
theorem row_branch0709 : checkRow ranks (fastLongPred 7) [7,6,10,9,4,2,1] 2 = true := by decide +kernel
theorem row_branch0710 : checkRow ranks (fastLongPred 7) [7,4,8,15,18,6,1] 1 = true := by decide +kernel
theorem row_branch0711 : checkRow ranks (fastLongPred 7) [7,8,12,0,0,0,14] 0 = true := by decide +kernel
end SevenColumn.Certificate739
