import P196.Sprint.Agent19.Fidelity
import P196.Agent118PrefixKernel.PrefixAncestry

/-!
# Agent 19 review: transfer of every prefix-exclusion format to plain arithmetic

The reviewed exclusions use four target predicates:
`Agent118.PrefixKernel.PalindromeStarts3` (217, 218, 777),
`Agent124.PrefixK.PalStarts3` (620, the 33 classes),
`SevenColumnKernel.PalindromeBridge.PalindromeStarts739` (739) and
`Agent124.PrefixL.PalStartsL` (four-digit lists, the 277-word list).
Each transfer lemma below turns an all-time exclusion in that format into the plain
statement: no palindrome iterate of 196 has a decimal truncation `orbit 196 t / 10 ^ k`
equal to the prefix.  The lemmas need only the target definitions, not the certificates;
`ArithHeavy.lean` applies them to the certificate endpoints.

Also: a new kernel-checked delay witness for 777 (19 steps, previous witness 14).
-/

namespace Sprint.Agent19.ArithTransfer

open Lychrel196 Sprint.Agent19.Fidelity

theorem agent118_iff (a b c P : Nat) :
    Agent118.PrefixKernel.PalindromeStarts3 a b c P ↔ Agent124.PrefixL.PalStartsL [a, b, c] P :=
  (Agent124.PrefixL.palStartsL_three_iff a b c P).symm

theorem fromDigits_three (a b c : Nat) : fromDigits [a, b, c] = 100 * a + 10 * b + c := by
  simp [fromDigits]
  omega

theorem fromDigits_four (a b c d : Nat) :
    fromDigits [a, b, c, d] = 1000 * a + 100 * b + 10 * c + d := by
  simp [fromDigits]
  omega

/-- Transfer for a three-digit predicate stated as `PalStartsL [a, b, c]`. -/
theorem transfer3 {a b c : Nat} (h1 : 1 ≤ a) (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 9)
    (hex : ∀ t, ¬ Agent124.PrefixL.PalStartsL [a, b, c] (orbit 196 t)) :
    ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 100 * a + 10 * b + c := by
  intro t k hp
  rw [← fromDigits_three]
  exact plain_of_palStartsL (by simp) (by simp; omega) (by simpa using h1) (hex t) hp k

theorem transfer118 {a b c : Nat} (h1 : 1 ≤ a) (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 9)
    (hex : ∀ t, ¬ Agent118.PrefixKernel.PalindromeStarts3 a b c (orbit 196 t)) :
    ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 100 * a + 10 * b + c :=
  transfer3 h1 ha hb hc (fun t h => hex t ((agent118_iff a b c _).mpr h))

theorem transfer124 {a b c : Nat} (h1 : 1 ≤ a) (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 9)
    (hex : ∀ t, ¬ Agent124.PrefixK.PalStarts3 a b c (orbit 196 t)) :
    ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 100 * a + 10 * b + c :=
  transfer3 h1 ha hb hc (fun t h => hex t ((palStarts3_iff a b c _).mpr h))

theorem transfer739
    (hex : ∀ t, ¬ SevenColumnKernel.PalindromeBridge.PalindromeStarts739 (orbit 196 t)) :
    ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 739 :=
  transfer124 (a := 7) (b := 3) (c := 9) (by decide) (by decide) (by decide) (by decide)
    (fun t h => hex t ((Agent124.PrefixK.palStarts3_739_iff _).mp h))

/-- Transfer for an explicit list of digit prefixes (validity checked by evaluation). -/
theorem transferList {L : List (List Nat × Nat)}
    (hv : L.all (fun e => validPrefix e.1) = true)
    (hex : ∀ t, ∀ e ∈ L, ¬ Agent124.PrefixL.PalStartsL e.1 (orbit 196 t)) :
    ∀ t k, Palindrome (orbit 196 t) → ∀ e ∈ L, orbit 196 t / 10 ^ k ≠ fromDigits e.1 := by
  intro t k hp e he
  exact plain_of_valid (List.all_eq_true.mp hv e he) (hex t e he) hp k

/-! ## New delay witness for 777 (lower bound 19 on any ancestry bound) -/

theorem w777_orbit19 : orbit 10000026100 19 = 77798878687889777 := by decide

theorem w777_family : Agent118.PrefixKernel.PalindromeStarts3 7 7 7 77798878687889777 :=
  (agent118_iff 7 7 7 _).mpr
    ⟨by decide, startsL_of_div (k := 14) (by simp) (by decide) (by decide) (by decide)⟩

/-- Some positive seed reaches a palindrome beginning with 777 after exactly 19 steps, so
no ancestry bound below 19 holds for 777 (`Agent118.Witnesses.depth14_777` had 14). -/
theorem depth19_777 : ∃ A P, 0 < A ∧ Agent118.PrefixKernel.PalindromeStarts3 7 7 7 P ∧
    orbit A 19 = P :=
  ⟨_, _, by decide, w777_family, w777_orbit19⟩

end Sprint.Agent19.ArithTransfer

#print axioms Sprint.Agent19.ArithTransfer.transfer118
#print axioms Sprint.Agent19.ArithTransfer.transfer124
#print axioms Sprint.Agent19.ArithTransfer.transfer739
#print axioms Sprint.Agent19.ArithTransfer.transferList
#print axioms Sprint.Agent19.ArithTransfer.depth19_777
