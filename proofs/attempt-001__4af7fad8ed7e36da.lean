import ReturnCertificate

/-!
Agent #110: exact structural accounting for Agent #109 return certificates.

All sums are finite recursive prefix sums in `Int`. The width equation follows
from the actual lengths of `Br`, `Ar`, and `Cr` and the trimming equations in
`LocalOK`; no numerical balance equation is an additional hypothesis. Trims
need not be maximal, and no integer realization or positive exterior digit is
assumed. These are necessary conditions on a valid symbolic certificate, not
a certificate instance, infinite seed, or a statement about 196.
-/

namespace Agent110.Accounting

open Agent109 Agent109.Cert

/-- Physical width occupied by the finite blocks, counting mirrored copies. -/
def width (s : State) : Int :=
  2 * (s.B.length : Int) + 2 * (s.A.length : Int) + (s.C.length : Int)

/-- Signed change of the outer band after the supplied trim. -/
def dg (s : State) (L : Link) : Int :=
  (gam s : Int) + (L.j : Int) + (L.j1 : Int) - 2

/-- Signed change of the inner band after the supplied trim. -/
def dh (s : State) (L : Link) : Int :=
  (gam s : Int) + (L.j2 : Int) + (L.k : Int) - 2

/-- Sum over the indices `0,...,n-1`; no external summation library is used. -/
def sumPrefix (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => sumPrefix f n + f n

def totalGam (cert : Certificate) : Int :=
  sumPrefix (fun i => (gam (cert.st i) : Int)) cert.P

def totalG (cert : Certificate) : Int :=
  sumPrefix (fun i => dg (cert.st i) (cert.lk i)) cert.P

def totalH (cert : Certificate) : Int :=
  sumPrefix (fun i => dh (cert.st i) (cert.lk i)) cert.P

theorem sumPrefix_congr {f g : Nat → Int} (n : Nat)
    (h : ∀ i, i < n → f i = g i) : sumPrefix f n = sumPrefix g n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [sumPrefix]
    rw [ih (fun i hi => h i (by omega)), h n (by omega)]

theorem sumPrefix_add (f g : Nat → Int) (n : Nat) :
    sumPrefix (fun i => f i + g i) n = sumPrefix f n + sumPrefix g n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sumPrefix, ih]; omega

theorem sumPrefix_sub (f g : Nat → Int) (n : Nat) :
    sumPrefix (fun i => f i - g i) n = sumPrefix f n - sumPrefix g n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sumPrefix, ih]; omega

theorem sumPrefix_two_mul (f : Nat → Int) (n : Nat) :
    sumPrefix (fun i => 2 * f i) n = 2 * sumPrefix f n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sumPrefix, ih]; omega

theorem sumPrefix_le {f g : Nat → Int} (n : Nat)
    (h : ∀ i, i < n → f i ≤ g i) : sumPrefix f n ≤ sumPrefix g n := by
  induction n with
  | zero => exact Int.le_refl _
  | succ n ih =>
    have h₁ := ih (fun i hi => h i (by omega))
    have h₂ := h n (by omega)
    simp only [sumPrefix]
    omega

theorem sumPrefix_difference (f : Nat → Int) (n : Nat) :
    sumPrefix (fun i => f (i + 1) - f i) n = f n - f 0 := by
  induction n with
  | zero => simp [sumPrefix]
  | succ n ih => simp only [sumPrefix, ih]; omega

/-- A cyclic difference telescopes to zero, including the last-to-first link. -/
theorem sumPrefix_cyclic_difference (f : Nat → Int) (P : Nat) (hP : 0 < P) :
    sumPrefix (fun i => f ((i + 1) % P) - f i) P = 0 := by
  have he := sumPrefix_congr P
    (f := fun i => f ((i + 1) % P) - f i)
    (g := fun i => f ((i + 1) % P) - f (i % P))
    (fun i hi => by rw [Nat.mod_eq_of_lt hi])
  rw [he, sumPrefix_difference (fun i => f (i % P))]
  simp [Nat.zero_mod, Nat.mod_self]

/-- The returned exterior block always gains precisely one position. -/
theorem Br_length (s : State) :
    (Br s.c s.B s.A s.C).length = s.B.length + 1 := by
  unfold Br
  split <;> rw [zipAdd_length] <;> simp [data, norm_length]

/-- The returned interface length is `|A|+2-gamma`, expressed without Nat subtraction. -/
theorem Ar_length (s : State) (hB : Bounded s.B) :
    (Ar s.c s.B s.A s.C).length + gam s = s.A.length + 2 := by
  have hg := gamma_le s.c s.B s.A s.C hB
  unfold Ar
  split <;> rw [zipAdd_length] <;> simp [data, norm_length, gam] at * <;> omega

/-- The returned central length is `|C|+2-gamma`, with exact pairing length. -/
theorem Cr_length (s : State) (hB : Bounded s.B) :
    (Cr s.c s.B s.A s.C).length + gam s = s.C.length + 2 := by
  have hg := gamma_le s.c s.B s.A s.C hB
  unfold Cr
  split <;> unfold pair <;> rw [zipAdd_length _ _ (by simp)] <;>
    simp [data, norm_length, gam] at * <;> omega

/-- Exact physical width balance for any accepted local trimming, maximal or not. -/
theorem local_width_balance (s s' : State) (L L' : Link)
    (h : LocalOK s s' L L') :
    width s' + 2 * (dg s L + dh s L) = width s + (gam s : Int) := by
  obtain ⟨_, hB, _, _, _, hBr, hAr, hCr, _, _, _, _, _⟩ := h
  have hb := Br_length s
  have ha := Ar_length s hB
  have hc := Cr_length s hB
  rw [hBr] at hb
  rw [hAr] at ha
  rw [hCr] at hc
  simp only [List.length_append, List.length_replicate] at hb ha hc
  unfold width dg dh
  omega

theorem local_outer_lower (s s' : State) (L L' : Link)
    (h : LocalOK s s' L L') : (L'.lo : Int) - (L.lo : Int) ≤ dg s L := by
  obtain ⟨_, _, _, _, _, _, _, _, _, _, _, hlo, _⟩ := h
  unfold dg
  omega

theorem local_inner_lower (s s' : State) (L L' : Link)
    (h : LocalOK s s' L L') : (L'.lo' : Int) - (L.lo' : Int) ≤ dh s L := by
  obtain ⟨_, _, _, _, _, _, _, _, _, _, _, _, hlo⟩ := h
  unfold dh
  omega

/-- The exact width identity summed around a valid cyclic certificate. -/
theorem totalGam_eq_twice_gains (cert : Certificate) (hv : Valid cert) :
    totalGam cert = 2 * (totalG cert + totalH cert) := by
  have he := sumPrefix_congr cert.P
    (f := fun i => (gam (cert.st i) : Int) -
      2 * (dg (cert.st i) (cert.lk i) + dh (cert.st i) (cert.lk i)))
    (g := fun i => width (cert.st ((i + 1) % cert.P)) - width (cert.st i))
    (fun i hi => by have hw := local_width_balance _ _ _ _ (hv.2 i hi); omega)
  rw [sumPrefix_cyclic_difference (fun i => width (cert.st i)) cert.P hv.1] at he
  rw [sumPrefix_sub, sumPrefix_two_mul, sumPrefix_add] at he
  change totalGam cert - 2 * (totalG cert + totalH cert) = 0 at he
  omega

theorem totalG_nonneg (cert : Certificate) (hv : Valid cert) : 0 ≤ totalG cert := by
  have he := sumPrefix_le cert.P
    (f := fun i => ((cert.lk ((i + 1) % cert.P)).lo : Int) - ((cert.lk i).lo : Int))
    (g := fun i => dg (cert.st i) (cert.lk i))
    (fun i hi => local_outer_lower _ _ _ _ (hv.2 i hi))
  rw [sumPrefix_cyclic_difference (fun i => ((cert.lk i).lo : Int)) cert.P hv.1] at he
  exact he

theorem totalH_nonneg (cert : Certificate) (hv : Valid cert) : 0 ≤ totalH cert := by
  have he := sumPrefix_le cert.P
    (f := fun i => ((cert.lk ((i + 1) % cert.P)).lo' : Int) - ((cert.lk i).lo' : Int))
    (g := fun i => dh (cert.st i) (cert.lk i))
    (fun i hi => local_inner_lower _ _ _ _ (hv.2 i hi))
  rw [sumPrefix_cyclic_difference (fun i => ((cert.lk i).lo' : Int)) cert.P hv.1] at he
  exact he

/-- Evenness of the actual total overflow, with an explicit nonnegative half. -/
theorem totalGam_even (cert : Certificate) (hv : Valid cert) :
    ∃ q : Int, 0 ≤ q ∧ totalGam cert = 2 * q := by
  refine ⟨totalG cert + totalH cert, ?_, totalGam_eq_twice_gains cert hv⟩
  have hg := totalG_nonneg cert hv
  have hh := totalH_nonneg cert hv
  omega

/-- Direct checker endpoint: no numerical accounting assumptions are supplied. -/
theorem checked_accounting (cert : Certificate) (hc : check cert = true) :
    totalGam cert = 2 * (totalG cert + totalH cert) ∧
    0 ≤ totalG cert ∧ 0 ≤ totalH cert ∧
    ∃ q : Int, 0 ≤ q ∧ totalGam cert = 2 * q := by
  have hv := check_sound cert hc
  exact ⟨totalGam_eq_twice_gains cert hv, totalG_nonneg cert hv,
    totalH_nonneg cert hv, totalGam_even cert hv⟩

end Agent110.Accounting
