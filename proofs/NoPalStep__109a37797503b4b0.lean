import ReturnCertificate

/-!
Agent #109: the actual successor of an integer realizing a complementary
two-gap template (both bands at least two) is never a palindrome.

Proof: the band-length-independent criterion `Agent109.Cert.StepPal` would force
equal digit sums of mirrored normalized blocks; normalization preserves the
digit sum plus carries modulo nine, and the complementary carries
`k_c + k_d = 1` then give a contradiction modulo nine in both the
no-overflow and the overflow case.

No cycle, safe orbit or statement about 196 is claimed.
-/

namespace Agent109.NoPal

open Agent109 Agent109.Cert

def dsum : Word → Nat
  | [] => 0
  | x :: xs => x + dsum xs

theorem dsum_append (a b : Word) : dsum (a ++ b) = dsum a + dsum b := by
  induction a with
  | nil => simp [dsum]
  | cons x xs ih => simp [dsum, ih]; omega

theorem dsum_reverse (a : Word) : dsum a.reverse = dsum a := by
  induction a with
  | nil => rfl
  | cons x xs ih => simp [dsum, dsum_append, ih]; omega

/-- Normalization keeps digit sum plus carries modulo nine. -/
theorem norm_mod9 (w : Word) (e : Nat) :
    (dsum (norm w e).1 + (norm w e).2) % 9 = (dsum w + e) % 9 := by
  induction w generalizing e with
  | nil => simp [norm, dsum]
  | cons x xs ih =>
    have := ih ((x + e) / 10)
    simp only [norm, dsum]
    omega

theorem kOf_cases (x : Nat) : (kOf x = 1 ∧ 10 ≤ x) ∨ (kOf x = 0 ∧ x < 10) := by
  unfold kOf; split <;> omega

/-- **No palindromic step.** For every phase and bounded blocks, the
band-length-independent palindrome criterion of the next integer fails. -/
theorem not_stepPal (c : Nat) (B A C : Word) (hc : Phase c) (hB : Bounded B)
    (hA : Bounded A) : ¬ StepPal c B A C := by
  have hk := complement_k c hc
  have hph := hc
  unfold Phase at hph
  have kc := kOf_cases c
  have kd := kOf_cases (18 - c)
  have kc1 : kOf c ≤ 1 := by rcases kc with h | h <;> omega
  have kd1 : kOf (18 - c) ≤ 1 := by rcases kd with h | h <;> omega
  have m0 := norm_mod9 B 0
  have m1 := norm_mod9 A (kOf c)
  have m3 := norm_mod9 A.reverse (kOf (18 - c))
  have m4 := norm_mod9 B.reverse (kOf c)
  rw [dsum_reverse] at m3 m4
  have e0 := norm_carry_le B 0 hB (by decide)
  have e1 := norm_carry_le A (kOf c) hA kc1
  have e3 := norm_carry_le A.reverse (kOf (18 - c)) (bounded_reverse A hA) kd1
  have e4 := norm_carry_le B.reverse (kOf c) (bounded_reverse B hB) kc1
  have ht : tOf c = c - 9 * kOf c := rfl
  have htd : tOf (18 - c) = (18 - c) - 9 * kOf (18 - c) := rfl
  intro h
  unfold StepPal at h
  simp only [data, u0, u1, u2, u3] at h
  generalize hDB : (norm B 0).1 = DB at *
  generalize hDA : (norm A (kOf c)).1 = DA at *
  generalize hDRA : (norm A.reverse (kOf (18 - c))).1 = DRA at *
  generalize hDRB : (norm B.reverse (kOf c)).1 = DRB at *
  generalize hE0 : (norm B 0).2 = E0 at *
  generalize hE1 : (norm A (kOf c)).2 = E1 at *
  generalize hE3 : (norm A.reverse (kOf (18 - c))).2 = E3 at *
  generalize hG : (norm B.reverse (kOf c)).2 = G at *
  split at h
  · -- no overflow: the interface blocks must mirror
    rename_i hG0
    obtain ⟨-, h2, -⟩ := h
    have hs := congrArg dsum h2
    have hh := congrArg List.head? h2
    simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
      List.singleton_append, List.cons_append, List.head?_cons] at hh
    simp only [dsum_append, dsum_reverse, dsum, List.reverse_append, List.reverse_cons,
      List.reverse_nil, List.nil_append, List.singleton_append, List.cons_append] at hs
    simp at hh
    rcases kc with ⟨hk1, hc1⟩ | ⟨hk1, hc1⟩ <;> rcases kd with ⟨hk2, hd2⟩ | ⟨hk2, hd2⟩ <;>
      omega
  · -- overflow
    rename_i hG0
    obtain ⟨h1, h2, -⟩ := h
    have hs1 := congrArg dsum h1
    have hs2 := congrArg dsum h2
    simp only [dsum_append, dsum_reverse, dsum, List.reverse_append, List.reverse_cons,
      List.reverse_nil, List.nil_append, List.singleton_append, List.cons_append] at hs1 hs2
    rcases kc with ⟨hk1, hc1⟩ | ⟨hk1, hc1⟩ <;> rcases kd with ⟨hk2, hd2⟩ | ⟨hk2, hd2⟩ <;>
      omega

/-! ## Successor blocks stay bounded (same proof as `Agent109.Outer.succ_bounded`) -/

theorem norm_digits_le (w : Word) (e : Nat) : ∀ y ∈ (norm w e).1, y ≤ 9 := by
  intro y hy; have := norm_digit_lt w e y hy; omega

theorem zipAdd_le (a b : Word) (ha : ∀ y ∈ a, y ≤ 9) (hb : ∀ y ∈ b, y ≤ 9) :
    Bounded (zipAdd a b) := by
  induction a generalizing b with
  | nil => intro z hz; cases b <;> simp [zipAdd] at hz
  | cons x xs ih =>
    intro z hz
    cases b with
    | nil => simp [zipAdd] at hz
    | cons y ys =>
      simp only [zipAdd, List.mem_cons] at hz
      rcases hz with hz | hz
      · have := ha x (by simp); have := hb y (by simp); omega
      · exact ih ys (fun t ht => ha t (by simp [ht])) (fun t ht => hb t (by simp [ht])) z hz

theorem k_le (x : Nat) : kOf x ≤ 1 := by unfold kOf; split <;> omega

theorem t_le (x : Nat) (hx : x ≤ 18) : tOf x ≤ 9 := by unfold tOf kOf; split <;> omega

theorem u_le (x e : Nat) (hx : x ≤ 18) (hx9 : x ≠ 9) (he : e ≤ 1) : x + e - 10 * kOf x ≤ 9 := by
  unfold kOf; split <;> omega

theorem succ_bounded (c : Nat) (B A C : Word) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    Bounded (Br c B A C) ∧ Bounded (Ar c B A C) ∧ Bounded (Cr c B A C) := by
  have hc' := complement_phase c hc
  unfold Phase at hc hc'
  have e0 := norm_carry_le B 0 hB (by decide)
  have e1 := norm_carry_le A (kOf c) hA (k_le c)
  have e2 := norm_carry_le C (kOf (18 - c)) hC (k_le _)
  have e3 := norm_carry_le A.reverse (kOf (18 - c)) (bounded_reverse A hA) (k_le _)
  have hu0 : u0 c B A C ≤ 9 := u_le c _ (by omega) hc.2.2 e0
  have hu1 : u1 c B A C ≤ 9 := u_le (18 - c) _ (by omega) hc'.2.2 e1
  have hu2 : u2 c B A C ≤ 9 := u_le (18 - c) _ (by omega) hc'.2.2 e2
  have hu3 : u3 c B A C ≤ 9 := u_le c _ (by omega) hc.2.2 e3
  have htc := t_le c (by omega)
  have htd := t_le (18 - c) (by omega)
  have dB := norm_digits_le B 0
  have dA := norm_digits_le A (kOf c)
  have dC := norm_digits_le C (kOf (18 - c))
  have dRA := norm_digits_le A.reverse (kOf (18 - c))
  have dRB := norm_digits_le B.reverse (kOf c)
  refine ⟨?_, ?_, ?_⟩
  · unfold Br; split
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with hy | hy; exact dB y hy; omega
      · intro y hy; simp only [List.mem_append, List.mem_singleton, List.mem_reverse] at hy
        rcases hy with hy | hy; exact dRB y hy; omega
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with hy | hy; exact dB y hy; omega
      · intro y hy; simp only [List.mem_append, List.mem_singleton, List.mem_reverse] at hy
        rcases hy with hy | hy; omega; exact dRB y hy
  · unfold Ar; split
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with (hy | hy) | hy; omega; exact dA y hy; omega
      · intro y hy; simp only [List.mem_append, List.mem_singleton, List.mem_reverse] at hy
        rcases hy with (hy | hy) | hy; omega; exact dRA y hy; omega
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with hy | hy; exact dA y hy; omega
      · intro y hy; simp only [List.mem_append, List.mem_singleton, List.mem_reverse] at hy
        rcases hy with hy | hy; omega; exact dRA y hy
  · unfold Cr pair; split
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with (hy | hy) | hy; omega; exact dC y hy; omega
      · intro y hy; simp only [List.mem_reverse, List.mem_append, List.mem_singleton] at hy
        rcases hy with (hy | hy) | hy; omega; exact dC y hy; omega
    · apply zipAdd_le
      · intro y hy; simp only [List.mem_append, List.mem_singleton] at hy
        rcases hy with hy | hy; exact dC y hy; omega
      · intro y hy; simp only [List.mem_reverse, List.mem_append, List.mem_singleton] at hy
        rcases hy with hy | hy; exact dC y hy; omega


/-! ## Ordinary-integer consequences -/

/-- The next integer after any realized complementary template (bands ≥ 2) is
not a palindrome. -/
theorem template_step_not_palindrome (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C (g + 2) (h + 2)) :
    ¬ Palindrome (step n) := by
  rw [step_palindrome_template n c B A C g h hc hB hA hC hn]
  exact not_stepPal c B A C hc hB hA

/-- **Long bands give a long palindrome-free stretch.** If `n` realizes a
complementary template with both bands at least `2k+2`, then the ordinary orbit
of `n` has no palindrome at times `1, …, k+1`. -/
theorem template_orbit_safe (n c : Nat) (B A C : Word) (g h k : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hg : 2 * k + 2 ≤ g) (hh : 2 * k + 2 ≤ h)
    (hn : pairWord n = template c B A C g h) :
    ∀ i, 1 ≤ i → i ≤ k + 1 → ¬ Palindrome (orbit n i) := by
  -- invariant: at time i ≤ k the orbit integer realizes a template with bands ≥ g-2i, h-2i
  have inv : ∀ i, i ≤ k → ∃ c' B' A' C' G H, Phase c' ∧ Bounded B' ∧ Bounded A' ∧
      Bounded C' ∧ g ≤ G + 2 * i ∧ h ≤ H + 2 * i ∧
      pairWord (orbit n i) = template c' B' A' C' G H := by
    intro i
    induction i with
    | zero => intro _; exact ⟨c, B, A, C, g, h, hc, hB, hA, hC, by omega, by omega, hn⟩
    | succ i ih =>
      intro hi
      obtain ⟨c', B', A', C', G, H, hc', hB', hA', hC', hG, hH, hrep⟩ := ih (by omega)
      obtain ⟨G', rfl⟩ : ∃ G', G = G' + 2 := ⟨G - 2, by omega⟩
      obtain ⟨H', rfl⟩ : ∃ H', H = H' + 2 := ⟨H - 2, by omega⟩
      have hs := actual_template_step (orbit n i) c' B' A' C' G' H' hc' hB' hA' hC' hrep
      have hbd := succ_bounded c' B' A' C' hc' hB' hA' hC'
      exact ⟨tOf c' + tOf c', Br c' B' A' C', Ar c' B' A' C', Cr c' B' A' C',
        G' + (data c' B' A' C').γ, H' + (data c' B' A' C').γ, next_phase c' hc', hbd.1,
        hbd.2.1, hbd.2.2, by omega, by omega, by rw [orbit]; exact hs⟩
  intro i hi1 hik
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  obtain ⟨c', B', A', C', G, H, hc', hB', hA', hC', hG, hH, hrep⟩ := inv j (by omega)
  obtain ⟨G', rfl⟩ : ∃ G', G = G' + 2 := ⟨G - 2, by omega⟩
  obtain ⟨H', rfl⟩ : ∃ H', H = H' + 2 := ⟨H - 2, by omega⟩
  rw [orbit]
  exact template_step_not_palindrome _ c' B' A' C' G' H' hc' hB' hA' hC' hrep

end Agent109.NoPal

#print axioms Agent109.NoPal.norm_mod9
#print axioms Agent109.NoPal.not_stepPal
#print axioms Agent109.NoPal.template_step_not_palindrome
#print axioms Agent109.NoPal.template_orbit_safe
