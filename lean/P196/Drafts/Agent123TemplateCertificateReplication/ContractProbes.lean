import P196.Drafts.Agent121MergedTemplateSafetyReview.NoPalCompat
import P196.Drafts.Agent109TemplateReturnCertificate.CertCompat

/-!
Agent #123: kernel-checked regression probes, not new research theorems.
These check the boundary at time zero and the distinction between a local
transition and a globally accepted cyclic certificate. All source dependencies
must be rebuilt with the pinned runner before compiling this file.
-/
namespace Agent123.Probes
open Agent109 Agent109.Cert

/-- A realized complementary template is permitted to start at a palindrome. -/
def start : Nat := 11888811

theorem start_pair : pairWord start = template 2 [] [] [] 2 2 := by decide

theorem start_palindrome : Palindrome start := by
  unfold Palindrome
  decide

theorem first_step_value : step start = 23777622 := by decide

theorem first_step_not_palindrome : ¬ Palindrome (step start) := by
  exact Agent109.NoPal.template_step_not_palindrome start 2 [] [] [] 0 0
    (by decide) (by simp [Bounded]) (by simp [Bounded]) (by simp [Bounded]) start_pair

/-- This is the existing author's deliberately rejected CertDemo, replayed
without relying on an external evaluation oracle. -/
def rejectedDemo : Certificate :=
  { states := [⟨2, [1], [3], [4]⟩, ⟨4, [3, 5], [1], [2, 2]⟩],
    links := [⟨0, 0, 0, 0, 5, 5⟩, ⟨0, 0, 0, 0, 5, 5⟩] }

theorem demo_rejected : check rejectedDemo = false := by decide

theorem zero_not_lychrel : ¬ Lychrel196.IsLychrel 0 := by
  intro h
  exact h 0 (by rfl)

end Agent123.Probes

#print axioms Agent123.Probes.start_pair
#print axioms Agent123.Probes.start_palindrome
#print axioms Agent123.Probes.first_step_value
#print axioms Agent123.Probes.first_step_not_palindrome
#print axioms Agent123.Probes.demo_rejected

#print axioms Agent123.Probes.zero_not_lychrel
