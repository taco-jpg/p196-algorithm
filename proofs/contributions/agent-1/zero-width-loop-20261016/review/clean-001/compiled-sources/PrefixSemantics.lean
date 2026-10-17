import ActualWordBridge

namespace Agent8

abbrev Triple3 := Nat × Nat × Nat

def firstThree : Word → Triple3
  | p :: a :: b :: _ => (p,a,b)
  | _ => (0,0,0)

def prefixNext (q : Triple3) (e : Nat) : Triple3 :=
  let p := q.1
  let a := q.2.1
  let b := q.2.2
  let l1 := p / 10
  let l2 := (a + l1) / 10
  let r2 := (b + e) / 10
  let r1 := (a + r2) / 10
  let g := (p + r1) / 10
  if g = 0 then
    (p % 10 + (p+r1) % 10,
      (a+l1) % 10 + (a+r2) % 10,
      (b+l2) % 10 + (b+e) % 10)
  else
    (p % 10 + 1,
      (a+l1) % 10 + (p+r1) % 10,
      (b+l2) % 10 + (a+r2) % 10)

def prefixOverflow (q : Triple3) (e : Nat) : Nat :=
  (q.1 + (q.2.1 + (q.2.2 + e)/10)/10)/10

theorem fixedDigits_append (a b : Word) (e : Nat) :
    fixedDigits (a++b) e = fixedDigits a e ++ fixedDigits b (terminalCarry a e) := by
  induction a generalizing e with
  | nil => rfl
  | cons x xs ih => simp [fixedDigits, terminalCarry, ih]

theorem shaped_prefix_step (p a b : Nat) (M : Word)
    (hp : p ≤ 18) (ha : a ≤ 18) (hb : b ≤ 18)
    (he : terminalCarry ([p,a,b]++M) 0 ≤ 1) :
    firstThree (stepWord ([p,a,b]++M++[b,a,p])) =
      prefixNext (p,a,b) (terminalCarry ([p,a,b]++M) 0) := by
  let e := terminalCarry ([p,a,b]++M) 0
  let l1 := p/10
  let l2 := (a+l1)/10
  let l3 := (b+l2)/10
  let r2 := (b+e)/10
  let r1 := (a+r2)/10
  let g := (p+r1)/10
  have hg : g ≤ 1 := by
    have he' : e ≤ 1 := he
    have hr2 : r2 ≤ 1 := by dsimp [r2]; omega
    have hr1 : r1 ≤ 1 := by dsimp [r1]; omega
    dsimp [g]; omega
  have hn : normalize ([p,a,b]++M++[b,a,p]) 0 =
      [p%10,(a+l1)%10,(b+l2)%10] ++ fixedDigits M l3 ++
      [(b+e)%10,(a+r2)%10,(p+r1)%10] ++ (if g=0 then [] else [g]) := by
    simp [normalize_append, fixedDigits_append, normalize, fixedDigits,
      terminalCarry, e, l1, l2, l3, r2, r1, g, List.append_assoc]
  change firstThree (stepWord ([p,a,b]++M++[b,a,p])) = prefixNext (p,a,b) e
  simp only [stepWord, hn]
  by_cases hzero : g=0
  · have hz : (p+(a+(b+e)/10)/10)/10=0 := hzero
    simp only [if_pos hzero]
    simp [pair, List.reverse_append, zipAdd, firstThree, prefixNext,
      hz, l1, l2, l3, r2, r1]
  · have hone : g=1 := by omega
    have hz : (p+(a+(b+e)/10)/10)/10=1 := hone
    simp only [if_neg hzero, hone]
    simp [pair, List.reverse_append, zipAdd, firstThree, prefixNext,
      hz, l1, l2, l3, r2, r1]

theorem symmetric_three_decomposition (w : Word) (p a b : Nat)
    (hr : w.reverse = w) (ht : w.take 3 = [p,a,b]) (hl : 6 ≤ w.length) :
    w = [p,a,b] ++ (w.drop 3).take (w.length-6) ++ [b,a,p] := by
  have hs : w.drop (w.length-3) = [b,a,p] := by
    calc
      w.drop (w.length-3) = (w.take 3).reverse := by rw [List.reverse_take, hr]
      _ = [b,a,p] := by rw [ht]; rfl
  have hi : 3 + (w.length-6) = w.length-3 := by omega
  have hd : (w.drop 3).drop (w.length-6) = [b,a,p] := by
    rw [List.drop_drop, hi, hs]
  have hm := List.take_append_drop (w.length-6) (w.drop 3)
  have hm' : w.drop 3 = (w.drop 3).take (w.length-6) ++ [b,a,p] := by
    calc
      w.drop 3 = (w.drop 3).take (w.length-6) ++ (w.drop 3).drop (w.length-6) := hm.symm
      _ = (w.drop 3).take (w.length-6) ++ [b,a,p] := by rw [hd]
  calc
    w = w.take 3 ++ w.drop 3 := (List.take_append_drop 3 w).symm
    _ = [p,a,b] ++ ((w.drop 3).take (w.length-6) ++ [b,a,p]) := by
      rw [ht]
      exact congrArg (fun z => [p,a,b]++z) hm'
    _ = [p,a,b] ++ (w.drop 3).take (w.length-6) ++ [b,a,p] := by simp [List.append_assoc]

def inputThree (w : Word) : Nat := terminalCarry (w.take (w.length-3)) 0

theorem inputThree_shaped (p a b : Nat) (M : Word) :
    inputThree ([p,a,b]++M++[b,a,p]) = terminalCarry ([p,a,b]++M) 0 := by
  have hn : ([p,a,b]++M++[b,a,p]).length-3 = ([p,a,b]++M).length := by simp
  simp only [inputThree, hn, List.take_left]

theorem inputThree_bound (w : Word) (hb : Bounded w 18) : inputThree w ≤ 1 := by
  apply terminalCarry_le_one _ 0 _ (by decide)
  intro x hx
  exact hb x (List.mem_of_mem_take hx)

theorem terminalCarry_eq_actual_overflow (w : Word) (hw : CanonicalPair w) :
    terminalCarry w 0 = overflow (w.headD 0) (lastInput w) := by
  have hs := (canonical_step w hw).2.2.1
  have hn := normalize_length w 0 hw.2.2.1 (by decide)
  have hp := pair_length (normalize w 0)
  change (stepWord w).length = (normalize w 0).length at hp
  omega

theorem prefix_step_of_canonical (w : Word) (hw : CanonicalPair w) (hl : 6 ≤ w.length) :
    firstThree (stepWord w) = prefixNext (firstThree w) (inputThree w) ∧
    inputThree w ≤ 1 ∧
    prefixOverflow (firstThree w) (inputThree w) = overflow (w.headD 0) (lastInput w) := by
  obtain ⟨p,a,b,M,heq⟩ : ∃ p a b M, w = p::a::b::M := by
    cases w with
    | nil => simp at hl
    | cons p xs =>
      cases xs with
      | nil => simp at hl
      | cons a ys =>
        cases ys with
        | nil => simp at hl
        | cons b M => exact ⟨p,a,b,M,rfl⟩
  have ht : w.take 3 = [p,a,b] := by simp [heq]
  have hf : firstThree w = (p,a,b) := by simp [heq, firstThree]
  let middle := (w.drop 3).take (w.length-6)
  have hs : w = [p,a,b] ++ middle ++ [b,a,p] := symmetric_three_decomposition w p a b hw.2.1 ht hl
  have hi : inputThree w = terminalCarry ([p,a,b]++middle) 0 := by rw [hs, inputThree_shaped]
  have hbnd := hw.2.2.1
  have hp : p ≤ 18 := hbnd p (by simp [heq])
  have ha : a ≤ 18 := hbnd a (by simp [heq])
  have hb : b ≤ 18 := hbnd b (by simp [heq])
  have he := inputThree_bound w hbnd
  have he' : terminalCarry ([p,a,b]++middle) 0 ≤ 1 := by rw [← hi]; exact he
  refine ⟨?_, he, ?_⟩
  · rw [hf, hi]
    exact (congrArg (fun z => firstThree (stepWord z)) hs).trans
      (shaped_prefix_step p a b middle hp ha hb he')
  · rw [hf, hi, ← terminalCarry_eq_actual_overflow w hw, hs, terminalCarry_append]
    simp [terminalCarry_append, terminalCarry, prefixOverflow]

theorem canonical_orbit_length_mono (w : Word) (hw : CanonicalPair w) (n : Nat) :
    w.length ≤ (orbit w n).length := by
  induction n with
  | zero => exact Nat.le_refl _
  | succ n ih =>
    have h := (canonical_step (orbit w n) (canonical_orbit w hw n)).2.2.1
    change (orbit w (n+1)).length = _ at h
    omega

theorem firstThree_valid (w : Word) (hw : CanonicalPair w) (hl : 3 ≤ w.length) :
    0 < (firstThree w).1 ∧ (firstThree w).1 ≤ 18 ∧
    (firstThree w).2.1 ≤ 18 ∧ (firstThree w).2.2 ≤ 18 := by
  cases w with
  | nil => simp at hl
  | cons p xs =>
    cases xs with
    | nil => simp at hl
    | cons a ys =>
      cases ys with
      | nil => simp at hl
      | cons b zs =>
        exact ⟨hw.2.2.2, hw.2.2.1 p (by simp), hw.2.2.1 a (by simp), hw.2.2.1 b (by simp)⟩


#print axioms fixedDigits_append
#print axioms shaped_prefix_step
#print axioms symmetric_three_decomposition
#print axioms inputThree_shaped
#print axioms inputThree_bound
#print axioms terminalCarry_eq_actual_overflow
#print axioms prefix_step_of_canonical
#print axioms canonical_orbit_length_mono
#print axioms firstThree_valid

end Agent8
