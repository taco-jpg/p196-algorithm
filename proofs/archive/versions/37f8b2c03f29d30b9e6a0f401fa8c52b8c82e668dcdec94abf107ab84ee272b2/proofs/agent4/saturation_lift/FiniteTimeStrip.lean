import NoAlternatingReturn

/-!
Agent #4: open-time quantitative extension of the alternating 6/12 strip.
All columns use actual decimal carry equations, but a bridge from an arbitrary
ordinary-integer orbit to a fixed-width aligned strip is NOT assumed proved.
The temporal interval is open at its right end; there is no cyclic successor.
-/
namespace P196.Agent4.TemporalStrip.FiniteTime

abbrev Window (P : Nat → Prop) (lo hi : Nat) : Prop :=
  ∀ j, lo ≤ j → j < hi → P j

def ValidAt (s : Cut Nat) (j : Nat) : Prop :=
  s.lowEven j ≤ 1 ∧ s.lowOdd j ≤ 1 ∧
  s.highEven j ≤ 1 ∧ s.highOdd j ≤ 1 ∧ s.delayed j ≤ 9

def ColumnAt (s t : Cut Nat) (x y : Nat → Nat) (j : Nat) : Prop :=
  x j ≤ 18 ∧ y j ≤ 18 ∧
  t.lowEven j = (x j+s.lowEven j)/10 ∧
  t.lowOdd j = (y j+s.lowOdd j)/10 ∧
  s.highEven j = (x j+t.highEven j)/10 ∧
  s.highOdd j = (y j+t.highOdd j)/10 ∧
  t.delayed j = (y j+t.highOdd j)%10 ∧
  y j = (x j+s.lowEven j)%10 + (x j+t.highEven j)%10 ∧
  x (j+1) = (y j+s.lowOdd j)%10 + s.delayed j

def LeftAt (s : Cut Nat) (j : Nat) : Prop :=
  s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1 ∧
  s.delayed j+s.lowOdd j=4

def RightAt (s : Cut Nat) (j : Nat) : Prop :=
  s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0 ∧
  s.delayed j+s.lowOdd j=6

def OutsideAt (s : Cut Nat) (j : Nat) : Prop :=
  s.lowEven j=0 ∧ s.lowOdd j=0 ∧ s.highEven j=0 ∧
  s.highOdd j=1 ∧ s.delayed j=1

theorem window_mono {P : Nat → Prop} {lo hi lo' hi' : Nat}
    (h : Window P lo hi) (hl : lo ≤ lo') (hh : hi' ≤ hi) :
    Window P lo' hi' := by
  intro j hj hk
  exact h j (by omega) (by omega)

/-- Reuse the previously checked scalar classification, at a single time. -/
theorem left_classify (s t : Cut Nat) (x y : Nat → Nat) (j : Nat)
    (hs : ValidAt s j) (ht : ValidAt t j) (hc : ColumnAt s t x y j)
    (hg : LeftAt t j) :
    (t.lowOdd j=0 ∧ x j=1 ∧ y j=3 ∧ s.lowEven j=1 ∧ s.highEven j=0 ∧ s.highOdd j=0) ∨
    (t.lowOdd j=1 ∧ x j=6 ∧ y j=12 ∧ s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1) := by
  obtain ⟨hx,hy,hlx,hly,hrx,hry,hd,hxy,_⟩ := hc
  obtain ⟨hle,hre,hro,hdel⟩ := hg
  apply left_scalar (x j) (y j) (s.lowEven j) (s.lowOdd j)
    (t.lowOdd j) (s.highEven j) (s.highOdd j)
    hx hy hs.1 hs.2.1 ht.2.1 hs.2.2.1 hs.2.2.2.1
  · omega
  · omega
  · simpa [hre] using hrx.symm
  · simpa [hro] using hry.symm
  · rw [hd] at hdel; simpa [hro] using hdel
  · simpa [hre] using hxy

theorem right_classify (s t : Cut Nat) (x y : Nat → Nat) (j : Nat)
    (hs : ValidAt s j) (ht : ValidAt t j) (hc : ColumnAt s t x y j)
    (hg : RightAt t j) :
    (t.lowOdd j=0 ∧ x j=12 ∧ y j=6 ∧ s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0) ∨
    (t.lowOdd j=1 ∧ x j=17 ∧ y j=15 ∧ s.lowEven j=0 ∧ s.highEven j=1 ∧ s.highOdd j=1) := by
  obtain ⟨hx,hy,hlx,hly,hrx,hry,hd,hxy,_⟩ := hc
  obtain ⟨hle,hre,hro,hdel⟩ := hg
  apply right_scalar (x j) (y j) (s.lowEven j) (s.lowOdd j)
    (t.lowOdd j) (s.highEven j) (s.highOdd j)
    hx hy hs.1 hs.2.1 ht.2.1 hs.2.2.1 hs.2.2.2.1
  · omega
  · omega
  · simpa [hre] using hrx.symm
  · simpa [hro] using hry.symm
  · rw [hd] at hdel; simpa [hro] using hdel
  · simpa [hre] using hxy

/-- A one-column pullback loses only one temporal pair at each endpoint. -/
theorem left_backward_window (s t : Cut Nat) (x y : Nat → Nat) (lo hi : Nat)
    (hs : Window (ValidAt s) lo hi) (ht : Window (ValidAt t) lo hi)
    (hc : Window (ColumnAt s t x y) lo hi) (hg : Window (LeftAt t) lo hi) :
    Window (LeftAt s) (lo+1) (hi-1) := by
  have classify := fun j hj hk =>
    left_classify s t x y j (hs j hj hk) (ht j hj hk) (hc j hj hk) (hg j hj hk)
  have regular : ∀ j, lo < j → j < hi →
      t.lowOdd j=1 ∧ x j=6 ∧ y j=12 ∧
      s.lowEven j=0 ∧ s.highEven j=0 ∧ s.highOdd j=1 := by
    intro j hj hk
    have hp := hc (j-1) (by omega) (by omega)
    have vp := hs (j-1) (by omega) (by omega)
    unfold ValidAt at vp
    have cp := classify (j-1) (by omega) (by omega)
    have hjj : j-1+1=j := by omega
    have step := hp.2.2.2.2.2.2.2.2
    rw [hjj] at step
    have low : 2 ≤ x j := by
      rcases cp with h0 | h1 <;> omega
    rcases classify j (by omega) hk with h0 | h1
    · omega
    · exact h1
  intro j hj hk
  have rj := regular j (by omega) (by omega)
  have rn := regular (j+1) (by omega) (by omega)
  have step := (hc j (by omega) (by omega)).2.2.2.2.2.2.2.2
  have v := hs j (by omega) (by omega)
  unfold ValidAt at v
  refine ⟨rj.2.2.2.1,rj.2.2.2.2.1,rj.2.2.2.2.2,?_⟩
  omega

theorem right_backward_window (s t : Cut Nat) (x y : Nat → Nat) (lo hi : Nat)
    (hs : Window (ValidAt s) lo hi) (ht : Window (ValidAt t) lo hi)
    (hc : Window (ColumnAt s t x y) lo hi) (hg : Window (RightAt t) lo hi) :
    Window (RightAt s) (lo+1) (hi-1) := by
  have classify := fun j hj hk =>
    right_classify s t x y j (hs j hj hk) (ht j hj hk) (hc j hj hk) (hg j hj hk)
  have regular : ∀ j, lo < j → j < hi →
      t.lowOdd j=0 ∧ x j=12 ∧ y j=6 ∧
      s.lowEven j=1 ∧ s.highEven j=1 ∧ s.highOdd j=0 := by
    intro j hj hk
    have hp := hc (j-1) (by omega) (by omega)
    have vp := hs (j-1) (by omega) (by omega)
    unfold ValidAt at vp
    have cp := classify (j-1) (by omega) (by omega)
    have hjj : j-1+1=j := by omega
    have step := hp.2.2.2.2.2.2.2.2
    rw [hjj] at step
    have upper : x j ≤ 16 := by
      rcases cp with h0 | h1 <;> omega
    rcases classify j (by omega) hk with h0 | h1
    · exact h0
    · omega
  intro j hj hk
  have rj := regular j (by omega) (by omega)
  have rn := regular (j+1) (by omega) (by omega)
  have step := (hc j (by omega) (by omega)).2.2.2.2.2.2.2.2
  have v := hs j (by omega) (by omega)
  unfold ValidAt at v
  refine ⟨rj.2.2.2.1,rj.2.2.2.2.1,rj.2.2.2.2.2,?_⟩
  omega

/-- Spatial induction, with a finite temporal margin instead of a cyclic clock. -/
theorem strip_backward_window (cuts : Nat → Cut Nat) (x y : Nat → Nat → Nat)
    (width lo hi : Nat)
    (hv : ∀ i, i≤width → Window (ValidAt (cuts i)) lo hi)
    (hc : ∀ i, i<width → Window (ColumnAt (cuts i) (cuts (i+1)) (x i) (y i)) lo hi)
    (tail : Window (LeftAt (cuts width)) lo hi ∨ Window (RightAt (cuts width)) lo hi) :
    Window (LeftAt (cuts 0)) (lo+width) (hi-width) ∨
    Window (RightAt (cuts 0)) (lo+width) (hi-width) := by
  induction width generalizing lo hi with
  | zero => simpa using tail
  | succ w ih =>
    have next : Window (LeftAt (cuts w)) (lo+1) (hi-1) ∨
        Window (RightAt (cuts w)) (lo+1) (hi-1) := by
      rcases tail with h | h
      · exact Or.inl (left_backward_window _ _ _ _ _ _
          (hv w (by omega)) (hv (w+1) (by omega)) (hc w (by omega)) h)
      · exact Or.inr (right_backward_window _ _ _ _ _ _
          (hv w (by omega)) (hv (w+1) (by omega)) (hc w (by omega)) h)
    have h := ih (lo+1) (hi-1)
      (fun i hi => window_mono (hv i (by omega)) (by omega) (by omega))
      (fun i hi => window_mono (hc i (by omega)) (by omega) (by omega)) next
    have hl : lo+1+w=lo+(w+1) := by omega
    have hh : hi-1-w=hi-(w+1) := by omega
    simpa only [hl,hh] using h

/-- Any open aligned strip has at most twice its exterior width in temporal pairs.
One temporal pair represents a nonoverflow step followed by an overflow step. -/
theorem finite_strip_duration_bound (cuts : Nat → Cut Nat) (x y : Nat → Nat → Nat)
    (width duration : Nat)
    (hv : ∀ i, i≤width → Window (ValidAt (cuts i)) 0 duration)
    (hc : ∀ i, i<width → Window (ColumnAt (cuts i) (cuts (i+1)) (x i) (y i)) 0 duration)
    (outside : Window (OutsideAt (cuts 0)) 0 duration)
    (tail : Window (LeftAt (cuts width)) 0 duration ∨
      Window (RightAt (cuts width)) 0 duration) : duration ≤ 2*width := by
  by_cases h : duration ≤ 2*width
  · exact h
  exfalso
  have back := strip_backward_window cuts x y width 0 duration hv hc tail
  have ho := outside width (by omega) (by omega)
  rcases back with hl | hr
  · have hh := hl width (by omega) (by omega)
    unfold OutsideAt at ho
    unfold LeftAt at hh
    omega
  · have hh := hr width (by omega) (by omega)
    unfold OutsideAt at ho
    unfold RightAt at hh
    omega

#print axioms window_mono
#print axioms left_classify
#print axioms right_classify
#print axioms left_backward_window
#print axioms right_backward_window
#print axioms strip_backward_window
#print axioms finite_strip_duration_bound
end P196.Agent4.TemporalStrip.FiniteTime
