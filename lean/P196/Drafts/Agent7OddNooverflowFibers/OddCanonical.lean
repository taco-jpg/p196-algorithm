import P196.Drafts.Agent7OddNooverflowFibers.OddActual
import P196.Drafts.Agent7OddNooverflowFibers.OddWords

/-!
The complete canonical coefficient-word domain for odd no-overflow fibers.
The middle coefficient is tested at the literal central list position.
Positive outer coefficient is checked on the full word, including width one.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

theorem oddMirror_head (xs : List Nat) (z : Nat) :
    (oddMirror xs z).headD 0 = xs.headD z := by
  cases xs <;> rfl

def canonicalOddPreimages (ss : List Symbol) (v : Fin 10) :
    List (List Nat × Nat) :=
  (oddPreimages ss v 0).filter (fun w => decide (0 < w.1.headD w.2))

theorem canonicalOdd_membership (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) :
    (xs,z) ∈ canonicalOddPreimages ss v ↔
      OddActualFiber ss v xs z ∧ 0 < xs.headD z := by
  simp [canonicalOddPreimages, mem_oddPreimages, oddPath_iff_actual]

theorem canonicalOdd_nodup (ss : List Symbol) (v : Fin 10) :
    (canonicalOddPreimages ss v).Nodup :=
  List.Pairwise.filter _ (oddPreimages_nodup ss v 0)

def fullOddPreimages (ss : List Symbol) (v : Fin 10) : List (List Nat) :=
  (canonicalOddPreimages ss v).map (fun w => oddMirror w.1 w.2)

theorem fullOddPreimages_nodup (ss : List Symbol) (v : Fin 10) :
    (fullOddPreimages ss v).Nodup := by
  apply List.Pairwise.map (fun w => oddMirror w.1 w.2) _ (canonicalOdd_nodup ss v)
  intro a b hab he
  apply hab
  have hh := oddMirror_injective a.1 b.1 a.2 b.2 he
  exact Prod.ext hh.1 hh.2

theorem fullOddPreimages_membership_encoded (ss : List Symbol) (v : Fin 10)
    (q : List Nat) :
    q ∈ fullOddPreimages ss v ↔ ∃ xs z,
      OddActualFiber ss v xs z ∧ 0 < xs.headD z ∧ oddMirror xs z = q := by
  constructor
  · intro h
    obtain ⟨⟨xs,z⟩, hw, he⟩ := List.mem_map.mp h
    obtain ⟨hf,hp⟩ := (canonicalOdd_membership ss v xs z).mp hw
    exact ⟨xs,z,hf,hp,he⟩
  · rintro ⟨xs,z,hf,hp,he⟩
    exact List.mem_map.mpr ⟨(xs,z),(canonicalOdd_membership ss v xs z).mpr ⟨hf,hp⟩,he⟩

/-- A literal complete-word predicate, without a presupposed half encoding. -/
def CanonicalOddFiber (ss : List Symbol) (v : Fin 10) (q : List Nat) : Prop :=
  q.length = 2*ss.length+1 ∧ q.reverse = q ∧
  (∀ x ∈ q, x < 19) ∧ 0 < q.headD 0 ∧
  (q[ss.length]?.getD 0) % 2 = 0 ∧
  (scan q 0).2 = 0 ∧
  Agent8.stepWord q = oddMirror (ss.map Fin.val) (2*v.val)

theorem canonicalOdd_of_encoding (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) (hf : OddActualFiber ss v xs z)
    (hp : 0 < xs.headD z) : CanonicalOddFiber ss v (oddMirror xs z) := by
  obtain ⟨hlen,hb,hzb,hze,hc,ht⟩ := hf
  refine ⟨by simp [hlen], oddMirror_reverse xs z, ?_, ?_, ?_, hc, ht⟩
  · intro x hx
    simp only [oddMirror, List.mem_append, List.mem_reverse, List.mem_singleton] at hx
    rcases hx with (hx | rfl) | hx
    · exact hb x hx
    · exact hzb
    · exact hb x hx
  · change 0 < (oddMirror xs z).headD 0
    rw [oddMirror_head]
    exact hp
  · rw [← hlen]
    simpa [oddMirror, odd_word_center] using hze

theorem canonicalOdd_has_encoding (ss : List Symbol) (v : Fin 10)
    (q : List Nat) (hf : CanonicalOddFiber ss v q) :
    ∃ xs z, OddActualFiber ss v xs z ∧ 0 < xs.headD z ∧ oddMirror xs z = q := by
  obtain ⟨hlen,hsym,hb,hp,hz,hc,ht⟩ := hf
  obtain ⟨xs,z,hxs,hq⟩ := symmetric_odd_decomposition q ss.length hlen hsym
  have he : q = oddMirror xs z := hq
  subst q
  have hxb : ∀ x ∈ xs, x < 19 := by
    intro x hx
    exact hb x (by simp [oddMirror, hx])
  have hzb : z < 19 := hb z (by simp [oddMirror])
  have hze : z % 2 = 0 := by
    rw [← hxs] at hz
    simpa [oddMirror, odd_word_center] using hz
  refine ⟨xs,z,⟨hxs,hxb,hzb,hze,hc,ht⟩,?_,rfl⟩
  simpa [oddMirror_head] using hp

/-- The enumerator is exactly the entire canonical odd no-overflow fiber.
Every symmetric word of the prescribed odd length is covered. -/
theorem fullOddPreimages_membership (ss : List Symbol) (v : Fin 10)
    (q : List Nat) : q ∈ fullOddPreimages ss v ↔ CanonicalOddFiber ss v q := by
  rw [fullOddPreimages_membership_encoded]
  constructor
  · rintro ⟨xs,z,hf,hp,rfl⟩
    exact canonicalOdd_of_encoding ss v xs z hf hp
  · exact canonicalOdd_has_encoding ss v q

theorem width_one_witness : fullOddPreimages [] 2 = [[2]] := by decide

#print axioms oddMirror_head
#print axioms canonicalOdd_membership
#print axioms canonicalOdd_nodup
#print axioms fullOddPreimages_nodup
#print axioms fullOddPreimages_membership_encoded
#print axioms canonicalOdd_of_encoding
#print axioms canonicalOdd_has_encoding
#print axioms fullOddPreimages_membership
#print axioms width_one_witness

end P196.Agent7.OddFibers
