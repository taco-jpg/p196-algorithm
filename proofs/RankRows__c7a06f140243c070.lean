import FiniteGraph

namespace ScalarFinite

structure Ranking where
  component : Nat → Nat
  cyclic : Nat → Bool
  weight : Nat → Nat
  rank : Nat → Nat
  bound : Nat

def VertexRow (R : Ranking) (u : Nat) : Prop :=
  R.weight (R.component u) ≤ R.rank (R.component u) ∧
  R.rank (R.component u) ≤ R.bound

def EdgeRow (D : Data) (R : Ranking) (u bit : Nat) : Prop :=
  let code := D.next u bit
  let v := code-1
  code ≠ 0 → v < D.size →
    (R.component u = R.component v → R.cyclic (R.component u) = true) ∧
    (R.component u ≠ R.component v →
      R.weight (R.component u)+R.rank (R.component v) ≤ R.rank (R.component u))

structure CheckedRank (D : Data) (R : Ranking) : Prop where
  vertices : ∀ u, u < D.size → VertexRow R u
  edges : ∀ u, u < D.size → ∀ bit, bit ≤ 1 → EdgeRow D R u bit

theorem checked_vertex_bounds {D : Data} {R : Ranking} (h : CheckedRank D R)
    (u : Nat) (hu : (graph D).valid u) :
    R.weight (R.component u) ≤ R.rank (R.component u) ∧
    R.rank (R.component u) ≤ R.bound := h.vertices u hu

theorem checked_edge_bounds {D : Data} {R : Ranking} (h : CheckedRank D R)
    (u v bit : Nat) (hu : (graph D).valid u) (hv : (graph D).valid v)
    (he : (graph D).edge u v bit) :
    (R.cyclic (R.component u) = false → R.component u ≠ R.component v) ∧
    (R.component u ≠ R.component v →
      R.weight (R.component u)+R.rank (R.component v) ≤ R.rank (R.component u)) := by
  have hr := h.edges u hu bit he.1
  unfold EdgeRow at hr
  simp only [he.2,Nat.add_sub_cancel] at hr
  have hh := hr (by omega) hv
  refine ⟨?_,hh.2⟩
  intro hf heq
  have ht := hh.1 heq
  rw [hf] at ht
  contradiction

end ScalarFinite
