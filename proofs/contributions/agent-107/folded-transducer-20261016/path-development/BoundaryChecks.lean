import Agent107TransducerPath

open Agent107.FoldedTransducer

/- Compile-time kernel controls only: empty words are rejected, one-column
inputs have no pair transitions, and both boundary overflow cases retain
the actual delayed high digit. These are not new general result claims. -/

example (q : Nat → Nat) (p : Nat → State) : ¬ Accepts 0 q p := by
  intro hp
  obtain ⟨h, _, hs⟩ := hp.1
  have ht := hp.2.2
  simp [Terminal, inputCenter, hs, initial] at ht

example : finitePath 1 (actualState 1 (fun _ => 2)) = [initial 0] := by decide

example : finitePath 1 (actualState 1 (fun _ => 18)) = [initial 1] := by decide

example : finitePath 2 (actualState 2 (fun _ => 18)) =
    [initial 1, ⟨1, 1, 1, 9, true⟩] := by decide

example : finitePath 3 (actualState 3 (fun i => if i = 1 then 18 else 9)) =
    [initial 1, ⟨1, 0, 1, 0, true⟩] := by decide

/- The two actual paths can be prolonged differently without changing the
unique finite trace. This checks the intended finite-only quantifier. -/
example : finitePath 1 (fun i => if i = 0 then initial 0 else initial 1) =
    finitePath 1 (fun _ => initial 0) := by decide
