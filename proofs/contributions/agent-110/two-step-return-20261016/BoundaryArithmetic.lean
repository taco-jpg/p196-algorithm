import Std

/-!
Agent #110 — research-only arithmetic kernel. UNCOMPILED in this session.
Intended complete proof must additionally import exact P196.Agent6.advance
and show any canonical period-two phase-6 orbit yields a boundaryCandidate.
This source is OUTSIDE every accepted Lean build. No axioms/admissions/unsafe.
-/
namespace Agent110.TwoStepBoundary

def firstLast (mu x a : Nat) : Nat :=
  if mu == 0 then 12 + (x + a) / 10
  else 6 + (x + a) / 10 + x % 10

def firstPenultPossible (mu x a want : Nat) : Bool :=
  if mu == 0 then decide (want = (x + a) % 10 + x % 10)
  else decide ((x + a) % 10 ≤ want ∧ want ≤ (x + a) % 10 + 9)

def secondLast (nu w b : Nat) : Nat :=
  if nu == 0 then 5 + (w + b) / 10
  else 2 + (w + b) / 10 + (w + 1) % 10

def secondPenultPossible (nu w b want : Nat) : Bool :=
  if nu == 0 then decide (want = (w + b) % 10 + (w + 1) % 10)
  else decide ((w + b) % 10 ≤ want ∧ want ≤ (w + b) % 10 + 9)

/-- q = first trim count; 2-q = second trim count; mu/nu overflow bits.
x is original terminal coefficient; w first-step surviving terminal coefficient.
The free reflected digits are allowed their full 0..9 range (overapprox). -/
def boundaryCandidate (q mu nu x a b w : Nat) : Bool :=
  (x != 6) &&
  (let L := firstLast mu x a
   if q == 0 then L != 12 && w == L
   else if q == 1 then
     L == 12 && w != 12 && firstPenultPossible mu x a w
   else
     L == 12 && firstPenultPossible mu x a 12 && w != 12) &&
  (let L := secondLast nu w b
   if q == 0 then L == 6 && secondPenultPossible nu w b 6
   else if q == 1 then L == 6 && secondPenultPossible nu w b x
   else L == x)

/-- Full finite search over necessary terminal-boundary parameters only.
No width cap is encoded, but the missing source-to-boundary theorem matters. -/
def anyBoundaryCandidate : Bool :=
  (List.range 3).any fun q =>
    (List.range 2).any fun mu =>
      (List.range 2).any fun nu =>
        (List.range 19).any fun x =>
          (List.range 2).any fun a =>
            (List.range 2).any fun b =>
              (List.range 19).any fun w =>
                boundaryCandidate q mu nu x a b w

/-- WIP: candidate kernel-reduction check; awaiting official Lean 4.19.0.
Do not label LEAN-CHECKED before compiling under the actual dependency pins. -/
theorem no_abstract_two_step_boundary : anyBoundaryCandidate = false := by
  decide

#print axioms no_abstract_two_step_boundary

/-!
MISSING FORMAL BRIDGES:
1. For canonical phase6 words of length >=2, exact norm/trim and
   the two-step state equality imply q+secondTrim=2.
2. Extract bounded x, w, carry bits a,b and overflow bits mu,nu,
   and prove boundaryCandidate q mu nu x a b w = true.
3. Handle empty and singleton source words by the exact source semantics.
4. Import this self-contained arithmetic result into the ORIGINAL
   ExteriorCore/ExteriorCoverage theorem without weakening Canonical.
-/
end Agent110.TwoStepBoundary
