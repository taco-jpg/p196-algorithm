import P196.F1Semigroup.F1Data
/-!
# Audit formalization, part 2: reachable relation states (434) and transition tables

The 434 relation states `S`, the tables `N0`/`N1` and BFS parents `Par` are *data*; everything below
re-verifies them inside the kernel (`decide +kernel`, chunked to bound kernel memory).
-/
namespace F1

/-- number of reachable relation states -/
def nS : Nat := 434

def unpack (p : Nat) : Rel := (List.range 18).map (fun j => (p >>> (18 * j)) % 262144)

def Sget (i : Nat) : Rel := unpack ((SP >>> (324 * i)) % 2 ^ 324)

def Nget (a : Bool) (i : Nat) : Nat := ((if a then N1P else N0P) >>> (9 * i)) % 512

def parJ (k : Nat) : Nat := (ParP >>> (16 * k)) % 512
def parA (k : Nat) : Bool := decide (((ParP >>> (16 * k)) / 512) % 2 = 1)

def accB (i : Nat) : Bool := accept (Sget i)

theorem S_zero : Sget 0 = initRel := by decide +kernel

/-- closure: every state has both successors inside the table, and the table entry is exactly `delta` -/
def tabOK (i : Nat) : Bool :=
  decide (Nget false i < nS) && decide (Nget true i < nS) &&
  (Sget (Nget false i) == delta false (Sget i)) && (Sget (Nget true i) == delta true (Sget i))

theorem tabOK_all : ∀ i, i < nS → tabOK i = true := by decide +kernel

/-- BFS parent certificate: every state `k > 0` is the image of an earlier state -/
def parOK (k : Nat) : Bool :=
  decide (parJ k < k) && decide (Nget (parA k) (parJ k) = k)

theorem parOK_all : ∀ k, k < nS → 0 < k → parOK k = true := by decide +kernel

theorem tab_step (a : Bool) (i : Nat) (hi : i < nS) :
    Nget a i < nS ∧ Sget (Nget a i) = delta a (Sget i) := by
  have h := tabOK_all i hi
  simp only [tabOK, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at h
  cases a
  · exact ⟨h.1.1.1, h.1.2⟩
  · exact ⟨h.1.1.2, h.2⟩

/-- run the index automaton -/
def irun (i : Nat) (w : List Bool) : Nat := w.foldl (fun j a => Nget a j) i

theorem irun_spec (w : List Bool) : ∀ i, i < nS →
    irun i w < nS ∧ Sget (irun i w) = run (Sget i) w := by
  induction w with
  | nil => intro i hi; exact ⟨hi, rfl⟩
  | cons a w ih =>
    intro i hi
    obtain ⟨h1, h2⟩ := tab_step a i hi
    obtain ⟨h3, h4⟩ := ih (Nget a i) h1
    refine ⟨h3, ?_⟩
    have e1 : irun i (a :: w) = irun (Nget a i) w := rfl
    have e2 : run (Sget i) (a :: w) = run (delta a (Sget i)) w := rfl
    rw [e1, e2, h4, h2]

theorem irun_append (i : Nat) (u v : List Bool) : irun i (u ++ v) = irun (irun i u) v := by
  simp [irun, List.foldl_append]

theorem run_append (r : Rel) (u v : List Bool) : run r (u ++ v) = run (run r u) v := by
  simp [run, List.foldl_append]

/-- every state of `S` is reached from the start by some word -/
theorem reach_all : ∀ k, k < nS → ∃ w, irun 0 w = k := by
  intro k
  induction k using Nat.strongRecOn with
  | _ k ih =>
    intro hk
    rcases Nat.eq_zero_or_pos k with h0 | hpos
    · exact ⟨[], by simp [irun, h0]⟩
    · have hp := parOK_all k hk hpos
      simp only [parOK, Bool.and_eq_true, decide_eq_true_eq] at hp
      obtain ⟨hj, hN⟩ := hp
      obtain ⟨w, hw⟩ := ih _ hj (by unfold nS at *; omega)
      refine ⟨w ++ [parA k], ?_⟩
      rw [irun_append, hw]
      simpa [irun] using hN

/-- The reachable set is exactly `S`: every word's relation is some `S i`, and every `S i` is reached. -/
theorem S_is_reachable_set :
    (∀ w, ∃ i, i < nS ∧ run initRel w = Sget i) ∧
    (∀ i, i < nS → ∃ w, run initRel w = Sget i) := by
  have h0 : 0 < nS := by decide
  constructor
  · intro w
    obtain ⟨h1, h2⟩ := irun_spec w 0 h0
    exact ⟨irun 0 w, h1, by rw [h2, S_zero]⟩
  · intro i hi
    obtain ⟨w, hw⟩ := reach_all i hi
    obtain ⟨h1, h2⟩ := irun_spec w 0 h0
    exact ⟨w, by rw [← S_zero, ← h2, hw]⟩

theorem LangB_irun (w : List Bool) : LangB w = accB (irun 0 w) := by
  have h0 : 0 < nS := by decide
  obtain ⟨_, h2⟩ := irun_spec w 0 h0
  unfold LangB accB
  rw [h2, S_zero]

end F1
