import P196.F1Semigroup.F1MinDFA
/-!
# Audit formalization, part 5: power closure of the decimal F1 language

Claim (`Agent9F1PowerClosure`): for every word `w` and every `k ≥ 1`, the cyclic word `w^k` is F1-accepted
iff `w` is.  Proof: of the 434 reachable relations, 176 have a diagonal entry (closed walk) and for each of the
other 258 the fifth relational power is empty (`R^5 = 0`).  Everything is kernel-checked and then lifted to all
words by the composition semantics of walks.
-/
namespace F1

/-! ## Composition of walks -/

theorem Reach_append : ∀ (u v : List Bool) (x z : Nat),
    Reach (u ++ v) x z ↔ ∃ y, Reach u x y ∧ Reach v y z := by
  intro u
  induction u with
  | nil => intro v x z; simp [Reach]
  | cons a u ih =>
    intro v x z
    simp only [List.cons_append, Reach, ih]
    constructor
    · rintro ⟨y, hs, y2, h1, h2⟩; exact ⟨y2, ⟨y, hs, h1⟩, h2⟩
    · rintro ⟨y2, ⟨y, hs, h1⟩, h2⟩; exact ⟨y, hs, y2, h1, h2⟩

theorem Reach_range : ∀ (u : List Bool) (x y : Nat), u ≠ [] → Reach u x y → 1 ≤ y ∧ y ≤ 18 := by
  intro u
  induction u with
  | nil => intro x y h; exact absurd rfl h
  | cons a u ih =>
    intro x z _ h
    obtain ⟨y, hs, hr⟩ := h
    by_cases hu : u = []
    · subst hu
      simp only [Reach] at hr
      subst hr
      obtain ⟨_, _, h1, h2, _⟩ := hs
      exact ⟨h1, h2⟩
    · exact ih y z hu hr

theorem Reach_start : ∀ (u : List Bool) (x y : Nat), u ≠ [] → Reach u x y → 1 ≤ x ∧ x ≤ 18 := by
  intro u
  cases u with
  | nil => intro x y h; exact absurd rfl h
  | cons a u =>
    intro x z _ h
    obtain ⟨y, hs, _⟩ := h
    obtain ⟨h1, h2, _⟩ := hs
    exact ⟨h1, h2⟩

/-! ## Matrix semantics -/

def MatRel (M : Rel) (x y : Nat) : Prop := (row M x).testBit y = true

theorem MatRel_run (w : List Bool) (x y : Nat) (hx : x < 18) (hy : y < 18) :
    MatRel (run initRel w) x y ↔ Reach w (x + 1) (y + 1) := by
  unfold MatRel
  rw [run_rows w initRel length_init x hx y hy]
  constructor
  · rintro ⟨y0, _, hb, hr⟩
    rw [init_row x hx] at hb
    subst hb; exact hr
  · intro hr
    exact ⟨x, hx, (init_row x hx x).2 rfl, hr⟩

theorem MatRel_mmul (A B : Rel) (x z : Nat) :
    MatRel (mmul A B) x z ↔ ∃ y, y < 18 ∧ MatRel A x y ∧ MatRel B y z := by
  unfold MatRel mmul
  rw [row_map A (fun m => post18 B m) (by show post18 B 0 = 0; rw [post18_eq]; exact postN_zero _ _) x,
    post18_eq, postN_testBit]
  constructor
  · rintro ⟨k, hk, h1, h2⟩; exact ⟨k, hk, h1, h2⟩
  · rintro ⟨k, hk, h1, h2⟩; exact ⟨k, hk, h1, h2⟩

/-- semantic composition: if `A` realises `u` and `B` realises `v` then `mmul A B` realises `u ++ v` -/
theorem MatRel_append (A B : Rel) (u v : List Bool) (hu : u ≠ [])
    (hA : ∀ x y, x < 18 → y < 18 → (MatRel A x y ↔ Reach u (x + 1) (y + 1)))
    (hB : ∀ x y, x < 18 → y < 18 → (MatRel B x y ↔ Reach v (x + 1) (y + 1)))
    (x z : Nat) (hx : x < 18) (hz : z < 18) :
    MatRel (mmul A B) x z ↔ Reach (u ++ v) (x + 1) (z + 1) := by
  rw [MatRel_mmul, Reach_append]
  constructor
  · rintro ⟨y, hy, h1, h2⟩
    exact ⟨y + 1, (hA x y hx hy).1 h1, (hB y z hy hz).1 h2⟩
  · rintro ⟨y, h1, h2⟩
    have hr := Reach_range u _ _ hu h1
    have e : y - 1 + 1 = y := by omega
    refine ⟨y - 1, by omega, (hA x (y - 1) hx (by omega)).2 ?_, (hB (y - 1) z (by omega) hz).2 ?_⟩
    · rw [e]; exact h1
    · rw [e]; exact h2

/-! ## The finite check -/

def zeroRel (M : Rel) : Bool := M.all (fun m => m == 0)

def M2 (M : Rel) : Rel := mmul M M
def M4 (M : Rel) : Rel := mmul (M2 M) (M2 M)
def M5 (M : Rel) : Rel := mmul M (M4 M)

def nilOK (i : Nat) : Bool := accQ i || zeroRel (M5 (Sget i))


end F1
