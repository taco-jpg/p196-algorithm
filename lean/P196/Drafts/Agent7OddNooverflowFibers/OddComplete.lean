import P196.Drafts.Agent7OddNooverflowFibers.OddSharp
import P196.Drafts.Agent7OddNooverflowFibers.OddOutputRange

/-!
An explicit decoder and equality-guarded enumerator for arbitrary output
words. Failed encodings produce the empty list. The actual-output range
theorem proves completeness for every requested output, including targets
outside the encoded range. All source-word conditions remain literal.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

def decodeSymbol (x : Nat) : Symbol := ⟨x % 19, Nat.mod_lt _ (by decide)⟩

theorem decodeSymbol_val (s : Symbol) : decodeSymbol s.val = s := by
  apply Fin.ext
  exact Nat.mod_eq_of_lt s.isLt

def targetHalf (m : Nat) (r : List Nat) : List Symbol :=
  (r.take m).map decodeSymbol

def targetCenter (m : Nat) (r : List Nat) : Fin 10 :=
  ⟨(r[m]?.getD 0 / 2) % 10, Nat.mod_lt _ (by decide)⟩

theorem targetHalf_encoded (ss : List Symbol) (v : Fin 10) :
    targetHalf ss.length (oddMirror (ss.map Fin.val) (2*v.val)) = ss := by
  simp [targetHalf, oddMirror, List.take_append, List.map_map, Function.comp_def, decodeSymbol_val]

theorem targetCenter_encoded (ss : List Symbol) (v : Fin 10) :
    targetCenter ss.length (oddMirror (ss.map Fin.val) (2*v.val)) = v := by
  have hmid : (oddMirror (ss.map Fin.val) (2*v.val))[ss.length]? = some (2*v.val) := by
    simpa only [oddMirror, List.length_map] using odd_word_center (ss.map Fin.val) (2*v.val)
  apply Fin.ext
  change ((oddMirror (ss.map Fin.val) (2*v.val))[ss.length]?.getD 0 / 2) % 10 = v.val
  rw [hmid]
  simp only [Option.getD_some]
  have hdiv : 2*v.val/2 = v.val := by omega
  rw [hdiv, Nat.mod_eq_of_lt v.isLt]

/-- The original literal domain with a completely arbitrary output word. -/
def CompleteOddFiber (m : Nat) (r q : List Nat) : Prop :=
  q.length = 2*m+1 ∧ q.reverse = q ∧
  (∀ x ∈ q, x < 19) ∧ 0 < q.headD 0 ∧
  (q[m]?.getD 0) % 2 = 0 ∧ (scan q 0).2 = 0 ∧ Agent8.stepWord q = r

def universalOddPreimages (m : Nat) (r : List Nat) : List (List Nat) :=
  let ss := targetHalf m r
  let v := targetCenter m r
  if ss.length = m ∧ oddMirror (ss.map Fin.val) (2*v.val) = r then
    fullOddPreimages ss v
  else []

theorem universalOddPreimages_encoded (m : Nat) (ss : List Symbol) (v : Fin 10)
    (hlen : ss.length = m) :
    universalOddPreimages m (oddMirror (ss.map Fin.val) (2*v.val)) =
      fullOddPreimages ss v := by
  subst m
  simp [universalOddPreimages, targetHalf_encoded, targetCenter_encoded]

theorem universalOddPreimages_nodup (m : Nat) (r : List Nat) :
    (universalOddPreimages m r).Nodup := by
  dsimp only [universalOddPreimages]
  split
  · exact fullOddPreimages_nodup _ _
  · exact List.nodup_nil

/-- Membership is exactly the full original fiber for an arbitrary target,
not just for targets already presented in half/center form. -/
theorem universalOddPreimages_membership (m : Nat) (r q : List Nat) :
    q ∈ universalOddPreimages m r ↔ CompleteOddFiber m r q := by
  dsimp only [universalOddPreimages]
  split
  · rename_i h
    rw [fullOddPreimages_membership]
    simp only [CanonicalOddFiber, CompleteOddFiber, h.1, h.2]
  · rename_i hbad
    simp only [List.not_mem_nil, false_iff]
    intro hf
    obtain ⟨hlen, _, _, _, _, hc, hstep⟩ := hf
    obtain ⟨ss, v, hs, hout⟩ := odd_nooverflow_output_range q m hlen hc
    have hr : r = oddMirror (ss.map Fin.val) (2*v.val) := hstep.symm.trans hout
    apply hbad
    rw [hr, ← hs, targetHalf_encoded, targetCenter_encoded]
    exact ⟨rfl, rfl⟩

theorem universalOddPreimages_bound (m : Nat) (r : List Nat) :
    (universalOddPreimages m r).length ≤ oddMax m := by
  dsimp only [universalOddPreimages]
  split
  · rename_i h
    simpa only [h.1] using fullOddPreimages_bound (targetHalf m r) (targetCenter m r)
  · exact Nat.zero_le _

theorem universal_sharp_family (m : Nat) :
    universalOddPreimages m
      (oddMirror ((sharpTargetHalf m).map Fin.val) (2*(sharpCenter m).val)) =
      sharpFamily m := by
  exact universalOddPreimages_encoded m _ _ (sharpTargetHalf_length m)

theorem universal_odd_fiber_maximum (m : Nat) :
    (∀ r : List Nat, (universalOddPreimages m r).length ≤ (fib (m+1)+1)/2) ∧
    (∃ r : List Nat, (universalOddPreimages m r).length = (fib (m+1)+1)/2) := by
  refine ⟨universalOddPreimages_bound m, ?_⟩
  refine ⟨oddMirror ((sharpTargetHalf m).map Fin.val) (2*(sharpCenter m).val), ?_⟩
  rw [universal_sharp_family]
  exact sharpFamily_length m

/-- Complete theorem: exact duplicate-free enumeration of every literal
canonical fiber, a uniform sharp bound, and an attained maximum for every
odd width. This counts coefficient words, not individual digit splittings. -/
theorem complete_odd_fiber_theorem (m : Nat) :
    (∀ r : List Nat,
      (universalOddPreimages m r).Nodup ∧
      (∀ q, q ∈ universalOddPreimages m r ↔ CompleteOddFiber m r q) ∧
      (universalOddPreimages m r).length ≤ (fib (m+1)+1)/2) ∧
    (∃ r : List Nat, (universalOddPreimages m r).length = (fib (m+1)+1)/2) := by
  refine ⟨?_, (universal_odd_fiber_maximum m).2⟩
  intro r
  exact ⟨universalOddPreimages_nodup m r,
    universalOddPreimages_membership m r, universalOddPreimages_bound m r⟩

theorem universal_width_one_zero : universalOddPreimages 0 [0] = [] := by decide

theorem universal_width_one_six : universalOddPreimages 0 [12] = [[6]] := by decide

theorem universal_wrong_parity : universalOddPreimages 1 [11,1,11] = [] := by decide

#print axioms decodeSymbol_val
#print axioms targetHalf_encoded
#print axioms targetCenter_encoded
#print axioms universalOddPreimages_encoded
#print axioms universalOddPreimages_nodup
#print axioms universalOddPreimages_membership
#print axioms universalOddPreimages_bound
#print axioms universal_sharp_family
#print axioms universal_odd_fiber_maximum
#print axioms complete_odd_fiber_theorem
#print axioms universal_width_one_zero
#print axioms universal_width_one_six
#print axioms universal_wrong_parity

end P196.Agent7.OddFibers
