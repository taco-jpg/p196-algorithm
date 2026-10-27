import P196.Agent108CyclicQuotientLift.WordWalk
import P196.Agent108CyclicQuotientLift.FiniteReturn

/-!
# Closed-word lifting through a finite labelled quotient

This formalizes the power-lifting argument proposed by Agent106 and
independently discussed by Agent113 for cyclic graph representations.
The exact assumption is pointwise edge lifting, not just a graph
homomorphism. A prescribed source may have a transient; the closed lift
need not start there, and its word can be a positive power of the original.
No exterior arithmetic, graph generator, or decimal result is asserted.
-/

namespace Agent108.CyclicQuotientLift

universe u v q

/-- A labelled closed quotient walk has a bounded transient and positive
return in any finite cover of its basepoint fiber. The cover may contain
duplicates or extra vertices; its length is the explicit supplied bound. -/
theorem lift_closed_with_transient
    {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    {q0 : Q} {w : List A} (carrier : List V)
    (hcarrier : ∀ x, pi x = q0 → x ∈ carrier)
    (x0 : V) (hx0 : pi x0 = q0) (hclosed : Walk F q0 w q0) :
    ∃ r m y, 0 < m ∧ r + m ≤ carrier.length ∧ pi y = q0 ∧
      Walk E x0 (wordPower w r) y ∧ Walk E y (wordPower w m) y := by
  classical
  have one (x : V) (hx : pi x = q0) :
      ∃ y, Walk E x w y ∧ pi y = q0 := by
    apply walk_lift pi hlift
    simpa only [hx] using hclosed
  let next : V → V := fun x =>
    if hx : pi x = q0 then Classical.choose (one x hx) else x
  have next_spec (x : V) (hx : pi x = q0) :
      Walk E x w (next x) ∧ pi (next x) = q0 := by
    simpa only [next, dif_pos hx] using Classical.choose_spec (one x hx)
  have invariant : ∀ n x, pi x = q0 → pi (iter next n x) = q0 := by
    intro n
    induction n with
    | zero => intro x hx; exact hx
    | succ n ih =>
        intro x hx
        exact (next_spec (iter next n x) (ih x hx)).2
  have trace : ∀ n x, pi x = q0 →
      Walk E x (wordPower w n) (iter next n x) := by
    intro n
    induction n with
    | zero => intro x _; exact rfl
    | succ n ih =>
        intro x hx
        rw [wordPower_succ_right]
        exact (walk_append (wordPower w n) w).mpr
          ⟨iter next n x, ih x hx, (next_spec _ (invariant n x hx)).1⟩
  have hmem : ∀ n, iter next n x0 ∈ carrier :=
    fun n => hcarrier _ (invariant n x0 hx0)
  obtain ⟨r, m, hm, hbound, hreturn⟩ :=
    finite_orbit_periodic_state next x0 carrier hmem
  refine ⟨r, m, iter next r x0, hm, hbound, invariant r x0 hx0,
    trace r x0 hx0, ?_⟩
  simpa only [hreturn] using trace m (iter next r x0) (invariant r x0 hx0)

/-- Nonempty quotient words have nonempty closed lifts of positive powers.
This is existential over the original starting vertex in the fiber. -/
theorem lift_nonempty_closed_power
    {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    {q0 : Q} {w : List A} (carrier : List V)
    (hcarrier : ∀ x, pi x = q0 → x ∈ carrier)
    (x0 : V) (hx0 : pi x0 = q0)
    (hw : w ≠ []) (hclosed : Walk F q0 w q0) :
    ∃ m y, 0 < m ∧ m ≤ carrier.length ∧ pi y = q0 ∧
      wordPower w m ≠ [] ∧ Walk E y (wordPower w m) y := by
  obtain ⟨r, m, y, hm, hbound, hy, _, hreturn⟩ :=
    lift_closed_with_transient pi hlift carrier hcarrier x0 hx0 hclosed
  exact ⟨m, y, hm, by omega, hy, wordPower_ne_nil hw hm, hreturn⟩

/-- A predicate on complete label words that survives positive repetition. -/
def PowerStable {A : Type v} (accept : List A → Prop) : Prop :=
  ∀ w m, accept w → 0 < m → accept (wordPower w m)

/-- Existence of a nonempty labelled closed walk satisfying a word predicate. -/
def ClosedWith {V : Type u} {A : Type v}
    (E : V → A → V → Prop) (accept : List A → Prop) : Prop :=
  ∃ x w, w ≠ [] ∧ Walk E x w x ∧ accept w

/-- The entire positive-repetition language of one fixed driver word. -/
def PositivePowers {A : Type v} (driver word : List A) : Prop :=
  ∃ k, 0 < k ∧ word = wordPower driver k

theorem positivePowers_powerStable {A : Type v} (driver : List A) :
    PowerStable (PositivePowers driver) := by
  rintro word m ⟨k, hk, rfl⟩ hm
  exact ⟨k * m, Nat.mul_pos hk hm, wordPower_mul driver k m⟩

/-- A surjective labelled homomorphism with pointwise lifting and finite
fibers preserves closed-word existence for power-stable predicates.
It does not preserve existence at one fixed word length. -/
theorem closedWith_iff_of_powerStable
    {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hmap : ∀ x a y, E x a y → F (pi x) a (pi y))
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    (onto : ∀ q0, ∃ x, pi x = q0)
    (fibers : Q → List V)
    (hfinite : ∀ q0 x, pi x = q0 → x ∈ fibers q0)
    {accept : List A → Prop} (hstable : PowerStable accept) :
    ClosedWith E accept ↔ ClosedWith F accept := by
  constructor
  · rintro ⟨x, w, hw, hwalk, ha⟩
    exact ⟨pi x, w, hw, walk_map pi hmap hwalk, ha⟩
  · rintro ⟨q0, w, hw, hwalk, ha⟩
    obtain ⟨x0, hx0⟩ := onto q0
    obtain ⟨m, y, hm, _, _, hnonempty, hreturn⟩ :=
      lift_nonempty_closed_power pi hlift (fibers q0) (hfinite q0)
        x0 hx0 hw hwalk
    exact ⟨y, wordPower w m, hnonempty, hreturn, hstable w m ha hm⟩

/-- The same equivalence transports a proved absence of accepted closed words. -/
theorem no_closedWith_iff_of_powerStable
    {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hmap : ∀ x a y, E x a y → F (pi x) a (pi y))
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    (onto : ∀ q0, ∃ x, pi x = q0)
    (fibers : Q → List V)
    (hfinite : ∀ q0 x, pi x = q0 → x ∈ fibers q0)
    {accept : List A → Prop} (hstable : PowerStable accept) :
    ¬ ClosedWith E accept ↔ ¬ ClosedWith F accept := by
  exact not_congr (closedWith_iff_of_powerStable pi hmap hlift onto fibers hfinite hstable)

/-- Concrete specialization to every positive power of a fixed driver;
the exponent is existential and may grow when lifting through the quotient. -/
theorem positivePowers_closedWith_iff
    {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hmap : ∀ x a y, E x a y → F (pi x) a (pi y))
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    (onto : ∀ q0, ∃ x, pi x = q0)
    (fibers : Q → List V)
    (hfinite : ∀ q0 x, pi x = q0 → x ∈ fibers q0)
    (driver : List A) :
    ClosedWith E (PositivePowers driver) ↔ ClosedWith F (PositivePowers driver) := by
  exact closedWith_iff_of_powerStable pi hmap hlift onto fibers hfinite
    (positivePowers_powerStable driver)

end Agent108.CyclicQuotientLift
