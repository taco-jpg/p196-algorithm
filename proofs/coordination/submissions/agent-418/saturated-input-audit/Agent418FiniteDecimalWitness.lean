import Agent418ArbitraryOddControls

/-! Finite ordinary-decimal witness to the false odd-input-balance assumption.
The reverseFuel/reverse10/step/orbit definitions are unchanged from the
repository's Lychrel196 namespace, read at source commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5,
LychrelDigitSums.lean Git blob 8a865176625283648a8a20dd2411ed77670eb0a2.
Namespace relocation only. The eight-step witness does not establish an
infinite decimal orbit following the abstract cycle.
-/
namespace Agent418.FiniteDecimalWitness
open Agent418.SaturatedInputAudit

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

def reverseFuel : Nat → Nat → Nat → Nat
  | 0, _, acc => acc
  | fuel + 1, n, acc =>
      if n = 0 then acc else reverseFuel fuel (n / 10) (10 * acc + n % 10)

def reverse10 (n : Nat) : Nat := reverseFuel n n 0
def step (n : Nat) : Nat := n + reverse10 n
def orbit (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => step (orbit n k)

def seed : Nat := 899559344030

def valueAt : Nat → Nat
  | 0 => 899559344030
  | 1 => 930003300028
  | 2 => 1750006600067
  | 3 => 9350072600638
  | 4 => 17710135301177
  | 5 => 94820488402948
  | 6 => 179740976805797
  | 7 => 977249655853768
  | _ => 1844608212796547

def widthAt : Nat → Nat
  | 0 | 1 => 12
  | 2 | 3 => 13
  | 4 | 5 => 14
  | 6 | 7 => 15
  | _ => 16

def digit (n i : Nat) : Nat := n / 10^i % 10

def pairDigit (n L i : Nat) : Nat := digit n i + digit n (L-1-i)

def prefixOf (n L : Nat) : Prefix :=
  ⟨pairDigit n L 0, pairDigit n L 1, pairDigit n L 2⟩

def carry (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i+1 => (q i + carry q i) / 10

def inputAt (i : Nat) : Nat :=
  carry (pairDigit (valueAt i) (widthAt i)) (widthAt i - 3)

def overflowAt (i : Nat) : Nat :=
  carry (pairDigit (valueAt i) (widthAt i)) (widthAt i)

/-- Exact ordinary reverse-add values, including the endpoint at time eight. -/
theorem witness_chain : ∀ i : Fin 9,
    orbit seed i.val = valueAt i.val := by decide +kernel

/-- No leading-zero width is smuggled into the concrete interpretation. -/
theorem witness_canonical_widths : ∀ i : Fin 9,
    10^(widthAt i.val-1) ≤ valueAt i.val ∧
      valueAt i.val < 10^(widthAt i.val) := by decide +kernel

/-- Every full concrete observation has the claimed prefix, input and output. -/
theorem witness_observations : ∀ i : Fin 8,
    prefixOf (valueAt i.val) (widthAt i.val) = cycleState i.val ∧
      inputAt i.val = skeletonInput 0 0 0 0 i.val ∧
      overflowAt i.val = i.val % 2 := by decide +kernel

theorem witness_endpoint :
    prefixOf (orbit seed 8) 16 = cycleState 0 := by decide +kernel

/-- Output saturation does not force odd-input balance even in this finite
    actual-decimal orbit, not merely in an unconstrained abstract path. -/
theorem concrete_balance_counterexample :
    2 * total overflowAt 8 = 8 ∧
      inputAt 1 + inputAt 3 + inputAt 5 + inputAt 7 ≠ 2 := by decide +kernel

#print axioms witness_chain
#print axioms witness_canonical_widths
#print axioms witness_observations
#print axioms witness_endpoint
#print axioms concrete_balance_counterexample

end Agent418.FiniteDecimalWitness
