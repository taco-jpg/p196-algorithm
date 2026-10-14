import Std

/-!
A general graph-certificate theorem for excluding periodic finite centers.

This formalizes the invariant/homomorphism/ranking argument. The concrete
47- and 73-vertex Python certificates and their decimal carry semantics
are NOT instantiated here. No Lychrel existence result is claimed.
-/
namespace TemporalInvariant

structure Graph (V : Type) (A : Type) where
  edge : V → A → V → Prop

def AcceptsCycle {V A : Type} (g : Graph V A)
    (word : Nat → A) (period : Nat) : Prop :=
  ∃ path : Nat → V, path period = path 0 ∧
    ∀ i, i < period → g.edge (path i) (word i) (path (i+1))

theorem map_cycle {V W A : Type} (g : Graph V A) (h : Graph W A)
    (f : V → W)
    (hf : ∀ u a v, g.edge u a v → h.edge (f u) a (f v))
    (word : Nat → A) (period : Nat)
    (hc : AcceptsCycle g word period) : AcceptsCycle h word period := by
  obtain ⟨path, closed, edges⟩ := hc
  exact ⟨fun i => f (path i), congrArg f closed,
    fun i hi => hf _ _ _ (edges i hi)⟩

theorem ranking_excludes_cycle {V A : Type} (g : Graph V A)
    (rank : V → Nat)
    (hr : ∀ u a v, g.edge u a v → rank u < rank v)
    (word : Nat → A) (period : Nat) (hp : 0 < period) :
    ¬ AcceptsCycle g word period := by
  rintro ⟨path, closed, edges⟩
  have lower : ∀ i, i ≤ period → rank (path 0) + i ≤ rank (path i) := by
    intro i
    induction i with
    | zero => intro _; omega
    | succ i ih =>
      intro hi
      have hprev := ih (by omega)
      have hstep := hr _ _ _ (edges i (by omega))
      omega
  have hend := lower period (Nat.le_refl period)
  rw [closed] at hend
  omega

/-- A phase-preserving temporal inverse graph mapped back to an invariant,
and an acyclic center-head graph, exclude every finite center completion.
Both temporal period and spatial depth are arbitrary natural numbers.
All links to a particular arithmetic system are explicit hypotheses. -/
theorem no_finite_center
    {S V W U A : Type}
    (invariant : Graph V A) (inverse : Graph W A) (heads : Graph U A)
    (word : S → Nat → A) (inward : S → S → Prop) (center : S → Prop)
    (f : W → V)
    (hf : ∀ u a v, inverse.edge u a v → invariant.edge (f u) a (f v))
    (rank : U → Nat)
    (hr : ∀ u a v, heads.edge u a v → rank u < rank v)
    (period : Nat) (hperiod : 0 < period)
    (hinverse : ∀ s t, inward s t → AcceptsCycle invariant (word s) period →
      AcceptsCycle inverse (word t) period)
    (hhead : ∀ s, center s → AcceptsCycle invariant (word s) period →
      AcceptsCycle heads (word s) period)
    (trace : Nat → S) (depth : Nat)
    (hstart : AcceptsCycle invariant (word (trace 0)) period)
    (hsteps : ∀ i, i < depth → inward (trace i) (trace (i+1))) :
    ¬ center (trace depth) := by
  have reachable : ∀ i, i ≤ depth → AcceptsCycle invariant (word (trace i)) period := by
    intro i
    induction i with
    | zero => intro _; exact hstart
    | succ i ih =>
      intro hi
      have hc := hinverse _ _ (hsteps i (by omega)) (ih (by omega))
      exact map_cycle inverse invariant f hf _ period hc
  intro hc
  exact ranking_excludes_cycle heads rank hr _ period hperiod
    (hhead _ hc (reachable depth (Nat.le_refl depth)))

#print axioms map_cycle
#print axioms ranking_excludes_cycle
#print axioms no_finite_center

end TemporalInvariant
