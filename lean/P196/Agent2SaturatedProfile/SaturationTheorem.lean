import P196.Agent2SaturatedProfile.SaturationCertificate

namespace P196.Agent4.Saturation

/-- The abstraction includes both possible incoming inner carry bits. -/
def Valid (s : Prefix) : Prop :=
  0 < s.a ∧ s.a ≤ 18 ∧ s.b ≤ 18 ∧ s.c ≤ 18

theorem finite_certificate (a b c e : Nat)
    (ha : 0 < a ∧ a ≤ 18) (hb : b ≤ 18) (hc : c ≤ 18) (he : e ≤ 1) :
    Check a b c e := by
  have casesA : a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases casesA with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  · subst a
    exact row1 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row2 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row3 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row4 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row5 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row6 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row7 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row8 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row9 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row10 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row11 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row12 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row13 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row14 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row15 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row16 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row17 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩
  · subst a
    exact row18 ⟨b, by omega⟩ ⟨c, by omega⟩ ⟨e, by omega⟩

theorem prefix_certificate (s : Prefix) (e : Nat) (hv : Valid s) (he : e ≤ 1) :
    82*(advance s e).2 + potential (advance s e).1 ≤ 41 + potential s ∧
    (82*(advance s e).2 + potential (advance s e).1 = 41 + potential s →
      clock (advance s e).1 = (clock s + 1) % 8) := by
  exact finite_certificate s.a s.b s.c e ⟨hv.1,hv.2.1⟩ hv.2.2.1 hv.2.2.2 he

/-- This 36-case check supplies positivity of the overflow count on closed walks. -/
theorem exterior_progress : ∀ a : Fin 19, ∀ r : Fin 2, 0 < a.val →
    a.val + 1 ≤
      (if (a.val+r.val)/10 = 0 then a.val%10 + (a.val+r.val)%10
       else a.val%10 + 1) + 10*((a.val+r.val)/10) := by decide +kernel

theorem prefix_progress (s : Prefix) (e : Nat) (hv : Valid s) (he : e ≤ 1) :
    s.a + 1 ≤ (advance s e).1.a + 10*(advance s e).2 := by
  have hr : (s.b + (s.c+e)/10)/10 ≤ 1 := by
    have hb := hv.2.2.1
    have hc := hv.2.2.2
    omega
  have h := exterior_progress ⟨s.a, by have hh:=hv.2.1; omega⟩
    ⟨(s.b+(s.c+e)/10)/10, by omega⟩ hv.1
  dsimp at h
  unfold advance
  dsimp only
  split <;> simp_all

def total (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n+1 => total f n + f n

theorem budget_telescope (u g : Nat → Nat) (n : Nat)
    (h : ∀ i < n, 82*g i + u (i+1) ≤ 41+u i) :
    82*total g n + u n ≤ 41*n + u 0 := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [total]
    omega

theorem progress_telescope (p g : Nat → Nat) (n : Nat)
    (h : ∀ i < n, p i + 1 ≤ p (i+1)+10*g i) :
    p 0 + n ≤ p n + 10*total g n := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [total]
    omega

theorem tight_clock_telescope (u g c : Nat → Nat) (n : Nat)
    (h : ∀ i < n, 82*g i + u (i+1) ≤ 41+u i ∧
      (82*g i + u (i+1) = 41+u i → c (i+1) = (c i+1)%8))
    (htight : 82*total g n + u n = 41*n + u 0) :
    c n % 8 = (c 0+n)%8 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hp := budget_telescope u g n (fun i hi => (h i (by omega)).1)
    have hs := h n (by omega)
    have heq : 82*total g n + u n = 41*n + u 0 := by
      simp only [total] at htight
      omega
    have heqlast : 82*g n + u (n+1) = 41+u n := by
      simp only [total] at htight
      omega
    have hc := hs.2 heqlast
    have hind := ih (fun i hi => h i (by omega)) heq
    omega

/-- Fully checked statement about the explicitly defined finite prefix relation. -/
theorem saturated_closed_prefix_period (s : Nat → Prefix) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i < n, Valid (s i)) (he : ∀ i < n, e i ≤ 1)
    (hs : ∀ i < n, (advance (s i) (e i)).1 = s (i+1))
    (hclose : s n = s 0)
    (hsaturated : 2*total (fun i => (advance (s i) (e i)).2) n = n) :
    n%8 = 0 := by
  let g := fun i => (advance (s i) (e i)).2
  have hcert : ∀ i < n, 82*g i + potential (s (i+1)) ≤ 41+potential (s i) ∧
      (82*g i + potential (s (i+1)) = 41+potential (s i) →
        clock (s (i+1)) = (clock (s i)+1)%8) := by
    intro i hi
    have h := prefix_certificate (s i) (e i) (hv i hi) (he i hi)
    simpa only [hs i hi] using h
  have ht : 82*total g n + potential (s n) = 41*n + potential (s 0) := by
    rw [hclose]
    change 2*total g n = n at hsaturated
    omega
  have hclock := tight_clock_telescope (fun i => potential (s i)) g
    (fun i => clock (s i)) n hcert ht
  dsimp only at hclock
  rw [hclose] at hclock
  omega

theorem closed_prefix_overflow_bounds (s : Nat → Prefix) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i < n, Valid (s i)) (he : ∀ i < n, e i ≤ 1)
    (hs : ∀ i < n, (advance (s i) (e i)).1 = s (i+1))
    (hclose : s n = s 0) :
    2*total (fun i => (advance (s i) (e i)).2) n ≤ n ∧
    n ≤ 10*total (fun i => (advance (s i) (e i)).2) n := by
  let g := fun i => (advance (s i) (e i)).2
  have hb := budget_telescope (fun i => potential (s i)) g n (by
    intro i hi
    have h := (prefix_certificate (s i) (e i) (hv i hi) (he i hi)).1
    simpa only [hs i hi] using h)
  have hp := progress_telescope (fun i => (s i).a) g n (by
    intro i hi
    have h := prefix_progress (s i) (e i) (hv i hi) (he i hi)
    simpa only [hs i hi] using h)
  dsimp only at hb hp
  rw [hclose] at hb hp
  change 2*total g n ≤ n ∧ n ≤ 10*total g n
  omega

/-- The even and mod-nine hypotheses must be supplied by a full quotient cycle.
They are not assertions that arbitrary prefix cycles obey those congruences. -/
theorem unit_phase_full_cycle_period_at_least_forty_two
    (s : Nat → Prefix) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i < n, Valid (s i)) (he : ∀ i < n, e i ≤ 1)
    (hs : ∀ i < n, (advance (s i) (e i)).1 = s (i+1))
    (hclose : s n = s 0) (hn : 0 < n) (hphase : n%6=0)
    (heven : total (fun i => (advance (s i) (e i)).2) n % 2 = 0)
    (hnine : total (fun i => (advance (s i) (e i)).2) n % 9 = 0) :
    42 ≤ n := by
  have hb := closed_prefix_overflow_bounds s e n hv he hs hclose
  have hsat := saturated_closed_prefix_period s e n hv he hs hclose
  omega

#print axioms finite_certificate
#print axioms prefix_certificate
#print axioms exterior_progress
#print axioms prefix_progress
#print axioms budget_telescope
#print axioms progress_telescope
#print axioms tight_clock_telescope
#print axioms saturated_closed_prefix_period
#print axioms closed_prefix_overflow_bounds
#print axioms unit_phase_full_cycle_period_at_least_forty_two

end P196.Agent4.Saturation
