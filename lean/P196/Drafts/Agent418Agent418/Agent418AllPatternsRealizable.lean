import P196.Drafts.Agent418Agent418.Agent418FiniteDecimalWitness

/-! Every four-bit odd-input schedule has an actual twelve-digit decimal
seed realizing the prescribed eight-step prefix cycle. This is a finite
block-realizability theorem, not a common-seed or all-time statement. -/
namespace Agent418.AllPatternsRealizable
open Agent418.SaturatedInputAudit Agent418.FiniteDecimalWitness
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

def candidate (p : Fin 16) : Nat :=
  match p.val with
  | 0 => 899763872030
  | 1 => 899993350030
  | 2 => 899858472030
  | 3 => 899550185030
  | 4 => 899489987030
  | 5 => 899443538030
  | 6 => 899692526030
  | 7 => 899539858030
  | 8 => 899876418030
  | 9 => 899653698030
  | 10 => 899749708030
  | 11 => 899787998030
  | 12 => 899719019030
  | 13 => 899956567030
  | 14 => 899831249030
  | _ => 899991788030

def patternInput (p : Fin 16) (i : Nat) : Nat :=
  match i with
  | 0 => 1
  | 1 => p.val / 8 % 2
  | 2 => 0
  | 3 => p.val / 4 % 2
  | 4 => 0
  | 5 => p.val / 2 % 2
  | 6 => 1
  | _ => p.val % 2

def width (i : Nat) : Nat := 12 + i / 2

def observedInput (n i : Nat) : Nat :=
  carry (pairDigit (orbit n i) (width i)) (width i - 3)

def observedOverflow (n i : Nat) : Nat :=
  carry (pairDigit (orbit n i) (width i)) (width i)

/-- Exact finite certificate for every candidate and every orbit index. -/
theorem all_canonical_widths : ∀ p : Fin 16, ∀ i : Fin 9,
    10^(width i.val-1) ≤ orbit (candidate p) i.val ∧
      orbit (candidate p) i.val < 10^(width i.val) := by decide +kernel

theorem all_observations : ∀ p : Fin 16, ∀ i : Fin 8,
    prefixOf (orbit (candidate p) i.val) (width i.val) = cycleState i.val ∧
      observedInput (candidate p) i.val = patternInput p i.val ∧
      observedOverflow (candidate p) i.val = i.val % 2 := by decide +kernel

theorem all_endpoints : ∀ p : Fin 16,
    prefixOf (orbit (candidate p) 8) 16 = cycleState 0 := by decide +kernel

theorem all_saturated : ∀ p : Fin 16,
    2 * total (observedOverflow (candidate p)) 8 = 8 := by decide +kernel

def Realizes (n : Nat) (p : Fin 16) : Prop :=
  (∀ i : Fin 9, 10^(width i.val-1) ≤ orbit n i.val ∧
    orbit n i.val < 10^(width i.val)) ∧
  (∀ i : Fin 8,
    prefixOf (orbit n i.val) (width i.val) = cycleState i.val ∧
      observedInput n i.val = patternInput p i.val ∧
      observedOverflow n i.val = i.val % 2) ∧
  prefixOf (orbit n 8) 16 = cycleState 0 ∧
  2 * total (observedOverflow n) 8 = 8

/-- In particular, saturation imposes no restriction on the four odd
controls of an isolated actual eight-step block. -/
theorem every_pattern_has_finite_decimal_seed (p : Fin 16) :
    ∃ n : Nat, Realizes n p :=
  ⟨candidate p, all_canonical_widths p, all_observations p,
    all_endpoints p, all_saturated p⟩

#print axioms all_canonical_widths
#print axioms all_observations
#print axioms all_endpoints
#print axioms all_saturated
#print axioms every_pattern_has_finite_decimal_seed
end Agent418.AllPatternsRealizable
