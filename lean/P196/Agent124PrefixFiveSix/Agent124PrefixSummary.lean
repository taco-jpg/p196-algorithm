import P196.Agent124PrefixFiveSix.A124K5Final
import P196.Agent124PrefixFiveSix.A124K5Final119
import P196.Agent124PrefixFiveSix.A124K6Final

/-! Summary of the 33 three-digit prefix classes of Agent #124.
Each entry `(a, b, c, B)` carries an ancestry bound `B`; every bound is at most 40,
within the kernel-checked first 100 iterates of 196. No P196 claim. -/

namespace Agent124.PrefixSummary
open Lychrel196 Agent124.PrefixK

/-- `(a, b, c, B)`: palindromes beginning `a b c` are reached within `B` steps. -/
def classes : List (Nat × Nat × Nat × Nat) :=
  [(1, 1, 9, 8),
   (2, 1, 3, 23),
   (2, 1, 6, 10),
   (2, 5, 7, 16),
   (2, 7, 6, 31),
   (2, 7, 7, 31),
   (2, 7, 8, 31),
   (3, 4, 8, 16),
   (3, 7, 7, 8),
   (3, 8, 4, 7),
   (3, 8, 5, 8),
   (4, 2, 6, 24),
   (4, 2, 9, 24),
   (4, 7, 4, 7),
   (6, 7, 4, 5),
   (7, 3, 7, 12),
   (7, 5, 5, 12),
   (7, 7, 8, 25),
   (7, 8, 3, 14),
   (7, 8, 4, 14),
   (7, 8, 5, 40),
   (7, 8, 6, 27),
   (7, 8, 7, 25),
   (7, 8, 8, 14),
   (7, 8, 9, 38),
   (8, 5, 6, 38),
   (8, 5, 7, 25),
   (8, 5, 8, 36),
   (8, 5, 9, 36),
   (9, 0, 5, 11),
   (9, 0, 6, 11),
   (9, 2, 3, 7),
   (9, 3, 5, 10)]

theorem classes_length : classes.length = 33 := rfl

/-- Uniform ancestry bounds for every listed class. -/
theorem ancestry_all : ∀ e ∈ classes, ∀ A P t, 0 < A →
    PalStarts3 e.1 e.2.1 e.2.2.1 P → orbit A t = P → t ≤ e.2.2.2 := by
  intro e he
  simp only [classes, List.mem_cons, List.not_mem_nil, or_false] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact Agent124.CertK5.ancestry_119
  · exact Agent124.CertK5.ancestry_213
  · exact Agent124.CertK5.ancestry_216
  · exact Agent124.CertK5.ancestry_257
  · exact Agent124.CertK6.ancestry_276
  · exact Agent124.CertK6.ancestry_277
  · exact Agent124.CertK6.ancestry_278
  · exact Agent124.CertK5.ancestry_348
  · exact Agent124.CertK6.ancestry_377
  · exact Agent124.CertK5.ancestry_384
  · exact Agent124.CertK6.ancestry_385
  · exact Agent124.CertK5.ancestry_426
  · exact Agent124.CertK5.ancestry_429
  · exact Agent124.CertK5.ancestry_474
  · exact Agent124.CertK5.ancestry_674
  · exact Agent124.CertK5.ancestry_737
  · exact Agent124.CertK5.ancestry_755
  · exact Agent124.CertK5.ancestry_778
  · exact Agent124.CertK5.ancestry_783
  · exact Agent124.CertK5.ancestry_784
  · exact Agent124.CertK6.ancestry_785
  · exact Agent124.CertK6.ancestry_786
  · exact Agent124.CertK5.ancestry_787
  · exact Agent124.CertK5.ancestry_788
  · exact Agent124.CertK5.ancestry_789
  · exact Agent124.CertK6.ancestry_856
  · exact Agent124.CertK6.ancestry_857
  · exact Agent124.CertK5.ancestry_858
  · exact Agent124.CertK5.ancestry_859
  · exact Agent124.CertK5.ancestry_905
  · exact Agent124.CertK5.ancestry_906
  · exact Agent124.CertK5.ancestry_923
  · exact Agent124.CertK5.ancestry_935

/-- The ordinary 196 orbit never contains a palindrome of any listed class. -/
theorem no_196_all : ∀ t, ∀ e ∈ classes, ¬ PalStarts3 e.1 e.2.1 e.2.2.1 (orbit 196 t) := by
  intro t e he
  simp only [classes, List.mem_cons, List.not_mem_nil, or_false] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact Agent124.CertK5.no_196_119 t
  · exact Agent124.CertK5.no_196_213 t
  · exact Agent124.CertK5.no_196_216 t
  · exact Agent124.CertK5.no_196_257 t
  · exact Agent124.CertK6.no_196_276 t
  · exact Agent124.CertK6.no_196_277 t
  · exact Agent124.CertK6.no_196_278 t
  · exact Agent124.CertK5.no_196_348 t
  · exact Agent124.CertK6.no_196_377 t
  · exact Agent124.CertK5.no_196_384 t
  · exact Agent124.CertK6.no_196_385 t
  · exact Agent124.CertK5.no_196_426 t
  · exact Agent124.CertK5.no_196_429 t
  · exact Agent124.CertK5.no_196_474 t
  · exact Agent124.CertK5.no_196_674 t
  · exact Agent124.CertK5.no_196_737 t
  · exact Agent124.CertK5.no_196_755 t
  · exact Agent124.CertK5.no_196_778 t
  · exact Agent124.CertK5.no_196_783 t
  · exact Agent124.CertK5.no_196_784 t
  · exact Agent124.CertK6.no_196_785 t
  · exact Agent124.CertK6.no_196_786 t
  · exact Agent124.CertK5.no_196_787 t
  · exact Agent124.CertK5.no_196_788 t
  · exact Agent124.CertK5.no_196_789 t
  · exact Agent124.CertK6.no_196_856 t
  · exact Agent124.CertK6.no_196_857 t
  · exact Agent124.CertK5.no_196_858 t
  · exact Agent124.CertK5.no_196_859 t
  · exact Agent124.CertK5.no_196_905 t
  · exact Agent124.CertK5.no_196_906 t
  · exact Agent124.CertK5.no_196_923 t
  · exact Agent124.CertK5.no_196_935 t

#print axioms classes_length
#print axioms ancestry_all
#print axioms no_196_all
end Agent124.PrefixSummary
