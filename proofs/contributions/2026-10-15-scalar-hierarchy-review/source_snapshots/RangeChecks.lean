import RankRows
namespace ScalarFinite

theorem checked_range (P : Nat → Prop) (start count : Nat)
    (h : ∀ i : Fin count, P (start+i.val)) :
    ∀ u, start ≤ u → u < start+count → P u := by
  intro u hlo hhi
  have hi : u-start < count := by omega
  have he : start+(u-start)=u := by omega
  simpa only [he] using h ⟨u-start,hi⟩

theorem join_ranges (P : Nat → Prop) (lo middle hi : Nat)
    (left : ∀ u, lo ≤ u → u < middle → P u)
    (right : ∀ u, middle ≤ u → u < hi → P u) :
    ∀ u, lo ≤ u → u < hi → P u := by
  intro u hlo hhi
  by_cases hm : u < middle
  · exact left u hlo hm
  · exact right u (by omega) hhi

end ScalarFinite
