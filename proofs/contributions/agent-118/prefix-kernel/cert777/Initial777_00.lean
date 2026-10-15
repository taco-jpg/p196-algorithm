import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem initial_000 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (0 + i.val)) = true := by decide +kernel
theorem initial_001 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (100 + i.val)) = true := by decide +kernel
theorem initial_002 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (200 + i.val)) = true := by decide +kernel
theorem initial_003 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (300 + i.val)) = true := by decide +kernel
theorem initial_004 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (400 + i.val)) = true := by decide +kernel
theorem initial_005 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (500 + i.val)) = true := by decide +kernel
theorem initial_006 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (600 + i.val)) = true := by decide +kernel
theorem initial_007 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (700 + i.val)) = true := by decide +kernel
theorem initial_008 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (800 + i.val)) = true := by decide +kernel
theorem initial_009 : ∀ i : Fin 100, checkInitial ranks 24 (targetInitialWord 7 7 7 (900 + i.val)) = true := by decide +kernel
end Agent118.Cert777
