import Agent1PeriodicOuterCatalog

/-!
Local rank and label facts for the exact original outer graph. Component labels
are the preserved partition indices; this file proves neither SCC maximality
nor reachability. Closed checks are split by the original 59 source phases.
-/

set_option maxRecDepth 16384
set_option maxHeartbeats 16000000

namespace Agent1.Periodic
open Agent8

/-- Original partition labels on catalog nodes, with a total default off catalog. -/
def outerComponent (s : OuterNode) : Nat :=
  match s.1 with
  | [0,0,0,0] => 131
  | [9,9,9,9] => 129
  | [18,18,18,18] => 130
  | [1,1,17,17] => match s.2 with
    | 7 => 57
    | 8 => 58
    | 12 => 66
    | _ => 8
  | [1,17,17,1] => match s.2 with
    | 7 => 41
    | 8 => 42
    | 12 => 50
    | _ => 8
  | [2,9,16,9] => match s.2 with
    | 3 => 51
    | _ => 8
  | [3,3,15,15] => match s.2 with
    | 14 => 100
    | 15 => 106
    | 16 => 59
    | 17 => 60
    | _ => 8
  | [3,15,15,3] => match s.2 with
    | 14 => 87
    | 15 => 93
    | 16 => 43
    | 17 => 44
    | _ => 8
  | [4,4,14,14] => match s.2 with
    | 1 => 90
    | 2 => 92
    | 3 => 96
    | 4 => 98
    | 5 => 54
    | 6 => 56
    | 7 => 47
    | 8 => 49
    | _ => 8
  | [4,9,14,9] => match s.2 with
    | 10 => 115
    | 11 => 116
    | 12 => 119
    | 13 => 120
    | 14 => 23
    | 15 => 24
    | 16 => 18
    | 17 => 19
    | _ => 8
  | [4,14,14,4] => match s.2 with
    | 1 => 77
    | 2 => 79
    | 3 => 83
    | 4 => 85
    | 5 => 38
    | 6 => 40
    | 7 => 31
    | 8 => 33
    | _ => 8
  | [6,9,12,9] => match s.2 with
    | 5 => 88
    | 6 => 94
    | 7 => 52
    | 8 => 45
    | _ => 8
  | [7,7,11,11] => match s.2 with
    | 7 => 73
    | 8 => 10
    | _ => 8
  | [7,11,11,7] => match s.2 with
    | 7 => 112
    | 8 => 11
    | _ => 8
  | [9,2,9,16] => match s.2 with
    | 3 => 67
    | _ => 8
  | [9,4,9,14] => match s.2 with
    | 10 => 76
    | 11 => 78
    | 12 => 82
    | 13 => 84
    | 14 => 37
    | 15 => 39
    | 16 => 30
    | 17 => 32
    | _ => 8
  | [9,6,9,12] => match s.2 with
    | 5 => 101
    | 6 => 107
    | 7 => 68
    | 8 => 61
    | _ => 8
  | [9,12,9,6] => match s.2 with
    | 5 => 75
    | 6 => 81
    | 7 => 36
    | 8 => 29
    | _ => 8
  | [9,14,9,4] => match s.2 with
    | 10 => 102
    | 11 => 104
    | 12 => 108
    | 13 => 110
    | 14 => 69
    | 15 => 71
    | 16 => 62
    | 17 => 64
    | _ => 8
  | [9,16,9,2] => match s.2 with
    | 3 => 35
    | _ => 8
  | [11,7,7,11] => match s.2 with
    | 7 => 86
    | 8 => 9
    | _ => 8
  | [11,11,7,7] => match s.2 with
    | 7 => 99
    | 8 => 12
    | _ => 8
  | [12,9,6,9] => match s.2 with
    | 5 => 114
    | 6 => 118
    | 7 => 22
    | 8 => 17
    | _ => 8
  | [14,4,4,14] => match s.2 with
    | 1 => 103
    | 2 => 105
    | 3 => 109
    | 4 => 111
    | 5 => 70
    | 6 => 72
    | 7 => 63
    | 8 => 65
    | _ => 8
  | [14,9,4,9] => match s.2 with
    | 10 => 89
    | 11 => 91
    | 12 => 95
    | 13 => 97
    | 14 => 53
    | 15 => 55
    | 16 => 46
    | 17 => 48
    | _ => 8
  | [14,14,4,4] => match s.2 with
    | 1 => 128
    | 2 => 127
    | 3 => 126
    | 4 => 125
    | 5 => 124
    | 6 => 123
    | 7 => 122
    | 8 => 121
    | 11 => 7
    | 12 => 6
    | 13 => 5
    | 14 => 4
    | 15 => 3
    | 16 => 2
    | 17 => 1
    | 18 => 0
    | _ => 8
  | [15,3,3,15] => match s.2 with
    | 14 => 113
    | 15 => 117
    | 16 => 15
    | 17 => 16
    | _ => 8
  | [15,15,3,3] => match s.2 with
    | 14 => 74
    | 15 => 80
    | 16 => 27
    | 17 => 28
    | _ => 8
  | [16,9,2,9] => match s.2 with
    | 3 => 21
    | _ => 8
  | [17,1,1,17] => match s.2 with
    | 7 => 13
    | 8 => 14
    | 12 => 20
    | _ => 8
  | [17,17,1,1] => match s.2 with
    | 7 => 25
    | 8 => 26
    | 12 => 34
    | _ => 8
  | _ => 8

/-- Reverse the stored indices; saturation makes the rank positive everywhere. -/
def componentRank (c : Nat) : Nat := 132 - min c 131

theorem componentRank_pos (c : Nat) : 0 < componentRank c := by
  have h := Nat.min_le_right c 131
  unfold componentRank
  omega

private def edgeRankCheck (e : OuterEdge) : Bool :=
  decide (componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source) ∧
    (outerComponent e.source ≠ outerComponent e.target →
      1 + componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source)) ∧
    (outerComponent e.source = outerComponent e.target →
      outerComponent e.source ∈ [8,129,130,131]))

private def nodeLabelCheck (s : OuterNode) : Bool :=
  decide ((outerComponent s = 131 → s.1 = [0,0,0,0]) ∧
    (s.1 = [14,14,4,4] → outerComponent s ∈ [8,129,130] → s.2 = 9 ∨ s.2 = 10))

/- Structural list assembly follows the existing private catalog checker;
   no graph-theoretic soundness principle is introduced here. -/
private inductive RankBlocksAll {α : Type} (f : α → Bool) : List (List α) → Prop
  | nil : RankBlocksAll f []
  | cons {n ns} (hn : n.all f = true) (hs : RankBlocksAll f ns) :
      RankBlocksAll f (n :: ns)

private theorem RankBlocksAll.flatten {α : Type} {f : α → Bool}
    {ns : List (List α)} (h : RankBlocksAll f ns) : ns.flatten.all f = true := by
  induction h with
  | nil => rfl
  | cons hn hs ih => simp only [List.flatten_cons, List.all_append, hn, ih, Bool.and_self]

private def rankNodes00 : List OuterNode := [
  ([0,0,0,0],1),
  ([0,0,0,0],2),
  ([0,0,0,0],3),
  ([0,0,0,0],4),
  ([0,0,0,0],5),
  ([0,0,0,0],6),
  ([0,0,0,0],7),
  ([0,0,0,0],8),
  ([0,0,0,0],9),
  ([0,0,0,0],10),
  ([0,0,0,0],11),
  ([0,0,0,0],12),
  ([0,0,0,0],13),
  ([0,0,0,0],14),
  ([0,0,0,0],15),
  ([0,0,0,0],16),
  ([0,0,0,0],17),
  ([0,0,0,0],18)
]

private def rankEdges00 : List OuterEdge := [
  ⟨([0,0,0,0],1), 0, none, ([0,0,0,0],2)⟩,
  ⟨([0,0,0,0],1), 0, none, ([0,0,0,0],3)⟩,
  ⟨([0,0,0,0],2), 0, none, ([0,0,0,0],4)⟩,
  ⟨([0,0,0,0],2), 0, none, ([0,0,0,0],5)⟩,
  ⟨([0,0,0,0],3), 0, none, ([0,0,0,0],6)⟩,
  ⟨([0,0,0,0],3), 0, none, ([0,0,0,0],7)⟩,
  ⟨([0,0,0,0],4), 0, none, ([0,0,0,0],8)⟩,
  ⟨([0,0,0,0],4), 0, none, ([0,0,0,0],9)⟩,
  ⟨([0,0,0,0],5), 0, none, ([0,0,0,0],10)⟩,
  ⟨([0,0,0,0],5), 0, none, ([0,0,0,0],11)⟩,
  ⟨([0,0,0,0],6), 0, none, ([0,0,0,0],12)⟩,
  ⟨([0,0,0,0],6), 0, none, ([0,0,0,0],13)⟩,
  ⟨([0,0,0,0],7), 0, none, ([0,0,0,0],14)⟩,
  ⟨([0,0,0,0],7), 0, none, ([0,0,0,0],15)⟩,
  ⟨([0,0,0,0],8), 0, none, ([0,0,0,0],16)⟩,
  ⟨([0,0,0,0],8), 0, none, ([0,0,0,0],17)⟩,
  ⟨([0,0,0,0],9), 0, none, ([0,0,0,0],18)⟩,
  ⟨([0,0,0,0],9), 1, none, ([0,0,0,0],10)⟩,
  ⟨([0,0,0,0],10), 1, none, ([0,0,0,0],1)⟩,
  ⟨([0,0,0,0],11), 1, none, ([0,0,0,0],2)⟩,
  ⟨([0,0,0,0],12), 1, none, ([0,0,0,0],3)⟩,
  ⟨([0,0,0,0],13), 1, none, ([0,0,0,0],4)⟩,
  ⟨([0,0,0,0],14), 1, none, ([0,0,0,0],5)⟩,
  ⟨([0,0,0,0],15), 1, none, ([0,0,0,0],6)⟩,
  ⟨([0,0,0,0],16), 1, none, ([0,0,0,0],7)⟩,
  ⟨([0,0,0,0],17), 1, none, ([0,0,0,0],8)⟩,
  ⟨([0,0,0,0],18), 1, none, ([0,0,0,0],9)⟩
]

private theorem nodeCheck00 : rankNodes00.all nodeLabelCheck = true := by decide

private theorem edgeCheck00 : rankEdges00.all edgeRankCheck = true := by decide

private def rankNodes04 : List OuterNode := [
  ([1,1,17,17],2),
  ([1,1,17,17],3),
  ([1,1,17,17],4),
  ([1,1,17,17],5),
  ([1,1,17,17],6),
  ([1,1,17,17],7),
  ([1,1,17,17],8),
  ([1,1,17,17],9),
  ([1,1,17,17],10),
  ([1,1,17,17],11),
  ([1,1,17,17],12),
  ([1,1,17,17],13),
  ([1,1,17,17],14),
  ([1,1,17,17],15),
  ([1,1,17,17],16),
  ([1,1,17,17],17),
  ([1,1,17,17],18)
]

private def rankEdges04 : List OuterEdge := [
  ⟨([1,1,17,17],2), 0, none, ([3,3,15,15],4)⟩,
  ⟨([1,1,17,17],2), 0, none, ([3,3,15,15],5)⟩,
  ⟨([1,1,17,17],3), 0, none, ([3,3,15,15],6)⟩,
  ⟨([1,1,17,17],3), 0, none, ([3,3,15,15],7)⟩,
  ⟨([1,1,17,17],4), 0, none, ([3,3,15,15],8)⟩,
  ⟨([1,1,17,17],4), 0, none, ([3,3,15,15],9)⟩,
  ⟨([1,1,17,17],5), 0, none, ([3,3,15,15],10)⟩,
  ⟨([1,1,17,17],5), 0, none, ([3,3,15,15],11)⟩,
  ⟨([1,1,17,17],6), 0, none, ([3,3,15,15],12)⟩,
  ⟨([1,1,17,17],6), 0, none, ([3,3,15,15],13)⟩,
  ⟨([1,1,17,17],7), 0, none, ([3,3,15,15],14)⟩,
  ⟨([1,1,17,17],7), 0, none, ([3,3,15,15],15)⟩,
  ⟨([1,1,17,17],8), 0, none, ([3,3,15,15],16)⟩,
  ⟨([1,1,17,17],8), 0, none, ([3,3,15,15],17)⟩,
  ⟨([1,1,17,17],9), 0, none, ([3,3,15,15],18)⟩,
  ⟨([1,1,17,17],9), 1, none, ([9,2,9,16],10)⟩,
  ⟨([1,1,17,17],10), 1, none, ([9,2,9,16],1)⟩,
  ⟨([1,1,17,17],11), 1, none, ([9,2,9,16],2)⟩,
  ⟨([1,1,17,17],12), 1, none, ([9,2,9,16],3)⟩,
  ⟨([1,1,17,17],13), 1, none, ([9,2,9,16],4)⟩,
  ⟨([1,1,17,17],14), 1, none, ([9,2,9,16],5)⟩,
  ⟨([1,1,17,17],15), 1, none, ([9,2,9,16],6)⟩,
  ⟨([1,1,17,17],16), 1, none, ([9,2,9,16],7)⟩,
  ⟨([1,1,17,17],17), 1, none, ([9,2,9,16],8)⟩,
  ⟨([1,1,17,17],18), 1, none, ([9,2,9,16],9)⟩
]

private theorem nodeCheck04 : rankNodes04.all nodeLabelCheck = true := by decide

private theorem edgeCheck04 : rankEdges04.all edgeRankCheck = true := by decide


end Agent1.Periodic
