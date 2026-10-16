import BaseBirths
import ReverseAdd

/-! One-step, nooverflow bridges from BaseBirths to the existing all-base
ordinary reverse-and-add semantics. No infinite-orbit assertion is made. -/
namespace ActualBaseBirths
open BaseBirths ResetNormalization PhysicalWidth ReverseAdd

/-- The actual incoming carry at index k is the terminal carry of the
ordinary normalization of the preceding k columns. -/
def incoming (b : Int) (xs : List (Int × Bool)) (k : Nat) : Int :=
  terminal b 0 (ordinaryTags (xs.take k))

theorem ordinary_body_at (b i : Int) (xs : List (Int × Bool)) (k : Nat)
    (hk : k < xs.length) :
    (body b i (ordinaryTags xs))[k]'(by simpa [body_length,ordinaryTags] using hk) =
      (xs[k].1 + terminal b i (ordinaryTags (xs.take k)))%b := by
  induction xs generalizing i k with
  | nil => simp at hk
  | cons p xs ih =>
    cases k with
    | zero => simp [ordinaryTags,body,terminal]
    | succ k =>
      simpa [ordinaryTags,body,terminal] using
        ih ((p.1+i)/b) k (by simpa using hk)

theorem actual_nooverflow_body (b : Int) (xs : List (Int × Bool))
    (hn : terminal b 0 (ordinaryTags xs) = 0) :
    actualDigits b xs = body b 0 (ordinaryTags xs) := by
  simp [actualDigits,atActualWidth,ordinaryTags_idempotent,hn]

theorem actual_nooverflow_length (b : Int) (xs : List (Int × Bool))
    (hn : terminal b 0 (ordinaryTags xs) = 0) :
    (actualDigits b xs).length = xs.length := by
  rw [actual_nooverflow_body b xs hn,body_length]
  simp [ordinaryTags]

theorem actual_nooverflow_at (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hn : terminal b 0 (ordinaryTags xs) = 0) (hk : k < xs.length) :
    (actualDigits b xs)[k]'(by rw [actual_nooverflow_length b xs hn]; exact hk) =
      (xs[k].1 + incoming b xs k)%b := by
  simp only [actual_nooverflow_body b xs hn, incoming]
  exact ordinary_body_at b 0 xs k hk

/-- Every actual incoming carry is a bit under the existing coefficient
bounds. -/
theorem incoming_bit (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs) :
    0 ≤ incoming b xs k ∧ incoming b xs k ≤ 1 := by
  have ht : Bounded b (xs.take k) := by
    intro p hp
    exact hbound p (List.mem_of_mem_take hp)
  have hbit := terminal_bit b 0 (ordinaryTags (xs.take k)) hb (by omega)
    (ordinary_bound b (xs.take k) ht)
  dsimp [incoming]
  omega

theorem pairs_at (ds : List Int) (k : Nat) (hk : k < ds.length) :
    (pairs ds)[k]'(by rw [pairs_length]; exact hk) =
      ds[k] + ds[ds.length-1-k]'(by omega) := by
  simp [pairs,List.getElem_zipWith,List.getElem_reverse]

theorem symmetric_coefficient_at (xs : List (Int × Bool)) (k : Nat)
    (hk : k < xs.length) (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    xs[xs.length-1-k].1 = xs[k].1 := by
  calc
    xs[xs.length-1-k].1 = (xs.map Prod.fst).reverse[k]'(by simpa using hk) := by
      simp only [List.getElem_reverse,List.length_map,List.getElem_map]
    _ = (xs.map Prod.fst)[k]'(by simpa using hk) := by simp only [hs]
    _ = xs[k].1 := by simp

/-- A true output pair at index k, under computed nooverflow, has exactly
the localPair formula.  The source symmetry is used at its real mirror
index; ordinary carrying determines both incoming carries. -/
theorem actual_nooverflow_pair_at (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hn : terminal b 0 (ordinaryTags xs) = 0) (hk : k < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (pairs (actualDigits b xs))[k]'(by
      rw [pairs_length,actual_nooverflow_length b xs hn]; exact hk) =
      localPair b xs[k].1 (incoming b xs k) (incoming b xs (xs.length-1-k)) := by
  have hlen := actual_nooverflow_length b xs hn
  rw [pairs_at]
  simp only [hlen]
  rw [actual_nooverflow_at b xs k hn hk,
    actual_nooverflow_at b xs (xs.length-1-k) hn (by omega),
    symmetric_coefficient_at xs k hk hs]
  rfl

/-- Complete classification of zero pairs in actual same-width output. -/
theorem actual_zero_iff (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (hn : terminal b 0 (ordinaryTags xs) = 0) (hk : k < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    let x := xs[k].1
    let a := incoming b xs k
    let c := incoming b xs (xs.length-1-k)
    (pairs (actualDigits b xs))[k]'(by
      rw [pairs_length,actual_nooverflow_length b xs hn]; exact hk) = 0 ↔
      (x=0 ∧ a=0 ∧ c=0) ∨ (x=b ∧ a=0 ∧ c=0) ∨
      (x=b-1 ∧ a=1 ∧ c=1) := by
  dsimp only
  rw [actual_nooverflow_pair_at b xs k hn hk hs]
  exact localPair_eq_zero_iff b xs[k].1 _ _ hb
    (hbound xs[k] (List.getElem_mem hk))
    (incoming_bit b xs k hb hbound)
    (incoming_bit b xs (xs.length-1-k) hb hbound)

/-- Complete classification of maximal pairs in actual same-width output. -/
theorem actual_max_iff (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (hn : terminal b 0 (ordinaryTags xs) = 0) (hk : k < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    let x := xs[k].1
    let a := incoming b xs k
    let c := incoming b xs (xs.length-1-k)
    (pairs (actualDigits b xs))[k]'(by
      rw [pairs_length,actual_nooverflow_length b xs hn]; exact hk) = 2*b-2 ↔
      (x=b-1 ∧ a=0 ∧ c=0) ∨ (x=b-2 ∧ a=1 ∧ c=1) ∨
      (x=2*b-2 ∧ a=1 ∧ c=1) := by
  dsimp only
  rw [actual_nooverflow_pair_at b xs k hn hk hs]
  exact localPair_eq_max_iff b xs[k].1 _ _ hb
    (hbound xs[k] (List.getElem_mem hk))
    (incoming_bit b xs k hb hbound)
    (incoming_bit b xs (xs.length-1-k) hb hbound)

/-- The all-base ordinary reverse-and-add specialization: source
coefficients are the true input mirror sums, and both extreme-output
classifications apply to the canonical digits of n+reverse_b(n).
The computed nooverflow condition is explicit. -/
theorem canonical_reverse_add_extremes (b : Int) (digits : List Int)
    (xs : List (Int × Bool)) (k : Nat) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hqs : xs.map Prod.fst = pairs digits)
    (hn : terminal b 0 (ordinaryTags xs) = 0) (hk : k < xs.length) :
    let output := actualDigits b xs
    let x := xs[k].1
    let a := incoming b xs k
    let c := incoming b xs (xs.length-1-k)
    (∀ d ∈ output, 0 ≤ d ∧ d < b) ∧ PositiveLast output ∧
    SignedDigitUniqueness.eval b output =
      SignedDigitUniqueness.eval b digits + reversedValue b digits ∧
    ((pairs output)[k]'(by
      rw [pairs_length,actual_nooverflow_length b xs hn]; exact hk) = 0 ↔
      (x=0 ∧ a=0 ∧ c=0) ∨ (x=b ∧ a=0 ∧ c=0) ∨
      (x=b-1 ∧ a=1 ∧ c=1)) ∧
    ((pairs output)[k]'(by
      rw [pairs_length,actual_nooverflow_length b xs hn]; exact hk) = 2*b-2 ↔
      (x=b-1 ∧ a=0 ∧ c=0) ∨ (x=b-2 ∧ a=1 ∧ c=1) ∨
      (x=2*b-2 ∧ a=1 ∧ c=1)) := by
  dsimp only
  have hbound := tagged_pairs_bound b digits xs hd hqs
  have hs : (xs.map Prod.fst).reverse = xs.map Prod.fst := by
    rw [hqs]
    exact pairs_symmetric digits
  obtain ⟨hout,hpos,_,hvalue⟩ := reverse_add_normalization b digits xs hb hd hp hqs
  exact ⟨hout,hpos,hvalue,actual_zero_iff b xs k hb hbound hn hk hs,
    actual_max_iff b xs k hb hbound hn hk hs⟩

#print axioms ordinary_body_at
#print axioms actual_nooverflow_body
#print axioms actual_nooverflow_length
#print axioms actual_nooverflow_at
#print axioms incoming_bit
#print axioms pairs_at
#print axioms symmetric_coefficient_at
#print axioms actual_nooverflow_pair_at
#print axioms actual_zero_iff
#print axioms actual_max_iff
#print axioms canonical_reverse_add_extremes

end ActualBaseBirths
