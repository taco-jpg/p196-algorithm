import LychrelDigitSums
import BoundaryBounds

/-!
Agent #4. The finite strip equations are derived here from the repository's
actual computed whole-word reverse-and-add map. Only an alternating overflow
clock and two fixed-depth constant coefficients at both parities are assumed.
These are restrictions on a finite actual orbit segment, not established facts
about the unrestricted orbit of 196.
-/
namespace P196.Agent4.TemporalStrip.ActualWord
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.TemporalStrip.FiniteTime

def wordAt (q : Nat → Nat) (L t : Nat) : Nat → Nat := (iterPairs q L t).2
def widthAt (q : Nat → Nat) (L t : Nat) : Nat := (iterPairs q L t).1

theorem widthAt_ge (q : Nat → Nat) (L t : Nat) : L ≤ widthAt q L t := by
  induction t with
  | zero => simp [widthAt,iterPairs]
  | succ t ih =>
    change L ≤ (iterPairs q L t).1 at ih
    simp only [widthAt,iterPairs,nextWidth]
    split <;> omega

theorem wordAt_step (q : Nat → Nat) (L t : Nat) :
    wordAt q L (t+1) = nextColumns (wordAt q L t) (widthAt q L t) := rfl

def actualCut (q : Nat → Nat) (L i : Nat) : Cut Nat where
  lowEven j := carry (wordAt q L (2*j)) i
  lowOdd j := carry (wordAt q L (2*j+1)) i
  highEven j := carry (wordAt q L (2*j)) (widthAt q L (2*j)-i)
  highOdd j := carry (wordAt q L (2*j+1)) (widthAt q L (2*j+1)-i)
  delayed j := extended (wordAt q L (2*j+1)) (widthAt q L (2*j+1))
    (widthAt q L (2*j+1)-i)

def evenCoefficient (q : Nat → Nat) (L i j : Nat) : Nat := wordAt q L (2*j) i
def oddCoefficient (q : Nat → Nat) (L i j : Nat) : Nat := wordAt q L (2*j+1) i

def Alternates (q : Nat → Nat) (L duration : Nat) : Prop := ∀ j, j<duration →
  carry (wordAt q L (2*j)) (widthAt q L (2*j))=0 ∧
  carry (wordAt q L (2*j+1)) (widthAt q L (2*j+1))=1

def Band (q : Nat → Nat) (L width duration a b : Nat) : Prop := ∀ j, j<duration →
  wordAt q L (2*j) (width-1)=a ∧ wordAt q L (2*j) width=a ∧
  wordAt q L (2*j+1) (width-1)=b ∧ wordAt q L (2*j+1) width=b

theorem actual_valid_at (q : Nat → Nat) (L i j : Nat)
    (ha : Admissible L q) (hi : i≤L) : ValidAt (actualCut q L i) j := by
  have he := CarryHistory.iterPairs_admissible q L (2*j) ha
  have ho := CarryHistory.iterPairs_admissible q L (2*j+1) ha
  have we := widthAt_ge q L (2*j)
  have wo := widthAt_ge q L (2*j+1)
  change Admissible (widthAt q L (2*j)) (wordAt q L (2*j)) at he
  change Admissible (widthAt q L (2*j+1)) (wordAt q L (2*j+1)) at ho
  unfold ValidAt actualCut
  dsimp only
  refine ⟨carry_bounded _ _ he.2.2.1 i (by omega),
    carry_bounded _ _ ho.2.2.1 i (by omega),
    carry_bounded _ _ he.2.2.1 _ (by omega),
    carry_bounded _ _ ho.2.2.1 _ (by omega),?_⟩
  unfold extended
  split
  · exact output_bounded _ _
  · have h := carry_bounded _ _ ho.2.2.1 (widthAt q L (2*j+1)) (by omega)
    omega

/-- Exact local equations, derived from computed carries and both genuine updates. -/
theorem actual_column_at (q : Nat → Nat) (L i j : Nat)
    (ha : Admissible L q) (hi : i<L)
    (he0 : carry (wordAt q L (2*j)) (widthAt q L (2*j))=0)
    (ho1 : carry (wordAt q L (2*j+1)) (widthAt q L (2*j+1))=1) :
    ColumnAt (actualCut q L i) (actualCut q L (i+1))
      (evenCoefficient q L i) (oddCoefficient q L i) j := by
  have he := CarryHistory.iterPairs_admissible q L (2*j) ha
  have ho := CarryHistory.iterPairs_admissible q L (2*j+1) ha
  have we := widthAt_ge q L (2*j)
  have wo := widthAt_ge q L (2*j+1)
  change Admissible (widthAt q L (2*j)) (wordAt q L (2*j)) at he
  change Admissible (widthAt q L (2*j+1)) (wordAt q L (2*j+1)) at ho
  have ie : i<widthAt q L (2*j) := by omega
  have io : i<widthAt q L (2*j+1) := by omega
  have re : widthAt q L (2*j)-(i+1)=widthAt q L (2*j)-1-i := by omega
  have ro : widthAt q L (2*j+1)-(i+1)=widthAt q L (2*j+1)-1-i := by omega
  unfold ColumnAt actualCut evenCoefficient oddCoefficient oddCoefficient
  dsimp only
  refine ⟨he.2.2.1 i ie,ho.2.2.1 i io,rfl,rfl,?_,?_,?_,?_,?_⟩
  · rw [re]
    exact (folded_carry_transition _ _ i ie he.2.2.2.1).2
  · rw [ro]
    exact (folded_carry_transition _ _ i io ho.2.2.2.1).2
  · rw [ro]
    have h := folded_delay_update (wordAt q L (2*j+1)) (widthAt q L (2*j+1)) i io ho.2.2.2.1
    simpa only [ro] using h
  · rw [wordAt_step,re]
    exact folded_emission_no_overflow _ _ i ie he.2.2.2.1 he0
  · have hn : 2*(j+1)=(2*j+1)+1 := by omega
    rw [hn,wordAt_step]
    exact folded_emission_overflow _ _ i io ho1

theorem actual_outside_at (q : Nat → Nat) (L j : Nat)
    (he0 : carry (wordAt q L (2*j)) (widthAt q L (2*j))=0)
    (ho1 : carry (wordAt q L (2*j+1)) (widthAt q L (2*j+1))=1) :
    OutsideAt (actualCut q L 0) j := by
  simp [OutsideAt,actualCut,carry,extended,he0,ho1]

/-- Two adjacent equal nonneutral coefficients determine both cut carries
and the delayed digit, independently of all deeper coefficients. -/
theorem constant_pair_cut (q : Nat → Nat) (L width c : Nat)
    (hb : ∀ i, i<L → q i≤18) (hs : ∀ i, i<L → q i=q (L-1-i))
    (hw : 0<width) (hwl : width<L) (hc : c≤18) (hne : c≠9)
    (hpre : q (width-1)=c) (hcur : q width=c) :
    carry q width=c/10 ∧ carry q (L-width)=c/10 ∧
    extended q L (L-width)=(c+c/10)%10 := by
  have lowBit := carry_bounded q L hb (width-1) (by omega)
  have highBit := carry_bounded q L hb (L-1-width) (by omega)
  have il : width-1+1=width := by omega
  have ilow : carry q width=(c+carry q (width-1))/10 := by
    calc
      carry q width = carry q ((width-1)+1) := congrArg (carry q) il.symm
      _ = (c+carry q (width-1))/10 := by rw [carry,hpre]
  have ihigh := (folded_carry_transition q L width hwl hs).2
  rw [hcur] at ihigh
  have hl : carry q width=c/10 := by omega
  have hh : carry q (L-width)=c/10 := by omega
  refine ⟨hl,hh,?_⟩
  have h := folded_delay_update q L (width-1) (by omega) hs
  have ir : L-1-(width-1)=L-width := by omega
  simpa only [il,ir,hpre,hh] using h

theorem actual_left_at (q : Nat → Nat) (L width j : Nat)
    (ha : Admissible L q) (hw : 0<width) (hwl : width<L)
    (h : wordAt q L (2*j) (width-1)=6 ∧ wordAt q L (2*j) width=6 ∧
      wordAt q L (2*j+1) (width-1)=12 ∧ wordAt q L (2*j+1) width=12) :
    LeftAt (actualCut q L width) j := by
  have he := CarryHistory.iterPairs_admissible q L (2*j) ha
  have ho := CarryHistory.iterPairs_admissible q L (2*j+1) ha
  have we := widthAt_ge q L (2*j)
  have wo := widthAt_ge q L (2*j+1)
  change Admissible (widthAt q L (2*j)) (wordAt q L (2*j)) at he
  change Admissible (widthAt q L (2*j+1)) (wordAt q L (2*j+1)) at ho
  have ce := constant_pair_cut _ _ width 6 he.2.2.1 he.2.2.2.1 hw
    (by omega) (by omega) (by omega) h.1 h.2.1
  have co := constant_pair_cut _ _ width 12 ho.2.2.1 ho.2.2.2.1 hw
    (by omega) (by omega) (by omega) h.2.2.1 h.2.2.2
  unfold LeftAt actualCut
  dsimp only
  exact ⟨ce.1,ce.2.1,co.2.1,by omega⟩

theorem actual_right_at (q : Nat → Nat) (L width j : Nat)
    (ha : Admissible L q) (hw : 0<width) (hwl : width<L)
    (h : wordAt q L (2*j) (width-1)=12 ∧ wordAt q L (2*j) width=12 ∧
      wordAt q L (2*j+1) (width-1)=6 ∧ wordAt q L (2*j+1) width=6) :
    RightAt (actualCut q L width) j := by
  have he := CarryHistory.iterPairs_admissible q L (2*j) ha
  have ho := CarryHistory.iterPairs_admissible q L (2*j+1) ha
  have we := widthAt_ge q L (2*j)
  have wo := widthAt_ge q L (2*j+1)
  change Admissible (widthAt q L (2*j)) (wordAt q L (2*j)) at he
  change Admissible (widthAt q L (2*j+1)) (wordAt q L (2*j+1)) at ho
  have ce := constant_pair_cut _ _ width 12 he.2.2.1 he.2.2.2.1 hw
    (by omega) (by omega) (by omega) h.1 h.2.1
  have co := constant_pair_cut _ _ width 6 ho.2.2.1 ho.2.2.2.1 hw
    (by omega) (by omega) (by omega) h.2.2.1 h.2.2.2
  unfold RightAt actualCut
  dsimp only
  exact ⟨ce.1,ce.2.1,co.2.1,by omega⟩

/-- The actual whole-word orbit cannot maintain either fixed-depth 6/12 band
for more than 2*width-1 alternating time pairs. No abstract carry path is assumed. -/
theorem actual_band_duration_bound (q : Nat → Nat) (L width duration : Nat)
    (ha : Admissible L q) (hw : 0<width) (hwl : width<L)
    (clock : Alternates q L duration)
    (band : Band q L width duration 6 12 ∨ Band q L width duration 12 6) :
    duration ≤ 2*width-1 := by
  apply finite_strip_boundary_bound (actualCut q L)
    (evenCoefficient q L) (oddCoefficient q L) width duration
  · intro i hi j _ _
    exact actual_valid_at q L i j ha (by omega)
  · intro i hi j _ hj
    exact actual_column_at q L i j ha (by omega) (clock j hj).1 (clock j hj).2
  · intro j _ hj
    exact actual_outside_at q L j (clock j hj).1 (clock j hj).2
  · rcases band with h | h
    · exact Or.inl (fun j _ hj => actual_left_at q L width j ha hw hwl (h j hj))
    · exact Or.inr (fun j _ hj => actual_right_at q L width j ha hw hwl (h j hj))

theorem actual_right_band_duration_bound (q : Nat → Nat) (L width duration : Nat)
    (ha : Admissible L q) (hw : 0<width) (hwl : width<L)
    (clock : Alternates q L duration) (band : Band q L width duration 12 6) :
    duration ≤ 2*(width-1) := by
  apply right_strip_boundary_bound (actualCut q L)
    (evenCoefficient q L) (oddCoefficient q L) width duration
  · intro i hi j _ _
    exact actual_valid_at q L i j ha (by omega)
  · intro i hi j _ hj
    exact actual_column_at q L i j ha (by omega) (clock j hj).1 (clock j hj).2
  · intro j _ hj
    exact actual_outside_at q L j (clock j hj).1 (clock j hj).2
  · exact fun j _ hj => actual_right_at q L width j ha hw hwl (band j hj)

/-- Numeric specialization: the initial q word is the actual canonical digit sum.
The imported iterPairs_representation theorem certifies every subsequent word. -/
theorem numeric_band_duration_bound (n : Nat) (d : Nat → Nat) (L width duration : Nat)
    (hcan : Canonical n d L) (hw : 0<width) (hwl : width<L)
    (clock : Alternates (columnSum d L) L duration)
    (band : Band (columnSum d L) L width duration 6 12 ∨
      Band (columnSum d L) L width duration 12 6) : duration ≤ 2*width-1 := by
  exact actual_band_duration_bound (columnSum d L) L width duration
    (NormalizationBridge.canonical_admissible n d L hcan) hw hwl clock band

#print axioms widthAt_ge
#print axioms wordAt_step
#print axioms actual_valid_at
#print axioms actual_column_at
#print axioms actual_outside_at
#print axioms constant_pair_cut
#print axioms actual_left_at
#print axioms actual_right_at
#print axioms actual_band_duration_bound
#print axioms actual_right_band_duration_bound
#print axioms numeric_band_duration_bound
end P196.Agent4.TemporalStrip.ActualWord
