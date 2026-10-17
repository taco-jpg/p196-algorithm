import Agent107TransducerGraph

/-!
# Finite deterministic automata and the original folded Horn certificate

The machine reads pair column sums followed by a separate optional center.
Its transition function is totalized on `Nat` for convenient finite-list
semantics.  The original 19-symbol, 11-center-slot Boolean arrays are adapted
separately; no behavior outside that original alphabet is claimed for them.

`Horn` contains only the two initial product states and the exact finite
edge/terminal templates.  In particular it does not assume language closure.
The extra terminal pair is consumed before inspecting the output center.
-/

namespace Agent107.FoldedDFA

open Agent107.FoldedTransducer

structure DFA (N : Nat) where
  positive : 0 < N
  step : Fin N → Nat → Fin N
  final : Fin N → Option Nat → Bool

namespace DFA

def start {N : Nat} (M : DFA N) : Fin N := ⟨0, M.positive⟩

def run {N : Nat} (M : DFA N) (a : Fin N) (xs : List Nat) : Fin N :=
  xs.foldl M.step a

def accepts {N : Nat} (M : DFA N) (w : Word) : Prop :=
  M.final (M.run M.start w.pairs) w.center = true

@[simp] theorem run_nil {N : Nat} (M : DFA N) (a : Fin N) :
    M.run a [] = a := rfl

@[simp] theorem run_cons {N : Nat} (M : DFA N) (a : Fin N)
    (q : Nat) (xs : List Nat) :
    M.run a (q :: xs) = M.run (M.step a q) xs := rfl

theorem run_append {N : Nat} (M : DFA N) (a : Fin N)
    (xs ys : List Nat) :
    M.run a (xs ++ ys) = M.run (M.run a xs) ys := by
  simp [run, List.foldl_append]

@[simp] theorem run_singleton {N : Nat} (M : DFA N) (a : Fin N) (q : Nat) :
    M.run a [q] = M.step a q := rfl

theorem run_ofFn_succ {N : Nat} (M : DFA N) (a : Fin N)
    (f : Nat → Nat) (k : Nat) :
    M.run a (List.ofFn (fun i : Fin (k + 1) => f i.val)) =
      M.step (M.run a (List.ofFn (fun i : Fin k => f i.val))) (f k) := by
  rw [ofFn_append_last, M.run_append, M.run_singleton]

end DFA

/-- A finite forward simulation certificate for the original folded graph. -/
structure Horn {N : Nat} (M : DFA N)
    (R : State → Fin N → Fin N → Prop) : Prop where
  starts : ∀ h : Nat, h ≤ 1 → R (initial h) M.start M.start
  edges : ∀ e ∈ Table.edges, ∀ a b : Fin N,
    R e.source a b → R e.target (M.step a e.input) (M.step b e.output)
  terminals : ∀ r ∈ Table.terminals, ∀ a b : Fin N,
    R r.source a b → M.final a r.center = true →
      M.final (M.run b r.extra.toList) r.outputCenter = true

end Agent107.FoldedDFA

#print axioms Agent107.FoldedDFA.DFA.run_nil
#print axioms Agent107.FoldedDFA.DFA.run_cons
#print axioms Agent107.FoldedDFA.DFA.run_append
#print axioms Agent107.FoldedDFA.DFA.run_singleton
#print axioms Agent107.FoldedDFA.DFA.run_ofFn_succ
