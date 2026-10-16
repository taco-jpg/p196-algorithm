import NoAlternatingReturn
import ArithmeticBridge

/-!
Agent #415: exact translation from the five-component temporal-strip relation
into the existing inverse-column arithmetic, not a new model of reverse-add.
The compressed fourth coordinate is `delayed + 1 - highOdd` in Nat.
The carry bound proves this subtraction never truncates a negative integer.
-/
namespace Agent415.InverseColumn
open P196.Agent4.TemporalStrip BoundaryCertificate

/-- The existing 88-letter encoding of a valid actual/abstract temporal cut. -/
def encode {J : Type} (s : Cut J) (j : J) : Nat :=
  ((s.lowEven j * 2 + s.lowOdd j) * 2 + s.highEven j) * 11 +
    (s.delayed j + 1 - s.highOdd j)

/-- Read an existing inverse option from the outer cut and the two pair sums. -/
def inverseOption {J : Type} (s : Cut J) (x y : J → Nat) (j : J) : Opt :=
  ⟨x j, s.lowEven j, s.lowOdd j, s.highEven j, s.highOdd j, y j⟩

/-- Compression retains all three encoded carries and the exact shifted digit. -/
theorem encode_components {J : Type} (s : Cut J) (hs : Valid s) (j : J) :
    encode s j < 88 ∧
    encode s j / 44 = s.lowEven j ∧
    encode s j / 22 % 2 = s.lowOdd j ∧
    encode s j / 11 % 2 = s.highEven j ∧
    encode s j % 11 = s.delayed j + 1 - s.highOdd j := by
  obtain ⟨ha, hb, hc, he, hz⟩ := hs j
  unfold encode
  omega

/-- Exact nonnegative shifted-digit identity; no clipping case is omitted. -/
theorem shifted_digit (r d e z : Nat) (hd : d ≤ 1)
    (he : e = (r+d)/10) (hz : z = (r+d)%10) :
    r+1 = z+1-d+10*e := by omega

theorem forced_high_carry (r d e : Nat) (hr : r ≤ 18) (hd : d ≤ 1)
    (he : e = (r+d)/10) :
    (¬ r < 9 ∨ e = 0) ∧ (¬ r > 9 ∨ e = 1) := by omega

/-- Every local inverse-fiber equation follows from the exact strip equations. -/
theorem column_permitted {J : Type} (next : J → J) (s t : Cut J)
    (x y : J → Nat) (hs : Valid s) (ht : Valid t)
    (hc : Column next s t x y) (j : J) :
    permitted (encode t j) (inverseOption s x y j) = true := by
  obtain ⟨hsa, hsb, hsc, hse, hsz⟩ := hs j
  obtain ⟨hta, htb, htc, hte, htz⟩ := ht j
  obtain ⟨hb, ha, hbb, hcc, hz⟩ := encode_components t ht j
  obtain ⟨hx, hy, hla, hlb, hrc, hre, hdel, hxy, hyx⟩ := hc j
  dsimp [permitted, inverseOption]
  simp only [Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true,
    decide_eq_true_eq, decide_eq_false_iff_not, beq_iff_eq]
  have hshift := shifted_digit (y j) (t.highOdd j) (s.highOdd j) (t.delayed j) hte hre hdel
  have hreset := forced_high_carry (y j) (t.highOdd j) (s.highOdd j) hy hte hre
  have hsc2 : (x j + t.highEven j) / 10 ≤ 1 := by simpa only [← hrc] using hsc
  simp only [ha, hbb, hcc, hz, hb, hx, hsa, hsb, hsc, hsc2, hse, hy,
    hla.symm, hxy.symm, hlb.symm, hrc, true_and, and_true]
  exact ⟨⟨hshift, by simpa using hreset.1⟩, by simpa using hreset.2⟩

/-- The cross-time output equation follows without a chosen inverse witness. -/
theorem column_output {J : Type} (next : J → J) (s t : Cut J)
    (x y : J → Nat) (hs : Valid s) (hc : Column next s t x y) (j : J) :
    outputOf (inverseOption s x y j) (inverseOption s x y (next j)) =
      some (encode s j) := by
  obtain ⟨ha, hb, hcarr, he, hz⟩ := hs j
  obtain ⟨hx, hy, hla, hlb, hrc, hre, hdel, hxy, hyx⟩ := hc j
  unfold outputOf
  dsimp only [inverseOption]
  split
  · split
    · simp only [Option.some.injEq]
      unfold encode
      omega
    · rename_i h
      simp at h
      omega
  · rename_i h
    simp at h
    omega

end Agent415.InverseColumn
#print axioms Agent415.InverseColumn.encode_components
#print axioms Agent415.InverseColumn.column_permitted
#print axioms Agent415.InverseColumn.column_output
