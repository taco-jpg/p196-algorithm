import P196.Sprint.Agent19.ArithTransfer
import P196.Agent124FourDigit.A124F4Final
import P196.Agent124FourDigit.A124F5Final

/-!
# Agent 19 review: plain-arithmetic form of the four-digit refinement lists

Applies the transfer lemmas of `ArithTransfer.lean` to the four-digit refinement lists: for every time `t` and every
`k`, if `orbit 196 t` is a palindrome then `orbit 196 t / 10 ^ k` is not the excluded prefix.
The `*_valid` checks show no listed prefix is vacuous (empty, leading zero, digit > 9).
-/

namespace Sprint.Agent19.ArithFourDigit

open Lychrel196 Sprint.Agent19.Fidelity Sprint.Agent19.ArithTransfer

theorem F4_00_valid : Agent124.CertF4.entries00.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_00 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries00, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_00_valid (fun t => Agent124.CertF4.no_196_00 t)

theorem F4_01_valid : Agent124.CertF4.entries01.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_01 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries01, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_01_valid (fun t => Agent124.CertF4.no_196_01 t)

theorem F4_02_valid : Agent124.CertF4.entries02.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_02 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries02, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_02_valid (fun t => Agent124.CertF4.no_196_02 t)

theorem F4_03_valid : Agent124.CertF4.entries03.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_03 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries03, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_03_valid (fun t => Agent124.CertF4.no_196_03 t)

theorem F4_04_valid : Agent124.CertF4.entries04.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_04 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries04, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_04_valid (fun t => Agent124.CertF4.no_196_04 t)

theorem F4_05_valid : Agent124.CertF4.entries05.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_05 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries05, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_05_valid (fun t => Agent124.CertF4.no_196_05 t)

theorem F4_06_valid : Agent124.CertF4.entries06.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F4_06 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF4.entries06, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F4_06_valid (fun t => Agent124.CertF4.no_196_06 t)

theorem F5_00_valid : Agent124.CertF5.entries00.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F5_00 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF5.entries00, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F5_00_valid (fun t => Agent124.CertF5.no_196_00 t)

theorem F5_01_valid : Agent124.CertF5.entries01.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F5_01 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF5.entries01, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F5_01_valid (fun t => Agent124.CertF5.no_196_01 t)

theorem F5_02_valid : Agent124.CertF5.entries02.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F5_02 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF5.entries02, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F5_02_valid (fun t => Agent124.CertF5.no_196_02 t)

theorem F5_03_valid : Agent124.CertF5.entries03.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F5_03 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF5.entries03, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F5_03_valid (fun t => Agent124.CertF5.no_196_03 t)

theorem F5_04_valid : Agent124.CertF5.entries04.all (fun e => validPrefix e.1) = true := by
  decide +kernel

theorem plain_F5_04 : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.CertF5.entries04, orbit 196 t / 10 ^ k ≠ fromDigits e.1 :=
  transferList F5_04_valid (fun t => Agent124.CertF5.no_196_04 t)

end Sprint.Agent19.ArithFourDigit

#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_00
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_01
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_02
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_03
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_04
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_05
#print axioms Sprint.Agent19.ArithFourDigit.plain_F4_06
#print axioms Sprint.Agent19.ArithFourDigit.plain_F5_00
#print axioms Sprint.Agent19.ArithFourDigit.plain_F5_01
#print axioms Sprint.Agent19.ArithFourDigit.plain_F5_02
#print axioms Sprint.Agent19.ArithFourDigit.plain_F5_03
#print axioms Sprint.Agent19.ArithFourDigit.plain_F5_04
