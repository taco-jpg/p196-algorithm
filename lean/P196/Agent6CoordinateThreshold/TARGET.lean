import P196.Agent6CoordinateThreshold.OuterFinite

/-!
Agent #115. UNPROVED TARGET (WIP), kept outside every accepted build.

Written proof: `NOTE.md` in this directory. This file only states, in terms of
the unchanged exact exterior map `P196.Agent7.Finite.outerNext`, that the
successor is determined by the band phase, Agent #110's centered value `Z`, and
the real value `ρ`. `ρ` is compared without rationals:
`ρ(c,B) = rhoNum c B / (9 * 10^|B|)`.

No theorem is claimed here; the proposition is a definition only.
-/

namespace Agent115.ExteriorFactorization

open P196.Agent7.Finite

/-- `Σ_{i<n} B_i 10^i`, outermost coefficient first. -/
def lowValue : List Nat → Nat
  | [] => 0
  | b :: bs => b + 10 * lowValue bs

/-- Agent #110's centered value `9 Σ B_i 10^i − c (10^n − 1)`. -/
def zValue (c : Nat) (B : List Nat) : Int :=
  9 * (lowValue B : Int) - (c : Int) * ((10 : Int) ^ B.length - 1)

/-- `Σ_{i<n} B_i 10^{n-1-i}` (the same coefficients read as a high-first integer). -/
def highValue (B : List Nat) : Nat :=
  B.foldl (fun acc b => 10 * acc + b) 0

/-- Numerator of `ρ(c,B) = (9 Σ_{i<n} B_i 10^{n-1-i} + c) / (9·10^n)`. -/
def rhoNum (c : Nat) (B : List Nat) : Nat := 9 * highValue B + c

def nonneutralPhase (c : Nat) : Prop := c ∈ [2, 4, 6, 8, 10, 12, 14, 16]

/-- The open formal target: equal phase, equal `Z` and equal `ρ` give the same
successor under the exact exterior map. -/
def Target : Prop :=
  ∀ (c : Nat) (B₁ B₂ : List Nat),
    nonneutralPhase c →
    validOuter { c := c, B := B₁ } = true →
    validOuter { c := c, B := B₂ } = true →
    zValue c B₁ = zValue c B₂ →
    rhoNum c B₁ * 10 ^ B₂.length = rhoNum c B₂ * 10 ^ B₁.length →
    outerNext { c := c, B := B₁ } = outerNext { c := c, B := B₂ }

end Agent115.ExteriorFactorization
