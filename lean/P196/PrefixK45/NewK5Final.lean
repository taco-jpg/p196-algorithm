import P196.PrefixK45.NewK5AllRows
import P196.PrefixK45.NewK5Short
import P196.Agent117P2641.Agent124PrefixL

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK5
open Agent124.CodeCert
set_option maxRecDepth 100000

open Agent124.PrefixL Lychrel196

/-- New prefix entries (digits, rank bound), chunk 0. -/
def entries00 : List (List Nat × Nat) :=
  [([1,2,1,3], 9), ([1,2,1,5], 9), ([1,2,1,6], 9), ([1,2,1,7], 9), ([1,2,1,8], 9), ([1,2,1,9], 9)]

theorem entries00_ok : entries00.all (entryOK 5 (R ranks)) = true := by
  decide +kernel

theorem entries00_le : entries00.all (fun e => Nat.ble (e.2 + 1) 100) = true := by
  decide +kernel

theorem ancestry_00 : ∀ e ∈ entries00, ∀ A P t, 0 < A →
    PalStartsL e.1 P → orbit A t = P → t ≤ e.2 + 1 :=
  ancestry_of_entries 5 (R ranks) allRows short entries00 entries00_ok

theorem no_196_00 : ∀ t, ∀ e ∈ entries00, ¬ PalStartsL e.1 (orbit 196 t) :=
  no_196_of_entries 5 (R ranks) allRows short entries00 entries00_ok entries00_le

#print axioms no_196_00


end PrefixK45.NewK5
