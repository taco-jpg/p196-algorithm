import Lean.Elab.Tactic.Omega

/-! Agent #4. Arbitrary-width, arbitrary-period temporal-strip obstruction.
A temporal index is one pair of successive reverse-and-add steps, with
nonoverflow followed by overflow. The successor map is only assumed onto.
All digit/carry and delayed reflection equations are explicit below. -/
namespace P196.Agent4.TemporalStrip

structure Cut (J : Type) where
  lowEven : J → Nat
  lowOdd : J → Nat
  highEven : J → Nat
  highOdd : J → Nat
  delayed : J → Nat

def Valid {J : Type} (s : Cut J) : Prop := ∀ j,
  s.lowEven j ≤ 1 ∧ s.lowOdd j ≤ 1 ∧
  s.highEven j ≤ 1 ∧ s.highOdd j ≤ 1 ∧ s.delayed j ≤ 9

/-- Cross one spatial column, simultaneously at every temporal pair.
The right cut is closer to the constant interior band. -/
def Column {J : Type} (next : J → J) (s t : Cut J) (even odd : J → Nat) : Prop := ∀ j,
  even j ≤ 18 ∧ odd j ≤ 18 ∧
  t.lowEven j = (even j+s.lowEven j)/10 ∧
  t.lowOdd j = (odd j+s.lowOdd j)/10 ∧
  s.highEven j = (even j+t.highEven j)/10 ∧
  s.highOdd j = (odd j+t.highOdd j)/10 ∧
  t.delayed j = (odd j+t.highOdd j)%10 ∧
  odd j = (even j+s.lowEven j)%10 + (even j+t.highEven j)%10 ∧
  even (next j) = (odd j+s.lowOdd j)%10 + s.delayed j

def LeftAligned {J : Type} (s : Cut J) : Prop := ∀ j,
  s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1 ∧
  s.delayed j+s.lowOdd j=4

def RightAligned {J : Type} (s : Cut J) : Prop := ∀ j,
  s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0 ∧
  s.delayed j+s.lowOdd j=6

/-- Exact scalar classification at one temporal pair. -/
theorem left_scalar (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=0) (ly : (y+b)/10=r)
    (rx : x/10=u) (ry : (y+1)/10=v)
    (hd : (y+1)%10+r=4)
    (time : y=(x+a)%10+x%10) :
    (r=0 ∧ x=1 ∧ y=3 ∧ a=1 ∧ u=0 ∧ v=0) ∨
    (r=1 ∧ x=6 ∧ y=12 ∧ a=0 ∧ u=0 ∧ v=1) := by
  have rr : r=0 ∨ r=1 := by omega
  rcases rr with rr | rr
  · left; omega
  · right; omega

/-- Exact scalar classification in the opposite band/overflow alignment. -/
theorem right_scalar (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=1) (ly : (y+b)/10=r)
    (rx : (x+1)/10=u) (ry : y/10=v)
    (hd : y%10+r=6)
    (time : y=(x+a)%10+(x+1)%10) :
    (r=0 ∧ x=12 ∧ y=6 ∧ a=1 ∧ u=1 ∧ v=0) ∨
    (r=1 ∧ x=17 ∧ y=15 ∧ a=0 ∧ u=1 ∧ v=1) := by
  have rr : r=0 ∨ r=1 := by omega
  rcases rr with rr | rr
  · left; omega
  · right; omega

/-- No restriction on the number of temporal pairs is needed. -/
theorem left_backward {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : LeftAligned t) : LeftAligned s := by
  have classify : ∀ j,
      (t.lowOdd j=0 ∧ x j=1 ∧ y j=3 ∧ s.lowEven j=1 ∧ s.highEven j=0 ∧ s.highOdd j=0) ∨
      (t.lowOdd j=1 ∧ x j=6 ∧ y j=12 ∧ s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1) := by
    intro j
    obtain ⟨hx,hy,hlx,hly,hrx,hry,hd,hxy,hyx⟩ := hc j
    obtain ⟨hle,hre,hro,hdel⟩ := hgood j
    have vs := hs j
    have vt := ht j
    apply left_scalar (x j) (y j) (s.lowEven j) (s.lowOdd j)
      (t.lowOdd j) (s.highEven j) (s.highOdd j) hx hy vs.1 vs.2.1 vt.2.1 vs.2.2.1 vs.2.2.2.1
    · omega
    · omega
    · simpa [hre] using hrx.symm
    · simpa [hro] using hry.symm
    · rw [hd] at hdel; simpa [hro] using hdel
    · simpa [hre] using hxy
  have low : ∀ j, 2 ≤ x j := by
    intro j
    obtain ⟨i,hi⟩ := onto j
    have h := (hc i).2.2.2.2.2.2.2.2
    have vi := hs i
    have cases := classify i
    rw [hi] at h
    rcases cases with h0 | h1 <;> omega
  have regular : ∀ j, t.lowOdd j=1 ∧ x j=6 ∧ y j=12 ∧ s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1 := by
    intro j
    rcases classify j with h0 | h1
    · have h := low j; omega
    · exact h1
  intro j
  have hj := regular j
  have hn := regular (next j)
  have h := (hc j).2.2.2.2.2.2.2.2
  have v := hs j
  refine ⟨hj.2.2.2.1,hj.2.2.2.2.1,hj.2.2.2.2.2,?_⟩
  omega

theorem right_backward {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : RightAligned t) : RightAligned s := by
  have classify : ∀ j,
      (t.lowOdd j=0 ∧ x j=12 ∧ y j=6 ∧ s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0) ∨
      (t.lowOdd j=1 ∧ x j=17 ∧ y j=15 ∧ s.lowEven j=0 ∧ s.highEven j=1 ∧ s.highOdd j=1) := by
    intro j
    obtain ⟨hx,hy,hlx,hly,hrx,hry,hd,hxy,hyx⟩ := hc j
    obtain ⟨hle,hre,hro,hdel⟩ := hgood j
    have vs := hs j
    have vt := ht j
    apply right_scalar (x j) (y j) (s.lowEven j) (s.lowOdd j)
      (t.lowOdd j) (s.highEven j) (s.highOdd j) hx hy vs.1 vs.2.1 vt.2.1 vs.2.2.1 vs.2.2.2.1
    · omega
    · omega
    · simpa [hre] using hrx.symm
    · simpa [hro] using hry.symm
    · rw [hd] at hdel; simpa [hro] using hdel
    · simpa [hre] using hxy
  have upper : ∀ j, x j ≤ 16 := by
    intro j
    obtain ⟨i,hi⟩ := onto j
    have h := (hc i).2.2.2.2.2.2.2.2
    have vi := hs i
    have cases := classify i
    rw [hi] at h
    rcases cases with h0 | h1 <;> omega
  have regular : ∀ j, t.lowOdd j=0 ∧ x j=12 ∧ y j=6 ∧ s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0 := by
    intro j
    rcases classify j with h0 | h1
    · exact h0
    · have h := upper j; omega
  intro j
  have hj := regular j
  have hn := regular (next j)
  have h := (hc j).2.2.2.2.2.2.2.2
  have v := hs j
  refine ⟨hj.2.2.2.1,hj.2.2.2.2.1,hj.2.2.2.2.2,?_⟩
  omega

def Outside {J : Type} (s : Cut J) : Prop := ∀ j,
  s.lowEven j=0 ∧ s.lowOdd j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1 ∧ s.delayed j=1

theorem no_alternating_six_twelve_strip {J : Type} (j0 : J) (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (cuts : Nat → Cut J)
    (x y : Nat → J → Nat) (width : Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column next (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False := by
  have back : ∀ n, n≤width →
      (LeftAligned (cuts n) ∨ RightAligned (cuts n)) →
      (LeftAligned (cuts 0) ∨ RightAligned (cuts 0)) := by
    intro n
    induction n with
    | zero => intro hn ht; exact ht
    | succ n ih =>
      intro hn ht
      apply ih (by omega)
      rcases ht with ht | ht
      · exact Or.inl (left_backward next onto (cuts n) (cuts (n+1)) (x n) (y n)
          (hv n (by omega)) (hv (n+1) hn) (hc n (by omega)) ht)
      · exact Or.inr (right_backward next onto (cuts n) (cuts (n+1)) (x n) (y n)
          (hv n (by omega)) (hv (n+1) hn) (hc n (by omega)) ht)
  have h := back width (by omega) tail
  have h0 := outside j0
  rcases h with h | h <;> have hh := h j0 <;> omega


/-- Cyclic successor is onto for every nonempty temporal period. -/
theorem cyclic_successor_onto (N : Nat) (hN : 0<N) :
    ∀ j : Fin N, ∃ i : Fin N,
      (⟨(i.val+1)%N, Nat.mod_lt _ hN⟩ : Fin N)=j := by
  intro j
  by_cases hz : j.val=0
  · refine ⟨⟨N-1,by omega⟩,?_⟩
    apply Fin.ext
    simp only [Fin.val_mk]
    have hn : N-1+1=N := by omega
    rw [hn,Nat.mod_self,hz]
  · refine ⟨⟨j.val-1,by have h:=j.isLt; omega⟩,?_⟩
    apply Fin.ext
    simp only [Fin.val_mk]
    have hj : j.val-1+1=j.val := by omega
    rw [hj,Nat.mod_eq_of_lt j.isLt]

/-- Concrete finite-period specialization: 2N time steps, arbitrary width. -/
theorem no_finite_alternating_six_twelve_strip (N width : Nat) (hN : 0<N)
    (cuts : Nat → Cut (Fin N)) (x y : Nat → Fin N → Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column
      (fun j => ⟨(j.val+1)%N,Nat.mod_lt _ hN⟩)
      (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False := by
  exact no_alternating_six_twelve_strip ⟨0,hN⟩ _
    (cyclic_successor_onto N hN) cuts x y width hv hc outside tail

#print axioms cyclic_successor_onto
#print axioms no_finite_alternating_six_twelve_strip

#print axioms left_scalar
#print axioms right_scalar
#print axioms left_backward
#print axioms right_backward
#print axioms no_alternating_six_twelve_strip
end P196.Agent4.TemporalStrip
