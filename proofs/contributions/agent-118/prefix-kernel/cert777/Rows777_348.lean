import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2014 : checkRowsBlock ranks (fastLongPred 7) leaf2014 = true := by decide +kernel
theorem row_branch2014 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,0,13] 1 = true := by decide +kernel
theorem checked_leaf2015 : checkRowsBlock ranks (fastLongPred 7) leaf2015 = true := by decide +kernel
theorem row_branch2015 : checkRow ranks (fastLongPred 7) [8,0,3,10,14,15,16] 3 = true := by decide +kernel
theorem checked_leaf2016 : checkRowsBlock ranks (fastLongPred 7) leaf2016 = true := by decide +kernel
theorem row_branch2016 : checkRow ranks (fastLongPred 7) [8,0,3,10,14,10,3] 3 = true := by decide +kernel
theorem checked_leaf2017 : checkRowsBlock ranks (fastLongPred 7) leaf2017 = true := by decide +kernel
theorem row_branch2017 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,6,14] 3 = true := by decide +kernel
theorem checked_leaf2018 : checkRowsBlock ranks (fastLongPred 7) leaf2018 = true := by decide +kernel
theorem row_branch2018 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,14,8] 3 = true := by decide +kernel
theorem checked_leaf2019 : checkRowsBlock ranks (fastLongPred 7) leaf2019 = true := by decide +kernel
theorem row_branch2019 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,10,9] 3 = true := by decide +kernel
theorem checked_leaf2020 : checkRowsBlock ranks (fastLongPred 7) leaf2020 = true := by decide +kernel
theorem row_branch2020 : checkRow ranks (fastLongPred 7) [8,0,3,10,16,2,0] 0 = true := by decide +kernel
theorem checked_leaf2021 : checkRowsBlock ranks (fastLongPred 7) leaf2021 = true := by decide +kernel
theorem row_branch2021 : checkRow ranks (fastLongPred 7) [8,0,3,10,16,10,7] 3 = true := by decide +kernel
theorem checked_leaf2022 : checkRowsBlock ranks (fastLongPred 7) leaf2022 = true := by decide +kernel
theorem row_branch2022 : checkRow ranks (fastLongPred 7) [8,0,3,10,16,5,17] 1 = true := by decide +kernel
theorem checked_leaf2023 : checkRowsBlock ranks (fastLongPred 7) leaf2023 = true := by decide +kernel
theorem row_branch2023 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,16,15] 3 = true := by decide +kernel
theorem checked_leaf2024 : checkRowsBlock ranks (fastLongPred 7) leaf2024 = true := by decide +kernel
theorem row_branch2024 : checkRow ranks (fastLongPred 7) [8,0,3,10,15,4,11] 3 = true := by decide +kernel
end Agent118.Cert777
