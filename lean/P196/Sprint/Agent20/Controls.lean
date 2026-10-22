import P196.Sprint.Agent20.PrefixFidelity
import P196.CertificateToLychrel.AdmissibleHeads

/-!
# Red team (sprint agent 20): non-vacuity controls

1. **The ancestry-bound hypothesis is falsifiable.**  The premise consumed by
   `SevenColumnKernel.PalindromeBridge.no_196_target_of_ancestry_bound` is a
   uniform bound `∀ A P t, 0 < A → Target P → orbit A t = P → t ≤ B`.  For the
   prefix 4456 it is false for every `B < 261`, witnessed by the record delayed
   seed 1186060307891929990 (261 steps to a 119-digit palindrome beginning 4456).
   So `PalStartsL` is not vacuous and the prefix method cannot certify 4456
   (it needs `B ≤ 100`).
2. **`CertificateToLychrel` concludes exactly "a decimal Lychrel number exists".**
   Its endpoint is stated with `Agent109.Palindrome` / `Agent109.orbit`, separate
   copies of the definitions.  They agree with `Lychrel196.Palindrome` /
   `Lychrel196.orbit` for all inputs, and the witness is automatically ≥ 10.
   (The hypothesis `check cert = true` is not shown satisfiable here; no
   certificate is known.)
-/

namespace Sprint.Agent20

open DecimalDigits Lychrel196 Agent124.PrefixL

/-! ## 1. Prefix 4456 -/

def seed4456 : Nat := 1186060307891929990

def pal4456 : Nat :=
  44562665878976437622437848976653870388884783662598425855963436955852489526638748888307835667984873422673467987856626544

set_option maxRecDepth 100000 in
theorem orbit_seed4456 : orbit seed4456 261 = pal4456 := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem pal4456_palindrome : Palindrome pal4456 := by
  decide +kernel

theorem pal4456_starts : PalStartsL [4, 4, 5, 6] pal4456 :=
  ⟨pal4456_palindrome,
    startsL_of_decStarts _ (by decide) _ ⟨115, by decide +kernel, by decide +kernel⟩⟩

/-- No uniform ancestry bound below 261 holds for palindromes beginning 4456. -/
theorem no_ancestry_bound_4456 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [4, 4, 5, 6] P → orbit A t = P → t ≤ B) :
    261 ≤ B :=
  h seed4456 pal4456 261 (by decide) pal4456_starts orbit_seed4456

/-- In particular the `entryOK` pipeline (which needs `bound + 1 ≤ 100`) can
never certify 4456, at any width `k`. -/
theorem no_entry_certificate_4456 (k : Nat) (R : List Nat → Option Nat)
    (rows : Agent124.PrefixR.RowsClosed k R) (short : Agent124.PrefixR.ShortClosed k R)
    (bound : Nat) (h : entryOK k R ([4, 4, 5, 6], bound) = true) : 260 ≤ bound := by
  have hall := ancestry_of_entries k R rows short [([4, 4, 5, 6], bound)]
    (by simp [h]) ([4, 4, 5, 6], bound) (by simp)
  have := no_ancestry_bound_4456 (bound + 1) hall
  omega


/-! ## 1b. Prefix 5554 (found by the 10^7-seed forward scan)

Seed 1702190 reaches the 48-digit palindrome
555458774083726674580862268085476627380477854555 at step 101, so no ancestry
bound below 101 holds for 5554 (nor for its parent 555).  With the current
`t ≤ 100` base check (`bound + 1 ≤ 100`) the method therefore cannot certify
5554 or 555 at any width; with a longer verified prefix of 196's orbit it could
in principle. -/

def seed5554 : Nat := 1702190

def pal5554 : Nat := 555458774083726674580862268085476627380477854555

set_option maxRecDepth 100000 in
theorem orbit_seed5554 : orbit seed5554 101 = pal5554 := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem pal5554_palindrome : Palindrome pal5554 := by
  decide +kernel

theorem no_ancestry_bound_5554 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [5, 5, 5, 4] P → orbit A t = P → t ≤ B) :
    101 ≤ B :=
  h seed5554 pal5554 101 (by decide)
    ⟨pal5554_palindrome, startsL_of_decStarts _ (by decide) _ ⟨44, by decide +kernel,
      by decide +kernel⟩⟩ orbit_seed5554

theorem no_ancestry_bound_555 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [5, 5, 5] P → orbit A t = P → t ≤ B) :
    101 ≤ B :=
  h seed5554 pal5554 101 (by decide)
    ⟨pal5554_palindrome, startsL_of_decStarts _ (by decide) _ ⟨45, by decide +kernel,
      by decide +kernel⟩⟩ orbit_seed5554


/-! ## 1c. Prefixes 6634 / 663 and the parent 445 of 4456

Seed 13968441660506503386020 reaches a 142-digit palindrome beginning 6634 at
step 289 (the 4456 witness above also rules out its parent 445). -/

def seed6634 : Nat := 13968441660506503386020

def pal6634 : Nat :=
  6634343445544188178365154497662249922269477578658488045222897505659677887769565057982225408848568757749622299422667944515638718814455443434366

set_option maxRecDepth 100000 in
theorem orbit_seed6634 : orbit seed6634 289 = pal6634 := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem pal6634_palindrome : Palindrome pal6634 := by
  decide +kernel

theorem no_ancestry_bound_6634 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [6, 6, 3, 4] P → orbit A t = P → t ≤ B) :
    289 ≤ B :=
  h seed6634 pal6634 289 (by decide)
    ⟨pal6634_palindrome, startsL_of_decStarts _ (by decide) _ ⟨138, by decide +kernel,
      by decide +kernel⟩⟩ orbit_seed6634

theorem no_ancestry_bound_663 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [6, 6, 3] P → orbit A t = P → t ≤ B) :
    289 ≤ B :=
  h seed6634 pal6634 289 (by decide)
    ⟨pal6634_palindrome, startsL_of_decStarts _ (by decide) _ ⟨139, by decide +kernel,
      by decide +kernel⟩⟩ orbit_seed6634

theorem no_ancestry_bound_445 (B : Nat)
    (h : ∀ A P t, 0 < A → PalStartsL [4, 4, 5] P → orbit A t = P → t ≤ B) :
    261 ≤ B :=
  h seed4456 pal4456 261 (by decide)
    ⟨pal4456_palindrome, startsL_of_decStarts _ (by decide) _ ⟨116, by decide +kernel,
      by decide +kernel⟩⟩ orbit_seed4456

/-! ## 2. `CertificateToLychrel` statement -/

theorem reverseFuel_agree (f n a : Nat) :
    Agent109.reverseFuel f n a = Lychrel196.reverseFuel f n a := by
  induction f generalizing n a with
  | zero => rfl
  | succ f ih => simp only [Agent109.reverseFuel, Lychrel196.reverseFuel, ih]

theorem reverse10_agree (n : Nat) : Agent109.reverse10 n = Lychrel196.reverse10 n :=
  reverseFuel_agree n n 0

theorem palindrome_agree (n : Nat) : Agent109.Palindrome n ↔ Lychrel196.Palindrome n := by
  unfold Agent109.Palindrome Lychrel196.Palindrome
  rw [reverse10_agree]

theorem orbit_agree (n k : Nat) : Agent109.orbit n k = Lychrel196.orbit n k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Agent109.orbit, Lychrel196.orbit, Agent109.step, Lychrel196.step, ih,
      reverse10_agree]

theorem small_palindromes : ∀ m, m < 10 → Lychrel196.Palindrome m := by decide

/-- An accepted return certificate yields a decimal Lychrel number in the
repository's canonical sense (`Lychrel196.IsLychrel`), necessarily ≥ 10. -/
theorem certificate_gives_isLychrel (cert : Agent109.Cert.Certificate)
    (hc : Agent109.Cert.check cert = true) :
    ∃ m, 10 ≤ m ∧ Lychrel196.IsLychrel m := by
  obtain ⟨m, hm⟩ := Agent112.Admissibility.certificate_existence_of_check cert hc
  have hl : Lychrel196.IsLychrel m := by
    intro k hk
    exact hm k ((palindrome_agree _).mpr (by rw [orbit_agree]; exact hk))
  refine ⟨m, ?_, hl⟩
  apply Nat.le_of_not_lt
  intro h
  exact hl 0 (small_palindromes m h)

end Sprint.Agent20

#print axioms Sprint.Agent20.orbit_seed4456
#print axioms Sprint.Agent20.pal4456_starts
#print axioms Sprint.Agent20.no_ancestry_bound_4456
#print axioms Sprint.Agent20.no_entry_certificate_4456
#print axioms Sprint.Agent20.no_ancestry_bound_5554
#print axioms Sprint.Agent20.no_ancestry_bound_555
#print axioms Sprint.Agent20.no_ancestry_bound_6634
#print axioms Sprint.Agent20.no_ancestry_bound_663
#print axioms Sprint.Agent20.no_ancestry_bound_445
#print axioms Sprint.Agent20.palindrome_agree
#print axioms Sprint.Agent20.orbit_agree
#print axioms Sprint.Agent20.certificate_gives_isLychrel

/-! ## 3. A necessary condition on accepted certificates

Every state of a valid certificate is the successor of the previous state in the
cyclic list, and `LocalOK` forces the successor phase to be `2 * tOf c`, which is
even.  Hence every phase in an accepted certificate is one of 2,4,6,8,10,12,14,16;
odd phases (and 9, already excluded by `Phase`) can never occur.  This narrows,
but does not decide, the satisfiability of `check cert = true`. -/

namespace Sprint.Agent20

theorem valid_phase_even (cert : Agent109.Cert.Certificate) (hv : Agent109.Cert.Valid cert)
    (i : Nat) (hi : i < cert.P) :
    (cert.st i).c ∈ [2, 4, 6, 8, 10, 12, 14, 16] := by
  obtain ⟨hP, hloc⟩ := hv
  obtain ⟨j, hj, hsucc⟩ : ∃ j, j < cert.P ∧ (j + 1) % cert.P = i := by
    rcases Nat.eq_zero_or_pos i with h0 | hpos
    · refine ⟨cert.P - 1, by omega, ?_⟩
      rw [Nat.sub_add_cancel hP, Nat.mod_self, h0]
    · refine ⟨i - 1, by omega, ?_⟩
      rw [Nat.sub_add_cancel hpos, Nat.mod_eq_of_lt hi]
  have hl := hloc j hj
  rw [hsucc] at hl
  obtain ⟨-, -, -, -, hc, -⟩ := hl
  obtain ⟨hp1, hp2, hp3⟩ := (hloc i hi).1
  have heven : (cert.st i).c % 2 = 0 := by rw [← hc]; omega
  have : (cert.st i).c = 2 ∨ (cert.st i).c = 4 ∨ (cert.st i).c = 6 ∨ (cert.st i).c = 8 ∨
      (cert.st i).c = 10 ∨ (cert.st i).c = 12 ∨ (cert.st i).c = 14 ∨ (cert.st i).c = 16 := by
    omega
  rcases this with h | h | h | h | h | h | h | h <;> simp [h]

theorem check_phase_even (cert : Agent109.Cert.Certificate)
    (hc : Agent109.Cert.check cert = true) (i : Nat) (hi : i < cert.P) :
    (cert.st i).c ∈ [2, 4, 6, 8, 10, 12, 14, 16] :=
  valid_phase_even cert (Agent109.Cert.check_sound cert hc) i hi

end Sprint.Agent20

#print axioms Sprint.Agent20.check_phase_even
