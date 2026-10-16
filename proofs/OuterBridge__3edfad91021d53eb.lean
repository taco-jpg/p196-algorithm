import ReturnCertificate
import OuterBounds

/-!
Agent #109: Lean bridge from Agent #7's exterior map
`P196.Agent7.Finite.outerNext` (branch `agent7/outer-boundary-audit` @ `da4a179`)
to the actual complementary template step (`Agent109.stepWord_template`,
`Agent109.actual_template_step`).

* `outerNext_eq`: Agent #7's raw exterior word is exactly `Agent109.Br c B A C`
  (for every interface `A` and center `C`), and `outerNext` is the maximally
  B-trimmed exterior of the actual successor.
* `actual_step_outer`: one ordinary reverse-and-add step of an integer realizing
  a template realizes the template with exterior `outerNext (c,B)`.
* `actual_outer_orbit`: along the ordinary orbit, the specified exterior
  follows Agent #7's `outerIterate` as long as both bands stay at least two;
  each transition maximally strips the new exterior. The initial exterior
  is not required to be trimmed in this general theorem.
* `actual_cap2_exit`: with Agent #7's kernel-checked `cap2_exits_by_seven`, an
  integer realizing a template with a valid exterior of length at most two and
  bands at least 14 reaches, within 7 ordinary steps, a template representation
  whose trimmed exterior has length greater than two.

No cycle, safe orbit or statement about 196 is claimed.
-/

namespace Agent109.Outer

open Agent109
open P196.Agent7.Finite (Outer outerNext stripSuffix outerIterate validOuter staysSmall
  cap2_unencoded exit_witness_of_false)

theorem normalize7_eq (w : Word) (e : Nat) :
    P196.Agent7.Finite.normalize w e = norm w e := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [P196.Agent7.Finite.normalize, norm, ih]

theorem kOf_eq (c : Nat) : (if 10 ≤ c then 1 else 0) = kOf c := rfl

/-- Agent #7's outer map is the trimmed exterior of the exact successor (8). -/
theorem outerNext_eq (c : Nat) (B A C : Word) :
    outerNext ⟨c, B⟩ = ⟨tOf c + tOf c, stripSuffix (tOf c + tOf c) (Br c B A C)⟩ := by
  have h2 : 2 * (c - 9 * kOf c) = tOf c + tOf c := by unfold tOf; omega
  simp only [outerNext, normalize7_eq, kOf_eq, Br, data, u0]
  by_cases hγ : (norm B.reverse (kOf c)).2 = 0
  · simp [hγ, h2, zipAdd_eq_zipWith, tOf]
  · have hb : ((norm B.reverse (kOf c)).2 == 0) = false := by simpa using hγ
    simp [hγ, hb, h2, zipAdd_eq_zipWith]

theorem stripSuffix_spec (c : Nat) (w : Word) :
    ∃ j, w = stripSuffix c w ++ List.replicate j c := by
  have hsplit := List.takeWhile_append_dropWhile (p := fun x => x == c) (l := w.reverse)
  have hrep : ∃ j, w.reverse.takeWhile (fun x => x == c) = List.replicate j c := by
    refine ⟨(w.reverse.takeWhile (fun x => x == c)).length, ?_⟩
    apply List.eq_replicate_iff.mpr
    refine ⟨rfl, ?_⟩
    intro x hx
    have key : ∀ l : Word, ∀ x ∈ l.takeWhile (fun x => x == c), x = c := by
      intro l; induction l with
      | nil => simp
      | cons y ys ih =>
        intro x hx
        by_cases hy : (y == c) = true
        · simp only [List.takeWhile_cons, hy, if_true] at hx
          rcases List.mem_cons.mp hx with h | h
          · subst h; simpa using hy
          · exact ih x h
        · simp only [List.takeWhile_cons, hy] at hx; simp at hx
    exact key _ x hx
  obtain ⟨j, hj⟩ := hrep
  refine ⟨j, ?_⟩
  have := congrArg List.reverse hsplit
  rw [List.reverse_reverse, List.reverse_append, hj, List.reverse_replicate] at this
  unfold stripSuffix
  exact this.symm

/-! ## Boundedness of the successor blocks -/

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

theorem bounded_strip (c : Nat) (w : Word) (hw : Bounded w) : Bounded (stripSuffix c w) := by
  obtain ⟨j, hj⟩ := stripSuffix_spec c w
  intro x hx; apply hw; rw [hj]; exact List.mem_append_left _ hx

/-! ## One actual step in outer form -/

theorem actual_step_outer (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C (g + 2) (h + 2)) :
    ∃ G, g ≤ G ∧ pairWord (step n) =
      template (outerNext ⟨c, B⟩).c (outerNext ⟨c, B⟩).B (Ar c B A C) (Cr c B A C)
        G (h + (data c B A C).γ) := by
  have hs := actual_template_step n c B A C g h hc hB hA hC hn
  obtain ⟨j, hj⟩ := stripSuffix_spec (tOf c + tOf c) (Br c B A C)
  rw [outerNext_eq c B A C]
  refine ⟨g + (data c B A C).γ + j + 0, by omega, ?_⟩
  have ht := Cert.template_trim (tOf c + tOf c)
    (stripSuffix (tOf c + tOf c) (Br c B A C)) (Ar c B A C) (Cr c B A C) j 0 0 0
    (g + (data c B A C).γ) (h + (data c B A C).γ)
  simp only [List.replicate_zero, List.nil_append, List.append_nil, Nat.add_zero] at ht
  rw [← hj] at ht
  rw [hs, ht]
  rfl

/-- Forward iterate of Agent #7's outer map. -/
def outerIter : Nat → Outer → Outer
  | 0, s => s
  | i + 1, s => outerNext (outerIter i s)

theorem outerIterate_eq (i : Nat) (s : Outer) : outerIterate i s = outerIter i s := by
  induction i generalizing s with
  | zero => rfl
  | succ i ih =>
    show outerIterate i (outerNext s) = outerNext (outerIter i s)
    rw [ih]
    clear ih
    induction i generalizing s with
    | zero => rfl
    | succ i ih2 => show outerNext (outerIter i (outerNext s)) = _; rw [ih2]; rfl

/-- **Actual outer orbit.** While both bands have stayed at least two, the
ordinary orbit of an integer realizing a template has, at time `i`, a template
representation whose phase and specified exterior are `outerIter i (c,B)`.
The initial exterior need not be trimmed; every positive-time exterior is
maximally suffix-trimmed by the preceding `outerNext` transition. -/
theorem actual_outer_orbit (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C g h) :
    ∀ i, 2 * i ≤ g → 2 * i ≤ h →
      ∃ A' C' G H, Phase (outerIter i ⟨c, B⟩).c ∧ Bounded (outerIter i ⟨c, B⟩).B ∧
        Bounded A' ∧ Bounded C' ∧ g ≤ G + 2 * i ∧ h ≤ H + 2 * i ∧
        pairWord (orbit n i) =
          template (outerIter i ⟨c, B⟩).c (outerIter i ⟨c, B⟩).B A' C' G H := by
  intro i
  induction i with
  | zero => intro _ _; exact ⟨A, C, g, h, hc, hB, hA, hC, by omega, by omega, hn⟩
  | succ i ih =>
    intro hg hh
    obtain ⟨A', C', G, H, hci, hBi, hAi, hCi, hG, hH, hrep⟩ := ih (by omega) (by omega)
    obtain ⟨G', rfl⟩ : ∃ G', G = G' + 2 := ⟨G - 2, by omega⟩
    obtain ⟨H', rfl⟩ : ∃ H', H = H' + 2 := ⟨H - 2, by omega⟩
    obtain ⟨G2, hG2, hstep⟩ := actual_step_outer (orbit n i) _ _ _ _ G' H' hci hBi hAi hCi hrep
    have hbd := succ_bounded _ _ _ _ hci hBi hAi hCi
    refine ⟨Ar (outerIter i ⟨c, B⟩).c (outerIter i ⟨c, B⟩).B A' C',
      Cr (outerIter i ⟨c, B⟩).c (outerIter i ⟨c, B⟩).B A' C', G2,
      H' + (data (outerIter i ⟨c, B⟩).c (outerIter i ⟨c, B⟩).B A' C').γ, ?_, ?_, hbd.2.1, hbd.2.2,
      by omega, by omega, ?_⟩
    · show Phase (outerNext (outerIter i ⟨c, B⟩)).c
      rw [outerNext_eq _ _ A' C']; exact next_phase _ hci
    · show Bounded (outerNext (outerIter i ⟨c, B⟩)).B
      rw [outerNext_eq _ _ A' C']; exact bounded_strip _ _ hbd.1
    · show pairWord (step (orbit n i)) = _
      rw [hstep]; rfl

/-- **Ordinary-integer cap-two exit.** If `n` realizes a template with an even
phase `2(p+1)`, a valid (Agent #7 `validOuter`) exterior of length at most two
and both bands at least 14, then within 7 ordinary reverse-and-add steps the
orbit has a template representation with Agent #7's trimmed exterior of length
greater than two. -/
theorem actual_cap2_exit (n : Nat) (p : Fin 8) (B A C : Word) (g h : Nat)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hlen : B.length ≤ 2) (hvalid : validOuter ⟨2 * (p.val + 1), B⟩ = true)
    (hg : 14 ≤ g) (hh : 14 ≤ h)
    (hn : pairWord n = template (2 * (p.val + 1)) B A C g h) :
    ∃ i, i ≤ 7 ∧ ∃ c' B' A' C' G H, 2 < B'.length ∧
      B' = (outerIterate i ⟨2 * (p.val + 1), B⟩).B ∧
      pairWord (orbit n i) = template c' B' A' C' G H := by
  have hc : Phase (2 * (p.val + 1)) := by
    have := p.isLt; unfold Phase; omega
  obtain ⟨i, hi, hex⟩ := exit_witness_of_false 7 _ (cap2_unencoded p B hlen hB hvalid)
  obtain ⟨A', C', G, H, -, -, -, -, -, -, hrep⟩ :=
    actual_outer_orbit n _ B A C g h hc hB hA hC hn i (by omega) (by omega)
  refine ⟨i, hi, (outerIterate i ⟨2 * (p.val + 1), B⟩).c,
    (outerIterate i ⟨2 * (p.val + 1), B⟩).B, A', C', G, H, ?_, rfl, ?_⟩
  · rw [outerIterate_eq] at hex; rw [outerIterate_eq]; exact hex
  · rw [outerIterate_eq]; exact hrep

end Agent109.Outer

#print axioms Agent109.Outer.outerNext_eq
#print axioms Agent109.Outer.stripSuffix_spec
#print axioms Agent109.Outer.succ_bounded
#print axioms Agent109.Outer.actual_step_outer
#print axioms Agent109.Outer.actual_outer_orbit
#print axioms Agent109.Outer.actual_cap2_exit
