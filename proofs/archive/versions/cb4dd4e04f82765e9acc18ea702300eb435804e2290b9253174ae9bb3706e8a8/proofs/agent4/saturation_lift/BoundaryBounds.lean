import FiniteTimeStrip

/-! Agent #4. Boundary-sensitive improvements of the open-time strip bound. -/
namespace P196.Agent4.TemporalStrip.FiniteTime

/-- An exterior boundary can meet a left-aligned tail for one pair, not two. -/
theorem left_outside_two_pairs (s t : Cut Nat) (x y : Nat → Nat) (j : Nat)
    (hs : ValidAt s j) (ht : ValidAt t j) (hc : ColumnAt s t x y j)
    (hs' : ValidAt s (j+1)) (ht' : ValidAt t (j+1))
    (hc' : ColumnAt s t x y (j+1))
    (ho : OutsideAt s j) (hg : LeftAt t j) (hg' : LeftAt t (j+1)) : False := by
  have cj := left_classify s t x y j hs ht hc hg
  have cn := left_classify s t x y (j+1) hs' ht' hc' hg'
  have step := hc.2.2.2.2.2.2.2.2
  unfold OutsideAt at ho
  rcases cj with h0 | h1
  · omega
  · rcases cn with n0 | n1 <;> omega

/-- The opposite tail alignment cannot touch an exterior boundary even once. -/
theorem right_outside_one_pair (s t : Cut Nat) (x y : Nat → Nat) (j : Nat)
    (hs : ValidAt s j) (ht : ValidAt t j) (hc : ColumnAt s t x y j)
    (ho : OutsideAt s j) (hg : RightAt t j) : False := by
  have cj := right_classify s t x y j hs ht hc hg
  unfold OutsideAt at ho
  rcases cj with h0 | h1 <;> omega

/-- The right alignment is preserved by spatial pullback on the smaller window. -/
theorem right_strip_backward (cuts : Nat → Cut Nat) (x y : Nat → Nat → Nat)
    (width lo hi : Nat)
    (hv : ∀ i, i≤width → Window (ValidAt (cuts i)) lo hi)
    (hc : ∀ i, i<width → Window (ColumnAt (cuts i) (cuts (i+1)) (x i) (y i)) lo hi)
    (tail : Window (RightAt (cuts width)) lo hi) :
    Window (RightAt (cuts 0)) (lo+width) (hi-width) := by
  induction width generalizing lo hi with
  | zero => simpa using tail
  | succ w ih =>
    have next := right_backward_window (cuts w) (cuts (w+1)) (x w) (y w) lo hi
      (hv w (by omega)) (hv (w+1) (by omega)) (hc w (by omega)) tail
    have h := ih (lo+1) (hi-1)
      (fun i hi => window_mono (hv i (by omega)) (by omega) (by omega))
      (fun i hi => window_mono (hc i (by omega)) (by omega) (by omega)) next
    have hl : lo+1+w=lo+(w+1) := by omega
    have hh : hi-1-w=hi-(w+1) := by omega
    simpa only [hl,hh] using h

/-- Improved bound for either alignment. Natural subtraction handles width zero. -/
theorem finite_strip_boundary_bound (cuts : Nat → Cut Nat) (x y : Nat → Nat → Nat)
    (width duration : Nat)
    (hv : ∀ i, i≤width → Window (ValidAt (cuts i)) 0 duration)
    (hc : ∀ i, i<width → Window (ColumnAt (cuts i) (cuts (i+1)) (x i) (y i)) 0 duration)
    (outside : Window (OutsideAt (cuts 0)) 0 duration)
    (tail : Window (LeftAt (cuts width)) 0 duration ∨
      Window (RightAt (cuts width)) 0 duration) : duration ≤ 2*width-1 := by
  cases width with
  | zero =>
    have h := finite_strip_duration_bound cuts x y 0 duration hv hc outside tail
    omega
  | succ w =>
    by_cases hb : duration ≤ 2*(w+1)-1
    · exact hb
    exfalso
    have back := strip_backward_window (fun i => cuts (i+1))
      (fun i => x (i+1)) (fun i => y (i+1)) w 0 duration
      (fun i hi => hv (i+1) (by omega))
      (fun i hi => hc (i+1) (by omega)) tail
    have hsw := hv 0 (by omega) w (by omega) (by omega)
    have htw := hv 1 (by omega) w (by omega) (by omega)
    have hcw := hc 0 (by omega) w (by omega) (by omega)
    have how := outside w (by omega) (by omega)
    rcases back with hl | hr
    · exact left_outside_two_pairs (cuts 0) (cuts 1) (x 0) (y 0) w
        hsw htw hcw
        (hv 0 (by omega) (w+1) (by omega) (by omega))
        (hv 1 (by omega) (w+1) (by omega) (by omega))
        (hc 0 (by omega) (w+1) (by omega) (by omega))
        how (hl w (by omega) (by omega)) (hl (w+1) (by omega) (by omega))
    · exact right_outside_one_pair (cuts 0) (cuts 1) (x 0) (y 0) w
        hsw htw hcw how (hr w (by omega) (by omega))

/-- The right alignment admits the stronger bound N <= 2*(width-1). -/
theorem right_strip_boundary_bound (cuts : Nat → Cut Nat) (x y : Nat → Nat → Nat)
    (width duration : Nat)
    (hv : ∀ i, i≤width → Window (ValidAt (cuts i)) 0 duration)
    (hc : ∀ i, i<width → Window (ColumnAt (cuts i) (cuts (i+1)) (x i) (y i)) 0 duration)
    (outside : Window (OutsideAt (cuts 0)) 0 duration)
    (tail : Window (RightAt (cuts width)) 0 duration) : duration ≤ 2*(width-1) := by
  cases width with
  | zero =>
    have h := finite_strip_duration_bound cuts x y 0 duration hv hc outside (Or.inr tail)
    omega
  | succ w =>
    by_cases hb : duration ≤ 2*w
    · simpa using hb
    exfalso
    have back := right_strip_backward (fun i => cuts (i+1))
      (fun i => x (i+1)) (fun i => y (i+1)) w 0 duration
      (fun i hi => hv (i+1) (by omega))
      (fun i hi => hc (i+1) (by omega)) tail
    exact right_outside_one_pair (cuts 0) (cuts 1) (x 0) (y 0) w
      (hv 0 (by omega) w (by omega) (by omega))
      (hv 1 (by omega) w (by omega) (by omega))
      (hc 0 (by omega) w (by omega) (by omega))
      (outside w (by omega) (by omega)) (back w (by omega) (by omega))

/-- A finite-width forward-infinite aligned strip is impossible; no return is needed. -/
theorem no_forward_infinite_aligned_strip (cuts : Nat → Cut Nat)
    (x y : Nat → Nat → Nat) (width : Nat)
    (hv : ∀ i, i≤width → ∀ j, ValidAt (cuts i) j)
    (hc : ∀ i, i<width → ∀ j, ColumnAt (cuts i) (cuts (i+1)) (x i) (y i) j)
    (outside : ∀ j, OutsideAt (cuts 0) j)
    (tail : (∀ j, LeftAt (cuts width) j) ∨ (∀ j, RightAt (cuts width) j)) : False := by
  have ht : Window (LeftAt (cuts width)) 0 (2*width+1) ∨
      Window (RightAt (cuts width)) 0 (2*width+1) := by
    rcases tail with h | h
    · exact Or.inl (fun j _ _ => h j)
    · exact Or.inr (fun j _ _ => h j)
  have h := finite_strip_duration_bound cuts x y width (2*width+1)
    (fun i hi j _ _ => hv i hi j) (fun i hi j _ _ => hc i hi j)
    (fun j _ _ => outside j) ht
  omega

/-- Small exact control: a one-pair open strip is genuinely possible. -/
def onePairOutside : Cut Nat := ⟨fun _ => 0, fun _ => 0, fun _ => 0, fun _ => 1, fun _ => 1⟩
def onePairTail : Cut Nat := ⟨fun _ => 0, fun _ => 1, fun _ => 0, fun _ => 1, fun _ => 3⟩
def onePairEven (j : Nat) : Nat := if j=0 then 6 else 3

theorem one_pair_control :
    ValidAt onePairOutside 0 ∧ ValidAt onePairTail 0 ∧
    OutsideAt onePairOutside 0 ∧ LeftAt onePairTail 0 ∧
    ColumnAt onePairOutside onePairTail onePairEven (fun _ => 12) 0 := by
  unfold ValidAt OutsideAt LeftAt ColumnAt
  decide

#print axioms left_outside_two_pairs
#print axioms right_outside_one_pair
#print axioms right_strip_backward
#print axioms finite_strip_boundary_bound
#print axioms right_strip_boundary_bound
#print axioms no_forward_infinite_aligned_strip
#print axioms one_pair_control
end P196.Agent4.TemporalStrip.FiniteTime
