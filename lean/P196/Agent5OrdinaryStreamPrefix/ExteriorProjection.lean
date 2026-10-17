import P196.Agent5OrdinaryStreamPrefix.ExteriorBridge

namespace P196.Agent6

def lowEnd (B : Word) (c : Nat) : Word :=
  (norm B 0).1 ++ [c + (norm B 0).2 - 10 * carryPhase c]

def highEnd (B : Word) (c : Nat) : Word :=
  digitPhase c :: (norm B.reverse (carryPhase c)).1

def carryEnd (e : Nat) : Word := if e == 0 then [] else [e]

def paired (D : Word) : Word := List.zipWith Nat.add D D.reverse

/-- Whole-word carrying exposes both exterior ends, whatever the middle. -/
theorem surrounded_digit_ends (B W : Word) (c g : Nat)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W) :
    ∃ M, normalizedDigits (surrounded B c g W) =
      lowEnd B c ++ M ++ highEnd B c ++
      carryEnd (norm B.reverse (carryPhase c)).2 := by
  refine ⟨List.replicate (g+1) (digitPhase c) ++ (norm W (carryPhase c)).1 ++
    [c+(norm W (carryPhase c)).2-10*carryPhase c] ++
    List.replicate g (digitPhase c), ?_⟩
  simp only [normalizedDigits, surrounded_normalization B W c g hc hB hW]
  simp only [lowEnd,highEnd,carryEnd,List.replicate_succ',List.append_assoc]
  rfl

theorem take_complete_prefix (a b : Word) : (a ++ b).take a.length = a := by
  rw [List.take_append_of_le_length (Nat.le_refl _)]
  exact List.take_length

/-- Prefix of a mirrored sum is computed from the two corresponding digit ends. -/
theorem paired_ends (L M R : Word) (t e : Nat) (he : e ≤ 1)
    (hlen : L.length = R.length+1) :
    (paired (L ++ M ++ (t :: R) ++ carryEnd e)).take (R.length+1) =
      List.zipWith Nat.add L
        (if e == 0 then R.reverse ++ [t] else 1 :: R.reverse) := by
  have hlo : (L ++ M ++ (t :: R) ++ carryEnd e).take (R.length+1) = L := by
    rw [← hlen]
    simpa only [List.append_assoc] using
      take_complete_prefix L (M ++ (t :: R) ++ carryEnd e)
  have hhi : (L ++ M ++ (t :: R) ++ carryEnd e).reverse.take (R.length+1) =
      (if e == 0 then R.reverse ++ [t] else 1 :: R.reverse) := by
    have hcases : e = 0 ∨ e = 1 := by omega
    rcases hcases with rfl | rfl
    · simp only [carryEnd,beq_self_eq_true,if_true,List.append_nil,
        List.reverse_append,List.reverse_cons]
      have h := take_complete_prefix (R.reverse ++ [t]) (M.reverse ++ L.reverse)
      simpa only [List.length_append,List.length_reverse,List.length_cons,
        List.length_nil,Nat.zero_add,List.append_assoc] using h
    · simp only [carryEnd,show (1 == 0) = false by decide,if_false,
        List.reverse_append,List.reverse_cons,List.reverse_nil,List.nil_append]
      have h := take_complete_prefix (1 :: R.reverse) (t :: (M.reverse ++ L.reverse))
      simpa only [List.length_cons,List.length_reverse,List.cons_append,
        List.append_assoc,List.singleton_append] using h
  simp only [paired,List.take_zipWith,hlo,hhi]

/-- The precise raw exterior coefficients obtained from actual whole-word carrying. -/
theorem surrounded_raw_exterior (B W : Word) (c g : Nat)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W) :
    (paired (normalizedDigits (surrounded B c g W))).take (B.length+1) =
      List.zipWith Nat.add (lowEnd B c)
        (if (norm B.reverse (carryPhase c)).2 == 0
         then (norm B.reverse (carryPhase c)).1.reverse ++ [digitPhase c]
         else 1 :: (norm B.reverse (carryPhase c)).1.reverse) := by
  obtain ⟨M,hm⟩ := surrounded_digit_ends B W c g hc hB hW
  have hBr : Coefficients B.reverse := by
    intro x hx
    exact hB x (by simpa using hx)
  have he := norm_carry_bit B.reverse (carryPhase c) hBr (carryPhase_bit c)
  have hlen : (lowEnd B c).length = (norm B.reverse (carryPhase c)).1.length + 1 := by
    simp [lowEnd,norm_length]
  rw [hm]
  simpa only [highEnd,norm_length,List.length_reverse] using
    paired_ends (lowEnd B c) M (norm B.reverse (carryPhase c)).1
      (digitPhase c) (norm B.reverse (carryPhase c)).2 he hlen

/-- Formal semiconjugacy at the exterior, with arbitrary middle and all gaps >=2.
This is an identity of continuously normalized digit words. -/
theorem actual_exterior_projection (B W : Word) (c g : Nat)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W) :
    trim (2*digitPhase c)
      ((paired (normalizedDigits (surrounded B c g W))).take (B.length+1)) =
      (advance ⟨c,B⟩).word := by
  rw [surrounded_raw_exterior B W c g hc hB hW]
  rfl

#print axioms surrounded_digit_ends
#print axioms take_complete_prefix
#print axioms paired_ends
#print axioms surrounded_raw_exterior
#print axioms actual_exterior_projection
end P196.Agent6
