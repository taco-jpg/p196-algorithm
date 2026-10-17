import Agent107DFA

/-!
The finite Horn templates propagate the synchronized input/output DFA
states through every complete folded path, with no bound on word length.
The final template consumes the optional extra output pair before testing
the output center, including the one-digit and odd-overflow cases.
-/

namespace Agent107.FoldedDFA

open Agent107.FoldedTransducer

/-- The certificate relation holds at every prefix of an arbitrary
complete accepting path. No admissibility assumption is made about the
unread half of `q`, and no finite word-length bound is imposed. -/
theorem horn_prefix_invariant {N : Nat} (M : DFA N)
    (R : State → Fin N → Fin N → Prop) (cert : Horn M R)
    (L : Nat) (q : Nat → Nat) (p : Nat → State) (hp : Accepts L q p) :
    ∀ i, i ≤ L / 2 →
      R (p i)
        (M.run M.start (List.ofFn (fun j : Fin i => q j.val)))
        (M.run M.start (List.ofFn (fun j : Fin i =>
          emit (p j.val) (q j.val) (p (j.val + 1)).high))) := by
  have hg := (graphAccepts_iff_accepts L q p).2 hp
  intro i hi
  induction i with
  | zero =>
    obtain ⟨h, hb, he⟩ := hp.1
    rw [he]
    simpa only [List.ofFn_zero, DFA.run_nil] using cert.starts h hb
  | succ i ih =>
    have hr := ih (by omega)
    have he := cert.edges (edgeAt q p i) (hg.2.1 i (by omega)) _ _ hr
    simpa only [DFA.run_ofFn_succ, edgeAt] using he

/-- Every complete accepting folded transducer path carries DFA acceptance
from its input to its exact emitted output. The premises are only the
finite Horn certificate, literal path acceptance and input membership. -/
theorem horn_accepting_output {N : Nat} (M : DFA N)
    (R : State → Fin N → Fin N → Prop) (cert : Horn M R)
    (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (hp : Accepts L q p) (ha : M.accepts (foldPrefix L q)) :
    M.accepts (pathOutput L q p) := by
  have hg := (graphAccepts_iff_accepts L q p).2 hp
  have hr := horn_prefix_invariant M R cert L q p hp (L / 2) (by omega)
  have ht := cert.terminals (terminalAt L q p) hg.2.2 _ _ hr ha
  simpa only [terminalAt, DFA.accepts, pathOutput, DFA.run_append] using ht

#print axioms horn_prefix_invariant
#print axioms horn_accepting_output

end Agent107.FoldedDFA
