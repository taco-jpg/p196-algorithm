import P196.EightCarryMaximalWidth.CertificateTools

/-!
Candidate cover for the remaining bounded fourth-smoothing branch.
The earlier result supplies the complete five-column cover. New workers
check every bounded extension and then exclude this six-column cover.
-/

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

/-- A cover for six-column survivors with difference (0,0,1,-3,5,-7). -/
def minusSevenSextuples : List Pair := [
  ([18, 7, 7, 2, 9, 0], [18, 7, 6, 5, 4, 7]),
  ([18, 7, 7, 2, 18, 0], [18, 7, 6, 5, 13, 7]),
  ([18, 7, 7, 2, 18, 9], [18, 7, 6, 5, 13, 16]),
  ([18, 7, 7, 11, 18, 0], [18, 7, 6, 14, 13, 7]),
  ([18, 7, 7, 11, 18, 9], [18, 7, 6, 14, 13, 16]),
  ([18, 7, 16, 2, 9, 0], [18, 7, 15, 5, 4, 7]),
  ([18, 7, 16, 2, 18, 0], [18, 7, 15, 5, 13, 7]),
  ([18, 7, 16, 2, 18, 9], [18, 7, 15, 5, 13, 16]),
  ([18, 7, 16, 11, 18, 0], [18, 7, 15, 14, 13, 7]),
  ([18, 7, 16, 11, 18, 9], [18, 7, 15, 14, 13, 16]),
  ([18, 16, 7, 2, 9, 0], [18, 16, 6, 5, 4, 7]),
  ([18, 16, 7, 2, 18, 0], [18, 16, 6, 5, 13, 7]),
  ([18, 16, 7, 2, 18, 9], [18, 16, 6, 5, 13, 16]),
  ([18, 16, 7, 11, 18, 0], [18, 16, 6, 14, 13, 7]),
  ([18, 16, 7, 11, 18, 9], [18, 16, 6, 14, 13, 16]),
  ([18, 16, 16, 2, 9, 0], [18, 16, 15, 5, 4, 7]),
  ([18, 16, 16, 2, 18, 0], [18, 16, 15, 5, 13, 7]),
  ([18, 16, 16, 2, 18, 9], [18, 16, 15, 5, 13, 16]),
  ([18, 16, 16, 11, 18, 0], [18, 16, 15, 14, 13, 7]),
  ([18, 16, 16, 11, 18, 9], [18, 16, 15, 14, 13, 16])
]

/-- A larger finite coefficient type may be used to certify a smaller
enumeration. Cases outside the enumerated range impose no obligation. -/
theorem extensions_cover_of_upper_fin
    (lo ro count bound : Nat) (hcount : count ≤ bound)
    (ps allowed : List Pair)
    (h : ∀ p, p ∈ ps → ∀ a : Fin bound, a.val < count →
      (allowed.contains (p.1 ++ [a.val + lo], p.2 ++ [a.val + ro]) ||
        !accepted (p.1 ++ [a.val + lo], p.2 ++ [a.val + ro])) = true) :
    covered (extensions lo ro count ps) allowed = true := by
  apply extensions_cover_of_points
  intro p hp a
  exact h p hp ⟨a.val, Nat.lt_of_lt_of_le a.isLt hcount⟩ a.isLt

#print axioms extensions_cover_of_upper_fin

end EightCarryThreePairSharp.Candidates
