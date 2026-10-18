import P196.Drafts.Agent109TemplateStepSafety.NoPalStep
import P196.Agent101ProtectedFamily.Compat

/-! Agent #109: `template_orbit_safe` restated with the accepted `Lychrel196`
semantics and Agent #8's `template`. -/

namespace Agent109.NoPalCompat
open Agent109

theorem lychrel_template_orbit_safe (n c : Nat) (B A C : Word) (g h k : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hg : 2 * k + 2 ≤ g) (hh : 2 * k + 2 ≤ h)
    (hn : pairWord n = Agent8.template c B A C g h) :
    ∀ i, 1 ≤ i → i ≤ k + 1 → ¬ Lychrel196.Palindrome (Lychrel196.orbit n i) := by
  intro i h1 h2
  rw [Compat.palindrome_eq, Compat.orbit_eq]
  exact NoPal.template_orbit_safe n c B A C g h k hc hB hA hC hg hh hn i h1 h2

end Agent109.NoPalCompat

#print axioms Agent109.NoPalCompat.lychrel_template_orbit_safe
