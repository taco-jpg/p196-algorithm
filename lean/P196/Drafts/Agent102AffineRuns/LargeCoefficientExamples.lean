import P196.Agent102AffineRuns.Agent102AffineDecision

/-!
独立检查的具体内核归约证书。H=10^100；所有例子只调用快速布尔判定。
这些有限证书不宣称算法复杂度定理，也不构造展开词。
-/
namespace Agent102.DecisionIndependentExamples

def H : Int := 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def one : List RunSpec := [⟨1, ⟨H, H⟩⟩]
def merged : List RunSpec := [⟨1, ⟨2 * H, 2 * H⟩⟩]
def splitWithZero : List RunSpec :=
  [⟨1, ⟨H, H⟩⟩, ⟨7, ⟨0, 0⟩⟩, ⟨1, ⟨H, H⟩⟩]
def negativeClipped : List RunSpec :=
  [⟨7, ⟨-H, H⟩⟩, ⟨8, ⟨0, -H⟩⟩, ⟨1, ⟨H, H⟩⟩]
def widthChanged : List RunSpec := [⟨1, ⟨H, H + 1⟩⟩]
def digitChanged : List RunSpec := [⟨2, ⟨H, H⟩⟩]
def symmetric : List RunSpec :=
  [⟨1, ⟨H, H⟩⟩, ⟨2, ⟨H, -H⟩⟩, ⟨1, ⟨H, H⟩⟩]
def asymmetric : List RunSpec := [⟨1, ⟨H, H⟩⟩, ⟨2, ⟨H, H⟩⟩]

theorem huge_split_equal : fastEqualOnTail splitWithZero merged = true := by decide

theorem huge_negative_lengths_clipped : fastEqualOnTail negativeClipped one = true := by decide

theorem huge_width_difference : fastEqualOnTail one widthChanged = false := by decide

theorem huge_digit_difference : fastEqualOnTail one digitChanged = false := by decide

theorem huge_palindrome : fastPalindromicOnTail symmetric = true := by decide

theorem huge_nonpalindrome : fastPalindromicOnTail asymmetric = false := by decide

#print axioms huge_split_equal
#print axioms huge_negative_lengths_clipped
#print axioms huge_width_difference
#print axioms huge_digit_difference
#print axioms huge_palindrome
#print axioms huge_nonpalindrome

end Agent102.DecisionIndependentExamples
