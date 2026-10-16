import Std

/-!
Agent #414. Exact representation bridge for the historical boundary certificate.
The literals below are taken from BoundaryData.graph0 and BoundaryDataK.graph0K
at p196-algorithm commit 9de08d78db6526e2ce2dd66cedd5e63f600424bd.
This file does not assert any new exterior obstruction or decimal-orbit result.
-/
namespace Agent414BoundaryTranscription

set_option maxRecDepth 10000
set_option maxHeartbeats 5000000

/-- The actual initial-graph table has the literal transcription claimed by
Agent #109. The proof uses the equations of Lean's original string parser. -/
theorem graph0_parseNats_eq :
    ("4176 16785439 33566782 50348057 67129400 83886087 100692024 117473305 134254654 151035935 167817296 184573959".splitOn " ").filterMap String.toNat? =
      [4176, 16785439, 33566782, 50348057, 67129400, 83886087,
       100692024, 117473305, 134254654, 151035935, 167817296, 184573959] := by
  simp +decide [String.splitOn, String.splitOnAux,
    String.toNat?, String.isNat, String.all, String.any, String.anyAux,
    String.foldl, String.foldlAux]

/-- Decoding the exact same entries preserves equality, for the original
edge decoder as well as any other decoder. No injectivity is required. -/
theorem graph0_decode_eq {α : Type} (decode : Nat → α) :
    (("4176 16785439 33566782 50348057 67129400 83886087 100692024 117473305 134254654 151035935 167817296 184573959".splitOn " ").filterMap String.toNat?).map decode =
      ([4176, 16785439, 33566782, 50348057, 67129400, 83886087,
        100692024, 117473305, 134254654, 151035935, 167817296, 184573959] : List Nat).map decode :=
  congrArg (List.map decode) graph0_parseNats_eq

#print axioms graph0_parseNats_eq
#print axioms graph0_decode_eq
end Agent414BoundaryTranscription
