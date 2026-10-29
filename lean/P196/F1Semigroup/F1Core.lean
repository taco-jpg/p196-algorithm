/-!
# Audit formalization, part 1: the base-10 first-coordinate (F1) automaton and its relation semigroup

Self-contained (Lean core only; no Mathlib, no sorry, no native_decide, no new axioms).

Spec (from `calculation/decimal_frontier/exterior_census/EXTERIOR.md` section 2.1): states `x ∈ 1..18`,
letter `g ∈ {0,1}`, free bit `h ∈ {0,1}`; an edge `x --g--> y` exists iff `(x+h)/10 = g` and
`y = x % 10 + (if g = 1 then 1 else (x+h) % 10)` (and `1 ≤ y ≤ 18`).
A *cyclic* word `w` is F1-accepted iff some closed walk `x --w--> x` exists.
-/
namespace F1

/-- Specification of one NFA edge. -/
def Step (a : Bool) (x y : Nat) : Prop :=
  1 ≤ x ∧ x ≤ 18 ∧ 1 ≤ y ∧ y ≤ 18 ∧
    ∃ h, h < 2 ∧ (x + h) / 10 = (if a then 1 else 0) ∧ y = x % 10 + (if a then 1 else (x + h) % 10)

instance (a : Bool) (x y : Nat) : Decidable (Step a x y) := by
  unfold Step; exact inferInstance

/-- Walks labelled by a word (specification). -/
def Reach : List Bool → Nat → Nat → Prop
  | [], x, y => x = y
  | a :: w, x, z => ∃ y, Step a x y ∧ Reach w y z

/-- The language: the cyclic word `w` has a closed walk (specification). -/
def Lang (w : List Bool) : Prop := ∃ x, 1 ≤ x ∧ x ≤ 18 ∧ Reach w x x

/-! ## Boolean-relation implementation: 18 bit-masks -/

/-- Edge table: `tab a` has, at index `k`, the mask of targets `y-1` of the edges from `k+1`. -/
def tab (a : Bool) : List Nat :=
  if a then [0, 0, 0, 0, 0, 0, 0, 0, 512, 1, 2, 4, 8, 16, 32, 64, 128, 256]
  else [6, 24, 96, 384, 1536, 6144, 24576, 98304, 131072, 0, 0, 0, 0, 0, 0, 0, 0, 0]

/-- The table is exactly the specification (finite check, 2*18*18 cases). -/
theorem tab_correct :
    ∀ a : Bool, ∀ k, k < 18 → ∀ j, j < 18 →
      (((tab a).getD k 0).testBit j = true ↔ Step a (k + 1) (j + 1)) := by
  decide +kernel

/-- image of the set `m` (a mask) under a table of masks, using the first `n` indices -/
def postN (T : List Nat) (m : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => postN T m n ||| (if m.testBit n then T.getD n 0 else 0)

theorem postN_testBit (T : List Nat) (m : Nat) (n j : Nat) :
    (postN T m n).testBit j = true ↔ ∃ k, k < n ∧ m.testBit k = true ∧ (T.getD k 0).testBit j = true := by
  induction n with
  | zero => simp [postN]
  | succ n ih =>
    simp only [postN, Nat.testBit_or, Bool.or_eq_true, ih]
    constructor
    · rintro (⟨k, hk, h1, h2⟩ | h)
      · exact ⟨k, by omega, h1, h2⟩
      · by_cases hm : m.testBit n = true
        · simp [hm] at h; exact ⟨n, by omega, hm, h⟩
        · simp [hm] at h
    · rintro ⟨k, hk, h1, h2⟩
      by_cases hkn : k = n
      · subst hkn; right; rw [if_pos h1]; exact h2
      · left; exact ⟨k, by omega, h1, h2⟩

/-- `postN T m 18`, unrolled (cheap for the kernel) -/
def post18 (T : List Nat) (m : Nat) : Nat :=
  let f := fun k => if m.testBit k then T.getD k 0 else 0
  f 0 ||| f 1 ||| f 2 ||| f 3 ||| f 4 ||| f 5 ||| f 6 ||| f 7 ||| f 8 |||
  f 9 ||| f 10 ||| f 11 ||| f 12 ||| f 13 ||| f 14 ||| f 15 ||| f 16 ||| f 17

theorem post18_eq (T : List Nat) (m : Nat) : post18 T m = postN T m 18 := by
  simp [post18, postN]

def img0 (m : Nat) : Nat :=
  ((m >>> 0) % 2 * 6) |||
  ((m >>> 1) % 2 * 24) |||
  ((m >>> 2) % 2 * 96) |||
  ((m >>> 3) % 2 * 384) |||
  ((m >>> 4) % 2 * 1536) |||
  ((m >>> 5) % 2 * 6144) |||
  ((m >>> 6) % 2 * 24576) |||
  ((m >>> 7) % 2 * 98304) |||
  ((m >>> 8) % 2 * 131072)

def img1 (m : Nat) : Nat :=
  ((m >>> 8) % 2 * 512) |||
  ((m >>> 9) % 2 * 1) |||
  ((m >>> 10) % 2 * 2) |||
  ((m >>> 11) % 2 * 4) |||
  ((m >>> 12) % 2 * 8) |||
  ((m >>> 13) % 2 * 16) |||
  ((m >>> 14) % 2 * 32) |||
  ((m >>> 15) % 2 * 64) |||
  ((m >>> 16) % 2 * 128) |||
  ((m >>> 17) % 2 * 256)

theorem ite_bit (m k c : Nat) : (if m.testBit k then c else 0) = (m >>> k) % 2 * c := by
  have h : m.testBit k = decide ((m >>> k) % 2 = 1) := by
    simp [Nat.testBit, Nat.and_one_is_mod]
  rcases Nat.mod_two_eq_zero_or_one (m >>> k) with h0 | h1
  · simp [h, h0]
  · simp [h, h1]

/-- fast image of a mask under the edge table of letter `a` -/
def img (a : Bool) (m : Nat) : Nat := if a then img1 m else img0 m

theorem img_eq (a : Bool) (m : Nat) : img a m = postN (tab a) m 18 := by
  simp only [postN, ite_bit]
  cases a <;> simp [img, img0, img1, tab, List.getD_eq_getElem?_getD]

abbrev Rel := List Nat

def row (r : Rel) (i : Nat) : Nat := r.getD i 0

/-- relation product: rows of `A` pushed through the table `B` -/
def mmul (A B : Rel) : Rel := A.map (fun m => post18 B m)

/-- one automaton step on a relation state -/
def delta (a : Bool) (r : Rel) : Rel := r.map (fun m => img a m)

def initRel : Rel := (List.range 18).map (fun i => 2 ^ i)

def run (r : Rel) (w : List Bool) : Rel := w.foldl (fun s a => delta a s) r

def accept (r : Rel) : Bool := (List.range 18).any (fun i => (row r i).testBit i)

/-- The language computed by the relation automaton. -/
def LangB (w : List Bool) : Bool := accept (run initRel w)

theorem row_map (r : Rel) (f : Nat → Nat) (hf : f 0 = 0) (i : Nat) :
    row (r.map f) i = f (row r i) := by
  unfold row
  by_cases h : i < r.length
  · simp [List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_eq_getElem h]
  · have : r[i]? = none := by simp; omega
    simp [List.getD_eq_getElem?_getD, List.getElem?_map, this, hf]

theorem postN_zero (T : List Nat) (n : Nat) : postN T 0 n = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [postN, ih]

theorem length_delta (a : Bool) (r : Rel) : (delta a r).length = r.length := by simp [delta]

theorem length_run (r : Rel) (w : List Bool) : (run r w).length = r.length := by
  induction w generalizing r with
  | nil => rfl
  | cons a w ih => simp only [run, List.foldl_cons] at *; rw [ih]; exact length_delta a r

theorem length_init : initRel.length = 18 := by decide

/-- Soundness/completeness of the row semantics of `run`. -/
theorem run_rows (w : List Bool) : ∀ (r : Rel), r.length = 18 → ∀ x, x < 18 → ∀ y, y < 18 →
    ((row (run r w) x).testBit y = true ↔
      ∃ y0, y0 < 18 ∧ (row r x).testBit y0 = true ∧ Reach w (y0 + 1) (y + 1)) := by
  induction w with
  | nil =>
    intro r _ x _ y hy
    simp only [run, List.foldl_nil, Reach]
    constructor
    · intro h; exact ⟨y, hy, h, rfl⟩
    · rintro ⟨y0, _, h, e⟩
      have : y0 = y := by omega
      subst this; exact h
  | cons a w ih =>
    intro r hr x hx y hy
    have hr' : (delta a r).length = 18 := by rw [length_delta]; exact hr
    have e : run r (a :: w) = run (delta a r) w := rfl
    rw [e, ih (delta a r) hr' x hx y hy]
    have hrow : row (delta a r) x = postN (tab a) (row r x) 18 := by
      unfold delta
      rw [row_map r (fun m => img a m) (by show img a 0 = 0; rw [img_eq]; exact postN_zero _ _) x]
      exact img_eq _ _
    constructor
    · rintro ⟨y1, hy1, h1, h2⟩
      rw [hrow, postN_testBit] at h1
      obtain ⟨k, hk, hb, ht⟩ := h1
      refine ⟨k, hk, hb, y1 + 1, ?_, h2⟩
      exact (tab_correct a k hk y1 hy1).1 ht
    · rintro ⟨y0, hy0, hb, y1, hs, hr1⟩
      have hr1' : 1 ≤ y1 ∧ y1 ≤ 18 := by obtain ⟨_, _, h1, h2, _⟩ := hs; exact ⟨h1, h2⟩
      have e1 : y1 - 1 + 1 = y1 := by omega
      refine ⟨y1 - 1, by omega, ?_, by rw [e1]; exact hr1⟩
      rw [hrow, postN_testBit]
      refine ⟨y0, hy0, hb, ?_⟩
      apply (tab_correct a y0 hy0 (y1 - 1) (by omega)).2
      have : y1 - 1 + 1 = y1 := by omega
      rw [this]; exact hs

theorem init_row (x : Nat) (hx : x < 18) (y : Nat) :
    (row initRel x).testBit y = true ↔ y = x := by
  have : row initRel x = 2 ^ x := by
    unfold row initRel
    simp [List.getD_eq_getElem?_getD, hx]
  rw [this, Nat.testBit_two_pow]
  simp [eq_comm]

/-- Main semantic theorem: the relation automaton computes exactly the spec language. -/
theorem LangB_iff (w : List Bool) : LangB w = true ↔ Lang w := by
  unfold LangB accept
  simp only [List.any_eq_true, List.mem_range]
  constructor
  · rintro ⟨i, hi, h⟩
    rw [run_rows w initRel length_init i hi i hi] at h
    obtain ⟨y0, hy0, hb, hr⟩ := h
    rw [init_row i hi] at hb
    subst hb
    exact ⟨y0 + 1, by omega, by omega, hr⟩
  · rintro ⟨x, hx1, hx2, hr⟩
    refine ⟨x - 1, by omega, ?_⟩
    rw [run_rows w initRel length_init (x - 1) (by omega) (x - 1) (by omega)]
    refine ⟨x - 1, by omega, (init_row (x-1) (by omega) (x-1)).2 rfl, ?_⟩
    have : x - 1 + 1 = x := by omega
    rw [this]; exact hr

end F1
