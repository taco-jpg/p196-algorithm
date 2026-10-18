import P196.Drafts.Agent116Cap3Kernel.Cap3Base

namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxHeartbeats 0

/-- Unlike ExitCheck, this statement has no validity/trim/head premise. -/
def AllExitCheck (p : Fin 8) (k : Nat) : Prop :=
  staysWithin 3 10 (encodedAt p k) = false

def AllBatchCheck (start count : Nat) : Prop :=
  ∀ (p : Fin 8) (j : Fin count), AllExitCheck p (start + j.val)

instance (p : Fin 8) (k : Nat) : Decidable (AllExitCheck p k) := by
  unfold AllExitCheck
  infer_instance

instance (start count : Nat) : Decidable (AllBatchCheck start count) := by
  unfold AllBatchCheck
  infer_instance

theorem of_all_batch {start count k : Nat} (h : AllBatchCheck start count)
    (p : Fin 8) (hlo : start ≤ k) (hhi : k < start + count) :
    AllExitCheck p k := by
  have heq : start + (k - start) = k := by omega
  simpa only [heq] using h p ⟨k - start, by omega⟩

#print axioms of_all_batch
end P196.Agent116.Cap3
