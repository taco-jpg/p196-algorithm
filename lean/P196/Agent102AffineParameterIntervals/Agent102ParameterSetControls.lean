import P196.Agent102AffineParameterIntervals.Agent102ParameterSetDecisions

/-!
Agent #102, genuine independent reviewer /root/research_map.
The ten expected sets were fixed in the independent literal-word controls
before candidate solver output was available. These certificates compare
whole represented parameter sets; no list order or disjointness is assumed.
The earlier Python point controls remain separate finite evidence.
-/

namespace Agent102.ParameterSetControls

open Agent102.ParameterSets

set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

def huge : Nat := 10 ^ 100

def twoIsolatedLeft : List RunSpec := [⟨7, ⟨1, -2⟩⟩, ⟨7, ⟨-1, 2⟩⟩]
def twoIsolatedRight : List RunSpec := [⟨7, ⟨0, 1⟩⟩]
def twoIsolatedExpected : Region := [⟨1, some 2⟩, ⟨3, some 4⟩]

theorem twoIsolated_certificate :
    equivalentRegions (equalityRegions twoIsolatedLeft twoIsolatedRight)
      twoIsolatedExpected = true := by decide

theorem twoIsolated_exact (k : Nat) :
    wordAt twoIsolatedLeft k = wordAt twoIsolatedRight k ↔ k = 1 ∨ k = 3 := by
  calc
    _ ↔ holds twoIsolatedExpected k :=
      (holds_equalityRegions twoIsolatedLeft twoIsolatedRight k).symm.trans
        ((equivalentRegions_spec _ _).mp twoIsolated_certificate k)
    _ ↔ _ := by simp [twoIsolatedExpected, holds, Interval.Contains] <;> omega

def boundedEmptyLeft : List RunSpec := [⟨4, ⟨-1, 2⟩⟩, ⟨4, ⟨1, -4⟩⟩]
def boundedEmptyRight : List RunSpec := []
def boundedEmptyExpected : Region := [⟨2, some 5⟩]

theorem boundedEmpty_certificate :
    equivalentRegions (equalityRegions boundedEmptyLeft boundedEmptyRight)
      boundedEmptyExpected = true := by decide

theorem boundedEmpty_exact (k : Nat) :
    wordAt boundedEmptyLeft k = wordAt boundedEmptyRight k ↔ 2 ≤ k ∧ k < 5 := by
  calc
    _ ↔ holds boundedEmptyExpected k :=
      (holds_equalityRegions boundedEmptyLeft boundedEmptyRight k).symm.trans
        ((equivalentRegions_spec _ _).mp boundedEmpty_certificate k)
    _ ↔ _ := by simp [boundedEmptyExpected, holds, Interval.Contains]

def middleHoleLeft : List RunSpec := [⟨5, ⟨1, -2⟩⟩, ⟨5, ⟨1, -6⟩⟩]
def middleHoleRight : List RunSpec := [⟨5, ⟨2, -8⟩⟩]
def middleHoleExpected : Region := [⟨0, some 3⟩, ⟨6, none⟩]

theorem middleHole_certificate :
    equivalentRegions (equalityRegions middleHoleLeft middleHoleRight)
      middleHoleExpected = true := by decide

theorem middleHole_exact (k : Nat) :
    wordAt middleHoleLeft k = wordAt middleHoleRight k ↔ k < 3 ∨ 6 ≤ k := by
  calc
    _ ↔ holds middleHoleExpected k :=
      (holds_equalityRegions middleHoleLeft middleHoleRight k).symm.trans
        ((equivalentRegions_spec _ _).mp middleHole_certificate k)
    _ ↔ _ := by simp [middleHoleExpected, holds, Interval.Contains]

def interiorZeroLeft : List RunSpec :=
  [⟨1, ⟨0, 1⟩⟩, ⟨7, ⟨-1, 2⟩⟩, ⟨1, ⟨0, 1⟩⟩]
def interiorZeroRight : List RunSpec := [⟨1, ⟨-1, 4⟩⟩]
def interiorZeroExpected : Region := [⟨2, some 3⟩]

theorem interiorZero_certificate :
    equivalentRegions (equalityRegions interiorZeroLeft interiorZeroRight)
      interiorZeroExpected = true := by decide

theorem interiorZero_exact (k : Nat) :
    wordAt interiorZeroLeft k = wordAt interiorZeroRight k ↔ k = 2 := by
  calc
    _ ↔ holds interiorZeroExpected k :=
      (holds_equalityRegions interiorZeroLeft interiorZeroRight k).symm.trans
        ((equivalentRegions_spec _ _).mp interiorZero_certificate k)
    _ ↔ _ := by simp [interiorZeroExpected, holds, Interval.Contains] <;> omega

def clippedSumLeft : List RunSpec := [⟨6, ⟨1, 0⟩⟩, ⟨6, ⟨-1, 2⟩⟩]
def clippedSumRight : List RunSpec := [⟨6, ⟨0, 2⟩⟩, ⟨6, ⟨1, -2⟩⟩]
def clippedSumExpected : Region := [⟨0, none⟩]

theorem clippedSum_certificate :
    equivalentRegions (equalityRegions clippedSumLeft clippedSumRight)
      clippedSumExpected = true := by decide

theorem clippedSum_exact (k : Nat) :
    wordAt clippedSumLeft k = wordAt clippedSumRight k ↔ True := by
  calc
    _ ↔ holds clippedSumExpected k :=
      (holds_equalityRegions clippedSumLeft clippedSumRight k).symm.trans
        ((equivalentRegions_spec _ _).mp clippedSum_certificate k)
    _ ↔ _ := by simp [clippedSumExpected, holds, Interval.Contains]

def badDigitLeft : List RunSpec := [⟨1, ⟨1, 0⟩⟩, ⟨2, ⟨-1, 3⟩⟩]
def badDigitRight : List RunSpec := [⟨1, ⟨1, 0⟩⟩, ⟨1, ⟨-1, 3⟩⟩]
def badDigitExpected : Region := [⟨3, none⟩]

theorem badDigit_certificate :
    equivalentRegions (equalityRegions badDigitLeft badDigitRight)
      badDigitExpected = true := by decide

theorem badDigit_exact (k : Nat) :
    wordAt badDigitLeft k = wordAt badDigitRight k ↔ 3 ≤ k := by
  calc
    _ ↔ holds badDigitExpected k :=
      (holds_equalityRegions badDigitLeft badDigitRight k).symm.trans
        ((equivalentRegions_spec _ _).mp badDigit_certificate k)
    _ ↔ _ := by simp [badDigitExpected, holds, Interval.Contains]

def literalZeroLeft : List RunSpec := [⟨0, ⟨0, 1⟩⟩]
def literalZeroRight : List RunSpec := []
def literalZeroExpected : Region := []

theorem literalZero_certificate :
    equivalentRegions (equalityRegions literalZeroLeft literalZeroRight)
      literalZeroExpected = true := by decide

theorem literalZero_exact (k : Nat) :
    wordAt literalZeroLeft k = wordAt literalZeroRight k ↔ False := by
  calc
    _ ↔ holds literalZeroExpected k :=
      (holds_equalityRegions literalZeroLeft literalZeroRight k).symm.trans
        ((equivalentRegions_spec _ _).mp literalZero_certificate k)
    _ ↔ _ := by simp [literalZeroExpected, holds]

def boundedPalindrome : List RunSpec :=
  [⟨1, ⟨-1, 3⟩⟩, ⟨2, ⟨0, 1⟩⟩, ⟨1, ⟨1, -5⟩⟩]
def boundedPalindromeExpected : Region := [⟨3, some 6⟩]

theorem boundedPalindrome_certificate :
    equivalentRegions (palindromeRegions boundedPalindrome)
      boundedPalindromeExpected = true := by decide

theorem boundedPalindrome_exact (k : Nat) :
    wordAt boundedPalindrome k = (wordAt boundedPalindrome k).reverse ↔ 3 ≤ k ∧ k < 6 := by
  calc
    _ ↔ holds boundedPalindromeExpected k :=
      (holds_palindromeRegions boundedPalindrome k).symm.trans
        ((equivalentRegions_spec _ _).mp boundedPalindrome_certificate k)
    _ ↔ _ := by simp [boundedPalindromeExpected, holds, Interval.Contains]

def hugeHoleLeft : List RunSpec :=
  [⟨5, ⟨1, -(huge : Int)⟩⟩, ⟨5, ⟨1, -(huge : Int) - 4⟩⟩]
def hugeHoleRight : List RunSpec := [⟨5, ⟨2, -(2 * (huge : Int)) - 4⟩⟩]
def hugeHoleExpected : Region := [⟨0, some (huge + 1)⟩, ⟨huge + 4, none⟩]

theorem hugeHole_certificate :
    equivalentRegions (equalityRegions hugeHoleLeft hugeHoleRight)
      hugeHoleExpected = true := by decide

theorem hugeHole_exact (k : Nat) :
    wordAt hugeHoleLeft k = wordAt hugeHoleRight k ↔ k < huge + 1 ∨ huge + 4 ≤ k := by
  calc
    _ ↔ holds hugeHoleExpected k :=
      (holds_equalityRegions hugeHoleLeft hugeHoleRight k).symm.trans
        ((equivalentRegions_spec _ _).mp hugeHole_certificate k)
    _ ↔ _ := by simp [hugeHoleExpected, holds, Interval.Contains]

def hugeDeclining : List RunSpec := [⟨1, ⟨-1, (huge : Int)⟩⟩, ⟨2, ⟨0, 1⟩⟩]
def hugeDecliningExpected : Region := [⟨huge, none⟩]

theorem hugeDeclining_certificate :
    equivalentRegions (palindromeRegions hugeDeclining)
      hugeDecliningExpected = true := by decide

theorem hugeDeclining_exact (k : Nat) :
    wordAt hugeDeclining k = (wordAt hugeDeclining k).reverse ↔ huge ≤ k := by
  calc
    _ ↔ holds hugeDecliningExpected k :=
      (holds_palindromeRegions hugeDeclining k).symm.trans
        ((equivalentRegions_spec _ _).mp hugeDeclining_certificate k)
    _ ↔ _ := by simp [hugeDecliningExpected, holds, Interval.Contains]

#print axioms twoIsolated_certificate
#print axioms twoIsolated_exact
#print axioms boundedEmpty_certificate
#print axioms boundedEmpty_exact
#print axioms middleHole_certificate
#print axioms middleHole_exact
#print axioms interiorZero_certificate
#print axioms interiorZero_exact
#print axioms clippedSum_certificate
#print axioms clippedSum_exact
#print axioms badDigit_certificate
#print axioms badDigit_exact
#print axioms literalZero_certificate
#print axioms literalZero_exact
#print axioms boundedPalindrome_certificate
#print axioms boundedPalindrome_exact
#print axioms hugeHole_certificate
#print axioms hugeHole_exact
#print axioms hugeDeclining_certificate
#print axioms hugeDeclining_exact

end Agent102.ParameterSetControls
