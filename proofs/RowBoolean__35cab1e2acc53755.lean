import FastRowsBase

namespace SevenColumn.Certificate

/-- A boolean traversal avoids constructing a nested decidability proof for
every row during kernel reduction. The whole block remains checked. -/
def checkRowsBlock (tree : RankTree) (pred : Word → List Word) : RankTree → Bool
  | .empty => true
  | .node _ p r left right =>
    checkRowsBlock tree pred left && checkRow tree pred p r && checkRowsBlock tree pred right

theorem checkRowsBlock_sound {tree block : RankTree} {pred : Word → List Word}
    (h : checkRowsBlock tree pred block = true) :
    block.All (fun p r => checkRow tree pred p r = true) := by
  induction block with
  | empty => trivial
  | node k p r left right ihl ihr =>
    simp only [checkRowsBlock, Bool.and_eq_true] at h
    exact ⟨ihl h.1.1, h.1.2, ihr h.2⟩

#print axioms checkRowsBlock_sound
end SevenColumn.Certificate
