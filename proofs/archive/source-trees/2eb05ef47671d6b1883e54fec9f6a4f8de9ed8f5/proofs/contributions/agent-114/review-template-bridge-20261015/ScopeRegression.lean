import IntegerEndpoints
import CertCompat

/-!
Agent #114: executable, kernel-checked review regressions.
These are scope and semantics controls, not new research theorems or a
certificate instance. Original results remain credited to their authors.
-/
namespace Agent114.Review

open Agent109

/-- Zero is a palindrome; empty words cannot supply a positive-seed witness. -/
theorem zero_semantics :
    pairWord 0 = [] ∧ Lychrel196.reverse10 0 = 0 ∧
    Lychrel196.Palindrome 0 := by decide

/-- Decimal reversal drops the zeros exposed at the most significant end. -/
theorem trailing_zero_semantics :
    digits 1000 = [0, 0, 0, 1] ∧ Lychrel196.reverse10 1000 = 1 ∧
    Lychrel196.step 1000 = 1001 ∧ Lychrel196.Palindrome (Lychrel196.step 1000) := by decide

/-- One exact 196 transition is a regression, not an infinite-time assertion. -/
theorem seed196_semantics :
    pairWord 196 = [7, 18, 7] ∧ Lychrel196.step 196 = 887 ∧
    pairWord (Lychrel196.step 196) = [15, 16, 15] ∧
    (pairWord 196).reverse = pairWord 196 ∧ ¬ Lychrel196.Palindrome 196 := by decide

/-- The two-step return obstruction holds for a seed that reaches a palindrome
at that very time. Thus the obstruction must not be described as orbit safety. -/
theorem two_step_exclusion_is_not_safety :
    pairWord 76 = Agent8.template 13 [] [] [] 1 0 ∧
    (∀ g h : Nat, 0 < g →
      pairWord (Lychrel196.orbit 76 2) ≠ Agent8.template 13 [] [] [] g h) ∧
    Lychrel196.orbit 76 2 = 484 ∧
    Lychrel196.Palindrome (Lychrel196.orbit 76 2) := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro g h hg
  exact Agent109.Endpoints.no_two_step_actual_template_return
    76 13 [] [] [] 1 0 g h (by decide) (by decide) hg (by decide)

/-- The six-phase endpoint also allows seeds hitting a palindrome earlier. -/
theorem six_step_exclusion_is_not_safety :
    Agent8.SixPhase 4 ∧ pairWord 13 = Agent8.template 4 [] [] [] 1 0 ∧
    (∀ g h : Nat, 1 ≤ g →
      pairWord (Lychrel196.orbit 13 6) ≠ Agent8.template 4 [] [] [] g h) ∧
    Lychrel196.step 13 = 44 ∧ Lychrel196.Palindrome (Lychrel196.step 13) := by
  refine ⟨by unfold Agent8.SixPhase; decide, by decide, ?_, by decide, by decide⟩
  intro g h hg
  exact Agent109.Endpoints.no_repeatable_six_step_actual_template_return
    13 4 [] [] [] 1 0 g h (by decide) (by unfold Agent8.SixPhase; decide) (by decide)
    hg (Nat.zero_le _) (by decide)

/-- Agent 8's canonical class strictly contains the mirrored pair words of positive integers.
The odd singleton is canonical but cannot be realized by an integer. This
checks why the certificate's separate even-middle admissibility is essential. -/
theorem canonical_is_not_realizable :
    (∀ n : Nat, n ≠ 0 → Agent8.CanonicalPair (pairWord n)) ∧
    Agent8.CanonicalPair [1] ∧ ¬ ∃ n : Nat, pairWord n = [1] := by
  refine ⟨Agent109.Endpoints.pairWord_canonical, ?_, ?_⟩
  · simp [Agent8.CanonicalPair, Agent8.Bounded]
  · rintro ⟨n, hn⟩
    have hl := zipAdd_length (digits n) (digits n).reverse (by simp)
    change (pairWord n).length = (digits n).length at hl
    rw [hn] at hl
    have hlen : (digits n).length = 1 := by simpa using hl.symm
    cases hd : digits n with
    | nil => simp [hd] at hlen
    | cons x xs =>
      have hxlen : xs.length + 1 = 1 := by
        simpa only [hd, List.length_cons] using hlen
      have hxs : xs = [] := List.length_eq_zero.mp (by omega)
      have he : x + x = 1 := by
        simpa [pairWord, hd, hxs, pair, zipAdd] using hn
      omega

open Agent109.Cert

def emptyCert : Certificate := ⟨[], []⟩
def missingLinkCert : Certificate := ⟨[⟨2, [], [], []⟩], []⟩
def oddCenterCert : Certificate := ⟨[⟨2, [], [], [1]⟩], []⟩
def evenCenterCert : Certificate := ⟨[⟨2, [], [], [2]⟩], []⟩

/-- Empty or truncated data cannot silently establish a certificate premise. -/
theorem malformed_certificates_rejected :
    check emptyCert = false ∧ check missingLinkCert = false := by decide

/-- A realizable first state's parity test is distinct from cycle validity. -/
theorem admissibility_is_not_validity :
    decide (Admissible0 oddCenterCert [] [1]) = false ∧
    decide (Admissible0 evenCenterCert [] [2]) = true ∧
    check evenCenterCert = false := by decide

end Agent114.Review
