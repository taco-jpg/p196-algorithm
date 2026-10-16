import Std

/-
Agent #9. Decimal no-overflow folded inverse paths.
Source argument: proofs/research/persist_inverse_fibers_proof.txt,
original source commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
All finite tables below are checked by Lean's kernel, not native_decide.
-/
namespace P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

abbrev State := Fin 4
abbrev Symbol := Fin 19

def low (p : State) : Nat := p.val / 2
def high (p : State) : Nat := p.val % 2

/-- One mirrored column. Low incoming/high outgoing are stored in `p`;
low outgoing/high incoming are stored in `q`. -/
def Local (s : Symbol) (p q : State) (x : Nat) : Prop :=
  x < 19 ∧ (x + low p) / 10 = low q ∧
  (x + high q) / 10 = high p ∧
  (x + low p) % 10 + (x + high q) % 10 = s.val

instance (s : Symbol) (p q : State) (x : Nat) : Decidable (Local s p q x) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

/-- Actual number of arithmetic labels, not a postulated adjacency matrix. -/
def weight (s : Symbol) (p q : State) : Nat :=
  ((List.range 19).filter (fun x => decide (Local s p q x))).length

def table (s : Symbol) (p q : State) : Nat :=
  if s.val = 9 then
    if (p.val,q.val) ∈ [(0,1),(1,1),(1,3),(2,0),(2,2),(3,2)] then 1 else 0
  else if s.val % 2 = 1 then
    if (p.val,q.val) ∈ [(0,1),(1,3),(2,0),(3,2)] then 1 else 0
  else
    if (p.val,q.val) = (0,0) ∨ (p.val,q.val) = (3,3) ∨
       ((p.val,q.val) = (1,2) ∧ s.val ≠ 18) ∨
       ((p.val,q.val) = (2,1) ∧ s.val ≠ 0) then 1 else 0

/-- Exhaustive exact local table: all 19 symbols and 16 state pairs. -/
theorem weight_eq_table : ∀ s : Symbol, ∀ p q : State, weight s p q = table s p q := by
  decide

/-- An arithmetic transition has at most one label. -/
theorem local_unique : ∀ s : Symbol, ∀ p q : State, ∀ x y : Fin 19,
    Local s p q x.val → Local s p q y.val → x = y := by
  intro s p q x y hx hy
  apply Fin.ext
  simp only [Local] at hx hy
  have hlow : low p < 2 := by unfold low; omega
  have hhigh : high q < 2 := Nat.mod_lt _ (by decide)
  have ex := Nat.mod_add_div (x.val + low p) 10
  have ey := Nat.mod_add_div (y.val + low p) 10
  have fx := Nat.mod_add_div (x.val + high q) 10
  have fy := Nat.mod_add_div (y.val + high q) 10
  omega

structure Counts where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
  deriving DecidableEq, Repr

def Counts.U (v : Counts) : Nat := v.a + v.d
def Counts.V (v : Counts) : Nat := v.b + v.c

def advance (s : Symbol) (v : Counts) : Counts :=
  ⟨v.a * weight s 0 0 + v.b * weight s 1 0 + v.c * weight s 2 0 + v.d * weight s 3 0,
   v.a * weight s 0 1 + v.b * weight s 1 1 + v.c * weight s 2 1 + v.d * weight s 3 1,
   v.a * weight s 0 2 + v.b * weight s 1 2 + v.c * weight s 2 2 + v.d * weight s 3 2,
   v.a * weight s 0 3 + v.b * weight s 1 3 + v.c * weight s 2 3 + v.d * weight s 3 3⟩

/-- The exact arithmetic DP in its five symbol classes. -/
theorem advance_formula (s : Symbol) (v : Counts) :
    advance s v =
      if s.val = 9 then ⟨v.c, v.a + v.b, v.c + v.d, v.b⟩
      else if s.val % 2 = 1 then ⟨v.c, v.a, v.d, v.b⟩
      else if s.val = 0 then ⟨v.a, 0, v.b, v.d⟩
      else if s.val = 18 then ⟨v.a, v.c, 0, v.d⟩
      else ⟨v.a, v.c, v.b, v.d⟩ := by
  simp only [advance, weight_eq_table]
  by_cases h9 : s.val = 9
  · simp [show (3 : State).val = 3 from rfl, table, h9]
  · by_cases ho : s.val % 2 = 1
    · simp [show (3 : State).val = 3 from rfl, table, h9, ho]
    · by_cases h0 : s.val = 0
      · simp [show (3 : State).val = 3 from rfl, table, h9, ho, h0]
      · by_cases h18 : s.val = 18
        · simp [show (3 : State).val = 3 from rfl, table, h9, ho, h0, h18]
        · simp [show (3 : State).val = 3 from rfl, table, h9, ho, h0, h18]

/-- Boundary symbols can only delete paths; all other updates are exact. -/
theorem advance_bounds (s : Symbol) (v : Counts) :
    ((advance s v).U ≤ v.U ∧ (advance s v).V ≤ v.V) ∨
    ((advance s v).U = v.V ∧ (advance s v).V = v.U) ∨
    ((advance s v).U = v.V ∧ (advance s v).V = v.U + v.V) := by
  rw [advance_formula]
  split
  · right; right; simp [Counts.U, Counts.V] <;> omega
  · split
    · right; left; simp [Counts.U, Counts.V] <;> omega
    · left; split
      · simp [Counts.U, Counts.V] <;> omega
      · split <;> simp [Counts.U, Counts.V] <;> omega

def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fib (n + 1) + fib n

@[simp] theorem fib_zero : fib 0 = 0 := rfl
@[simp] theorem fib_one : fib 1 = 1 := rfl
@[simp] theorem fib_succ_succ (n : Nat) : fib (n+2) = fib (n+1) + fib n := rfl

theorem fib_le_succ (n : Nat) : fib n ≤ fib (n+1) := by
  cases n with
  | zero => decide
  | succ n => rw [show n+1+1 = n+2 by omega, fib_succ_succ]; omega

def initial : Counts := ⟨1,0,0,0⟩
def run : List Symbol → Counts → Counts
  | [], v => v
  | s :: ss, v => run ss (advance s v)
def inverseCount (ss : List Symbol) : Nat := (run ss initial).U

/-- Arbitrary-length induction once a Fibonacci envelope holds. -/
theorem run_bound (ss : List Symbol) (n : Nat) (v : Counts)
    (hu : v.U ≤ fib (n+1)) (hv : v.V ≤ fib (n+2)) :
    (run ss v).U ≤ fib (n + ss.length + 1) ∧
    (run ss v).V ≤ fib (n + ss.length + 2) := by
  induction ss generalizing n v with
  | nil => simpa [run] using And.intro hu hv
  | cons s ss ih =>
    have hf : fib (n+1) ≤ fib (n+2) := fib_le_succ (n+1)
    have hf' : fib (n+2) ≤ fib (n+3) := fib_le_succ (n+2)
    have hh : (advance s v).U ≤ fib (n+2) ∧
        (advance s v).V ≤ fib (n+3) := by
      rcases advance_bounds s v with h | h | h
      · omega
      · omega
      · have he : fib (n+3) = fib (n+2) + fib (n+1) := fib_succ_succ (n+1)
        omega
    have hh' := ih (n+1) (advance s v) hh.1 hh.2
    simpa [run, List.length_cons, Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using hh'

/-- Both boundary symbols are included in this finite base case. -/
theorem two_symbol_bound : ∀ s t : Symbol,
    (advance t (advance s initial)).U ≤ 1 ∧
    (advance t (advance s initial)).V ≤ 1 := by
  decide

theorem one_symbol_bound : ∀ s : Symbol, inverseCount [s] ≤ 1 := by decide

/-- Sharp upper bound for every target of half-width at least two. -/
theorem inverseCount_bound (s t : Symbol) (ss : List Symbol) :
    inverseCount (s :: t :: ss) ≤ fib (ss.length + 1) := by
  have h := two_symbol_bound s t
  have hh := run_bound ss 0 (advance t (advance s initial)) h.1 h.2
  simpa [inverseCount, run] using hh.1

/-- Appending a target symbol applies its arithmetic transition once. -/
theorem run_append (xs ys : List Symbol) (v : Counts) :
    run (xs ++ ys) v = run ys (run xs v) := by
  induction xs generalizing v with
  | nil => rfl
  | cons s ss ih => simpa [run] using ih (advance s v)

theorem advance_nine (v : Counts) :
    (advance 9 v).U = v.V ∧ (advance 9 v).V = v.U + v.V := by
  rw [advance_formula]
  simp [show (9 : Symbol).val = 9 from rfl, Counts.U, Counts.V] <;> omega

theorem replicate_snoc {α : Type} (n : Nat) (a : α) :
    List.replicate (n+1) a = List.replicate n a ++ [a] := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [List.replicate_succ, List.cons_append] using congrArg (List.cons a) ih

/-- All-nine words realize the exact Fibonacci pair, not merely its bound. -/
theorem nines_exact (n : Nat) :
    (run (List.replicate (n+1) 9) initial).U = fib n ∧
    (run (List.replicate (n+1) 9) initial).V = fib (n+1) := by
  induction n with
  | zero => decide
  | succ n ih =>
    have hr : List.replicate (n+1+1) (9 : Symbol) =
        List.replicate (n+1) 9 ++ [9] := by
      exact replicate_snoc (n+1) 9
    rw [hr, run_append]
    simp only [run]
    have hh := advance_nine (run (List.replicate (n+1) 9) initial)
    rw [ih.1, ih.2] at hh
    change _ = fib (n+1) ∧ _ = fib (n+2)
    rw [fib_succ_succ]
    constructor <;> omega

theorem first_eleven_eq_nine : advance 11 initial = advance 9 initial := by decide

/-- The sharp family starts with an actual positive exterior label five. -/
theorem leading_eleven_exact (n : Nat) :
    inverseCount (11 :: List.replicate n 9) = fib n := by
  have h := (nines_exact n).1
  simpa [inverseCount, List.replicate_succ, run, ← first_eleven_eq_nine] using h

theorem leading_eleven_labels : ∀ q : State, ∀ x : Fin 19,
    Local 11 0 q x.val ↔ q = 1 ∧ x.val = 5 := by decide

#print axioms weight_eq_table
#print axioms local_unique
#print axioms advance_formula
#print axioms advance_bounds
#print axioms run_bound
#print axioms inverseCount_bound
#print axioms nines_exact
#print axioms leading_eleven_exact
#print axioms leading_eleven_labels

end P196.Agent9.InverseFibers
