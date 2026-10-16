import ExteriorAbsorbedObstruction

namespace P196.Agent6
set_option maxRecDepth 100000

/-! Literal ordinary-integer realizations of both potential obstructions.
Each displayed digit word is connected by the actual canonical map.
These are finite controls, not persistent or returned full interfaces. -/

def witnessReversal0 : Word := [0,0,0,0,0,0,3,3,3,3,9,9,9,9,6,6,6,6,5,1]
def witnessReversal1 : Word := [1,5,6,6,6,6,2,3,3,3,3,3,3,3,7,6,6,6,5,1]
def witnessReversal2 : Word := [2,0,3,3,3,4,6,6,6,6,6,6,6,5,3,3,3,3,1,3]

theorem ordinary_Reversal_literal_control :
    numeral witnessReversal0 = 15666699993333000000 ∧
    paired witnessReversal0 = surrounded [1,5] 6 2 [12,12,12,12,12,12,12,12] ∧
    numeral witnessReversal1 = 15666733333332666651 ∧
    paired witnessReversal1 = surrounded [2,10] 12 1 [13,5,6,6,6,6,6,6,5,13] ∧
    numeral witnessReversal2 = 31333356666666433302 ∧
    paired witnessReversal2 = surrounded [5,1] 6 1 [7,11,12,12,12,12,12,12,11,7] ∧
    reverseAddDigits witnessReversal0 = witnessReversal1 ∧
    reverseAddDigits witnessReversal1 = witnessReversal2 := by
  decide +kernel

#print axioms ordinary_Reversal_literal_control

def witnessAbsorbedA0 : Word := [1,0,0,0,3,3,3,3,0,0,0,0,6,6,6,6,9,9,9,9,4,8,8,9]
def witnessAbsorbedA1 : Word := [0,9,8,4,2,3,3,3,7,6,6,6,6,6,6,6,2,3,3,3,5,8,8,0,1]
def witnessAbsorbedA2 : Word := [1,9,6,3,8,6,6,6,9,2,3,3,3,3,3,3,0,7,6,6,7,2,7,0,2]
def witnessAbsorbedA3 : Word := [3,9,3,6,5,3,3,4,0,6,6,6,6,6,6,5,9,3,3,3,6,6,3,0,4]

theorem ordinary_AbsorbedA_literal_control :
    numeral witnessAbsorbedA0 = 988499996666000033330001 ∧
    paired witnessAbsorbedA0 = surrounded [10,8,8,4] 12 2 [6,6,6,6,6,6,6,6] ∧
    numeral witnessAbsorbedA1 = 1088533326666666733324890 ∧
    paired witnessAbsorbedA1 = surrounded [1,9,16,12,7] 6 1 [9,12,12,12,12,12,12,12,9] ∧
    numeral witnessAbsorbedA2 = 2072766703333332966683691 ∧
    paired witnessAbsorbedA2 = surrounded [3,9,13,5,15] 12 0 [13,9,5,6,6,6,6,6,5,9,13] ∧
    numeral witnessAbsorbedA3 = 4036633395666666043356393 ∧
    paired witnessAbsorbedA3 = surrounded [7,9,6,12,11] 6 0 [7,9,11,12,12,12,12,12,11,9,7] ∧
    reverseAddDigits witnessAbsorbedA0 = witnessAbsorbedA1 ∧
    reverseAddDigits witnessAbsorbedA1 = witnessAbsorbedA2 ∧
    reverseAddDigits witnessAbsorbedA2 = witnessAbsorbedA3 := by
  decide +kernel

#print axioms ordinary_AbsorbedA_literal_control

def witnessAbsorbedB0 : Word := [6,0,0,0,3,3,3,3,0,0,0,0,6,6,6,6,9,9,9,9,4,8,3,9]
def witnessAbsorbedB1 : Word := [5,4,8,4,2,3,3,3,7,6,6,6,6,6,6,6,2,3,3,3,5,8,3,5,1]
def witnessAbsorbedB2 : Word := [6,9,1,3,8,6,6,6,9,2,3,3,3,3,3,3,0,7,6,6,7,2,2,0,7]

theorem ordinary_AbsorbedB_literal_control :
    numeral witnessAbsorbedB0 = 938499996666000033330006 ∧
    paired witnessAbsorbedB0 = surrounded [15,3,8,4] 12 2 [6,6,6,6,6,6,6,6] ∧
    numeral witnessAbsorbedB1 = 1538533326666666733324845 ∧
    paired witnessAbsorbedB1 = surrounded [6,9,11,12,7] 6 1 [9,12,12,12,12,12,12,12,9] ∧
    numeral witnessAbsorbedB2 = 7022766703333332966683196 ∧
    paired witnessAbsorbedB2 = surrounded [13,9,3,5,15] 12 0 [13,9,5,6,6,6,6,6,5,9,13] ∧
    reverseAddDigits witnessAbsorbedB0 = witnessAbsorbedB1 ∧
    reverseAddDigits witnessAbsorbedB1 = witnessAbsorbedB2 := by
  decide +kernel

#print axioms ordinary_AbsorbedB_literal_control

end P196.Agent6
