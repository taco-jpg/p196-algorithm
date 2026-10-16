import AlternatingScalarBoundary

/-!
Agent #14 M99-A04 bridge contract.

This file intentionally contains only the exact interface that an ordinary
decimal bridge must satisfy. It does not assert that the bridge exists.
No placeholder proof is accepted.
-/
namespace Agent14.OrdinaryExteriorBridge

open Agent9.AlternatingScalarBoundary

/-- A bridge witness supplies the abstract root-to-tail traces for the
genuine ordinary decimal representation. The witness must be proved from
the repository's canonical decimal definitions before it can be used. -/
structure Witness where
  width : Nat
  rootTrace : Trace
  sixTrace : Trace
  twelveTrace : Trace
  root_eq : rootTrace = constant root
  six_eq : sixTrace = constant six
  twelve_eq : twelveTrace = constant twelve
  six_path : ∀ i, i < width → Step (rootTrace) (rootTrace)
  twelve_path : ∀ i, i < width → Step (rootTrace) (rootTrace)

/-- The intended endpoint after the actual decimal-to-Slot bridge is proved.
This is a target, not an accepted theorem. -/
def SixBridgeTarget : Prop :=
  ∀ (w : Witness), Agent9.AlternatingScalarBoundary.no_six_boundary
    w.width (fun _ => w.rootTrace) w.root_eq.symm w.six_eq.symm
    (by intro i hi; simpa [w.root_eq, w.six_eq] using w.six_path i hi)

/-- Twelve analogue of the bridge target. -/
def TwelveBridgeTarget : Prop :=
  ∀ (w : Witness), Agent9.AlternatingScalarBoundary.no_twelve_boundary
    w.width (fun _ => w.rootTrace) w.root_eq.symm w.twelve_eq.symm
    (by intro i hi; simpa [w.root_eq, w.twelve_eq] using w.twelve_path i hi)

end Agent14.OrdinaryExteriorBridge
