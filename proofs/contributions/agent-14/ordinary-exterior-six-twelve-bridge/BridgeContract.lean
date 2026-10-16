import AlternatingScalarBoundary

/-!
Agent #14 M99-A04 bridge interface.

This module deliberately does not claim the ordinary decimal bridge.
It records the exact abstract witness that must be supplied by that bridge.
-/
namespace Agent14.OrdinaryExteriorBridge

open Agent9.AlternatingScalarBoundary

structure Witness where
  n : Nat
  cols : Nat → Trace
  hroot : cols 0 = constant root
  hsix : cols n = constant six
  htwelve : cols n = constant twelve
  hpath : ∀ i, i < n → Step (cols i) (cols (i+1))

theorem six_consequence (w : Witness) : False :=
  Agent9.AlternatingScalarBoundary.no_six_boundary
    w.n w.cols w.hroot w.hsix w.hpath

theorem twelve_consequence (w : Witness) : False :=
  Agent9.AlternatingScalarBoundary.no_twelve_boundary
    w.n w.cols w.hroot w.htwelve w.hpath

/-
Remaining bridge obligation:

  Given the genuine decimal reverse-and-add orbit/canonical digit data,
  construct Witness with the same Slot/Tile equations as Agent9.

In particular, the proof must establish hroot, the aligned six/twelve tail,
and every adjacent Step in hpath from the actual ordinary decimal update.
Those facts cannot be replaced by a surrogate trace or an assumed equivalence.
-/

end Agent14.OrdinaryExteriorBridge
