import Indexing
import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace Agent13ProductWeights
open DecimalDigits FoldedDecimal Agent13FoldedFamily
open scoped BigOperators

/-- Finite coefficient words, with equality on exactly their declared width. -/
abbrev FiniteWord := (L : Nat) × (Fin L → Fin 19)

def digits (s : FiniteWord) (i : Nat) : Nat := if hi : i < s.1 then (s.2 ⟨i,hi⟩).val else 0

def encodeWord (q : Nat → Nat) (L : Nat) (hq : ∀ i, i < L → q i ≤ 18) : FiniteWord :=
  ⟨L, fun i => ⟨q i.val, by have := hq i.val i.isLt; omega⟩⟩

theorem digits_bounded (s : FiniteWord) (i : Nat) : digits s i ≤ 18 := by
  unfold digits
  split
  · have h := (s.2 ⟨i,‹i < s.1›⟩).isLt; omega
  · omega

theorem encodeWord_width (q : Nat → Nat) (L : Nat) (hq : ∀ i, i < L → q i ≤ 18) :
    (encodeWord q L hq).1 = L := rfl

theorem digits_encodeWord (q : Nat → Nat) (L : Nat) (hq : ∀ i, i < L → q i ≤ 18)
    (i : Nat) (hi : i < L) : digits (encodeWord q L hq) i = q i := by
  simp [digits, encodeWord, hi]

theorem digits_at (s : FiniteWord) (i : Fin s.1) : digits s i.val = (s.2 i).val := by
  simp [digits, i.isLt]

theorem finiteWord_ext (s t : FiniteWord) (hw : s.1=t.1)
    (hd : ∀ i, i < s.1 → digits s i = digits t i) : s=t := by
  rcases s with ⟨L,q⟩
  rcases t with ⟨M,p⟩
  dsimp at hw
  subst M
  congr 1
  funext i
  apply Fin.ext
  have h := hd i.val i.isLt
  simpa [digits, i.isLt] using h

/-- Exact transition relation expressed only using the original folded map. -/
def MapsTo (s t : FiniteWord) : Prop :=
  nextWidth (digits s) s.1 = t.1 ∧ ∀ i, i < t.1 → nextColumns (digits s) s.1 i = digits t i

def SafeState (s : FiniteWord) : Prop := WordSafe s.1 (digits s)

/-- Actual next width never decreases, including the overflow branch. -/
theorem mapsTo_width_le (s t : FiniteWord) (h : MapsTo s t) : s.1 ≤ t.1 := by
  have hw := h.1
  unfold nextWidth at hw
  split at hw <;> omega

noncomputable section

def stateBox (L : Nat) : Finset FiniteWord := (Finset.range (L+1)).sigma (fun _ => Finset.univ)

theorem mem_stateBox_iff (s : FiniteWord) (L : Nat) : s ∈ stateBox L ↔ s.1 ≤ L := by
  classical
  simp [stateBox, Nat.lt_succ_iff]

/-- A finite enumeration of the entire actual safe incoming fiber. -/
def safeFiber (t : FiniteWord) : Finset FiniteWord := by
  classical
  exact (stateBox t.1).filter (fun s => SafeState s ∧ MapsTo s t)

theorem mem_safeFiber_iff (s t : FiniteWord) : s ∈ safeFiber t ↔ SafeState s ∧ MapsTo s t := by
  classical
  simp only [safeFiber, Finset.mem_filter, mem_stateBox_iff]
  constructor
  · exact fun h => h.2
  · exact fun h => ⟨mapsTo_width_le s t h.2,h⟩

def incoming (w : FiniteWord → ℝ) (t : FiniteWord) : ℝ := ∑ s ∈ safeFiber t, w s

theorem full_safe_fiber_finite (t : FiniteWord) : Set.Finite {s | SafeState s ∧ MapsTo s t} := by
  have he : {s | SafeState s ∧ MapsTo s t} = (safeFiber t : Set FiniteWord) := by
    ext s
    exact (mem_safeFiber_iff s t).symm
  rw [he]
  exact Finset.finite_toSet _

/-- Every represented transition has the advertised ordinary-decimal meaning. -/
theorem mapsTo_actual_step (s t : FiniteWord) (hmap : MapsTo s t)
    (n : Nat) (d : Nat → Nat) (hc : Canonical n d s.1)
    (hr : ∀ i, i < s.1 → columnSum d s.1 i = digits s i) :
    ∃ d', Canonical (Lychrel196.step n) d' t.1 ∧
      ∀ i, i < t.1 → columnSum d' t.1 i = digits t i := by
  obtain ⟨d',hc',hr'⟩ := representation_next n d (digits s) s.1 hc hr
  rw [hmap.1] at hc' hr'
  exact ⟨d',hc',fun i hi => (hr' i hi).trans (hmap.2 i hi)⟩

/-- Actual reversal with a nonzero accumulator detects the canonical width.
This reuses the existing reversal semantics rather than introducing a new width. -/
theorem canonical_width_unique (n L M : Nat) (d e : Nat → Nat)
    (hd : Canonical n d L) (he : Canonical n e M) : L=M := by
  have hd0 := reverseAux_value d L 0 hd.2.1 (Or.inr hd.2.2.1)
  have hd1 := reverseAux_value d L 1 hd.2.1 (Or.inr hd.2.2.1)
  have he0 := reverseAux_value e M 0 he.2.1 (Or.inr he.2.2.1)
  have he1 := reverseAux_value e M 1 he.2.1 (Or.inr he.2.2.1)
  rw [hd.2.2.2] at hd0 hd1
  rw [he.2.2.2] at he0 he1
  have hp : 10^L=10^M := by omega
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with h | h
  · have ht := Nat.pow_lt_pow_right (by decide : 1 < 10) h
    omega
  · have ht := Nat.pow_lt_pow_right (by decide : 1 < 10) h
    omega

/-- Completeness of the arithmetic interpretation, including overflow inputs:
every actual canonical input/output representation gives the encoded edge. -/
theorem actual_step_mapsTo (s t : FiniteWord) (n : Nat) (d e : Nat → Nat)
    (hc : Canonical n d s.1)
    (hr : ∀ i, i < s.1 → columnSum d s.1 i = digits s i)
    (hc' : Canonical (Lychrel196.step n) e t.1)
    (hr' : ∀ i, i < t.1 → columnSum e t.1 i = digits t i) : MapsTo s t := by
  obtain ⟨f,hf,hq⟩ := representation_next n d (digits s) s.1 hc hr
  have hw := canonical_width_unique (Lychrel196.step n) _ _ f e hf hc'
  refine ⟨hw,?_⟩
  rw [hw] at hf hq
  have hd := value_injective f e t.1 hf.2.1 hc'.2.1 (hf.2.2.2.trans hc'.2.2.2.symm)
  intro i hi
  rw [← hq i hi, ← hr' i hi]
  simp only [columnSum,reflected]
  rw [hd i hi, hd (t.1-1-i) (by have := hc'.1; omega)]

/-- Distinct selected predecessors contribute a true partial sum to the full fiber. -/
theorem partial_sum_le_incoming {ι : Type} [Fintype ι] (w : FiniteWord → ℝ)
    (hw : ∀ s, SafeState s → 0 ≤ w s) (t : FiniteWord) (f : ι → FiniteWord)
    (hf : Function.Injective f) (hm : ∀ i, SafeState (f i) ∧ MapsTo (f i) t) :
    (∑ i, w (f i)) ≤ incoming w t := by
  classical
  have he : (∑ s ∈ Finset.univ.image f, w s) = ∑ i, w (f i) :=
    Finset.sum_image (fun i _ j _ h => hf h)
  rw [← he]
  apply Finset.sum_le_sum_of_subset_of_nonneg
  · intro s hs
    obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hs
    exact (mem_safeFiber_iff (f i) t).mpr (hm i)
  · intro s hs _
    exact hw s ((mem_safeFiber_iff s t).mp hs).1

end
end Agent13ProductWeights
