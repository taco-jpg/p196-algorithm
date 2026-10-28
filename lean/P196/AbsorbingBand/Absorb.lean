import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Absorbing-band templates (merged symmetric lattice format, uniform band)

For a base `b ≥ 2`, a block `B`, a band value `c` (a pair-sum coefficient, `c ≤ 2(b-1)`,
`c ≠ b-1`) and a band length `l`, the template coefficient word (least significant first) is

  `ltmpl B c l = B ++ c^l ++ reverse B`.

The band is *absorbing*: for every incoming carry `e ≤ 1`, the run `c^(m+1)` emits the carry
`kc b c = [b ≤ c]` (independent of `e`), first digit `(c+e) % b` and then `m` copies of
`ya b c = (c + kc b c) % b`.  This file proves the exact normalization of the whole template and
the exact canonical digit word of its value.  Nothing here is specific to a base or to 196.
-/

namespace AbsorbingBand

open Agent120.Neutral

/-- Constant carry leaving an absorbing run. -/
def kc (b c : Nat) : Nat := if b ≤ c then 1 else 0

/-- Uniform digit of an absorbing run after its first position. -/
def ya (b c : Nat) : Nat := (c + kc b c) % b

theorem kc_le_one (b c : Nat) : kc b c ≤ 1 := by
  unfold kc; split <;> omega

theorem div_absorb {b c e : Nat} (hb : 2 ≤ b) (hc : c ≤ 2 * (b - 1)) (hne : c ≠ b - 1)
    (he : e ≤ 1) : (c + e) / b = kc b c := by
  unfold kc
  split
  · rename_i h
    exact Nat.div_eq_of_lt_le (by omega) (by omega)
  · rename_i h
    exact Nat.div_eq_of_lt (by omega)

/-- With the constant carry as carry-in, the run reproduces itself digitwise. -/
theorem norm_replicate_fix {b c : Nat} (hb : 2 ≤ b) (hc : c ≤ 2 * (b - 1)) (hne : c ≠ b - 1) :
    ∀ m : Nat, norm b (List.replicate m c) (kc b c) = (List.replicate m (ya b c), kc b c)
  | 0 => rfl
  | m + 1 => by
      rw [List.replicate_succ, norm_cons, div_absorb hb hc hne (kc_le_one b c),
        norm_replicate_fix hb hc hne m, List.replicate_succ] <;> rfl

/-- An absorbing run swallows its incoming carry. -/
theorem norm_replicate_absorb {b c : Nat} (hb : 2 ≤ b) (hc : c ≤ 2 * (b - 1))
    (hne : c ≠ b - 1) {e : Nat} (he : e ≤ 1) (m : Nat) :
    norm b (List.replicate (m + 1) c) e =
      ((c + e) % b :: List.replicate m (ya b c), kc b c) := by
  rw [List.replicate_succ, norm_cons, div_absorb hb hc hne he, norm_replicate_fix hb hc hne m] <;> rfl

/-- The absorbing template. -/
def ltmpl (B : List Nat) (c l : Nat) : List Nat := B ++ (List.replicate l c ++ B.reverse)

/-- First band digit (it still sees the carry leaving `B`). -/
def xa (b : Nat) (B : List Nat) (c : Nat) : Nat := (c + e1 b B) % b
/-- Normalized upper copy of `B`, entered with the constant carry of the band. -/
def DRa (b : Nat) (B : List Nat) (c : Nat) : List Nat := (norm b B.reverse (kc b c)).1
/-- Final carry: `1` iff the value gains a digit. -/
def gama (b : Nat) (B : List Nat) (c : Nat) : Nat := (norm b B.reverse (kc b c)).2

/-- Digit word of the template value (band length `m + 1`), without a possible new top digit. -/
def outW (b : Nat) (B : List Nat) (c m : Nat) : List Nat :=
  DB b B ++ ([xa b B c] ++ (List.replicate m (ya b c) ++ DRa b B c))

/-- Hypotheses of the one-step theorem. -/
structure LHyp (b : Nat) (B : List Nat) (c : Nat) : Prop where
  base : 2 ≤ b
  boundB : ∀ v ∈ B, v ≤ 2 * (b - 1)
  boundc : c ≤ 2 * (b - 1)
  cne : c ≠ b - 1
  ne : B ≠ []
  ext : B.head? ≠ some 0

section
variable {b : Nat} {B : List Nat} {c : Nat}

theorem LHyp.e1_le (h : LHyp b B c) : e1 b B ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B 0 h.boundB (by omega)

theorem LHyp.gam_le (h : LHyp b B c) : gama b B c ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B.reverse _
    (fun v hv => h.boundB v (List.mem_reverse.mp hv)) (kc_le_one b c)

theorem LHyp.xa_lt (h : LHyp b B c) : xa b B c < b :=
  Nat.mod_lt _ (by have := h.base; omega)

theorem ya_lt (hb : 2 ≤ b) : ya b c < b := Nat.mod_lt _ (by omega)

theorem length_DRa : (DRa b B c).length = B.length := by
  unfold DRa; rw [norm_length]; simp

theorem length_ltmpl (l : Nat) : (ltmpl B c l).length = 2 * B.length + l := by
  simp [ltmpl] <;> omega

theorem length_outW (m : Nat) : (outW b B c m).length = 2 * B.length + (m + 1) := by
  simp [outW, length_DB, length_DRa] <;> omega

/-- Exact normalization of the whole template. -/
theorem norm_ltmpl (h : LHyp b B c) (m : Nat) :
    norm b (ltmpl B c (m + 1)) 0 = (outW b B c m, gama b B c) := by
  unfold ltmpl outW
  rw [norm_append, norm_append]
  rw [show (norm b B 0).2 = e1 b B from rfl,
    norm_replicate_absorb h.base h.boundc h.cne h.e1_le m]
  rfl

/-- Value of the template from its normalization. -/
theorem val_ltmpl (h : LHyp b B c) (m : Nat) :
    val b (ltmpl B c (m + 1)) =
      val b (outW b B c m) + b ^ (outW b B c m).length * gama b B c := by
  have hv := norm_val b (ltmpl B c (m + 1)) 0
  rw [norm_ltmpl h m] at hv
  simp only at hv
  rw [length_ltmpl] at hv
  rw [length_outW]
  omega

theorem digits_outW_lt (h : LHyp b B c) (m : Nat) : ∀ d ∈ outW b B c m, d < b := by
  have hb : 0 < b := by have := h.base; omega
  intro d hd
  simp only [outW, List.mem_append, List.mem_singleton, List.mem_replicate] at hd
  rcases hd with hd | rfl | ⟨_, rfl⟩ | hd
  · exact norm_digit_lt b hb B 0 d hd
  · exact h.xa_lt
  · exact ya_lt h.base
  · exact norm_digit_lt b hb B.reverse _ d hd

theorem exists_head (hne : B ≠ []) : ∃ a, B.head? = some a := by
  cases B with
  | nil => exact absurd rfl hne
  | cons x xs => exact ⟨x, rfl⟩

/-- Exact canonical digits of the template value (band length `m + 1`). -/
theorem digits_ltmpl (h : LHyp b B c) (m : Nat) :
    digits b (val b (ltmpl B c (m + 1))) =
      if gama b B c = 0 then outW b B c m else outW b B c m ++ [1] := by
  have hb := h.base
  have hlt := digits_outW_lt h m
  rw [val_ltmpl h m]
  rcases (by have := h.gam_le; omega : gama b B c = 0 ∨ gama b B c = 1) with h0 | h1
  · simp only [h0, Nat.mul_zero, Nat.add_zero, if_true]
    apply digits_val b hb
    refine ⟨hlt, ?_⟩
    obtain ⟨a, ha⟩ := exists_head h.ne
    have ha0 : a ≠ 0 := by intro h'; subst h'; exact h.ext ha
    have hra : B.reverse.getLast? = some a := by rw [List.getLast?_reverse]; exact ha
    obtain ⟨d, hd, had⟩ := norm_getLast?_ge b (by omega) B.reverse (kc b c) a hra h0
    have hDR : (DRa b B c).getLast? = some d := hd
    simp only [outW, List.getLast?_append, hDR, Option.some_or]
    intro hd0
    simp only [Option.some.injEq] at hd0
    omega
  · simp only [h1, Nat.mul_one, Nat.one_ne_zero, if_false]
    have hv : val b (outW b B c m ++ [1]) =
        val b (outW b B c m) + b ^ (outW b B c m).length := by
      rw [val_append]; simp
    rw [← hv]
    apply digits_val b hb
    refine ⟨?_, by simp⟩
    intro d hd
    simp only [List.mem_append, List.mem_singleton] at hd
    rcases hd with hd | rfl
    · exact hlt d hd
    · omega

end

end AbsorbingBand

#print axioms AbsorbingBand.norm_replicate_absorb
#print axioms AbsorbingBand.norm_ltmpl
#print axioms AbsorbingBand.digits_ltmpl
