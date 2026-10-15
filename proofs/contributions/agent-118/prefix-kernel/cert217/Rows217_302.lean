import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2002 : checkRowsBlock ranks (fastLongPred 7) leaf2002 = true := by decide +kernel
theorem row_branch2002 : checkRow ranks (fastLongPred 7) [5,17,5,10,1,10,13] 2 = true := by decide +kernel
theorem checked_leaf2003 : checkRowsBlock ranks (fastLongPred 7) leaf2003 = true := by decide +kernel
theorem row_branch2003 : checkRow ranks (fastLongPred 7) [5,17,5,10,0,15,18] 2 = true := by decide +kernel
theorem checked_leaf2004 : checkRowsBlock ranks (fastLongPred 7) leaf2004 = true := by decide +kernel
theorem row_branch2004 : checkRow ranks (fastLongPred 7) [5,17,5,10,1,18,5] 2 = true := by decide +kernel
theorem checked_leaf2005 : checkRowsBlock ranks (fastLongPred 7) leaf2005 = true := by decide +kernel
theorem row_branch2005 : checkRow ranks (fastLongPred 7) [5,17,5,10,2,17,10] 2 = true := by decide +kernel
theorem checked_leaf2006 : checkRowsBlock ranks (fastLongPred 7) leaf2006 = true := by decide +kernel
theorem row_branch2006 : checkRow ranks (fastLongPred 7) [5,17,5,10,2,13,1] 1 = true := by decide +kernel
theorem checked_leaf2007 : checkRowsBlock ranks (fastLongPred 7) leaf2007 = true := by decide +kernel
theorem row_branch2007 : checkRow ranks (fastLongPred 7) [5,17,5,10,1,14,12] 2 = true := by decide +kernel
end Agent118.Cert217
