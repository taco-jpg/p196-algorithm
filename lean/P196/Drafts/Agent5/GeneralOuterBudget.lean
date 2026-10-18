import P196.Agent5EvenBaseAbsorption.GeneralCarryMass

namespace P196.Agent5.General.Outer

def overflow (b p e : Nat) : Nat := (p + e) / b

def next (b p e : Nat) : Nat :=
  if p + e < b then 2 * p + e else p % b + 1

def potential (b p : Nat) : Nat :=
  if p = b then (b - 1).log2 - 1 else p.log2

theorem log_mono (a b : Nat) (ha : 0 < a) (hab : a ≤ b) : a.log2 ≤ b.log2 := by
  have hx := Nat.log2_self_le (n := a) (by omega)
  exact (Nat.le_log2 (by omega : b ≠ 0)).2 (by omega)

theorem log_double_upper (p e : Nat) (hp : 0 < p) (he : e ≤ 1) :
    (2 * p + e).log2 ≤ p.log2 + 1 := by
  have h := Nat.lt_log2_self (n := p)
  have hx : 2 * p + e < 2 ^ (p.log2 + 1 + 1) := by
    rw [Nat.pow_succ]
    omega
  have hl := (Nat.log2_lt (by omega : 2 * p + e ≠ 0)).2 hx
  omega

theorem log_double_lower (a b : Nat) (ha : 0 < a) (hab : 2 * a ≤ b) :
    a.log2 + 1 ≤ b.log2 := by
  apply (Nat.le_log2 (by omega)).2
  rw [Nat.pow_succ]
  have hx := Nat.log2_self_le (n := a) (by omega)
  omega

theorem potential_le_log (b p : Nat) (hb : 2 ≤ b) : potential b p ≤ p.log2 := by
  unfold potential
  split
  next h =>
    subst p
    have hmono := log_mono (b-1) b (by omega) (by omega)
    omega
  next h => exact Nat.le_refl _

theorem logarithmic_outer_budget (b p e : Nat) (hb : 5 ≤ b)
    (hp : 0 < p ∧ p ≤ 2*b-2) (he : e ≤ 1) :
    2 * overflow b p e + potential b (next b p e) ≤ 1 + potential b p := by
  by_cases hno : p+e < b
  · have hf : overflow b p e = 0 := Nat.div_eq_of_lt hno
    have hn : next b p e = 2*p+e := if_pos hno
    have hs : potential b p = p.log2 := if_neg (by omega)
    rw [hf, hn, hs]
    have hl := potential_le_log b (2*p+e) (by omega)
    have hu := log_double_upper p e hp.1 he
    omega
  · have hf : overflow b p e = 1 := by
      apply Nat.div_eq_of_lt_le <;> omega
    have hn : next b p e = p%b+1 := if_neg hno
    rw [hf, hn]
    have hlog : 2 ≤ (b-1).log2 := by
      apply (Nat.le_log2 (by omega)).2
      change 4 ≤ b-1
      omega
    by_cases hlt : p < b
    · have hpb : p = b-1 := by omega
      subst p
      have hmod : (b-1)%b = b-1 := Nat.mod_eq_of_lt (by omega)
      rw [hmod]
      have heq : b-1+1=b := by omega
      rw [heq]
      simp only [potential, if_pos rfl, if_true, if_neg (by omega : b-1 ≠ b)]
      omega
    · by_cases heq : p=b
      · subst p
        have hz : Nat.log2 1 = 0 := by
          have hl := (Nat.log2_lt (by decide : (1 : Nat) ≠ 0)).2 (by decide : 1 < 2^1)
          omega
        simp only [Nat.mod_self, Nat.zero_add, potential, if_pos rfl, if_true,
          if_neg (by omega : 1 ≠ b), hz]
        omega
      · have hpgt : b<p := by omega
        have hmod : p%b = p-b := by
          rw [Nat.mod_eq_sub_mod (by omega), Nat.mod_eq_of_lt (by omega)]
        rw [hmod]
        have hqb : p-b+1≠b := by omega
        simp only [potential, if_neg heq, if_neg hqb]
        have hl := log_double_lower (p-b+1) p (by omega) (by omega)
        omega

theorem scalar_progress (b p e : Nat) (hb : 2 ≤ b)
    (hp : 0 < p ∧ p ≤ 2*b-2) (he : e ≤ 1) :
    p+1 ≤ next b p e + b * overflow b p e := by
  by_cases hno : p+e<b
  · have hf : overflow b p e=0 := Nat.div_eq_of_lt hno
    have hn : next b p e=2*p+e := if_pos hno
    rw [hf, hn]
    omega
  · have hf : overflow b p e=1 := by
      apply Nat.div_eq_of_lt_le <;> omega
    have hn : next b p e=p%b+1 := if_neg hno
    rw [hf, hn]
    have hd := Nat.mod_add_div p b
    have hp0 : p/b=0 ∨ p/b=1 := by
      by_cases hlt : p<b
      · exact Or.inl (Nat.div_eq_of_lt hlt)
      · apply Or.inr
        apply Nat.div_eq_of_lt_le <;> omega
    rcases hp0 with hx | hx <;> simp only [hx, Nat.mul_zero, Nat.mul_one] at hd <;> omega

theorem odd_modulus_even_positive (m G : Int) (hm : 0<m) (hodd : m%2=1)
    (hpos : 0<G) (hdiv : G%m=0) (heven : G%2=0) : 2*m≤G := by
  have hd := Int.emod_add_ediv G m
  rw [hdiv, Int.zero_add] at hd
  have hkpos : 0<G/m := by
    by_cases hk : 0 < G/m
    · exact hk
    · have hn : G/m≤0 := by omega
      have hnprod := Int.mul_nonpos_of_nonneg_of_nonpos (by omega : 0≤m) hn
      omega
  have hpar : (G/m)%2=0 := by
    have ht := congrArg (fun x : Int => x%2) hd
    change (m * (G/m))%2=G%2 at ht
    rw [Int.mul_emod, hodd] at ht
    simp only [Int.one_mul, Int.emod_emod] at ht
    omega
  have hk : 2≤G/m := by omega
  have hg := Int.mul_le_mul_of_nonneg_left hk (by omega : 0≤m)
  omega

theorem progress_telescope (b : Int) (p g : Nat → Int) (n : Nat)
    (h : ∀ i, i<n → p i+1 ≤ p (i+1)+b*g i) :
    p 0+(n : Int) ≤ p n+b*prefixSum g n := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [prefixSum, Int.mul_add, Int.natCast_succ]
    omega

theorem closed_scalar_bounds (b : Nat) (p e : Nat → Nat) (n : Nat)
    (hb : 5≤b) (hn : 0<n)
    (hv : ∀ i, i<n → 0<p i ∧ p i≤2*b-2 ∧ e i≤1)
    (hs : ∀ i, i<n → p (i+1)=next b (p i) (e i)) (hc : p n=p 0) :
    let G := prefixSum (fun i => (overflow b (p i) (e i) : Int)) n
    0<G ∧ 2*G≤n ∧ (n : Int)≤(b : Int)*G := by
  let g := fun i => (overflow b (p i) (e i) : Int)
  have hbudget := budget_telescopes (fun i => (potential b (p i) : Int)) g n (by
    intro i hi
    have h := logarithmic_outer_budget b (p i) (e i) hb ⟨(hv i hi).1, (hv i hi).2.1⟩ (hv i hi).2.2
    dsimp only
    rw [hs i hi]
    dsimp [g]
    omega)
  have hprogress := progress_telescope (b : Int) (fun i => (p i : Int)) g n (by
    intro i hi
    have h := scalar_progress b (p i) (e i) (by omega) ⟨(hv i hi).1, (hv i hi).2.1⟩ (hv i hi).2.2
    dsimp only
    rw [hs i hi]
    dsimp [g]
    rw [← Int.natCast_mul]
    omega)
  dsimp only at hbudget hprogress
  rw [hc] at hbudget hprogress
  have hpos : 0<prefixSum g n := by
    by_cases hg : 0<prefixSum g n
    · exact hg
    · have hnon : prefixSum g n≤0 := by omega
      have hprod := Int.mul_nonpos_of_nonneg_of_nonpos (by omega : (0 : Int)≤b) hnon
      omega
  dsimp only
  change 0<prefixSum g n ∧ 2*prefixSum g n≤(n : Int) ∧ (n : Int)≤(b : Int)*prefixSum g n
  omega

theorem even_base_return_bound (b : Nat) (P G : Int) (hb : 6≤b) (he : b%2=0)
    (hg : 0<G) (hdiv : G%(b-1 : Nat)=0) (hG : G%2=0) (hp : 2*G≤P) :
    2*(b-1 : Nat)≤G ∧ 4*(b-1 : Nat)≤P := by
  have hodd : ((b-1 : Nat) : Int)%2=1 := by omega
  have hm : (0 : Int)<(b-1 : Nat) := by omega
  have h := odd_modulus_even_positive ((b-1 : Nat) : Int) G hm hodd hg hdiv hG
  omega

theorem base4_scalar_countercycle :
    next 4 1 1=3 ∧ next 4 3 1=4 ∧ next 4 4 0=1 ∧
    overflow 4 1 1+overflow 4 3 1+overflow 4 4 0=2 := by decide

#print axioms progress_telescope
#print axioms closed_scalar_bounds
#print axioms even_base_return_bound
#print axioms base4_scalar_countercycle
#print axioms log_mono
#print axioms log_double_upper
#print axioms log_double_lower
#print axioms potential_le_log
#print axioms logarithmic_outer_budget
#print axioms scalar_progress
#print axioms odd_modulus_even_positive

end P196.Agent5.General.Outer
