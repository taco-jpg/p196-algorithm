import Agent15ActualFourthColumn

/-! Agent #418: sixty-four concrete ordinary-decimal two-block realizations.
All arithmetic uses the original Lychrel196 and DecimalDigits definitions.
The eight-state table is the same table in Agent215's saturated-cycle profile.
No exhaustive exclusion or infinite continuation is asserted here. -/
namespace Agent418.TwoBlockWitnesses
open DecimalDigits Agent15.ActualFourthColumn P196.Agent4.Saturation
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

def cycleState (i : Nat) : Prefix :=
  match i % 8 with
  | 0 => ⟨8,12,9⟩
  | 1 => ⟨17,5,0⟩
  | 2 => ⟨8,13,5⟩
  | 3 => ⟨17,6,11⟩
  | 4 => ⟨8,14,8⟩
  | 5 => ⟨17,8,17⟩
  | 6 => ⟨8,16,16⟩
  | _ => ⟨17,13,14⟩

def seed (p : Fin 64) : Nat :=
  ([899570584030,899298207030,899687763030,899440875030,899544564030,8998535214961030,8998880782531030,899538735030,899305367030,899304567030,899491876030,899462546030,899483396030,899549165030,899992941030,899595255030,899701704030,899453327030,899868803030,8999175193702030,899408777030,899807033030,899489987030,8994777855157030,899682516030,899767815030,8995016917347030,899579257030,899988693030,899572067030,899465978030,899740306030,899459719030,899970604030,8994505051629030,899813118030,899597329030,899641868030,899679948030,899827747030,899806207030,899811837030,899938336030,899807737030,899756698030,899799538030,899843287030,89979145641141959302965382535714162735873085278030,899789098030,899960376030,89982176525241329000434419461522815777175776308030,8998205198408030,899998937030,899743299030,8998472413198030,899878109030,899964618030,899804929030,899816429030,899960288030,899895479030,899939298030,899999338030,89988865628515749030] : List Nat).getD p.val 0

def initialWidth (p : Fin 64) : Nat :=
  ([12,12,12,12,12,16,16,12,12,12,12,12,12,12,12,12,12,12,12,16,12,12,12,16,12,12,16,12,12,12,12,12,12,12,16,12,12,12,12,12,12,12,12,12,12,12,12,50,12,12,50,16,12,12,16,12,12,12,12,12,12,12,12,20] : List Nat).getD p.val 0

def patternCode (p : Fin 64) : Nat :=
  ([0,1,2,3,4,6,7,17,18,19,32,33,34,35,38,39,48,49,50,51,53,54,66,67,81,82,83,96,97,98,99,112,113,114,115,128,145,146,147,160,161,162,163,166,176,177,178,179,181,182,194,195,209,210,211,224,225,226,227,231,240,241,242,243] : List Nat).getD p.val 0

def width (w i : Nat) : Nat := w + i / 2

def digit (n i : Nat) : Nat := n / 10^i % 10

def digitsAt (n i : Nat) : Nat → Nat := digit (Lychrel196.orbit n i)

def pairsAt (n w i : Nat) : Nat → Nat := columnSum (digitsAt n i) (width w i)

def inputAt (n w i : Nat) : Nat := carry (pairsAt n w i) (width w i - 3)

def overflowAt (n w i : Nat) : Nat := carry (pairsAt n w i) (width w i)

/-- Actual finite positional sums and nonzero leading digits, including both endpoints. -/
theorem all_value_lead : ∀ p : Fin 64, ∀ i : Fin 17,
    0 < width (initialWidth p) i.val ∧
    0 < digitsAt (seed p) i.val (width (initialWidth p) i.val - 1) ∧
    value (digitsAt (seed p) i.val) (width (initialWidth p) i.val) =
      Lychrel196.orbit (seed p) i.val := by decide +kernel

/-- Digit bounds are universal, not a finite-width assumption. -/
theorem digit_le_nine (n i : Nat) : digit n i ≤ 9 := by
  unfold digit
  omega

theorem all_canonical (p : Fin 64) (i : Fin 17) :
    Canonical (Lychrel196.orbit (seed p) i.val) (digitsAt (seed p) i.val)
      (width (initialWidth p) i.val) := by
  have h := all_value_lead p i
  exact ⟨h.1, fun j _ => digit_le_nine _ j, h.2.1, h.2.2⟩

theorem all_prefixes : ∀ p : Fin 64, ∀ i : Fin 17,
    (projectQuad (pairsAt (seed p) (initialWidth p) i.val)).p =
      cycleState i.val := by decide +kernel

theorem all_odd_inputs : ∀ p : Fin 64, ∀ j : Fin 8,
    inputAt (seed p) (initialWidth p) (2*j.val+1) =
      (patternCode p / 2^(7-j.val)) % 2 := by decide +kernel

theorem all_overflows : ∀ p : Fin 64, ∀ i : Fin 16,
    overflowAt (seed p) (initialWidth p) i.val = i.val % 2 := by decide +kernel

theorem all_positive : ∀ p : Fin 64, 0 < seed p := by decide +kernel

theorem codes_injective : ∀ p q : Fin 64, patternCode p = patternCode q → p = q := by
  decide +kernel

def Realizes (n w code : Nat) : Prop :=
  0 < n ∧
  (∀ i : Fin 17, Canonical (Lychrel196.orbit n i.val) (digitsAt n i.val) (width w i.val)) ∧
  (∀ i : Fin 17, (projectQuad (pairsAt n w i.val)).p = cycleState i.val) ∧
  (∀ j : Fin 8, inputAt n w (2*j.val+1) = (code / 2^(7-j.val)) % 2) ∧
  (∀ i : Fin 16, overflowAt n w i.val = i.val % 2)

/-- Every listed distinct code has a finite positive ordinary-decimal witness.
This conclusion is exactly sixteen steps, not an all-time realization. -/
theorem every_listed_pattern_realized (p : Fin 64) :
    ∃ n w, Realizes n w (patternCode p) :=
  ⟨seed p, initialWidth p, all_positive p, all_canonical p,
    all_prefixes p, all_odd_inputs p, all_overflows p⟩

#print axioms all_value_lead
#print axioms digit_le_nine
#print axioms all_canonical
#print axioms all_prefixes
#print axioms all_odd_inputs
#print axioms all_overflows
#print axioms all_positive
#print axioms codes_injective
#print axioms every_listed_pattern_realized
end Agent418.TwoBlockWitnesses
