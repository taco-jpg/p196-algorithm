import Agent1PeriodicOuterChoices

/-! A linear certificate for distinct finite catalog nodes. Strict order of
natural keys implies distinct source values without any key-injectivity claim.
The checker tests only adjacent keys; its soundness uses transitivity of <. -/
namespace Agent1.Periodic

/-- The original phase digits, followed by the outside coefficient, in base 19. -/
def catalogOrderKey (s : OuterNode) : Nat :=
  s.1.foldl (fun acc d => acc * 19 + d) 0 * 19 + s.2

/-- Compare a previous key with the next key, then advance once. -/
def strictNatKeysFrom (previous : Nat) : List Nat → Bool
  | [] => true
  | a :: xs => decide (previous < a) && strictNatKeysFrom a xs

/-- A linear adjacent-comparison checker for strictly increasing natural keys. -/
def strictNatKeys : List Nat → Bool
  | [] => true
  | a :: xs => strictNatKeysFrom a xs

private theorem strictNatKeysFrom_sound (a : Nat) (xs : List Nat)
    (h : strictNatKeysFrom a xs = true) :
    (∀ b ∈ xs, a < b) ∧ xs.Pairwise (· < ·) := by
  induction xs generalizing a with
  | nil =>
      exact ⟨fun _ hm => nomatch hm, List.Pairwise.nil⟩
  | cons b xs ih =>
      change (decide (a < b) && strictNatKeysFrom b xs) = true at h
      have hab : a < b := of_decide_eq_true (Bool.and_eq_true.mp h).1
      obtain ⟨hhead, htail⟩ := ih b (Bool.and_eq_true.mp h).2
      refine ⟨?_, List.Pairwise.cons hhead htail⟩
      intro c hc
      rcases List.mem_cons.mp hc with hcb | hc
      · exact hcb ▸ hab
      · exact Nat.lt_trans hab (hhead c hc)

/-- Adjacent strict order is sufficient for pairwise strict order. -/
theorem strictNatKeys_pairwise (xs : List Nat)
    (h : strictNatKeys xs = true) : xs.Pairwise (· < ·) := by
  cases xs with
  | nil => exact List.Pairwise.nil
  | cons a xs =>
      obtain ⟨hhead, htail⟩ := strictNatKeysFrom_sound a xs h
      exact List.Pairwise.cons hhead htail

/-- Distinct keys certify distinct nodes; key injectivity is not required. -/
theorem nodup_of_strictNatKeys {α : Type _} (key : α → Nat) (xs : List α)
    (h : strictNatKeys (xs.map key) = true) : xs.Nodup := by
  have hp : xs.Pairwise (fun a b => key a < key b) :=
    List.pairwise_map.mp (strictNatKeys_pairwise (xs.map key) h)
  exact hp.imp (fun hab he => Nat.ne_of_lt hab (congrArg key he))

/-- Public catalog helper: a kernel-checked adjacent-key test proves Nodup. -/
theorem outerCatalog_nodup_of_checked (xs : List OuterNode)
    (h : strictNatKeys (xs.map catalogOrderKey) = true) : xs.Nodup :=
  nodup_of_strictNatKeys catalogOrderKey xs h

end Agent1.Periodic

#print axioms Agent1.Periodic.strictNatKeys_pairwise
#print axioms Agent1.Periodic.nodup_of_strictNatKeys
#print axioms Agent1.Periodic.outerCatalog_nodup_of_checked
