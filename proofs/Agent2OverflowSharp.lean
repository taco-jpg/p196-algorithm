import PeriodObstructions

/-!
Agent #2: the explicit sharp overflow family.
The target and all source words use the existing Agent8 normalization.
This module is a component of the overflow-fiber proof, not an all-time
palindrome-avoidance result.
-/

namespace P196.Agent2.OverflowFibers

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

def bitCoefficient (b : Bool) : Nat := if b then 14 else 5

def binaryWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 =>
      (binaryWords n).map (false :: ·) ++
      (binaryWords n).map (true :: ·)

def sharpWord (odd : Bool) (bs : List Bool) : List Nat :=
  14 :: (bs.map bitCoefficient ++ (if odd then [14] else []) ++
    (bs.map bitCoefficient).reverse ++ [14])

/-- Input width is n+2; the overflow target has width n+3. -/
def sharpTarget (n : Nat) : List Nat :=
  5 :: (List.replicate (n + 1) 10 ++ [5])

theorem bitCoefficient_injective (a b : Bool)
    (h : bitCoefficient a = bitCoefficient b) : a = b := by
  cases a <;> cases b <;> simp_all [bitCoefficient]

theorem bitCoefficient_values (b : Bool) :
    bitCoefficient b = 5 ∨ bitCoefficient b = 14 := by
  cases b <;> simp [bitCoefficient]

theorem binaryWords_length (n : Nat) :
    (binaryWords n).length = 2 ^ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [binaryWords, ih, Nat.pow_succ, Nat.mul_two]

theorem binaryWords_member_length (n : Nat) (bs : List Bool)
    (h : bs ∈ binaryWords n) : bs.length = n := by
  induction n generalizing bs with
  | zero => simp [binaryWords] at h; simp [h]
  | succ n ih =>
      simp only [binaryWords, List.mem_append, List.mem_map] at h
      rcases h with ⟨xs, hx, rfl⟩ | ⟨xs, hx, rfl⟩ <;>
        simp [ih xs hx]

theorem binaryWords_nodup (n : Nat) : (binaryWords n).Nodup := by
  induction n with
  | zero => simp [binaryWords]
  | succ n ih =>
      rw [binaryWords]
      apply List.pairwise_append.mpr
      refine ⟨?_, ?_, ?_⟩
      · exact List.Pairwise.map _ (fun _ _ h he => h (List.cons.inj he).2) ih
      · exact List.Pairwise.map _ (fun _ _ h he => h (List.cons.inj he).2) ih
      · intro xs hx ys hy he
        simp only [List.mem_map] at hx hy
        rcases hx with ⟨a, ha, rfl⟩
        rcases hy with ⟨b, hb, rfl⟩
        cases he

theorem sharpWord_length (odd : Bool) (bs : List Bool) :
    (sharpWord odd bs).length = 2 * bs.length + 2 + (if odd then 1 else 0) := by
  cases odd <;> simp [sharpWord] <;> omega

theorem sharpWord_symmetric (odd : Bool) (bs : List Bool) :
    (sharpWord odd bs).reverse = sharpWord odd bs := by
  cases odd <;> simp [sharpWord, List.reverse_append, List.reverse_cons,
    List.append_assoc]

theorem sharpWord_positive (odd : Bool) (bs : List Bool) :
    0 < (sharpWord odd bs).headD 0 := by simp [sharpWord]

theorem sharpWord_coefficients (odd : Bool) (bs : List Bool) :
    ∀ x ∈ sharpWord odd bs, x = 5 ∨ x = 14 := by
  intro x hx
  have hmap : ∀ z ∈ bs.map bitCoefficient, z = 5 ∨ z = 14 := by
    intro z hz
    rcases List.mem_map.mp hz with ⟨b, hb, rfl⟩
    exact bitCoefficient_values b
  cases odd <;> simp only [sharpWord, Bool.false_eq_true, ↓reduceIte,
    Bool.true_eq, List.mem_cons, List.mem_append, List.mem_reverse,
    List.mem_singleton, List.not_mem_nil, or_false] at hx
  · rcases hx with rfl | ((hx | hx) | hx)
    · exact Or.inr rfl
    · exact hmap x hx
    · exact hmap x hx
    · exact Or.inr hx
  · rcases hx with rfl | (((hx | hx) | hx) | hx)
    · exact Or.inr rfl
    · exact hmap x hx
    · exact Or.inr hx
    · exact hmap x hx
    · exact Or.inr hx

theorem sharpWord_prefix (odd : Bool) (bs : List Bool) :
    ((sharpWord odd bs).drop 1).take bs.length = bs.map bitCoefficient := by
  simp [sharpWord, List.take_append]

theorem sharpWord_injective (odd : Bool) (a b : List Bool)
    (h : sharpWord odd a = sharpWord odd b) : a = b := by
  have hl := congrArg List.length h
  rw [sharpWord_length, sharpWord_length] at hl
  have hab : a.length = b.length := by omega
  have hh := congrArg (fun q : List Nat => (q.drop 1).take a.length) h
  dsimp only at hh
  rw [sharpWord_prefix, hab, sharpWord_prefix] at hh
  clear h hl hab
  induction a generalizing b with
  | nil => cases b <;> simp_all
  | cons x xs ih =>
      cases b with
      | nil => simp at hh
      | cons y ys =>
          simp only [List.map_cons, List.cons.injEq] at hh
          have hxy := bitCoefficient_injective x y hh.1
          subst y
          exact congrArg (List.cons x) (ih ys hh.2)

def sharpFamily (odd : Bool) (n : Nat) : List (List Nat) :=
  (binaryWords n).map (sharpWord odd)

theorem sharpFamily_length (odd : Bool) (n : Nat) :
    (sharpFamily odd n).length = 2 ^ n := by
  simp [sharpFamily, binaryWords_length]

theorem sharpFamily_nodup (odd : Bool) (n : Nat) :
    (sharpFamily odd n).Nodup := by
  exact List.Pairwise.map _ (fun _ _ h he => h (sharpWord_injective odd _ _ he))
    (binaryWords_nodup n)

theorem normalize_tens_one (n : Nat) (xs : List Nat) :
    Agent8.normalize (List.replicate n 10 ++ xs) 1 =
      List.replicate n 1 ++ Agent8.normalize xs 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, Agent8.normalize, ih]

theorem sharpTarget_normalize (n : Nat) :
    Agent8.normalize (sharpTarget n) 0 =
      5 :: 0 :: (List.replicate n 1 ++ [6]) := by
  simp [sharpTarget, List.replicate_succ, Agent8.normalize, normalize_tens_one]

theorem sharpTarget_not_palindrome (n : Nat) :
    Agent8.normalize (sharpTarget n) 0 ≠
      (Agent8.normalize (sharpTarget n) 0).reverse := by
  rw [sharpTarget_normalize]
  intro h
  have hh := congrArg (fun xs : List Nat => xs.headD 0) h
  simp [List.reverse_cons, List.reverse_append] at hh

#print axioms binaryWords_nodup
#print axioms sharpWord_injective
#print axioms sharpFamily_length
#print axioms sharpFamily_nodup
#print axioms sharpTarget_normalize
#print axioms sharpTarget_not_palindrome

end P196.Agent2.OverflowFibers
