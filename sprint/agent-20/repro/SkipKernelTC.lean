/-
RED-TEAM REPRODUCER — DO NOT MOVE UNDER lean/.  (sprint agent 20)

Shows that `tools/verify.py` (source regex for sorry/admit/native_decide/axiom
+ `#print axioms` audit) does not detect a declaration that was added to the
environment without kernel type checking.  The false theorem below is accepted
and `#print axioms` reports that it depends on no axioms at all.

Run:  cd lean && lake env lean ../sprint/agent-20/repro/SkipKernelTC.lean
-/
import Lean
open Lean Elab Command

set_option debug.skipKernelTC true in
run_cmd liftCoreM do
  addDecl (Declaration.thmDecl
    { name := `RedTeam.bad, levelParams := [], type := mkConst ``False,
      value := mkConst ``True.intro })

theorem RedTeam.boom : (1 : Nat) = 2 := RedTeam.bad.elim

#print axioms RedTeam.boom
