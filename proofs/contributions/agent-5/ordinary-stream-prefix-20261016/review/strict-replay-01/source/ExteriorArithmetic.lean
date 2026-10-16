import ExteriorProjection

namespace P196.Agent6

def numeral : Word → Nat
  | [] => 0
  | x :: xs => x + 10 * numeral xs

def DecimalDigits (w : Word) : Prop := ∀ x ∈ w, x < 10

def PositiveLast (w : Word) : Prop :=
  ∃ front last, w = front ++ [last] ∧ 0 < last

theorem numeral_append (a b : Word) :
    numeral (a ++ b) = numeral a + 10^a.length * numeral b := by
  induction a with
  | nil => simp [numeral]
  | cons x xs ih =>
      simp only [List.cons_append,numeral,ih,List.length_cons,Nat.pow_succ]
      simp only [Nat.mul_add]
      have hm : (10 ^ xs.length * 10) * numeral b =
          10 * (10 ^ xs.length * numeral b) := by ac_rfl
      rw [hm]
      omega

theorem norm_value (w : Word) (e : Nat) :
    numeral (norm w e).1 + 10^w.length * (norm w e).2 = numeral w + e := by
  induction w generalizing e with
  | nil => simp [norm,numeral]
  | cons x xs ih =>
      have ht := ih ((x+e)/10)
      have hd := Nat.mod_add_div (x+e) 10
      simp only [norm,numeral,List.length_cons,Nat.pow_succ]
      have hre : (10^xs.length * 10) * (norm xs ((x+e)/10)).2 =
          10 * (10^xs.length * (norm xs ((x+e)/10)).2) := by
        ac_rfl
      rw [hre]
      omega

theorem normalized_value (q : Word) : numeral (normalizedDigits q) = numeral q := by
  have h := norm_value q 0
  unfold normalizedDigits
  rw [numeral_append]
  simp only [norm_length]
  split
  next he =>
    have heq : (norm q 0).2 = 0 := by simpa using he
    simp only [numeral,Nat.mul_zero,Nat.add_zero]
    simpa [heq] using h
  next he =>
    simp only [numeral,Nat.mul_zero,Nat.add_zero]
    omega

theorem norm_digit_bounds (q : Word) (e : Nat) : DecimalDigits (norm q e).1 := by
  induction q generalizing e with
  | nil => intro x hx; simp [norm] at hx
  | cons x xs ih =>
      intro d hd
      simp only [norm,List.mem_cons] at hd
      rcases hd with rfl | htail
      · exact Nat.mod_lt _ (by decide)
      · exact ih ((x+e)/10) d htail

theorem normalized_digit_bounds (q : Word) (hq : Coefficients q) :
    DecimalDigits (normalizedDigits q) := by
  have hc := norm_carry_bit q 0 hq (by omega)
  have hd := norm_digit_bounds q 0
  intro d hm
  simp only [normalizedDigits,List.mem_append] at hm
  rcases hm with hm | hm
  · exact hd d hm
  · split at hm
    next he => simp at hm
    next he =>
      have heq : d = (norm q 0).2 := by simpa using hm
      omega

theorem normalized_positive_last (q : Word) (hq : Coefficients q)
    (hp : PositiveLast q) : PositiveLast (normalizedDigits q) := by
  obtain ⟨pre,x,rfl,hx⟩ := hp
  have hpre : Coefficients pre := by
    intro d hd
    exact hq d (by simp [hd])
  have hxmax := hq x (by simp)
  have he := norm_carry_bit pre 0 hpre (by omega)
  have hsmall : (x+(norm pre 0).2)/10 ≤ 1 := by omega
  by_cases hzero : (x+(norm pre 0).2)/10 = 0
  · have hmod : 0 < (x+(norm pre 0).2)%10 := by omega
    refine ⟨(norm pre 0).1,(x+(norm pre 0).2)%10,?_,hmod⟩
    simp [normalizedDigits,norm_append,norm,hzero]
  · have hone : (x+(norm pre 0).2)/10 = 1 := by omega
    refine ⟨(norm pre 0).1 ++ [(x+(norm pre 0).2)%10],1,?_,by omega⟩
    simp [normalizedDigits,norm_append,norm,hone,List.append_assoc]

theorem numeral_zip_add (a b : Word) (hlen : a.length = b.length) :
    numeral (List.zipWith Nat.add a b) = numeral a + numeral b := by
  induction a generalizing b with
  | nil =>
      have hb : b = [] := List.length_eq_zero_iff.mp (by simpa using hlen.symm)
      subst b
      rfl
  | cons x xs ih =>
      cases b with
      | nil => simp at hlen
      | cons y ys =>
          have htail : xs.length = ys.length := by simpa using hlen
          change (x+y) + 10 * numeral (List.zipWith Nat.add xs ys) =
            (x+10*numeral xs) + (y+10*numeral ys)
          rw [ih ys htail,Nat.mul_add]
          omega

theorem paired_value (D : Word) : numeral (paired D) = numeral D + numeral D.reverse :=
  numeral_zip_add D D.reverse (by simp)

theorem paired_symmetric (D : Word) : (paired D).reverse = paired D := by
  unfold paired
  rw [List.reverse_zipWith (by simp),List.reverse_reverse,List.zipWith_comm]
  congr 1
  funext a b
  exact Nat.add_comm b a

theorem paired_coefficients (D : Word) (hD : DecimalDigits D) : Coefficients (paired D) := by
  have helper : ∀ a b : Word, DecimalDigits a → DecimalDigits b →
      Coefficients (List.zipWith Nat.add a b) := by
    intro a
    induction a with
    | nil => intro b ha hb x hx; simp at hx
    | cons x xs ih =>
        intro b ha hb
        cases b with
        | nil => intro x hx; simp at hx
        | cons y ys =>
            have hx := ha x (by simp)
            have hy := hb y (by simp)
            have ht := ih ys (by intro d hd; exact ha d (by simp [hd]))
              (by intro d hd; exact hb d (by simp [hd]))
            intro d hd
            simp only [List.zipWith_cons_cons,List.mem_cons] at hd
            rcases hd with rfl | hd
            · change x+y ≤ 18
              omega
            · exact ht d hd
  exact helper D D.reverse hD (by intro d hd; exact hD d (by simpa using hd))

theorem paired_positive_last (D : Word) (hp : PositiveLast D) : PositiveLast (paired D) := by
  obtain ⟨pre,last,hD,hpos⟩ := hp
  have hne : D ≠ [] := by
    intro he
    have hm : last ∈ D := by rw [hD]; simp
    simp [he] at hm
  obtain ⟨a,tail,ha⟩ := List.exists_cons_of_ne_nil hne
  have hr : D.reverse = last :: pre.reverse := by simp [hD]
  let rest := List.zipWith Nat.add tail pre.reverse
  have hpair : paired D = (a+last) :: rest := by
    unfold paired
    rw [hr,ha]
    rfl
  refine ⟨rest.reverse,a+last,?_,by omega⟩
  calc
    paired D = (paired D).reverse := (paired_symmetric D).symm
    _ = rest.reverse ++ [a+last] := by rw [hpair,List.reverse_cons]

/-- Canonical digit realization of the ordinary reverse-and-add output. -/
def reverseAddDigits (D : Word) : Word := normalizedDigits (paired D)

theorem reverseAddDigits_correct (D : Word) (hD : DecimalDigits D)
    (hp : PositiveLast D) :
    DecimalDigits (reverseAddDigits D) ∧ PositiveLast (reverseAddDigits D) ∧
    numeral (reverseAddDigits D) = numeral D + numeral D.reverse := by
  have hq := paired_coefficients D hD
  exact ⟨normalized_digit_bounds (paired D) hq,
    normalized_positive_last (paired D) hq (paired_positive_last D hp),
    (normalized_value (paired D)).trans (paired_value D)⟩

/-- Ordinary reverse-and-add and the complementary-band exterior factor agree.
All source digit, coefficient, and band hypotheses are explicit. -/
theorem ordinary_reverse_add_exterior (D B W : Word) (c g : Nat)
    (hD : DecimalDigits D) (hp : PositiveLast D)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c g W) :
    DecimalDigits (reverseAddDigits D) ∧ PositiveLast (reverseAddDigits D) ∧
    numeral (reverseAddDigits D) = numeral D + numeral D.reverse ∧
    trim (2*digitPhase c) ((paired (reverseAddDigits D)).take (B.length+1)) =
      (advance ⟨c,B⟩).word := by
  obtain ⟨hd,hpos,hval⟩ := reverseAddDigits_correct D hD hp
  refine ⟨hd,hpos,hval,?_⟩
  unfold reverseAddDigits
  rw [hshape]
  exact actual_exterior_projection B W c g hc hB hW

#print axioms numeral_append
#print axioms norm_value
#print axioms normalized_value
#print axioms norm_digit_bounds
#print axioms normalized_digit_bounds
#print axioms normalized_positive_last
#print axioms numeral_zip_add
#print axioms paired_value
#print axioms paired_symmetric
#print axioms paired_coefficients
#print axioms paired_positive_last
#print axioms reverseAddDigits_correct
#print axioms ordinary_reverse_add_exterior
end P196.Agent6
