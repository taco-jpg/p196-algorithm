import Agent415ActualInverseColumn

/-!
Agent #415: derive the 8/17 exterior root from exact temporal-strip equations,
then obtain a finite inverse-column path from the actual decimal pair orbit.
The outer-8, alternation, common-width and return premises remain explicit.
-/
namespace Agent415.InverseColumn
open P196.Agent4.TemporalStrip BoundaryCertificate
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open Agent104.TemporalStripObligations

/-- Persistent outer even sum 8 forces odd sum 17 and the next encoded root 41.
Neither the odd pair sum nor the inverse-certificate root is assumed. -/
theorem outer_eight_forces_root {J : Type} (next : J → J) (s t : Cut J)
    (x y : J → Nat) (hs : Outside s) (ht : Valid t)
    (hc : Column next s t x y) (hx : ∀ j, x j = 8) (j : J) :
    y j = 17 ∧ encode t j = 41 := by
  obtain ⟨hsa, hsb, hsc, hse, hsz⟩ := hs j
  obtain ⟨hta, htb, htc, hte, htz⟩ := ht j
  obtain ⟨hxb, hyb, hla, hlb, hrc, hre, hdel, hxy, hyx⟩ := hc j
  rw [hx j, hsa] at hla hxy
  rw [hx (next j), hsb, hsz] at hyx
  have hodd : y j = 17 := by omega
  have hinner : t.highEven j = 1 := by omega
  have hlo0 : t.lowEven j = 0 := by omega
  have hlo1 : t.lowOdd j = 1 := by omega
  have hshift := shifted_digit (y j) (t.highOdd j) (s.highOdd j)
    (t.delayed j) hte hre hdel
  refine ⟨hodd, ?_⟩
  unfold encode
  rw [hlo0, hlo1, hinner]
  omega

/-- Consecutive edges produce the actual finite spatial path, for any length. -/
theorem path_of_interval {α : Type} (E : α → α → Prop) (w : Nat → α)
    (a m : Nat) (h : ∀ i, i < m → E (w (a+i)) (w (a+i+1))) :
    ReverseClosure.Path E (w a) (w (a+m)) := by
  induction m with
  | zero => simpa using ReverseClosure.Path.refl (w a)
  | succ m ih =>
    have hp := ih (fun i hi => h i (by omega))
    exact ReverseClosure.Path.snoc hp (h m (by omega))

/-- The first interior temporal word is the existing certificate root 41. -/
theorem actual_root_eight (q : Nat → Nat) (L n width : Nat)
    (hn : 0 < n) (hwidth : 0 < width) (ha : Admissible L q)
    (hw : ∀ j : Fin n, width ≤ widthAt q L (2*j.val) ∧
      width ≤ widthAt q L (2*j.val+1))
    (hg : ∀ j : Fin n,
      carry (qAt q L (2*j.val)) (widthAt q L (2*j.val)) = 0 ∧
      carry (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1)) = 1)
    (hp : ∀ i, i < width → qAt q L (2*n) i = q i)
    (houter : ∀ j : Fin n, qAt q L (2*j.val) 0 = 8) :
    actualWord q L n hn 1 = (fun _ => 41) := by
  obtain ⟨hv, hc, ho⟩ := Agent112.TwoPhase.actual_prefix_transport q L n width hn ha hw hg hp
  funext i
  exact (outer_eight_forces_root (cycleNext n hn) _ _ _ _ ho
    (hv 1 (by omega)) (hc 0 hwidth) houter ⟨i % n, Nat.mod_lt i hn⟩).2

/-- The inverse-column path is derived, not postulated, for the actual orbit. -/
theorem actual_root_path (q : Nat → Nat) (L n width : Nat)
    (hn : 0 < n) (hwidth : 0 < width) (ha : Admissible L q)
    (hw : ∀ j : Fin n, width ≤ widthAt q L (2*j.val) ∧
      width ≤ widthAt q L (2*j.val+1))
    (hg : ∀ j : Fin n,
      carry (qAt q L (2*j.val)) (widthAt q L (2*j.val)) = 0 ∧
      carry (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1)) = 1)
    (hp : ∀ i, i < width → qAt q L (2*n) i = q i)
    (houter : ∀ j : Fin n, qAt q L (2*j.val) 0 = 8) :
    ReverseClosure.Path (ArithmeticColumn n) (fun _ => 41)
      (actualWord q L n hn width) := by
  have hcol := actual_inverse_columns q L n width hn ha hw hg hp
  have hpath := path_of_interval (ArithmeticColumn n) (actualWord q L n hn)
    1 (width-1) (fun i hi => hcol (1+i) (by omega))
  rw [actual_root_eight q L n width hn hwidth ha hw hg hp houter] at hpath
  simpa only [show 1+(width-1) = width by omega] using hpath

end Agent415.InverseColumn
#print axioms Agent415.InverseColumn.outer_eight_forces_root
#print axioms Agent415.InverseColumn.path_of_interval
#print axioms Agent415.InverseColumn.actual_root_eight
#print axioms Agent415.InverseColumn.actual_root_path
