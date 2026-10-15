import ExteriorCapTwo

namespace P196.Agent6

@[simp] theorem trim_append_phase (c : Nat) (w : Word) :
    trim c (w ++ [c]) = trim c w := by
  simp [trim, List.reverse_append]

@[simp] theorem trim_phase_pair (c : Nat) : trim c [c,c] = [] := by
  simp [trim]

/-- Structural assumptions on a canonical periodic exterior. -/
def Canonical (s : Exterior) : Prop :=
  0 < s.phase ∧ s.phase ≤ 16 ∧ s.phase % 2 = 0 ∧
  (∀ x ∈ s.word, x ≤ 18) ∧
  (∀ x xs, s.word = x :: xs → 0 < x) ∧
  trim s.phase s.word = s.word

/-- Every canonical cap-two exterior is represented by the checked decoder. -/
theorem capTwo_coverage (s : Exterior) (hs : Canonical s)
    (hlen : s.word.length ≤ 2) :
    ∃ i j z, i < 8 ∧ j < 18 ∧ z < 19 ∧ s = decode 1 i j z := by
  rcases s with ⟨c,w⟩
  rcases hs with ⟨hpos,hmax,heven,hcoeff,hhead,htrim⟩
  dsimp only at hpos hmax heven hcoeff hhead htrim hlen
  have hi : c / 2 - 1 < 8 := by omega
  have hc : 2 * (c / 2 - 1 + 1) = c := by omega
  cases w with
  | nil =>
      refine ⟨c/2-1,c-1,c,hi,by omega,by omega,?_⟩
      have hm : c % 19 = c := Nat.mod_eq_of_lt (by omega)
      simp [decode,digits19,hc,hm,show c-1+1=c by omega]
  | cons x xs =>
      have hxpos : 0 < x := hhead x xs rfl
      have hxmax : x ≤ 18 := hcoeff x (by simp)
      cases xs with
      | nil =>
          refine ⟨c/2-1,x-1,c,hi,by omega,by omega,?_⟩
          have hm : c % 19 = c := Nat.mod_eq_of_lt (by omega)
          simp only [decode,digits19,hc,hm,show x-1+1=x by omega]
          congr 1
          change [x] = trim c ([x] ++ [c])
          rw [trim_append_phase, htrim]
      | cons y ys =>
          have hymax : y ≤ 18 := hcoeff y (by simp)
          have hys : ys = [] := by
            have : ys.length = 0 := by simp only [List.length_cons] at hlen; omega
            exact List.length_eq_zero_iff.mp this
          subst ys
          refine ⟨c/2-1,x-1,y,hi,by omega,by omega,?_⟩
          have hm : y % 19 = y := Nat.mod_eq_of_lt (by omega)
          simp [decode,digits19,hc,hm,show x-1+1=x by omega,htrim]

/-- Unconditional finite certificate for all canonical exteriors of length <=2. -/
theorem capTwo_uniform_escape (s : Exterior) (hs : Canonical s)
    (hlen : s.word.length ≤ 2) :
    ∃ t, t ≤ 7 ∧ 2 < (iterate t s).word.length := by
  obtain ⟨i,j,z,hi,hj,hz,heq⟩ := capTwo_coverage s hs hlen
  subst s
  exact capTwo_escape i j z hi hj hz

/-- There is no seven-transition canonical path entirely inside cap two. -/
theorem capTwo_no_confined_path (s : Exterior) (hs : Canonical s)
    (hpath : ∀ t, t ≤ 7 → (iterate t s).word.length ≤ 2) : False := by
  have hlen : s.word.length ≤ 2 := hpath 0 (by omega)
  obtain ⟨t,ht,he⟩ := capTwo_uniform_escape s hs hlen
  have hb := hpath t ht
  omega

#print axioms trim_append_phase
#print axioms trim_phase_pair
#print axioms capTwo_coverage
#print axioms capTwo_uniform_escape
#print axioms capTwo_no_confined_path
end P196.Agent6
