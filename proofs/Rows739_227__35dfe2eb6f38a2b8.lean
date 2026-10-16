import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0908 : leaf0908.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0909 : leaf0909.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0910 : leaf0910.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0911 : leaf0911.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0908 : checkRow ranks (fastLongPred 7) [12,10,5,16,16,6,18] 6 = true := by decide +kernel
theorem row_branch0909 : checkRow ranks (fastLongPred 7) [12,10,5,16,18,5,0] 3 = true := by decide +kernel
theorem row_branch0910 : checkRow ranks (fastLongPred 7) [12,10,5,16,16,12,15] 3 = true := by decide +kernel
theorem row_branch0911 : checkRow ranks (fastLongPred 7) [12,10,5,16,18,18,8] 0 = true := by decide +kernel
end SevenColumn.Certificate739
