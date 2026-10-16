import Lean

/-!
An all-width obstruction in the exact N/O spatial cut relation.
No native evaluation, custom axiom, or admitted proof is used.
The connection to an actual exterior is a separate bridge obligation.
-/
namespace Agent9.AlternatingScalarBoundary

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

structure Slot where
  a : Int
  b : Int
  c : Int
  z : Int
  deriving DecidableEq, Repr

theorem slot_ext (x y : Slot) (ha : x.a = y.a) (hb : x.b = y.b)
    (hc : x.c = y.c) (hz : x.z = y.z) : x = y := by
  cases x
  cases y
  simp_all

def Valid (s : Slot) : Prop :=
  0 ≤ s.a ∧ s.a ≤ 1 ∧ 0 ≤ s.b ∧ s.b ≤ 1 ∧
  0 ≤ s.c ∧ s.c ≤ 1 ∧ -1 ≤ s.z ∧ s.z ≤ 9

/-- The exact local inverse equations of the archived N/O cut model. -/
structure Tile (outer inner : Slot) (q r e qNext : Int) : Prop where
  outer_valid : Valid outer
  inner_valid : Valid inner
  q_bounds : 0 ≤ q ∧ q ≤ 18
  r_bounds : 0 ≤ r ∧ r ≤ 18
  e_bounds : 0 ≤ e ∧ e ≤ 1
  r_value : r = inner.z + 10*e
  low_forces : r < 9 → e = 0
  high_forces : 9 < r → e = 1
  low_n : (q + outer.a) / 10 = inner.a
  n_emission : (q + outer.a) % 10 + (q + inner.c) % 10 = r
  low_o : (r + outer.b) / 10 = inner.b
  high_n : outer.c = (q + inner.c) / 10
  o_emission : qNext = (r + outer.b) % 10 + outer.z + e
  pending_digit : 0 ≤ outer.z + e ∧ outer.z + e ≤ 9

def six : Slot := ⟨0,1,0,2⟩
def sixBad : Slot := ⟨0,0,0,3⟩
def twelve : Slot := ⟨1,0,1,6⟩
def twelveBad : Slot := ⟨1,1,1,5⟩
def root : Slot := ⟨0,1,1,7⟩

/-- Local options at the 6/12 scalar-bulk cut. -/
theorem six_fiber (x : Slot) (q r e qNext : Int)
    (h : Tile x six q r e qNext) :
    q = 6 ∧ r = 12 ∧ e = 1 ∧ x.a = 0 ∧ x.c = 0 := by
  rcases h with ⟨ho,hi,hq,hr,he,hv,hl,hh,hn,hnorm,hb,hc,hemit,hpend⟩
  simp only [six] at *
  unfold Valid at ho hi
  omega

theorem sixBad_fiber (x : Slot) (q r e qNext : Int)
    (h : Tile x sixBad q r e qNext) :
    q = 1 ∧ r = 3 ∧ e = 0 ∧ x.a = 1 ∧ x.c = 0 := by
  rcases h with ⟨ho,hi,hq,hr,he,hv,hl,hh,hn,hnorm,hb,hc,hemit,hpend⟩
  simp only [sixBad] at *
  unfold Valid at ho hi
  omega

theorem twelve_fiber (x : Slot) (q r e qNext : Int)
    (h : Tile x twelve q r e qNext) :
    q = 12 ∧ r = 6 ∧ e = 0 ∧ x.a = 1 ∧ x.c = 1 := by
  rcases h with ⟨ho,hi,hq,hr,he,hv,hl,hh,hn,hnorm,hb,hc,hemit,hpend⟩
  simp only [twelve] at *
  unfold Valid at ho hi
  omega

theorem twelveBad_fiber (x : Slot) (q r e qNext : Int)
    (h : Tile x twelveBad q r e qNext) :
    q = 17 ∧ r = 15 ∧ e = 1 ∧ x.a = 0 ∧ x.c = 1 := by
  rcases h with ⟨ho,hi,hq,hr,he,hv,hl,hh,hn,hnorm,hb,hc,hemit,hpend⟩
  simp only [twelveBad] at *
  unfold Valid at ho hi
  omega

abbrev Trace := Nat → Slot

def constant (s : Slot) : Trace := fun _ => s

/-- One spatial column, with exact consecutive N/O temporal equations. -/
def Step (outer inner : Trace) : Prop :=
  ∃ q r e : Nat → Int, ∀ j, Tile (outer j) (inner j) (q j) (r j) (e j) (q (j+1))

/-- A predecessor of the first scalar trace has only two possible letters. -/
theorem predecessor_six (x : Trace) (h : Step x (constant six)) (j : Nat) :
    x j = six ∨ x j = sixBad := by
  obtain ⟨q,r,e,ht⟩ := h
  have h0 := ht j
  have f0 := six_fiber (x j) (q j) (r j) (e j) (q (j+1)) h0
  have f1 := six_fiber (x (j+1)) (q (j+1)) (r (j+1)) (e (j+1)) (q (j+1+1)) (ht (j+1))
  have hv := h0.outer_valid
  have he := h0.o_emission
  unfold Valid at hv
  by_cases hb : (x j).b = 1
  · left
    apply slot_ext <;> simp only [six] <;> omega
  · right
    apply slot_ext <;> simp only [sixBad] <;> omega

theorem predecessor_twelve (x : Trace) (h : Step x (constant twelve)) (j : Nat) :
    x j = twelve ∨ x j = twelveBad := by
  obtain ⟨q,r,e,ht⟩ := h
  have h0 := ht j
  have f0 := twelve_fiber (x j) (q j) (r j) (e j) (q (j+1)) h0
  have f1 := twelve_fiber (x (j+1)) (q (j+1)) (r (j+1)) (e (j+1)) (q (j+1+1)) (ht (j+1))
  have hv := h0.outer_valid
  have he := h0.o_emission
  unfold Valid at hv
  by_cases hb : (x j).b = 0
  · left
    apply slot_ext <;> simp only [twelve] <;> omega
  · right
    apply slot_ext <;> simp only [twelveBad] <;> omega

/-- A second predecessor removes the exceptional letter after one temporal shift. -/
theorem viable_predecessor_six (p x : Trace) (hp : Step p x)
    (hx : Step x (constant six)) (j : Nat) : x (j+1) = six := by
  have hx0 := predecessor_six x hx j
  have hx1 := predecessor_six x hx (j+1)
  rcases hx1 with hgood | hbad
  · exact hgood
  · obtain ⟨q,r,e,ht⟩ := hp
    have h0 := ht j
    have h1 : Tile (p (j+1)) sixBad (q (j+1)) (r (j+1)) (e (j+1)) (q (j+1+1)) := by
      simpa only [hbad] using ht (j+1)
    have f1 := sixBad_fiber _ _ _ _ _ h1
    have hb := h0.outer_valid
    have he := h0.o_emission
    have hd := h0.pending_digit
    unfold Valid at hb
    rcases hx0 with hgood0 | hbad0
    · have f0 := six_fiber _ _ _ _ _ (by simpa only [hgood0] using h0)
      omega
    · have f0 := sixBad_fiber _ _ _ _ _ (by simpa only [hbad0] using h0)
      omega

theorem viable_predecessor_twelve (p x : Trace) (hp : Step p x)
    (hx : Step x (constant twelve)) (j : Nat) : x (j+1) = twelve := by
  have hx0 := predecessor_twelve x hx j
  have hx1 := predecessor_twelve x hx (j+1)
  rcases hx1 with hgood | hbad
  · exact hgood
  · obtain ⟨q,r,e,ht⟩ := hp
    have h0 := ht j
    have h1 : Tile (p (j+1)) twelveBad (q (j+1)) (r (j+1)) (e (j+1)) (q (j+1+1)) := by
      simpa only [hbad] using ht (j+1)
    have f1 := twelveBad_fiber _ _ _ _ _ h1
    have hb := h0.outer_valid
    have he := h0.o_emission
    have hd := h0.pending_digit
    unfold Valid at hb
    rcases hx0 with hgood0 | hbad0
    · have f0 := twelve_fiber _ _ _ _ _ (by simpa only [hgood0] using h0)
      omega
    · have f0 := twelveBad_fiber _ _ _ _ _ (by simpa only [hbad0] using h0)
      omega


def shift (x : Trace) : Trace := fun j => x (j+1)

theorem step_shift (x y : Trace) (h : Step x y) : Step (shift x) (shift y) := by
  obtain ⟨q,r,e,ht⟩ := h
  exact ⟨(fun j => q (j+1)), (fun j => r (j+1)), (fun j => e (j+1)), fun j => ht (j+1)⟩

/-- A generic finite-spatial-path exclusion from one-shift reverse rigidity.
The temporal traces are arbitrary forward-infinite traces, not assumed periodic. -/
theorem no_finite_path (s bad outside : Slot)
    (hr : outside ≠ s ∧ outside ≠ bad)
    (hpre : ∀ x, Step x (constant s) → ∀ j, x j = s ∨ x j = bad)
    (herase : ∀ p x, Step p x → Step x (constant s) → ∀ j, x (j+1) = s)
    (n : Nat) (cols : Nat → Trace)
    (hroot : cols 0 = constant outside)
    (htail : cols n = constant s)
    (hpath : ∀ i, i < n → Step (cols i) (cols (i+1))) : False := by
  induction n generalizing cols with
  | zero =>
      have h : outside = s := congrFun (hroot.symm.trans htail) 0
      exact hr.1 h
  | succ n ih =>
      by_cases hn : n = 0
      · subst n
        have hs : Step (constant outside) (constant s) := by
          simpa only [hroot, htail] using hpath 0 (by omega)
        rcases hpre (constant outside) hs 0 with h | h
        · exact hr.1 h
        · exact hr.2 h
      · have hlast : Step (cols n) (constant s) := by
          simpa only [htail] using hpath n (by omega)
        have hprior : Step (cols (n-1)) (cols n) := by
          have h := hpath (n-1) (by omega)
          simpa only [show n-1+1=n by omega] using h
        have hc : shift (cols n) = constant s := by
          funext j
          exact herase (cols (n-1)) (cols n) hprior hlast j
        apply ih (fun i => shift (cols i))
        · change shift (cols 0) = constant outside
          rw [hroot]
          rfl
        · exact hc
        · intro i hi
          exact step_shift _ _ (hpath i (by omega))

/-- No finite-width boundary can join the 8/17 root to the 6/12 scalar trace. -/
theorem no_six_boundary (n : Nat) (cols : Nat → Trace)
    (hroot : cols 0 = constant root) (htail : cols n = constant six)
    (hpath : ∀ i, i < n → Step (cols i) (cols (i+1))) : False := by
  exact no_finite_path six sixBad root (by decide) predecessor_six
    viable_predecessor_six n cols hroot htail hpath

theorem no_twelve_boundary (n : Nat) (cols : Nat → Trace)
    (hroot : cols 0 = constant root) (htail : cols n = constant twelve)
    (hpath : ∀ i, i < n → Step (cols i) (cols (i+1))) : False := by
  exact no_finite_path twelve twelveBad root (by decide) predecessor_twelve
    viable_predecessor_twelve n cols hroot htail hpath

#print axioms slot_ext
#print axioms six_fiber
#print axioms sixBad_fiber
#print axioms twelve_fiber
#print axioms twelveBad_fiber
#print axioms predecessor_six
#print axioms predecessor_twelve
#print axioms viable_predecessor_six
#print axioms viable_predecessor_twelve
#print axioms step_shift
#print axioms no_finite_path
#print axioms no_six_boundary
#print axioms no_twelve_boundary

end Agent9.AlternatingScalarBoundary
