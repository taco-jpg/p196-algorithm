import P196.Drafts.Agent15SpectralCarryCharge.BinaryCode

/-!
The original antisymmetric charge, with the actual word length retained.
The initial incoming zero is not part of the outgoing-carry word.
-/

namespace P196.Agent15.SpectralCarry

theorem reverse_take_half_iff {α : Type} (cs : List α) :
    cs.reverse.take (cs.length / 2) = cs.take (cs.length / 2) ↔
      cs.reverse = cs := by
  constructor
  · intro h
    have half (j : Nat) (hj : j < cs.length / 2) :
        cs.reverse[j]? = cs[j]? := by
      have he := congrArg (fun xs : List α => xs[j]?) h
      simpa only [List.getElem?_take_of_lt hj] using he
    apply List.ext_getElem?
    intro i
    by_cases hi : i < cs.length
    · by_cases hf : i < cs.length / 2
      · exact half i hf
      · by_cases hj : cs.length - 1 - i < cs.length / 2
        · have he := half (cs.length - 1 - i) hj
          have hjlen : cs.length - 1 - i < cs.length := by omega
          rw [List.getElem?_reverse hjlen] at he
          have back : cs.length - 1 - (cs.length - 1 - i) = i := by omega
          rw [back] at he
          rw [List.getElem?_reverse hi]
          exact he.symm
        · have center : cs.length - 1 - i = i := by omega
          rw [List.getElem?_reverse hi, center]
    · have hn : cs.length ≤ i := by omega
      have hr : cs.reverse.length ≤ i := by simpa using hn
      exact (List.getElem?_eq_none hr).trans (List.getElem?_eq_none hn).symm
  · intro h
    rw [h]

def halfCharge (w : Nat → Int) (cs : List Nat) : Int :=
  weighted w (cs.reverse.take (cs.length / 2)) -
    weighted w (cs.take (cs.length / 2))

def oddCharge (cs : List Nat) : Int := halfCharge oddWeight cs

def evenCharge (cs : List Nat) : Int := halfCharge evenWeight cs

def carryCharge (cs : List Nat) : Int :=
  if cs.length % 2 = 1 then oddCharge cs else evenCharge cs

theorem binary_reverse {cs : List Nat} (h : Binary cs) : Binary cs.reverse := by
  intro a ha
  exact h a (List.mem_reverse.mp ha)

theorem binary_take {cs : List Nat} (h : Binary cs) (n : Nat) :
    Binary (cs.take n) := by
  intro a ha
  exact h a (List.mem_of_mem_take ha)

theorem halfCharge_zero_iff (w : Nat → Int) (hpos : ∀ n, 0 ≤ w n)
    (hdom : ∀ n, weightSum w n < w n) {cs : List Nat} (hc : Binary cs) :
    halfCharge w cs = 0 ↔ cs.reverse = cs := by
  constructor
  · intro hz
    apply (reverse_take_half_iff cs).mp
    apply weighted_injective_binary w hpos hdom
      (binary_take (binary_reverse hc) _) (binary_take hc _)
    · simp
    · unfold halfCharge at hz
      omega
  · intro h
    simp [halfCharge, h]

theorem oddCharge_zero_iff {cs : List Nat} (hc : Binary cs) :
    oddCharge cs = 0 ↔ cs.reverse = cs := by
  exact halfCharge_zero_iff oddWeight (fun n => Int.le_of_lt (oddWeight_pos n))
    oddWeight_superincreasing hc

theorem evenCharge_zero_iff {cs : List Nat} (hc : Binary cs) :
    evenCharge cs = 0 ↔ cs.reverse = cs := by
  exact halfCharge_zero_iff evenWeight (fun n => Int.le_of_lt (evenWeight_pos n))
    evenWeight_superincreasing hc

theorem carryCharge_zero_iff {cs : List Nat} (hc : Binary cs) :
    carryCharge cs = 0 ↔ cs.reverse = cs := by
  unfold carryCharge
  split
  · exact oddCharge_zero_iff hc
  · exact evenCharge_zero_iff hc

end P196.Agent15.SpectralCarry
