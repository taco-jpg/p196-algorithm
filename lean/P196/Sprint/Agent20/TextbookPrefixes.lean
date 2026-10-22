import P196.Sprint.Agent20.PrefixFidelity
import P196.Agent124FourDigit.A124F4Final
import P196.Agent124FourDigit.A124F5Final
import P196.Agent117P2641.A124117P2641K7Final

/-!
# Red team (sprint agent 20): the main-branch four-digit exclusions in textbook form

Every prefix in the 12 entry lists of `Agent124FourDigit` (1,730 prefixes) and the
single 2641 endpoint is well-formed (checked by `decide`), so each `no_196_NN`
endpoint excludes exactly the palindromes whose decimal expansion begins with
the listed digits, stated with plain inequalities (no digit functions).
-/

namespace Sprint.Agent20.Textbook
open Lychrel196 Sprint.Agent20

/-- Transfer for a whole entry list. -/
theorem list_textbook (entries : List (List Nat × Nat))
    (hw : entries.all (fun e => decide (WellFormed e.1)) = true)
    (h : ∀ t, ∀ e ∈ entries, ¬ Agent124.PrefixL.PalStartsL e.1 (orbit 196 t)) :
    ∀ e ∈ entries, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
      num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) := by
  intro e he t r
  have hwe : WellFormed e.1 := by
    have := List.all_eq_true.mp hw e he
    simpa using this
  exact no_196_textbook e.1 hwe (fun t => h t e he) t r

theorem f4_00 : ∀ e ∈ Agent124.CertF4.entries00, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_00

theorem f4_01 : ∀ e ∈ Agent124.CertF4.entries01, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_01

theorem f4_02 : ∀ e ∈ Agent124.CertF4.entries02, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_02

theorem f4_03 : ∀ e ∈ Agent124.CertF4.entries03, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_03

theorem f4_04 : ∀ e ∈ Agent124.CertF4.entries04, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_04

theorem f4_05 : ∀ e ∈ Agent124.CertF4.entries05, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_05

theorem f4_06 : ∀ e ∈ Agent124.CertF4.entries06, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF4.no_196_06

theorem f5_00 : ∀ e ∈ Agent124.CertF5.entries00, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF5.no_196_00

theorem f5_01 : ∀ e ∈ Agent124.CertF5.entries01, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF5.no_196_01

theorem f5_02 : ∀ e ∈ Agent124.CertF5.entries02, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF5.no_196_02

theorem f5_03 : ∀ e ∈ Agent124.CertF5.entries03, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF5.no_196_03

theorem f5_04 : ∀ e ∈ Agent124.CertF5.entries04, ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    num e.1 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num e.1 + 1) * 10 ^ r) :=
  list_textbook _ (by decide) Agent124.CertF5.no_196_04

/-- 2641 in plain terms: no iterate of 196 is a palindrome in [2641·10^r, 2642·10^r). -/
theorem no_196_2641_textbook : ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
    2641 * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < 2642 * 10 ^ r) :=
  no_196_textbook [2, 6, 4, 1] (by decide) Agent124.Cert117P2641K7.no_196_2641

end Sprint.Agent20.Textbook

#print axioms Sprint.Agent20.Textbook.f4_00
#print axioms Sprint.Agent20.Textbook.f4_01
#print axioms Sprint.Agent20.Textbook.f4_02
#print axioms Sprint.Agent20.Textbook.f4_03
#print axioms Sprint.Agent20.Textbook.f4_04
#print axioms Sprint.Agent20.Textbook.f4_05
#print axioms Sprint.Agent20.Textbook.f4_06
#print axioms Sprint.Agent20.Textbook.f5_00
#print axioms Sprint.Agent20.Textbook.f5_01
#print axioms Sprint.Agent20.Textbook.f5_02
#print axioms Sprint.Agent20.Textbook.f5_03
#print axioms Sprint.Agent20.Textbook.f5_04
#print axioms Sprint.Agent20.Textbook.no_196_2641_textbook
