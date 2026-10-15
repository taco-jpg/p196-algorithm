import Rank218
import PrefixChecksBase
-- EXPECTED TO FAIL: a claimed initial bound of 32 for the chunk containing index 9988.
namespace Agent118.MustFail
open SevenColumn.Certificate Agent118.PrefixKernel Agent118.Cert218
set_option maxRecDepth 100000
theorem bad_initial : ∀ i : Fin 100, checkInitial ranks 32 (targetInitialWord 2 1 8 (9900 + i.val)) = true := by decide +kernel
end Agent118.MustFail
