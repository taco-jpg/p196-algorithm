import Compat

/-!
# 正时间整数轨道与实际规范化字的回文等价

Agent #105 / lean_runtime，session 8f1107db019a。
将原 Agent109.Compat.isLychrel_iff 中的局部 `key` 抽出为可复用接口。
所有整数操作仍为原 Lychrel196 常量，所有列表操作仍为原 Agent8 常量；
通过原 Compat 的已证明相容性定理与 Agent109.step_palindrome_iff 连接。

在正整数时间 i，检查的是 pair-word 轨道时间 i-1 的规范化数字字。
这一定理不涵盖时间 0 的初值回文性，也不假定存在非回文返回或任何
Lychrel 初值。给定 hrep 的版本只替换已知的 pairWord 表示。
-/

namespace Agent105.IntegerSafety

/-- 原 Compat 局部等价的公开版本，适用于所有自然数初值。 -/
theorem palindrome_orbit_succ_iff (n k : Nat) :
    Lychrel196.Palindrome (Lychrel196.orbit n (k + 1)) ↔
      (Agent8.normalize (Agent8.orbit (Agent109.pairWord n) k) 0).reverse =
        Agent8.normalize (Agent8.orbit (Agent109.pairWord n) k) 0 := by
  rw [Agent109.Compat.palindrome_eq, Agent109.Compat.orbit_eq,
    Agent109.orbit, Agent109.step_palindrome_iff, Agent109.pairWord_orbit,
    Agent109.Compat.orbit_word_eq, Agent109.Compat.normalize_eq]

/-- 在实际正时间 i，将整数回文性精确改写为时间 i-1 的规范化字回文性。 -/
theorem palindrome_orbit_positive_iff (n i : Nat) (hi : 1 ≤ i) :
    Lychrel196.Palindrome (Lychrel196.orbit n i) ↔
      (Agent8.normalize (Agent8.orbit (Agent109.pairWord n) (i - 1)) 0).reverse =
        Agent8.normalize (Agent8.orbit (Agent109.pairWord n) (i - 1)) 0 := by
  have htime : i - 1 + 1 = i := by omega
  simpa only [htime] using palindrome_orbit_succ_iff n (i - 1)

/-- 给定实际 pairWord 表示后，正时间整数回文性可直接用该列表轨道检验。 -/
theorem palindrome_orbit_positive_iff_of_pairWord (n i : Nat) (w : Agent8.Word)
    (hi : 1 ≤ i) (hrep : Agent109.pairWord n = w) :
    Lychrel196.Palindrome (Lychrel196.orbit n i) ↔
      (Agent8.normalize (Agent8.orbit w (i - 1)) 0).reverse =
        Agent8.normalize (Agent8.orbit w (i - 1)) 0 := by
  rw [palindrome_orbit_positive_iff n i hi, hrep]

/-- 同一真实表示下，正时间避回文性与规范化字不等于其反转精确等价。 -/
theorem nonpalindrome_orbit_positive_iff_of_pairWord (n i : Nat) (w : Agent8.Word)
    (hi : 1 ≤ i) (hrep : Agent109.pairWord n = w) :
    (¬ Lychrel196.Palindrome (Lychrel196.orbit n i)) ↔
      (Agent8.normalize (Agent8.orbit w (i - 1)) 0).reverse ≠
        Agent8.normalize (Agent8.orbit w (i - 1)) 0 := by
  exact not_congr (palindrome_orbit_positive_iff_of_pairWord n i w hi hrep)

end Agent105.IntegerSafety

#print axioms Agent105.IntegerSafety.palindrome_orbit_succ_iff
#print axioms Agent105.IntegerSafety.palindrome_orbit_positive_iff
#print axioms Agent105.IntegerSafety.palindrome_orbit_positive_iff_of_pairWord
#print axioms Agent105.IntegerSafety.nonpalindrome_orbit_positive_iff_of_pairWord
