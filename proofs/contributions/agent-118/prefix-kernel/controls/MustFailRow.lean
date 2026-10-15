import Rank218
import PrefixChecksBase
-- EXPECTED TO FAIL: the stored row [1,0,13,5,4,8,6] has rank 6, so claiming rank 0 must be rejected.
namespace Agent118.MustFail
open SevenColumn.Certificate Agent118.PrefixKernel Agent118.Cert218
set_option maxRecDepth 100000
theorem bad_row : checkRow ranks (fastLongPred 7) [1,0,13,5,4,8,6] 0 = true := by decide +kernel
end Agent118.MustFail
