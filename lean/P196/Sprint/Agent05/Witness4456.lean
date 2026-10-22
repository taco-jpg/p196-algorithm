import P196.Sprint.Agent05.DelayWitness

/-!
# The 261-step witness for prefix 4456 (sprint agent 05)

The seed 1186060307891929990 (Jason Doucette, 2005; OEIS A281506) reaches its
first palindrome after 261 reverse-and-add steps; that palindrome has 119 digits
and begins 4456. All facts below are reduced by the kernel with the unchanged
`orbit`. Consequence: every Agent124 prefix certificate for 4456 (or for its
prefixes 445 and 44) has rank bound at least 260, so the route
`no_196_of_entries` (base check t ≤ 100) can never exclude 4456; a longer base
check would need N ≥ 261.
-/

namespace Sprint.Agent05.W4456
open Lychrel196 Agent124.PrefixR Agent124.PrefixL Sprint.Agent05

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def seed : Nat := 1186060307891929990
def target : Nat := 44562665878976437622437848976653870388884783662598425855963436955852489526638748888307835667984873422673467987856626544

def w : Witness := ⟨[4,4,5,6], seed, 261, target, 119⟩
def w445 : Witness := ⟨[4,4,5], seed, 261, target, 119⟩
def w44 : Witness := ⟨[4,4], seed, 261, target, 119⟩

theorem w_ok : witnessOK w = true ∧ witnessOK w445 = true ∧ witnessOK w44 = true := by
  decide +kernel

/-- 261 is the first palindrome time of this seed. -/
theorem first_hit : Palindrome (orbit seed 261) ∧ ∀ t, t < 261 → ¬ Palindrome (orbit seed t) := by
  have h : noPalindromeFor 261 seed = true := by decide +kernel
  exact ⟨(witnessOK_sound w w_ok.1).2.1, noPalindromeFor_sound 261 seed h⟩

theorem reaches : 0 < seed ∧ PalStartsL [4,4,5,6] (orbit seed 261) :=
  witnessOK_sound w w_ok.1

/-- Every uniform ancestry bound for 4456 is at least 261. -/
theorem ancestry_bound_ge (B : Nat) (h : AncestryBound [4,4,5,6] B) : 261 ≤ B :=
  le_of_witness h reaches.1 reaches.2

/-- Every accepted certificate entry for 4456, 445 or 44 has rank bound ≥ 260. -/
theorem entry_bound_ge (k : Nat) (R : List Nat → Option Nat) (rows : RowsClosed k R)
    (short : ShortClosed k R) (b : Nat) :
    (entryOK k R ([4,4,5,6], b) = true → 260 ≤ b) ∧
    (entryOK k R ([4,4,5], b) = true → 260 ≤ b) ∧
    (entryOK k R ([4,4], b) = true → 260 ≤ b) := by
  refine ⟨fun hok => ?_, fun hok => ?_, fun hok => ?_⟩
  · have := entry_bound_ge_of_witnessOK w w_ok.1 k R rows short b hok
    simp [w] at this; omega
  · have := entry_bound_ge_of_witnessOK w445 w_ok.2.1 k R rows short b hok
    simp [w445] at this; omega
  · have := entry_bound_ge_of_witnessOK w44 w_ok.2.2 k R rows short b hok
    simp [w44] at this; omega

/-- With base check `N ≤ 260` (the repository uses `N = 100`), no entry list that
passes both premises of `no_196_of_entries` contains 4456, 445 or 44. -/
theorem not_mem_entries (k : Nat) (R : List Nat → Option Nat) (rows : RowsClosed k R)
    (short : ShortClosed k R) (entries : List (List Nat × Nat))
    (h : entries.all (entryOK k R) = true) (N : Nat) (hN : N ≤ 260)
    (hb : entries.all (fun e => Nat.ble (e.2 + 1) N) = true) :
    ∀ b, ([4,4,5,6], b) ∉ entries ∧ ([4,4,5], b) ∉ entries ∧ ([4,4], b) ∉ entries := by
  intro b
  refine ⟨?_, ?_, ?_⟩
  · exact not_mem_entries_of_witnessOK w w_ok.1 k R rows short entries h N hb
      (by simp [w]; omega) b
  · exact not_mem_entries_of_witnessOK w445 w_ok.2.1 k R rows short entries h N hb
      (by simp [w445]; omega) b
  · exact not_mem_entries_of_witnessOK w44 w_ok.2.2 k R rows short entries h N hb
      (by simp [w44]; omega) b

end Sprint.Agent05.W4456

#print axioms Sprint.Agent05.W4456.w_ok
#print axioms Sprint.Agent05.W4456.first_hit
#print axioms Sprint.Agent05.W4456.reaches
#print axioms Sprint.Agent05.W4456.ancestry_bound_ge
#print axioms Sprint.Agent05.W4456.entry_bound_ge
#print axioms Sprint.Agent05.W4456.not_mem_entries
