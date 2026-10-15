import A120Base

/-!
# Agent #120: exact one-step dynamics of the neutral one-band template

For a base `b >= 2`, an exterior block `B`, a center block `C` and a gap `g`,
the template coefficient word (least significant first) is

  `tmpl b B C g = B ++ (b-1)^g ++ C ++ (b-1)^g ++ reverse B`.

Its value is the reverse-and-add image of any ordinary integer with that
pair word. If the two band carries differ (`e1 ≠ e2`), this file proves:

* the exact canonical digit word of the value (`digits_tmpl`);
* the exact next coefficient word, again a template with the explicit
  interfaces `nextB`, `nextC` and gap `g - gam` (`pairs_digits_tmpl`);
* the value is never a palindrome when `g ≥ 2` (`not_isPal_tmpl`);
* the ordinary base-`b` reverse-and-add step of the value is the value of the
  next template (`step_tmpl`).

No hypothesis on `C` (symmetry, parity) is needed for these statements.
-/

namespace Agent120.Neutral

/-- The neutral one-band template, right-associated. -/
def tmpl (b : Nat) (B C : List Nat) (g : Nat) : List Nat :=
  B ++ (List.replicate g (b - 1) ++ (C ++ (List.replicate g (b - 1) ++ B.reverse)))

/-- Carry leaving the exterior block (low end). -/
def e1 (b : Nat) (B : List Nat) : Nat := (norm b B 0).2
/-- Carry leaving the center block. -/
def e2 (b : Nat) (B C : List Nat) : Nat := (norm b C (e1 b B)).2
def DB (b : Nat) (B : List Nat) : List Nat := (norm b B 0).1
def DC (b : Nat) (B C : List Nat) : List Nat := (norm b C (e1 b B)).1
def DR (b : Nat) (B C : List Nat) : List Nat := (norm b B.reverse (e2 b B C)).1
/-- Final carry: `1` iff the reverse-and-add value gains a digit. -/
def gam (b : Nat) (B C : List Nat) : Nat := (norm b B.reverse (e2 b B C)).2
/-- Uniform digit of the lower band. -/
def xd (b : Nat) (B : List Nat) : Nat := (b - 1) * (1 - e1 b B)
/-- Uniform digit of the upper band. -/
def yd (b : Nat) (B C : List Nat) : Nat := (b - 1) * (1 - e2 b B C)

/-- Next exterior block (before moving neutral coefficients into the band). -/
def nextB (b : Nat) (B C : List Nat) : List Nat :=
  if gam b B C = 0 then List.zipWith (· + ·) (DB b B) (DR b B C).reverse
  else List.zipWith (· + ·) (DB b B ++ [xd b B]) (1 :: (DR b B C).reverse)

/-- Next center block (before moving neutral coefficients into the band). -/
def nextC (b : Nat) (B C : List Nat) : List Nat :=
  if gam b B C = 0 then List.zipWith (· + ·) (DC b B C) (DC b B C).reverse
  else List.zipWith (· + ·) (DC b B C ++ [yd b B C]) (yd b B C :: (DC b B C).reverse)

/-- Digit word of the template value, without a possible new leading digit. -/
def outWord (b : Nat) (B C : List Nat) (g : Nat) : List Nat :=
  DB b B ++ (List.replicate g (xd b B) ++
    (DC b B C ++ (List.replicate g (yd b B C) ++ DR b B C)))

/-- Hypotheses of the one-step theorem. -/
structure Hyp (b : Nat) (B C : List Nat) : Prop where
  base : 2 ≤ b
  boundB : ∀ v ∈ B, v ≤ 2 * (b - 1)
  boundC : ∀ v ∈ C, v ≤ 2 * (b - 1)
  ext : B.head? ≠ some 0
  flip : e1 b B ≠ e2 b B C

section
variable {b : Nat} {B C : List Nat}

theorem Hyp.e1_le (h : Hyp b B C) : e1 b B ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B 0 h.boundB (by omega)

theorem Hyp.e2_le (h : Hyp b B C) : e2 b B C ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) C _ h.boundC h.e1_le

theorem Hyp.gam_le (h : Hyp b B C) : gam b B C ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B.reverse _
    (fun v hv => h.boundB v (List.mem_reverse.mp hv)) h.e2_le

theorem Hyp.xy (h : Hyp b B C) : xd b B + yd b B C = b - 1 := by
  have h1 := h.e1_le; have h2 := h.e2_le; have hf := h.flip
  unfold xd yd
  rcases (by omega : e1 b B = 0 ∨ e1 b B = 1) with h1' | h1' <;>
  rcases (by omega : e2 b B C = 0 ∨ e2 b B C = 1) with h2' | h2' <;>
  simp_all

theorem Hyp.x_ne_y (h : Hyp b B C) : xd b B ≠ yd b B C := by
  have h1 := h.e1_le; have h2 := h.e2_le; have hf := h.flip; have hb := h.base
  unfold xd yd
  rcases (by omega : e1 b B = 0 ∨ e1 b B = 1) with h1' | h1' <;>
  rcases (by omega : e2 b B C = 0 ∨ e2 b B C = 1) with h2' | h2' <;>
  simp_all <;> omega

theorem Hyp.xd_lt (h : Hyp b B C) : xd b B < b := by
  have := h.base
  unfold xd
  rcases (by have := h.e1_le; omega : e1 b B = 0 ∨ e1 b B = 1) with h1 | h1 <;>
    simp [h1] <;> omega

theorem Hyp.yd_lt (h : Hyp b B C) : yd b B C < b := by
  have := h.base
  unfold yd
  rcases (by have := h.e2_le; omega : e2 b B C = 0 ∨ e2 b B C = 1) with h1 | h1 <;>
    simp [h1] <;> omega

theorem length_DB : (DB b B).length = B.length := norm_length b B 0
theorem length_DC : (DC b B C).length = C.length := norm_length b C _
theorem length_DR : (DR b B C).length = B.length := by
  unfold DR; rw [norm_length]; simp

/-- Exact normalization of the whole template. -/
theorem norm_tmpl (h : Hyp b B C) (g : Nat) :
    norm b (tmpl b B C g) 0 = (outWord b B C g, gam b B C) := by
  unfold tmpl outWord
  rw [norm_append, norm_append, norm_append, norm_append]
  have hb := h.base
  rw [show (norm b B 0).2 = e1 b B from rfl,
    norm_replicate_neutral b hb g (e1 b B) h.e1_le]
  simp only
  rw [show (norm b C (e1 b B)).2 = e2 b B C from rfl,
    norm_replicate_neutral b hb g (e2 b B C) h.e2_le]
  rfl

theorem length_tmpl (g : Nat) :
    (tmpl b B C g).length = 2 * B.length + 2 * g + C.length := by
  simp [tmpl]; omega

theorem length_outWord (g : Nat) :
    (outWord b B C g).length = 2 * B.length + 2 * g + C.length := by
  simp [outWord, length_DB, length_DC, length_DR]; omega

/-- Value of the template from its normalization. -/
theorem val_tmpl (h : Hyp b B C) (g : Nat) :
    val b (tmpl b B C g) =
      val b (outWord b B C g) + b ^ (outWord b B C g).length * gam b B C := by
  have hv := norm_val b (tmpl b B C g) 0
  rw [norm_tmpl h g] at hv
  simp only at hv
  rw [length_tmpl] at hv
  rw [length_outWord]
  omega

/-- Last digit of a normalization without a final carry is at least the last coefficient. -/
theorem norm_getLast?_ge (b : Nat) (hb : 0 < b) :
    ∀ (w : List Nat) (c a : Nat), w.getLast? = some a → (norm b w c).2 = 0 →
      ∃ d, (norm b w c).1.getLast? = some d ∧ a ≤ d
  | [], _, _, h, _ => by simp at h
  | [v], c, a, h, h0 => by
      simp only [List.getLast?_singleton, Option.some.injEq] at h
      rw [norm_cons] at h0 ⊢
      simp only [norm_nil] at h0 ⊢
      refine ⟨(v + c) % b, by simp, ?_⟩
      have hlt : v + c < b := by
        rcases Nat.lt_or_ge (v + c) b with hl | hl
        · exact hl
        · have : 1 ≤ (v + c) / b := (Nat.le_div_iff_mul_le hb).mpr (by omega)
          omega
      rw [Nat.mod_eq_of_lt hlt]; omega
  | v :: u :: w, c, a, h, h0 => by
      rw [getLast?_cons_of_ne_nil (by simp)] at h
      rw [norm_cons] at h0 ⊢
      simp only at h0 ⊢
      obtain ⟨d, hd, had⟩ := norm_getLast?_ge b hb (u :: w) _ a h h0
      refine ⟨d, ?_, had⟩
      have hne : (norm b (u :: w) ((v + c) / b)).1 ≠ [] := by
        intro he
        have := congrArg List.length he
        rw [norm_length] at this; simp at this
      rw [getLast?_cons_of_ne_nil hne, hd]

theorem digits_outWord_lt (h : Hyp b B C) (g : Nat) :
    ∀ d ∈ outWord b B C g, d < b := by
  have hb : 0 < b := by have := h.base; omega
  intro d hd
  simp only [outWord, List.mem_append, List.mem_replicate] at hd
  rcases hd with hd | ⟨_, rfl⟩ | hd | ⟨_, rfl⟩ | hd
  · exact norm_digit_lt b hb B 0 d hd
  · exact h.xd_lt
  · exact norm_digit_lt b hb C _ d hd
  · exact h.yd_lt
  · exact norm_digit_lt b hb B.reverse _ d hd

/-- Exact canonical digits of the template value. -/
theorem digits_tmpl (h : Hyp b B C) (g : Nat) (hg : 1 ≤ g) :
    digits b (val b (tmpl b B C g)) =
      if gam b B C = 0 then outWord b B C g else outWord b B C g ++ [1] := by
  have hb := h.base
  have hlt := digits_outWord_lt h g
  rw [val_tmpl h g]
  rcases (by have := h.gam_le; omega : gam b B C = 0 ∨ gam b B C = 1) with h0 | h1
  · simp only [h0, Nat.mul_zero, Nat.add_zero, if_true]
    apply digits_val b hb
    refine ⟨hlt, ?_⟩
    -- the most significant digit is positive
    by_cases hB : B = []
    · subst hB
      have he2 : e2 b [] C = 0 := by
        have : gam b [] C = e2 b [] C := by simp [gam]
        omega
      obtain ⟨g', rfl⟩ : ∃ g', g = g' + 1 := ⟨g - 1, by omega⟩
      simp only [outWord, DR, List.reverse_nil, norm_nil, List.append_nil, List.getLast?_append,
        List.getLast?_replicate, Nat.add_one_ne_zero, if_false, Option.some_or]
      simp [yd, he2]
      omega
    · obtain ⟨a, ha⟩ : ∃ a, B.head? = some a := by
        cases B with
        | nil => exact absurd rfl hB
        | cons x xs => exact ⟨x, rfl⟩
      have ha0 : a ≠ 0 := by intro h'; subst h'; exact h.ext ha
      have hra : B.reverse.getLast? = some a := by rw [List.getLast?_reverse]; exact ha
      obtain ⟨d, hd, had⟩ := norm_getLast?_ge b (by omega) B.reverse (e2 b B C) a hra h0
      have hDR : (DR b B C).getLast? = some d := hd
      simp only [outWord, List.getLast?_append, hDR, Option.some_or]
      intro hd0
      simp only [Option.some.injEq] at hd0
      omega
  · simp only [h1, Nat.mul_one, Nat.one_ne_zero, if_false]
    have hv : val b (outWord b B C g ++ [1]) =
        val b (outWord b B C g) + b ^ (outWord b B C g).length := by
      rw [val_append]; simp
    rw [← hv]
    apply digits_val b hb
    refine ⟨?_, by simp⟩
    intro d hd
    simp only [List.mem_append, List.mem_singleton] at hd
    rcases hd with hd | rfl
    · exact hlt d hd
    · omega

/-- Block-reflection identity for `zipWith (· + ·)` on equal-length lists. -/
theorem zipWith_add_reverse_swap (u w : List Nat) (hl : u.length = w.length) :
    List.zipWith (· + ·) w.reverse u.reverse = (List.zipWith (· + ·) u w).reverse := by
  rw [List.reverse_zipWith hl, List.zipWith_comm]
  congr 1
  funext a c
  omega

/-- The next coefficient word is again a template (no overflow case). -/
theorem pairs_outWord_noOverflow (h : Hyp b B C) (g : Nat) (h0 : gam b B C = 0) :
    pairs (outWord b B C g) = tmpl b (nextB b B C) (nextC b B C) g := by
  unfold pairs outWord tmpl nextB nextC
  simp only [h0, if_true]
  simp only [List.reverse_append, List.reverse_replicate, List.append_assoc]
  have l1 : (DB b B).length = (DR b B C).reverse.length := by
    simp [length_DB, length_DR]
  have l2 : (List.replicate g (xd b B)).length = (List.replicate g (yd b B C)).length := by simp
  have l3 : (DC b B C).length = (DC b B C).reverse.length := by simp
  have l4 : (List.replicate g (yd b B C)).length = (List.replicate g (xd b B)).length := by simp
  rw [List.zipWith_append l1, List.zipWith_append l2, List.zipWith_append l3,
    List.zipWith_append l4]
  rw [List.zipWith_replicate, List.zipWith_replicate, Nat.min_self, h.xy,
    Nat.add_comm (yd b B C), h.xy]
  congr 4
  have := zipWith_add_reverse_swap (DB b B) (DR b B C).reverse (by rw [l1])
  rw [List.reverse_reverse] at this
  exact this

/-- The next coefficient word is again a template (overflow case). -/
theorem pairs_outWord_overflow (h : Hyp b B C) (g : Nat) (hg : 1 ≤ g)
    (h1 : gam b B C = 1) :
    pairs (outWord b B C g ++ [1]) = tmpl b (nextB b B C) (nextC b B C) (g - 1) := by
  obtain ⟨g', rfl⟩ : ∃ g', g = g' + 1 := ⟨g - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  have hreg : outWord b B C (g' + 1) ++ [1] =
      (DB b B ++ [xd b B]) ++ (List.replicate g' (xd b B) ++
        ((DC b B C ++ [yd b B C]) ++ (List.replicate g' (yd b B C) ++ (DR b B C ++ [1])))) := by
    simp [outWord, List.replicate_succ, List.append_assoc]
  unfold pairs
  rw [hreg]
  have hrev : ((DB b B ++ [xd b B]) ++ (List.replicate g' (xd b B) ++
        ((DC b B C ++ [yd b B C]) ++ (List.replicate g' (yd b B C) ++ (DR b B C ++ [1]))))).reverse =
      (1 :: (DR b B C).reverse) ++ (List.replicate g' (yd b B C) ++
        ((yd b B C :: (DC b B C).reverse) ++ (List.replicate g' (xd b B) ++
          (xd b B :: (DB b B).reverse)))) := by
    simp [List.reverse_append, List.append_assoc]
  rw [hrev]
  have l1 : (DB b B ++ [xd b B]).length = (1 :: (DR b B C).reverse).length := by
    simp [length_DB, length_DR]
  have l2 : (List.replicate g' (xd b B)).length = (List.replicate g' (yd b B C)).length := by simp
  have l3 : (DC b B C ++ [yd b B C]).length = (yd b B C :: (DC b B C).reverse).length := by simp
  have l4 : (List.replicate g' (yd b B C)).length = (List.replicate g' (xd b B)).length := by simp
  rw [List.zipWith_append l1, List.zipWith_append l2, List.zipWith_append l3,
    List.zipWith_append l4]
  rw [List.zipWith_replicate, List.zipWith_replicate, Nat.min_self, h.xy,
    Nat.add_comm (yd b B C), h.xy]
  unfold tmpl nextB nextC
  simp only [h1, Nat.one_ne_zero, if_false]
  congr 4
  have hsw := zipWith_add_reverse_swap (DB b B ++ [xd b B]) (1 :: (DR b B C).reverse) l1
  rw [List.reverse_cons, List.reverse_reverse, List.reverse_append] at hsw
  simpa using hsw

/-- The next coefficient word, from the canonical digits of the template value. -/
theorem pairs_digits_tmpl (h : Hyp b B C) (g : Nat) (hg : 1 ≤ g) :
    pairs (digits b (val b (tmpl b B C g))) =
      tmpl b (nextB b B C) (nextC b B C) (g - gam b B C) := by
  rw [digits_tmpl h g hg]
  rcases (by have := h.gam_le; omega : gam b B C = 0 ∨ gam b B C = 1) with h0 | h1
  · simp only [h0, if_true, Nat.sub_zero]
    exact pairs_outWord_noOverflow h g h0
  · simp only [h1, Nat.one_ne_zero, if_false]
    exact pairs_outWord_overflow h g hg h1

/-- One ordinary base-`b` reverse-and-add step maps the template value to the next one. -/
theorem step_tmpl (h : Hyp b B C) (g : Nat) (hg : 1 ≤ g) :
    step b (val b (tmpl b B C g)) =
      val b (tmpl b (nextB b B C) (nextC b B C) (g - gam b B C)) := by
  rw [step_eq_val_pairs b h.base, pairs_digits_tmpl h g hg]

/-- With gap at least two, the template value is not a base-`b` palindrome. -/
theorem not_isPal_tmpl (h : Hyp b B C) (g : Nat) (hg : 2 ≤ g) :
    ¬ IsPal b (val b (tmpl b B C g)) := by
  unfold IsPal
  rw [digits_tmpl h g (by omega)]
  have hxy := h.x_ne_y
  obtain ⟨g', rfl⟩ : ∃ g', g = g' + 2 := ⟨g - 2, by omega⟩
  rcases (by have := h.gam_le; omega : gam b B C = 0 ∨ gam b B C = 1) with h0 | h1
  · simp only [h0, if_true]
    intro hpal
    have hr : (outWord b B C (g' + 2)).reverse =
        (DR b B C).reverse ++ (List.replicate (g' + 2) (yd b B C) ++
          ((DC b B C).reverse ++ (List.replicate (g' + 2) (xd b B) ++ (DB b B).reverse))) := by
      simp [outWord, List.reverse_append, List.append_assoc]
    have hw : outWord b B C (g' + 2) =
        DB b B ++ (List.replicate (g' + 2) (xd b B) ++
          (DC b B C ++ (List.replicate (g' + 2) (yd b B C) ++ DR b B C))) := rfl
    rw [hr, hw] at hpal
    have hl : (DB b B).length = (DR b B C).reverse.length := by simp [length_DB, length_DR]
    have ht := congrArg List.head? (List.append_inj hpal hl).2
    simp [List.replicate_succ] at ht
    exact hxy ht
  · simp only [h1, Nat.one_ne_zero, if_false]
    intro hpal
    have hw : outWord b B C (g' + 2) ++ [1] =
        (DB b B ++ [xd b B]) ++ (List.replicate (g' + 1) (xd b B) ++
          (DC b B C ++ (List.replicate (g' + 2) (yd b B C) ++ (DR b B C ++ [1])))) := by
      simp [outWord, List.replicate_succ, List.append_assoc]
    have hr : (outWord b B C (g' + 2) ++ [1]).reverse =
        (1 :: (DR b B C).reverse) ++ (List.replicate (g' + 2) (yd b B C) ++
          ((DC b B C).reverse ++ (List.replicate (g' + 2) (xd b B) ++ (DB b B).reverse))) := by
      simp [outWord, List.reverse_append, List.append_assoc]
    rw [hr, hw] at hpal
    have hl : (DB b B ++ [xd b B]).length = (1 :: (DR b B C).reverse).length := by
      simp [length_DB, length_DR]
    have ht := congrArg List.head? (List.append_inj hpal hl).2
    simp [List.replicate_succ] at ht
    exact hxy ht

end

end Agent120.Neutral

#print axioms Agent120.Neutral.digits_tmpl
#print axioms Agent120.Neutral.pairs_digits_tmpl
#print axioms Agent120.Neutral.step_tmpl
#print axioms Agent120.Neutral.not_isPal_tmpl
