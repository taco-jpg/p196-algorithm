import ChargeSymmetry

/-!
Exact finite-sum bridge to the two original carry_coordinates formulas.
The sum is over all mirror pairs, with the complete carry-word length retained.
-/

namespace P196.Agent15.SpectralCarry

def sumFirst : (Nat → Int) → Nat → Int
  | _, 0 => 0
  | f, n + 1 => f 0 + sumFirst (fun i => f (i + 1)) n

theorem sumFirst_eq_range_sum (f : Nat → Int) (n : Nat) :
    sumFirst f n = ((List.range n).map f).sum := by
  induction n generalizing f with
  | zero => rfl
  | succ n ih =>
    simp [sumFirst, List.range_succ_eq_map, List.map_map, ih, Function.comp_def]

theorem sumFirst_congr {f g : Nat → Int} (n : Nat)
    (h : ∀ i, i < n → f i = g i) : sumFirst f n = sumFirst g n := by
  induction n generalizing f g with
  | zero => rfl
  | succ n ih =>
    simp only [sumFirst]
    rw [h 0 (by omega)]
    apply congrArg (fun z => g 0 + z)
    apply ih
    intro i hi
    exact h (i + 1) (by omega)

theorem sumFirst_sub (f g : Nat → Int) (n : Nat) :
    sumFirst f n - sumFirst g n = sumFirst (fun i => f i - g i) n := by
  induction n generalizing f g with
  | zero => simp [sumFirst]
  | succ n ih =>
    simp only [sumFirst]
    have h := ih (fun i => f (i + 1)) (fun i => g (i + 1))
    omega

theorem weighted_eq_sumFirst (w : Nat → Int) (cs : List Nat) :
    weighted w cs = sumFirst
      (fun i => ((cs[i]?.getD 0 : Nat) : Int) * w (cs.length - 1 - i)) cs.length := by
  induction cs with
  | nil => rfl
  | cons a cs ih =>
    simp only [weighted, List.length_cons, sumFirst,
      List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [ih]
    congr 1
    apply sumFirst_congr
    intro i hi
    congr 2 <;> omega

theorem weighted_take_eq_sumFirst (w : Nat → Int) (cs : List Nat)
    (n : Nat) (hn : n ≤ cs.length) :
    weighted w (cs.take n) = sumFirst
      (fun i => ((cs[i]?.getD 0 : Nat) : Int) * w (n - 1 - i)) n := by
  rw [weighted_eq_sumFirst, List.length_take_of_le hn]
  apply sumFirst_congr
  intro i hi
  rw [List.getElem?_take_of_lt hi]

theorem halfCharge_eq_source_sum (w : Nat → Int) (cs : List Nat) :
    halfCharge w cs = sumFirst
      (fun i => (((cs[cs.length - 1 - i]?.getD 0 : Nat) : Int) -
        ((cs[i]?.getD 0 : Nat) : Int)) * w (cs.length / 2 - 1 - i))
      (cs.length / 2) := by
  have hn : cs.length / 2 ≤ cs.length := by omega
  have hr : cs.length / 2 ≤ cs.reverse.length := by simpa using hn
  unfold halfCharge
  rw [weighted_take_eq_sumFirst w cs.reverse _ hr,
    weighted_take_eq_sumFirst w cs _ hn, sumFirst_sub]
  apply sumFirst_congr
  intro i hi
  have hil : i < cs.length := by omega
  rw [List.getElem?_reverse hil, Int.sub_mul]

theorem oddCharge_eq_source_sum (cs : List Nat) (m : Nat)
    (hlen : cs.length = 2 * m + 1) :
    oddCharge cs = sumFirst
      (fun i => (((cs[2 * m - i]?.getD 0 : Nat) : Int) -
        ((cs[i]?.getD 0 : Nat) : Int)) * U (m - i)) m := by
  unfold oddCharge
  rw [halfCharge_eq_source_sum]
  have hm : cs.length / 2 = m := by omega
  rw [hm]
  apply sumFirst_congr
  intro i hi
  have hind : cs.length - 1 - i = 2 * m - i := by omega
  have hw : m - 1 - i + 1 = m - i := by omega
  simp only [oddWeight, hind, hw]

theorem evenCharge_eq_source_sum (cs : List Nat) (m : Nat)
    (hlen : cs.length = 2 * m) :
    evenCharge cs = sumFirst
      (fun i => (((cs[2 * m - 1 - i]?.getD 0 : Nat) : Int) -
        ((cs[i]?.getD 0 : Nat) : Int)) * S (m - 1 - i)) m := by
  unfold evenCharge
  rw [halfCharge_eq_source_sum]
  have hm : cs.length / 2 = m := by omega
  simp only [hlen, hm, evenWeight]

theorem carryCharge_eq_odd_source_sum (cs : List Nat) (m : Nat)
    (hlen : cs.length = 2 * m + 1) :
    carryCharge cs = sumFirst
      (fun i => (((cs[2 * m - i]?.getD 0 : Nat) : Int) -
        ((cs[i]?.getD 0 : Nat) : Int)) * U (m - i)) m := by
  have hp : cs.length % 2 = 1 := by omega
  simp only [carryCharge, hp, ↓reduceIte]
  exact oddCharge_eq_source_sum cs m hlen

theorem carryCharge_eq_even_source_sum (cs : List Nat) (m : Nat)
    (hlen : cs.length = 2 * m) :
    carryCharge cs = sumFirst
      (fun i => (((cs[2 * m - 1 - i]?.getD 0 : Nat) : Int) -
        ((cs[i]?.getD 0 : Nat) : Int)) * S (m - 1 - i)) m := by
  have hp : ¬ cs.length % 2 = 1 := by omega
  simp only [carryCharge, hp, ↓reduceIte]
  exact evenCharge_eq_source_sum cs m hlen

end P196.Agent15.SpectralCarry
