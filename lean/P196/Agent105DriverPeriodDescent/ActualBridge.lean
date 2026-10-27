import P196.Agent105DriverPeriodDescent.FiniteGraph
import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# The actual exterior equations produce a path in the carry graph

This file bridges the list-valued normalization and exterior-update definitions
to `FiniteGraph`.  It does not impose a width bound.  Peeling one coefficient
from each exterior produces one graph edge; exhausting the two equal-length
lists produces the forbidden terminal state.
-/

namespace Agent105.DriverPeriod

open Agent120.Neutral

private theorem reflected_cons (x c : Nat) (xs : List Nat) :
    (norm 6 (x :: xs).reverse c).1.reverse =
      (x + (norm 6 xs.reverse c).2) % 6 :: (norm 6 xs.reverse c).1.reverse := by
  simp [List.reverse_cons, norm_append, norm_cons]

private theorem reverse_carry_cons (x c : Nat) (xs : List Nat) :
    (norm 6 (x :: xs).reverse c).2 =
      (x + (norm 6 xs.reverse c).2) / 6 := by
  simp [List.reverse_cons, norm_append, norm_cons]

/-- The unprocessed suffixes satisfy the actual two-phase digit equations at
the given spatial cut.  The reverse initial carries are the fixed terminal
values `1-e = (1,0)`. -/
structure Compatible (s : Cut) (X0 X1 : List Nat) : Prop where
  lengths : X0.length = X1.length
  bound0 : ∀ x ∈ X0, x ≤ 10
  bound1 : ∀ x ∈ X1, x ≤ 10
  low0 : (norm 6 X0 s.l0.val).2 = 0
  low1 : (norm 6 X1 s.l1.val).2 = 1
  high0 : (norm 6 X0.reverse 1).2 = s.h0.val
  high1 : (norm 6 X1.reverse 0).2 = s.h1.val
  time0 : X1 = List.zipWith (· + ·) (norm 6 X0 s.l0.val).1
    (norm 6 X0.reverse 1).1.reverse
  time1 : X0 ++ [5] = List.zipWith (· + ·) ((norm 6 X1 s.l1.val).1 ++ [0])
    (s.y.val :: (norm 6 X1.reverse 0).1.reverse)

private theorem compatible_nil {s : Cut} (h : Compatible s [] []) : s = terminal := by
  have hl0 : s.l0.val = 0 := by simpa using h.low0
  have hl1 : s.l1.val = 1 := by simpa using h.low1
  have hh0 : s.h0.val = 1 := by simpa using h.high0.symm
  have hh1 : s.h1.val = 0 := by simpa using h.high1.symm
  have hy : s.y.val = 5 := by
    have he := h.time1
    simpa [List.zipWith] using he.symm
  rcases s with ⟨l0, l1, h0, h1, y⟩
  have el0 : l0 = (0 : Fin 2) := Fin.ext hl0
  have el1 : l1 = (1 : Fin 2) := Fin.ext hl1
  have eh0 : h0 = (1 : Fin 2) := Fin.ext hh0
  have eh1 : h1 = (0 : Fin 2) := Fin.ext hh1
  have ey : y = (5 : Fin 6) := Fin.ext hy
  subst l0; subst l1; subst h0; subst h1; subst y
  rfl

/-- Every finite pair of suffixes satisfying the actual digit equations gives
a finite graph path ending at the prescribed terminal carries. -/
theorem compatible_walk {s : Cut} {X0 X1 : List Nat}
    (h : Compatible s X0 X1) : Walk s terminal := by
  induction X0 generalizing X1 s with
  | nil =>
      have hx : X1 = [] := List.length_eq_zero_iff.mp (by simpa using h.lengths.symm)
      subst X1
      rw [compatible_nil h]
      exact Walk.nil terminal
  | cons a A ih =>
      cases X1 with
      | nil =>
          have hh := h.lengths
          simp at hh
      | cons z Z =>
          have ha : a ≤ 10 := h.bound0 a List.mem_cons_self
          have hz : z ≤ 10 := h.bound1 z List.mem_cons_self
          have hA : ∀ x ∈ A, x ≤ 10 := by
            intro x hx
            exact h.bound0 x (List.mem_cons_of_mem a hx)
          have hZ : ∀ x ∈ Z, x ≤ 10 := by
            intro x hx
            exact h.bound1 x (List.mem_cons_of_mem z hx)
          let l0 : Fin 2 := ⟨(a + s.l0.val) / 6, by have := s.l0.isLt; omega⟩
          let l1 : Fin 2 := ⟨(z + s.l1.val) / 6, by have := s.l1.isLt; omega⟩
          let h0 : Fin 2 := ⟨(norm 6 A.reverse 1).2, by
            have hh := norm_carry_le_one 6 (by decide) A.reverse 1
              (fun x hx => by simpa using hA x (List.mem_reverse.mp hx)) (by decide)
            omega⟩
          let h1 : Fin 2 := ⟨(norm 6 Z.reverse 0).2, by
            have hh := norm_carry_le_one 6 (by decide) Z.reverse 0
              (fun x hx => by simpa using hZ x (List.mem_reverse.mp hx)) (by decide)
            omega⟩
          let y : Fin 6 := ⟨(z + h1.val) % 6, Nat.mod_lt _ (by decide)⟩
          let t : Cut := ⟨l0, l1, h0, h1, y⟩
          have ht0 := h.time0
          simp only [norm_cons, reflected_cons, List.zipWith_cons_cons] at ht0
          have ht1 := h.time1
          simp only [norm_cons, reflected_cons, List.cons_append,
            List.zipWith_cons_cons] at ht1
          have ht0head := (List.cons.inj ht0).1
          have ht0tail := (List.cons.inj ht0).2
          have ht1head := (List.cons.inj ht1).1
          have ht1tail := (List.cons.inj ht1).2
          have hc : Column s t a z := {
            low0 := by rfl
            low1 := by rfl
            high0 := by
              have hh := h.high0.symm
              rw [reverse_carry_cons] at hh
              simpa [t, h0] using hh
            high1 := by
              have hh := h.high1.symm
              rw [reverse_carry_cons] at hh
              simpa [t, h1] using hh
            reverse1 := by rfl
            time0 := by simpa [t, h0] using ht0head
            time1 := by simpa using ht1head
          }
          have ht : Compatible t A Z := {
            lengths := by simpa using h.lengths
            bound0 := hA
            bound1 := hZ
            low0 := by simpa [norm_cons, t, l0] using h.low0
            low1 := by simpa [norm_cons, t, l1] using h.low1
            high0 := by rfl
            high1 := by rfl
            time0 := by simpa [t, l0] using ht0tail
            time1 := by simpa [t, l1, y, h1] using ht1tail
          }
          exact Walk.cons (step_of_column s t a z ha hz hc) (ih ht)

/-- There is no actual fixed-width two-step exterior return with complete
driver `e=g=01`, in base 6.  The centers are arbitrary witnesses of `Hyp`;
their own updates are not assumed. -/
theorem no_fixed_width_two_step (B0 C0 B1 C1 : List Nat)
    (h0 : Hyp 6 B0 C0) (h1 : Hyp 6 B1 C1)
    (hl : B0.length = B1.length)
    (he0 : e1 6 B0 = 0) (he1 : e1 6 B1 = 1)
    (hg0 : gam 6 B0 C0 = 0) (hg1 : gam 6 B1 C1 = 1)
    (hn0 : nextB 6 B0 C0 = B1)
    (hn1 : nextB 6 B1 C1 = B0 ++ [5]) : False := by
  have hf0 : e2 6 B0 C0 = 1 := by
    have hb := h0.e2_le
    have hf := h0.flip
    rw [he0] at hf
    omega
  have hf1 : e2 6 B1 C1 = 0 := by
    have hb := h1.e2_le
    have hf := h1.flip
    rw [he1] at hf
    omega
  have hc : Compatible root B0 B1 := {
    lengths := hl
    bound0 := by simpa using h0.boundB
    bound1 := by simpa using h1.boundB
    low0 := by simpa [root, e1] using he0
    low1 := by simpa [root, e1] using he1
    high0 := by simpa [root, gam, hf0] using hg0
    high1 := by simpa [root, gam, hf1] using hg1
    time0 := by simpa [root, nextB, hg0, DB, DR, hf0] using hn0.symm
    time1 := by simpa [root, nextB, hg1, DB, DR, xd, he1, hf1] using hn1.symm
  }
  exact no_root_terminal (compatible_walk hc)

end Agent105.DriverPeriod
