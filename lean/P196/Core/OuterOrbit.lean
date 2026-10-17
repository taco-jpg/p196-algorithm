import P196.Core.OuterCharge

/-! Domain closure, leading growth, and sharp global five-step charge entry.
All statements use the explicit list map in OuterCharge, not assumed dynamics.
No ordinary-decimal semiconjugacy or P196 theorem is postulated. -/
namespace P196.Agent3.Charge

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000


/-! Domain and leading-pair bridge. -/
theorem normalize_append (a b : List Nat) (e : Nat) :
    normalize (a ++ b) e =
      ((normalize a e).1 ++ (normalize b (normalize a e).2).1,
       (normalize b (normalize a e).2).2) := by
  induction a generalizing e with
  | nil => simp [normalize]
  | cons x xs ih => simp [normalize, ih]

theorem head_append_bulk (c : Nat) (w : List Nat) :
    (w ++ [c]).headD c = w.headD c := by
  cases w <;> rfl

theorem head_trim (c : Nat) (w : List Nat) :
    (trim c w).headD c = w.headD c := by
  have h (v : List Nat) :
      ((v.dropWhile (fun x => x == c)).reverse).headD c = v.reverse.headD c := by
    induction v with
    | nil => rfl
    | cons x xs ih =>
      by_cases hc : x = c
      · subst x
        simpa [List.dropWhile_cons, List.reverse_cons, head_append_bulk] using ih
      · simp [List.dropWhile_cons_of_neg, hc]
  simpa [trim] using h w.reverse

theorem mem_trim (c x : Nat) (w : List Nat) (hx : x ∈ trim c w) : x ∈ w := by
  have h (v : List Nat) : x ∈ v.dropWhile (fun y => y == c) → x ∈ v := by
    induction v with
    | nil => simp
    | cons y ys ih =>
      by_cases hc : y = c
      · subst y
        intro hh
        have hm : x ∈ ys := ih (by simpa [List.dropWhile_cons] using hh)
        simp [hm]
      · simp [List.dropWhile_cons_of_neg, hc]
  have hm : x ∈ w.reverse := h w.reverse (by simpa [trim] using hx)
  simpa using hm

theorem normalize_digits (w : List Nat) (e x : Nat)
    (hx : x ∈ (normalize w e).1) : x ≤ 9 := by
  induction w generalizing e with
  | nil => simp [normalize] at hx
  | cons a xs ih =>
    simp only [normalize, List.mem_cons] at hx
    rcases hx with hx | hx
    · omega
    · exact ih ((a + e) / 10) hx

theorem zip_digit_bounds (a b : List Nat)
    (ha : ∀ x ∈ a, x ≤ 9) (hb : ∀ x ∈ b, x ≤ 9) :
    ∀ x ∈ List.zipWith (fun x y => x + y) a b, x ≤ 18 := by
  induction a generalizing b with
  | nil => simp
  | cons u us ih =>
    cases b with
    | nil => simp
    | cons v vs =>
      intro x hx
      simp only [List.zipWith_cons_cons, List.mem_cons] at hx
      rcases hx with hx | hx
      · have hu := ha u (by simp)
        have hv := hb v (by simp)
        omega
      · exact ih vs (by intro y hy; exact ha y (by simp [hy]))
          (by intro y hy; exact hb y (by simp [hy])) x hx

#print axioms normalize_append
#print axioms head_append_bulk
#print axioms head_trim
#print axioms mem_trim
#print axioms normalize_digits
#print axioms zip_digit_bounds


def Valid (c : Nat) (B : List Nat) : Prop :=
  1 ≤ c ∧ c ≤ 17 ∧ c ≠ 9 ∧ (∀ x ∈ B, x ≤ 18) ∧ 1 ≤ B.headD c

theorem step_phase (c : Nat) (B : List Nat) (hv : Valid c B) :
    1 ≤ (step c B).1 ∧ (step c B).1 ≤ 17 ∧ (step c B).1 ≠ 9 := by
  rcases hv with ⟨hc0, hc1, hc9, _, _⟩
  simp only [step]
  split <;> omega

theorem step_digits (c : Nat) (B : List Nat) (hv : Valid c B) :
    ∀ x ∈ (step c B).2, x ≤ 18 := by
  rcases hv with ⟨hc0, hc1, hc9, hB, _⟩
  let k := if c < 9 then 0 else 1
  let left := (normalize B 0).1 ++ [c + (normalize B 0).2 - 10 * k]
  let right := if (normalize B.reverse k).2 = 1 then
      1 :: (normalize B.reverse k).1.reverse
    else (normalize B.reverse k).1.reverse ++ [c - 9 * k]
  have he : (normalize B 0).2 ≤ 1 := normalize_carry B 0 (by omega) hB
  have ht : c - 9 * k ≤ 9 := by dsimp [k]; split <;> omega
  have hu : c + (normalize B 0).2 - 10 * k ≤ 9 := by dsimp [k]; split <;> omega
  have hl : ∀ y ∈ left, y ≤ 9 := by
    intro y hy
    simp only [left, List.mem_append, List.mem_singleton] at hy
    rcases hy with hy | hy
    · exact normalize_digits B 0 y hy
    · omega
  have hr : ∀ y ∈ right, y ≤ 9 := by
    intro y hy
    dsimp [right] at hy
    split at hy
    · simp only [List.mem_cons, List.mem_reverse] at hy
      rcases hy with hy | hy
      · omega
      · exact normalize_digits B.reverse _ y hy
    · simp only [List.mem_append, List.mem_reverse, List.mem_singleton] at hy
      rcases hy with hy | hy
      · exact normalize_digits B.reverse _ y hy
      · omega
  intro x hx
  exact zip_digit_bounds left right hl hr x (mem_trim _ x _ hx)

theorem step_head_cons (c p : Nat) (B : List Nat) :
    (step c (p :: B)).2.headD (step c (p :: B)).1 =
      if (p + (normalize B.reverse (if c < 9 then 0 else 1)).2) / 10 = 1
      then p % 10 + 1
      else p % 10 + (p + (normalize B.reverse (if c < 9 then 0 else 1)).2) % 10 := by
  simp only [step, head_trim, List.reverse_cons, normalize_append, normalize,
    List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.cons_append, Nat.add_zero]
  split <;> split <;> simp_all [List.headD]

theorem step_positive (c : Nat) (B : List Nat) (hv : Valid c B) :
    1 ≤ (step c B).2.headD (step c B).1 := by
  rcases hv with ⟨hc0, hc1, hc9, hB, hp⟩
  cases B with
  | nil =>
    simp only [step, normalize, List.reverse_nil, head_trim, List.nil_append]
    split <;> simp_all [List.headD] <;> omega
  | cons p B =>
    rw [step_head_cons]
    have hp0 : 1 ≤ p := hp
    have hp1 : p ≤ 18 := hB p (by simp)
    have he : (normalize B.reverse (if c < 9 then 0 else 1)).2 ≤ 1 := by
      apply normalize_carry
      · split <;> omega
      · intro x hx
        exact hB x (by simp [List.mem_reverse] at hx; simp [hx])
    by_cases hg : (p + (normalize B.reverse (if c < 9 then 0 else 1)).2) / 10 = 1
    · rw [if_pos hg]; omega
    · rw [if_neg hg]; omega

theorem step_valid (c : Nat) (B : List Nat) (hv : Valid c B) :
    Valid (step c B).1 (step c B).2 := by
  have hp := step_phase c B hv
  exact ⟨hp.1, hp.2.1, hp.2.2, step_digits c B hv, step_positive c B hv⟩

theorem nonoverflow_leading_growth (c : Nat) (B : List Nat) (hv : Valid c B)
    (hg : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 0) :
    2 * B.headD c ≤ (step c B).2.headD (step c B).1 := by
  rcases hv with ⟨hc0, hc1, hc9, hB, hp⟩
  cases B with
  | nil =>
    simp only [List.reverse_nil, normalize] at hg
    have hlo : c < 9 := by split at hg <;> omega
    simp only [step, normalize, List.reverse_nil, if_pos hlo, Nat.mul_zero,
      Nat.sub_zero, Nat.add_zero, List.nil_append]
    rw [head_trim]
    simp
    omega
  | cons p B =>
    rw [step_head_cons]
    have he : (normalize B.reverse (if c < 9 then 0 else 1)).2 ≤ 1 := by
      apply normalize_carry
      · split <;> omega
      · intro x hx
        exact hB x (by simp [List.mem_reverse] at hx; simp [hx])
    simp only [List.reverse_cons, normalize_append, normalize] at hg
    have hnot : (p + (normalize B.reverse (if c < 9 then 0 else 1)).2) / 10 ≠ 1 := by omega
    rw [if_neg hnot]
    simp only [List.headD_cons]
    omega

#print axioms step_phase
#print axioms step_digits
#print axioms step_head_cons
#print axioms step_positive
#print axioms step_valid
#print axioms nonoverflow_leading_growth


def advance (s : Nat × List Nat) : Nat × List Nat := step s.1 s.2

def orbit : Nat → (Nat × List Nat) → Nat × List Nat
  | 0, s => s
  | n + 1, s => advance (orbit n s)

theorem leading_bounds (c : Nat) (B : List Nat) (hv : Valid c B) :
    1 ≤ B.headD c ∧ B.headD c ≤ 18 := by
  refine ⟨hv.2.2.2.2, ?_⟩
  cases B with
  | nil => exact Nat.le_trans hv.2.1 (by decide)
  | cons p tail => exact hv.2.2.2.1 p (by simp)

theorem orbit_valid (n : Nat) (s : Nat × List Nat) (hv : Valid s.1 s.2) :
    Valid (orbit n s).1 (orbit n s).2 := by
  induction n with
  | zero => exact hv
  | succ n ih => exact step_valid _ _ ih

theorem nonzero_step_growth (c : Nat) (B : List Nat) (hv : Valid c B)
    (hnz : charge (step c B).1 (step c B).2 % 11 ≠ 0) :
    charge c B % 11 ≠ 0 ∧
    2 * B.headD c ≤ (step c B).2.headD (step c B).1 := by
  have hin : charge c B % 11 ≠ 0 := by
    intro hzero
    exact hnz (step_charge_preserves_zero c B hv.1 hv.2.1 hv.2.2.1 hv.2.2.2.1 hzero)
  have hg : (normalize B.reverse (if c < 9 then 0 else 1)).2 ≤ 1 := by
    apply normalize_carry
    · split <;> omega
    · intro x hx
      exact hv.2.2.2.1 x (by simpa using hx)
  have hzero : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 0 := by
    apply Classical.byContradiction
    intro h
    have hone : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 1 := by omega
    exact hnz (step_charge_overflow c B hv.1 hv.2.1 hv.2.2.1 hone)
  exact ⟨hin, nonoverflow_leading_growth c B hv hzero⟩

theorem nonzero_orbit_lower_bound (n : Nat) (s : Nat × List Nat)
    (hv : Valid s.1 s.2) (hnz : charge (orbit n s).1 (orbit n s).2 % 11 ≠ 0) :
    2 ^ n ≤ (orbit n s).2.headD (orbit n s).1 := by
  induction n with
  | zero => exact (leading_bounds _ _ hv).1
  | succ n ih =>
    have h := nonzero_step_growth _ _ (orbit_valid n s hv) hnz
    have hprev := ih h.1
    simp only [Nat.pow_succ]
    change 2 ^ n * 2 ≤ (step (orbit n s).1 (orbit n s).2).2.headD (step (orbit n s).1 (orbit n s).2).1
    omega

theorem charge_zero_after_five (s : Nat × List Nat) (hv : Valid s.1 s.2) :
    charge (orbit 5 s).1 (orbit 5 s).2 % 11 = 0 := by
  apply Classical.byContradiction
  intro hnz
  have hlo := nonzero_orbit_lower_bound 5 s hv hnz
  have hhi := (leading_bounds _ _ (orbit_valid 5 s hv)).2
  change 32 ≤ (orbit 5 s).2.headD (orbit 5 s).1 at hlo
  omega

theorem zero_charge_orbit (n : Nat) (s : Nat × List Nat)
    (hv : Valid s.1 s.2) (hz : charge s.1 s.2 % 11 = 0) :
    charge (orbit n s).1 (orbit n s).2 % 11 = 0 := by
  induction n with
  | zero => exact hz
  | succ n ih =>
    have h := orbit_valid n s hv
    exact step_charge_preserves_zero _ _ h.1 h.2.1 h.2.2.1 h.2.2.2.1 ih

theorem orbit_add (n m : Nat) (s : Nat × List Nat) :
    orbit (n + m) s = orbit n (orbit m s) := by
  induction n with
  | zero => simp [orbit]
  | succ n ih => simp [Nat.succ_add, orbit, ih]

theorem charge_zero_from_five (n : Nat) (s : Nat × List Nat)
    (hv : Valid s.1 s.2) (hn : 5 ≤ n) :
    charge (orbit n s).1 (orbit n s).2 % 11 = 0 := by
  have h := zero_charge_orbit (n - 5) (orbit 5 s)
    (orbit_valid 5 s hv) (charge_zero_after_five s hv)
  rw [← orbit_add] at h
  have heq : n - 5 + 5 = n := by omega
  simpa only [heq] using h

theorem orbit_multiple_return (P k : Nat) (s : Nat × List Nat)
    (hreturn : orbit P s = s) : orbit (P * k) s = s := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Nat.mul_succ, orbit_add, hreturn, ih]

theorem returned_outer_charge_zero (P : Nat) (s : Nat × List Nat)
    (hP : 0 < P) (hv : Valid s.1 s.2) (hreturn : orbit P s = s) :
    charge s.1 s.2 % 11 = 0 := by
  have hz := charge_zero_from_five (P * 5) s hv (by omega)
  simpa only [orbit_multiple_return P 5 s hreturn] using hz

#print axioms leading_bounds
#print axioms orbit_valid
#print axioms nonzero_step_growth
#print axioms nonzero_orbit_lower_bound
#print axioms charge_zero_after_five
#print axioms zero_charge_orbit
#print axioms orbit_add
#print axioms charge_zero_from_five
#print axioms orbit_multiple_return
#print axioms returned_outer_charge_zero


theorem five_step_bound_sharp :
    Valid 1 [] ∧ charge (orbit 4 (1, [])).1 (orbit 4 (1, [])).2 % 11 ≠ 0 ∧
    charge (orbit 5 (1, [])).1 (orbit 5 (1, [])).2 % 11 = 0 := by
  constructor
  · simp [Valid, List.headD]
  · decide +kernel

#print axioms five_step_bound_sharp

end P196.Agent3.Charge
