import PrefixCertificate

/-!
Boolean reflection of `RankTree.All` for certificate row checks (Agent #124).
`allRowsB tree pred sub` checks every node of the subtree `sub` against the
complete executable inverse `pred` and the whole tree `tree`; its soundness
lemma converts a kernel-evaluated `true` into the propositional row premise.
-/

namespace Agent124.CertCheck

open SevenColumn.Certificate

def allRowsB (tree : RankTree) (pred : Word → List Word) : RankTree → Bool
  | .empty => true
  | .node _ p r left right =>
      allRowsB tree pred left && checkRow tree pred p r && allRowsB tree pred right

theorem allRowsB_sound {tree : RankTree} {pred : Word → List Word} :
    ∀ {sub : RankTree}, allRowsB tree pred sub = true →
      sub.All (fun p r => checkRow tree pred p r = true)
  | .empty, _ => trivial
  | .node _ p r left right, h => by
      simp only [allRowsB, Bool.and_eq_true] at h
      exact ⟨allRowsB_sound h.1.1, h.1.2, allRowsB_sound h.2⟩

end Agent124.CertCheck

#print axioms Agent124.CertCheck.allRowsB_sound
