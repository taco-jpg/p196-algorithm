import Agent124CodeCert
import Agent124PrefixL

/-!
Agent #117, seven-column prefix 2641, formal targets only.

WIP, not imported into the accepted build. Requires the exact frozen
Agent124 source dependency closure. No generated rank instance has
compiled in this session. These are propositions, NOT proved theorems.
-/

namespace Agent117.C2641

open Lychrel196
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR Agent124.PrefixL

def prefix : List Nat := [2, 6, 4, 1]

/-- Complete acceptance premises for the published 25624-row code tree. -/
def CertificatePremises (tree : CodeTree) : Prop :=
  tree.All (fun c r => rowOK tree 7 c r = true) ∧
  (∀ n, n < 7 → (symWords n).all (shortOKC tree) = true) ∧
  entryOK 7 (R tree) (prefix, 5) = true

/-- Arithmetic consequence sought only AFTER the concrete certificate passes. -/
def BoundedTarget : Prop :=
  ∀ A P t, 0 < A →
    PalStartsL prefix P → orbit A t = P → t ≤ 6

/-- A proper subfamily exclusion, not a solution of the 196 conjecture. -/
def ExcludeTargetFor196 : Prop :=
  ∀ t, ¬ PalStartsL prefix (orbit 196 t)

end Agent117.C2641
