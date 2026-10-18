import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0988 : leaf0988.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0989 : leaf0989.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0990 : leaf0990.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0991 : leaf0991.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0988 : checkRow ranks (fastLongPred 7) [14,13,9,18,18,13,11] 1 = true := by decide +kernel
theorem row_branch0989 : checkRow ranks (fastLongPred 7) [14,13,0,18,18,4,3] 0 = true := by decide +kernel
theorem row_branch0990 : checkRow ranks (fastLongPred 7) [14,17,4,1,4,17,12] 3 = true := by decide +kernel
theorem row_branch0991 : checkRow ranks (fastLongPred 7) [14,17,4,10,4,16,11] 3 = true := by decide +kernel
end SevenColumn.Certificate739
