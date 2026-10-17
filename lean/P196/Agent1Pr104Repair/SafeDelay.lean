import P196.Foundations.LychrelDigitSums

/-!
Exact predecessor-tested safe images and finite first-hit delays.
All generic hypotheses are explicit.  The decimal specialization uses the
actual executable reverse-and-add map.  No Lychrel existence is asserted
without a stated additional finite-delay bound or safe-image cutoff.
-/

namespace SafeImageDynamics

variable {α : Type} (f : α → α) (Valid Bad : α → Prop)

def iter (x : α) : Nat → α
  | 0 => x
  | k + 1 => f (iter x k)

theorem iter_add (x : α) (a b : Nat) :
    iter f x (a + b) = iter f (iter f x a) b := by
  induction b with
  | zero => rfl
  | succ b ih =>
    change f (iter f x (a + b)) = f (iter f (iter f x a) b)
    exact congrArg f ih

theorem iter_valid (hf : ∀ x, Valid x → Valid (f x))
    (x : α) (hx : Valid x) (k : Nat) : Valid (iter f x k) := by
  induction k with
  | zero => exact hx
  | succ k ih => exact hf _ ih

/-- The predecessor is tested; the resulting target is not tested. -/
def image : Nat → α → Prop
  | 0, x => Valid x
  | r + 1, y => ∃ x, image r x ∧ ¬ Bad x ∧ f x = y

def SafePrefix (x : α) (r : Nat) : Prop :=
  ∀ k, k < r → ¬ Bad (iter f x k)

/-- Zero-based first bad state. Decimal `Bad` will mean next-step palindrome. -/
def FirstBad (x : α) (r : Nat) : Prop :=
  Bad (iter f x r) ∧ SafePrefix f Bad x r

theorem image_iff (y : α) (r : Nat) :
    image f Valid Bad r y ↔
      ∃ x, Valid x ∧ iter f x r = y ∧ SafePrefix f Bad x r := by
  induction r generalizing y with
  | zero =>
    constructor
    · intro hy
      exact ⟨y, hy, rfl, by intro k hk; omega⟩
    · rintro ⟨x, hx, he, _⟩
      change x = y at he
      simpa only [← he] using hx
  | succ r ih =>
    constructor
    · rintro ⟨z, hz, hsafe, he⟩
      obtain ⟨x, hx, hreach, hprefix⟩ := (ih z).mp hz
      refine ⟨x, hx, by simpa only [iter, hreach] using he, ?_⟩
      intro k hk
      by_cases hkr : k < r
      · exact hprefix k hkr
      · have heq : k = r := by omega
        simpa only [heq, hreach] using hsafe
    · rintro ⟨x, hx, he, hprefix⟩
      refine ⟨iter f x r, (ih _).mpr ⟨x, hx, rfl, ?_⟩, ?_, he⟩
      · intro k hk
        exact hprefix k (by omega)
      · exact hprefix r (by omega)

theorem image_bad_iff (r : Nat) :
    (∃ y, image f Valid Bad r y ∧ Bad y) ↔
      ∃ x, Valid x ∧ FirstBad f Bad x r := by
  constructor
  · rintro ⟨y, hy, hb⟩
    obtain ⟨x, hx, he, hs⟩ := (image_iff f Valid Bad y r).mp hy
    exact ⟨x, hx, by simpa only [he] using hb, hs⟩
  · rintro ⟨x, hx, hb, hs⟩
    exact ⟨iter f x r, (image_iff f Valid Bad _ r).mpr ⟨x, hx, rfl, hs⟩, hb⟩

theorem firstBad_suffix (x : α) (a r : Nat)
    (h : FirstBad f Bad x (a + r)) :
    FirstBad f Bad (iter f x a) r := by
  constructor
  · simpa only [iter_add] using h.1
  · intro k hk
    rw [← iter_add]
    exact h.2 (a + k) (by omega)

/-- Finite attained first-bad indices form an initial segment. -/
theorem firstBad_downward (hf : ∀ x, Valid x → Valid (f x))
    (x : α) (hx : Valid x) (d r : Nat) (hr : r ≤ d)
    (hd : FirstBad f Bad x d) :
    ∃ y, Valid y ∧ FirstBad f Bad y r := by
  refine ⟨iter f x (d - r), iter_valid f Valid hf x hx (d - r), ?_⟩
  apply firstBad_suffix f Bad x (d - r) r
  simpa only [Nat.sub_add_cancel hr] using hd

/-- A safe-image cutoff is exactly a uniform bound on finite first-bad times. -/
theorem cutoff_iff_finite_bound (hf : ∀ x, Valid x → Valid (f x)) (r : Nat) :
    (∀ y, image f Valid Bad r y → ¬ Bad y) ↔
      ∀ x d, Valid x → FirstBad f Bad x d → d < r := by
  constructor
  · intro hcut x d hx hd
    apply Classical.byContradiction
    intro hlt
    obtain ⟨y, hy, hr⟩ := firstBad_downward f Valid Bad hf x hx d r (by omega) hd
    obtain ⟨z, hz, hb⟩ := (image_bad_iff f Valid Bad r).mpr ⟨y, hy, hr⟩
    exact hcut z hz hb
  · intro hbound y hy hb
    obtain ⟨x, hx, hd⟩ := (image_bad_iff f Valid Bad r).mp ⟨y, hy, hb⟩
    have := hbound x r hx hd
    omega

theorem image_descending (hf : ∀ x, Valid x → Valid (f x)) (r : Nat) :
    ∀ y, image f Valid Bad (r + 1) y → image f Valid Bad r y := by
  induction r with
  | zero =>
    rintro y ⟨x, hx, _, he⟩
    exact he ▸ hf x hx
  | succ r ih =>
    rintro y ⟨x, hx, hs, he⟩
    exact ⟨x, ih x hx, hs, he⟩

def kernel (r : Nat) (x : α) : Prop := image f Valid Bad r x ∧ ¬ Bad x

theorem kernel_descending (hf : ∀ x, Valid x → Valid (f x)) (r : Nat) :
    ∀ y, kernel f Valid Bad (r + 1) y → kernel f Valid Bad r y := by
  intro y hy
  exact ⟨image_descending f Valid Bad hf r y hy.1, hy.2⟩

/-- Closure of K_r = S_r \ Bad fails exactly at a bad target in S_(r+1). -/
theorem kernel_closed_iff (hf : ∀ x, Valid x → Valid (f x)) (r : Nat) :
    (∀ x, kernel f Valid Bad r x → kernel f Valid Bad r (f x)) ↔
      ∀ y, image f Valid Bad (r + 1) y → ¬ Bad y := by
  constructor
  · intro hclose y hy
    obtain ⟨x, hx, hs, he⟩ := hy
    exact he ▸ (hclose x ⟨hx, hs⟩).2
  · intro hcut x hx
    have hnext : image f Valid Bad (r + 1) (f x) := ⟨x, hx.1, hx.2, rfl⟩
    exact ⟨image_descending f Valid Bad hf r _ hnext, hcut _ hnext⟩

theorem firstBad_exists_of_bad (x : α) (k : Nat) (hb : Bad (iter f x k)) :
    ∃ d, d ≤ k ∧ FirstBad f Bad x d := by
  classical
  induction k using Nat.strongRecOn with
  | ind k ih =>
    by_cases hp : ∃ j, j < k ∧ Bad (iter f x j)
    · obtain ⟨j, hj, hbj⟩ := hp
      obtain ⟨d, hd, hfirst⟩ := ih j hj hbj
      exact ⟨d, by omega, hfirst⟩
    · refine ⟨k, Nat.le_refl _, hb, ?_⟩
      intro j hj hbj
      exact hp ⟨j, hj, hbj⟩

/-- The safety of a sufficiently long finite prefix and a uniform bound
on finite first-bad times certify this particular orbit for all time. -/
theorem avoids_of_finite_bound (r : Nat)
    (hbound : ∀ x d, Valid x → FirstBad f Bad x d → d < r)
    (x : α) (hx : Valid x) (hsafe : SafePrefix f Bad x r) :
    ∀ k, ¬ Bad (iter f x k) := by
  intro k hb
  obtain ⟨d, _, hfirst⟩ := firstBad_exists_of_bad f Bad x k hb
  exact hsafe d (hbound x d hx hfirst) hfirst.1

#print axioms image_iff
#print axioms image_bad_iff
#print axioms firstBad_downward
#print axioms cutoff_iff_finite_bound
#print axioms image_descending
#print axioms kernel_descending
#print axioms kernel_closed_iff
#print axioms avoids_of_finite_bound

end SafeImageDynamics
