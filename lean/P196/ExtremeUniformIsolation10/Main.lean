/-!
# Audit E: extreme uniform lattice predecessor isolation, base 10, EVERY overflow word

Formalises the core of `results/E2ExtremeUniformIsolation.md` for base `b = 10`
(the note proves it for every base on paper; this file is the base-10 instance, for all words).

Model (position automaton of `bauto5` / `agent10_e2_p24.cpp`, one position, `p = gs.length` times).
A predecessor of a target cut state `(L', H', Y')` is a cyclic trajectory of triples
`(x_t, l_t, y_t)`: pair coefficient `x_t`, lower carry `l_t`, previous overflow digit `y_t`
(`y_t` is only meaningful at overflow times `g_t = true`; at `g_t = false` it is fixed to `0`).
With the target's lower carry `L2`, demanded carry `c` and overflow digit `Y2`:

* `(x_t + l_t) / 10 = L2`,
* at an overflow time `(x_t + c) % 10 = Y2`,
* `x_{t+1} = (x_t + l_t) % 10 + (g_t ? y_t : (x_t + c) % 10)`,  and `x_p = x_0`.

The predecessor cut state is `L_t = l_t`, `H_t = (x_t + c) / 10`, `Y = y_t` at overflow times,
so a unique trajectory means a unique predecessor.

Targets: `u = 0`  is `(L2, c, Y2) = (0, 0, 0)`;  `u = 18` is `(1, 1, 9)`.

Claim proved (no `sorry`, no axioms beyond the core ones, `decide`/induction only):
for every `Bool` word `gs` the only closed trajectory into the target is the constant one
(`x = 0, l = 0, y = 0`  resp.  `x = 18, l = 1, y = 9 at overflow / 0 elsewhere`), and it exists.

NOT claimed: reachability of the target from the root (separate easy argument in the note),
other bases, nonuniform lattices.
-/

set_option synthInstance.maxSize 4096
set_option synthInstance.maxHeartbeats 400000
set_option maxRecDepth 100000

namespace AuditE

abbrev Tr := Nat × Nat × Nat

/-- Next pair coefficient. -/
def nxt (c : Nat) (g : Bool) (e : Tr) : Nat :=
  (e.1 + e.2.1) % 10 + (if g then e.2.2 else (e.1 + c) % 10)

/-- Local admissibility of one triple at one time. -/
def ok (L2 c Y2 : Nat) (g : Bool) (e : Tr) : Bool :=
  decide (e.1 ≤ 18) && decide (e.2.1 ≤ 1) && decide ((e.1 + e.2.1) / 10 = L2) &&
  (if g then decide ((e.1 + c) % 10 = Y2) && decide (e.2.2 ≤ 9) else decide (e.2.2 = 0))

/-- Follow a trajectory; `some x'` is the pair coefficient after the last step. -/
def walk (L2 c Y2 : Nat) : List Bool → List Tr → Nat → Option Nat
  | [], [], x => some x
  | g :: gs, e :: es, x =>
      if e.1 = x ∧ ok L2 c Y2 g e = true then walk L2 c Y2 gs es (nxt c g e) else none
  | _, _, _ => none

/-! ## u = 0 -/

def canon0 (gs : List Bool) : List Tr := gs.map fun _ => (0, 0, 0)

theorem loc0 : ∀ g : Bool, ∀ x, x < 19 → ∀ l, l < 2 → ∀ y, y < 10 →
    ok 0 0 0 g (x, l, y) = true →
      x ≤ nxt 0 g (x, l, y) ∧ (nxt 0 g (x, l, y) ≤ x → (x, l, y) = (0, 0, 0)) := by
  intro g; cases g <;> decide

theorem walk0_mono : ∀ (gs : List Bool) (tr : List Tr) (x x' : Nat),
    walk 0 0 0 gs tr x = some x' → x ≤ x' ∧ (x' ≤ x → tr = canon0 gs)
  | [], [], x, x', h => by
      simp [walk] at h; subst h; exact ⟨Nat.le_refl _, fun _ => rfl⟩
  | [], _ :: _, x, x', h => by simp [walk] at h
  | _ :: _, [], x, x', h => by simp [walk] at h
  | g :: gs, e :: es, x, x', h => by
      obtain ⟨xe, l, y⟩ := e
      simp only [walk] at h
      split at h
      · rename_i hc
        obtain ⟨hx, hok⟩ := hc
        have hx' : xe = x := hx
        subst hx'
        have hb : xe < 19 ∧ l < 2 ∧ y < 10 := by
          revert hok; cases g <;> simp [ok] <;> omega
        have hl := loc0 g xe hb.1 l hb.2.1 y hb.2.2 hok
        obtain ⟨ih1, ih2⟩ := walk0_mono gs es _ x' h
        refine ⟨Nat.le_trans hl.1 ih1, fun hle => ?_⟩
        have h1 : nxt 0 g (xe, l, y) ≤ xe := Nat.le_trans ih1 hle
        have h2 := hl.2 h1
        have h3 : x' ≤ nxt 0 g (xe, l, y) := by
          have := hl.1; omega
        have h4 := ih2 h3
        simp only [canon0, List.map_cons]
        rw [h2]
        simp only [canon0] at h4
        rw [h4]
      · simp at h

theorem canon0_walk : ∀ gs : List Bool, walk 0 0 0 gs (canon0 gs) 0 = some 0
  | [] => rfl
  | g :: gs => by
      have ih := canon0_walk gs
      cases g <;> simp [walk, canon0, ok, nxt] at ih ⊢ <;> exact ih

/-- For every overflow word the unique cyclic trajectory into the all-zero target is the zero one. -/
theorem unique_pred_zero (gs : List Bool) (tr : List Tr) (x0 : Nat)
    (h : walk 0 0 0 gs tr x0 = some x0) : tr = canon0 gs :=
  (walk0_mono gs tr x0 x0 h).2 (Nat.le_refl _)

/-! ## u = 18 -/

def canon18 (gs : List Bool) : List Tr := gs.map fun g => (18, 1, if g then 9 else 0)

theorem loc18 : ∀ g : Bool, ∀ x, x < 19 → ∀ l, l < 2 → ∀ y, y < 10 →
    ok 1 1 9 g (x, l, y) = true →
      nxt 1 g (x, l, y) ≤ x ∧
        (x ≤ nxt 1 g (x, l, y) → (x, l, y) = (18, 1, if g then 9 else 0)) := by
  intro g; cases g <;> decide

theorem walk18_mono : ∀ (gs : List Bool) (tr : List Tr) (x x' : Nat),
    walk 1 1 9 gs tr x = some x' → x' ≤ x ∧ (x ≤ x' → tr = canon18 gs)
  | [], [], x, x', h => by
      simp [walk] at h; subst h; exact ⟨Nat.le_refl _, fun _ => rfl⟩
  | [], _ :: _, x, x', h => by simp [walk] at h
  | _ :: _, [], x, x', h => by simp [walk] at h
  | g :: gs, e :: es, x, x', h => by
      obtain ⟨xe, l, y⟩ := e
      simp only [walk] at h
      split at h
      · rename_i hc
        obtain ⟨hx, hok⟩ := hc
        have hx' : xe = x := hx
        subst hx'
        have hb : xe < 19 ∧ l < 2 ∧ y < 10 := by
          revert hok; cases g <;> simp [ok] <;> omega
        have hl := loc18 g xe hb.1 l hb.2.1 y hb.2.2 hok
        obtain ⟨ih1, ih2⟩ := walk18_mono gs es _ x' h
        refine ⟨Nat.le_trans ih1 hl.1, fun hle => ?_⟩
        have h1 : xe ≤ nxt 1 g (xe, l, y) := Nat.le_trans hle ih1
        have h2 := hl.2 h1
        have h3 : nxt 1 g (xe, l, y) ≤ x' := by
          have := hl.1; omega
        have h4 := ih2 h3
        simp only [canon18, List.map_cons]
        rw [h2]
        simp only [canon18] at h4
        rw [h4]
      · simp at h

theorem canon18_walk : ∀ gs : List Bool, walk 1 1 9 gs (canon18 gs) 18 = some 18
  | [] => rfl
  | g :: gs => by
      have ih := canon18_walk gs
      cases g <;> simp [walk, canon18, ok, nxt] at ih ⊢ <;> exact ih

theorem unique_pred_top (gs : List Bool) (tr : List Tr) (x0 : Nat)
    (h : walk 1 1 9 gs tr x0 = some x0) : tr = canon18 gs :=
  (walk18_mono gs tr x0 x0 h).2 (Nat.le_refl _)

end AuditE

#print axioms AuditE.unique_pred_zero
#print axioms AuditE.unique_pred_top
#print axioms AuditE.canon0_walk
#print axioms AuditE.canon18_walk
